# Bad Practice: Missing Input Validation

## 🔴 Critical

Accepting unvalidated model state can lead to invalid data persistence, downstream errors, or unexpected behavior.

```csharp
[HttpPost]
public async Task<IActionResult> CreateOrder(Order order)
{
    _db.Orders.Add(order);
    await _db.SaveChangesAsync();
    return Ok();
}
```

**Expected finding:** Flag as 🔴 Critical because there is no `[ApiController]` model validation, no explicit `ModelState.IsValid` guard, and the endpoint accepts an EF entity directly.
