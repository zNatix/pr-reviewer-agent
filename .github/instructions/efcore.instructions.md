---
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**"]
excludeAgent: "coding-agent"
---

# Entity Framework Core Standards — C# / .NET

## Querying
- Use `AsNoTracking()` for read-only queries — avoids change tracker overhead
- `Where()` before `ToList()` — never materialize then filter in memory
- Use `Select()` to fetch only needed columns — avoid `SELECT *`
- Use `Any()` for existence checks; never `Count() > 0` or `ToList().Any()`
- Use `AsSplitQuery()` when eager-loading multiple collections to avoid cartesian explosion
- Use `IQueryable` at the repository boundary; materialize (`ToListAsync`, `FirstOrDefaultAsync`) at the service/controller level

## Tracking & Change Detection
- Know when tracking is needed: updates/deletes use tracking; reads use `AsNoTracking()`
- `AutoDetectChangesEnabled = false` for bulk operations (EF Core 6+)
- Attach vs Update: prefer `context.Attach(entity).State = EntityState.Modified` for precise control

## Batching & Bulk
- Use `ExecuteUpdateAsync` / `ExecuteDeleteAsync` (EF Core 7+) for bulk operations — never load entities then save one-by-one
- Batch size: configure `MaxBatchSize` for insert/update operations
- For very large bulk operations, consider `SqlBulkCopy` or raw SQL instead of EF Core

## Transactions
- Use `IDbContextTransaction` when multiple `SaveChangesAsync` calls form a single logical operation
- Always wrap multi-step saves in `await using var transaction = await context.Database.BeginTransactionAsync()`
- Flag multiple `SaveChangesAsync()` calls without an explicit transaction when they update related entities
- Use `context.Database.CreateExecutionStrategy()` for retry logic with transient failures

## Concurrency
- Use `[Timestamp]` or `IsRowVersion()` for optimistic concurrency on entities that can be modified concurrently
- Flag entities without concurrency tokens when the application has concurrent write scenarios
- Always catch `DbUpdateConcurrencyException` and handle appropriately (reload + retry, or notify user)
- Never silently discard concurrency exceptions

## Migrations
- Migrations must be reversible (`Down` method) or documented why not
- Never `Database.EnsureCreated()` in production — use migrations
- Idempotent SQL in migration scripts: check existence before `CREATE/ALTER/DROP`
- `__EFMigrationsHistory` table must be managed by EF Core only — never manually edit

## Compiled Queries
- For hot-path queries executed 1000s of times, use `EF.CompileQuery` or `EF.CompileAsyncQuery`
- Flag repeated `.Where().Select().FirstOrDefaultAsync()` patterns that could be compiled

## Anti-patterns to Flag
- `ToList()` before `Where()` — materializes entire table
- Loading entire entity for single property access: `var name = (await ctx.Users.FirstAsync(u => u.Id == id)).Name` → use `Select(u => u.Name)`
- N+1 queries: lazy loading or explicit `Load()` in loops
- `SaveChanges()` in a loop — batch changes and save once
- `DbContext` used across multiple threads (not thread-safe)
- `new DbContext()` instead of DI / factory
- Raw SQL concatenation: `FromSqlRaw($"SELECT * FROM Users WHERE Name = '{name}'")` → `FromSql($"SELECT * FROM Users WHERE Name = {name}")` or parameterized
