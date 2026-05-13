import { useState } from "react";

// NOTE: The STANDARDS.md content below is an abbreviated example for the setup guide.
// Always refer to the actual STANDARDS.md file in the repository root for the
// authoritative and up-to-date engineering standards.

const DEFAULT_FILE = "STANDARDS.md";

const files = {
  "STANDARDS.md": `# Engineering Standards

This document defines how all software changes are made in this repository.
It is designed to be **AI-assisted, human-governed**.

Every rule exists to protect users, prevent regressions, and keep the system safe to deploy.

---

## Rule 1 — Design (ChatGPT — Automated)

Before any code is written, a design must exist.

**ChatGPT is responsible for producing the architecture and design.**

This step is **automated**: when a Feature Request issue is opened, the \`design-agent\` workflow calls GPT-4o and automatically creates a filled Design Proposal issue. The proposal is linked back to the feature request.

A human must **review and approve** the Design Proposal before Claude starts building. The \`needs-approval\` label signals it is pending review.

To trigger design generation manually on any issue, add the \`needs-design\` label.

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

\`\`\`
tests/             ← all test files in a flat layout
\`\`\`

Sub-directories (\`unit/\`, \`api/\`, \`ux/\`) may be introduced as the test suite grows, but are not required from the start. What matters is that all three test types are present.

Code without tests is not complete.

### Rule 2d — Infrastructure as Code

When infrastructure changes are needed, Claude generates:

- Terraform configuration files
- GitHub Actions workflow files
- Any other config-as-code (Docker, k8s manifests, etc.)

These follow the same PR process as application code — no manual changes to infrastructure.

---

## Rule 3 — Review (GitHub Copilot)

Every PR is automatically reviewed by **GitHub Copilot** (requested by \`request-copilot-review\` workflow on PR open).

Copilot checks for:
- Security vulnerabilities
- Regressions in existing behaviour
- Code quality and coverage gaps

If Copilot **requests changes**, Claude automatically picks up the comments (\`claude-autofix\` workflow), fixes the issues, and commits back to the PR branch.

This loop continues until Copilot approves or no further automated fixes are possible.

## Rule 4 — Final Review and Merge (Human)

After Copilot approves and all CI checks pass, **a human** reads the full diff, reviews the AI review output, and makes the final merge decision.

**A PR cannot be merged without human approval.**

---

## CI — What runs on every PR

| Workflow | What it does | Blocks merge on failure |
|----------|-------------|------------------------|
| \`build-check\` | Runs all tests — unit, API, and UX | Yes |
| \`secret-scan\` | Blocks commits containing credentials or API keys | Yes |
| \`docs-check\` | Ensures architecture docs are present and up to date | Yes |
| \`ai-review\` | Claude preliminary review — advisory only | No |
| \`request-copilot-review\` | Requests Copilot as reviewer automatically | No |

On Copilot \`changes_requested\`:

| Workflow | What it does |
|----------|-------------|
| \`claude-autofix\` | Reads Copilot comments, fixes issues, commits back to branch |

All blocking checks must pass before merge. Human approval is always required.

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
- [ ] \`docs/architecture/system.yaml\` updated if architecture changed
- [ ] \`README.md\` updated if behaviour changed

---

## Non-negotiables

- Never commit secrets or credentials
- Never push directly to main
- Never skip tests
- Never skip the design step
- Every change needs a human approval`,
};

const fileTree = [
  { path: "STANDARDS.md", type: "doc", icon: "📋" },
  { path: ".ai/claude-pr-generator.md", type: "ai", icon: "🤖" },
  { path: ".github/CODEOWNERS", type: "config", icon: "👤" },
  { path: ".github/pull_request_template.md", type: "template", icon: "📝" },
  { path: ".github/workflows/build-check.yml", type: "workflow", icon: "⚙️" },
  { path: ".github/workflows/secret-scan.yml", type: "workflow", icon: "🔐" },
  { path: ".github/workflows/docs-check.yml", type: "workflow", icon: "📄" },
  { path: ".github/workflows/ai-review.yml", type: "workflow", icon: "🧠" },
  { path: ".github/workflows/deploy-gate.yml", type: "workflow", icon: "🚀" },
  { path: "docs/architecture/system.yaml", type: "arch", icon: "🏗️" },
  { path: "tests/test_basic.py", type: "test", icon: "🧪" },
];

const typeColors = {
  doc:      { bg: "#1a2a1a", border: "#2d5a2d", badge: "#3d8b3d", label: "DOC" },
  ai:       { bg: "#1a1a2a", border: "#2d2d5a", badge: "#4a4aaa", label: "AI" },
  config:   { bg: "#2a1a1a", border: "#5a2d2d", badge: "#8b3d3d", label: "CONFIG" },
  template: { bg: "#2a2a1a", border: "#5a5a2d", badge: "#8b8b3d", label: "TEMPLATE" },
  workflow: { bg: "#1a2a2a", border: "#2d5a5a", badge: "#3d8b8b", label: "WORKFLOW" },
  arch:     { bg: "#2a1a2a", border: "#5a2d5a", badge: "#8b3d8b", label: "ARCH" },
  test:     { bg: "#2a2a1a", border: "#5a5a2d", badge: "#aaaa3d", label: "TEST" },
};

const steps = [
  { num: "01", title: "Create branch",      cmd: "git checkout -b agentic-baseline",                                                          desc: "Never commit to main directly" },
  { num: "02", title: "Create directories", cmd: "mkdir -p .ai .github/workflows docs/architecture tests",                                    desc: "Set up the folder structure" },
  { num: "03", title: "Add all files",      desc: "Copy each file from this guide into the correct path",                                     cmd: "# Copy files from each tab above" },
  { num: "04", title: "Add ANTHROPIC_API_KEY", desc: "GitHub repo → Settings → Secrets → Actions",                                           cmd: "# Repo Settings → Secrets → ANTHROPIC_API_KEY" },
  { num: "05", title: "Commit and push",    cmd: 'git add .\ngit commit -m "Enable Agentic Engineering baseline"\ngit push origin agentic-baseline', desc: "Push the branch" },
  { num: "06", title: "Create pull request", desc: "Open PR on GitHub — watch all 4 CI checks run",                                          cmd: "gh pr create --fill" },
  { num: "07", title: "Enable branch protection", desc: "Settings → Branches → Require: build-check, secret-scan, docs-check, ai-review + 1 reviewer", cmd: "# GitHub Settings → Branch Protection Rules" },
];

export default function AgenticBaseline() {
  const [activeFile, setActiveFile] = useState(DEFAULT_FILE);
  const [activeTab, setActiveTab] = useState("files");
  const [copied, setCopied] = useState(false);
  const [copyError, setCopyError] = useState(false);

  const currentFile = files[activeFile] || "(file content — see repo)";
  const currentMeta = fileTree.find(f => f.path === activeFile);
  const currentType = currentMeta?.type || "doc";
  const colors = typeColors[currentType];

  const copyContent = async () => {
    try {
      if (!navigator.clipboard) {
        // Fallback for browsers without clipboard API
        setCopyError(true);
        setTimeout(() => setCopyError(false), 3000);
        return;
      }
      await navigator.clipboard.writeText(currentFile);
      setCopied(true);
      setCopyError(false);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      // Show visual error feedback to user
      setCopyError(true);
      setTimeout(() => setCopyError(false), 3000);
    }
  };

  return (
    <div style={{
      fontFamily: "'JetBrains Mono', 'Fira Code', 'Courier New', monospace",
      background: "#0d0d0d",
      minHeight: "100vh",
      color: "#e0e0e0",
    }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #0d1117 0%, #161b22 100%)",
        borderBottom: "1px solid #21262d",
        padding: "20px 28px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: "12px",
      }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "4px" }}>
            <span style={{ fontSize: "18px" }}>⚡</span>
            <span style={{ fontSize: "13px", color: "#58a6ff", letterSpacing: "0.15em", fontWeight: 700 }}>
              AGENTIC ENGINEERING v1
            </span>
          </div>
          <div style={{ fontSize: "20px", fontWeight: 700, color: "#f0f6fc" }}>lipi-lang baseline</div>
          <div style={{ fontSize: "11px", color: "#8b949e", marginTop: "2px" }}>
            [YOUR_ORG]/[YOUR_REPO] · Review branch protection rules before enabling org-wide
          </div>
        </div>
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
          {["build-check", "secret-scan", "docs-check", "ai-review"].map(w => (
            <span key={w} style={{
              fontSize: "10px", padding: "3px 8px",
              background: "#1c2d1c", border: "1px solid #2d5a2d",
              borderRadius: "4px", color: "#56d364", letterSpacing: "0.05em",
            }}>✓ {w}</span>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", borderBottom: "1px solid #21262d", background: "#161b22", padding: "0 28px" }}>
        {[
          { id: "files",    label: "📁 Files",        count: fileTree.length },
          { id: "steps",    label: "🔢 Setup Steps",  count: steps.length },
          { id: "settings", label: "⚙️ GitHub Settings" },
        ].map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{
            background: "none", border: "none", cursor: "pointer",
            padding: "12px 16px", fontSize: "12px", letterSpacing: "0.05em",
            color: activeTab === tab.id ? "#f0f6fc" : "#8b949e",
            borderBottom: activeTab === tab.id ? "2px solid #58a6ff" : "2px solid transparent",
            display: "flex", alignItems: "center", gap: "6px",
          }}>
            {tab.label}
            {tab.count && (
              <span style={{
                background: "#21262d", borderRadius: "10px",
                padding: "1px 6px", fontSize: "10px", color: "#8b949e",
              }}>{tab.count}</span>
            )}
          </button>
        ))}
      </div>

      {/* Files tab */}
      {activeTab === "files" && (
        <div style={{ display: "flex", height: "calc(100vh - 160px)", minHeight: "500px" }}>
          <div style={{
            width: "240px", minWidth: "200px",
            background: "#161b22", borderRight: "1px solid #21262d",
            overflowY: "auto", padding: "12px 0",
          }}>
            {fileTree.map(file => {
              const c = typeColors[file.type];
              const isActive = activeFile === file.path;
              return (
                <button key={file.path} onClick={() => setActiveFile(file.path)} style={{
                  width: "100%", textAlign: "left", background: isActive ? c.bg : "none",
                  border: "none", borderLeft: isActive ? `2px solid ${c.border}` : "2px solid transparent",
                  cursor: "pointer", padding: "8px 16px", transition: "all 0.15s",
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                    <span style={{ fontSize: "12px" }}>{file.icon}</span>
                    <span style={{ fontSize: "10px", color: isActive ? "#f0f6fc" : "#8b949e", wordBreak: "break-all", lineHeight: 1.4 }}>
                      {file.path.split("/").pop()}
                    </span>
                  </div>
                  {file.path.includes("/") && (
                    <div style={{ fontSize: "9px", color: "#484f58", marginTop: "2px", paddingLeft: "18px" }}>
                      {file.path.split("/").slice(0, -1).join("/")}
                    </div>
                  )}
                </button>
              );
            })}
          </div>

          <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
            <div style={{
              padding: "10px 20px", background: colors.bg,
              borderBottom: `1px solid ${colors.border}`,
              display: "flex", justifyContent: "space-between", alignItems: "center",
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <span style={{
                  fontSize: "9px", background: colors.badge,
                  color: "#fff", padding: "2px 6px", borderRadius: "3px", letterSpacing: "0.1em",
                }}>{colors.label}</span>
                <span style={{ fontSize: "11px", color: "#8b949e" }}>{activeFile}</span>
              </div>
              <button onClick={copyContent} style={{
                background: copyError ? "#2d1c1c" : (copied ? "#1c2d1c" : "#21262d"),
                border: `1px solid ${copyError ? "#5a2d2d" : (copied ? "#2d5a2d" : "#30363d")}`,
                borderRadius: "4px", padding: "4px 12px",
                fontSize: "10px", color: copyError ? "#f85149" : (copied ? "#56d364" : "#8b949e"),
                cursor: "pointer", letterSpacing: "0.05em",
              }}>
                {copyError ? "✗ COPY FAILED" : (copied ? "✓ COPIED" : "COPY")}
              </button>
            </div>
            <pre style={{
              flex: 1, margin: 0, padding: "20px",
              overflowY: "auto", overflowX: "auto",
              fontSize: "11px", lineHeight: "1.7",
              color: "#c9d1d9", background: "#0d1117",
              whiteSpace: "pre",
            }}>
              {currentFile}
            </pre>
          </div>
        </div>
      )}

      {/* Steps tab */}
      {activeTab === "steps" && (
        <div style={{ padding: "28px", maxWidth: "700px" }}>
          <div style={{ marginBottom: "20px" }}>
            <div style={{ fontSize: "13px", color: "#58a6ff", letterSpacing: "0.1em", marginBottom: "6px" }}>SETUP SEQUENCE</div>
            <div style={{ fontSize: "11px", color: "#8b949e" }}>
              Follow these steps in order. All steps must complete before raising the PR.
            </div>
          </div>
          {steps.map((step, i) => (
            <div key={i} style={{
              marginBottom: "16px", background: "#161b22",
              border: "1px solid #21262d", borderRadius: "6px", overflow: "hidden",
            }}>
              <div style={{
                display: "flex", alignItems: "center", gap: "12px",
                padding: "12px 16px", borderBottom: "1px solid #21262d", background: "#0d1117",
              }}>
                <span style={{ fontSize: "11px", color: "#58a6ff", fontWeight: 700, letterSpacing: "0.1em" }}>STEP {step.num}</span>
                <span style={{ fontSize: "13px", color: "#f0f6fc", fontWeight: 600 }}>{step.title}</span>
              </div>
              <div style={{ padding: "12px 16px" }}>
                <div style={{ fontSize: "11px", color: "#8b949e", marginBottom: "10px" }}>{step.desc}</div>
                <pre style={{
                  background: "#0d1117", border: "1px solid #21262d",
                  borderRadius: "4px", padding: "10px 14px",
                  fontSize: "11px", color: "#56d364", margin: 0,
                  overflowX: "auto", whiteSpace: "pre",
                }}>{step.cmd}</pre>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Settings tab */}
      {activeTab === "settings" && (
        <div style={{ padding: "28px", maxWidth: "700px" }}>
          <div style={{ marginBottom: "20px" }}>
            <div style={{ fontSize: "13px", color: "#58a6ff", letterSpacing: "0.1em", marginBottom: "6px" }}>GITHUB REPO SETTINGS</div>
            <div style={{ fontSize: "11px", color: "#8b949e" }}>
              These must be configured manually in GitHub after the PR is merged.
            </div>
          </div>
          {[
            {
              section: "Secrets → Actions",
              path: "Settings → Secrets and variables → Actions",
              items: [
                { key: "ANTHROPIC_API_KEY", desc: "Your Anthropic API key — required for ai-review workflow", critical: true },
              ],
            },
            {
              section: "Branch Protection — main",
              path: "Settings → Branches → Add rule → Branch name: main",
              items: [
                { key: "Require a pull request before merging", desc: "No direct commits to main", critical: true },
                { key: "Required status checks", desc: "build-check, secret-scan, docs-check, ai-review — all must pass", critical: true },
                { key: "Require at least 1 approving review", desc: "Human-in-the-loop — you must approve every PR", critical: true },
                { key: "Do not allow bypassing the above settings", desc: "Applies to admins too — no exceptions", critical: true },
                { key: "Block force pushes", desc: "Prevents history rewriting", critical: false },
              ],
            },
            {
              section: "Validation Test",
              path: "After setup — test the guardrails",
              items: [
                { key: "Create a PR with no tests folder", desc: "Should fail: build-check ❌", critical: false },
                { key: "Add a fake AWS key in a test file", desc: "Should fail: secret-scan ❌", critical: false },
                { key: "Delete system.yaml temporarily", desc: "Should fail: docs-check ❌", critical: false },
                { key: "Submit a proper PR with all files", desc: "Should pass: all checks ✅", critical: false },
              ],
            },
          ].map((section, i) => (
            <div key={i} style={{
              marginBottom: "20px", background: "#161b22",
              border: "1px solid #21262d", borderRadius: "6px", overflow: "hidden",
            }}>
              <div style={{ padding: "12px 16px", background: "#0d1117", borderBottom: "1px solid #21262d" }}>
                <div style={{ fontSize: "12px", color: "#f0f6fc", fontWeight: 600 }}>{section.section}</div>
                <div style={{ fontSize: "10px", color: "#8b949e", marginTop: "2px" }}>📍 {section.path}</div>
              </div>
              <div style={{ padding: "8px 0" }}>
                {section.items.map((item, j) => (
                  <div key={j} style={{
                    padding: "10px 16px",
                    borderBottom: j < section.items.length - 1 ? "1px solid #21262d" : "none",
                    display: "flex", alignItems: "flex-start", gap: "10px",
                  }}>
                    <span style={{ fontSize: "12px", marginTop: "1px" }}>{item.critical ? "🔴" : "🟡"}</span>
                    <div>
                      <div style={{ fontSize: "11px", color: "#c9d1d9", fontWeight: 600 }}>{item.key}</div>
                      <div style={{ fontSize: "10px", color: "#8b949e", marginTop: "2px" }}>{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
