# Good Practice: Accessible Locators in Playwright

## ✅ Good Practice

Prefer semantic locators (role, label, placeholder) and web-first assertions for resilient, fast tests.

```csharp
[Test]
public async Task Login_WithValidCredentials_RedirectsToDashboard()
{
    var usernameField = Page.GetByLabel("Username");
    await usernameField.FillAsync("admin");

    await Page.GetByRole(AriaRole.Button, new() { Name = "Sign in" }).ClickAsync();
    await Expect(Page).ToHaveURLAsync("**/dashboard");

    await Expect(Page.GetByText("Welcome, admin")).ToBeVisibleAsync();
}
```

Semantic locators survive DOM refactoring and auto-waiting eliminates flaky sleeps.
