---
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Security Review Rules — Auth, Secrets & Deserialization

## 🔴 BLOCK MERGE — Critical

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
