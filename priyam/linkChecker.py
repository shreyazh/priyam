import subprocess
import sys
from pathlib import Path

def run_linkchecker():
    script = Path(__file__).parent / "external" / "LinkCheckerOriginal.py"

    if not script.exists():
        raise FileNotFoundError(f"Cannot find: {script}")

    subprocess.run([sys.executable, str(script)])
