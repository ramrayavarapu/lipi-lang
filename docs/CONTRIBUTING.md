# Contributing to lipi-lang | lipi-lang కు సహకారం

## English

### Welcome!

Thank you for your interest in contributing to lipi-lang! This project aims to make programming accessible to Telugu-speaking students.

### Before You Start

1. **Read the README** - Understand the project goals
2. **Check existing issues** - See if your idea is already being discussed
3. **Review SECURITY.md** - Understand security requirements

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ramrayavarapu/lipi-lang.git
cd lipi-lang

# Install pre-commit hooks (recommended)
pip install pre-commit
pre-commit install

# Run tests to verify setup
python3 test_lipi.py
```

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation

3. **Run tests**
   ```bash
   # Run all tests
   python3 test_lipi.py

   # Run security scanner
   python3 security_check.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

### Security Requirements ⚠️

**CRITICAL:** All code must pass security checks before merge.

Your changes MUST:
- ✅ Pass all 39 automated tests
- ✅ Pass security scanner
- ✅ Not introduce dangerous functions (eval, exec, __import__)
- ✅ Not add file system operations
- ✅ Not add network operations
- ✅ Not add command execution

**Automated checks will:**
- Run on every push
- Block merge if tests fail
- Scan for security vulnerabilities
- Check for malicious patterns

### Adding New Features

When adding features:

1. **Add tests first** (Test-Driven Development)
   ```python
   def test_new_feature(self):
       # Your test code
       pass
   ```

2. **Implement the feature**
3. **Add security tests if applicable**
4. **Update documentation**
5. **Verify all tests pass**

### Code Style

- Use clear variable names
- Add comments for complex logic
- Support both Telugu and English where applicable
- Follow existing patterns in codebase

### Testing Guidelines

```python
# Good test (basic feature)
def test_telugu_print_statement(self):
    """Test Telugu print with string literal"""
    env = {}
    with captured_output() as output:
        lipi.run_lipi_line('చెప్పు "నమస్తే"', env)
    self.assertEqual(output.getvalue().strip(), "నమస్తే")

# v2.0 feature test example
def test_file_operations(self):
    """Test v2.0 file I/O operations"""
    env = {}
    # Write file
    lipi.run_lipi_line('file_write("/tmp/test.txt", "content")', env)
    # Read file
    content = lipi.eval_lipi_expr('file_read("/tmp/test.txt")', env)
    self.assertEqual(content, "content")

# Include security test if needed
def test_no_injection_in_feature(self):
    """Ensure new feature prevents injection"""
    # Test code here
```

### Documentation

Update relevant documentation:
- `README.md` - User-facing changes
- `SECURITY.md` - Security-related changes
- Code comments - Complex logic
- Docstrings - Function/class documentation

### Pull Request Process

1. **Ensure all tests pass**
   ```bash
   python3 test_lipi.py && python3 security_check.py
   ```

2. **Create Pull Request**
   - Clear description of changes
   - Link to related issues
   - List of tests added

3. **Wait for CI checks**
   - GitHub Actions will run automatically
   - Fix any failures

4. **Code Review**
   - Address reviewer feedback
   - Make requested changes
   - Re-run tests

5. **Merge**
   - Maintainer will merge after approval
   - Your contribution is live!

### What We're Looking For

**High Priority:**
- Bug fixes for v3.0 features (Modules, OOP, MySQL, PostgreSQL)
- Bug fixes for v2.0 features (File I/O, SQLite, HTTP)
- Security improvements
- Test coverage improvements
- Documentation improvements
- Community engagement & feedback

**Medium Priority:**
- New v4.0+ language features (package manager, advanced tooling)
- Performance optimizations
- Error message improvements
- Additional Telugu keyword synonyms

**Low Priority:**
- Code refactoring (must maintain compatibility)
- Style changes

### What to Avoid

❌ **Do NOT:**
- Add external dependencies without discussion
- Introduce security vulnerabilities
- Break existing functionality
- Remove tests
- Commit secrets or credentials
- Use offensive language in code/comments

### Getting Help

- 💬 Open a discussion for questions
- 🐛 Open an issue for bugs
- 💡 Open an issue for feature requests

### Recognition

Contributors will be:
- Listed in project credits
- Mentioned in release notes
- Part of making programming accessible!

---

## తెలుగు | Telugu

### స్వాగతం!

lipi-lang కు సహకరించడానికి మీ ఆసక్తికి ధన్యవాదాలు! ఈ ప్రాజెక్ట్ తెలుగు మాట్లాడే విద్యార్థులకు ప్రోగ్రామింగ్‌ను అందుబాటులోకి తీసుకురావడం లక్ష్యం.

### అభివృద్ధి సెటప్

```bash
# రిపోజిటరీని క్లోన్ చేయండి
git clone https://github.com/ramrayavarapu/lipi-lang.git
cd lipi-lang

# టెస్ట్‌లను రన్ చేయండి
python3 test_lipi.py
```

### మార్పులు చేయడం

1. **బ్రాంచ్ సృష్టించండి**
2. **మీ మార్పులు చేయండి**
3. **టెస్ట్‌లను రన్ చేయండి**
4. **మీ మార్పులను కమిట్ చేయండి**

### భద్రతా అవసరాలు ⚠️

**కీలకం:** అన్ని కోడ్ భద్రతా తనిఖీలలో ఉత్తీర్ణత సాధించాలి.

మీ మార్పులు తప్పనిసరిగా:
- ✅ అన్ని 39 ఆటోమేటెడ్ టెస్ట్‌లను పాస్ చేయాలి
- ✅ సెక్యూరిటీ స్కానర్‌ను పాస్ చేయాలి
- ✅ ప్రమాదకరమైన ఫంక్షన్లను ప్రవేశపెట్టకూడదు

### సహాయం పొందడం

- 💬 ప్రశ్నల కోసం చర్చను ప్రారంభించండి
- 🐛 బగ్‌ల కోసం ఇష్యూను ఓపెన్ చేయండి
- 💡 ఫీచర్ రిక్వెస్ట్‌ల కోసం ఇష్యూను ఓపెన్ చేయండి

---

**Thank you for contributing to making programming accessible in Telugu!**
**తెలుగులో ప్రోగ్రామింగ్‌ను అందుబాటులోకి తీసుకురావడంలో సహకరించినందుకు ధన్యవాదాలు!**
