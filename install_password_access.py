#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path.cwd()

EXAMS = {
    "practice1": ROOT/"exam-prep/practice1/index.html",
    "practice2": ROOT/"exam-prep/practice2/index.html",
    "practice3": ROOT/"exam-prep/practice3/index.html",
    "practice4": ROOT/"exam-prep/practice4/index.html",
    "finalReview": ROOT/"exam-prep/final-review/index.html",
}

OAPS = {
    "oap1ph": ROOT/"oap-simulations/1-PH/index.html",
    "oap1itw": ROOT/"oap-simulations/1-ITW/index.html",
    "oap3": ROOT/"oap-simulations/3-ITW+PH/index.html",
    "oap4": ROOT/"oap-simulations/4/index.html",
    "oap5": ROOT/"oap-simulations/5/index.html",
    "oap61": ROOT/"oap-simulations/6-1/index.html",
    "oap62": ROOT/"oap-simulations/6-2/index.html",
    "oap7": ROOT/"oap-simulations/7/index.html",
    "oap8": ROOT/"oap-simulations/8/index.html",
}

def read(p): return p.read_text(encoding="utf-8", errors="replace")
def write(p,t): p.write_text(t, encoding="utf-8")

def strip_access(text):
    text = re.sub(r'\s*<link[^>]+access-control\.css[^>]*>\s*', '\n', text, flags=re.I)
    text = re.sub(r'\s*<script[^>]+access\.js[^>]*></script>\s*', '\n', text, flags=re.I)
    text = re.sub(r'\s*<script[^>]+access-control\.js[^>]*></script>\s*', '\n', text, flags=re.I)
    text = re.sub(r'\s*<script>\s*document\.documentElement\.classList\.add\(["\']bfin-access-pending["\']\);\s*</script>\s*', '\n', text, flags=re.I)
    return text

def patch_landing(path, section):
    text = strip_access(read(path))

    if section == "exam":
        # Replace the legacy "hidden" control with visible cards.
        text = re.sub(
            r'data-practice-tests\s*=\s*["\']hidden["\']',
            'data-practice-tests="visible"',
            text,
            flags=re.I
        )
        # Also make the CSS default visible so no JS timing issue can hide cards.
        text = re.sub(
            r'(\.practice-test-content\s*\{[^}]*?)display\s*:\s*none\s*!important\s*;',
            r'\1display: flex !important;',
            text,
            flags=re.I | re.S
        )

    css = '<link rel="stylesheet" href="access-control.css">'
    scripts = '<script src="access.js"></script>\n<script src="access-control.js"></script>'
    text = re.sub(r'</head>', css+'\n</head>', text, count=1, flags=re.I)
    text = re.sub(r'</body>', scripts+'\n</body>', text, count=1, flags=re.I)
    write(path, text)

def patch_direct(path, key, marker):
    text = strip_access(read(path))

    if re.search(fr'{re.escape(marker)}\s*=', text, flags=re.I):
        text = re.sub(
            fr'{re.escape(marker)}\s*=\s*["\'][^"\']*["\']',
            f'{marker}="{key}"',
            text, count=1, flags=re.I
        )
    else:
        text = re.sub(r'<html\b', f'<html {marker}="{key}"', text, count=1, flags=re.I)

    pending = (
        '<script>document.documentElement.classList.add("bfin-access-pending");</script>\n'
        '<link rel="stylesheet" href="../access-control.css">\n'
        '<script src="../access.js"></script>'
    )
    text = re.sub(r'<head\b[^>]*>', lambda m: m.group(0)+'\n'+pending, text, count=1, flags=re.I)
    text = re.sub(r'</body>', '<script src="../access-control.js"></script>\n</body>', text, count=1, flags=re.I)
    write(path, text)

def main():
    exam_landing = ROOT/"exam-prep/index.html"
    oap_landing = ROOT/"oap-simulations/index.html"

    required = [exam_landing, oap_landing, *EXAMS.values(), *OAPS.values()]
    missing = [p for p in required if not p.exists()]
    if missing:
        print("Run this from the financial-reporting-apps repository root.")
        print("Missing:")
        for p in missing: print(" -", p.relative_to(ROOT))
        sys.exit(1)

    patch_landing(exam_landing, "exam")
    print("PATCHED exam-prep/index.html")

    for key, path in EXAMS.items():
        patch_direct(path, key, "data-bfin-exam-key")
        print("PATCHED", path.relative_to(ROOT))

    patch_landing(oap_landing, "oap")
    print("PATCHED oap-simulations/index.html")

    for key, path in OAPS.items():
        patch_direct(path, key, "data-bfin-oap-key")
        print("PATCHED", path.relative_to(ROOT))

    print("\nDone.")
    print("Exam passwords: exam-prep/access.js")
    print("OAP passwords:  oap-simulations/access.js")

if __name__ == "__main__":
    main()
