# Bad Practice: Unpinned GitHub Actions

## 🔴 Critical

Referencing actions by mutable tag or branch allows compromised or malicious code to run in your CI pipeline.

```yaml
name: Build
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v3
      - run: dotnet build
```

**Expected finding:** Flag as 🔴 Critical supply-chain risk because floating tags (`@v4`, `@v3`) can be retargeted to malicious commits without code review.
