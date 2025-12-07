# Security Policy | భద్రతా విధానం

## English | ఇంగ్లీష్

### Overview

This document outlines the security measures implemented in lipi-lang to prevent malicious vulnerabilities before code gets merged. These protections are especially important as this is an interpreter that executes code.

### Security Testing Infrastructure

#### 1. Comprehensive Test Suite (`test_lipi.py`)

**53 automated tests covering:**
- ✅ Basic expression evaluation
- ✅ Telugu keyword functionality
- ✅ English keyword functionality
- ✅ Bilingual support
- ✅ **Security vulnerability tests**
- ✅ File execution safety
- ✅ Error handling
- ✅ Input validation
- ✅ v3.0 Module system (import/export)
- ✅ v3.0 OOP (classes, inheritance)

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
3. **No imports** - User code cannot import arbitrary Python modules
4. **Controlled file I/O (v2.0)** - File operations through whitelisted built-in functions only
5. **Controlled network access (v2.0)** - HTTP operations through secure built-in functions only
6. **Controlled database access (v2.0-v3.0)** - SQLite, MySQL, PostgreSQL through parameterized queries
7. **Path traversal prevention (v3.0)** - Module system blocks `../` patterns, uses safe path operations
8. **SQL injection prevention (v3.0)** - All database queries use parameterized statements
9. **No system commands** - Cannot execute shell commands (`subprocess`, `os.system`, `os.popen` blocked)

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
| Path Traversal | Controlled file I/O (v2.0), Module `../` blocking (v3.0) | ✅ Tested |
| Import Injection | No import statements allowed | ✅ Tested |
| SQL Injection | Parameterized queries for all databases (v2.0-v3.0) | ✅ Tested |
| HTTP Injection | URL validation, controlled urllib usage (v2.0) | ✅ Tested |
| Module Path Injection (v3.0) | Path traversal prevention in module system | ✅ Tested |
| DoS (CPU) | (TODO: Add timeout mechanism) | ⚠️ Partial |
| DoS (Memory) | (TODO: Add memory limits) | ⚠️ Partial |
| XSS | Not applicable (CLI tool) | N/A |

### Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT open a public issue**
2. Email the maintainer with details
3. Allow time for patch before disclosure
4. We will acknowledge within 48 hours

### Security Checklist for Contributors

Before submitting a pull request:

- [ ] All tests pass: `python3 tests/test_lipi.py`
- [ ] No new `eval()`, `exec()`, `__import__()` usage (outside controlled functions)
- [ ] File operations only through built-in `file_read()`, `file_write()`, `file_append()`
- [ ] Network operations only through built-in `http_get()`, `http_post()`
- [ ] Database operations only through built-in functions:
  - SQLite: `db_connect()`, `db_query()`, `db_close()`
  - MySQL: `mysql_connect()`, `mysql_query()`, `mysql_close()`
  - PostgreSQL: `postgres_connect()`, `postgres_query()`, `postgres_close()`
- [ ] Module operations use path traversal prevention (block `../`)
- [ ] No new subprocess/system calls
- [ ] Added tests for new functionality
- [ ] Updated security tests if needed
- [ ] Security workflow passes (GitHub Actions)

### Running Security Tests

```bash
# Run all tests
python3 tests/test_lipi.py

# Security checks are integrated into GitHub Actions workflow
# See .github/workflows/security-tests.yml for details

# Local verification
python3 tests/test_lipi.py  # All 53 tests must pass
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

- **v2.0** - Production-ready with enterprise features (2025-12-01)
  - File I/O operations (controlled, whitelisted)
  - HTTP/API support (secure urllib.request)
  - Database connectivity (SQLite file-based)
  - Updated security workflow for v2.0 features
  - All 39 tests passing
  - Zero vulnerabilities

- **v1.0** - Functions and data structures (2025-11-30)
  - Function definitions and calls
  - Arrays and dictionaries
  - Error handling (try/catch/finally)
  - Module system (exports/imports)

- **v0.5** - Initial security infrastructure (2025-11-30)
  - Comprehensive test suite
  - GitHub Actions CI/CD
  - Security testing framework

---

**Last Updated:** 2025-12-01
**Current Version:** v2.0
**Security Contact:** [Repository Maintainer]
