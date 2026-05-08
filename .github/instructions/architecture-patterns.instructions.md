---
version: "1.0.0"
applyTo: ["**/*.cs", "!**/Program.cs", "!**/Startup.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**", "!**/*Test*.cs", "!**/*Tests.cs"]
excludeAgent: "coding-agent"
---

# Architecture Patterns — Nullable, Records, IAsyncEnumerable

## Nullable Reference Types (.NET 6+)
- Projects must enable `<Nullable>enable</Nullable>` in `.csproj`
- `!` (null-forgiving operator) requires inline comment justifying why null is impossible at that point
- Public API methods: never return `null` for collections — return `Enumerable.Empty<T>()` or `Array.Empty<T>()`
- Flag `T?` on DTO properties without explicit `[Required]` attribute or documented default value
- Flag `string?` returns from public methods without null check guidance in XML docs
- Constructor-injected dependencies should be non-nullable (DI guarantees resolution)

## Modern C# Patterns (.NET 6+)

### Record Types
- Use `record` for immutable DTOs and value objects — built-in value equality, `with` expressions, and `ToString()`
- Use `record struct` for high-performance value types (no heap allocation, value semantics)
- Flag `class` DTOs with manual `Equals`/`GetHashCode` overrides where `record` would suffice
- Note: `record` types have a synthesized constructor for `init`-only properties; DI does NOT call it — use `required` properties or positional parameters for DI-injected records

### IAsyncEnumerable<T>
- Return `IAsyncEnumerable<T>` for streaming APIs that yield results as they become available
- Flag `Task<List<T>>` return types on methods that stream data (EF Core queries, paginated APIs) — consider `IAsyncEnumerable<T>` to reduce memory pressure
- Always dispose `IAsyncEnumerable<T>` with `await foreach` or `ConfigureAwait(false).GetAsyncEnumerator()` with `finally` block
- Flag `await foreach` without `CancellationToken` — pass `cancellationToken` via `.WithCancellation(cancellationToken)`
