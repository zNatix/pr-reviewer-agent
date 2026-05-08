---
applyTo: ["**/*Appium*.cs", "**/*AppiumTest*.cs", "**/*MobileTest*.cs", "**/Mobile*/**/*.cs", "**/Appium*/**/*.cs"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Appium for .NET — Waits, Locators & Context Switching

## Waits & Synchronization

### Appium/Selenium does NOT have Playwright-style auto-waiting
- ✅ Use explicit waits: `WebDriverWait` with `ExpectedConditions`
- ⚠️ `driver.Manage().Timeouts().ImplicitWait` may be set globally, but never mix it with `WebDriverWait` in the same interaction
- ❌ `Thread.Sleep()` or `Task.Delay()` as synchronization — flaky, slow
- ❌ `.Result` or `.Wait()` on async Appium operations — always `await`

### Explicit wait pattern (preferred)
```
var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
var element = wait.Until(ExpectedConditions.ElementIsVisible(By.Id("loginButton")));
element.Click();
```

## Element Location

### Priority order for locators (Appium-specific)
1. `AccessibilityId("loginButton")` — accessibility ID (most stable, cross-platform)
2. `Id("com.app:id/login")` — resource ID (Android native, iOS XCUITest accessibilityIdentifier)
3. `ClassName("android.widget.Button")` — class name (less stable across OS versions)
4. `XPath("//android.widget.Button[@text='Login']")` — XPath **(expensive on mobile, avoid when possible)**
5. `CssSelector(...)` — only for webview/hybrid context

### Locator best practices
- Prefer `AccessibilityId` — works on both Android and iOS, stable, meaningful
- XPath on mobile is **slow** and **CPU-intensive** — flag if used without justification
- Never chain 3+ XPath queries in one test
- Use `FindElement(By.Id(...))` for resource IDs, not XPath

## Context Switching (Hybrid Apps)

### Native ↔ WebView
```
// Switch to webview
driver.Context = driver.Contexts.First(c => c.Contains("WEBVIEW"));
// Back to native
driver.Context = "NATIVE_APP";
```

- Flag missing `try-catch` around context switching (webview may not load)
- Flag hardcoded context names instead of using `driver.Contexts`
- Flag tests that switch contexts without verifying the switch succeeded
