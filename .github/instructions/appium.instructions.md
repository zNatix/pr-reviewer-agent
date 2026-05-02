---
applyTo: ["**/*Appium*.cs", "**/*AppiumTest*.cs", "**/*MobileTest*.cs", "**/Mobile*/**/*.cs", "**/Appium*/**/*.cs"]
excludeAgent: "coding-agent"
---

# Appium for .NET — Mobile Test Automation Standards

> Official docs: https://appium.io/docs/en/2.3/quickstart/test-dotnet/
> Client repo: https://github.com/appium/dotnet-client/
> NuGet: `Appium.WebDriver` (extends Selenium `OpenQA.Selenium`)

## Driver Lifecycle & Architecture

### Driver types
- `AndroidDriver` — Android (UIAutomator2, Espresso automation engines)
- `IOSDriver` — iOS (XCUITest automation engine)
- `WindowsDriver` — Windows desktop apps
- All extend `OpenQA.Selenium.Appium.AppiumDriver`, which extends Selenium's `WebDriver`

### Lifecycle (per test or per scenario — NEVER static/singleton)
```
[OneTimeSetUp]  → Create Appium server connection (if shared across tests)
[SetUp]         → Create driver with capabilities (fresh session per test)
[Test]          → Execute test
[TearDown]      → driver.Quit() + driver.Dispose()
[OneTimeTearDown] → Cleanup (if any)
```

- ✅ Use `driver.Quit()` in `[TearDown]` to close the Appium session
- ✅ Use `driver.Dispose()` after `Quit()` to release local resources
- ✅ Use `[OneTimeSetUp]` for expensive setup (emulator launch, server health check)
- ❌ Never create driver as `static` field — sessions are not thread-safe
- ❌ Never call `Quit()` in `[OneTimeTearDown]` when drivers are created in `[SetUp]` — scope mismatch

## Capabilities (CRITICAL)

### Capabilities must be externalized
- ❌ Hardcoded capabilities in test code (deviceName, platformVersion, app path)
- ✅ Read from environment variables, config file, or `appsettings.json`
- ✅ Use `ConfigurationBuilder` or `IOptions<T>` pattern

### Required capabilities (Appium 2.x)
```
var options = new AppiumOptions();
options.AutomationName = AutomationName.AndroidUIAutomator2; // or XCUITest
options.PlatformName = "Android"; // or "iOS"
options.DeviceName = Environment.GetEnvironmentVariable("APPIUM_DEVICE") ?? "Android Emulator";
```

### App provision
- `options.App = "/path/to/app.apk"` — local path
- Remote URLs require pre-uploaded app ID (BrowserStack, Sauce Labs, LambdaTest)
- Never commit `.apk` / `.ipa` files to the repo — use CI artifacts or cloud device farms

### Cloud Device Farms (BrowserStack, Sauce Labs, LambdaTest)
- Cloud capabilities use vendor-specific namespaces:
  - BrowserStack: `bstack:options` with `userName`, `accessKey`, `appiumVersion`
  - Sauce Labs: `sauce:options` with `username`, `accessKey`
  - LambdaTest: `lt:options` with `user`, `accessKey`, `w3c: true`
- Flag capabilities without vendor namespace when targeting cloud farms (W3C may reject them silently)
- Never hardcode cloud credentials — use environment variables
- Cloud farm URLs: `https://hub.browserstack.com/wd/hub`, `https://ondemand.saucelabs.com/wd/hub`, `https://hub.lambdatest.com/wd/hub`

### Additional Appium options
- `noReset: true` — don't reset app state between sessions (use cautiously — breaks test isolation)
- `fullReset: true` — uninstall app after session (CI preference)
- `appPackage` + `appActivity` — required for Android
- `bundleId` — required for iOS

## Waits & Synchronization

### Appium/Selenium does NOT have Playwright-style auto-waiting
- ✅ Use explicit waits: `WebDriverWait` with `ExpectedConditions`
- ✅ Use `driver.Manage().Timeouts().ImplicitWait` (set once, applies to all `FindElement` calls)
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
- `driver.LockDevice()` / `driver.UnlockDevice()` — test lock screen scenarios
- `driver.Rotate(ScreenOrientation.Landscape)` — orientation testing
- `driver.PressKeyCode(AndroidKeyCode.Home)` — Android key events
- `driver.ExecuteScript("mobile: terminateApp", ...)` — force-close app
- `driver.ExecuteScript("mobile: activateApp", ...)` — bring app to foreground

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
