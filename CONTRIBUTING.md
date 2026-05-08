# Contributing to pr-reviewer-agent

Thanks for helping improve the PR reviewer agent.

## How to propose a new instruction file

1. Create `instructions/your-domain.instructions.md` in `.github/instructions/`
2. Include YAML frontmatter with `applyTo` (glob patterns), `version` (semver), and `excludeAgent` (array)
3. Follow the existing severity structure: `## 🔴 Critical` → `## 🟡 Warning` → `## 🔵 Suggestion`
4. Add a row to the instruction file table in `README.md` and `copilot-instructions.md`
5. Add a row to the agent's instruction table in `pr-reviewer.agent.md`

## How to test locally

No CI runner needed — you can smoke-test instruction file changes manually:

1. **Create a test PR** in your fork with known violations in the domain you're adding
2. **Invoke `@pr-reviewer`** in Copilot Chat on that PR and verify your new rules fire correctly
3. **Check expected severity**: compare against `review-output.instructions.md` definitions. If a rule could be argued as Critical vs Warning, ask: "would I block a production deploy for this?"
4. **Recommended model for testing**: `claude-sonnet-4-6` (catches more edge cases in instructions). For production, omit `model` to let Copilot select the best available model, or pin a supported model from the [official list](https://docs.github.com/en/copilot/reference/ai-models/supported-models)
5. **Validate frontmatter**: the `validate-instructions.yml` workflow runs on PR — check it passes before requesting review

## How to propose a new agent

1. Create `.github/agents/your-agent.agent.md`
2. Follow the `pr-reviewer.agent.md` structure: persona, process, flag catalog, prompt injection defense
3. Set `model` as a single supported string or omit it to inherit the organization's default
4. Set `version` following semver

## Submission checklist

- [ ] YAML frontmatter is valid (CI catches this — `validate-instructions.yml`)
- [ ] `applyTo` uses exclusion patterns to avoid overlap with test/migration specific files
- [ ] `excludeAgent` is a scalar string (not an array)
- [ ] `version` is semver (`X.Y.Z`)
- [ ] Severity definitions align with `review-output.instructions.md`
- [ ] No hardcoded secrets or credentials
- [ ] Instruction file is focused — one domain per file
- [ ] Smoke-tested against a real PR with known violations
