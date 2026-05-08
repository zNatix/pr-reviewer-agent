---
applyTo: ["**/*Playwright*.cs", "**/*PlaywrightTest*.cs", "**/E2E/**/*.cs", "**/Playwright*/**/*.cs"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

# Playwright for .NET — Actions, Network & Screenshots

## Actions

### Auto-waiting is built in — don't add manual waits
- Playwright waits for element to be [actionable](https://playwright.dev/dotnet/docs/actionability) before clicking, filling, etc.
- ❌ `await Page.WaitForSelectorAsync("#element"); await Page.ClickAsync("#element")` — redundant
- ❌ `await Task.Delay(500)` — flaky, unnecessary

### Navigation
- `await Page.GotoAsync(url)` — auto-waits for load state
- Use `Page.GotoAsync(url, new() { WaitUntil = WaitUntilState.NetworkIdle })` for SPAs

### Form interactions
- `await Page.GetByLabel("Email").FillAsync("user@test.com")` — clears + types
- `await Page.GetByLabel("Country").SelectOptionAsync(new[] { "Spain" })` — dropdowns
- `await Page.GetByLabel("I agree").CheckAsync()` / `UncheckAsync()` — checkboxes

## Network & Mocking

### API mocking (preferred over hitting real APIs in E2E tests)
- `await Page.RouteAsync("**/api/**", async route => { await route.FulfillAsync(new() { Body = json }); })`
- Mock external dependencies — don't test third-party services
- Use `Page.UnrouteAllAsync()` in `[TearDown]` to clean up routes

### Wait for API responses
- `var response = await Page.WaitForResponseAsync("**/api/orders")` — better than `Task.Delay` after action

## File Upload & Download
- Upload: `await Page.GetByLabel("Upload file").SetInputFilesAsync("file.pdf")`
- Download: `var download = await Page.RunAndWaitForDownloadAsync(() => Page.GetByText("Download").ClickAsync());`
- Never mock file dialogs with `Dialog` handler — use `SetInputFilesAsync`

## Screenshots, Videos & Traces
- `await Page.ScreenshotAsync(new() { Path = "screenshot.png" })`
- Enable trace: override `ContextOptions()` with `new BrowserNewContextOptions { RecordVideoDir = "videos/" }`
- Use `Page.Video?.SaveAsync("video.webm")` in tear down when recording
