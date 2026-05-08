# GitHub Copilot Code Review Setup Guide

> Based on official GitHub Copilot docs (May 2026).

## Prerequisites

- **Copilot Business** or **Copilot Enterprise** subscription.
- Organization policy must explicitly enable **Copilot Code Review**.
- Personal plans: **Copilot Pro** or **Copilot Pro+**.

## Per-User Setup (Copilot Pro / Pro+)

1. Click your profile photo → **Settings**.
2. In the left sidebar, click **Copilot**.
3. Under **Automatic Copilot code review**, select your preference from the dropdown.

## Per-Repository Setup (Branch Rulesets)

1. On the repo, go to **Settings → Rules → Rulesets**.
2. Click **New branch ruleset**.
3. Under **Target branches**, add the branches to protect (e.g., `main`, `release/**`).
4. Scroll to **Code review** and check:
   - **Automatically request Copilot code review**
   - *(Optional)* **Review new pushes**
   - *(Optional)* **Review draft pull requests**
5. Save the ruleset.

## Per-Organization Setup (Repository Rulesets)

1. Go to **Organization Settings → Repository → Rulesets**.
2. Click **New ruleset** and choose **Repository ruleset**.
3. Select **Target repositories** (all or specific).
4. Configure **Target branches** as above.
5. Enable the same Copilot code review options and save.

## Important Notes

- **GitHub Actions minutes**: Starting **June 1, 2026**, Copilot Code Review consumes Actions minutes. Monitor usage.
- **Default excluded files**: Copilot excludes lockfiles (e.g., `package-lock.json`, `yarn.lock`), config files (e.g., `.env`, `*.toml`), SVG, logs, `vendor/`, generated code, and similar assets from review.
- **Custom instructions**: Repositories can enable a **Custom instructions** toggle in repo settings to tailor review behavior.
- **Model switching**: Model switching is **not supported** for Copilot Code Review. The default model is used.
