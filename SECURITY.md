# Security Policy

## Supported Versions

This is a template repository for GitHub Copilot custom agents and instructions. Security updates apply to the latest version on the `master` branch.

| Version | Supported          |
| ------- | ------------------ |
| latest master | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in the agent instructions, workflows, or configuration files, please report it responsibly.

**Scope of security reports:**
- Prompt injection vectors not covered by current defenses
- Misleading instructions that could cause Copilot to approve insecure code
- Workflow vulnerabilities (excessive permissions, unsafe `pull_request_target` usage, unpinned actions)
- Secret leakage in examples or documentation
- Supply chain risks in validation scripts or dependencies

**How to report:**
1. Open a **private security advisory** via GitHub Security Advisories (preferred)
2. Or email the repository maintainer (if listed in the profile)

**What to include:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested mitigation (if any)

**Response timeline:**
- Acknowledgment within 48 hours
- Initial assessment within 7 days
- Fix or mitigation plan within 30 days

## Disclosure Policy

We follow coordinated disclosure. Once a fix is released, we will publish a security advisory and update this document.

## Security Best Practices for Adopters

When adopting this template in your own repository:
- Review all `*.instructions.md` files for alignment with your security standards
- Never enable the `pr-reviewer-trusted` agent on untrusted fork PRs
- Keep `validate-instructions.yml` pinned to specific action SHAs
- Run `scripts/validate_copilot_config.py` before merging instruction changes

