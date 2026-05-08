---
version: "1.0.0"
applyTo: [".github/workflows/*.yml", ".github/workflows/*.yaml"]
excludeAgent: "coding-agent"
---

# GitHub Actions Security Rules

## 🔴 Critical — Block Merge

### Dangerous Triggers
- `pull_request_target` with checkout of untrusted code — flag unless explicitly justified and hardened
- `workflow_dispatch` with no input validation when the workflow has write permissions

### Secrets & Permissions
- Never echo secrets or pass them as command-line arguments
- `permissions` block must be present and minimal; default `write-all` or missing `permissions` is a blocker
- Workflows that run on forks must not access repository secrets unless using `pull_request_target` with trusted base ref only

### Unpinned Actions
- All third-party actions must be pinned by full commit SHA (not tag) — e.g., `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`
- Exception: `actions/*` and `github/*` official actions may use version tags if SHA pinning is not org-mandated

## 🟡 Warning — Should Fix

### Runner & Environment
- `runs-on: self-hosted` without labels that restrict to trusted runners
- `ubuntu-latest` is acceptable but consider pinning to a specific version for reproducibility

### Artifact Handling
- Uploading build artifacts from untrusted PRs without sandboxing — sanitize filenames to prevent path traversal in artifact names

### Code Injection
- Avoid `${{ github.event.pull_request.title }}` or body in `run:` scripts without sanitization — use environment variables instead

## 🔵 Suggestion — Approve with Nits

- Use `concurrency` blocks to cancel redundant runs
- Separate `build` and `deploy` jobs with explicit dependency via `needs`
