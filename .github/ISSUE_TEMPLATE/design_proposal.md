---
name: Design Proposal (Rule 1)
about: Architecture or design from ChatGPT — required before any code is written
title: '[DESIGN] '
labels: design, needs-approval
assignees: ramrayavarapu
---

## What are we building?

<!-- Plain English description of the change -->

## Why is it needed?

<!-- What user problem does this solve? What breaks without it? -->

## How does it fit into the existing system?

<!-- Which components are affected? Describe the data flow. -->

**Components affected:**
- 

**Data flow:**
```
[input] → [processing] → [output]
```

**API contracts changed:**
- [ ] Yes — describe below
- [ ] No

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Regression in existing behaviour | | |
| Security exposure | | |
| Performance degradation | | |

## Cost Impact

- **Infrastructure change:** (compute / storage / network)
- **Third-party API usage:** (name, estimated cost per call, volume)
- **Scaling impact:** 10 users / 1,000 users / 100,000 users
- **Optimisation strategy:** (caching / batching / lazy loading / etc.)

## Test Approach

- **Unit tests:** what functions need testing
- **API tests:** which endpoints need validation
- **UX tests:** which user flows need end-to-end coverage

## Definition of Done

- [ ] Design reviewed and approved by human
- [ ] Cost impact accepted
- [ ] Claude assigned to build (Rule 2)
- [ ] Tests approach agreed
