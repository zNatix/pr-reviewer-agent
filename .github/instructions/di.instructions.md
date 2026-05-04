---
version: "1.0.0"
# Test files excluded — DI in tests follows test-framework conventions (NUnit/Playwright/Appium instruction files).
# Migrations excluded — auto-generated code.
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**", "!**/*Test*.cs", "!**/*Tests.cs"]
excludeAgent: ["coding-agent"]
---

# Dependency Injection Standards — C# / .NET

## Constructor Injection
- Constructor injection always — never `IServiceProvider.GetService<T>()` outside composition root
- Flag `IServiceProvider` injected into services (service locator anti-pattern)
- All constructor-injected dependencies should be `readonly` fields

## Lifetime Management
- Use the correct lifetime for each registration:
  - `AddSingleton`: stateless services, configuration wrappers, caches (thread-safe)
  - `AddScoped`: per-request services (ASP.NET), per-scenario (Reqnroll)
  - `AddTransient`: lightweight, stateless services; new instance every injection
- **Captive dependencies**: never inject a Scoped service into a Singleton
- **Scoped from Singleton**: flag `IServiceScopeFactory` misuse (should be rare, documented)
- For background services (`BackgroundService`, `IHostedService`): always create scope via `IServiceScopeFactory`

## Registration
- Register services by interface: `services.AddScoped<IOrderService, OrderService>()`
- Use `TryAdd*` variants for services that may already be registered
- Validate on build in development: `hostBuilder.UseDefaultServiceProvider(o => o.ValidateScopes = true)` or `ValidateOnBuild = true`
- Options pattern: `services.Configure<MyOptions>(configuration.GetSection("MyOptions"))` — never `new MyOptions()` then manually populate

## Keyed Services (.NET 8+)
- Use `[FromKeyedServices("key")]` when multiple implementations of same interface exist
- Flag `GetRequiredKeyedService<T>(key)` outside composition root (service locator)

## Anti-patterns to Flag
- `IServiceProvider.GetService<T>()` or `GetRequiredService<T>()` inside services/controllers
- `new MyService()` inside a class that receives DI (bypasses the container)
- Static `HttpClient` or `new HttpClient()` instead of `IHttpClientFactory`
- Transient service depending on Scoped/Transient DbContext (EF Core contexts are Scoped)
- Singleton service holding mutable state without `ConcurrentDictionary` or locking
