---
applyTo: "**/*.cs"
excludeAgent: "coding-agent"
---

# Performance Standards — C# / .NET

## 🔴 Critical — Block Merge

### Entity Framework Core
- `Where()` before `ToList()` — never materialize then filter
- Use `AsNoTracking()` for read-only queries
- Use `Any()` for existence checks (`Any()` > `Count() > 0` > `ToList().Any()`)
- Use `Select()` to fetch only needed columns — avoid `SELECT *`

### Async/Await
- Never `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` on Tasks
- `async void` only in event handlers — everywhere else `async Task`
- Use `ConfigureAwait(false)` in library code
- Avoid `Task.Run()` on ASP.NET Core — it steals threads from the pool

### Memory & Allocations
- Avoid `string` concatenation in loops — use `StringBuilder`
- Avoid `ToList()` when `IEnumerable` is sufficient
- Use `ArrayPool<T>` for large temporary arrays in hot paths
- Use `Span<T>` / `Memory<T>` for performance-critical string/buffer operations
- Boxing: avoid casting value types to `object` in hot paths

### HTTP
- `IHttpClientFactory` for all HttpClient instances — never `new HttpClient()`
- Use typed clients or named clients, not string-based factory in hot paths

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
