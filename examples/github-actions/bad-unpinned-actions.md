# Bad Practice: Unpinned GitHub Actions

## 🔴 Critical

Referencing actions by mutable tag or branch allows compromised or malicious code to run in your CI pipeline.

```yaml
name: Build
on: [push]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: docker/login-action@v3
      - uses: actions/setup-dotnet@v3
      - run: dotnet build
```

**Expected finding:** Flag as 🔴 Critical supply-chain risk because floating tags (`@v3`) can be retargeted to malicious commits without code review. Note: `actions/*` and `github/*` may use tags if your organization policy permits, but third-party actions should always be pinned.
