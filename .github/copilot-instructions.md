# Repository Standards — C# / Reqnroll / NUnit

## Code Style
- Follow Microsoft's C# Coding Conventions: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
- PascalCase for classes, methods, properties, public members
- camelCase for parameters and local variables
- _camelCase for private instance fields (prefix with underscore)
- I prefix for interfaces (IUserService, IRepository)
- Async methods end with Async suffix (GetUserAsync)
- Use file-scoped namespaces
- Use primary constructors where appropriate (C# 12+)
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
