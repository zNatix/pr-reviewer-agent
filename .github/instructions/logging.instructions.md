---
version: "1.0.0"
# Test files excluded — logging in tests follows test-framework conventions.
# Migrations excluded — auto-generated code.
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**", "!**/*Test*.cs", "!**/*Tests.cs"]
excludeAgent: ["coding-agent"]
---

# Logging Standards — C# / .NET

## Structured Logging
- Use `ILogger<T>` with structured logging: `_logger.LogError("Failed to process order {OrderId}", id)` — never string interpolation
- Log levels: `Trace`/`Debug` for dev diagnostics, `Information` for key events, `Warning` for recoverable issues, `Error` for failures, `Critical` for system-down scenarios
- Guard expensive log message evaluation: `if (_logger.IsEnabled(LogLevel.Debug)) { _logger.LogDebug(...) }`

## What Never to Log
- Passwords, tokens, API keys, credit card numbers, or any PII
- Full HTTP request/response bodies containing sensitive data
- Connection strings or internal IPs
- Stack traces to end users (log internally, return sanitized error to client)

## High-Performance Logging (.NET 6+)
- Use `LoggerMessage` source generators for hot-path logging:
  ```csharp
  private static readonly Action<ILogger, int, Exception?> OrderProcessed =
      LoggerMessage.Define<int>(LogLevel.Information, new EventId(1, nameof(OrderProcessed)), "Order {OrderId} processed");
  ```
- Flag `string.Format` or `$` interpolation inside log calls in hot paths (>1000 calls/sec)

## Correlation & Tracing
- Include correlation IDs (e.g., `Request-Id` header) in logs for distributed tracing
- Flag missing `Activity` / `OpenTelemetry` span creation in cross-service calls
- Use `HttpContext.TraceIdentifier` for request-level correlation in ASP.NET Core

## Exception Logging
- Always pass the exception object: `_logger.LogError(ex, "message")` — never just `ex.Message`
- Never `catch (Exception) { _logger.LogError("error"); }` without the exception parameter
- Use `ILogger.BeginScope()` for contextual enrichment (e.g., `{UserId}`, `{TenantId}`)

## Anti-patterns to Flag
- `Console.WriteLine()` in library or production code
- `Debug.WriteLine()` left in production paths
- Logging inside tight loops without guard clause
- Logging sensitive data (PII, secrets, tokens)
- `_logger.LogInformation($"User {name} logged in")` — always use structured params
