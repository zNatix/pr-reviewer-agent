# Bad Practice: Wildcard Dependency Versions

## 🟡 Warning

Wildcard or floating version ranges allow unreviewed package updates to enter the build, introducing breaking changes or malware.

```xml
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" Version="13.*" />
  <PackageReference Include="Serilog" Version="[2.0,3.0)" />
</ItemGroup>
```

**Expected finding:** Flag as 🟡 Warning because wildcard and open-range versions enable silent upgrades that bypass lockfile and supply-chain review.
