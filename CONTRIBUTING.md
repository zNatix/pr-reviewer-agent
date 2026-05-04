# Contributing to pr-reviewer-agent

Thanks for helping improve the PR reviewer agent.

## How to propose a new instruction file

1. Create `instructions/your-domain.instructions.md` in `.github/instructions/`
2. Include YAML frontmatter with `applyTo` (glob patterns) and `excludeAgent`
3. Follow the existing severity structure: `## 🔴 Critical` → `## 🟡 Warning` → `## 🔵 Suggestion`
4. Add a row to the instruction file table in `README.md` and `copilot-instructions.md`
5. Add a row to the agent's instruction table in `pr-reviewer.agent.md`
6. Test on a sample PR with known issues in your domain

## How to propose a new agent

1. Create `.github/agents/your-agent.agent.md`
2. Follow the `pr-reviewer.agent.md` structure: persona, process, flag catalog, prompt injection defense
3. Add a `model` field with fallback array

## Submission checklist

- [ ] YAML frontmatter is valid (run `.github/workflows/validate-instructions.yml`)
- [ ] `applyTo` uses exclusion patterns to avoid overlap with test/migration specific files
- [ ] Severity definitions align with `review-output.instructions.md`
- [ ] No hardcoded secrets or credentials
- [ ] Instruction file is focused — one domain per file
