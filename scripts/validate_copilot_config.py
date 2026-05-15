#!/usr/bin/env python3
"""
Validate GitHub Copilot custom instructions and agent frontmatter.
Enforces documented schema compatibility, size limits, and semantic rules.
Also validates YAML syntax of workflows, labeler, and issue templates.
"""

import glob
import os
import re
import sys

import yaml

MAX_CODE_REVIEW_CHARS = 4000
WARN_AT = 3800

errors = 0
warnings = 0
semver_re = re.compile(r"^\d+\.\d+\.\d+(-[\w.]+)?(\+[\w.]+)?$")
DEPRECATED_MODELS = {"gpt-5.2-codex", "gpt-5.2"}
ALLOWED_EXCLUDE_AGENTS = {"coding-agent", "code-review", "cloud-agent"}
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def extract_frontmatter(path: str):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return None, "missing opening ---", content
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None, "missing closing --- or malformed frontmatter", content
    return m.group(1).strip(), None, content


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
                print(f"  INFO: references non-existent instruction file (ok if optional/stack guide): {ref}")


def validate_yaml_file(path: str):
    global errors
    try:
        with open(path, encoding="utf-8") as f:
            yaml.safe_load(f)
        print(f"  OK (YAML valid)")
    except yaml.YAMLError as e:
        print(f"  ERROR: YAML parse failed: {e}")
        errors += 1


existing_instructions = collect_instruction_files()

# Validate README file count matches actual instruction files
readme_count_path = "README.md"
if os.path.exists(readme_count_path):
    with open(readme_count_path, encoding="utf-8") as f:
        readme_text = f.read()
    count_match = re.search(r"(\d+)\s+split instruction files? across", readme_text)
    if count_match:
        declared_count = int(count_match.group(1))
        actual_count = len(existing_instructions)
        if declared_count != actual_count:
            print(f"  ERROR: README declares {declared_count} instruction files, but {actual_count} found in .github/instructions/")
            errors += 1
    else:
        print(f"  WARNING: could not find instruction file count in README.md")
        warnings += 1


def validate_labeler_schema(path: str):
    global errors, warnings
    try:
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except yaml.YAMLError:
        return
    if not isinstance(doc, dict):
        print(f"  ERROR: labeler.yml must be a YAML mapping")
        errors += 1
        return
    for label, rules in doc.items():
        if not isinstance(rules, list):
            print(f"  ERROR: labeler rule '{label}' must be a list, got {type(rules).__name__}")
            errors += 1
            continue
        for idx, rule in enumerate(rules):
            if not isinstance(rule, dict):
                print(f"  ERROR: labeler rule '{label}[{idx}]' must be an object, got {type(rule).__name__}")
                errors += 1
                continue
            valid_keys = {"changed-files", "head-branch", "base-branch"}
            if not any(k in rule for k in valid_keys):
                print(f"  ERROR: labeler rule '{label}[{idx}]' missing valid key ({valid_keys})")
                errors += 1
                continue
            if "changed-files" in rule:
                cfs = rule["changed-files"]
                if not isinstance(cfs, list):
                    print(f"  ERROR: labeler '{label}[{idx}].changed-files' must be a list, got {type(cfs).__name__}")
                    errors += 1
                    continue
                for cidx, cf in enumerate(cfs):
                    if not isinstance(cf, dict):
                        print(f"  ERROR: labeler '{label}[{idx}].changed-files[{cidx}]' must be an object, got {type(cf).__name__}")
                        errors += 1
                        continue
                    glob_keys = {"any-glob-to-any-file", "any-glob-to-all-files", "all-globs-to-any-file", "all-globs-to-all-files"}
                    if not any(k in cf for k in glob_keys):
                        print(f"  ERROR: labeler '{label}[{idx}].changed-files[{cidx}]' missing valid glob key ({glob_keys})")
                        errors += 1

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

    # applyTo: required, must be non-empty string or list of non-empty strings
    if "applyTo" not in doc:
        print("  ERROR: missing required field applyTo")
        errors += 1
    elif doc["applyTo"] is None:
        print("  ERROR: applyTo is null")
        errors += 1
    elif isinstance(doc["applyTo"], str):
        if not doc["applyTo"]:
            print("  ERROR: applyTo must be a non-empty string")
            errors += 1
    elif isinstance(doc["applyTo"], list):
        if not doc["applyTo"]:
            print("  ERROR: applyTo list is empty")
            errors += 1
        else:
            for idx, item in enumerate(doc["applyTo"]):
                if not isinstance(item, str) or not item:
                    print(f"  ERROR: applyTo list item {idx} must be a non-empty string, got {type(item).__name__}")
                    errors += 1
    else:
        print(f"  ERROR: applyTo must be a string or list of strings, got {type(doc['applyTo']).__name__}")
        errors += 1

    # excludeAgent: must be scalar string
    if "excludeAgent" in doc:
        ea = doc["excludeAgent"]
        if not isinstance(ea, str) or not ea:
            print(f"  ERROR: excludeAgent must be a non-empty scalar string, got {type(ea).__name__}")
            errors += 1
        elif ea not in ALLOWED_EXCLUDE_AGENTS:
            print(f"  WARNING: excludeAgent value {ea!r} not in known allowlist {ALLOWED_EXCLUDE_AGENTS}")
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
            print(f"  INFO: trusted agent includes 'execute' tool — ensure this is restricted to trusted branches")

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

# Validate review-output contains Diff Coverage
review_output_path = ".github/instructions/review-output.instructions.md"
if os.path.exists(review_output_path):
    print(f"Checking {review_output_path} for Diff Coverage")
    with open(review_output_path, encoding="utf-8") as f:
        review_output_content = f.read()
    if "## Diff Coverage" not in review_output_content:
        print("  ERROR: review-output.instructions.md missing ## Diff Coverage block")
        errors += 1
    else:
        print("  OK")

# Validate agents reference diff-review
for f in sorted(glob.glob(".github/agents/*.agent.md")):
    print(f"Checking {f} references diff-review")
    with open(f, encoding="utf-8") as fh:
        agent_content = fh.read()
    if "diff-review.instructions.md" not in agent_content:
        print("  ERROR: agent does not reference diff-review.instructions.md")
        errors += 1
    else:
        print("  OK")

# Validate copilot-instructions.md
copilot_path = ".github/copilot-instructions.md"
if os.path.exists(copilot_path):
    print(f"Checking {copilot_path}")
    with open(copilot_path, encoding="utf-8") as f:
        copilot_content = f.read()
    check_instruction_references(copilot_path, copilot_content, existing_instructions, strict=True)
    errors += check_size(copilot_path, copilot_content)
    if "diff-review.instructions.md" not in copilot_content:
        print("  ERROR: copilot-instructions.md does not reference diff-review.instructions.md")
        errors += 1
    print("  OK")

# Validate README for stale references and roadmap accuracy
readme_path = "README.md"
if os.path.exists(readme_path):
    print(f"Checking {readme_path}")
    with open(readme_path, encoding="utf-8") as f:
        readme_content = f.read()
    check_instruction_references(readme_path, readme_content, existing_instructions, strict=False)
    if "diff-review.instructions.md" not in readme_content:
        print("  WARNING: README does not reference diff-review.instructions.md")
        warnings += 1
    for line in readme_content.splitlines():
        if line.strip().startswith("- [ ]"):
            for ref in re.findall(r"[\w\-]+\.instructions\.md", line):
                full = os.path.join(".github/instructions", ref)
                if full in existing_instructions:
                    print(f"  WARNING: README roadmap lists unchecked item for existing file: {ref}")
                    warnings += 1
    print("  OK")

# Validate docs and examples links
linked_paths = set()
for root, dirs, files in os.walk("docs"):
    for name in files:
        linked_paths.add(os.path.join(root, name).replace("\\", "/"))
for root, dirs, files in os.walk("examples"):
    for name in files:
        linked_paths.add(os.path.join(root, name).replace("\\", "/"))

for check_path in ["README.md", ".github/copilot-instructions.md"]:
    if not os.path.exists(check_path):
        continue
    with open(check_path, encoding="utf-8") as f:
        content = f.read()
    found_links = re.findall(r"(?:docs|examples)/[\w\-\./]+\.(?:md|patch|yml|yaml)", content)
    for link in set(found_links):
        if link not in linked_paths:
            print(f"  WARNING: {check_path} references missing doc/example: {link}")
            warnings += 1

# Validate GitHub YAML files (workflows, labeler, issue templates)
print("Checking GitHub YAML files")
for pattern in [".github/workflows/*.yml", ".github/workflows/*.yaml", ".github/labeler.yml", ".github/ISSUE_TEMPLATE/*.yml"]:
    for f in sorted(glob.glob(pattern)):
        print(f"  {f}")
        validate_yaml_file(f)

labeler_path = ".github/labeler.yml"
if os.path.exists(labeler_path):
    print(f"Checking {labeler_path} schema (actions/labeler v5)")
    validate_labeler_schema(labeler_path)
    print("  OK")

strict = "--strict-warnings" in sys.argv

if errors:
    print(f"::error::{errors} validation error(s)")
    sys.exit(1)
if warnings:
    print(f"::warning::{warnings} validation warning(s)")
    if strict:
        sys.exit(1)
print("All files validated.")
