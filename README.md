# 🔍 PR Reviewer Agent for GitHub Copilot

> A specialized GitHub Copilot custom agent that reviews pull requests with expert-level scrutiny — built for **C# / .NET / Reqnroll / Gherkin / NUnit / Playwright / Appium** projects.

![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Agent-8A2BE2?logo=github)
![Platform](https://img.shields.io/badge/Platform-GitHub.com%20%7C%20VS%20Code%20%7C%20Visual%20Studio-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Audited](https://img.shields.io/badge/Audited-2x_✅-success)

---

## What is this?

A **production-oriented template** for GitHub Copilot that acts as your automated first-pass code reviewer. Drop it into any C# repository on **Copilot Business or Enterprise** and Copilot will gain a senior reviewer persona with 15 years of .NET experience.

The agent catches what humans miss — unhandled edge cases, security vulnerabilities, EF Core anti-patterns, missing BDD step definitions — while respecting your team's standards.

### Key Features

| Feature | Description |
|---|---|
| **27 split instruction files across 18 review domains** | Security, architecture, performance, logging, DI, NUnit, xUnit, MSTest, Gherkin, Reqnroll, Playwright, Appium, API design, GitHub Actions, supply chain, diff coverage |
| **Diff Coverage contract** | Structured Diff Map with causal Review Chapters and mandatory hunk coverage before findings |
| **Token budget controls** | 25-file cap, skip auto-generated code, Dependabot fast-path, 30-finding max |
| **Prompt injection defense** | Rejects malicious instructions embedded in code comments, READMEs, or PR descriptions |
| **Dual-mode support** | Works as both automatic Code Review (lightweight, every PR) and `@pr-reviewer` Chat agent (deep 8-step review) |
| **BDD traceability** | Best-effort Gherkin ↔ step definition matching with honest capabilities disclaimer |
| **Stack-adaptable** | Drop-in compatible with xUnit, MSTest, SpecFlow, Dapper, Selenium — see adaptation guide below |

---

## Two Modes of Operation

This repo supports **two distinct Copilot features**. They work differently — understand which you're using:

| | **Automatic Code Review** | **@pr-reviewer Custom Agent** |
|---|---|---|
| **How it runs** | Automatically when you open a PR | Manually invoked via `@pr-reviewer` in Copilot Chat |
| **What it reads** | `copilot-instructions.md` + `instructions/*.md` | `agents/pr-reviewer.agent.md` + `instructions/*.md` |
| **Depth** | Fast, inline comments | Deep 8-step review with diff analysis, BDD traceability, context search |
| **Output** | Inline PR comments | Structured summary + findings per file |
| **Best for** | Every PR, quick feedback | Complex PRs, security reviews, architecture changes |

> ⚠️ **Important**: The 8-step review process, BDD traceability, and specialized tooling (`search`/`execute`) only work in **@pr-reviewer Chat mode**. Automatic Code Review provides a lighter pass using the same instruction files but without the agent persona.

### Compatibility Matrix

| Client | Repo-wide instructions | Path-specific instructions | Custom agent (`@pr-reviewer`) |
|---|---|---|---|
| GitHub.com Code Review | Yes | Yes | Depends on mode support |
| VS Code Code Review | Yes | Limited in some modes | Depends on IDE support |
| Visual Studio Code Review | Yes | Limited | Depends on IDE support |
| JetBrains Code Review | Yes | Yes | Depends on IDE support |
| Eclipse | Limited | No | No |

> Behavior may vary between clients. Test in your target environment after installation.

---

## Quick Start

```bash
git clone https://github.com/zNatix/pr-reviewer-agent.git
cp -rn pr-reviewer-agent/.github/ /path/to/your-repo/.github/
# -n = no-clobber: won't overwrite existing files
git add .github && git commit -m "feat: add Copilot PR reviewer agent"
git push
```

Done. Invoke it as `@pr-reviewer` in Copilot Chat on **GitHub.com**, **VS Code**, or **Visual Studio**.

For automatic reviews on every PR, enable **Copilot Code Review** in your repository or organization settings. This is external configuration — not included in this template.

### See it in action
- `examples/archive/sample-pr-diff.patch` — a PR with 16 deliberately injected bugs
- `examples/archive/sample-review-output.md` — the agent's review catching all 16
- `examples/archive/sample-diff-coverage-output.md` — Diff Coverage + Review Chapters + Human Judgment Questions example
- `examples/{domain}/bad-*.md` and `examples/{domain}/good-*.md` — bad vs good code pairs by domain

---

## What it reviews

| Priority | Category | Examples |
|---|---|---|
| 🔴 **Critical** | Security | SQL injection, hardcoded secrets, auth bypass, insecure deserialization, SSRF, path traversal |
| 🟡 **Warning** | Reliability | Missing error handling, missing tests, N+1 queries, `.Result` calls, resilience gaps |
| 🔵 **Suggestion** | Quality | Naming conventions, code duplication, LINQ simplifications, XML docs |

### Test Automation Support

The agent also reviews Playwright and Appium test code:

| Tool | What it checks |
|---|---|
| **Playwright** | Locator strategy (role > label > testid > CSS — never XPath), web-first assertions vs manual waits, base class lifecycle (`PageTest`/`ContextTest`), test isolation, API mocking, no `.Result` on async ops |
| **Appium** | Driver lifecycle (`Quit`/`Dispose` in tear down), externalized capabilities, explicit waits vs `Thread.Sleep`, `AccessibilityId` priority over XPath, W3C Actions over deprecated `TouchAction`, parallel execution port config |

### Review Process (8 steps)
1. **Understand intent** (PR description + linked work items + Gherkin features)
2. **Diff analysis** (file by file, cascading impact)
3. **Context check** (search codebase for affected callers, DI registrations, configs)
4. **BDD traceability** (best-effort — Gherkin ↔ step definitions via grep + dotnet test listing)
5. **Test quality** (happy path + edge cases + failure modes)
6. **Security scan** (OWASP Top 10 + deserialization, SSRF, ReDoS, open redirect, mass assignment)
7. **Performance** (allocations, async misuse, EF Core anti-patterns, resilience, rate limiting)
8. **Standards enforcement** (SOLID, DRY, DI, logging, Microsoft conventions)

---

## File structure

```
.github/
├── copilot-instructions.md                      # Repo-wide standards (all Copilot interactions)
├── agents/
│   ├── pr-reviewer.agent.md                     # ✨ The reviewer agent (safe, no execute)
│   └── pr-reviewer-trusted.agent.md             # Deep reviewer for trusted branches (execute allowed)
└── instructions/
    ├── review-output.instructions.md            # Output format, severity tiers, summary template, Diff Coverage
    ├── diff-review.instructions.md              # Diff Map, causal Review Chapters, hunk coverage, human judgment questions
    ├── security-injection.instructions.md       # SQL injection, XSS, input validation, path traversal, ReDoS
    ├── security-auth.instructions.md            # Auth, secrets, deserialization, SSRF, open redirect
    ├── security-warnings.instructions.md        # Crypto, headers, cookies, dependencies
    ├── secrets.instructions.md                  # Secret scanning, hardcoded credentials, connection strings
    ├── architecture-core.instructions.md        # SOLID, DRY, DI, project structure, code quality
    ├── architecture-patterns.instructions.md    # Nullable, records, IAsyncEnumerable
    ├── performance-critical.instructions.md     # EF Core, async, memory, HTTP
    ├── performance-warnings.instructions.md     # Collections, LINQ, logging, concurrency, resilience
    ├── gherkin.instructions.md                  # Feature file syntax, Given-When-Then, tags
    ├── reqnroll.instructions.md                 # Step definitions, hooks, Reqnroll-specific DI
    ├── nunit.instructions.md                    # Test naming, assertions, parallel execution, timeouts
    ├── xunit.instructions.md                    # Traits, fixtures, TheoryData, member data
    ├── mstest.instructions.md                   # TestMethod, DataRow, TestInitialize, DeploymentItem
    ├── logging.instructions.md                  # ILogger<T>, structured logging, no PII, source gen
    ├── di.instructions.md                       # Constructor injection, lifetimes, captive deps, keyed services
    ├── efcore.instructions.md                   # Querying, tracking, batching, migrations, compiled queries
    ├── playwright-base.instructions.md          # Base classes, locators, assertions
    ├── playwright-actions.instructions.md       # Actions, network mocking, file upload, screenshots
    ├── playwright-anti-patterns.instructions.md # Anti-patterns and common mistakes
    ├── appium-lifecycle.instructions.md         # Drivers, capabilities, lifecycle
    ├── appium-locators.instructions.md          # Waits, locators, context switching
    ├── appium-gestures.instructions.md          # Gestures, device interaction, anti-patterns
    ├── api-design.instructions.md               # HTTP semantics, pagination, idempotency, DTOs
    ├── github-actions.instructions.md           # Workflow security, permissions, SHA pinning
    └── supply-chain.instructions.md             # NuGet, Docker, deterministic builds, typosquatting
```

### How the files work together

| File | Scope | Read by |
|---|---|---|
| `copilot-instructions.md` | All PRs, all agents | Code Review + Coding Agent + Chat |
| `*.instructions.md` | Per file type (via `applyTo`) | Code Review + Chat. Coding Agent excluded in this template — remove `excludeAgent` field from frontmatter if you want Coding Agent to honor them too |
| `pr-reviewer.agent.md` | When `@pr-reviewer` is invoked | Custom agent persona only |

---

## Adapt to Your Stack

### Minimal customization checklist (<1 hour)

1. **Edit `pr-reviewer.agent.md`**: update the model if needed (see [supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models))
2. **Adjust `copilot-instructions.md`**: replace `Company.Project.Layer` naming with your conventions
3. **Review security instruction files**: add your specific compliance requirements to `security-injection.instructions.md`, `security-auth.instructions.md`, and `security-warnings.instructions.md`
4. **Test**: open a test PR and invoke `@pr-reviewer` in Copilot Chat

### Stack variations

| Your framework | Change |
|---|---|
| **xUnit instead of NUnit** | Keep `nunit.instructions.md` for reference; add `xunit.instructions.md` (naming, assertions, `IClassFixture`, `[Theory]`) |
| **MSTest** | Keep `nunit.instructions.md` for reference; add `mstest.instructions.md` (`[TestMethod]`, `[DataRow]`, `[TestInitialize]`) |
| **SpecFlow (not Reqnroll)** | Rename `reqnroll.instructions.md`; update namespaces to `TechTalk.SpecFlow` |
| **Dapper (not EF Core)** | Keep `efcore.instructions.md` for reference but add `dapper.instructions.md` |
| **Minimal APIs** | Add `api-design.instructions.md` with endpoint conventions |
| **No BDD** | Remove `gherkin.instructions.md` and `reqnroll.instructions.md` |
| **Selenium (not Playwright)** | Replace Playwright instruction files; add Selenium-specific rules |
| **No mobile testing** | Remove Appium instruction files |

---

## Token Budget

The agent enforces a **25-file cap per review** to control AI credit consumption:
- Skips auto-generated files (`*.Designer.cs`, `*.g.cs`, `*.generated.cs`, EF migrations)
- Reviews in priority order on large PRs; un-reviewed files are listed explicitly
- Dependabot PRs get security-only review (skips BDD traceability + test quality)
- Findings capped at 30 items for readability

For detailed thresholds and cost-aware policies, see [`docs/review-budget.md`](docs/review-budget.md).

---

## Known Limitations

Be honest about what this agent can and can't do. These are not bugs — they're design trade-offs.

| Limitation | Impact | Mitigation |
|---|---|---|
| **BDD traceability is grep-based, not AST-resolved** | May miss step definition matches when `[Scope]` attribute is used or Cucumber expressions are complex | Run `dotnet test --list-tests` as supplementary check (the agent will try this if Reqnroll project detected) |
| **Instruction files split to stay under Copilot Code Review's 4KB-per-file context limit** | Files are now split so each stays below the limit. Verify with `scripts/validate_copilot_config.py` | Keep new files under 3,800 characters |
| **`excludeAgent: "coding-agent"` behavior partially smoke-tested** | The Nov 12 2025 changelog documents `"coding-agent"`, but current GitHub docs list only `"code-review"` and `"cloud-agent"`. See [`docs/smoke-tests.md`](docs/smoke-tests.md) for the test matrix. Behavior may vary by client. | Run the tests in your target environment and report results |
| **Not tested on PRs >100 files** | Token budget caps at 25 files — the rest are listed as skipped. On massive PRs, important changes may be in the skipped portion | Split large PRs; the agent will list skipped files explicitly |
| **Severity tiers are guidance, not enforcement** | LLM non-determinism: the agent may classify the same bug as 🟡 Warning on one run and 🔴 Critical on another | Use as first-pass triage, not final gate. Human reviewer always has final say |
| **No CI status checking** | The agent cannot verify if CI is green — it will remind you to check manually | Enable branch protection rules with required checks in GitHub |
| **No coverage of Selenium, Cypress, or other test frameworks** | Only Playwright and Appium have dedicated rule files. Other frameworks get only the universal C# rules | Add your own `selenium.instructions.md`, `cypress.instructions.md`, etc. following the same pattern |

---

## Roadmap

### v1.0 ✅ (current)
- [x] 18 review domains / 27 split instruction files implemented
- [x] Token budget with scoping, Dependabot fast-path, skip patterns
- [x] Dual-mode documentation (Automatic Code Review vs `@pr-reviewer` Chat)
- [x] Prompt injection defense
- [x] Iterative architecture/security audits with external feedback
- [x] Stack adaptation guide (xUnit, MSTest, SpecFlow, Dapper, Selenium, Minimal APIs)

### v1.0.1 ✅ (current patch)
- [x] Fix `model` frontmatter to string (was array)
- [x] Remove `execute` from default agent; create `pr-reviewer-trusted` agent
- [x] Split instruction files to stay under 4KB Copilot Code Review limit
- [x] Fix `excludeAgent` to scalar string
- [x] Add compatibility matrix to README
- [x] Add CI validation script with PyYAML pinning and size checks
- [x] Migrate custom agents from `gpt-5.2-codex` to omitted model
- [x] Remove stale references to old consolidated instruction files
- [x] Document smoke tests for `excludeAgent`, custom agents and path-specific review
- [x] Add semantic validation for stale file references and deprecated models
- [x] Add `api-design.instructions.md`
- [x] Add `github-actions.instructions.md` and `supply-chain.instructions.md`
- [x] Add review budget policy for large PRs and cost-aware review
- [x] Add `diff-review.instructions.md` with Diff Map, Review Chapters, and Human Judgment Questions
> Smoke tests are documented in `docs/smoke-tests.md`; empirical execution across clients is pending.

### v1.1 🚧 (pending empirical validation)
- [ ] Run smoke tests across GitHub.com, VS Code, Visual Studio, JetBrains and record results
- [x] Document automatic Copilot Code Review setup via GitHub rulesets/settings
- [x] Optional workflow for PR labeling and instruction validation
- [x] xUnit and MSTest instruction files
- [ ] Expand `examples/` into bad-PR/good-PR pairs by domain (partial — selected domains only)
- [x] Issue templates for false positives, missed findings and rule requests

### v2.0-template
- [ ] Monorepo support
- [ ] Sub-agent composition
- [ ] Rule packs by stack
- [ ] Feedback-loop documentation

### v2.0-product
- [ ] GitHub Checks API inline annotations
- [ ] GitHub App or Action runtime
- [ ] Azure DevOps integration
- [ ] Metrics and reporting

---

## Requirements

- **GitHub Copilot Business** or **Enterprise** plan
- Copilot Code Review enabled in organization policies (for automatic mode)
- Repository language: **C# / .NET** — covers Reqnroll, NUnit, Playwright, Appium, EF Core, ASP.NET Core (adaptable to other stacks)

---

## Contributing

This is a template — fork it, adapt it to your stack, and share improvements via PR. Contributions for additional test frameworks (xUnit, MSTest), BDD tools (SpecFlow, Cucumber), or language stacks are welcome.

---

## License

MIT — use it, fork it, adapt it to your team. No attribution required (but appreciated).

---

*Built with iterative feedback from multiple architecture/security audits and verified against official GitHub Copilot documentation. `excludeAgent` field documented in [changelog (Nov 12, 2025)](https://github.blog/changelog/2025-11-12-copilot-code-review-and-coding-agent-now-support-agent-specific-instructions/).*
