---
version: "1.0.0"
applyTo: ["**/*.csproj", "**/nuget.config", "**/packages.lock.json", "**/Directory.Packages.props", "**/Dockerfile*", "**/docker-compose*"]
excludeAgent: "coding-agent"
---

# Supply Chain Security Rules

## 🔴 Critical — Block Merge

### Dependencies
- No unversioned or wildcard (`*`) package references in `.csproj` or `Directory.Packages.props` — exact versions or centrally managed versions only
- No references to non-official NuGet feeds without justification and audit trail in `nuget.config`
- `packages.lock.json` must be present and up to date if lockfile mode is enabled; flag if it is stale or missing when expected

### Docker
- Base images must use specific digests or immutable tags — never `latest`
- Do not run containers as root (`USER` directive must be non-root when possible)
- No secrets baked into images (`ARG`/`ENV` for credentials is a blocker)

## 🟡 Warning — Should Fix

### Package Integrity
- Verify package signing where possible; flag unlisted or deprecated packages on NuGet.org
- Be alert for typosquatting: `Newtonsoft.Jason` instead of `Newtonsoft.Json`, `Microsft.Extensions` instead of `Microsoft.Extensions`

### Build Reproducibility
- `Deterministic` build property should be `true` in `.csproj`
- Source linking should be enabled for published packages (`EmbedUntrackedSources`, `PublishRepositoryUrl`)

## 🔵 Suggestion — Approve with Nits

- Pin `global.json` to a specific SDK version band
- Use `CentralPackageManagement` in monorepos to reduce version drift
- Enable `NuGetAudit` (`<NuGetAuditMode>all</NuGetAuditMode>`) to surface transitive vulnerabilities at build time
