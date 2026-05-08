# Smoke Tests

> Empirical validation matrix for `excludeAgent`, custom agents, path-specific instructions, and model loading.
> Last updated: 2026-05-08

## Environment

- Repository: `zNatix/pr-reviewer-agent`
- GitHub Copilot plan: Business or Enterprise
- Target clients: GitHub.com, VS Code, Visual Studio, JetBrains

## Test Matrix

| ID | Test | Objective | Steps | Expected Result | Status |
|---|---|---|---|---|---|---|
| ST-01 | Code Review path-specific instructions | Verify `.instructions.md` files with `applyTo` are honored in automatic Code Review | 1. Open a PR that changes `**/*.cs` files.<br>2. Ensure `security-injection.instructions.md` has `applyTo` matching those files. | Copilot Code Review flags injection-related issues on changed `.cs` files. | Not run |
| ST-02 | Coding Agent exclusion | Verify `excludeAgent: "coding-agent"` prevents instruction contamination during code generation | 1. Open Copilot Chat in IDE.<br>2. Ask Coding Agent to generate code that violates a rule present **only** in `.github/instructions/*.md` (e.g., Playwright XPath locator from `playwright-base.instructions.md`), not in `copilot-instructions.md`.<br>3. Observe whether the generated code follows the rule or not. | Coding Agent generates code without being constrained by review-only rules. | Not run |
| ST-03 | Custom agent `@pr-reviewer` loads safely | Confirm safe agent loads without `execute` | 1. In Copilot Chat, invoke `@pr-reviewer`.<br>2. Ask it to review a PR diff. | Agent responds, uses `read` and `search`, does not offer `execute`. | Not run |
| ST-04 | Trusted agent `@pr-reviewer-trusted` loads with `execute` | Confirm trusted profile includes `execute` and documents restrictions | 1. In Copilot Chat, invoke `@pr-reviewer-trusted`.<br>2. Verify it lists `execute` in available tools. | Agent shows `execute` tool and includes warning about trusted branches only. | Not run |
| ST-05a | IDE parity — GitHub.com | Document findings on GitHub.com Code Review | 1. Run ST-01 on GitHub.com.<br>2. Record findings and severity alignment. | Results documented in Results Log. | Not run |
| ST-05b | IDE parity — VS Code | Document findings in VS Code Copilot Code Review panel | 1. Run ST-01 in VS Code.<br>2. Record findings and severity alignment. | Results documented in Results Log. | Not run |
| ST-05c | IDE parity — Visual Studio | Document findings in Visual Studio | 1. Run ST-01 in Visual Studio.<br>2. Record findings and severity alignment. | Results documented in Results Log. | Not run |
| ST-05d | IDE parity — JetBrains | Document findings in JetBrains IDEs | 1. Run ST-01 in JetBrains.<br>2. Record findings and severity alignment. | Results documented in Results Log. | Not run |
| ST-06 | Model loading | Verify agent loads with omitted model and no deprecated model warnings | 1. Load `@pr-reviewer` and `@pr-reviewer-trusted`.<br>2. Check that no deprecated model (e.g., `gpt-5.2-codex`) is referenced.<br>3. Confirm client-selected model is visible/acceptable. | Agent loads without model warnings. | Not run |

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
3. Open a test PR with deliberate issues (see `examples/archive/sample-pr-diff.patch`).
4. Trigger Copilot Code Review or `@pr-reviewer` in your preferred client.
5. Record results in the **Results Log** above and open a PR to update this file.
