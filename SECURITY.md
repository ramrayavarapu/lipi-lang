# Security Policy | భద్రతా విధానం

## English | ఇంగ్లీష్

### Overview

This document outlines the security measures implemented in lipi-lang to prevent malicious vulnerabilities before code gets merged. These protections are especially important as this is an interpreter that executes code.

### Security Testing Infrastructure

#### 1. Comprehensive Test Suite (`test_lipi.py`)

**39 automated tests covering:**
- ✅ Basic expression evaluation
- ✅ Telugu keyword functionality
- ✅ English keyword functionality
- ✅ Bilingual support
- ✅ **Security vulnerability tests**
- ✅ File execution safety
- ✅ Error handling
- ✅ Input validation

**Security-Specific Tests:**
- Code injection prevention
- Command injection prevention
- File access injection prevention
- eval() injection prevention
- Import statement blocking
- Dunder method access blocking
- DoS protection (large numbers)
- Unicode injection safety

#### 2. Automated Security Scanner (`security_check.py`)

Scans all code for:
- ❌ Dangerous Python functions (exec, compile, etc.)
- ❌ Code injection vulnerabilities
- ❌ Command execution (os.system, subprocess)
- ❌ Unsafe file operations
- ❌ Network operations (socket, urllib, etc.)

**Exit code 1 if critical issues found** - prevents commits with vulnerabilities.

#### 3. GitHub Actions CI/CD (`.github/workflows/security-tests.yml`)

**Runs on every push and pull request:**

- 🔬 Full test suite on Python 3.8-3.12
- 🔍 Security scanner
- 🛡️ Bandit static security analysis
- 📊 Pylint code quality checks
- 🔐 TruffleHog secrets scanning
- 🚫 Suspicious pattern detection
- 📦 Dependency verification
- 💉 Code injection tests

**All tests must pass before merge.**

#### 4. Pre-commit Hooks (`.pre-commit-config.yaml`)

**Runs locally before each commit:**
- ✅ YAML/JSON validation
- ✅ Large file prevention
- ✅ Private key detection
- ✅ Security test suite
- ✅ Security scanner

Install with:
```bash
pip install pre-commit
pre-commit install
```

### Security Design Principles

#### Sandboxed Execution

The Lipi interpreter is designed with security in mind:

1. **No eval() on untrusted input** - Only our controlled `eval_lipi_expr()` function
2. **No exec()** - Never executes arbitrary Python code
3. **No imports** - User code cannot import Python modules
4. **No file I/O** - Cannot read/write files from Lipi code
5. **No network access** - Cannot make network requests
6. **No system commands** - Cannot execute shell commands

#### Safe Expression Evaluation

`eval_lipi_expr()` function only allows:
- String literals: `"text"`
- Integer literals: `123`
- Variables from controlled environment
- Basic operators: `+`, comparison operators
- **Nothing else**

### Vulnerability Prevention

| Vulnerability Type | Prevention Method | Test Coverage |
|-------------------|-------------------|---------------|
| Code Injection | Limited expression syntax, no eval/exec | ✅ Tested |
| Command Injection | No os.system/subprocess usage | ✅ Tested |
| Path Traversal | No file system access | ✅ Tested |
| Import Injection | No import statements allowed | ✅ Tested |
| DoS (CPU) | (TODO: Add timeout mechanism) | ⚠️ Partial |
| DoS (Memory) | (TODO: Add memory limits) | ⚠️ Partial |
| XSS | Not applicable (CLI tool) | N/A |
| SQL Injection | No database access | N/A |

### Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT open a public issue**
2. Email the maintainer with details
3. Allow time for patch before disclosure
4. We will acknowledge within 48 hours

### Security Checklist for Contributors

Before submitting a pull request:

- [ ] All tests pass: `python3 test_lipi.py`
- [ ] Security scan passes: `python3 security_check.py`
- [ ] No new `eval()`, `exec()`, `__import__()` usage
- [ ] No new file system operations
- [ ] No new network operations
- [ ] No new subprocess/system calls
- [ ] Added tests for new functionality
- [ ] Updated security tests if needed

### Running Security Tests

```bash
# Run all tests
python3 test_lipi.py

# Run security scanner
python3 security_check.py

# Run both (what CI does)
python3 test_lipi.py && python3 security_check.py
```

### Continuous Monitoring

- GitHub Actions runs on every push
- Dependabot monitors dependencies (when added)
- CodeQL analysis (can be enabled)
- Regular security audits

### Future Security Enhancements

Planned security improvements:

- [ ] Execution timeout mechanism (prevent infinite loops)
- [ ] Memory usage limits
- [ ] Recursion depth limits
- [ ] Rate limiting for REPL
- [ ] Sandboxed execution environment
- [ ] Security audit logging
- [ ] Fuzz testing integration

---

## తెలుగు | Telugu

### సారాంశం (Overview)

ఈ డాక్యుమెంట్ lipi-lang లో కోడ్ మెర్జ్ అయ్యే ముందు హానికరమైన లోపాలను నిరోధించడానికి అమలు చేసిన భద్రతా చర్యలను వివరిస్తుంది.

### భద్రతా పరీక్ష మౌలిక సదుపాయాలు

#### 1. సమగ్ర పరీక్ష సూట్ (`test_lipi.py`)

**39 ఆటోమేటెడ్ టెస్ట్‌లు:**
- ప్రాథమిక ఎక్స్‌ప్రెషన్ మూల్యాంకనం
- తెలుగు కీవర్డ్ ఫంక్షనాలిటీ
- ఇంగ్లీష్ కీవర్డ్ ఫంక్షనాలిటీ
- ద్విభాషా మద్దతు
- **భద్రతా దుర్బలత్వ పరీక్షలు**
- ఫైల్ ఎగ్జిక్యూషన్ భద్రత
- ఎర్రర్ హ్యాండ్లింగ్
- ఇన్‌పుట్ వాలిడేషన్

#### 2. ఆటోమేటెడ్ సెక్యూరిటీ స్కానర్ (`security_check.py`)

అన్ని కోడ్‌ను స్కాన్ చేస్తుంది:
- ప్రమాదకరమైన Python ఫంక్షన్లు
- కోడ్ ఇంజెక్షన్ దుర్బలత్వాలు
- కమాండ్ ఎగ్జిక్యూషన్
- అసురక్షిత ఫైల్ ఆపరేషన్లు
- నెట్‌వర్క్ ఆపరేషన్లు

#### 3. GitHub Actions CI/CD

**ప్రతి పుష్ మరియు పుల్ రిక్వెస్ట్‌లో రన్ అవుతుంది:**
- పూర్తి పరీక్ష సూట్
- భద్రతా స్కానర్
- Bandit స్టాటిక్ సెక్యూరిటీ అనాలిసిస్
- కోడ్ క్వాలిటీ చెక్స్
- సీక్రెట్స్ స్కానింగ్

### భద్రతా సమస్యలను నివేదించడం

భద్రతా దుర్బలత్వాన్ని కనుగొంటే:
1. పబ్లిక్ ఇష్యూ ఓపెన్ చేయవద్దు
2. మెయింటైనర్‌కు ఇమెయిల్ చేయండి
3. పాచ్ కోసం సమయం ఇవ్వండి

### భద్రతా చెక్‌లిస్ట్

పుల్ రిక్వెస్ట్ సబ్మిట్ చేయడానికి ముందు:
- [ ] అన్ని టెస్ట్‌లు పాస్ అవుతున్నాయా
- [ ] సెక్యూరిటీ స్కాన్ పాస్ అవుతుందా
- [ ] కొత్త ప్రమాదకర ఫంక్షన్లు లేవా
- [ ] కొత్త ఫైల్ ఆపరేషన్లు లేవా

---

## Version History

- **v0.5** - Initial security infrastructure
  - Comprehensive test suite
  - Security scanner
  - GitHub Actions CI/CD
  - Pre-commit hooks

---

**Last Updated:** 2025-11-30
**Security Contact:** [Repository Maintainer]
