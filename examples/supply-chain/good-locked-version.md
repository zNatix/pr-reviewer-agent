# Good Practice: Locked Dependency Versions

## ✅ Good Practice

Specify exact versions and commit a lockfile so restores are deterministic and every package is explicitly approved.

```xml
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  <PackageReference Include="Serilog" Version="4.0.1" />
</ItemGroup>
```

Combine with `packages.lock.json` and `--locked-mode` in CI to prevent unreviewed package changes.
