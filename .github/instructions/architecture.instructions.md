---
applyTo: "**/*.cs"
excludeAgent: "coding-agent"
---

# Architecture & Code Quality Standards

## SOLID
- **S**: Each class/step definition has ONE responsibility. If you need "and" to describe what it does, split it
- **O**: Use strategy/factory patterns instead of `if type == "A" else if type == "B"` chains
- **L**: Derived classes must be substitutable for base. Flag `NotImplementedException` in overrides
- **I**: Interfaces with >5 methods — consider splitting. Fat interfaces breed coupling
- **D**: Depend on abstractions, not concretions. `new MyService()` inside a method is a violation

## DRY
- Same or nearly-same logic in 2+ places → extract
- Same Gherkin step text in 3+ feature files with duplicate step definitions → consolidate
- Same validation logic in controller + service + step definition → single validator

## Separation of Concerns
- Controllers: HTTP concerns only (routing, status codes, model binding)
- Services: business logic
- Repositories: data access
- Step definitions: BDD orchestration only — delegate to services
- No business logic in constructors

## Naming & Structure
- Projects follow naming: `Company.Project.Layer` (e.g., `Contoso.Orders.Api`, `Contoso.Orders.Domain`)
- Feature folders or clean architecture: `Features/Orders/`, `Features/Users/` or `Domain/`, `Application/`, `Infrastructure/`
- No "Common", "Utils", "Helpers" dumping grounds — each utility must have a specific home

## Dependency Injection
- Constructor injection always — never `IServiceProvider.GetService<T>()` outside composition root
- Register services by interface: `services.AddScoped<IOrderService, OrderService>()`
- Options pattern: `services.Configure<MyOptions>(configuration.GetSection("MyOptions"))`

## Flag Immediately
- Business logic in controllers or step definitions
- `static` classes holding mutable state
- Service locator pattern (`IServiceProvider` injected into services)
- Classes with >500 lines
- Methods with >50 lines
- Cyclomatic complexity — deeply nested if/switch should be refactored with patterns
