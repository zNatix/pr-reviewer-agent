---
version: "1.0.0"
# Test files excluded — NUnit/Playwright/Appium instruction files cover test performance concerns.
# Migrations excluded — auto-generated code.
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**", "!**/*Test*.cs", "!**/*Tests.cs"]
excludeAgent: "coding-agent"
---

# Performance Standards — Critical (Block Merge)

## 🔴 Critical — Block Merge

### Entity Framework Core
- `Where()` before `ToList()` — never materialize then filter
- Use `AsNoTracking()` for read-only queries
- Use `Any()` for existence checks (`Any()` > `Count() > 0` > `ToList().Any()`)
- Use `Select()` to fetch only needed columns — avoid `SELECT *`

### Async/Await
- Never `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` on Tasks
- `async void` only in event handlers — everywhere else `async Task`
- `ConfigureAwait(false)` in library code (nuget packages). Not needed in ASP.NET Core controllers or applications where `SynchronizationContext` is null (.NET Core+)
- Avoid `Task.Run()` on ASP.NET Core — it steals threads from the pool

### Memory & Allocations
- Avoid `string` concatenation in loops — use `StringBuilder`
- Avoid `ToList()` when `IEnumerable` is sufficient
- Use `ArrayPool<T>` for large temporary arrays in hot paths
- Use `Span<T>` / `Memory<T>` for performance-critical string/buffer operations
- Boxing: avoid casting value types to `object` in hot paths
- .NET 8+: Use `SearchValues<T>` for efficient character/byte search patterns — `SearchValues.Create("AEIOU")` is faster than `Contains` + `IndexOf` chains
- .NET 8+: Use `FrozenDictionary<TKey,TValue>` and `FrozenSet<T>` for read-only collections created once and queried frequently — faster lookups than `Dictionary<TKey,TValue>` after initial freeze cost
- .NET 9+: Use `OrderedDictionary<TKey,TValue>` when insertion order matters (replaces `Dictionary` + `List` workaround)

### HTTP
- `IHttpClientFactory` for all HttpClient instances in services — never `new HttpClient()`
- Note: `new HttpClient()` is acceptable in short-lived console apps, tests, or one-off scripts
- Use typed clients or named clients, not string-based factory in hot paths
