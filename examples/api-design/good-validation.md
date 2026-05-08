# Good Practice: Validated API Input

## ✅ Good Practice

Validate incoming models explicitly, use DTOs at the boundary, and return structured problem details.

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public class OrdersController : ControllerBase
{
    [HttpPost]
    [ProducesResponseType(typeof(OrderDto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> CreateOrder(
        [FromBody] CreateOrderDto dto,
        CancellationToken cancellationToken)
    {
        if (!ModelState.IsValid)
            return ValidationProblem(ModelState);

        var order = MapToEntity(dto);
        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);

        var result = MapToDto(order);
        return CreatedAtAction(nameof(GetOrder), new { id = result.Id }, result);
    }
}
```

Rules demonstrated:
- DTO at controller boundary (no EF entity exposure)
- `[Authorize]` applied
- `CancellationToken` propagated
- `ValidationProblemDetails` returned for 400s
- `CreatedAtAction` with DTO
