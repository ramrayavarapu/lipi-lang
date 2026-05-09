# Agentic Engineering Standards

This repository follows a structured AI-assisted engineering model.

---

## Rule 1: Design (ChatGPT)

All work MUST start with a design.

The design MUST include:

### Functional

- What is being built
- Why it is needed
- Expected user outcome

### Technical

- Impact on existing system
- Components affected
- Data flow

### Risk

- Functional risks
- Technical risks
- Failure scenarios

### Testing

- Unit test approach
- Integration test approach
- User experience validation

---

### 💰 Cost Impact (MANDATORY)

Every design MUST evaluate cost implications.

#### 1. Infrastructure Cost

- Will this increase compute usage (CPU, memory, runtime)?
- Will this increase storage (DB, files, logs)?
- Will this increase network calls (APIs, external services)?

#### 2. Third-Party Cost

- Does this use paid APIs (LLMs, SaaS, etc.)?
- Estimated cost per request / per user
- Rate limits or quota considerations

#### 3. Scaling Cost

- What happens at: 10 users / 1,000 users / 100,000 users

#### 4. Cost Optimisation Strategy

Design must include at least one of:

- Caching strategy
- Batching requests
- Reducing API calls
- Using cheaper alternatives where possible
- Lazy loading / on-demand execution

#### 5. Cost Risk

- What could unexpectedly increase cost?
- How will it be detected?

#### 6. Monitoring Plan

- What metrics will track cost?
- Where will this be monitored?

🚫 A design WITHOUT cost consideration is considered INCOMPLETE.

---

## Rule 2: Build (Claude)

### 2a: Code

- All code must be delivered via Pull Request
- No direct commits to main

### 2b: Safety

Claude must ensure:

- No security vulnerabilities introduced
- No regression introduced
- Existing functionality continues to work

### 2c: Testing

Claude must add:

- Unit tests (mandatory)
- Integration tests (where applicable)
- Behaviour validation

Code without tests is incomplete.

### 2d: Infrastructure

Claude may generate:

- GitHub workflows
- Config files

All must follow repo standards.

---

## Rule 3: Review (GitHub Copilot + Human)

- AI review is performed first (security, quality, regression, performance)
- Human reviewer makes final decision

---

## CI Requirements

All PRs must pass:

- build-check
- secret-scan
- docs-check
- ai-review

Failure in any = PR cannot be merged.

---

## Security Rules

- Never commit secrets
- Never hardcode credentials
- Use environment variables or secret managers
- Validate all inputs
- Fail safely

---

## Definition of Done

A change is complete only if:

- [ ] Design exists
- [ ] Cost impact evaluated
- [ ] Code implemented
- [ ] Tests added
- [ ] CI passes
- [ ] Reviewed
- [ ] Documented
- [ ] Safe to deploy
