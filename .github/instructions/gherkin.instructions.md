---
applyTo: "**/*.feature"
version: "1.0.0"
excludeAgent: ["coding-agent"]
---

# Gherkin Feature File Standards

> For step definition and hook standards, see `reqnroll.instructions.md`.

## Feature File Structure
- `Feature:` must describe business value in user-centric language
- `Scenario:` names use business terminology, never implementation details
- Each scenario tests ONE behavior
- Use `Scenario Outline` + `Examples:` for data variations (don't copy-paste scenarios)
- Use `Background:` for shared preconditions across all scenarios in a feature (not for data that varies per scenario)

## Given-When-Then Ordering
- `Given` establishes context and preconditions
- `When` describes the action — one action per scenario
- `Then` verifies ONE outcome (multiple `And` for same outcome is OK)
- Never: Given-Then-When, And-When-Then spaghetti ordering
- Step text: Given = past tense, When = present tense (convention)

## Data Tables & Doc Strings
- Use Data Tables for structured input/output in steps
- Use `"""` doc strings for multi-line text or JSON payloads
- `Examples:` tables for `Scenario Outline` — one row per data set

## Tags
- `@smoke` — critical path tests
- `@regression` — defensive coverage
- `@slow` — tests taking >5 seconds
- `@skip` — temporarily disabled with documented reason

## Internationalization
- If features use non-English language, declare with `# language: <code>` at top of file
- Keep language consistent within a project

## Anti-patterns to Flag
- Scenarios without assertions (no `Then`)
- Scenarios longer than 15 lines
- Implementation details in Gherkin (CSS selectors, database queries, API paths)
- Ambiguous step text that could match multiple step definitions without `[Scope]`
- Technical jargon in scenario names (e.g., "Test POST /api/orders returns 200")
