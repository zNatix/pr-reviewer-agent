---
applyTo: ["**/*Tests.cs", "**/*Test.cs", "**/Tests/**/*.cs"]
version: "1.0.0"
excludeAgent: "coding-agent"
---

## 🔴 Critical
- Use `[TestMethod]` for tests, `[TestClass]` for classes. `[DataRow]` and `[DynamicData]` for data-driven tests. Do not use NUnit `[Test]` or `[TestCase]`.
- Use `[TestInitialize]` / `[TestCleanup]` for per-test setup; `[ClassInitialize]` / `[ClassCleanup]` for per-class setup. Do not use NUnit `[SetUp]` / `[TearDown]`.
- Use `Assert.ThrowsException<T>` / `Assert.ThrowsExceptionAsync<T>` for expected exceptions. Do not use `[ExpectedException]`.
- One conceptual assertion per test. Tests asserting `Assert.IsTrue(true)` or empty bodies are invalid.

## 🟡 Warning
- `[Timeout]` attribute available. Ensure values are reasonable; avoid zero or extremely long timeouts.
- Use `[DoNotParallelize]` on tests or `[Parallelize]` at assembly level to control concurrency. Default may vary by runner.
- Ensure `[ClassInitialize]` and `[ClassCleanup]` methods are `static` where required.
- Flag `Thread.Sleep` in async tests; prefer `Task.Delay`.

## 🔵 Suggestion
- Naming: `MethodName_Scenario_ExpectedBehavior`.
- Keep test classes focused; one concern per class.
- Use `TestContext` for logging and data sharing when appropriate.
