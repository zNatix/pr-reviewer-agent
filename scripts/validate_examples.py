#!/usr/bin/env python3
"""
Validate examples/ folder regression harness.
Checks that every bad-*.md declares an expected severity and contains a code block,
and that every good-*.md does not declare a finding severity.
"""

import glob
import os
import re
import sys

EXAMPLES_DIR = "examples"
SEVERITY_RE = re.compile(r"^##\s+(🔴\s+Critical|🟡\s+Warning|🔵\s+Suggestion)", re.MULTILINE)
GOOD_RE = re.compile(r"^##\s+✅\s+Good Practice", re.MULTILINE)
CODE_BLOCK_RE = re.compile(r"```\w*\n", re.MULTILINE)

def validate_pair(domain, bad_path, good_path):
    errors = 0
    warnings = 0

    # Validate bad file
    with open(bad_path, encoding="utf-8") as f:
        bad_content = f.read()

    severity_match = SEVERITY_RE.search(bad_content)
    if not severity_match:
        print(f"  ERROR [{domain}/bad]: missing expected severity header (## 🔴 Critical / 🟡 Warning / 🔵 Suggestion)")
        errors += 1
    else:
        severity = severity_match.group(1)
        print(f"  OK [{domain}/bad]: expected severity = {severity}")

    if not CODE_BLOCK_RE.search(bad_content):
        print(f"  ERROR [{domain}/bad]: missing code block")
        errors += 1
    else:
        print(f"  OK [{domain}/bad]: contains code block")

    if "Expected finding" not in bad_content:
        print(f"  WARNING [{domain}/bad]: missing 'Expected finding' description")
        warnings += 1
    else:
        print(f"  OK [{domain}/bad]: contains expected finding description")

    # Validate good file
    with open(good_path, encoding="utf-8") as f:
        good_content = f.read()

    if SEVERITY_RE.search(good_content):
        print(f"  ERROR [{domain}/good]: must not declare a finding severity (## 🔴 / 🟡 / 🔵)")
        errors += 1
    else:
        print(f"  OK [{domain}/good]: no finding severity declared")

    if not GOOD_RE.search(good_content):
        print(f"  WARNING [{domain}/good]: missing '## ✅ Good Practice' header")
        warnings += 1
    else:
        print(f"  OK [{domain}/good]: Good Practice header present")

    if not CODE_BLOCK_RE.search(good_content):
        print(f"  ERROR [{domain}/good]: missing code block")
        errors += 1
    else:
        print(f"  OK [{domain}/good]: contains code block")

    return errors, warnings


def main():
    total_errors = 0
    total_warnings = 0
    domains_checked = 0

    print("Validating examples/ regression harness")

    for domain_dir in sorted(glob.glob(os.path.join(EXAMPLES_DIR, "*/"))):
        domain = os.path.basename(os.path.dirname(domain_dir))
        if domain == "archive":
            continue

        bad_files = sorted(glob.glob(os.path.join(domain_dir, "bad-*.md")))
        good_files = sorted(glob.glob(os.path.join(domain_dir, "good-*.md")))

        if not bad_files and not good_files:
            continue

        print(f"\nDomain: {domain}")
        domains_checked += 1

        if not bad_files:
            print(f"  ERROR [{domain}]: missing bad-*.md example")
            total_errors += 1
        if not good_files:
            print(f"  ERROR [{domain}]: missing good-*.md example")
            total_errors += 1

        # Match any bad/good pair in the same directory; names need not be symmetrical.
        for bad in bad_files:
            if good_files:
                e, w = validate_pair(domain, bad, good_files[0])
                total_errors += e
                total_warnings += w

    print(f"\n{'=' * 50}")
    print(f"Domains checked: {domains_checked}")
    print(f"Errors: {total_errors}")
    print(f"Warnings: {total_warnings}")

    if total_errors:
        print("\n::error::Examples validation failed")
        sys.exit(1)
    if total_warnings:
        print("\n::warning::Examples validation passed with warnings")
    else:
        print("\nAll examples validated.")


if __name__ == "__main__":
    main()
