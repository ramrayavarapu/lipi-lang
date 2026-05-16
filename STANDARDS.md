# Engineering Standards

This document defines how all software changes are made in this repository.
It is designed to be **AI-assisted, human-governed**.

Every rule exists to protect users, prevent regressions, and keep the system safe to deploy.

---

## Rule 1 — Design (ChatGPT — Automated)

Before any code is written, a design must exist.

**ChatGPT is responsible for producing the architecture and design.**

This step is **automated**: when a Feature Request issue is opened, the `design-agent` workflow calls GPT-4o and automatically creates a filled Design Proposal issue linked back to the feature request. When a pull request is opened, the same workflow also posts an auto-generated Design Proposal comment on the PR for review.

A human must **review and approve** the Design Proposal before Claude starts building. The `needs-approval` label signals it is pending review.

To trigger design generation manually on any issue, add the `needs-design` label.

No code is written without an approved design.

---

## Rule 2 — Build (Claude)

### Rule 2a — Code via Pull Request

Claude writes all code and submits it via Pull Request.
**Nothing is committed directly to main — ever.**

Every PR references the design issue it implements.

### Rule 2b — Safety First

Before submitting a PR, Claude must verify:

- No security vulnerabilities have been introduced
- Existing functionality still works (no regression)
- All inputs are validated at system boundaries
- No secrets, credentials, or API keys are present in code

### Rule 2c — Automated Tests

Every PR must include tests that prove the change works end-to-end:

| Test type | What it covers |
|-----------|---------------|
| **Unit tests** | Individual functions and business logic |
| **Backend API tests** | Endpoints respond correctly, error cases handled |
| **User experience tests** | Key user flows behave as expected |

Tests live in:

```
tests/             ← all test files in a flat layout
```

Sub-directories (`unit/`, `api/`, `ux/`) may be introduced as the test suite grows, but are not required from the start. What matters is that all three test types are present.

Code without tests is not complete.

### Rule 2d — Infrastructure as Code

When infrastructure changes are needed, Claude generates:

- Terraform configuration files
- GitHub Actions workflow files
- Any other config-as-code (Docker, k8s manifests, etc.)

These follow the same PR process as application code — no manual changes to infrastructure.

---

## Rule 3 — Review (GitHub Copilot)

Every PR is automatically reviewed by **GitHub Copilot** (requested by `request-copilot-review` workflow on PR open).

Copilot checks for:
- Security vulnerabilities
- Regressions in existing behaviour
- Code quality and coverage gaps

If Copilot **requests changes**, Claude automatically picks up the comments (`claude-autofix` workflow), fixes the issues, and commits back to the PR branch.

This loop continues until Copilot approves or no further automated fixes are possible.

## Rule 4 — Final Review and Merge (Human)

After Copilot approves and all CI checks pass, **a human** reads the full diff, reviews the AI review output, and makes the final merge decision.

**A PR cannot be merged without human approval.**

---

## CI — What runs on every PR

| Workflow | What it does | Blocks merge on failure |
|----------|-------------|------------------------|
| `build-check` | Runs all tests — unit, API, and UX | Yes |
| `secret-scan` | Blocks commits containing credentials or API keys | Yes |
| `docs-check` | Ensures architecture docs are present and up to date | Yes |
| `ai-review` | Claude preliminary review — posts result as PR comment | Yes (must complete) |
| `request-copilot-review` | Requests Copilot as reviewer automatically | No |

On Copilot `changes_requested`:

| Workflow | What it does |
|----------|-------------|
| `claude-autofix` | Reads Copilot comments, fixes issues, commits back to branch |

All blocking checks must pass before merge. Human approval is always required.

### Branch protection setup (required once per repo)

`ai-review` posts its output as a PR comment and must complete before a human
can merge. To enforce this in GitHub:

1. Go to **Settings → Branches → Add branch protection rule** for `main`
2. Enable **Require status checks to pass before merging**
3. Add these required checks: `build-check`, `secret-scan`, `docs-check`, `ai-review`
4. Enable **Require a pull request before merging** → set **Required approvals** to `1`

This guarantees the order: CI runs → AI review posts its comment → human reads
the comment → human approves → merge is unblocked.

---

## Definition of Done

A change is complete only when all of the following are true:

- [ ] Design issue exists and is linked in the PR
- [ ] Cost impact assessed in the design
- [ ] Code implemented by Claude via PR
- [ ] Unit, API, and UX tests added
- [ ] All CI checks pass
- [ ] Copilot review completed
- [ ] Human reviewer approved
- [ ] `docs/architecture/system.yaml` updated if architecture changed
- [ ] `README.md` updated if behaviour changed

---

## AI Agent Cost Monitoring

This repository uses three AI APIs. All costs must be assessed before work begins and reviewed quarterly.

| Agent | API | Trigger | Cost control |
|-------|-----|---------|-------------|
| ChatGPT Design Agent | OpenAI GPT-4o | Feature Request opened | Authorised users only (OWNER / MEMBER / COLLABORATOR). Set a monthly budget alert in the OpenAI dashboard. |
| Claude Build + Review | Anthropic Claude | PR opened / Copilot review submitted | Key scoped to this repo. Monitor usage in the Anthropic console. |
| GitHub Copilot | GitHub Copilot API | PR opened | Covered by the GitHub subscription. |

**Budget alerts**: Set spend alerts in both the OpenAI and Anthropic dashboards.
If a month's AI spend exceeds the expected budget, pause automated agents by removing the relevant secret until the cause is identified.

---

## API Key Security and Rotation

All secrets are stored in GitHub Actions secrets (`Settings → Secrets → Actions`). Follow these rules:

1. **Never hardcode** API keys in code, workflow files, or documentation.
2. **Least privilege**: each key must have the minimum required permissions.
   - `OPENAI_API_KEY` — GPT-4o chat completions only
   - `ANTHROPIC_API_KEY` — Claude messages API only
   - `CLAUDE_AUTOFIX_PAT` — fine-grained PAT with `Contents: write` and `Workflows: write` on this repo only
3. **Rotation schedule**: rotate all keys every 90 days. Add a calendar reminder.
4. **Compromise procedure**: if a key is suspected leaked, revoke it immediately in the provider's dashboard, then add a new secret in GitHub before re-enabling the workflow.
5. **Access audit**: review who has access to repo secrets quarterly (`Settings → Collaborators & teams`).

---

## Non-negotiables

- Never commit secrets or credentials
- Never push directly to main
- Never skip tests
- Never skip the design step
- Every change needs a human approval
