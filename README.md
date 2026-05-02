# 🔍 PR Reviewer Agent for GitHub Copilot

> A specialized GitHub Copilot custom agent that reviews pull requests with expert-level scrutiny — built for **C# / .NET / Reqnroll / Gherkin / NUnit / Playwright / Appium** projects.

![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Agent-8A2BE2?logo=github)
![Platform](https://img.shields.io/badge/Platform-GitHub.com%20%7C%20VS%20Code%20%7C%20Visual%20Studio-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Audited](https://img.shields.io/badge/Audited-2x_✅-success)

---

## What is this?

A production-ready **custom agent** for GitHub Copilot that acts as your automated first-pass code reviewer. Drop it into any C# repository on **Copilot Business or Enterprise** and Copilot will gain a senior reviewer persona with 15 years of .NET experience.

The agent catches what humans miss — unhandled edge cases, security vulnerabilities, EF Core anti-patterns, missing BDD step definitions — while respecting your team's standards.

### Key Features

| Feature | Description |
|---|---|
| **12 domain-specific rule files** | Security (OWASP + deserialization/SSRF/ReDoS), architecture (SOLID/nullability), performance (EF Core/async/resilience), logging, DI, NUnit, Gherkin, Reqnroll, Playwright, Appium |
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

For automatic reviews on every PR, enable **Copilot Code Review** in your repository settings.

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
├── copilot-instructions.md                # Repo-wide standards (all Copilot interactions)
├── agents/
│   └── pr-reviewer.agent.md               # ✨ The reviewer agent (persona + process)
└── instructions/
    ├── review-output.instructions.md      # Output format, severity tiers, summary template
    ├── security.instructions.md           # OWASP, auth, secrets, deserialization, SSRF, ReDoS
    ├── architecture.instructions.md       # SOLID, DRY, DI, project structure, code quality
    ├── performance.instructions.md        # EF Core, async, memory, HTTP, resilience, rate limiting
    ├── gherkin.instructions.md            # Feature file syntax, Given-When-Then, tags
    ├── reqnroll.instructions.md           # Step definitions, hooks, Reqnroll-specific DI
    ├── nunit.instructions.md              # Test naming, assertions, parallel execution, timeouts
    ├── logging.instructions.md            # ILogger<T>, structured logging, no PII, source gen
    ├── di.instructions.md                 # Constructor injection, lifetimes, captive deps, keyed services
    ├── efcore.instructions.md             # Querying, tracking, batching, migrations, compiled queries
    ├── playwright.instructions.md         # Locators, assertions, base classes, lifecycle, anti-patterns
    └── appium.instructions.md             # Drivers, capabilities, waits, gestures, mobile lifecycle
```

### How the files work together

| File | Scope | Read by |
|---|---|---|
| `copilot-instructions.md` | All PRs, all agents | Code Review + Coding Agent + Chat |
| `*.instructions.md` | Per file type (via `applyTo`) | Code Review + Coding Agent (unless `excludeAgent` excludes) |
| `pr-reviewer.agent.md` | When `@pr-reviewer` is invoked | Custom agent persona only |

---

## Adapt to Your Stack

### Minimal customization checklist (<1 hour)

1. **Edit `pr-reviewer.agent.md`**: update the model if needed (see [supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models))
2. **Adjust `copilot-instructions.md`**: replace `Company.Project.Layer` naming with your conventions
3. **Review `security.instructions.md`**: add your specific compliance requirements
4. **Test**: open a test PR and invoke `@pr-reviewer` in Copilot Chat

### Stack variations

| Your framework | Change |
|---|---|
| **xUnit instead of NUnit** | Replace `nunit.instructions.md` with xUnit equivalent (naming, assertions, traits) |
| **MSTest** | Replace `nunit.instructions.md`; update test categories |
| **SpecFlow (not Reqnroll)** | Rename `reqnroll.instructions.md`; update namespaces to `TechTalk.SpecFlow` |
| **Dapper (not EF Core)** | Keep `efcore.instructions.md` for reference but add `dapper.instructions.md` |
| **Minimal APIs** | Add `api-design.instructions.md` with endpoint conventions |
| **No BDD** | Remove `gherkin.instructions.md` and `reqnroll.instructions.md` |
| **Selenium (not Playwright)** | Replace `playwright.instructions.md`; add Selenium-specific rules |
| **No mobile testing** | Remove `appium.instructions.md` |

---

## Token Budget

The agent enforces a **25-file cap per review** to control AI credit consumption:
- Skips auto-generated files (`*.Designer.cs`, `*.g.cs`, `*.generated.cs`, EF migrations)
- Reviews in priority order on large PRs; un-reviewed files are listed explicitly
- Dependabot PRs get security-only review (skips BDD traceability + test quality)
- Findings capped at 30 items for readability

---

## Roadmap

### v1.0 ✅ (current)
- [x] 12 domain-specific instruction files (security, architecture, performance, logging, DI, EF Core, NUnit, Gherkin, Reqnroll, Playwright, Appium, review-output)
- [x] Token budget with scoping, Dependabot fast-path, skip patterns
- [x] Dual-mode documentation (Automatic Code Review vs `@pr-reviewer` Chat)
- [x] Prompt injection defense
- [x] 2x independent architecture audits (6.5/10 → 8.5/10)
- [x] Stack adaptation guide (xUnit, MSTest, SpecFlow, Dapper, Selenium, Minimal APIs)

### v1.0.1 (next patch)
- [ ] `api-design.instructions.md` (versioning, ProblemDetails, pagination, ETag)
- [ ] Supply chain security rules (lockfile verification, typosquatting, signed packages)
- [ ] Token budget refinement: byte-cap for PRs >100 changed files

### v1.1
- [ ] GitHub Actions workflow for automated PR review on every PR
- [ ] Auto-labeling suggestions (`size/L`, `breaking-change`, `needs-migration`)
- [ ] xUnit and MSTest instruction files
- [ ] `examples/` folder with bad-PR/good-PR for customization onboarding

### v2.0
- [ ] Integration with GitHub Checks API for inline annotations
- [ ] Sub-agents for specialized reviews (security-only, perf-only)
- [ ] Monorepo support (multi-language gating based on diff contents)
- [ ] Feedback loop: issue template for reporting false positives
- [ ] Integration with Azure DevOps work items

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

*Built with feedback from two independent architecture audits (v1: 6.5/10, v2: 8.5/10) and verified against official GitHub Copilot documentation (custom agents, supported models, instructions format). Model `gpt-5.2-codex` confirmed in [supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models) and [OpenAI Codex agent docs](https://docs.github.com/en/copilot/concepts/agents/openai-codex).*
