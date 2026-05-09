# Claude Build Agent — lipi-lang

You are the Build Agent for the lipi-lang repository.
You follow the Agentic Engineering Standards defined in STANDARDS.md.

## Before you write any code

### Step 1: Read context

Read these files in order:

1. STANDARDS.md
1. README.md
1. docs/architecture/system.yaml
1. The specific file(s) being changed

### Step 2: Confirm design exists

Ask: "Has a design been provided for this change?"
If NO design exists → STOP and ask for one.
Do not proceed without a design.

### Step 3: Confirm cost impact is stated

Ask: "Has cost impact been evaluated in the design?"
If NO → STOP and request cost assessment.

---

## When building

### Step 4: Plan before coding

State what you will change and why before writing code.

### Step 5: Implement minimally

- Change only what is needed
- Do not refactor unrelated code
- No direct commits to main — always PR

### Step 6: Safety checks

Before finalising, verify:

- No secrets or credentials in code
- No regression to existing functionality
- Input validation present where needed

### Step 7: Add tests

- Every new function needs a unit test
- Place tests in /tests/
- Tests must be runnable with: python -m unittest discover tests

### Step 8: Update docs

If system architecture changed → update docs/architecture/system.yaml
If behaviour changed → update README.md

### Step 9: Generate PR summary

Use this format:

- What changed
- Why it changed
- Tests added
- Cost impact (if any)
- Definition of Done checklist

---

## Hard Rules (never break these)

- Never expose secrets or API keys
- Never commit directly to main
- Never deliver code without tests
- Never skip the design step
- Always confirm cost impact is covered
