# Lipi-Lang Quick Reference | లిపి-భాష శీఘ్ర సూచన

Complete keyword and syntax reference for lipi-lang programming language.

## 📝 Basic Syntax | ప్రాథమిక వాక్యనిర్మాణం

### Comments | వ్యాఖ్యలు
```python
# This is a comment in English
# ఇది ఇంగ్లీష్‌లో వ్యాఖ్య

# Both languages support comments
# రెండు భాషలు వ్యాఖ్యలకు మద్దతు ఇస్తాయి
```

## 🔤 Variables | వేరియబుల్స్

### Variable Assignment | వేరియబుల్ కేటాయింపు

**Telugu:**
```python
పేరు = "రాము"
వయసు = 25
నగరం = "హైదరాబాద్"
```

**English:**
```python
name = "Ramu"
age = 25
city = "Hyderabad"
```

**Bilingual (Mixed):**
```python
పేరు = "Ramu"
age = 25
నగరం = "Hyderabad"
```

## 📊 Data Types | డేటా రకాలు

### Strings | స్ట్రింగ్స్ (చరరాశి)
```python
పేరు = "రాము"          # Telugu variable
name = "Ramu"           # English variable
message = 'Hello'       # Single quotes work too
సందేశం = 'నమస్తే'      # Telugu with single quotes
```

### Numbers | సంఖ్యలు
```python
వయసు = 25              # Integer
age = 30                # Integer
ధర = 99.99             # Float/Decimal
price = 49.50           # Float/Decimal
```

### Booleans | బూలియన్లు
```python
సత్యం = true           # Telugu true
అబద్ధం = false         # Telugu false
isActive = true         # English true
isComplete = false      # English false
```

## 🖨️ Output | అవుట్‌పుట్

### Print Statements | ప్రింట్ స్టేట్‌మెంట్స్

**Telugu:**
```python
చెప్పు "నమస్తే"
చెప్పు "పేరు: " + పేరు
చెప్పు వయసు
```

**English:**
```python
print "Hello"
print "Name: " + name
print age
```

**String Concatenation:**
```python
చెప్పు "నా పేరు " + పేరు + " మరియు నా వయసు " + వయసు
print "My name is " + name + " and I am " + age
```

## 🔀 Conditional Statements | షరతుల స్టేట్‌మెంట్స్

### If-Else | ఒకవేళ-లేకపోతే

**Telugu:**
```python
ఒకవేళ వయసు > 18:
    చెప్పు "పెద్దవారు"
లేకపోతే:
    చెప్పు "చిన్నవారు"
ముగింపు
```

**English:**
```python
if age > 18:
    print "Adult"
else:
    print "Minor"
end
```

**Bilingual:**
```python
ఒకవేళ age >= 18:
    చెప్పు "You are an adult"
    print "మీరు పెద్దవారు"
లేకపోతే:
    చెప్పు "You are a minor"
ముగింపు
```

### Comparison Operators | పోలిక ఆపరేటర్లు

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `వయసు == 25` |
| `!=` | Not equal to | `age != 30` |
| `>` | Greater than | `వయసు > 18` |
| `<` | Less than | `age < 50` |
| `>=` | Greater or equal | `వయసు >= 21` |
| `<=` | Less or equal | `age <= 65` |

## 🔁 Loops | లూప్స్

### While Loop | వరకు లూప్

**Telugu:**
```python
సంఖ్య = 1

వరకు సంఖ్య <= 5:
    చెప్పు సంఖ్య
    సంఖ్య = సంఖ్య + 1
ముగింపు
```

**English:**
```python
count = 1

while count <= 5:
    print count
    count = count + 1
end
```

### For Loop | ప్రతి లూప్

**Telugu:**
```python
ప్రతి ఐ లో పరిధి(1, 6):
    చెప్పు "సంఖ్య: " + ఐ
ముగింపు
```

**English:**
```python
for i in range(1, 6):
    print "Number: " + i
end
```

## 📋 Complete Keyword Reference | పూర్తి కీవర్డ్ సూచన

### Core Keywords | ప్రధాన కీవర్డ్‌లు

| Telugu | English | Purpose | Example |
|--------|---------|---------|---------|
| `చెప్పు` | `print` | Output/Display | `చెప్పు "Hello"` |
| `ఒకవేళ` | `if` | Conditional | `ఒకవేళ x > 5:` |
| `లేకపోతే:` | `else:` | Alternative | `లేకపోతే:` |
| `వరకు` | `while` | While loop | `వరకు count < 10:` |
| `ప్రతి` | `for` | For loop | `ప్రతి i లో range(10):` |
| `లో` | `in` | Iterator | `ప్రతి ఐ లో పరిధి(5):` |
| `ముగింపు` | `end` | End block | `ముగింపు` |

### Advanced Keywords (v1.0+) | ఆధునాతన కీవర్డ్‌లు

| Telugu | English | Purpose | Example |
|--------|---------|---------|---------|
| `పనిచేయి` | `function` | Define function | `పనిచేయి add(a, b):` |
| `రిటర్న్` | `return` | Return value | `రిటర్న్ a + b` |
| `ప్రయత్నించు:` | `try:` | Error handling | `ప్రయత్నించు:` |
| `పట్టుకో:` | `catch:` | Catch errors | `పట్టుకో:` |
| `చివరకు:` | `finally:` | Finally block | `చివరకు:` |
| `జాబితా` | `list` | Create list | `జాబితా = [1, 2, 3]` |
| `పరిధి` | `range` | Range function | `పరిధి(1, 10)` |

### File & Network (v2.0+) | ఫైల్ & నెట్‌వర్క్

| Telugu | English | Purpose | Example |
|--------|---------|---------|---------|
| `ఫైల్_చదువు` | `file_read` | Read file | `ఫైల్_చదువు("data.txt")` |
| `ఫైల్_వ్రాయి` | `file_write` | Write file | `ఫైల్_వ్రాయి("out.txt", data)` |
| `http_పొందు` | `http_get` | HTTP GET | `http_పొందు("https://api...")` |
| `http_పంపు` | `http_post` | HTTP POST | `http_పంపు(url, data)` |

### Database (v2.0+) | డేటాబేస్

| Telugu | English | Purpose | Example |
|--------|---------|---------|---------|
| `డేటాబేస్_కనెక్ట్` | `db_connect` | Connect to DB | `డేటాబేస్_కనెక్ట్("db.sqlite")` |
| `డేటాబేస్_ప్రశ్న` | `db_query` | Run SQL query | `డేటాబేస్_ప్రశ్న(db, sql)` |

### OOP & Modules (v3.0+) | OOP & మాడ్యూల్స్

| Telugu | English | Purpose | Example |
|--------|---------|---------|---------|
| `క్లాస్` | `class` | Define class | `క్లాస్ Person:` |
| `స్వీయ` | `self` | Self reference | `స్వీయ.name = name` |
| `దిగుమతి` | `import` | Import module | `దిగుమతి func from "module"` |
| `ఎగుమతి` | `export` | Export items | `ఎగుమతి func, var` |

## 💡 Common Patterns | సాధారణ నమూనాలు

### Pattern 1: User Input & Output
```python
# Telugu
పేరు = "రాము"
చెప్పు "నమస్తే, " + పేరు + "!"

# English
name = "Ramu"
print "Hello, " + name + "!"
```

### Pattern 2: Counting Loop
```python
# Telugu
ప్రతి సంఖ్య లో పరిధి(1, 11):
    చెప్పు "లెక్క: " + సంఖ్య
ముగింపు

# English
for number in range(1, 11):
    print "Count: " + number
end
```

### Pattern 3: Conditional Check
```python
# Telugu
స్కోరు = 85

ఒకవేళ స్కోరు >= 90:
    చెప్పు "అద్భుతం!"
లేకపోతే:
    ఒకవేళ స్కోరు >= 75:
        చెప్పు "బాగుంది!"
    లేకపోతే:
        చెప్పు "మెరుగుపరచండి"
    ముగింపు
ముగింపు
```

### Pattern 4: Function Definition (v1.0+)
```python
# Telugu
పనిచేయి చదరపు(సంఖ్య):
    రిటర్న్ సంఖ్య * సంఖ్య
ముగింపు

ఫలితం = చదరపు(5)
చెప్పు "5 యొక్క చదరపు: " + ఫలితం

# English
function square(number):
    return number * number
end

result = square(5)
print "Square of 5: " + result
```

## 🎯 Best Practices | ఉత్తమ పద్ధతులు

### 1. Choose One Language Per Project
```python
# Good: Consistent Telugu
పేరు = "రాము"
వయసు = 25
చెప్పు పేరు

# Also Good: Consistent English
name = "Ramu"
age = 25
print name
```

### 2. Use Meaningful Variable Names
```python
# Good
విద్యార్థి_పేరు = "రాము"
student_name = "Ramu"

# Avoid
x = "రాము"
a = "Ramu"
```

### 3. Add Comments for Clarity
```python
# Calculate area of rectangle
# దీర్ఘచతురస్రం వైశాల్యం లెక్కించండి
పొడవు = 10
వెడల్పు = 5
వైశాల్యం = పొడవు * వెడల్పు
చెప్పు "వైశాల్యం: " + వైశాల్యం
```

### 4. Proper Block Endings
```python
# Always end blocks with ముగింపు/end
ఒకవేళ condition:
    # statements
ముగింపు  # Don't forget this!

while condition:
    # statements
end  # Or this!
```

## 🔍 Quick Examples | శీఘ్ర ఉదాహరణలు

### Example 1: Simple Calculator
```python
# Telugu Calculator
సంఖ్య1 = 10
సంఖ్య2 = 5

చెప్పు "కూడిక: " + (సంఖ్య1 + సంఖ్య2)
చెప్పు "తీసివేత: " + (సంఖ్య1 - సంఖ్య2)
చెప్పు "గుణకారం: " + (సంఖ్య1 * సంఖ్య2)
చెప్పు "భాగహారం: " + (సంఖ్య1 / సంఖ్య2)
```

### Example 2: Grade Calculator
```python
# English Grade Calculator
score = 85

if score >= 90:
    print "Grade: A"
else:
    if score >= 80:
        print "Grade: B"
    else:
        if score >= 70:
            print "Grade: C"
        else:
            print "Grade: D"
        end
    end
end
```

### Example 3: Multiplication Table
```python
# Bilingual Multiplication Table
సంఖ్య = 5

print "Multiplication table for " + సంఖ్య
చెప్పు "గుణకార పట్టిక: " + సంఖ్య

ప్రతి i లో పరిధి(1, 11):
    ఫలితం = సంఖ్య * i
    చెప్పు సంఖ్య + " × " + i + " = " + ఫలితం
ముగింపు
```

## 🌍 Real-World Examples | వాస్తవిక ఉదాహరణలు

### Example 4: Age Validator
```python
# Telugu Version - వయసు ధ్రువీకరణ
పేరు = "రాధ"
వయసు = 16

చెప్పు "పేరు: " + పేరు
చెప్పు "వయసు: " + వయసు

ఒకవేళ వయసు < 13:
    చెప్పు "⚠️ చాలా చిన్నవారు - తల్లిదండ్రుల అనుమతి అవసరం"
లేకపోతే:
    ఒకవేళ వయసు < 18:
        చెప్పు "✓ టీనేజర్ - పరిమిత యాక్సెస్"
    లేకపోతే:
        చెప్పు "✓ పూర్తి యాక్సెస్"
    ముగింపు
ముగింపు

# English Version
name = "Radha"
age = 16

print "Name: " + name
print "Age: " + age

if age < 13:
    print "⚠️ Too young - parental consent required"
else:
    if age < 18:
        print "✓ Teenager - limited access"
    else:
        print "✓ Full access"
    end
end
```

### Example 5: Sum of Numbers
```python
# Telugu - సంఖ్యల మొత్తం
మొత్తం = 0
సంఖ్య = 1

వరకు సంఖ్య <= 100:
    మొత్తం = మొత్తం + సంఖ్య
    సంఖ్య = సంఖ్య + 1
ముగింపు

చెప్పు "1 నుండి 100 వరకు మొత్తం: " + మొత్తం

# English - Sum of Numbers
total = 0
number = 1

while number <= 100:
    total = total + number
    number = number + 1
end

print "Sum from 1 to 100: " + total
```

### Example 6: Password Strength Checker
```python
# Bilingual Password Checker
పాస్‌వర్డ్ = "MySecret123"
పొడవు = 12  # Length of password

ఒకవేళ పొడవు < 6:
    చెప్పు "❌ Weak password - చాలా చిన్నది"
లేకపోతే:
    ఒకవేళ పొడవు < 10:
        చెప్పు "⚠️ Medium password - బాగుంది కానీ మెరుగుపరచవచ్చు"
    లేకపోతే:
        చెప్పు "✅ Strong password - చాలా బలమైనది!"
    ముగింపు
ముగింపు
```

### Example 7: Shopping Cart Total
```python
# Telugu Shopping Cart
item1_ధర = 150
item2_ధర = 300
item3_ధర = 75

ఉప_మొత్తం = item1_ధర + item2_ధర + item3_ధర
పన్ను = ఉప_మొత్తం * 0.18  # 18% GST
మొత్తం_ధర = ఉప_మొత్తం + పన్ను

చెప్పు "ఉప మొత్తం: ₹" + ఉప_మొత్తం
చెప్పు "GST (18%): ₹" + పన్ను
చెప్పు "మొత్తం ధర: ₹" + మొత్తం_ధర

ఒకవేళ మొత్తం_ధర > 500:
    డిస్కౌంట్ = మొత్తం_ధర * 0.10
    తుది_ధర = మొత్తం_ధర - డిస్కౌంట్
    చెప్పు "🎉 10% డిస్కౌంట్ వర్తించబడింది!"
    చెప్పు "చెల్లించవలసిన మొత్తం: ₹" + తుది_ధర
ముగింపు
```

### Example 8: Temperature Converter
```python
# Celsius to Fahrenheit
సెల్సియస్ = 37
ఫారెన్‌హీట్ = (సెల్సియస్ * 9 / 5) + 32

చెప్పు సెల్సియస్ + "°C = " + ఫారెన్‌హీట్ + "°F"

ఒకవేళ సెల్సియస్ < 0:
    చెప్పు "🥶 గడ్డకట్టే ఉష్ణోగ్రత!"
లేకపోతే:
    ఒకవేళ సెల్సియస్ < 15:
        చెప్పు "🧥 చల్లగా ఉంది"
    లేకపోతే:
        ఒకవేళ సెల్సియస్ < 30:
            చెప్పు "☀️ సౌకర్యవంతమైన ఉష్ణోగ్రత"
        లేకపోతే:
            చెప్పు "🔥 చాలా వేడిగా ఉంది!"
        ముగింపు
    ముగింపు
ముగింపు
```

## ⚠️ Common Errors & Solutions | సాధారణ దోషాలు & పరిష్కారాలు

### Error 1: Forgetting `ముగింపు/end`
```python
# ❌ WRONG
ఒకవేళ వయసు > 18:
    చెప్పు "పెద్దవారు"
# Missing ముగింపు!

# ✅ CORRECT
ఒకవేళ వయసు > 18:
    చెప్పు "పెద్దవారు"
ముగింపు
```

### Error 2: Incorrect Indentation
```python
# ❌ WRONG
ఒకవేళ x > 5:
చెప్పు "Too big"  # Should be indented!
ముగింపు

# ✅ CORRECT
ఒకవేళ x > 5:
    చెప్పు "Too big"  # Properly indented
ముగింపు
```

### Error 3: Mixing Quote Types
```python
# ❌ WRONG
పేరు = "రాము'  # Mixed quotes!

# ✅ CORRECT
పేరు = "రాము"  # Matching quotes
# or
పేరు = 'రాము'  # Both work, but must match
```

### Error 4: String + Number Without Conversion
```python
# ❌ WRONG (in full interpreter)
వయసు = 25
చెప్పు "వయసు: " + వయసు  # May cause type error

# ✅ CORRECT
వయసు = 25
చెప్పు "వయసు: " + str(వయసు)  # Convert to string

# ⚠️ Note: Learning platform handles this automatically
```

### Error 5: Wrong Comparison Operator
```python
# ❌ WRONG
ఒకవేళ వయసు = 18:  # Assignment, not comparison!
    చెప్పు "Eighteen"
ముగింపు

# ✅ CORRECT
ఒకవేళ వయసు == 18:  # Use == for comparison
    చెప్పు "Eighteen"
ముగింపు
```

### Error 6: Infinite Loop
```python
# ❌ WRONG
సంఖ్య = 1
వరకు సంఖ్య <= 10:
    చెప్పు సంఖ్య
    # Forgot to increment! Loop runs forever
ముగింపు

# ✅ CORRECT
సంఖ్య = 1
వరకు సంఖ్య <= 10:
    చెప్పు సంఖ్య
    సంఖ్య = సంఖ్య + 1  # Increment to avoid infinite loop
ముగింపు
```

### Error 7: Undefined Variable
```python
# ❌ WRONG
చెప్పు పేరు  # Variable not defined yet!

# ✅ CORRECT
పేరు = "రాము"  # Define first
చెప్పు పేరు   # Then use
```

## 💡 Debugging Tips | డీబగ్గింగ్ చిట్కాలు

**1. Print Everything (చెప్పు-Driven Development)**
```python
సంఖ్య = 10
చెప్పు "Before calculation: " + సంఖ్య
ఫలితం = సంఖ్య * 2
చెప్పు "After calculation: " + ఫలితం
```

**2. Check One Thing at a Time**
```python
# Break complex conditions into steps
వయసు = 17
పేరు = "రాము"

చెప్పు "Checking age..."
ఒకవేళ వయసు >= 18:
    చెప్పు "Age check passed"
లేకపోతే:
    చెప్పు "Age check failed"
ముగింపు
```

**3. Comment Out Code to Isolate Problems**
```python
పేరు = "రాము"
వయసు = 25

చెప్పు పేరు
# ఒకవేళ వయసు > 18:  # Comment this out to test
#     చెప్పు "Adult"
# ముగింపు
```

## 📚 Learning Resources | నేర్చుకునే వనరులు

1. **Learning Platform** - Complete the interactive lessons in `index.html`
2. **Example Files** - Check `../examples/` directory for more code samples
3. **Main Documentation** - See `../README.md` for full lipi-lang documentation
4. **v3.0 Guide** - Read `../docs/V3_GUIDE.md` for advanced features

## ❓ Common Questions | సాధారణ ప్రశ్నలు

### Q: Can I mix Telugu and English keywords?
**A:** Yes! Lipi-lang is fully bilingual. Use whichever language you're comfortable with.

### Q: What's the difference between చెప్పు and print?
**A:** They're identical! చెప్పు is Telugu, print is English. Both do the same thing.

### Q: Do I need Python installed to use the learning platform?
**A:** No! The learning platform runs entirely in your web browser. However, to run full lipi-lang programs, you'll need Python and the interpreter at `../src/lipi.py`

### Q: Where are my variables stored?
**A:** Variables are stored in memory during program execution. The learning platform also uses browser LocalStorage to save your progress.

---

**Quick Tip:** Keep this reference open while coding for easy keyword lookup!
**శీఘ్ర చిట్కా:** కోడింగ్ చేస్తున్నప్పుడు సులభంగా కీవర్డ్ శోధన కోసం ఈ సూచనను తెరిచి ఉంచండి!
