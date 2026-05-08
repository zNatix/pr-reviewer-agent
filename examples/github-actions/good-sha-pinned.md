# Good Practice: SHA-Pinned GitHub Actions

## ✅ Good Practice

Pin third-party actions to a full-length commit SHA and annotate the expected version in a comment.

```yaml
name: Build
on: [push]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-dotnet@6bd8b7f7774af54e05809fcc5431931b3eb1ddee # v4.0.1
      - run: dotnet build
```

SHA pinning guarantees that only the audited commit runs, even if the tag is later moved or compromised.
