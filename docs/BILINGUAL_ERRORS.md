# Bilingual Error Messages (v3.0)

## Overview

As of v3.0, lipi-lang supports fully bilingual error messages. You can choose to see error messages in either English or Telugu using the `--lang` command-line option.

## Usage

### Default (English Error Messages)

```bash
python lipi.py script.lipi.py
```

Example error output:
```
[Error] Runtime error: [Error] Unknown expression: undefined_variable
```

### Telugu Error Messages

```bash
python lipi.py script.lipi.py --lang te
```

Example error output:
```
[లోపం] రన్‌టైమ్ లోపం: [లోపం] తెలియని వ్యక్తీకరణ: undefined_variable
```

### In REPL Mode

```bash
# English REPL
python lipi.py

# Telugu REPL
python lipi.py --lang te
```

## Supported Error Messages

The following error types have bilingual support:

| Error Type | English | Telugu |
|------------|---------|--------|
| Runtime error | Runtime error | రన్‌టైమ్ లోపం |
| Unknown expression | Unknown expression | తెలియని వ్యక్తీకరణ |
| Function not defined | Function not defined | ఫంక్షన్ నిర్వచించబడలేదు |
| Variable not defined | Variable not defined | వేరియబుల్ నిర్వచించబడలేదు |
| Class not defined | Class not defined | క్లాస్ నిర్వచించబడలేదు |
| Invalid syntax | Invalid syntax | చెల్లని వాక్యనిర్మాణం |
| Division by zero | Division by zero | సున్నాతో భాగహారం |
| Import error | Import error | దిగుమతి లోపం |
| Module not found | Module not found | మాడ్యూల్ కనుగొనబడలేదు |
| Circular import detected | Circular import detected | వృత్తాకార దిగుమతి గుర్తించబడింది |
| Invalid module path | Invalid module path. Path traversal not allowed | చెల్లని మాడ్యూల్ పాత్. పాత్ ట్రావర్సల్ అనుమతించబడదు |
| Database error | Database error | డేటాబేస్ లోపం |
| Connection error | Connection error | కనెక్షన్ లోపం |
| File error | File error | ఫైల్ లోపం |
| HTTP error | HTTP error | HTTP లోపం |
| Type error | Type error | రకం లోపం |
| Attribute error | Attribute error | ఆట్రిబ్యూట్ లోపం |
| Index out of range | Index out of range | ఇండెక్స్ పరిధి దాటింది |
| Key not found | Key not found | కీ కనుగొనబడలేదు |

## Examples

### Example 1: Undefined Variable Error

**File:** `test.lipi.py`
```python
చెప్పు unknown_var
```

**English mode:**
```bash
$ python lipi.py test.lipi.py
[Error] Runtime error: [Error] Unknown expression: unknown_var
```

**Telugu mode:**
```bash
$ python lipi.py test.lipi.py --lang te
[లోపం] రన్‌టైమ్ లోపం: [లోపం] తెలియని వ్యక్తీకరణ: unknown_var
```

### Example 2: Module Not Found Error

**File:** `test_import.lipi.py`
```python
దిగుమతి func from "nonexistent"
```

**English mode:**
```bash
$ python lipi.py test_import.lipi.py
[Error] Runtime error: [Error] Module not found: /path/to/nonexistent.lipi.py
```

**Telugu mode:**
```bash
$ python lipi.py test_import.lipi.py --lang te
[లోపం] రన్‌టైమ్ లోపం: [లోపం] మాడ్యూల్ కనుగొనబడలేదు: /path/to/nonexistent.lipi.py
```

### Example 3: Path Traversal Security Error

**File:** `test_security.lipi.py`
```python
దిగుమతి hack from "../../../etc/passwd"
```

**English mode:**
```bash
$ python lipi.py test_security.lipi.py
[Error] Runtime error: [Error] Invalid module path. Path traversal not allowed: ../../../etc/passwd
```

**Telugu mode:**
```bash
$ python lipi.py test_security.lipi.py --lang te
[లోపం] రన్‌టైమ్ లోపం: [లోపం] చెల్లని మాడ్యూల్ పాత్. పాత్ ట్రావర్సల్ అనుమతించబడదు: ../../../etc/passwd
```

### Example 4: Circular Import Detection

**File:** `a.lipi.py`
```python
దిగుమతి func from "b"
```

**File:** `b.lipi.py`
```python
దిగుమతి func from "a"
```

**English mode:**
```bash
$ python lipi.py a.lipi.py
[Error] Runtime error: [Error] Circular import detected: a.lipi.py -> b.lipi.py -> a.lipi.py
```

**Telugu mode:**
```bash
$ python lipi.py a.lipi.py --lang te
[లోపం] రన్‌టైమ్ లోపం: [లోపం] వృత్తాకార దిగుమతి గుర్తించబడింది: a.lipi.py -> b.lipi.py -> a.lipi.py
```

## Command-Line Help

View all available options:

```bash
$ python lipi.py --help

usage: lipi.py [-h] [--lang {en,te}] [file]

Lipi Language v3.0 - Bilingual (Telugu + English) Programming

positional arguments:
  file            Lipi script file to run

options:
  -h, --help      show this help message and exit
  --lang {en,te}  Error message language: en (English) or te (Telugu).
                  Default: en

Examples:
  python lipi.py script.lipi.py           # Run script in English error mode
  python lipi.py script.lipi.py --lang te # Run script with Telugu errors
  python lipi.py --lang te                # Start REPL with Telugu errors
  python lipi.py                          # Start REPL with English errors
```

## Benefits

### For Telugu Developers
- Learn programming in your native language
- Error messages in Telugu make debugging more accessible
- No need to translate error messages mentally

### For English Developers
- Standard English error messages
- Familiar debugging experience
- Easy collaboration with Telugu developers

### For Mixed Teams
- Each developer can work in their preferred language
- Error preferences can be set individually
- Same codebase, personalized error experience

## Implementation Details

The bilingual error system is implemented using:

1. **Error Message Dictionary**: Two complete dictionaries (English and Telugu) for all error types
2. **Language Preference**: Global setting that can be configured via `--lang` argument
3. **Error Formatter**: `get_error_message()` function that retrieves messages in the selected language
4. **Fallback System**: If a message is missing in Telugu, falls back to English

This ensures:
- ✅ Consistent error messages across the codebase
- ✅ Easy to add new error types
- ✅ Graceful degradation if translations are missing
- ✅ Zero performance overhead

## Future Enhancements (v4.0+)

Potential improvements for future versions:

1. **Environment Variable Support**: `LIPI_LANG=te python lipi.py script.lipi.py`
2. **Config File**: Store language preference in `.lipirc` configuration file
3. **More Languages**: Add support for other Indian languages (Hindi, Tamil, etc.)
4. **Localized Stack Traces**: Translate stack trace messages as well
5. **IDE Integration**: Language preference in IDE settings

## Contributing

To add new error messages or improve translations:

1. Add the error key to `ERROR_MESSAGES` dictionary in `src/lipi.py`
2. Provide both English (`'en'`) and Telugu (`'te'`) translations
3. Use `get_error_message('error_key', detail)` in your code
4. Test with both `--lang en` and `--lang te`
5. Submit a pull request!

Example:
```python
ERROR_MESSAGES = {
    'en': {
        'new_error': 'This is a new error message',
    },
    'te': {
        'new_error': 'ఇది కొత్త దోష సందేశం',
    }
}

# Usage in code:
raise LipiException(get_error_message('new_error', detail_info))
```

---

**Last Updated:** December 7, 2025
**Feature Version:** v3.0
**Status:** Implemented and tested
