# Bad Practice: Missing Input Validation

## 🟡 Warning

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

**Expected finding:** Flag as 🟡 Warning because there is no `[ApiController]` model validation check and no explicit `ModelState.IsValid` guard.
