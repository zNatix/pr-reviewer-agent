---
applyTo: "**/*.cs"
excludeAgent: "cloud-agent"
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
- One logical assertion per test (multiple `Assert.That` on same result is OK)
- Use `Assert.Throws<SpecificException>(() => ...)` for exceptions
- Never `Assert.True(true)` or assertions that don't actually verify behavior

## Test Categories
- `[Category("Unit")]` — no external dependencies
- `[Category("Integration")]` — database, filesystem, network
- `[Category("BDD")]` — Reqnroll tests

## What to Flag
- Tests with no assertions
- Tests that only assert `Is.NotNull` without further verification
- Tests with external dependencies not mocked (unit tests)
- Missing tests for new public methods
- Missing [TestCase] coverage for edge cases (null, empty, boundary)
- Step definition methods over 30 lines (too much logic in step)
