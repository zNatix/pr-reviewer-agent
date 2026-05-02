---
applyTo: "**/*.cs"
excludeAgent: "coding-agent"
---

# Playwright for .NET — Test Automation Standards

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
- Browser name via `.runsettings` or CLI: `Playwright.BrowserName=chromium|firefox|webkit`
- Headless mode configurable via `Playwright.LaunchOptions.Headless=false`
- Parallelization: MSTest uses `ExecutionScope.ClassLevel` by default; NUnit supports `[Parallelizable]`
- Use `DEBUG=pw:api` for verbose API logging when debugging

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
| Assertion | Purpose |
|---|---|
| `ToBeVisibleAsync()` | Element is visible and in DOM |
| `ToBeHiddenAsync()` | Element is hidden or removed |
| `ToBeEnabledAsync()` / `ToBeDisabledAsync()` | Interactive state |
| `ToBeCheckedAsync()` | Checkbox/radio state |
| `ToHaveTextAsync("text")` | Exact text match |
| `ToContainTextAsync("text")` | Text contains substring |
| `ToHaveValueAsync("val")` | Input value |
| `ToHaveAttributeAsync("href", "/login")` | Attribute value |
| `ToHaveCountAsync(3)` | Number of matching elements |
| `ToHaveURLAsync("**/dashboard")` | URL pattern match |
| `ToHaveTitleAsync("Title")` | Page title |

## Actions

### Auto-waiting is built in — don't add manual waits
- Playwright waits for element to be [actionable](https://playwright.dev/dotnet/docs/actionability) before clicking, filling, etc.
- ❌ `await Page.WaitForSelectorAsync("#element"); await Page.ClickAsync("#element")` — redundant
- ❌ `await Task.Delay(500)` — flaky, unnecessary

### Navigation
- `await Page.GotoAsync(url)` — auto-waits for load state
- Use `Page.GotoAsync(url, new() { WaitUntil = WaitUntilState.NetworkIdle })` for SPAs

### Form interactions
- `await Page.GetByLabel("Email").FillAsync("user@test.com")` — clears + types
- `await Page.GetByLabel("Country").SelectOptionAsync(new[] { "Spain" })` — dropdowns
- `await Page.GetByLabel("I agree").CheckAsync()` / `UncheckAsync()` — checkboxes

## Network & Mocking

### API mocking (preferred over hitting real APIs in E2E tests)
- `await Page.RouteAsync("**/api/**", async route => { await route.FulfillAsync(new() { Body = json }); })`
- Mock external dependencies — don't test third-party services
- Use `Page.UnrouteAllAsync()` in `[TearDown]` to clean up routes

### Wait for API responses
- `var response = await Page.WaitForResponseAsync("**/api/orders")` — better than `Task.Delay` after action

## File Upload & Download
- Upload: `await Page.GetByLabel("Upload file").SetInputFilesAsync("file.pdf")`
- Download: `var download = await Page.RunAndWaitForDownloadAsync(() => Page.GetByText("Download").ClickAsync());`
- Never mock file dialogs with `Dialog` handler — use `SetInputFilesAsync`

## Screenshots, Videos & Traces
- `await Page.ScreenshotAsync(new() { Path = "screenshot.png" })`
- Enable trace: override `ContextOptions()` with `new BrowserNewContextOptions { RecordVideoDir = "videos/" }`
- Use `Page.Video?.SaveAsync("video.webm")` in tear down when recording

## 🚫 Anti-patterns to Flag Immediately

### 🔴 Critical — Block Merge
- `new Playwright()` or manual lifecycle management of `IBrowser`/`IBrowserContext` — use base classes
- `.Result` or `.Wait()` on async Playwright methods — always `await`
- `Thread.Sleep()` or `Task.Delay()` as synchronization mechanism — use assertions with auto-wait
- Hardcoded URLs in tests (use `ContextOptions().BaseURL` or configuration)
- Missing `[TearDown]` / `TestCleanup` that disposes resources

### 🟡 Warning
- XPath locators or CSS locators when role/text/label locators are available
- `Page.WaitForSelectorAsync()` before `ClickAsync()` — redundant
- Tests that depend on execution order (not isolated)
- Multiple `Page.GotoAsync()` in the same test to different domains (use separate tests)
- Tests without assertions (navigation-only)
- `Page.ScreenshotAsync()` calls without `try-catch` (can hide assertion failures)
- Not using `BrowserNewContextOptions` to set consistent viewport/timezone/locale

### 🔵 Suggestion
- Missing `data-testid` attributes when CSS selectors are used repeatedly
- Tests longer than 30 lines without helper methods
- Duplicate locator chains across tests (extract to Page Object or helper)
- Not using `filter()` when `.Nth()` would be clearer
- Overriding `ContextOptions()` without calling `base.ContextOptions()` for defaults
