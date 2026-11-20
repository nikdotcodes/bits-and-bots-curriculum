#!/usr/bin/env python3
"""Build all existing lesson sources. Run from any working directory."""
from pathlib import Path
import base64
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "sessions"
BUILD = ROOT / "build"

def run(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run([str(x) for x in cmd], cwd=ROOT, check=True)

def check_font(font_name="Space Grotesk"):
    """Ask XeLaTeX/fontspec to resolve the font, matching the PDF build."""
    if not shutil.which("xelatex"):
        print(f"font ({font_name}): NOT CHECKED (xelatex missing)")
        return False
    document = (
        "\\documentclass{article}\n"
        "\\usepackage{fontspec}\n"
        f"\\setmainfont{{{font_name}}}\n"
        "\\begin{document}Font check\\end{document}\n"
    )
    with tempfile.TemporaryDirectory(prefix="bitsandbots-font-check-") as temp:
        source = Path(temp) / "font-check.tex"
        source.write_text(document, encoding="utf-8")
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", source.name],
            cwd=temp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, check=False, timeout=60,
        )
        if result.returncode == 0:
            print(f"font ({font_name}): OK (XeLaTeX/fontspec)")
            return True
        print(f"font ({font_name}): NOT AVAILABLE to XeLaTeX")
        print("  macOS: brew install --cask font-space-grotesk")
        print("  Ubuntu/CI: sudo apt-get install fonts-space-grotesk")
        print("  After installing, rerun: make check")
        return False


def check():
    ok = True
    for tool in ("pandoc", "xelatex", "node", "npm"):
        location = shutil.which(tool)
        print(f"{tool}: {location or 'NOT FOUND'}")
        ok = bool(location) and ok
    marp_installed = (ROOT / "node_modules/.bin/marp").exists()
    print("marp:", "installed" if marp_installed else "run npm ci")
    ok = marp_installed and ok
    print("sessions:", len(list(SESSIONS.glob('[0-9][0-9]-*'))))
    ok = check_font() and ok
    if not ok:
        raise SystemExit("Environment check failed; resolve the issues above.")

def build_pdfs():
    if not shutil.which("pandoc") or not shutil.which("xelatex"):
        raise SystemExit("PDF builds require pandoc and xelatex")
    for session in sorted(SESSIONS.glob('[0-9][0-9]-*')):
        for source, defaults in (("leader-guide.md", "pandoc-leader.yaml"), ("activity-sheet.md", "pandoc-child.yaml"), ("challenges.md", "pandoc-child.yaml")):
            src = session / source
            if src.exists():
                out = BUILD / "pdf" / f"{session.name}-{src.stem}.pdf"
                out.parent.mkdir(parents=True, exist_ok=True)
                run(["pandoc", "--defaults", f"config/{defaults}", src.relative_to(ROOT), "-o", out.relative_to(ROOT)])

def build_slides(fmt):
    """Render Marp slides as PDF or browser-based HTML with embedded logo."""
    marp = ROOT / "node_modules/.bin/marp"
    if not marp.exists():
        raise SystemExit("Run npm ci to install Marp CLI")
    if fmt not in ("slides", "html"):
        raise ValueError(f"Unsupported slide format: {fmt}")

    # Embed the logo as a data URL in a generated copy of the theme. Relative
    # URLs inside a --theme-set stylesheet are unreliable in exported HTML/PDF.
    theme = ROOT / "themes/bitsandbots.css"
    logo = ROOT / "themes/BitsAndBotBot.png"
    if not logo.is_file():
        raise SystemExit(f"Missing title-slide logo: {logo}")
    css = theme.read_text(encoding="utf-8")
    original_url = 'url("./BitsAndBotBot.png")'
    if original_url not in css:
        raise SystemExit(f"Expected {original_url} in {theme}")
    encoded = base64.b64encode(logo.read_bytes()).decode("ascii")
    css = css.replace(original_url, f'url("data:image/png;base64,{encoded}")')

    is_html = fmt == "html"
    output_dir = "html" if is_html else "slides"
    suffix = "html" if is_html else "pdf"
    with tempfile.TemporaryDirectory(prefix="bitsandbots-marp-") as temp:
        generated_theme = Path(temp) / "bitsandbots.css"
        generated_theme.write_text(css, encoding="utf-8")
        for session in sorted(SESSIONS.glob('[0-9][0-9]-*')):
            src = session / "slides.md"
            if not src.exists():
                continue
            out = BUILD / output_dir / f"{session.name}-slides.{suffix}"
            out.parent.mkdir(parents=True, exist_ok=True)
            cmd = [marp, src.relative_to(ROOT), "--theme-set", generated_theme]
            if is_html:
                cmd += ["--template", "bespoke"]
            else:
                cmd += ["--pdf"]
            run([*cmd, "-o", out.relative_to(ROOT)])

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    if action == "check": check()
    elif action == "pdf": build_pdfs()
    elif action == "slides": build_slides("slides")
    elif action in ("html", "html-slides"): build_slides("html")
    else: raise SystemExit(f"Unknown action: {action}")
