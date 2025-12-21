# Bilingual Error Messages in Lipi-Lang
## ద్విభాషా లోపం సందేశాలు లిపి-లాంగ్‌లో

Complete guide to error handling in Telugu and English

---

## 🎯 Overview

**Yes! Lipi-lang supports bilingual error messages** in both Telugu and English!

There are **two levels** of error messages:

### 1. **Application-Level Errors** (Developer-Controlled)
You write custom error messages in Telugu, English, or both!

### 2. **Interpreter-Level Errors** (Built-in)
The lipi-lang interpreter has bilingual support for common errors.

---

## ✅ Application-Level Error Messages

### Telugu Error Messages

```python
పనిచేయి divide(a, b):
    యెడల b == 0:
        చెప్పు "❌ లోపం: సున్నాతో భాగించడం సాధ్యం కాదు!"
        చెప్పు "   దయచేసి సున్నా కాని సంఖ్యను ఉపయోగించండి"
        రిటర్న్ null
    ముగింపు
    రిటర్న్ a / b
ముగింపు
```

**Output:**
```
❌ లోపం: సున్నాతో భాగించడం సాధ్యం కాదు!
   దయచేసి సున్నా కాని సంఖ్యను ఉపయోగించండి
```

### Bilingual Error Messages

```python
function square_root(n):
    if n < 0:
        చెప్పు "❌ లోపం: ప్రతికూల సంఖ్య యొక్క వర్గమూలం లెక్కించలేము!"
        print "❌ Error: Cannot calculate square root of negative number!"
        return null
    end
    # ... rest of function
end
```

**Output:**
```
❌ లోపం: ప్రతికూల సంఖ్య యొక్క వర్గమూలం లెక్కించలేము!
❌ Error: Cannot calculate square root of negative number!
```

---

## 🔧 Interpreter-Level Error Messages

### Built-in Bilingual Errors

The lipi-lang interpreter includes Telugu translations for common errors:

#### 1. **Unknown Variable/Expression**

```python
print unknown_variable
```

**Output:**
```
[లోపం] Runtime error: తెలియని వ్యక్తీకరణ (unknown expression): unknown_variable
```

- `లోపం` = Error
- `తెలియని వ్యక్తీకరణ` = Unknown expression

#### 2. **Unknown Syntax**

```python
some_invalid_syntax_here
```

**Output:**
```
[లోపం] Runtime error: తెలియని లైన్ (unknown line): some_invalid_syntax_here
```

- `తెలియని లైన్` = Unknown line

#### 3. **Function Not Found**

```python
result = call nonexistent_function(10)
```

**Output:**
```
[లోపం] Runtime error: Function not found: nonexistent_function
```

#### 4. **Wrong Number of Arguments**

```python
పనిచేయి add(a, b):
    రిటర్న్ a + b
ముగింపు

result = కాల్ add(5)  # Missing second argument
```

**Output:**
```
[లోపం] Runtime error: Function add expects 2 arguments, got 1
```

---

## 📊 Common Error Types in Telugu

### Error Categories

| Error Type | Telugu | Example |
|------------|--------|---------|
| **Error** | లోపం | లోపం: విలువ లేదు |
| **Division by zero** | సున్నాతో భాగించడం | సున్నాతో భాగించలేము! |
| **Negative number** | ప్రతికూల సంఖ్య | ప్రతికూల సంఖ్య చెల్లదు |
| **Invalid input** | చెల్లని ఇన్‌పుట్ | చెల్లని ఇన్‌పుట్ విలువ |
| **Null/Empty** | శూన్యం | విలువ శూన్యంగా ఉంది |
| **Too low** | చాలా తక్కువ | విలువ చాలా తక్కువగా ఉంది |
| **Too high** | చాలా ఎక్కువ | విలువ చాలా ఎక్కువగా ఉంది |
| **Not allowed** | అనుమతి లేదు | ఈ కార్యకలాపం అనుమతి లేదు |
| **Required** | అవసరం | ఈ విలువ అవసరం |
| **Please** | దయచేసి | దయచేసి సరైన విలువ ఇవ్వండి |

---

## 💡 Best Practices

### 1. **Always Provide Both Languages**

For maximum accessibility, include both Telugu and English:

```python
function validate(value):
    యెడల value == null:
        చెప్పు "❌ లోపం: విలువ శూన్యంగా ఉంది!"
        print "❌ Error: Value is null!"
        రిటర్న్ false
    ముగింపు
    రిటర్న్ true
end
```

### 2. **Use Clear Error Messages**

```python
# Good - Clear and specific
చెప్పు "❌ లోపం: సున్నాతో భాగించలేము!"
చెప్పు "   దయచేసి సున్నా కాని సంఖ్యను ఉపయోగించండి"

# Not ideal - Too vague
చెప్పు "❌ లోపం!"
```

### 3. **Include Context**

```python
పనిచేయి divide(a, b):
    యెడల b == 0:
        చెప్పు "❌ లోపం: సున్నాతో భాగించలేము!"
        print "❌ Error: Cannot divide by zero!"
        # Include values for debugging
        a_str = str(a)
        b_str = str(b)
        చెప్పు "   విలువలు: a = " + a_str + ", b = " + b_str
        print "   Values: a = " + a_str + ", b = " + b_str
        రిటర్న్ null
    ముగింపు
    రిటర్న్ a / b
ముగింపు
```

### 4. **Use Unicode Symbols**

Make errors visually distinct:

```python
చెప్పు "❌ లోపం: Division by zero"    # Error
చెప్పు "⚠️  హెచ్చరిక: Low battery"    # Warning
చెప్పు "✅ విజయం: Operation complete"  # Success
చెప్పు "ℹ️  సమాచారం: Processing..."    # Info
```

---

## 📝 Error Message Templates

### Division by Zero

```python
యెడల b == 0:
    చెప్పు "❌ లోపం: సున్నాతో భాగించడం సాధ్యం కాదు!"
    print "❌ Error: Division by zero is not allowed!"
    చెప్పు "   దయచేసి సున్నా కాని సంఖ్యను ఉపయోగించండి"
    print "   Please use a non-zero number"
    రిటర్న్ null
ముగింపు
```

### Negative Value

```python
if n < 0:
    చెప్పు "❌ లోపం: ప్రతికూల విలువ చెల్లదు!"
    print "❌ Error: Negative value not allowed!"
    val_str = str(n)
    చెప్పు "   విలువ: " + val_str
    print "   Value: " + val_str
    return null
end
```

### Null/Empty Value

```python
యెడల value == null:
    చెప్పు "❌ లోపం: విలువ శూన్యంగా ఉంది!"
    print "❌ Error: Value is null!"
    చెప్పు "   దయచేసి చెల్లుబాటు అయ్యే విలువను అందించండి"
    print "   Please provide a valid value"
    రిటర్న్ false
ముగింపు
```

### Range Validation

```python
యెడల value < min_val:
    చెప్పు "❌ లోపం: విలువ చాలా తక్కువగా ఉంది!"
    print "❌ Error: Value is too low!"
    min_str = str(min_val)
    చెప్పు "   కనీస విలువ: " + min_str
    print "   Minimum value: " + min_str
    రిటర్న్ false
ముగింపు
```

### Invalid Type

```python
if type_check_failed:
    చెప్పు "❌ లోపం: చెల్లని డేటా రకం!"
    print "❌ Error: Invalid data type!"
    చెప్పు "   ఆశించిన రకం: సంఖ్య, పొందినది: వాక్యం"
    print "   Expected: number, Got: string"
    return null
end
```

---

## 🎯 Real-World Examples

### Calculator with Full Error Handling

```python
పనిచేయి safe_calculate(operation, a, b):
    # Validate inputs
    యెడల a == null:
        చెప్పు "❌ లోపం: మొదటి సంఖ్య శూన్యం!"
        print "❌ Error: First number is null!"
        రిటర్న్ null
    ముగింపు

    if b == null:
        చెప్పు "❌ లోపం: రెండవ సంఖ్య శూన్యం!"
        print "❌ Error: Second number is null!"
        return null
    end

    # Perform operation
    యెడల operation == "add":
        రిటర్న్ a + b
    ముగింపు

    if operation == "divide":
        యెడల b == 0:
            చెప్పు "❌ లోపం: సున్నాతో భాగించలేము!"
            print "❌ Error: Cannot divide by zero!"
            రిటర్న్ null
        ముగింపు
        return a / b
    end

    # Unknown operation
    చెప్పు "❌ లోపం: తెలియని కార్యకలాపం: " + operation
    print "❌ Error: Unknown operation: " + operation
    రిటర్న్ null
ముగింపు
```

---

## 📊 Summary

### ✅ What Works

| Feature | Status | Example |
|---------|--------|---------|
| **Custom Telugu errors** | ✅ Full support | `చెప్పు "❌ లోపం: ..."` |
| **Custom English errors** | ✅ Full support | `print "❌ Error: ..."` |
| **Bilingual errors** | ✅ Full support | Both in same program |
| **Interpreter errors** | ✅ Partial Telugu | `[లోపం] తెలియని వ్యక్తీకరణ` |
| **Unicode symbols** | ✅ Full support | ❌ ✅ ⚠️ ℹ️ |

### 🎓 Key Takeaways

1. **Application errors**: Fully customizable in Telugu, English, or both
2. **Interpreter errors**: Partially bilingual (key messages in Telugu)
3. **Best practice**: Always include both languages for accessibility
4. **Clear messages**: Provide context and suggested fixes
5. **Visual aids**: Use Unicode symbols for better UX

---

## 🚀 Try It Yourself

Run the error demonstration:

```bash
python3 src/lipi.py examples/error_demo.lipi.py
```

You'll see:
- ✅ Division by zero errors
- ✅ Negative square root errors
- ✅ Invalid input errors
- ✅ Range validation errors
- ✅ Null value errors
- ✅ Built-in interpreter errors

All with **bilingual messages in Telugu and English!**

---

**Happy Error Handling! | లోపం నిర్వహణ సంతోషంగా ఉండండి!** 🎯
