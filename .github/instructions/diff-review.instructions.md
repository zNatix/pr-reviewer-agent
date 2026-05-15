---
applyTo: "**"
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Diff Review Contract

> These rules define how the agent must read, map, and account for every changed hunk before producing findings. Adapted for GitHub Copilot agent review.

## Diff Map (mandatory first step)

Before producing any findings, build a **Diff Map** from the PR changed files.

The Diff Map must include:
- Every file that appears in the PR diff.
- File status: `added`, `modified`, `deleted`, `renamed`, `moved`.
- Changed line ranges (hunks) per file.
- Risk domain per file: `security`, `business-logic`, `test`, `config`, `infrastructure`, `docs`.
- Decision: `reviewed`, `skipped`, `not-accessible`.

### File status rules
- `added`: new file.
- `modified`: content changed, path unchanged.
- `deleted`: file removed.
- `renamed`: path changed + content changed.
- `moved`: path changed, no content change.

### Risk domain rules
- `security`: auth, crypto, input parsing, secrets handling, supply chain.
- `business-logic`: controllers, services, domain logic, repositories.
- `test`: `*.cs` under test paths, `*.feature`, `*.specflow`.
- `config`: `appsettings*.json`, `nuget.config`, Dockerfiles.
- `infrastructure`: GitHub Actions, Terraform, ARM/Bicep.
- `docs`: markdown, XML docs, README.

## Clustering rules (causal grouping)

Group hunks into **Review Chapters** by causal relationship, not by file alone.

- Changes that set up or enable later changes belong together.
- Multi-file changes are fine (schema + API + UI = one chapter).
- Moves/refactors: group deletions + additions as one chapter.
- Split only when changes are truly independent: a reviewer could understand one without knowing the other.
- Tests belong with their implementation chapter.
- Config/dependency changes can be their own chapter if unrelated to a feature chapter.

### Chapter ordering
1. Foundation first: types, interfaces, schemas, utilities.
2. Core logic next: main implementation.
3. Integration last: wiring, configuration, tests.

### Hunk ordering within a chapter
- Group all hunks from the same file together.
- Within the same file, list hunks in ascending line order.

## Coverage rules

Every changed hunk must be accounted for exactly once.

- No hunk may be omitted without explicit reason.
- No hunk may appear in more than one chapter.
- If a file is skipped (e.g., auto-generated, lockfile-only), list it under `Files skipped` with reason.

### Skip reasons (examples)
- `auto-generated`: `*.Designer.cs`, `*.g.cs`, `*.generated.cs`, `**/Migrations/*.cs` (unless PR claims manual changes).
- `lockfile-only`: no dependency version changes.
- `binary`: images, fonts, compiled assets.
- `out-of-scope`: docs not affecting behavior, large generated snapshots.

## Human judgment questions

Separate **bugs/linter-catchable issues** from **questions only a human can answer**.

- Bugs (SQL injection, async void, missing null checks) go into findings with severity.
- Human judgment questions go into `Human judgment questions`.
- Do not invent questions to fill space. Use empty array when none apply.
- Frame each question as a question, not a statement.

### Good examples
- "Should `retryCount` reset when the user switches orgs?"
- "Is a 60-minute session timeout appropriate for this user base?"

### Bad examples
- "Check that the auth logic is correct." — vague.
- "The function now handles errors." — changelog item.
- "Make sure the tests pass." — CI catches this.

## Token budget and scoping

- Max files reviewed per pass: 25.
- Priority order: security-sensitive > business logic > tests > config > docs.
- For PRs >25 files: build Diff Map for all, review top 25 by risk, list skipped files explicitly.
- For files >500 lines: read with offset/limit targeting changed hunks only.
