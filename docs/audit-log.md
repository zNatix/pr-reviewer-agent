# Audit Log

## 2026-05-08 — Full Repository Audit

**Scope:** All `.github/instructions/*.md`, `.github/agents/*.md`, `.github/workflows/*.yml`, `scripts/`, `examples/`, `docs/`, `README.md`, `CONTRIBUTING.md`.
**Commands run:**
- `python scripts/validate_copilot_config.py` → passed with 4 warnings.
- `git status --short` → clean working tree.
- Manual file reads + subagent deep research on docs, rules, CI, examples.
- Web fetch of official GitHub Copilot docs and changelog (Nov 12 2025).

**Key findings (see implementation plan for fixes):**
1. Smoke tests documented but never executed; README claims v1.1 complete.
2. GitHub Actions workflows use mutable tags instead of pinned SHA.
3. `CONTRIBUTING.md` contradicts itself on `excludeAgent` scalar vs array.
4. Validator script allows invalid `applyTo` types and weak frontmatter parsing.
5. Rule contradictions across Appium waits, Playwright selectors, HttpClient severity, EF Core `IQueryable` boundary.
6. Examples contain “good” code that violates current instructions.
7. Missing coverage for secrets in config files and XSS in Razor/JS.
8. No Dependabot configuration for action updates.

**Contrast with external sources:**
- GitHub official docs confirm `excludeAgent` values: `"code-review"`, `"cloud-agent"`, `"coding-agent"`.
- GitHub Actions hardening guide mandates full commit SHA pinning as the only immutable reference.
- Path-specific instructions support varies by client (GitHub.com vs IDE).

**Result:** Implementation plan created and approved.
