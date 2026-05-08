---
applyTo: ["**/*Playwright*.cs", "**/*PlaywrightTest*.cs", "**/E2E/**/*.cs", "**/Playwright*/**/*.cs"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Playwright for .NET — Anti-patterns

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
