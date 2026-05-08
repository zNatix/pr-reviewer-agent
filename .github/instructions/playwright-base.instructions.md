---
applyTo: ["**/*Playwright*.cs", "**/*PlaywrightTest*.cs", "**/E2E/**/*.cs", "**/Playwright*/**/*.cs"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Playwright for .NET — Base Classes & Locators

> Official docs: https://playwright.dev/dotnet/docs/intro
> Best practices: https://playwright.dev/docs/best-practices
> NuGet: `Microsoft.Playwright` + `Microsoft.Playwright.NUnit` / `Microsoft.Playwright.MSTest`

## Base Classes & Test Structure

### Use the official base classes
- Prefer `PageTest` (one isolated `Page` per test), `ContextTest` (one `BrowserContext` per test), or `BrowserTest` (shared browser)
- Never instantiate `IPlaywright` / `IBrowser` / `IBrowserContext` manually — the base class manages the lifecycle
- Override `ContextOptions()` to customize browser context (viewport, color scheme, base URL, geolocation, etc.)

### Test Isolation
- Each test gets a fresh `BrowserContext` (equivalent to incognito profile) — tests are isolated by default
- Do NOT share state between tests via `static` fields or `[OneTimeSetUp]` for page-level data
- Use `[SetUp]` / `TestInitialize` for per-test preconditions, not for business logic

### Run Configuration
- Browser via `.runsettings` or CLI: `Playwright.BrowserName=chromium|firefox|webkit`
- Headless via `Playwright.LaunchOptions.Headless`
- Parallel: NUnit `[Parallelizable]`; MSTest `ExecutionScope.ClassLevel`
- `DEBUG=pw:api` for verbose logging

## Locators (CRITICAL)

### Priority order — use the most resilient locator first
1. `GetByRole(AriaRole.Button, new() { Name = "Submit" })` — user-facing, accessible
2. `GetByLabel("Username")` — form labels
3. `GetByPlaceholder("Search...")` — input placeholders
4. `GetByText("Welcome back")` — visible text content
5. `GetByTestId("submit-button")` — explicit `data-testid` attributes (most stable, requires dev cooperation)
6. `Locator("css=...")` — CSS selectors **(last resort)**
7. `Locator("xpath=...")` — XPath **(AVOID — brittle, tied to DOM structure)**

### Locator anti-patterns — flag immediately
- XPath selectors: `Page.Locator("//div[@class='foo']/span[2]")` → unstable across DOM changes
- CSS class-based selectors tied to framework internals (e.g., Tailwind hashes, CSS module class names)
- Index-based selectors: `.Nth(2)` → fragile; use filtering instead
- Chaining more than 3 locators

### Chaining & Filtering
- Use chaining to narrow scope: `Page.GetByRole(AriaRole.Listitem).Filter(new() { HasText = "Product 2" })`
- Filter by text or by another locator — not by DOM position
- Combine locators: `Page.GetByTestId("cart").GetByRole(AriaRole.Button, new() { Name = "Checkout" })`

## Assertions

### Use Playwright's web-first assertions (not NUnit assertions for page state)
- ✅ `await Expect(Page).ToHaveTitleAsync("My App")`
- ✅ `await Expect(locator).ToBeVisibleAsync()`
- ✅ `await Expect(locator).ToContainTextAsync("Success")`
- ❌ `Assert.That(locator.IsVisibleAsync().Result, Is.True)` — race condition + `.Result` antipattern
- ❌ `Thread.Sleep(2000)` before assertion — Playwright auto-waits

### Common assertions
Use `Expect(locator).ToBeVisibleAsync()`, `ToBeHiddenAsync()`, `ToBeEnabledAsync()`, `ToBeDisabledAsync()`, `ToBeCheckedAsync()`, `ToHaveTextAsync()`, `ToContainTextAsync()`, `ToHaveValueAsync()`, `ToHaveAttributeAsync()`, `ToHaveCountAsync()`, `ToHaveURLAsync()`, `ToHaveTitleAsync()`.
