---
applyTo: ["**/*.cs", "**/*.cshtml", "**/*.razor", "**/*.js", "**/*.ts", "**/*.tsx", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Security Review Rules — Injection & Input Validation

## 🔴 BLOCK MERGE — Critical

### SQL Injection
- Never concatenate user input into SQL strings
- Always use parameterized queries with EF Core, Dapper, or SqlCommand.Parameters
- Flag any raw SQL string with `+` or string interpolation

### Cross-Site Scripting (XSS)
- Flag `@Html.Raw(userInput)` in Razor views without prior sanitization (HtmlSanitizer)
- Flag `[AllowHtml]` on model properties without a dedicated sanitizer pipeline
- Never set `innerHTML` or `outerHTML` from user input in client-side code — use `textContent` or DOM APIs
- Flag `Microsoft.AspNetCore.Html.HtmlString` constructed from user-controlled data
- Flag `HttpUtility.HtmlDecode()` followed by raw output without re-encoding
- Use `IHtmlEncoder` (`System.Text.Encodings.Web.HtmlEncoder.Default`) for manual HTML encoding
- Content-Security-Policy header with `script-src 'self'` as defense-in-depth layer

### Input Validation
- All public API parameters must be validated (not null, within range, valid format)
- Use `[Required]`, `[Range]`, `[MaxLength]`, `[RegularExpression]` data annotations on DTOs
- Validate file uploads: type, size, content, path traversal
- Never trust client-side validation alone

### Path Traversal
- `Path.Combine(baseDir, userInput)` without normalization: flag unless followed by `Path.GetFullPath()` + `.StartsWith(baseDir)` check
- User-controlled file names used in `File.ReadAllText()`, `File.Open()`, etc. without path sanitization

### Regex Denial of Service (ReDoS)
- Flag user-controlled input compiled into `new Regex(pattern)` without `RegexOptions.NonBacktracking` (.NET 7+) or explicit timeout
- Patterns with nested quantifiers (`(a+)+`, `(.*)*`, etc.) on untrusted input

### Open Redirect
- `Redirect(url)` from query string or user input → must validate with `Url.IsLocalUrl()` before redirecting (Critical)
- `LocalRedirect(url)` from user input → Warning if not pre-validated; note that `LocalRedirect` already throws for non-local URLs, but explicit validation improves error handling
- Flag any `return Redirect(userProvidedUrl)` in controller actions

### Mass Assignment
- `[HttpPost] Action(EntityModel)` → require dedicated DTO, never bind directly to EF entities
- Flag `[Bind]` attribute whitelisting properties on entity models (use DTOs instead)

## Exceptions — Do Not Flag When

- **CSP**: `script-src` uses `nonce-`, `hash-`, or `strict-dynamic` instead of `'self'` alone — this is stronger, not weaker.
- **Authorization**: A global fallback policy (e.g., `options.FallbackPolicy = ...`) is registered in `Program.cs` and the endpoint does not explicitly opt out with `[AllowAnonymous]`.
- **Rate limiting**: Middleware or attribute-based global rate limiting is configured; do not require per-endpoint duplication.
- **Open redirect**: `Url.IsLocalUrl()` or equivalent validation is already present, or the URL is sourced from a trusted allowlist, not raw user input.
