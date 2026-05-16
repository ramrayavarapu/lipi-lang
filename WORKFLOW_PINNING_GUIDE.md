# GitHub Actions Security Pinning Guide
## Implementation Instructions for Design Issue #77

### Overview
This guide provides specific commit SHAs and step-by-step instructions to implement version pinning for GitHub Actions workflows as specified in Design Issue #77.

### Critical Security Actions Required

#### 1. Pin actions/checkout to Commit SHA
**Current**: `actions/checkout@v4`  
**Target**: `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11`

**Files to Update:**
- `.github/workflows/build-check.yml` (line 13)
- `.github/workflows/security-tests.yml` (lines 20, 63, 121, 151) 
- `.github/workflows/claude-build-agent.yml` (line 35)
- `.github/workflows/docs-check.yml` (line 13)
- `.github/workflows/secret-scan.yml` (line 13)
- `.github/workflows/claude-autofix.yml` (line 23)
- `.github/workflows/ai-review.yml` (line 30)
- `.github/workflows/design-agent.yml` (line 37)

#### 2. Pin actions/setup-python to Commit SHA
**Current v4**: `actions/setup-python@v4`  
**Target**: `actions/setup-python@65d7f2d534ac1bc67fcd52423e459d7f65fa7115`

**Current v5**: `actions/setup-python@v5`  
**Target**: `actions/setup-python@82c7e631bb3cdc910f68e0081d67478d79c6982d`

**Files to Update:**
- `.github/workflows/security-tests.yml` (lines 23, 154) → Use v4 SHA
- `.github/workflows/build-check.yml` (line 16) → Use v5 SHA

#### 3. Pin actions/github-script to Commit SHA  
**Current**: `actions/github-script@v7`  
**Target**: `actions/github-script@60a2d8b64675a63f597c7bed8c04b5f5b8c2e2cd`

**Files to Update:**
- `.github/workflows/request-copilot-review.yml` (line 18)
- `.github/workflows/claude-autofix.yml` (line 201)
- `.github/workflows/ai-review.yml` (line 155)
- `.github/workflows/design-agent.yml` (line 118)

#### 4. Pin trufflesecurity/trufflehog to Commit SHA
**Current**: `trufflesecurity/trufflehog@main` ⚠️ **CRITICAL SECURITY RISK**  
**Target**: `trufflesecurity/trufflehog@3e86065cf0b030a97c47d4b40b87a5ea76ba8b74`

**Files to Update:**
- `.github/workflows/security-tests.yml` (line 66)

### Implementation Steps

1. **Create feature branch**:
   ```bash
   git checkout -b security/pin-github-actions-shas
   ```

2. **Update each workflow file** with the commit SHAs listed above

3. **Verify changes** by running:
   ```bash
   python3 -m unittest tests.test_github_actions_security -v
   ```

4. **Test workflow integrity**:
   ```bash
   # Test that workflows are still syntactically valid
   python3 -c "import yaml; [yaml.safe_load(open(f)) for f in ['workflow_file1.yml', 'workflow_file2.yml']]"
   ```

5. **Commit and create PR**:
   ```bash
   git add .github/workflows/
   git commit -m "security: pin GitHub Actions to commit SHAs

   - Pin actions/checkout@v4 to commit SHA b4ffde6
   - Pin actions/setup-python@v4/v5 to commit SHAs  
   - Pin actions/github-script@v7 to commit SHA 60a2d8b
   - Pin trufflesecurity/trufflehog@main to commit SHA 3e86065
   
   This addresses security vulnerabilities identified in Design Issue #77
   by preventing execution of potentially malicious code through unpinned
   action versions.
   
   Resolves: #77"
   git push origin security/pin-github-actions-shas
   ```

### Testing Requirements

The following test files have been created to validate the security improvements:

1. **Unit Tests**: `tests/test_github_actions_security.py`
   - Validates commit SHA formats
   - Detects unpinned actions
   - Verifies security principles

2. **API Tests**: `tests/test_github_actions_security_api.py`  
   - Tests GitHub API integration
   - Validates workflow structure
   - Tests version comparison logic

3. **UX Tests**: `tests/test_github_actions_security_ux.py`
   - Tests developer experience
   - Validates security audit accessibility
   - Tests user feedback mechanisms

### Security Benefits

After implementation:
- ✅ Eliminates risk from `trufflehog@main` branch reference
- ✅ Prevents execution of malicious code through compromised action versions
- ✅ Provides audit trail of exact action versions used
- ✅ Enables security scanning of specific action commits
- ✅ Complies with security best practices for CI/CD pipelines

### Verification Commands

After implementation, verify security improvements:

```bash
# Run security validation tests
python3 -m unittest tests.test_github_actions_security* -v

# Check for any remaining unpinned actions  
grep -r "actions/.*@v[0-9]" .github/workflows/ || echo "✅ No version tags found"
grep -r "@main\|@master" .github/workflows/ || echo "✅ No branch references found"

# Verify commit SHA format (should find pinned actions)
grep -r "@[a-f0-9]\{40\}" .github/workflows/ && echo "✅ Found pinned actions"
```

### Maintenance Notes

- **SHA Updates**: Monitor action repositories for security updates and update SHAs as needed
- **Automation**: Consider implementing automated SHA update checking in CI/CD
- **Documentation**: Keep this guide updated when adding new workflows
- **Security Scanning**: Regularly scan action commits for vulnerabilities

**Status**: Implementation guide complete. Ready for manual workflow updates.