---
applyTo: "**/*.cs"
excludeAgent: "coding-agent"
---

# Security Review Rules — C# / .NET

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

### Authentication & Authorization
- All controller actions must have `[Authorize]` attribute or be explicitly public with documented reason
- Authorization checks must happen server-side, never rely on client-side hiding
- JWT/Token validation must check expiration, issuer, and signature
- Never disable CSRF protection without explicit security review comment
- All POST/PUT/PATCH/DELETE controller actions must include `[ValidateAntiForgeryToken]` (traditional MVC) or validate antiforgery via `IAntiforgery` (API with cookie auth)
- APIs using bearer tokens (JWT) are inherently CSRF-safe; cookie-authenticated APIs require explicit antiforgery
- Never set `SameSite=None` on auth cookies without `Secure=true`

### Secrets & Credentials
- No hardcoded API keys, connection strings, tokens, or passwords
- Use User Secrets (dev), Azure Key Vault, or environment variables (prod)
- Check for `.gitignore` excluding `appsettings.Development.json` if it contains real secrets

### Input Validation
- All public API parameters must be validated (not null, within range, valid format)
- Use `[Required]`, `[Range]`, `[MaxLength]`, `[RegularExpression]` data annotations on DTOs
- Validate file uploads: type, size, content, path traversal
- Never trust client-side validation alone

### Sensitive Data
- Never log passwords, tokens, credit card numbers, or PII
- Never return sensitive data in API responses
- Use `[JsonIgnore]` on sensitive entity properties

### Deserialization
- Flag any use of `BinaryFormatter` (deprecated, RCE vector since .NET 5, removed in .NET 9)
- `JsonSerializer` with user input: never `TypeNameHandling.All` or `TypeNameHandling.Auto`
- `XmlSerializer` with untrusted XML: flag if types are not from a known allowlist
- `XmlReaderSettings.DtdProcessing` must be `DtdProcessing.Prohibit` when parsing untrusted XML

### Server-Side Request Forgery (SSRF)
- `HttpClient.GetAsync(url)` or similar where `url` comes from user input → require allowlist or DNS validation before request
- Flag any user-controlled URL passed directly to `HttpClient`, `WebClient`, or `HttpWebRequest`

### Path Traversal
- `Path.Combine(baseDir, userInput)` without normalization: flag unless followed by `Path.GetFullPath()` + `.StartsWith(baseDir)` check
- User-controlled file names used in `File.ReadAllText()`, `File.Open()`, etc. without path sanitization

### Regex Denial of Service (ReDoS)
- Flag user-controlled input compiled into `new Regex(pattern)` without `RegexOptions.NonBacktracking` (.NET 7+) or explicit timeout
- Patterns with nested quantifiers (`(a+)+`, `(.*)*`, etc.) on untrusted input

### Open Redirect
- `Redirect(url)` or `LocalRedirect()` from query string or user input → must validate with `Url.IsLocalUrl()` before redirecting
- Flag any `return Redirect(userProvidedUrl)` in controller actions

### Mass Assignment
- `[HttpPost] Action(EntityModel)` → require dedicated DTO, never bind directly to EF entities
- Flag `[Bind]` attribute whitelisting properties on entity models (use DTOs instead)

## 🟡 MUST FIX — Warning

### Cryptography
- Use `System.Security.Cryptography` APIs, never custom encryption
- For general hashing: SHA-256 or stronger (not MD5, not SHA-1)
- **For passwords**: SHA-256 is NOT sufficient. Use ASP.NET Core Identity's `PasswordHasher<TUser>` (PBKDF2), `bcrypt`, or `Argon2id`
- Never store passwords with reversible encryption

### Secure Headers
- HTTPS enforced everywhere — flag any HTTP endpoints
- CORS policies must be specific (no `AllowAnyOrigin` with `AllowCredentials`)
- Flag `AllowAnyHeader` + `AllowAnyMethod` + `AllowCredentials` — triple combination is a security hole

### Cookie Security
- Auth cookies must set `HttpOnly = true` (prevents `document.cookie` access from XSS)
- Auth cookies must set `Secure = true` (HTTPS-only transport)
- Auth cookies must set `SameSite = Strict` or `SameSite = Lax` (CSRF defense). Never `SameSite = None` on auth cookies without documenting why cross-site auth is required
- Flag `Cookie.Secure = false` in production configuration
- Flag `Cookie.HttpOnly = false` on session or auth cookies
- Anti-forgery tokens should be scoped per user session, not shared across users

### Dependency Security
- Flag packages with known CVEs (check if updated in PR)
- Flag deprecated or unsupported package versions

### OAuth / Token Logging
- Flag logging of access tokens, refresh tokens, or authorization codes — even in debug logs
- Flag tokens in query string URLs (OAuth `redirect_uri` with `code` or `token` params) being logged
- Return URLs with tokens should use POST (form_post) or fragment, not query string
