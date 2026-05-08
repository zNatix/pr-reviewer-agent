# Good Practice: Externalized Appium Capabilities

## ✅ Good Practice

Read capabilities and server endpoints from environment variables so the same test runs locally, on CI, or in a cloud device farm.

```csharp
[TestFixture]
public class MobileTests
{
    private AndroidDriver _driver;

    [SetUp]
    public void Setup()
    {
        var options = new AppiumOptions();
        options.PlatformName = "Android";
        options.AutomationName = AutomationName.AndroidUIAutomator2;
        options.DeviceName = Environment.GetEnvironmentVariable("APPIUM_DEVICE") ?? "Android Emulator";
        options.PlatformVersion = Environment.GetEnvironmentVariable("APPIUM_PLATFORM_VERSION") ?? "14.0";
        options.AddAdditionalAppiumOption("appPackage",
            Environment.GetEnvironmentVariable("APPIUM_APP_PACKAGE") ?? "com.android.settings");

        var serverUri = new Uri(Environment.GetEnvironmentVariable("APPIUM_HOST") ?? "http://127.0.0.1:4723/");
        _driver = new AndroidDriver(serverUri, options);
    }

    [TearDown]
    public void TearDown()
    {
        try
        {
            _driver?.Quit();
        }
        finally
        {
            _driver?.Dispose();
        }
    }
}
```

Externalized configuration makes the test suite portable and environment-agnostic. Required capabilities (`AutomationName`) and teardown (`Quit` + `Dispose`) are included.
