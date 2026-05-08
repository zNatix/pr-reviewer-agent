---
version: "1.0.0"
# Test files excluded — NUnit/Playwright/Appium instruction files cover test performance concerns.
# Migrations excluded — auto-generated code.
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**", "!**/*Test*.cs", "!**/*Tests.cs"]
excludeAgent: "coding-agent"
---

# Performance Standards

## 🔴 Critical — Block Merge

### Entity Framework Core
- `Where()` before `ToList()` — never materialize then filter in memory
- Unbounded queries without `Take()` / pagination in production endpoints
- N+1 query loops (loading related data inside a loop without `Include` or projection)

### Async/Await
- Never `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` on Tasks in production code
- `async void` outside event handlers
- Sync-over-async in ASP.NET Core request pipeline (e.g., `Task.Run(...).Result`)
- Avoid `Task.Run()` on ASP.NET Core — it steals threads from the pool

### Memory & Allocations
- `string` concatenation in hot paths/loops — use `StringBuilder`
- Boxing value types to `object` in hot paths

### HTTP
- `new HttpClient()` in production services — use `IHttpClientFactory`
- Note: `new HttpClient()` is acceptable in short-lived console apps, tests, or one-off scripts

## 🟡 Warning

### Entity Framework Core
- Use `AsNoTracking()` for read-only queries
- Use `Any()` for existence checks (`Any()` > `Count() > 0` > `ToList().Any()`)
- Use `Select()` to fetch only needed columns — avoid `SELECT *`

### Memory & Allocations
- `ToList()` when `IEnumerable` is sufficient
- Use `ArrayPool<T>` for large temporary arrays in hot paths
- Use `Span<T>` / `Memory<T>` for performance-critical string/buffer operations
- .NET 8+: Use `SearchValues<T>` for efficient character/byte search patterns
- .NET 8+: Use `FrozenDictionary<TKey,TValue>` and `FrozenSet<T>` for read-only collections queried frequently
- .NET 9+: Use `OrderedDictionary<TKey,TValue>` when insertion order matters

## 🔵 Suggestion
- `ConfigureAwait(false)` in library code (NuGet packages). Not needed in ASP.NET Core controllers or apps where `SynchronizationContext` is null (.NET Core+)
- Use typed clients or named clients instead of string-based factory in hot paths
