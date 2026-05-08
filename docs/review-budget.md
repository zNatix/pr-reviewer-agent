# Review Budget Policy

> Cost-aware review strategy for large pull requests and Copilot Code Review consumption.
> Effective: 2026-05-08

## Context

Starting June 1, 2026, GitHub Copilot Code Review consumes GitHub Actions minutes. This document defines how the reviewer agent should prioritize work to stay effective without excessive cost.

## Thresholds

| PR Size | Policy |
|---|---|
| **≤ 25 changed files** | Full review across all domains. Default mode. |
| **26–100 changed files** | Priority review: security-sensitive files first, then business logic, then tests. List skipped files explicitly. |
| **> 100 changed files** | Security-only pass + architectural concerns on modified entry points. Recommend PR split in review summary. |

## Prioritization Order

1. Security-sensitive files (auth, crypto, input parsing)
2. `.cs` business logic and controllers/endpoints
3. `.feature` Gherkin files (if behavior changed)
4. `.csproj`/`.sln`/`.props` (dependency changes)
5. Config files (`appsettings*.json`, `nuget.config`)
6. Documentation and markdown

## Skip Patterns (Always)

- `*.Designer.cs`, `*.g.cs`, `*.generated.cs`
- `**/Migrations/*.cs` (unless PR description claims manual migration changes)
- `**/obj/**`, `**/bin/**`
- Lockfile-only changes without dependency version changes (e.g., formatting)

## Dependabot / Renovate PRs

- Skip BDD traceability and test quality checks
- Focus exclusively on CVE severity, compatibility risk, and license changes
- Cap findings at 10 items

## Cost Notes

- Copilot Code Review minutes count against your Actions quota
- Large PRs cost more and yield lower signal-to-noise ratio
- Recommendation: split PRs larger than 50 files when deep review is required
- The `@pr-reviewer` custom agent (Chat mode) does not consume Actions minutes directly, but token usage still applies to your Copilot quota

## Agent Behavior

When reviewing, the agent must:
- State the number of files reviewed vs. total changed files
- List skipped files by name (or pattern if >20)
- Build a Diff Map so that every changed hunk is accounted for as `reviewed` or `skipped` with reason
- For files beyond the 25-file cap, still list them in the Diff Map under `Files skipped`
- If findings exceed 30 items, summarize by severity and detail only the top 10
- For PRs >100 files, add a note: "Consider splitting this PR for a more thorough review."
