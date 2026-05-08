#!/usr/bin/env python3
"""
Validate GitHub Copilot custom instructions and agent frontmatter.
Enforces documented schema compatibility and size limits.
"""

import glob
import re
import sys

import yaml

MAX_CODE_REVIEW_CHARS = 4000
WARN_AT = 3500

errors = 0
warnings = 0
semver_re = re.compile(r"^\d+\.\d+\.\d+(-[\w.]+)?(\+[\w.]+)?$")


def extract_frontmatter(path: str):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return None, "missing opening ---", content
    end = content.find("---", 3)
    if end == -1:
        return None, "missing closing ---", content
    return content[3:end].strip(), None, content


def check_size(path: str, content: str):
    global warnings
    length = len(content)
    if length > MAX_CODE_REVIEW_CHARS:
        print(f"  ERROR: file exceeds {MAX_CODE_REVIEW_CHARS} chars ({length}) — Copilot Code Review may truncate")
        return 1
    elif length > WARN_AT:
        print(f"  WARNING: file exceeds {WARN_AT} chars ({length}) — approaching Copilot Code Review limit")
        warnings += 1
    return 0


# Validate instruction files
for f in sorted(glob.glob(".github/instructions/*.instructions.md")):
    print(f"Checking {f}")
    fm, err, content = extract_frontmatter(f)
    if err:
        print(f"  ERROR: {err}")
        errors += 1
        continue

    try:
        doc = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        print(f"  ERROR: YAML parse failed: {e}")
        errors += 1
        continue

    if not isinstance(doc, dict):
        print(f"  ERROR: frontmatter must be a YAML mapping, got {type(doc).__name__}")
        errors += 1
        continue

    # applyTo: required
    if "applyTo" not in doc:
        print("  ERROR: missing required field applyTo")
        errors += 1
    elif doc["applyTo"] is None:
        print("  ERROR: applyTo is null")
        errors += 1

    # excludeAgent: scalar string preferred (array accepted for backward compat)
    if "excludeAgent" in doc:
        ea = doc["excludeAgent"]
        if isinstance(ea, list) and len(ea) == 1:
            print(f"  WARNING: excludeAgent is an array with one item; prefer scalar string: {ea[0]!r}")
            warnings += 1

    # version: must be semver string
    if "version" not in doc:
        print("  ERROR: missing version field")
        errors += 1
    elif not isinstance(doc["version"], str) or not semver_re.match(doc["version"]):
        print(f'  ERROR: version must be semver (e.g. 1.0.0), got: {doc.get("version")}')
        errors += 1

    errors += check_size(f, content)
    print("  OK")

# Validate agent files
for f in sorted(glob.glob(".github/agents/*.agent.md")):
    print(f"Checking {f}")
    fm, err, content = extract_frontmatter(f)
    if err:
        print(f"  ERROR: {err}")
        errors += 1
        continue

    try:
        doc = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        print(f"  ERROR: YAML parse failed: {e}")
        errors += 1
        continue

    if not isinstance(doc, dict):
        print("  ERROR: frontmatter must be a YAML mapping")
        errors += 1
        continue

    for field in ["name", "description"]:
        if field not in doc:
            print(f"  ERROR: missing required field: {field}")
            errors += 1

    # model: must be string (or omitted)
    if "model" in doc:
        if not isinstance(doc["model"], str):
            print(f'  ERROR: model must be a string or omitted, got {type(doc["model"]).__name__}')
            errors += 1

    # tools: must be array
    if "tools" not in doc:
        print("  ERROR: missing tools field")
        errors += 1
    elif not isinstance(doc["tools"], list):
        print(f'  ERROR: tools must be an array, got {type(doc["tools"]).__name__}')
        errors += 1
    else:
        if "execute" in doc["tools"]:
            print(f"  WARNING: agent includes 'execute' tool — ensure this is intentional and restricted to trusted branches")
            warnings += 1

    # version: semver
    if "version" not in doc:
        print("  ERROR: missing version field")
        errors += 1
    elif not isinstance(doc["version"], str) or not semver_re.match(doc["version"]):
        print(f'  ERROR: version must be semver, got: {doc.get("version")}')
        errors += 1

    print("  OK")

if errors:
    print(f"::error::{errors} validation error(s)")
    sys.exit(1)
if warnings:
    print(f"::warning::{warnings} validation warning(s)")
print("All files validated.")
