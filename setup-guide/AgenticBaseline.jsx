import { useState } from "react";

const files = {
  "STANDARDS.md": `# Agentic Engineering Standards

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
- [ ] Safe to deploy`,
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
  const [activeFile, setActiveFile] = useState("STANDARDS.md");
  const [activeTab, setActiveTab] = useState("files");
  const [copied, setCopied] = useState(false);

  const currentFile = files[activeFile] || "(file content — see repo)";
  const currentMeta = fileTree.find(f => f.path === activeFile);
  const currentType = currentMeta?.type || "doc";
  const colors = typeColors[currentType];

  const copyContent = () => {
    navigator.clipboard.writeText(currentFile);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
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
            ramrayavarapu/lipi-lang · Test before org-wide rollout
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
                background: copied ? "#1c2d1c" : "#21262d",
                border: `1px solid ${copied ? "#2d5a2d" : "#30363d"}`,
                borderRadius: "4px", padding: "4px 12px",
                fontSize: "10px", color: copied ? "#56d364" : "#8b949e",
                cursor: "pointer", letterSpacing: "0.05em",
              }}>
                {copied ? "✓ COPIED" : "COPY"}
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
