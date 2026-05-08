# Good Practice: Parameterized Queries

## ✅ Good Practice

Use LINQ or parameterized SQL so the database engine treats user input as data, not executable code.

```csharp
[HttpGet("search")]
public async Task<IActionResult> Search(string? keyword)
{
    var orders = await _db.Orders
        .Where(o => o.Description.Contains(keyword ?? ""))
        .ToListAsync();
    return Ok(orders);
}
```

This approach prevents injection by letting EF Core generate safe, parameterized SQL under the hood.
