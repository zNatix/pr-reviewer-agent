# Bad Practice: Hardcoded Appium Capabilities

## 🟡 Warning

Hardcoding device names, platform versions, and server URLs makes tests impossible to run on CI or different devices.

```csharp
[OneTimeSetUp]
public void Setup()
{
    var options = new AppiumOptions();
    options.PlatformName = "Android";
    options.DeviceName = "Pixel 7";
    options.PlatformVersion = "14.0";
    options.AddAdditionalAppiumOption("appPackage", "com.android.settings");
    options.AddAdditionalAppiumOption("appActivity", ".Settings");

    _driver = new AndroidDriver(new Uri("http://192.168.1.100:4723/"), options);
}
```

**Expected finding:** Flag as 🟡 Warning because capabilities and server URL are hardcoded, preventing execution on other environments.
