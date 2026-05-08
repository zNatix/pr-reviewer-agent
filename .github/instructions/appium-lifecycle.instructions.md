---
applyTo: ["**/*Appium*.cs", "**/*AppiumTest*.cs", "**/*MobileTest*.cs", "**/Mobile*/**/*.cs", "**/Appium*/**/*.cs"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Appium for .NET — Driver Lifecycle & Capabilities

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
