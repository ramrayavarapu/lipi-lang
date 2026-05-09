# Engineering Standards

This document defines how all software changes are made in this repository.
It is designed to be **AI-assisted, human-governed**.

Every rule exists to protect users, prevent regressions, and keep the system safe to deploy.

---

## Rule 1 — Design (ChatGPT — Automated)

Before any code is written, a design must exist.

**ChatGPT is responsible for producing the architecture and design.**

This step is **automated**: when a Feature Request issue is opened, the `design-agent` workflow calls GPT-4o and automatically creates a filled Design Proposal issue. The proposal is linked back to the feature request.

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
tests/
  unit/        ← logic and functions
  api/         ← endpoint and integration tests
  ux/          ← user flow and behaviour tests
```

Code without tests is not complete.

### Rule 2d — Infrastructure as Code

When infrastructure changes are needed, Claude generates:

- Terraform configuration files
- GitHub Actions workflow files
- Any other config-as-code (Docker, k8s manifests, etc.)

These follow the same PR process as application code — no manual changes to infrastructure.

---

## Rule 3 — Review (GitHub Copilot + Human)

Every PR is reviewed twice before merge:

1. **GitHub Copilot** runs an automated review checking for:
   - Security vulnerabilities
   - Regressions in existing behaviour
   - Code quality and coverage gaps

2. **A human** reads the review, inspects the diff, and approves the merge.

**A PR cannot be merged without both.**

---

## CI — What runs on every PR

| Workflow | What it does | Blocks merge on failure |
|----------|-------------|------------------------|
| `build-check` | Runs all tests — unit, API, and UX | Yes |
| `secret-scan` | Blocks commits containing credentials or API keys | Yes |
| `docs-check` | Ensures architecture docs are present and up to date | Yes |

All three must pass. Failure in any blocks the merge.

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

## Non-negotiables

- Never commit secrets or credentials
- Never push directly to main
- Never skip tests
- Never skip the design step
- Every change needs a human approval
