---
version: "1.0.0"
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**"]
excludeAgent: "coding-agent"
---

# API Design Standards — ASP.NET Core

## 🔴 Critical — Block Merge

### Contracts & Serialization
- Never return EF Core entities directly from controllers/minimal API endpoints — always project to DTOs/records
- Public DTOs must be versioned; changing property names/types without versioning breaks clients
- `JsonSerializerOptions` must not use `PropertyNamingPolicy = null` on public APIs unless backward-compatible contract is explicitly documented

### Input Validation
- All public endpoints must validate input via `[ApiController]` + model binding or `FluentValidation` — silent failures are not acceptable
- File upload endpoints: validate extension, MIME type, and size before processing

### Authorization
- Every controller action or minimal API endpoint must have `[Authorize]` or `[AllowAnonymous]` with a documented rationale
- Never rely solely on global authorization filters without endpoint-level verification

## 🟡 Warning — Should Fix

### HTTP Semantics
- Return correct status codes: `201 Created` for POST that creates, `204 NoContent` for successful DELETE, `409 Conflict` for concurrency collisions
- Use `ProblemDetails` (or `ValidationProblemDetails`) for 4xx errors — never return raw exception messages or stack traces
- `GET` and `HEAD` must be safe and idempotent; `PUT` must be fully idempotent; `PATCH` must document semantics

### Pagination & Limits
- List endpoints must support pagination (`page`/`pageSize` or `cursor`) with a maximum page size cap (e.g., 100)
- Default page size must be documented and enforced

### Idempotency
- Mutating operations exposed to external callers must support idempotency keys (`Idempotency-Key` header or similar) when duplicate submission is possible

## 🔵 Suggestion — Approve with Nits

- Use `ProducesResponseType` attributes for Swagger/OpenAPI documentation
- Versioning strategy: URL path (`/v1/`) or header — pick one and apply consistently
- Prefer `IAsyncEnumerable<T>` for streaming large collections instead of buffering into `List<T>`
- Use `CancellationToken` on all async service/repository methods and pass it through to EF Core and HTTP calls
