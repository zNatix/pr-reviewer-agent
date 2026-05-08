# Example: PR Review Output

> This is the output from `@pr-reviewer` on a test PR with deliberately injected bugs.
> The PR added 3 files: OrdersController.cs, PlaywrightTests.cs, AppiumTests.cs.
> 16 bugs planted across 4 categories: SQL injection, async void, hardcoded credentials,
> missing disposal, XPath misuse, Thread.Sleep, static driver, and more.

---

## Review Summary
- Files reviewed: 3
- 🔴 Critical: 6 (must fix before merge)
- 🟡 Warnings: 8 (should fix before merge)
- 🔵 Suggestions: 0 (address at your discretion)
- BDD coverage: N/A (no .feature files in this PR)
- Missing tests: 2 uncovered paths detected

### Verdict: ❌ Request Changes

---

## Findings by File

### OrdersController.cs

---

**Location**: `OrdersController.cs:15`
**Severity**: 🔴 Critical
**Issue**: SQL injection via string concatenation in raw SQL query
**Why it matters**: User-controlled `keyword` parameter is concatenated directly into SQL. Attacker input like `' OR 1=1 --` exfiltrates the entire Orders table. This is OWASP #1 injection flaw.
**Fix**: Use parameterized LINQ instead:
```csharp
var orders = await _db.Orders
    .Where(o => o.Description.Contains(keyword ?? ""))
    .ToListAsync();
```
Or if raw SQL is required, use `FormattableString`:
```csharp
FormattableString sql = $"SELECT * FROM Orders WHERE Description LIKE '%' + {keyword} + '%'";
var orders = await _db.Orders.FromSqlInterpolated(sql).ToListAsync();
```
**Reference**: https://learn.microsoft.com/en-us/ef/core/querying/sql-queries#passing-parameters

---

**Location**: `OrdersController.cs:22`
**Severity**: 🔴 Critical
**Issue**: `async void` on controller action `CreateOrder`
**Why it matters**: ASP.NET Core cannot track `async void` methods — exceptions crash the process. The caller gets no response and the server terminates.
**Fix**:
```csharp
[HttpPost]
public async Task<IActionResult> CreateOrder(Order order)
{
    _db.Orders.Add(order);
    await _db.SaveChangesAsync();
    return CreatedAtAction(nameof(Get), new { id = order.Id }, order);
}
```
**Reference**: https://learn.microsoft.com/en-us/aspnet/core/mvc/controllers/routing#async-void

---

**Location**: `OrdersController.cs:28`
**Severity**: 🟡 Warning
**Issue**: No null check on `FindAsync` result before calling `Remove()`
**Why it matters**: If `id` doesn't exist, `order` is null and `_db.Orders.Remove(null)` throws `ArgumentNullException`. No error handling at all.
**Fix**:
```csharp
var order = await _db.Orders.FindAsync(id);
if (order is null) return NotFound();
_db.Orders.Remove(order);
await _db.SaveChangesAsync();
return NoContent();
```

---

**Location**: `OrdersController.cs:34`
**Severity**: 🔴 Critical
**Issue**: Hardcoded production database connection string with password
**Why it matters**: This credential is now in git history, visible to anyone with repo access. The password `SuperSecret123!` is exposed. This is a data breach waiting to happen.
**Fix**: Move to configuration:
```csharp
var connString = _configuration.GetConnectionString("DefaultConnection");
```
And in `appsettings.Development.json` (gitignored):
```json
{ "ConnectionStrings": { "DefaultConnection": "Server=..." } }
```

---

### PlaywrightTests.cs

---

**Location**: `PlaywrightTests.cs:12`
**Severity**: 🟡 Warning
**Issue**: XPath locator instead of semantic locator
**Why it matters**: XPath `//div[@class='login-form']//input[1]` breaks if a designer adds a `<div>` above the form or changes the class name. Playwright recommends: role > label > placeholder > testid > CSS > XPath (last resort).
**Fix**:
```csharp
var usernameField = Page.GetByLabel("Username");
// or
var usernameField = Page.GetByPlaceholder("Enter your username");
```
**Reference**: https://playwright.dev/docs/locators

---

**Location**: `PlaywrightTests.cs:16`
**Severity**: 🟡 Warning
**Issue**: `Thread.Sleep(2000)` as synchronization mechanism
**Why it matters**: Flaky — if the server takes 2.1 seconds, test fails. If it takes 100ms, waste 1.9s per test run. Playwright auto-waits for assertions.
**Fix**: Remove the sleep, use web-first assertion:
```csharp
await Page.GetByRole(AriaRole.Button, new() { Name = "Submit" }).ClickAsync();
await Expect(Page).ToHaveURLAsync("**/dashboard");
```

---

**Location**: `PlaywrightTests.cs:19`
**Severity**: 🔴 Critical
**Issue**: `.Result` on async Playwright method `TitleAsync()`
**Why it matters**: `.Result` blocks the thread and can deadlock when `SynchronizationContext` is captured. In Playwright, all operations are async. Must `await`.
**Fix**:
```csharp
var title = await Page.TitleAsync();
Assert.That(title, Does.Contain("Dashboard"));
```

---

**Location**: `PlaywrightTests.cs:9-24`
**Severity**: 🟡 Warning
**Issue**: Test has no assertion that verifies successful login
**Why it matters**: The test navigates and clicks but never checks that the login actually succeeded. A redirect to an error page passes the test.
**Fix**: Add post-login assertions:
```csharp
await Expect(Page.GetByText("Welcome, admin")).ToBeVisibleAsync();
```

---

### AppiumTests.cs

---

**Location**: `AppiumTests.cs:11`
**Severity**: 🔴 Critical
**Issue**: `static AndroidDriver` field — not thread-safe, can't parallelize
**Why it matters**: If any test runs in parallel, multiple threads share the same driver → race conditions, stale element references, test corruption. Appium driver sessions are not thread-safe.
**Fix**: Remove `static`, create fresh driver per test in `[SetUp]`:
```csharp
private AndroidDriver _driver;

[SetUp]
public void Setup()
{
    // ... create driver ...
}
```

---

**Location**: `AppiumTests.cs:16-23`
**Severity**: 🟡 Warning
**Issue**: Hardcoded device capabilities (device name, platform version, package names)
**Why it matters**: Tied to one specific device. Can't run on CI with different emulators. Package names change between builds.
**Fix**: Externalize via environment variables:
```csharp
options.DeviceName = Environment.GetEnvironmentVariable("APPIUM_DEVICE") ?? "Android Emulator";
options.PlatformVersion = Environment.GetEnvironmentVariable("APPIUM_PLATFORM_VERSION") ?? "14.0";
options.AddAdditionalAppiumOption("appPackage", 
    Environment.GetEnvironmentVariable("APPIUM_APP_PACKAGE") ?? "com.android.settings");
```

---

**Location**: `AppiumTests.cs:24`
**Severity**: 🟡 Warning
**Issue**: Hardcoded Appium server URL
**Why it matters**: Different environments (local dev, CI, cloud farm) have different server URLs. Breaks on any environment except the developer's machine.
**Fix**:
```csharp
var serverUri = new Uri(Environment.GetEnvironmentVariable("APPIUM_HOST") ?? "http://127.0.0.1:4723/");
```

---

**Location**: `AppiumTests.cs:27`
**Severity**: 🔴 Critical
**Issue**: Missing `[TearDown]` — no `driver.Quit()` or `driver.Dispose()`
**Why it matters**: Appium sessions stay alive consuming server resources. Over multiple test runs, sessions accumulate until the server runs out of capacity or crashes.
**Fix**:
```csharp
[TearDown]
public void TearDown()
{
    try { _driver?.Quit(); } catch { /* don't hide test failures */ }
    _driver?.Dispose();
}
```

---

**Location**: `AppiumTests.cs:32`
**Severity**: 🟡 Warning
**Issue**: XPath locator on mobile without explicit wait
**Why it matters**: Appium XPath on Android is slow (traverses entire UI tree per query). Without `WebDriverWait`, the element may not exist yet → `NoSuchElementException`.
**Fix**:
```csharp
var wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(10));
var batteryItem = wait.Until(ExpectedConditions.ElementIsVisible(
    MobileBy.AccessibilityId("Battery")));
```
Prefer `AccessibilityId` over XPath on mobile.

---

**Location**: `AppiumTests.cs:36`
**Severity**: 🟡 Warning
**Issue**: `Thread.Sleep(1000)` as synchronization
**Why it matters**: Same issue as Playwright — flaky and slow. Use explicit wait instead.
**Fix**: Add `WebDriverWait` for the expected state after click:
```csharp
wait.Until(d => d.PageSource.Contains("Battery usage"));
```

---

## Skipped Files
No files skipped — PR is under the 25-file cap.

---

## Prompt Injection Check
✅ No prompt injection detected in PR description, commit messages, or file contents.
