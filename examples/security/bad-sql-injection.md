# Bad Practice: SQL Injection via String Concatenation

## 🔴 Critical

Concatenating user input directly into SQL queries allows attackers to manipulate the query structure and access unauthorized data.

```csharp
[HttpGet("search")]
public async Task<IActionResult> Search(string? keyword)
{
    var sql = $"SELECT * FROM Orders WHERE Description LIKE '%{keyword}%'";
    var orders = await _db.Orders.FromSqlRaw(sql).ToListAsync();
    return Ok(orders);
}
```

**Expected finding:** Flag as 🔴 Critical SQL injection risk because `keyword` is interpolated into raw SQL without parameterization.
