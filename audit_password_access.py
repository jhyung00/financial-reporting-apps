#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path.cwd()

checks = [
    ("exam landing", ROOT/"exam-prep/index.html", ["access.js", "access-control.js"]),
    ("practice1", ROOT/"exam-prep/practice1/index.html", ['data-bfin-exam-key="practice1"', "../access.js"]),
    ("practice2", ROOT/"exam-prep/practice2/index.html", ['data-bfin-exam-key="practice2"', "../access.js"]),
    ("practice3", ROOT/"exam-prep/practice3/index.html", ['data-bfin-exam-key="practice3"', "../access.js"]),
    ("practice4", ROOT/"exam-prep/practice4/index.html", ['data-bfin-exam-key="practice4"', "../access.js"]),
    ("final review", ROOT/"exam-prep/final-review/index.html", ['data-bfin-exam-key="finalReview"', "../access.js"]),
    ("OAP landing", ROOT/"oap-simulations/index.html", ["access.js", "access-control.js"]),
    ("OAP 1 PH", ROOT/"oap-simulations/1-PH/index.html", ['data-bfin-oap-key="oap1ph"', "../access.js"]),
    ("OAP 1 ITW", ROOT/"oap-simulations/1-ITW/index.html", ['data-bfin-oap-key="oap1itw"', "../access.js"]),
    ("OAP 3", ROOT/"oap-simulations/3-ITW+PH/index.html", ['data-bfin-oap-key="oap3"', "../access.js"]),
    ("OAP 4", ROOT/"oap-simulations/4/index.html", ['data-bfin-oap-key="oap4"', "../access.js"]),
    ("OAP 5", ROOT/"oap-simulations/5/index.html", ['data-bfin-oap-key="oap5"', "../access.js"]),
    ("OAP 6-1", ROOT/"oap-simulations/6-1/index.html", ['data-bfin-oap-key="oap61"', "../access.js"]),
    ("OAP 6-2", ROOT/"oap-simulations/6-2/index.html", ['data-bfin-oap-key="oap62"', "../access.js"]),
    ("OAP 7", ROOT/"oap-simulations/7/index.html", ['data-bfin-oap-key="oap7"', "../access.js"]),
    ("OAP 8", ROOT/"oap-simulations/8/index.html", ['data-bfin-oap-key="oap8"', "../access.js"]),
]

errors = []
for label, path, needles in checks:
    if not path.exists():
        errors.append(f"{label}: missing {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    for needle in needles:
        if needle not in text:
            errors.append(f"{label}: missing {needle}")

for p in [
    ROOT/"exam-prep/access.js",
    ROOT/"exam-prep/access-control.js",
    ROOT/"exam-prep/access-control.css",
    ROOT/"oap-simulations/access.js",
    ROOT/"oap-simulations/access-control.js",
    ROOT/"oap-simulations/access-control.css",
]:
    if not p.exists():
        errors.append(f"missing {p.relative_to(ROOT)}")

print("BFIN 367 PASSWORD ACCESS AUDIT")
print("="*55)
if errors:
    for e in errors: print("ERROR:", e)
    print(f"\nAUDIT FAILED: {len(errors)} error(s)")
    sys.exit(1)

print("PASS Exam Prep landing")
print("PASS Practice Exams 1-4")
print("PASS Final Review")
print("PASS OAP landing")
print("PASS OAP 1-PH, 1-ITW, 3, 4, 5, 6-1, 6-2, 7, 8")
print("\nAUDIT PASSED: 0 errors")
