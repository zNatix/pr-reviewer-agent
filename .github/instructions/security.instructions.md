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

### Authentication & Authorization
- All controller actions must have `[Authorize]` attribute or be explicitly public with documented reason
- Authorization checks must happen server-side, never rely on client-side hiding
- JWT/Token validation must check expiration, issuer, and signature
- Never disable CSRF protection without explicit security review comment

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

## 🟡 MUST FIX — Warning

### Cryptography
- Use `System.Security.Cryptography` APIs, never custom encryption
- Use SHA-256 or stronger for hashing (not MD5, not SHA-1)
- Passwords: use ASP.NET Core Identity's built-in hashing (PBKDF2)

### Secure Headers
- HTTPS enforced everywhere — flag any HTTP endpoints
- CORS policies must be specific (no `AllowAnyOrigin` with `AllowCredentials`)

### Dependency Security
- Flag packages with known CVEs (check if updated in PR)
- Flag deprecated or unsupported package versions
