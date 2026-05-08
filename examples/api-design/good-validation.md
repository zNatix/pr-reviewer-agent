# Good Practice: Validated API Input

## ✅ Good Practice

Validate incoming models explicitly and return a 400 Bad Request when validation fails.

```csharp
[HttpPost]
public async Task<IActionResult> CreateOrder([FromBody] Order order)
{
    if (!ModelState.IsValid)
        return BadRequest(ModelState);

    _db.Orders.Add(order);
    await _db.SaveChangesAsync();
    return CreatedAtAction(nameof(GetOrder), new { id = order.Id }, order);
}
```

This ensures only well-formed data reaches the database and clients receive meaningful error responses.
