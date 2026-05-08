---
version: "1.0.0"
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**", "!**/*Test*.cs", "!**/*Tests.cs"]
excludeAgent: "coding-agent"
---

# Performance Standards — Warnings

## 🟡 Warning

### Collections
- Prefer `IEnumerable<T>` for return types when callers don't need list/index access
- Use `ICollection<T>` or `IList<T>` only when mutation is required by callers
- Dictionary lookups: `TryGetValue()` instead of `ContainsKey()` + indexer

### LINQ
- `FirstOrDefault()` + null check over `Single()` when duplicates are possible
- `.Count() > 0` → `.Any()`
- Multiple `.Where()` calls can often be merged into one
- Avoid `.OrderBy().OrderBy()` — the second overwrites the first

### Logging
- Use `LoggerMessage` source generators for high-performance logging (C# 12+)
- Use structured logging: `_logger.LogInformation("Processing {OrderId}", id)`
- Never string interpolation in log messages
- Guard expensive log parameter evaluation with `_logger.IsEnabled(LogLevel.Debug)`

### Concurrency & Resource Disposal
- Types implementing both `IDisposable` and `IAsyncDisposable` must be disposed with `await using` when used in async code
- Flag `using` (sync) on types that implement `IAsyncDisposable` in async methods
- Use `ConcurrentDictionary<TKey,TValue>` instead of `Dictionary` + manual locking
- Flag sync-over-async on hot paths — this causes thread pool starvation under load
- Use `Task.WhenAll` for independent parallel async operations, not sequential awaits
- `Parallel.ForEach` with async bodies → flag; use `Task.WhenAll` or `Parallel.ForEachAsync` (.NET 6+)

### Resilience
- `HttpClient` calls in production code without retry/fallback policy → flag (use Polly or `Microsoft.Extensions.Resilience`)
- Retry logic without exponential backoff and jitter
- No timeout on `HttpClient` requests (default 100s is too high for most service-to-service calls)
- Missing circuit breaker pattern on critical external dependencies

### Rate Limiting
- ASP.NET Core endpoints exposed publicly without `[EnableRateLimiting]` or rate limiting middleware → flag
- Missing rate limiting on authentication endpoints (login, token refresh) — brute force vector
