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

Domain-specific rule files in `.github/instructions/` apply during code review. Each file uses `excludeAgent: ["coding-agent"]` because these are review rules (flagging anti-patterns, enforcing conventions), not code-generation rules. Remove the `excludeAgent` field if you want the Coding Agent to also follow these rules when generating code.

For detailed, domain-specific rules used during code review, see:

| Domain | File |
|--------|------|
| Security (OWASP, auth, secrets, input validation) | `.github/instructions/security.instructions.md` |
| Architecture & SOLID | `.github/instructions/architecture.instructions.md` |
| Performance, async, EF Core | `.github/instructions/performance.instructions.md` |
| Gherkin feature files | `.github/instructions/gherkin.instructions.md` |
| Reqnroll step definitions & hooks | `.github/instructions/reqnroll.instructions.md` |
| NUnit test standards | `.github/instructions/nunit.instructions.md` |
| Logging | `.github/instructions/logging.instructions.md` |
| Dependency Injection | `.github/instructions/di.instructions.md` |
| Entity Framework Core | `.github/instructions/efcore.instructions.md` |
| Review output format | `.github/instructions/review-output.instructions.md` |
| Playwright E2E tests | `.github/instructions/playwright.instructions.md` |
| Appium mobile tests | `.github/instructions/appium.instructions.md` |
