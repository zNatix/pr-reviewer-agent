#!/usr/bin/env python3
"""
Validate GitHub Copilot custom instructions and agent frontmatter.
Enforces documented schema compatibility, size limits, and semantic rules.
"""

import glob
import os
import re
import sys

import yaml

MAX_CODE_REVIEW_CHARS = 4000
WARN_AT = 3500

errors = 0
warnings = 0
semver_re = re.compile(r"^\d+\.\d+\.\d+(-[\w.]+)?(\+[\w.]+)?$")
DEPRECATED_MODELS = {"gpt-5.2-codex", "gpt-5.2"}
ALLOWED_EXCLUDE_AGENTS = {"coding-agent", "code-review", "cloud-agent"}


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


def collect_instruction_files() -> set:
    return set(glob.glob(".github/instructions/*.instructions.md"))


def check_instruction_references(path: str, content: str, existing: set, strict: bool = True):
    global errors, warnings
    found = set(re.findall(r"[\w\-]+\.instructions\.md", content))
    for ref in found:
        full = os.path.join(".github/instructions", ref)
        if full not in existing:
            if strict:
                print(f"  ERROR: references non-existent instruction file: {ref}")
                errors += 1
            else:
                print(f"  WARNING: references non-existent instruction file: {ref}")
                warnings += 1


existing_instructions = collect_instruction_files()

# Validate instruction files
for f in sorted(existing_instructions):
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
        val = ea[0] if isinstance(ea, list) else ea
        if val not in ALLOWED_EXCLUDE_AGENTS:
            print(f"  WARNING: excludeAgent value {val!r} not in known allowlist {ALLOWED_EXCLUDE_AGENTS}")
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

    # model: must be string (or omitted), and not deprecated
    if "model" in doc:
        m = doc["model"]
        if not isinstance(m, str):
            print(f'  ERROR: model must be a string or omitted, got {type(m).__name__}')
            errors += 1
        else:
            if m.lower() in DEPRECATED_MODELS:
                print(f'  ERROR: model {m!r} is deprecated — omit or use a supported model')
                errors += 1
    else:
        print("  INFO: model omitted — Copilot will select the best available model")

    # tools: must be array
    if "tools" not in doc:
        print("  ERROR: missing tools field")
        errors += 1
    elif not isinstance(doc["tools"], list):
        print(f'  ERROR: tools must be an array, got {type(doc["tools"]).__name__}')
        errors += 1
    else:
        has_execute = "execute" in doc["tools"]
        is_trusted = "trusted" in os.path.basename(f).lower()
        if has_execute and not is_trusted:
            print(f"  ERROR: non-trusted agent includes 'execute' tool — remove it or rename agent to include 'trusted'")
            errors += 1
        elif has_execute:
            print(f"  WARNING: trusted agent includes 'execute' tool — ensure this is restricted to trusted branches")
            warnings += 1

    # version: semver
    if "version" not in doc:
        print("  ERROR: missing version field")
        errors += 1
    elif not isinstance(doc["version"], str) or not semver_re.match(doc["version"]):
        print(f'  ERROR: version must be semver, got: {doc.get("version")}')
        errors += 1

    # semantic: references to instruction files
    check_instruction_references(f, content, existing_instructions)

    print("  OK")

# Validate README for stale references
readme_path = "README.md"
if os.path.exists(readme_path):
    print(f"Checking {readme_path}")
    with open(readme_path, encoding="utf-8") as f:
        readme_content = f.read()
    check_instruction_references(readme_path, readme_content, existing_instructions, strict=False)
    print("  OK")

if errors:
    print(f"::error::{errors} validation error(s)")
    sys.exit(1)
if warnings:
    print(f"::warning::{warnings} validation warning(s)")
print("All files validated.")
