---
applyTo: ["**/*Tests.cs", "**/*Test.cs", "**/Tests/**/*.cs"]
version: "1.0.0"
excludeAgent: ["coding-agent"]
---

# NUnit Test Standards

## Method Naming
- Format: `MethodName_Scenario_ExpectedBehavior`
- Examples: `CalculateTax_WithZeroIncome_ReturnsZero`, `Authenticate_WithInvalidToken_ThrowsUnauthorized`

## Test Structure
- Use `[SetUp]` for common arrange — keep it minimal
- Use `[TearDown]` for cleanup — always in try-catch
- Use `[OneTimeSetUp]` only for expensive resources (databases, containers)
- Tests must never depend on execution order

## Assertions
- Use constraint model: `Assert.That(result, Is.EqualTo(expected))`
- Never classic: `Assert.AreEqual(expected, result)`
- One conceptual assertion per test; use `Assert.Multiple { ... }` when validating multiple properties of the same result
- `Is.EqualTo` (value equality via `.Equals()`) vs `Is.SameAs` (reference equality) vs `Is.EquivalentTo` (unordered collection comparison) — be precise
- Use `Assert.That(action, Throws.TypeOf<X>().With.Message.Contains("..."))` when exception message matters
- Never `Assert.True(true)` or assertions that don't actually verify behavior

## Test Categories
- `[Category("Unit")]` — no external dependencies
- `[Category("Integration")]` — database, filesystem, network
- `[Category("BDD")]` — Reqnroll tests

## Parallel Execution (NUnit 4+)
- Use `[Parallelizable(ParallelScope.All)]` at assembly level for independent tests
- Never mark tests as parallelizable if they share database or file system state
- Use `[NonParallelizable]` on specific tests that must run sequentially

## Timeouts & Cancellation
- Use `[CancelAfter(milliseconds)]` on tests with risk of hanging (network calls, external APIs)
- Long-running tests without timeout → flag

## Advanced Patterns

### Test Execution Order
- `[Order(N)]` only when tests genuinely depend on prior state (rare). Document the dependency reason in a comment.
- Flag `[Order]` without justification — test isolation should be the default.

### Data-Driven Tests
- Use `[TestCaseSource(typeof(MyTestData), nameof(MyTestData.Cases))]` for complex or dynamic test data
- `[TestCase]` for simple inline data; `[TestCaseSource]` for external data sources or reusable datasets
- Flag `[TestCaseSource]` that references an undefined member or non-`static` source
- Never use `[TestCase]` with 10+ values (unreadable) — switch to `[TestCaseSource]`

### Explicit Tests
- `[Explicit]` marks tests that only run when explicitly selected (e.g., destructive tests, prod-like environment tests)
- Flag `[Explicit]` without documented justification — silent skip from CI can hide regressions
- Valid reasons: manual-only run, requires special hardware, writes to production database

## What to Flag
- Tests with no assertions
- Tests that only assert `Is.NotNull` without further verification
- Tests with external dependencies not mocked (unit tests)
- Missing tests for new public methods
- Missing [TestCase] coverage for edge cases (null, empty, boundary)
