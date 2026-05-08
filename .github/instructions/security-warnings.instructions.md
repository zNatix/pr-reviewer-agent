---
applyTo: ["**/*.cs", "!**/*.g.cs", "!**/*.Designer.cs", "!**/Migrations/**"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Security Review Rules — Warnings

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
