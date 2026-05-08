# Repository Standards — C# / Reqnroll / NUnit

> These are universal standards that apply to ALL Copilot interactions in this repo (Chat, Code Review, Coding Agent).
> For domain-specific review rules, see `.github/instructions/`.

## Code Style
- Follow Microsoft C# Coding Conventions
- PascalCase classes/methods/properties; camelCase params/locals; _camelCase private fields
- `I` prefix interfaces; `Async` suffix async methods
- File-scoped namespaces; expression-bodied members for single-line code

## Architecture
- Business logic lives in services, not controllers or step definitions
- Constructor injection only; interfaces for cross-layer services
- DTOs/ViewModels at layer boundaries — never expose entities
- Feature folders or clean architecture; no flat structures

## What Never Passes Review
- Hardcoded secrets, keys, connection strings
- SQL concatenation without parameterization
- `async void` (except event handlers); `.Result`/`.Wait()` on async
- `new HttpClient()` — use `IHttpClientFactory`
- Empty `catch (Exception)` without rethrow or logging
- Missing Reqnroll step defs for new Gherkin scenarios
- Public methods without XML docs
- Tests asserting nothing meaningful (`Assert.True(true)`, `Is.NotNull` only)

## Instruction Files

Domain-specific rule files in `.github/instructions/` apply during code review. Each file uses `excludeAgent: "coding-agent"` because these are review rules, not code-generation rules. Remove the field if you want the Coding Agent to also follow them.

| Domain | File |
|--------|------|
| Security — Injection | `.github/instructions/security-injection.instructions.md` |
| Security — Auth | `.github/instructions/security-auth.instructions.md` |
| Security — Warnings | `.github/instructions/security-warnings.instructions.md` |
| Architecture — Core | `.github/instructions/architecture-core.instructions.md` |
| Architecture — Patterns | `.github/instructions/architecture-patterns.instructions.md` |
| Performance — Critical | `.github/instructions/performance-critical.instructions.md` |
| Performance — Warnings | `.github/instructions/performance-warnings.instructions.md` |
| Gherkin | `.github/instructions/gherkin.instructions.md` |
| Reqnroll | `.github/instructions/reqnroll.instructions.md` |
| NUnit | `.github/instructions/nunit.instructions.md` |
| xUnit | `.github/instructions/xunit.instructions.md` |
| MSTest | `.github/instructions/mstest.instructions.md` |
| Logging | `.github/instructions/logging.instructions.md` |
| DI | `.github/instructions/di.instructions.md` |
| EF Core | `.github/instructions/efcore.instructions.md` |
| Output format | `.github/instructions/review-output.instructions.md` |
| Playwright — Base | `.github/instructions/playwright-base.instructions.md` |
| Playwright — Actions | `.github/instructions/playwright-actions.instructions.md` |
| Playwright — Anti-patterns | `.github/instructions/playwright-anti-patterns.instructions.md` |
| Appium — Lifecycle | `.github/instructions/appium-lifecycle.instructions.md` |
| Appium — Locators | `.github/instructions/appium-locators.instructions.md` |
| Appium — Gestures | `.github/instructions/appium-gestures.instructions.md` |
| API Design | `.github/instructions/api-design.instructions.md` |
| GitHub Actions | `.github/instructions/github-actions.instructions.md` |
| Supply Chain | `.github/instructions/supply-chain.instructions.md` |
