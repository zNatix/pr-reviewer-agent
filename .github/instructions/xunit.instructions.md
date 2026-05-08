---
applyTo: ["**/*Tests.cs", "**/*Test.cs", "**/Tests/**/*.cs"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

## 🔴 Critical
- Use `[Fact]` for parameterless tests, `[Theory]` + `[InlineData]` / `[MemberData]` for data-driven tests. Never use NUnit `[Test]` or `[TestCase]`.
- Constructor injection for shared state; use `IClassFixture<T>` or `ICollectionFixture<T>`. Never use NUnit `[SetUp]` / `[TearDown]`.
- Use `Assert.Throws<T>` / `Assert.ThrowsAsync<T>` for expected exceptions. Do not use `[ExpectedException]`.
- One conceptual assertion per test. Tests asserting `Assert.True(true)` or empty bodies are invalid.

## 🟡 Warning
- xUnit runs tests in parallel by default. Serialize with `[Collection("Name")]` when shared mutable state exists.
- No `[Timeout]` attribute in xUnit v2; v3 accepts `CancellationToken` parameter. Flag usage of `[Timeout]`.
- Flag `Thread.Sleep` inside async tests; use `Task.Delay` with cancellation.
- Fixtures must implement `IDisposable` / `IAsyncDisposable`. Flag missing disposal.

## 🔵 Suggestion
- Naming: `MethodName_Scenario_ExpectedBehavior`.
- Keep test classes focused; one concern per class.
- Use `IAsyncLifetime` for async fixture setup when needed.
