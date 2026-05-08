# Example: Diff Coverage Output

> This is the Diff Coverage block from `@pr-reviewer` on a test PR with deliberately injected bugs.
> The PR added 3 files: OrdersController.cs, PlaywrightTests.cs, AppiumTests.cs.

---

## Diff Coverage
- Files changed: 3
- Files reviewed: 3
- Files skipped: 0
- Changed hunks reviewed: 5
- Skipped hunks: 0

### Review Chapters
1. **Add OrdersController with search and delete endpoints** — `OrdersController.cs` (hunks 1-3)
2. **Add Playwright login test with semantic locators** — `PlaywrightTests.cs` (hunk 1)
3. **Add Appium settings test with device setup** — `AppiumTests.cs` (hunk 1)

### Human Judgment Questions
- "Should the `Search` endpoint allow empty `keyword` without a default filter?" (`OrdersController.cs`)
- "Is `Thread.Sleep(1000)` acceptable as a temporary measure while waiting for a backend fix?" (`AppiumTests.cs`)

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
**Reference**: https://playwright.dev/docs/actionability

---

### AppiumTests.cs

---

**Location**: `AppiumTests.cs:18`
**Severity**: 🔴 Critical
**Issue**: `static` AndroidDriver field is not thread-safe
**Why it matters**: Parallel test execution will corrupt driver state, causing random failures or cross-test contamination. Use instance fields with proper `[SetUp]`/`[TearDown]`.
**Fix**:
```csharp
private AndroidDriver? _driver;
[SetUp]
public void Setup() { ... }
[TearDown]
public void TearDown() => _driver?.Quit();
```

---

**Location**: `AppiumTests.cs:24`
**Severity**: 🔴 Critical
**Issue**: Hardcoded capabilities and server URL
**Why it matters**: Tied to one specific device. Can't run on CI with different emulators. Package names change between builds.
**Fix**: Externalize to config or environment variables:
```csharp
options.PlatformName = Environment.GetEnvironmentVariable("APPIUM_PLATFORM") ?? "Android";
```

---

**Location**: `AppiumTests.cs:40`
**Severity**: 🟡 Warning
**Issue**: XPath locator on mobile without explicit wait
**Why it matters**: XPath is brittle on mobile. Missing explicit wait means element not found errors on slower devices.
**Fix**: Use `AccessibilityId` priority and explicit waits:
```csharp
var batteryItem = _driver.FindElement(MobileBy.AccessibilityId("Battery"));
new WebDriverWait(_driver, TimeSpan.FromSeconds(10))
    .Until(ExpectedConditions.ElementIsVisible(MobileBy.AccessibilityId("Battery")));
```

---

**Location**: `AppiumTests.cs:44`
**Severity**: 🟡 Warning
**Issue**: `Thread.Sleep(1000)` as sync
**Why it matters**: Wastes time and is flaky. Use explicit waits or polling.
**Fix**: Replace with wait:
```csharp
new WebDriverWait(_driver, TimeSpan.FromSeconds(5))
    .Until(d => d.PageSource.Contains("Battery usage"));
```

---

**Location**: `AppiumTests.cs:35`
**Severity**: 🔴 Critical
**Issue**: Missing `[TearDown]` — no `driver.Quit()` or `driver.Dispose()`
**Why it matters**: Leaks Appium sessions, exhausts device resources, and leaves orphan processes.
**Fix**:
```csharp
[TearDown]
public void TearDown() => _driver?.Quit();
```

---

## Review Summary
- Files reviewed: 3
- 🔴 Critical: 6 (must fix before merge)
- 🟡 Warnings: 8 (should fix before merge)
- 🔵 Suggestions: 0 (address at your discretion)
- BDD coverage: N/A (no .feature files in this PR)
- Missing tests: 2 uncovered paths detected

### Verdict: ❌ Request Changes
