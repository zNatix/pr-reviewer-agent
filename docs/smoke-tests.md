# Smoke Tests

> Empirical validation matrix for `excludeAgent`, custom agents, path-specific instructions, and model loading.
> Last updated: 2026-05-08

## Environment

- Repository: `zNatix/pr-reviewer-agent`
- GitHub Copilot plan: Business or Enterprise
- Target clients: GitHub.com, VS Code, Visual Studio, JetBrains

## Test Matrix

| ID | Test | Objective | Steps | Expected Result | Status |
|---|---|---|---|---|---|
| ST-01 | Code Review path-specific instructions | Verify `.instructions.md` files with `applyTo` are honored in automatic Code Review | 1. Open a PR that changes `**/*.cs` files.<br>2. Ensure `security-injection.instructions.md` has `applyTo: "**/*.cs"`. | Copilot Code Review flags injection-related issues on changed `.cs` files. | Not run |
| ST-02 | Coding Agent exclusion | Verify `excludeAgent: "coding-agent"` prevents instruction contamination during code generation | 1. Open Copilot Chat in IDE.<br>2. Ask Coding Agent to generate a method that violates a rule (e.g., `new HttpClient()`).<br>3. Observe whether the generated code follows the rule or not. | Coding Agent generates code without being constrained by review-only rules. | Not run |
| ST-03 | Custom agent `@pr-reviewer` loads safely | Confirm safe agent loads without `execute` | 1. In Copilot Chat, invoke `@pr-reviewer`.<br>2. Ask it to review a PR diff. | Agent responds, uses `read` and `search`, does not offer `execute`. | Not run |
| ST-04 | Trusted agent `@pr-reviewer-trusted` loads with `execute` | Confirm trusted profile includes `execute` and documents restrictions | 1. In Copilot Chat, invoke `@pr-reviewer-trusted`.<br>2. Verify it lists `execute` in available tools. | Agent shows `execute` tool and includes warning about trusted branches only. | Not run |
| ST-05 | IDE parity check | Document differences between GitHub.com and IDE behavior | 1. Run ST-01 on GitHub.com.<br>2. Run ST-01 in VS Code Copilot Code Review panel.<br>3. Compare findings. | Differences (if any) are documented in the table below. | Not run |

## Results Log

| Date | Environment | Test ID | Result | Notes |
|---|---|---|---|---|
| 2026-05-08 | — | — | — | No live tests executed yet. Fill this table after testing. |

## Known Client Differences

| Feature | GitHub.com | VS Code | Visual Studio | JetBrains |
|---|---|---|---|---|
| Path-specific instructions | Supported | Limited in some modes | Limited | Supported |
| Custom agents (`@pr-reviewer`) | Supported | Depends on IDE support | Depends on IDE support | Depends on IDE support |
| Automatic Code Review | Supported | N/A | N/A | N/A |

## How to Run

1. Fork this repository into a private test repo.
2. Copy `.github/` to the test repo.
3. Open a test PR with deliberate issues (see `examples/sample-pr-diff.patch`).
4. Trigger Copilot Code Review or `@pr-reviewer` in your preferred client.
5. Record results in the **Results Log** above and open a PR to update this file.
