# Repository Standards — C# / Reqnroll / NUnit

> These are universal standards that apply to ALL Copilot interactions in this repo (Chat, Code Review, Coding Agent).
> For domain-specific review rules, see `.github/instructions/`.

## Code Style
- Follow Microsoft's C# Coding Conventions: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
- PascalCase for classes, methods, properties, public members
- camelCase for parameters and local variables
- _camelCase for private instance fields (prefix with underscore)
- I prefix for interfaces (IUserService, IRepository)
- Async methods end with Async suffix (GetUserAsync)
- Use file-scoped namespaces
- Prefer expression-bodied members for single-line methods and properties

## Architecture
- All business logic in services, not controllers or step definitions
- Step definitions delegate to helper classes — not raw implementation
- DI with constructor injection always (no service locator anti-pattern)
- Interfaces for all services used across layers
- DTOs/ViewModels for crossing layer boundaries — never expose entities to API surface
- Feature folders or clean architecture layers — not flat project structures

## What Never Passes Review
- Hardcoded secrets, keys, or connection strings
- SQL string concatenation or dynamic SQL without parameterization
- async void (except event handlers)
- .Result, .Wait(), .GetAwaiter().GetResult() on async methods
- new HttpClient() (use IHttpClientFactory)
- Catching Exception without rethrow or logging
- Missing Reqnroll step definitions for new Gherkin scenarios
- Public methods without XML doc comments
- Tests that assert nothing meaningful (assert true, assert not null only)

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
