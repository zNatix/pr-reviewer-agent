---
applyTo: ["**/Steps/**/*.cs", "**/StepDefinitions/**/*.cs", "**/Hooks/**/*.cs", "**/Hooks.cs"]
version: "1.0.0"
excludeAgent: ["coding-agent"]
---

# Reqnroll Step Definitions & Hooks Standards

> Reqnroll is the open-source reboot of SpecFlow. Bindings (step definitions, hooks, step argument transformations) are global for the entire Reqnroll project. Namespace is `Reqnroll`, not `TechTalk.SpecFlow`.

## Step Definition Rules

### Size & Delegation
- Step definition methods: <15 lines ideal, 30 max
- Step definitions delegate to page objects / service helpers — no raw Selenium/HttpClient calls in steps
- No business logic in step definitions — they orchestrate, services execute

### Regex & Bindings
- Regex (or Cucumber expressions) in `[Given]`/`[When]`/`[Then]` must be specific enough to avoid ambiguity with other steps
- Use `[Scope]` attribute when binding to a specific feature or tag
- Prefer Cucumber expressions (`Given I have {int} items`) over raw regex for readability

### Reuse & Organization
- Reuse step definitions across features — never duplicate "Given I am logged in" across multiple classes
- Step definition classes must be `public` and methods `public`
- Use constructor injection in step definition classes for dependencies via `IObjectContainer` (Reqnroll's DI, not ASP.NET Core DI)
- Migrating from SpecFlow: replace `TechTalk.SpecFlow` namespace with `Reqnroll`

### Dependency Injection (Reqnroll-specific)
- Reqnroll supports `Microsoft.Extensions.DependencyInjection` directly (unlike SpecFlow)
- Use `IObjectContainer` for step-level context, not `IServiceProvider`
- Context classes injected via constructor or `[ScenarioContext]` / `[FeatureContext]`

### Flag Immediately
- Step definition methods >30 lines
- Raw Selenium/HttpClient calls inside step definitions (delegate to helpers)
- Duplicate step text bindings without `[Scope]` differentiation
- Step definitions that catch exceptions without rethrowing (hides test failures)
- Missing step definition for any Gherkin step in new/altered `.feature` files

## Hooks

### Before/After Scenario
- `[BeforeScenario]`: test data setup only, never business logic
- `[AfterScenario]`: cleanup — always wrapped in try-catch to avoid hiding test failures
- Hooks belong in `Hooks.cs` at project root or `Hooks/` folder — not scattered across step definition classes

### Before/After Feature & Test Run
- `[BeforeFeature]` / `[AfterFeature]`: expensive shared setup (database containers, test servers)
- `[BeforeTestRun]` / `[AfterTestRun]`: assembly-level setup (once per test run)
- All hook methods must be `public static` or `public` depending on scope

### Hook Order
- Use `Order` property on hook attributes when multiple hooks of the same type exist
- `[BeforeScenario(Order = 1)]` runs before `[BeforeScenario(Order = 2)]`

## Anti-patterns to Flag
- Business logic in `[BeforeScenario]` hooks
- Hooks that throw unhandled exceptions in `[AfterScenario]`
- Mixing SpecFlow and Reqnroll namespaces in same project (migration artifact)
- Step definitions with `NotImplementedException` — indicates incomplete migration/scaffolding
- Using `ScenarioContext.Current` (static) instead of injected `ScenarioContext`
