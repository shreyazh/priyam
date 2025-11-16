import os
import sys
import tempfile
import uuid
import json
import time
import webbrowser
import re
import platform
from functools import partial

# --- UI toolkits ---
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog, font, ttk

try:
    import customtkinter as ctk
except Exception:
    ctk = None  # We'll gracefully fall back to Tk/ttk if CustomTkinter isn't available

# =======================
# Config
# =======================
APP_NAME = "Texter: Open-Source Text Editor"
AUTOSAVE_INTERVAL_MS = 30_000  # autosave every 30 seconds
AUTOSAVE_PREFIX = "advanced_text_editor_autosave_"
AUTOSAVE_META_EXT = ".meta.json"

SUPPORTED_ENCODINGS = [
    "utf-8",
    "utf-8-sig",
    "utf-16",
    "utf-16-le",
    "utf-16-be",
    "latin-1",
    "cp1252",
]

HEADING_SIZES = {
    "Normal": 0,
    "H1": 26,
    "H2": 22,
    "H3": 20,
    "H4": 18,
    "H5": 16,
    "H6": 14,
    "H7": 13,
}

FONT_SIZE_OPTIONS = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 32, 36, 48, 64, 72]

# Platform-appropriate modifier (for bindings) and label accelerator
IS_MAC = platform.system() == "Darwin"
BIND_MOD = "Command" if IS_MAC else "Control"
ACCEL = "⌘" if IS_MAC else "Ctrl"

# =======================
# Data Structures
# =======================
class TabData:
    def __init__(self, frame, text_widget, file_path=None, autosave_id=None, encoding="utf-8"):
        self.frame = frame
        self.text = text_widget
        self.file_path = file_path
        self.autosave_id = autosave_id or str(uuid.uuid4())
        self.encoding = encoding
        # formatting-aware history (content + tags)
        self.history = []
        self.future = []
        self.last_snapshot_serial = None

        # For typing: a tuple (bold, italic, underline) controlling new characters
        self.typing_style = (False, False, False)

# =======================
# Main App
# =======================
class AdvancedEditor:
    def __init__(self, root):
        self.root = root
        root.title(APP_NAME)
        root.geometry("1180x780")

        # --- Dark theming ---
        self.using_ctk = ctk is not None
        if self.using_ctk:
            ctk.set_appearance_mode("dark")  # force dark only
            ctk.set_default_color_theme("dark-blue")
        else:
            # Apply a dark ttk theme
            self._init_dark_ttk_theme()

        container = ctk.CTkFrame(root) if self.using_ctk else tk.Frame(root, bg="#111318")
        container.grid(row=0, column=0, sticky="nsew")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # Toolbar
        self.toolbar = ctk.CTkFrame(container) if self.using_ctk else tk.Frame(container, bg="#111318")
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))

        # Notebook (tabs)
        style = ttk.Style()
        if not self.using_ctk:
            style.configure("TNotebook", background="#0c0e12", borderwidth=0)
            style.configure("TNotebook.Tab", background="#1a1c22", foreground="#d7dae0", padding=(12, 6))
            style.map("TNotebook.Tab",
                      background=[("selected", "#23262e")],
                      foreground=[("selected", "#ffffff")])
        self.notebook = ttk.Notebook(container)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        # Status bar
        self.statusbar = ctk.CTkFrame(container) if self.using_ctk else tk.Frame(container, bg="#111318")
        self.statusbar.grid(row=2, column=0, sticky="ew", padx=10, pady=(6, 10))

        # --- State ---
        self.tabs = {}  # frame -> TabData
        self.current_font_family = tk.StringVar(value="Inter" if "Inter" in font.families() else "Helvetica")
        self.base_font_size = tk.IntVar(value=13)
        self.wrap_on = tk.BooleanVar(value=True)

        # A cache of style tags for bold/italic/underline combinations
        # key: (bold:bool, italic:bool, underline:bool) -> tagname str
        self.style_tag_cache = {}

        # Menus and toolbar
        self._build_menus()
        self._build_toolbar()
        self._build_statusbar()
        self._bind_shortcuts()

        # Right-click menu for tabs
        self._build_tab_context_menu()
        self.notebook.bind("<Button-3>", self._on_tab_right_click)
        if IS_MAC:
            self.notebook.bind("<Button-2>", self._on_tab_right_click)  # some mac configs

        # keyboard focus fix on fresh open
        self.root.after(50, self._focus_text_safely)

        # Start with a tab
        self._create_tab()

        # Autosave
        self.autosave_dir = tempfile.gettempdir()
        self._recover_autosaves_on_startup()
        self._schedule_autosave()

    # ---------- Dark ttk theme (fallback if CTk not available) ----------
    def _init_dark_ttk_theme(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(".", background="#0c0e12", foreground="#e7e9ee", fieldbackground="#0c0e12")
        style.configure("TLabel", background="#0c0e12", foreground="#e7e9ee")
        style.configure("TCombobox", fieldbackground="#161a21", background="#161a21", foreground="#e7e9ee",
                        arrowsize=16)
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#161a21")],
                  foreground=[("disabled", "#7b8190")])
        style.configure("TEntry", fieldbackground="#161a21", foreground="#e7e9ee")
        style.configure("TButton", background="#1f2430", foreground="#e7e9ee")
        style.map("TButton",
                  background=[("active", "#2a3140")])
        style.configure("TNotebook", background="#0c0e12", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1a1c22", foreground="#d7dae0", padding=(12, 6))

    # ---------- UI Builders ----------
    def _build_menus(self):
        menu_bar = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=menu_bar)

        def accel(txt):
            return f"{txt} {ACCEL}+"

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label=f"New Tab\t{ACCEL}+T", command=self._new_tab)
        file_menu.add_command(label=f"Open…\t{ACCEL}+O", command=self._open_in_new_tab)
        file_menu.add_command(label="Open with Encoding…", command=self._open_with_encoding)
        file_menu.add_separator()
        file_menu.add_command(label=f"Save\t{ACCEL}+S", command=self._save_current_tab)
        file_menu.add_command(label="Save As…", command=self._save_current_tab_as)
        file_menu.add_command(label="Save As (choose encoding)…", command=self._save_as_with_encoding)
        file_menu.add_separator()
        file_menu.add_command(label=f"Close Tab\t{ACCEL}+W", command=self._close_current_tab)
        file_menu.add_command(label=f"Exit\t{ACCEL}+Q", command=self._exit_editor)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label=f"Undo\t{ACCEL}+Z", command=self._undo)
        edit_menu.add_command(label=f"Redo\t{ACCEL}+Y", command=self._redo)
        edit_menu.add_separator()
        edit_menu.add_command(label=f"Cut\t{ACCEL}+X", command=self._cut)
        edit_menu.add_command(label=f"Copy\t{ACCEL}+C", command=self._copy)
        edit_menu.add_command(label=f"Paste\t{ACCEL}+V", command=self._paste)
        edit_menu.add_command(label=f"Select All\t{ACCEL}+A", command=self._select_all)
        edit_menu.add_command(label="Clear All", command=self._clear_all)
        edit_menu.add_separator()
        edit_menu.add_command(label=f"Find / Replace\t{ACCEL}+F", command=self._find_replace)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Word Wrap", variable=self.wrap_on, command=self._toggle_wrap)

        tools_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Make Bullet List", command=self._make_bullet_list)
        tools_menu.add_command(label="Make Numbered List", command=self._make_numbered_list)
        tools_menu.add_separator()
        tools_menu.add_command(label="Insert Link…", command=self._insert_link)
        tools_menu.add_command(label="Insert Email Link…", command=self._insert_email_link)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(
            label="About",
            command=lambda: messagebox.showinfo(
                "About",
                f"{APP_NAME}\nBuilt with Python & Tkinter\nBy Shreyash Srivastva"
            ),
        )

    def _build_toolbar(self):
        # Font family
        families = sorted(list(font.families()))
        family_label = (ctk.CTkLabel(self.toolbar, text="Font") if self.using_ctk
                        else ttk.Label(self.toolbar, text="Font"))
        family_label.grid(row=0, column=0, padx=(6, 6), pady=4, sticky="w")

        self.family_combo = ttk.Combobox(self.toolbar, values=families, width=18, state="readonly")
        self.family_combo.set(self.current_font_family.get())
        self.family_combo.bind("<<ComboboxSelected>>", lambda e: self._set_font_family(self.family_combo.get()))
        self.family_combo.grid(row=0, column=1, padx=(0, 10), pady=4, sticky="w")

        # Font size dropdown
        size_label = (ctk.CTkLabel(self.toolbar, text="Size") if self.using_ctk
                      else ttk.Label(self.toolbar, text="Size"))
        size_label.grid(row=0, column=2, padx=(0, 6), pady=4, sticky="w")

        self.size_combo = ttk.Combobox(self.toolbar, values=FONT_SIZE_OPTIONS, width=5, state="readonly")
        self.size_combo.set(self.base_font_size.get())
        self.size_combo.bind("<<ComboboxSelected>>", lambda e: self._set_font_size(int(self.size_combo.get())))
        self.size_combo.grid(row=0, column=3, padx=(0, 16), pady=4, sticky="w")

        # Bold / Italic / Underline (modern compact buttons)
        mkbtn = (ctk.CTkButton if self.using_ctk else tk.Button)
        btn_kwargs = dict(width=36) if self.using_ctk else dict(width=3, bg="#23262e", fg="#e7e9ee", bd=0, relief=tk.FLAT)

        self.bold_btn = mkbtn(self.toolbar, text="B", command=self._toggle_bold, **btn_kwargs)
        self.italic_btn = mkbtn(self.toolbar, text="I", command=self._toggle_italic, **btn_kwargs)
        self.underline_btn = mkbtn(self.toolbar, text="U", command=self._toggle_underline, **btn_kwargs)
        self.bold_btn.grid(row=0, column=4, padx=3)
        self.italic_btn.grid(row=0, column=5, padx=3)
        self.underline_btn.grid(row=0, column=6, padx=3)

        # Headings
        self.heading_var = tk.StringVar(value="Normal")
        self.heading_combo = ttk.Combobox(self.toolbar, values=list(HEADING_SIZES.keys()), width=10, textvariable=self.heading_var, state="readonly")
        self.heading_combo.grid(row=0, column=7, padx=(12, 10))
        self.heading_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_heading(self.heading_var.get()))

        # Lists
        self.bullet_btn = mkbtn(self.toolbar, text="• List", width=70, command=self._make_bullet_list)
        self.number_btn = mkbtn(self.toolbar, text="1. List", width=70, command=self._make_numbered_list)
        self.bullet_btn.grid(row=0, column=8, padx=4)
        self.number_btn.grid(row=0, column=9, padx=4)

        # Hyperlink
        self.link_btn = mkbtn(self.toolbar, text="Link", width=60, command=self._insert_link)
        self.email_btn = mkbtn(self.toolbar, text="Email", width=60, command=self._insert_email_link)
        self.link_btn.grid(row=0, column=10, padx=4)
        self.email_btn.grid(row=0, column=11, padx=4)

        # Color
        self.color_btn = mkbtn(self.toolbar, text="A•", width=50, command=self._set_text_color)
        self.color_btn.grid(row=0, column=12, padx=(4, 8))

        # filler
        if self.using_ctk:
            spacer = ctk.CTkLabel(self.toolbar, text="")
            spacer.grid(row=0, column=13, sticky="ew")
        self.toolbar.grid_columnconfigure(13, weight=1)

    def _build_statusbar(self):
        self.status = tk.StringVar()
        self.encoding_var = tk.StringVar(value="utf-8")

        status_lbl = (ctk.CTkLabel(self.statusbar, textvariable=self.status, anchor="w")
                      if self.using_ctk
                      else ttk.Label(self.statusbar, textvariable=self.status))
        status_lbl.grid(row=0, column=0, sticky="w", padx=6, pady=6)

        enc_label = (ctk.CTkLabel(self.statusbar, text="Encoding:")
                     if self.using_ctk else ttk.Label(self.statusbar, text="Encoding:"))
        enc_label.grid(row=0, column=1, padx=(12, 4))

        self.enc_combo = ttk.Combobox(self.statusbar, values=SUPPORTED_ENCODINGS, width=12, textvariable=self.encoding_var, state="readonly")
        self.enc_combo.grid(row=0, column=2, padx=(0, 8))
        self.enc_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_encoding_to_tab(self.encoding_var.get()))

        self.statusbar.grid_columnconfigure(3, weight=1)

    def _build_tab_context_menu(self):
        self.tab_menu = tk.Menu(self.root, tearoff=0)
        self.tab_menu.add_command(label="Close Tab", command=self._close_current_tab)
        self.tab_menu.add_command(label="Close Others", command=self._close_other_tabs)

    # ---------- Tabs ----------
    def _create_tab(self, title="Untitled", content="", file_path=None, recovered=False, autosave_id=None, encoding="utf-8"):
        frame = (ctk.CTkFrame(self.notebook) if self.using_ctk else tk.Frame(self.notebook, bg="#0c0e12"))
        text = tk.Text(
            frame,
            undo=False,
            wrap="word" if self.wrap_on.get() else "none",
            bg="#0f1117",
            fg="#e7e9ee",
            insertbackground="#ffffff",
            padx=12,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
        )
        text.pack(fill="both", expand=True, padx=2, pady=2)

        # Base font
        base_font = font.Font(family=self.current_font_family.get(), size=self.base_font_size.get())
        text.configure(font=base_font, spacing1=2, spacing2=2, spacing3=4)

        # Headings (paragraph-level)
        for name, sz in HEADING_SIZES.items():
            if name == "Normal":
                continue
            tagname = name.lower()
            text.tag_configure(tagname, font=font.Font(family=self.current_font_family.get(), size=sz, weight="bold"))

        # Hyperlink tag (visual style only; per-URL tag holds target)
        text.tag_configure("link", foreground="#7aa2ff", underline=1)
        text.tag_bind("link", "<Enter>", lambda e: text.config(cursor="hand2"))
        text.tag_bind("link", "<Leave>", lambda e: text.config(cursor=""))
        text.tag_bind("link", "<Button-1>", self._open_link_at_event)

        # find highlight
        text.tag_configure("highlight", background="#ffe083", foreground="#000000")

        text.insert("1.0", content)
        text.bind("<KeyRelease>", self._on_text_change)
        text.bind("<ButtonRelease>", self._update_status)
        text.bind("<<Modified>>", self._on_modified_apply_typing_style)

        # snapshot hooks to include formatting in history
        text.bind("<KeyRelease>", lambda e: self._snapshot_state())

        tab_id = self.notebook.add(frame, text=title if not recovered else f"Recovered - {title}")
        td = TabData(frame, text, file_path=file_path, autosave_id=autosave_id, encoding=encoding)
        self.tabs[frame] = td
        self.notebook.select(frame)

        # first snapshot
        self._snapshot_state(force=True)
        self._update_status()
        return td

    def _close_current_tab(self, event=None):
        sel = self.notebook.select()
        if not sel:
            return
        frame = self.root.nametowidget(sel)
        td = self.tabs.get(frame)
        if td:
            if messagebox.askyesno("Close tab", "Close this tab? Unsaved changes will be lost."):
                self._remove_autosave_file(td)
                self.notebook.forget(frame)
                del self.tabs[frame]
                if not self.tabs:
                    self._create_tab()

    def _close_other_tabs(self):
        current = self.notebook.select()
        to_close = []
        for tab_id in self.notebook.tabs():
            if tab_id != current:
                to_close.append(tab_id)
        for tab_id in to_close:
            frame = self.root.nametowidget(tab_id)
            td = self.tabs.get(frame)
            if td:
                self._remove_autosave_file(td)
                self.notebook.forget(frame)
                del self.tabs[frame]

    def _new_tab(self, event=None):
        self._create_tab()

    def _open_in_new_tab(self, event=None, encoding=None):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        enc = encoding or self._ask_encoding_dialog(default=self.encoding_var.get())
        if not enc:
            return
        try:
            with open(path, "r", encoding=enc) as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Open Error", f"Failed to open file:\n{e}")
            return
        title = os.path.basename(path)
        td = self._create_tab(title=title, content=content, file_path=path, encoding=enc)
        self.encoding_var.set(enc)
        self._apply_encoding_to_tab(enc)

    def _open_with_encoding(self):
        self._open_in_new_tab(encoding=self._ask_encoding_dialog(default=self.encoding_var.get()))

    def _save_current_tab(self, event=None):
        td = self._get_current_tabdata()
        if not td:
            return
        if td.file_path:
            self._write_file(td.file_path, td.text.get("1.0", "end-1c"), td.encoding)
            self._update_tab_title(td)
        else:
            self._save_current_tab_as()

    def _save_current_tab_as(self, event=None):
        td = self._get_current_tabdata()
        if not td:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        enc = td.encoding or self.encoding_var.get()
        self._write_file(path, td.text.get("1.0", "end-1c"), enc)
        td.file_path = path
        self._update_tab_title(td)
        self._remove_autosave_file(td)  # clear autosave metadata since user saved

    def _save_as_with_encoding(self):
        td = self._get_current_tabdata()
        if not td:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        enc = self._ask_encoding_dialog(default=td.encoding)
        if not enc:
            return
        td.encoding = enc
        self.encoding_var.set(enc)
        self._write_file(path, td.text.get("1.0", "end-1c"), enc)
        td.file_path = path
        self._update_tab_title(td)
        self._remove_autosave_file(td)

    def _ask_encoding_dialog(self, default="utf-8"):
        d = tk.Toplevel(self.root)
        d.title("Choose Encoding")
        d.transient(self.root)
        d.grab_set()
        (ttk.Label(d, text="Encoding:")).grid(row=0, column=0, padx=10, pady=10)
        enc_var = tk.StringVar(value=default if default in SUPPORTED_ENCODINGS else SUPPORTED_ENCODINGS[0])
        enc_combo = ttk.Combobox(d, values=SUPPORTED_ENCODINGS, width=20, textvariable=enc_var, state="readonly")
        enc_combo.grid(row=0, column=1, padx=10, pady=10)
        chosen = {"value": None}
        def ok():
            chosen["value"] = enc_var.get()
            d.destroy()
        def cancel():
            chosen["value"] = None
            d.destroy()
        ttk.Button(d, text="OK", command=ok).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(d, text="Cancel", command=cancel).grid(row=1, column=1, padx=10, pady=10)
        self.root.wait_window(d)
        return chosen["value"]

    def _write_file(self, path, data, encoding):
        try:
            with open(path, "w", encoding=encoding, newline="\n") as f:
                f.write(data)
            messagebox.showinfo("Saved", f"Saved to {path} ({encoding})")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{e}")

    def _update_tab_title(self, td):
        title = os.path.basename(td.file_path) if td.file_path else "Untitled"
        self.notebook.tab(td.frame, text=title)

    def _get_current_tabdata(self):
        sel = self.notebook.select()
        if not sel:
            return None
        frame = self.root.nametowidget(sel)
        return self.tabs.get(frame)

    # ---------- Status bar ----------
    def _update_status(self, event=None):
        td = self._get_current_tabdata()
        if not td:
            self.status.set("")
            return
        cursor_pos = td.text.index(tk.INSERT)
        row, col = cursor_pos.split(".")
        content = td.text.get("1.0", "end-1c")
        words = len(re.findall(r"\S+", content))
        chars = len(content)
        tab_title = os.path.basename(td.file_path) if td.file_path else self.notebook.tab(td.frame, option="text")
        self.status.set(f"{tab_title}  •  Ln {row}  •  Col {int(col)+1}  •  Words {words}  •  Chars {chars}")

    def _on_text_change(self, event=None):
        self._update_status()

    # When Tk marks the text widget modified, apply typing style to the last inserted char if needed
    def _on_modified_apply_typing_style(self, event=None):
        td = self._get_current_tabdata()
        if not td:
            return
        text = td.text
        if text.edit_modified():
            try:
                insert_index = text.index(tk.INSERT)
                last_index = f"{insert_index}-1c"
                if text.get(last_index, insert_index) and text.compare(last_index, "<", insert_index):
                    if td.typing_style != (False, False, False):
                        tagname = self._ensure_style_tag(*td.typing_style)
                        text.tag_add(tagname, last_index, insert_index)
            except Exception:
                pass
            text.edit_modified(False)

    def _focus_text_safely(self):
        td = self._get_current_tabdata()
        if td:
            td.text.focus_set()

    # ---------- Autosave ----------
    def _autosave_all_tabs(self):
        for td in list(self.tabs.values()):
            try:
                content = td.text.get("1.0", "end-1c")
                fname = AUTOSAVE_PREFIX + td.autosave_id + ".txt"
                fpath = os.path.join(self.autosave_dir, fname)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                meta = {
                    "file_path": td.file_path,
                    "timestamp": time.time(),
                    "title": os.path.basename(td.file_path) if td.file_path else self.notebook.tab(td.frame, option="text"),
                    "encoding": td.encoding,
                }
                meta_path = fpath + AUTOSAVE_META_EXT
                with open(meta_path, "w", encoding="utf-8") as m:
                    json.dump(meta, m)
            except Exception:
                pass
        self._schedule_autosave()

    def _schedule_autosave(self):
        self.root.after(AUTOSAVE_INTERVAL_MS, self._autosave_all_tabs)

    def _list_autosave_files(self):
        files = []
        for name in os.listdir(self.autosave_dir):
            if name.startswith(AUTOSAVE_PREFIX) and name.endswith(".txt"):
                files.append(os.path.join(self.autosave_dir, name))
        return files

    def _recover_autosaves_on_startup(self):
        autosave_files = self._list_autosave_files()
        if not autosave_files:
            return
        to_recover = []
        for fpath in autosave_files:
            meta_path = fpath + AUTOSAVE_META_EXT
            try:
                with open(meta_path, "r", encoding="utf-8") as m:
                    meta = json.load(m)
            except Exception:
                meta = {"file_path": None, "title": "Recovered", "encoding": "utf-8"}
            to_recover.append((fpath, meta))
        if not to_recover:
            return
        if not messagebox.askyesno("Recover files", f"Found {len(to_recover)} autosave file(s). Recover them?"):
            return
        for fpath, meta in to_recover:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                content = ""
            title = meta.get("title") or "Recovered"
            file_path = meta.get("file_path")
            autosave_id = os.path.basename(fpath)[len(AUTOSAVE_PREFIX):-4]
            encoding = meta.get("encoding", "utf-8")
            self._create_tab(title=title, content=content, file_path=file_path, recovered=True, autosave_id=autosave_id, encoding=encoding)
            try:
                os.remove(fpath)
                mp = fpath + AUTOSAVE_META_EXT
                if os.path.exists(mp):
                    os.remove(mp)
            except Exception:
                pass

    def _remove_autosave_file(self, td):
        fname = AUTOSAVE_PREFIX + td.autosave_id + ".txt"
        fpath = os.path.join(self.autosave_dir, fname)
        metapath = fpath + AUTOSAVE_META_EXT
        for p in (fpath, metapath):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass

    # ---------- Combined Inline Formatting (Bold/Italic/Underline) ----------
    # We use a single tag per combination and cache fonts by (bold, italic, underline)
    def _ensure_style_tag(self, bold: bool, italic: bool, underline: bool) -> str:
        key = (bool(bold), bool(italic), bool(underline))
        tagname = f"style_{int(bold)}{int(italic)}{int(underline)}"
        td = self._get_current_tabdata()
        if not td:
            return tagname
        txt = td.text
        if tagname not in txt.tag_names():
            # Create a font derived from the current family/size
            f = font.Font(family=self.current_font_family.get(), size=self.base_font_size.get(),
                          weight=("bold" if bold else "normal"),
                          slant=("italic" if italic else "roman"),
                          underline=1 if underline else 0)
            txt.tag_configure(tagname, font=f)
            self.style_tag_cache[key] = tagname
        return tagname

    def _clear_style_tags_in_range(self, text: tk.Text, start: str, end: str):
        for t in list(text.tag_names()):
            if t.startswith("style_"):
                text.tag_remove(t, start, end)

    def _get_combined_style_at_index(self, text: tk.Text, idx: str):
        """Returns (bold, italic, underline) based on the topmost style_* tag at idx, else defaults."""
        tags = text.tag_names(idx)
        # find any style_ tags; if multiple, the last one in tag order "wins"
        for t in reversed(tags):
            if t.startswith("style_") and len(t) == len("style_") + 3:
                b, i, u = t[-3], t[-2], t[-1]
                return (b == "1", i == "1", u == "1")
        # fallback: no style tag present
        return (False, False, False)

    def _toggle_style_on_selection(self, which: str):
        """which in {'bold','italic','underline'}"""
        td = self._get_current_tabdata()
        if not td:
            return
        text = td.text
        if text.tag_ranges("sel"):
            a, b = text.index("sel.first"), text.index("sel.last")
            # Use the style at the selection start as the baseline
            base = self._get_combined_style_at_index(text, a)
            bold, italic, underline = base
            if which == "bold":
                bold = not bold
            elif which == "italic":
                italic = not italic
            else:
                underline = not underline
            # Normalize the entire selection to the new combined style
            self._clear_style_tags_in_range(text, a, b)
            tagname = self._ensure_style_tag(bold, italic, underline)
            text.tag_add(tagname, a, b)
            self._snapshot_state()
        else:
            # Toggle typing style
            bold, italic, underline = td.typing_style
            if which == "bold":
                bold = not bold
            elif which == "italic":
                italic = not italic
            else:
                underline = not underline
            td.typing_style = (bold, italic, underline)
            preview = []
            if bold: preview.append("Bold")
            if italic: preview.append("Italic")
            if underline: preview.append("Underline")
            self.status.set(f"Typing style: {', '.join(preview) if preview else '(none)'}")
            self.root.after(1200, self._update_status)

    def _toggle_bold(self): self._toggle_style_on_selection("bold")
    def _toggle_italic(self): self._toggle_style_on_selection("italic")
    def _toggle_underline(self): self._toggle_style_on_selection("underline")

    # ---------- Headings (paragraph-level) ----------
    def _apply_heading(self, name):
        td = self._get_current_tabdata()
        if not td:
            return
        text = td.text
        # remove all heading tags first in selection/current line
        tag_names = [k.lower() for k in HEADING_SIZES.keys() if k != "Normal"]
        def clear_headings(a, b):
            for t in tag_names:
                text.tag_remove(t, a, b)
        if text.tag_ranges("sel"):
            a, b = text.index("sel.first"), text.index("sel.last")
            clear_headings(a, b)
            if name != "Normal":
                text.tag_add(name.lower(), a, b)
        else:
            line_start = text.index("insert linestart")
            line_end = text.index("insert lineend")
            clear_headings(line_start, line_end)
            if name != "Normal":
                text.tag_add(name.lower(), line_start, line_end)
        self._snapshot_state()

    # ---------- Color ----------
    def _set_text_color(self):
        color = colorchooser.askcolor()[1]
        td = self._get_current_tabdata()
        if color and td:
            tagname = f"color_{color}"
            if tagname not in td.text.tag_names():
                td.text.tag_configure(tagname, foreground=color)
            if td.text.tag_ranges("sel"):
                td.text.tag_add(tagname, "sel.first", "sel.last")
                self._snapshot_state()
            else:
                # Apply to typing by making a composite style+color tag layered:
                # We keep color as a separate tag to allow combining with B/I/U style tags.
                td.text.tag_add(tagname, tk.INSERT, tk.INSERT)  # no-op; just ensure exists
                self.status.set(f"Typing color: {color}")
                self.root.after(1200, self._update_status)

    # ---------- Lists (no extra indentation) ----------
    def _make_bullet_list(self):
        self._apply_list_prefix(prefix="• ")

    def _make_numbered_list(self):
        self._apply_list_prefix(prefix=None, numbered=True)

    def _apply_list_prefix(self, prefix="- ", numbered=False):
        td = self._get_current_tabdata()
        if not td:
            return
        text = td.text

        def apply_to_line(idx, i):
            line_start = text.index(f"{idx} linestart")
            current = text.get(line_start, f"{idx} lineend")
            # Avoid extra indentation: strip existing bullets and spaces first
            new = re.sub(r"^(\s*(?:[\-\*•]|\d+\.)\s+)?", "", current)
            if numbered:
                new = f"{i}. {new}"
            else:
                new = f"{prefix}{new}"
            text.delete(line_start, f"{idx} lineend")
            text.insert(line_start, new)

        if text.tag_ranges("sel"):
            first = int(text.index("sel.first").split(".")[0])
            last = int(text.index("sel.last").split(".")[0])
            n = 1
            for ln in range(first, last + 1):
                apply_to_line(f"{ln}.0", n)
                n += 1
        else:
            curr = text.index("insert")
            ln = curr.split(".")[0]
            apply_to_line(f"{ln}.0", 1)
        self._snapshot_state()

    # ---------- Links ----------
    def _insert_link(self):
        td = self._get_current_tabdata()
        if not td:
            return
        url = simpledialog.askstring("Insert Link", "Enter URL:")
        if not url:
            return
        display = simpledialog.askstring("Insert Link", "Text to display (optional):")
        text = td.text
        if text.tag_ranges("sel"):
            a, b = text.index("sel.first"), text.index("sel.last")
            if display:
                text.delete(a, b)
                text.insert(a, display)
                b = text.index(f"{a}+{len(display)}c")
        else:
            a = text.index("insert")
            disp = display or url
            text.insert(a, disp)
            b = text.index(f"{a}+{len(disp)}c")
        tagname = self._make_link_tag(url)
        text.tag_add(tagname, a, b)
        text.tag_add("link", a, b)
        self._snapshot_state()

    def _insert_email_link(self):
        td = self._get_current_tabdata()
        if not td:
            return
        email = simpledialog.askstring("Email", "Enter email address:")
        if not email:
            return
        subject = simpledialog.askstring("Email", "Subject (optional):")
        mailto = f"mailto:{email}"
        if subject:
            mailto += f"?subject={subject}"
        text = td.text
        disp = email
        a = text.index("insert") if not text.tag_ranges("sel") else text.index("sel.first")
        if text.tag_ranges("sel"):
            b = text.index("sel.last")
            text.delete(a, b)
        text.insert(a, disp)
        b = text.index(f"{a}+{len(disp)}c")
        tagname = self._make_link_tag(mailto)
        text.tag_add(tagname, a, b)
        text.tag_add("link", a, b)
        self._snapshot_state()

    def _make_link_tag(self, url):
        td = self._get_current_tabdata()
        text = td.text
        tagname = f"link_{abs(hash(url))}"
        if tagname not in text.tag_names():
            text.tag_configure(tagname)  # create
            if not hasattr(text, "_link_targets"):
                text._link_targets = {}
            text._link_targets[tagname] = url
        return tagname

    def _open_link_at_event(self, event):
        td = self._get_current_tabdata()
        if not td:
            return
        text = td.text
        idx = text.index(f"@{event.x},{event.y}")
        tags = text.tag_names(idx)
        for t in tags:
            if t.startswith("link_") and hasattr(text, "_link_targets"):
                url = text._link_targets.get(t)
                if url:
                    webbrowser.open(url)
                    return

    # ---------- View helpers ----------
    def _toggle_wrap(self):
        for td in self.tabs.values():
            td.text.config(wrap="word" if self.wrap_on.get() else "none")

    def _set_font_family(self, fam):
        self.current_font_family.set(fam)
        self._refresh_fonts()
        self._snapshot_state()

    def _set_font_size(self, size):
        self.base_font_size.set(size)
        self._refresh_fonts()
        self._snapshot_state()

    def _refresh_fonts(self):
        # Update base font and all style/heading tag fonts to current family/size
        for td in self.tabs.values():
            base = font.Font(family=self.current_font_family.get(), size=self.base_font_size.get())
            td.text.configure(font=base)
            # Update heading tags
            for name, sz in HEADING_SIZES.items():
                if name == "Normal":
                    continue
                td.text.tag_configure(name.lower(), font=font.Font(family=self.current_font_family.get(), size=sz, weight="bold"))
            # Update cached style_* tags to new base family/size while keeping attributes
            for t in td.text.tag_names():
                if t.startswith("style_") and len(t) == len("style_") + 3:
                    b = t[-3] == "1"
                    i = t[-2] == "1"
                    u = t[-1] == "1"
                    f = font.Font(family=self.current_font_family.get(), size=self.base_font_size.get(),
                                  weight=("bold" if b else "normal"),
                                  slant=("italic" if i else "roman"),
                                  underline=1 if u else 0)
                    td.text.tag_configure(t, font=f)

    def _apply_encoding_to_tab(self, enc):
        td = self._get_current_tabdata()
        if td:
            td.encoding = enc

    # ---------- Find/Replace ----------
    def _find_replace(self, event=None):
        td = self._get_current_tabdata()
        if not td:
            return
        text = td.text

        find_str = simpledialog.askstring("Find", "Find:")
        if not find_str:
            return
        replace_str = simpledialog.askstring("Replace", "Replace with (leave blank to skip):")
        if replace_str is not None:
            content = text.get("1.0", "end-1c")
            new_content = content.replace(find_str, replace_str)
            text.delete("1.0", "end")
            text.insert("1.0", new_content)
            self._snapshot_state()
        else:
            text.tag_remove("highlight", "1.0", "end")
            start = "1.0"
            while True:
                start = text.search(find_str, start, stopindex="end")
                if not start:
                    break
                end = f"{start}+{len(find_str)}c"
                text.tag_add("highlight", start, end)
                start = end

    # ---------- Shortcuts & exit ----------
    def _bind_shortcuts(self):
        # Bind cross-platform: Control on Win/Linux, Command on macOS
        mod = BIND_MOD

        self.root.bind(f"<{mod}-t>", lambda e: self._new_tab())
        self.root.bind(f"<{mod}-o>", lambda e: self._open_in_new_tab())
        self.root.bind(f"<{mod}-s>", lambda e: self._save_current_tab())
        self.root.bind(f"<{mod}-w>", lambda e: self._close_current_tab())
        self.root.bind(f"<{mod}-q>", lambda e: self._exit_editor())
        self.root.bind(f"<{mod}-a>", lambda e: self._select_all())
        self.root.bind(f"<{mod}-f>", lambda e: self._find_replace())

        # formatting shortcuts
        self.root.bind(f"<{mod}-b>", lambda e: self._toggle_bold())
        self.root.bind(f"<{mod}-i>", lambda e: self._toggle_italic())
        self.root.bind(f"<{mod}-u>", lambda e: self._toggle_underline())

        # zoom
        self.root.bind(f"<{mod}-=>", self._inc_font_size)  # = (plus w/o shift)
        self.root.bind(f"<{mod}-plus>", self._inc_font_size)
        self.root.bind(f"<{mod}-minus>", self._dec_font_size)
        self.root.bind(f"<{mod}-0>", self._reset_font_size)

        # Also support Ctrl variants on mac in case of alt keyboard layouts
        if IS_MAC:
            for k in ("t","o","s","w","q","a","f","b","i","u"):
                self.root.bind(f"<Control-{k}>", lambda e: None)  # prevent duplicate default behavior

    def _inc_font_size(self, event=None):
        new_size = min(64, self.base_font_size.get() + 1)
        self.base_font_size.set(new_size)
        self.size_combo.set(new_size)
        self._refresh_fonts()

    def _dec_font_size(self, event=None):
        new_size = max(8, self.base_font_size.get() - 1)
        self.base_font_size.set(new_size)
        self.size_combo.set(new_size)
        self._refresh_fonts()

    def _reset_font_size(self, event=None):
        self.base_font_size.set(13)
        self.size_combo.set(13)
        self._refresh_fonts()

    def _exit_editor(self, event=None):
        if messagebox.askyesno("Exit", "Close the editor?"):
            for td in list(self.tabs.values()):
                if td.file_path:
                    self._remove_autosave_file(td)
            self.root.destroy()

    # ---------- Tab context menu ----------
    def _on_tab_right_click(self, event):
        x, y = event.x, event.y
        elem = self.notebook.identify(x, y)
        if "label" in elem:
            self.notebook.select(self.notebook.index(f"@{x},{y}"))
            self.tab_menu.tk_popup(event.x_root, event.y_root)

    # ---------- History (text + tags) ----------
    def _capture_state(self):
        td = self._get_current_tabdata()
        if not td:
            return None
        txt = td.text
        content = txt.get("1.0", "end-1c")
        tags_state = {}
        for tname in txt.tag_names():
            if tname in ("sel", "current"):
                continue
            ranges = txt.tag_ranges(tname)
            if ranges:
                pairs = []
                for i in range(0, len(ranges), 2):
                    a, b = str(ranges[i]), str(ranges[i+1])
                    pairs.append((a, b))
                tags_state[tname] = pairs
        insert_idx = txt.index(tk.INSERT)
        return {
            "content": content,
            "tags": tags_state,
            "insert": insert_idx,
            "encoding": td.encoding,
            "font_family": self.current_font_family.get(),
            "font_size": self.base_font_size.get(),
        }

    def _restore_state(self, state):
        if state is None:
            return
        td = self._get_current_tabdata()
        if not td:
            return
        txt = td.text
        txt.delete("1.0", "end")
        txt.insert("1.0", state.get("content", ""))

        # clear all tags
        for t in txt.tag_names():
            txt.tag_remove(t, "1.0", "end")

        # reapply known tag configs (fonts)
        self.current_font_family.set(state.get("font_family", self.current_font_family.get()))
        self.base_font_size.set(state.get("font_size", self.base_font_size.get()))
        self.size_combo.set(self.base_font_size.get())
        self._refresh_fonts()

        # recreate color and style tags as needed
        for tname, pairs in state.get("tags", {}).items():
            if tname not in txt.tag_names():
                if tname.startswith("color_"):
                    color = tname.split("_", 1)[1]
                    txt.tag_configure(tname, foreground=color)
                elif tname.startswith("style_") and len(tname) == len("style_") + 3:
                    b, i, u = tname[-3] == "1", tname[-2] == "1", tname[-1] == "1"
                    self._ensure_style_tag(b, i, u)
                elif tname.startswith("link_"):
                    txt.tag_configure(tname)
            for a, b in pairs:
                txt.tag_add(tname, a, b)

        # generic link style re-ensured
        txt.tag_configure("link", foreground="#7aa2ff", underline=1)
        txt.mark_set(tk.INSERT, state.get("insert", "1.0"))
        td.encoding = state.get("encoding", td.encoding)
        self.encoding_var.set(td.encoding)
        self._update_status()

    def _snapshot_state(self, force=False):
        td = self._get_current_tabdata()
        if not td:
            return
        state = self._capture_state()
        serial = (hash(state["content"]) ^ hash(tuple(sorted((k, tuple(v)) for k, v in state["tags"].items())))) & 0xFFFFFFFF
        if force or serial != td.last_snapshot_serial:
            td.history.append(state)
            if len(td.history) > 200:
                td.history = td.history[-200:]
            td.future.clear()
            td.last_snapshot_serial = serial

    def _undo(self, event=None):
        td = self._get_current_tabdata()
        if not td or not td.history:
            return
        if len(td.history) >= 1:
            state = td.history.pop()
            td.future.append(self._capture_state())
            self._restore_state(state)

    def _redo(self, event=None):
        td = self._get_current_tabdata()
        if not td or not td.future:
            return
        state = td.future.pop()
        td.history.append(self._capture_state())
        self._restore_state(state)

    def _cut(self):
        td = self._get_current_tabdata()
        if td:
            td.text.event_generate("<<Cut>>")
            self._snapshot_state()

    def _copy(self):
        td = self._get_current_tabdata()
        if td:
            td.text.event_generate("<<Copy>>")

    def _paste(self):
        td = self._get_current_tabdata()
        if td:
            td.text.event_generate("<<Paste>>")
            self._snapshot_state()

    def _select_all(self, event=None):
        td = self._get_current_tabdata()
        if td:
            td.text.tag_add("sel", "1.0", "end")
            return "break"

    def _clear_all(self):
        td = self._get_current_tabdata()
        if td:
            td.text.delete("1.0", "end")
            self._snapshot_state()

if __name__ == "__main__":
    Root = ctk.CTk() if ctk is not None else tk.Tk()
    app = AdvancedEditor(Root)
    Root.mainloop()