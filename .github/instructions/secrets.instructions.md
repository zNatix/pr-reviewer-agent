---
applyTo:
  - "**/appsettings*.json"
  - "**/.env"
  - "**/.env.*"
  - "**/*.yaml"
  - "**/*.yml"
  - "**/*.config"
  - "**/*.json"
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Secrets & Configuration Review Rules

## 🔴 Critical — Block Merge
- Hardcoded secrets, API keys, connection strings, or tokens in any config file
- Passwords or private keys committed in YAML, JSON, or `.env` files
- `dotnet user-secrets` IDs committed without corresponding `UserSecretsId` in project file (check consistency)

## 🟡 Warning
- Missing encryption at rest for sensitive configuration sections
- Default credentials in connection strings (`User Id=sa;Password=...`)
- Committing `.env` files that are not explicitly marked as templates (`.env.example` is OK)
- Exposed `ASPNETCORE_ENVIRONMENT=Production` with debug settings enabled

## 🔵 Suggestion
- Use placeholder values like `<YOUR_KEY>`, `<REPLACE_ME>`, or `__SECRET__` in committed templates
- Document required secrets in README or setup docs rather than inline comments
- Prefer Azure Key Vault / AWS Secrets Manager references over inline secrets in container environments
