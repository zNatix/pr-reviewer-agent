# Bad Practice: Fragile XPath Locator

## 🟡 Warning

XPath locators tied to DOM structure and class names break easily when the UI changes.

```csharp
[Test]
public async Task Login_WithValidCredentials_RedirectsToDashboard()
{
    var usernameField = Page.Locator("//div[@class='login-form']//input[1]");
    await usernameField.FillAsync("admin");

    await Page.Locator("//button[@type='submit']").ClickAsync();
    Thread.Sleep(2000);

    var title = Page.TitleAsync().Result;
    Assert.That(title, Does.Contain("Dashboard"));
}
```

**Expected findings:**
- Brittle XPath locators → 🟡 Warning
- `Thread.Sleep` as synchronization → 🟡 Warning
- Blocking `.Result` on async call → at least 🟡 Warning (may be treated as 🔴 Critical per async rules in production contexts)
