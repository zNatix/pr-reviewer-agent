---
applyTo: ["**/*Appium*.cs", "**/*AppiumTest*.cs", "**/*MobileTest*.cs", "**/Mobile*/**/*.cs", "**/Appium*/**/*.cs"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Appium for .NET — Gestures, Device Interaction & Anti-patterns

## Gestures & Mobile-Specific Actions

### Touch actions (Appium 2.x)
- Prefer W3C Actions API over deprecated `TouchAction` class
- Use `driver.PerformActions()` with `PointerInputDevice` for complex gestures
- Flag use of deprecated `TouchAction` / `MultiAction` APIs (removed in Selenium 4+)

### Common gestures
- Swipe: use `driver.ExecuteScript("mobile: swipe", ...)` or W3C Actions
- Scroll: `driver.ExecuteScript("mobile: scroll", ...)` — not `FindElement` + swipe loop
- Long press: W3C Actions with `PointerInputDevice.CreatePointerMove` + pause
- Pinch/zoom: multi-touch W3C Actions

## Device Interaction
- `driver.Lock/UnlockDevice()`, `Rotate()`, `PressKeyCode()`
- `ExecuteScript("mobile: terminateApp")` / `activateApp` for lifecycle tests

## Screenshots & Logging
- `driver.GetScreenshot().SaveAsFile("screenshot.png")` — capture on failure
- `driver.Manage().Logs.GetLog(LogType.Browser)` — webview console logs
- Always wrap screenshot capture in `try-catch` inside `[TearDown]` — don't hide test failures
- Flag screenshots without descriptive file names (use test name + timestamp)

## Parallel Execution
- Appium server supports multiple sessions — but each needs unique `systemPort` (Android) or `wdaLocalPort` (iOS)
- Flag tests marked `[Parallelizable]` without unique port configuration
- Use `appium --port 4723 --base-path /wd/hub` for server; multiple servers for parallel

## 🚫 Anti-patterns to Flag Immediately

### 🔴 Critical — Block Merge
- Hardcoded device capabilities (deviceName, platformVersion, app path, tokens)
- Missing `driver.Quit()` in `[TearDown]` / `[AfterScenario]`
- `driver` as `static` field (not thread-safe, can't parallelize)
- Driver created in constructor instead of `[SetUp]` (no isolation between tests)
- `noReset: true` without explicit justification (breaks test isolation)
- `.Result` or `.Wait()` on async Appium/WebDriver methods
- XPath-only locators without `WebDriverWait` (Appium XPath is slow, element may not exist yet)

### 🟡 Warning
- `Thread.Sleep()` or `Task.Delay()` as synchronization
- `ImplicitWait` used alongside `WebDriverWait` (unpredictable behavior)
- Missing `try-catch` around driver.Quit() in tear down (exceptions hide test failures)
- Tests that depend on execution order (not isolated)
- Missing `Category("Integration")` on Appium tests (they require real devices/emulators)
- `appPackage` / `appActivity` / `bundleId` hardcoded in tests instead of config
- Deprecated `TouchAction` / `MultiAction` usage (use W3C Actions API)
- Context switching without verifying `driver.Contexts` contains the target

### 🔵 Suggestion
- Missing `AccessibilityId` on mobile elements that are tested (improves test stability)
- Screenshot-on-failure without a descriptive file path
- Tests longer than 30 lines without helper methods or Screen Objects
- Duplicate locator chains across tests (extract to Screen Object pattern)
- Not using `--readable-timestamps` on Appium server for CI debugging
- Missing `Category("Mobile")` tag on Appium-specific test classes
