---
applyTo: "**/*.cs"
excludeAgent: "coding-agent"
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

## What to Flag
- Tests with no assertions
- Tests that only assert `Is.NotNull` without further verification
- Tests with external dependencies not mocked (unit tests)
- Missing tests for new public methods
- Missing [TestCase] coverage for edge cases (null, empty, boundary)
