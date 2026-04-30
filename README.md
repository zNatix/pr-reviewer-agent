# 🔍 PR Reviewer Agent for GitHub Copilot

> A specialized GitHub Copilot custom agent that reviews pull requests with expert-level scrutiny — built for **C# / .NET / Reqnroll / Gherkin / NUnit** projects.

![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Agent-8A2BE2?logo=github)
![Platform](https://img.shields.io/badge/Platform-GitHub.com%20%7C%20VS%20Code%20%7C%20Visual%20Studio-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What is this?

A production-ready **custom agent** for GitHub Copilot that acts as your automated first-pass code reviewer. Drop it into any C# repository on **Copilot Business or Enterprise** and Copilot will gain a senior reviewer persona with 15 years of .NET experience.

The agent catches what humans miss — unhandled edge cases, security vulnerabilities, EF Core anti-patterns, missing BDD step definitions — while respecting your team's standards.

---

## Quick Start

```bash
git clone https://github.com/zNatix/pr-reviewer-agent.git
cp -r pr-reviewer-agent/.github /path/to/your-repo/
git add .github && git commit -m "feat: add Copilot PR reviewer agent"
git push
```

Done. Invoke it anywhere as `@pr-reviewer` in Copilot Chat on **GitHub.com**, **VS Code**, or **Visual Studio**.

---

## What it reviews

| Priority | Category | Examples |
|---|---|---|
| 🔴 **Critical** | Security | SQL injection, hardcoded secrets, auth bypass, missing step definitions |
| 🟡 **Warning** | Reliability | Missing error handling, missing tests, N+1 queries, `.Result` calls |
| 🔵 **Suggestion** | Quality | Naming conventions, code duplication, LINQ simplifications, XML docs |

### Review Process (8 steps)
1. Understand intent (PR description + linked work items + Gherkin features)
2. Diff analysis (file by file, cascading impact)
3. Context check (search codebase for affected callers, DI registrations, configs)
4. **BDD traceability** (Gherkin ↔ step definitions)
5. Test quality (happy path + edge cases + failure modes)
6. Security scan (OWASP Top 10)
7. Performance (allocations, async misuse, EF Core patterns)
8. Standards enforcement (SOLID, DRY, Microsoft conventions)

---

## File structure

```
.github/
├── copilot-instructions.md                # Repo-wide standards
├── agents/
│   └── pr-reviewer.agent.md               # ✨ The reviewer agent
└── instructions/
    ├── security.instructions.md           # OWASP, auth, secrets
    ├── gherkin.instructions.md            # Feature files, Given-When-Then
    ├── nunit.instructions.md              # Test naming, assertions, categories
    ├── performance.instructions.md        # EF Core, async, memory, LINQ, HTTP
    └── architecture.instructions.md       # SOLID, DRY, DI, project structure
```

### How the files work together

| File | Scope | Read by |
|---|---|---|
| `copilot-instructions.md` | All PRs, all agents | Code Review + Coding Agent |
| `security.instructions.md` | All `.cs` files | **Code Review only** (`excludeAgent: cloud-agent`) |
| `gherkin.instructions.md` | All `.feature` files | **Code Review only** |
| `nunit.instructions.md` | All `.cs` files | **Code Review only** |
| `performance.instructions.md` | All `.cs` files | **Code Review only** |
| `architecture.instructions.md` | All `.cs` files | **Code Review only** |
| `pr-reviewer.agent.md` | When `@pr-reviewer` is invoked | Available as custom agent persona |

---

## Key design decisions

### Why `excludeAgent: cloud-agent` everywhere?
Instruction files are for **code review only**. The coding agent shouldn't follow the same strict rules when generating code — it would become too constrained. If you want coding style rules for code generation, create separate instruction files without `excludeAgent`.

### Why Gherkin traceability is a 🔴 Critical?
Reqnroll scenarios without matching step definitions are dead code. Step definitions without matching scenarios are untested code. The reviewer enforces bidirectional traceability on every PR that touches `.feature` or step definition files.

### Why `gpt-5.2-codex`?
It balances review quality with cost (as of April 2026). For teams wanting deeper security analysis, switch the `model:` field to `claude-sonnet-4.6` in `pr-reviewer.agent.md`. For lighter/faster reviews, switch to `gpt-5-mini`.

---

## Customization

### Adapt to your team

Edit `pr-reviewer.agent.md` and update the **Project-Specific Rules** section:

```markdown
## Project-Specific Rules
- Tech Stack: [your stack]
- Test framework: [xUnit / NUnit / MSTest]
- CI/CD: [GitHub Actions / Azure DevOps / Jenkins]
- Never approve PRs that: [your team's red lines]
```

### Add your own rules

Create new `*.instructions.md` files in `.github/instructions/`:

```markdown
---
applyTo: "src/api/**/*.cs"
excludeAgent: "cloud-agent"
---

# API Conventions
- All controllers return `ActionResult<T>` not `IActionResult`
- Use `[ApiController]` attribute on all controllers
- Validate request DTOs with `[Required]` / `[Range]` attributes
```

### Choose a different model

Edit the `model:` field in `pr-reviewer.agent.md` YAML frontmatter. See [GitHub's model pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing).

---

## Requirements

- **GitHub Copilot Business** or **Enterprise** plan
- Copilot Code Review enabled in organisation policies
- (Optional) GitHub Actions for full project context analysis
- Repository language: **C# / .NET** with **Reqnroll + NUnit**

---

## Roadmap

- [ ] Sub-agents for specialized reviews (security-only, perf-only)
- [ ] Integration with Azure DevOps work items
- [ ] Support for xUnit and MSTest instruction files
- [ ] GitHub Actions workflow for automated PR reviewer on every PR

---

## Contributing

This is a template — fork it, adapt it to your stack, and share improvements via PR. If your team uses a different BDD framework (SpecFlow, Cucumber) or test framework (xUnit, MSTest), contributions are welcome.

---

## License

MIT — use it, fork it, adapt it to your team. No attribution required (but appreciated).

---

*Built with feedback from 10 official GitHub documentation sources and 2,500+ analyzed agent files.*
