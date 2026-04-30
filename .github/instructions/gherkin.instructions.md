---
applyTo: "**/*.feature"
excludeAgent: "cloud-agent"
---

# Gherkin / Reqnroll Standards

## Feature File Rules
- `Feature:` must describe business value in user-centric language
- `Scenario:` names use business terminology, never implementation details
- Each scenario tests ONE behavior
- Use `Scenario Outline` + `Examples:` for data variations (don't copy-paste scenarios)

## Given-When-Then Rules
- `Given` establishes context and preconditions
- `When` describes the action — one action per scenario
- `Then` verifies ONE outcome (multiple `And` for same outcome is OK)
- Never: Given-Then-When, And-When-Then spaghetti ordering

## Tags
- `@smoke` — critical path tests
- `@regression` — defensive coverage
- `@slow` — tests taking >5 seconds
- `@skip` — temporarily disabled with documented reason

## Anti-patterns to flag
- Scenarios without assertions (no `Then`)
- Scenarios longer than 15 lines
- Implementation details in Gherkin (CSS selectors, database queries, API paths)
- Ambiguous step text that could match multiple step definitions without `[Scope]`
