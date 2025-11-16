import threading
import concurrent.futures
from urllib.parse import urljoin, urlparse
import csv
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from playwright.sync_api import sync_playwright

def create_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0 Safari/537.36"
        )
    })
    return session


def get_rendered_html_js(url: str, timeout_ms: int = 30000) -> str:
    """
    Use Playwright (Chromium) to fully render JS-heavy pages (React, Next.js, etc.)
    and return the final HTML.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=timeout_ms)
        html = page.content()
        browser.close()
    return html


def get_raw_html(url: str, session: requests.Session, timeout: int = 20) -> str:
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def is_http_url(href: str) -> bool:
    if not href:
        return False
    href = href.strip()

    if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return False

    parsed = urlparse(href)
    if parsed.scheme in ("http", "https"):
        return True
    if parsed.scheme == "":
        return True
    return False


def extract_links(html: str, base_url: str):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    raw_count = 0

    for a in soup.find_all("a", href=True):
        raw_href = a.get("href")
        raw_count += 1
        if not is_http_url(raw_href):
            continue
        abs_url = urljoin(base_url, raw_href)
        links.add(abs_url)
    return sorted(links), raw_count


def check_link(url: str, timeout: int = 10):
    """
    Returns (url, is_broken, info_string).
    is_broken: True if HTTP status >= 400 or request fails.
    info_string: status or error message.
    """
    session = create_session()
    try:
        try:
            resp = session.head(url, allow_redirects=True, timeout=timeout)
            code = resp.status_code
            if code >= 400:
                return url, True, f"HTTP {code} (HEAD)"
            if code in (405, 403):
                raise requests.RequestException(f"HEAD not reliable: {code}")
            return url, False, f"HTTP {code} (HEAD)"
        except requests.RequestException:
            resp = session.get(url, allow_redirects=True, timeout=timeout)
            code = resp.status_code
            if code >= 400:
                return url, True, f"HTTP {code} (GET)"
            return url, False, f"HTTP {code} (GET)"
    except requests.RequestException as e:
        return url, True, f"Error: {e}"

class LinkCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Broken Link Checker (JS-compatible)")
        self.root.geometry("1000x650")

        self.session = create_session()
        self.results = [] 

        self.build_ui()

    def build_ui(self):
        # dark mode thing
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        dark_bg = "#1e1e1e"
        dark_fg = "#ffffff"
        tree_bg = "#252526"

        self.root.configure(bg=dark_bg)
        style.configure("TLabel", background=dark_bg, foreground=dark_fg)
        style.configure("TFrame", background=dark_bg)
        style.configure("TButton", padding=5)
        style.configure(
            "Treeview",
            background=tree_bg,
            fieldbackground=tree_bg,
            foreground=dark_fg,
            bordercolor=dark_bg,
        )
        style.map(
            "Treeview",
            background=[("selected", "#094771")],
            foreground=[("selected", "#ffffff")],
        )

        # controls frame
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="Page URL:").grid(row=0, column=0, sticky=tk.W)

        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(control_frame, textvariable=self.url_var, width=80)
        self.url_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        self.use_js_var = tk.BooleanVar(value=True)
        self.use_js_check = ttk.Checkbutton(
            control_frame,
            text="Use JS rendering (Playwright) for React/Next.js",
            variable=self.use_js_var,
        )
        self.use_js_check.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        self.start_button = ttk.Button(control_frame, text="Check Links", command=self.on_start)
        self.start_button.grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)

        # filter / export / clipboard buttons
        self.filter_button = ttk.Button(control_frame, text="Show Broken Only", command=self.show_broken_only)
        self.filter_button.grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)

        self.show_all_button = ttk.Button(control_frame, text="Show All", command=self.show_all)
        self.show_all_button.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)

        self.export_button = ttk.Button(control_frame, text="Export Broken to CSV", command=self.export_broken_to_csv)
        self.export_button.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)

        self.copy_button = ttk.Button(control_frame, text="Copy Broken to Clipboard", command=self.copy_broken_to_clipboard)
        self.copy_button.grid(row=0, column=4, padx=5, pady=2, sticky=tk.W)

        # progress and summary
        progress_frame = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        progress_frame.pack(fill=tk.X)
        style = ttk.Style()
        style.configure(
            "green.Horizontal.TProgressbar",
            troughcolor="white",
            background="green"
        )

        self.progress_var = tk.DoubleVar(value=0)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style="green.Horizontal.TProgressbar",
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.pack(anchor=tk.W, pady=(5, 0))


        # result table
        columns = ("url", "status", "broken")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("url", text="URL")
        self.tree.heading("status", text="Status")
        self.tree.heading("broken", text="Broken?")

        self.tree.column("url", width=600, anchor=tk.W)
        self.tree.column("status", width=230, anchor=tk.W)
        self.tree.column("broken", width=80, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # srollbar
        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        # highlight style for broken rows
        self.tree.tag_configure("broken", background="#5a1a1a", foreground="#ffcccc")

        # enable column sorting
        self._sort_state = {}
        for col in columns:
            self.tree.heading(col, text=self.tree.heading(col, "text"),
                              command=lambda c=col: self.sort_by_column(c))
          

    ## event handlers and helpers

    def on_start(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return

        # clear prev results
        self.tree.delete(*self.tree.get_children())
        self.results = []

        self.progress_var.set(0)
        self.status_var.set("Starting...")

        self.start_button.config(state=tk.DISABLED)

        use_js = self.use_js_var.get()

        worker_thread = threading.Thread(target=self.run_check, args=(url, use_js), daemon=True)
        worker_thread.start()

    def run_check(self, url: str, use_js: bool):
        try:
            self.update_status("Fetching page HTML...")
            if use_js:
                html = get_rendered_html_js(url)
            else:
                html = get_raw_html(url, self.session)

            links, raw_count = extract_links(html, url)
            total_links = len(links)

            if total_links == 0:
                self.update_status(f"No checkable links found (raw <a> tags: {raw_count}).")
                self.enable_start_button()
                return

            self.update_status(f"Found {total_links} checkable links (raw <a> tags: {raw_count}). Checking...")
            results = []

            # multithreaded checking
            max_workers = min(20, max(4, total_links // 2))
            completed = 0

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_url = {executor.submit(check_link, link): link for link in links}
                for future in concurrent.futures.as_completed(future_to_url):
                    url_res, is_broken, info = future.result()
                    results.append((url_res, is_broken, info))
                    completed += 1
                    progress = (completed / total_links) * 100
                    self.update_progress(progress)
                    self.update_status(f"Checking links... {completed}/{total_links}")

            self.root.after(0, lambda: self.display_results(results))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.enable_start_button()

    def display_results(self, results):
        self.results = results[:] 

        self.populate_tree(self.results)

        broken_count = sum(1 for _, is_broken, _ in self.results if is_broken)
        total = len(self.results)

        self.status_var.set(f"Done. Checked {total} link(s). Broken: {broken_count}.")
        self.progress_var.set(100)
        self.enable_start_button()

        # sound effect
        self.root.bell()

    def populate_tree(self, results_subset):
        self.tree.delete(*self.tree.get_children())
        for url_res, is_broken, info in sorted(results_subset, key=lambda x: x[0]):
            broken_text = "Yes" if is_broken else "No"
            row_id = self.tree.insert("", tk.END, values=(url_res, info, broken_text))
            if is_broken:
                self.tree.item(row_id, tags=("broken",))

    def show_broken_only(self):
        if not self.results:
            return
        broken_only = [r for r in self.results if r[1]]
        self.populate_tree(broken_only)
        self.status_var.set(f"Showing broken links only ({len(broken_only)}/{len(self.results)}).")

    def show_all(self):
        if not self.results:
            return
        self.populate_tree(self.results)
        broken_count = sum(1 for _, b, _ in self.results if b)
        self.status_var.set(f"Showing all links. Total: {len(self.results)}, broken: {broken_count}.")

    def export_broken_to_csv(self):
        if not self.results:
            messagebox.showinfo("Info", "No results to export.")
            return
        broken = [r for r in self.results if r[1]]
        if not broken:
            messagebox.showinfo("Info", "No broken links to export.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Broken Links",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["URL", "Status"])
                for url_res, _, info in broken:
                    writer.writerow([url_res, info])
            messagebox.showinfo("Success", f"Exported {len(broken)} broken link(s) to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV:\n{e}")

    def copy_broken_to_clipboard(self):
        if not self.results:
            messagebox.showinfo("Info", "No results to copy.")
            return
        broken = [r for r in self.results if r[1]]
        if not broken:
            messagebox.showinfo("Info", "No broken links to copy.")
            return

        text = "\n".join(url for url, _, _ in broken)
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Success", f"Copied {len(broken)} broken link(s) to clipboard.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard:\n{e}")

    def sort_by_column(self, col):
        reverse = self._sort_state.get(col, False)
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            data.sort(key=lambda t: float(self._safe_num(t[0])), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower() if isinstance(t[0], str) else t[0], reverse=reverse)

        for index, (_, k) in enumerate(data):
            self.tree.move(k, "", index)

        self._sort_state[col] = not reverse

    @staticmethod
    def _safe_num(value):
        s = "".join(ch for ch in str(value) if (ch.isdigit() or ch == "."))
        if not s:
            raise ValueError
        return s

    def update_status(self, text: str):
        self.root.after(0, lambda: self.status_var.set(text))

    def update_progress(self, value: float):
        self.root.after(0, lambda: self.progress_var.set(value))

    def enable_start_button(self):
        self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))


def main():
    root = tk.Tk()
    app = LinkCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()