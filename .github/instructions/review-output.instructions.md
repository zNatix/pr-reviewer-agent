---
applyTo: "**"
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Code Review Output Format

This file defines the output format for ALL code review agents and Copilot Code Review (automatic) in this repository.

## Finding Format

For each finding, use this exact format:

```
**Location**: `File.cs:line`
**Severity**: 🔴 Critical / 🟡 Warning / 🔵 Suggestion
**Issue**: Concise one-line description
**Why it matters**: 1-2 sentences on the impact
**Fix**: Code example of the fix (if applicable)
**Reference**: Link to official docs or team standard (if applicable)
```

Group findings by file. Summarize at the top with an overall verdict.

## Diff Coverage (mandatory)

Before findings, include a Diff Coverage block that proves every changed hunk was considered:

```
## Diff Coverage
- Files changed: X
- Files reviewed: X
- Files skipped: X (list with reason)
- Changed hunks reviewed: X
- Skipped hunks: X (list with reason)

### Review Chapters
1. **Title** — files/hunks covered
2. ...

### Human Judgment Questions
- Question (location)
```

Rules:
- Every changed file must appear under reviewed or skipped.
- Every changed hunk must be accounted for exactly once.
- Skipped files/hunks need a reason matching `diff-review.instructions.md`.
- Human judgment questions only for decisions a human must make; bugs go into findings.

## Summary Template

At the end of every review, include:

```
## Review Summary
- Files reviewed: X
- 🔴 Critical: X (must fix before merge)
- 🟡 Warnings: X (should fix before merge)
- 🔵 Suggestions: X (address at your discretion)
- BDD coverage: Gherkin scenarios matched / unmatched step definitions
- Missing tests: X uncovered paths detected

### Verdict: ✅ Approve / ⚠️ Approve with Comments / ❌ Request Changes
```

## Severity Definitions

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 Critical | Security vulnerability, data loss, broken contracts, hardcoded secrets | **Must fix before merge** |
| 🟡 Warning | Missing tests, error handling gaps, performance regressions, deprecated APIs | **Should fix before merge** |
| 🔵 Suggestion | Naming conventions, code style, LINQ simplifications, minor DRY opportunities | **Address at team's discretion** |
