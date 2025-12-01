# Best Practices for lipi-lang Development

## English | తెలుగు

**English:** This document provides best practices and conventions for writing maintainable, collaborative code in lipi-lang.

**తెలుగు:** ఈ డాక్యుమెంట్ lipi-lang లో నిర్వహించదగిన, సహకార కోడ్ రాయడానికి ఉత్తమ పద్ధతులు మరియు సంప్రదాయాలను అందిస్తుంది.

---

## Variable and Function Naming Conventions

### Problem Statement

**English:** In a bilingual environment, deciding between Telugu and English variable names affects code readability and collaboration.

**తెలుగు:** ద్విభాషా వాతావరణంలో, తెలుగు మరియు ఇంగ్లీష్ వేరియబుల్ పేర్లు మధ్య నిర్ణయం తీసుకోవడం కోడ్ రీడబిలిటీ మరియు సహకారాన్ని ప్రభావితం చేస్తుంది.

**Example of Challenge:**
```python
# Pure Telugu (harder for English developers to read)
పేరు = "రాము"
వయసు = 25
చిరునామా = "హైదరాబాద్"

# Hard to type without Telugu keyboard
# Hard to search/grep for English developers
# Hard to understand variable meaning without translation
```

---

## Recommended Conventions

### ✅ **Option 1: English Variables, Telugu Keywords (RECOMMENDED)**

**Best for bilingual teams and production code**

```python
# Telugu keywords + English variables
name = "Ram"
age = 25
address = "Hyderabad"

యెడల age > 18:
    చెప్పు "Adult: " + name
ముగింపు

# English developer can easily:
# - Read variable names
# - Type them (standard keyboard)
# - Search/grep for "name", "age"
# - Understand business logic
```

**Advantages:**
- ✅ Easy to type (English keyboard)
- ✅ Easy to search/grep
- ✅ Standard naming conventions apply
- ✅ English developers can read
- ✅ Telugu developers still use Telugu keywords
- ✅ Smoother transition to other languages

**When to use:**
- Production code
- Team collaboration (mixed Telugu/English developers)
- Code that will be maintained long-term
- Libraries and shared modules

---

### ✅ **Option 2: Telugu Variables + Telugu Keywords**

**Best for learning and Telugu-only teams**

```python
# Pure Telugu
పేరు = "రాము"
వయసు = 25
చిరునామా = "హైదరాబాద్"

యెడల వయసు > 18:
    చెప్పు "అడల్ట్: " + పేరు
ముగింపు
```

**Advantages:**
- ✅ Natural for Telugu-only learners
- ✅ Complete immersion in Telugu
- ✅ No English knowledge required
- ✅ Good for education/learning phase

**Disadvantages:**
- ⚠️ Requires Telugu keyboard
- ⚠️ Hard for English developers to read
- ⚠️ Difficult to search/grep
- ⚠️ Harder to collaborate with English teams

**When to use:**
- Learning/education environments
- Telugu-only teams
- Personal projects
- Proof-of-concepts

---

### ✅ **Option 3: Mixed Variables (Context-Dependent)**

**Best for domain-specific terminology**

```python
# Business terms in English, cultural terms in Telugu
customer_name = "రాముడు"
customer_age = 25
పండుగ = "దీపావళి"
discount_rate = 0.15

యెడల పండుగ == "దీపావళి":
    final_price = original_price * (1 - discount_rate)
    చెప్పు "Special discount for " + పండుగ
ముగింపు
```

**When to use:**
- Domain-specific terms that are naturally Telugu
- Cultural/regional concepts
- Mixed-audience code

---

## Function Naming Conventions

### Recommended Pattern

**For collaboration:** Function names in English, implementations can use Telugu

```python
# GOOD: English function names (easy to discover)
function calculate_total(items):
    మొత్తం = 0

    వరకు i < len(items):
        మొత్తం = మొత్తం + items[i].price
        i = i + 1
    ముగింపు

    return మొత్తం
end

# Easy to call from any code:
total = call calculate_total(cart_items)
```

**For Telugu-only teams:** Telugu function names are fine

```python
పనిచేయి మొత్తం_లెక్కించు(వస్తువులు):
    మొత్తం = 0
    # ... implementation
    రిటర్న్ మొత్తం
ముగింపు
```

---

## Module and File Naming

### Recommended Convention

**File names:** Use English (easier for tools, IDEs, and sharing)

```
✅ GOOD:
users.lipi.py
products.lipi.py
cart.lipi.py
orders.lipi.py

❌ AVOID:
వినియోగదారులు.lipi.py  # Hard to type, share, version control
```

**Module exports:** Can be Telugu or English based on audience

```python
# File: users.lipi.py

# Export in both languages for flexibility
పనిచేయి సృష్టించు_వినియోగదారుడు(name, email):
    # Implementation
ముగింపు

function create_user(name, email):
    # Same implementation, different name
    return call సృష్టించు_వినియోగదారుడు(name, email)
end

export create_user, సృష్టించు_వినియోగదారుడు
```

---

## Code Comments

### Bilingual Comments for Collaboration

```python
# English comment explaining business logic
# తెలుగు వ్యాఖ్యానం వ్యాపార తర్కాన్ని వివరిస్తుంది

function process_order(order_id):
    # Validate order exists
    # ఆర్డర్ ఉందో తనిఖీ చేయండి

    order = database.get_order(order_id)

    if order == null:
        print "Order not found"
        చెప్పు "ఆర్డర్ కనుగొనబడలేదు"
        return false
    end

    # Process payment
    # చెల్లింపును ప్రాసెస్ చేయండి
    # ... more code
end
```

---

## String Literals

### Recommendation: Based on Audience

**For end users (Telugu speakers):**
```python
error_message = "దోషం సంభవించింది"
success_message = "విజయవంతంగా జోడించబడింది"
చెప్పు error_message
```

**For developers/logs:**
```python
log_message = "User created successfully"
debug_info = "Processing order #" + order_id
print log_message
```

**Best practice:** Use Telugu for user-facing messages, English for developer messages

---

## Constants and Configuration

### Recommendation: English (Industry Standard)

```python
# GOOD: Easy to recognize as constants
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"

# These are universal programming conventions
# Keep them in English for familiarity
```

---

## API/Interface Contracts

### When Building Libraries

**Public API:** Provide both Telugu and English versions

```python
# Library: math_utils.lipi.py

# Telugu API
పనిచేయి వర్గమూలం(సంఖ్య):
    # Implementation
ముగింపు

# English API (wrapper)
function square_root(number):
    return call వర్గమూలం(number)
end

# Export both
export వర్గమూలం, square_root
```

**Users can choose:**
```python
# Telugu developer
result = call వర్గమూలం(16)

# English developer
result = call square_root(16)
```

---

## Summary: Decision Tree

```
Are you writing code that will be:

1. Maintained by mixed Telugu/English team?
   → Use English variables + Telugu keywords ✅

2. Only for Telugu learners/education?
   → Use Telugu variables + Telugu keywords ✅

3. A shared library for both audiences?
   → Provide both Telugu and English APIs ✅

4. Production application?
   → English variables + bilingual comments ✅

5. Personal/learning project?
   → Your choice! Both are fine ✅
```

---

## Code Review Guidelines

### What to Check

**Readability:**
- [ ] Variable names are clear (Telugu or English, but consistent)
- [ ] Function names follow team conventions
- [ ] Comments explain complex logic
- [ ] String messages appropriate for audience

**Collaboration:**
- [ ] English developers can understand flow
- [ ] Telugu keywords enhance, not hinder
- [ ] Mixed teams can work together
- [ ] Code is searchable/greppable

**Maintainability:**
- [ ] Conventions are consistent within file
- [ ] File names are tool-friendly (English)
- [ ] Constants follow standards
- [ ] APIs are well-documented

---

## Examples from Real Code

### ✅ GOOD: Production-Ready Bilingual Code

```python
# File: order_processor.lipi.py
# Author: Mixed team (Telugu + English developers)

import database from "config/database"

# Configuration (English - standard)
MAX_RETRY = 3
TIMEOUT_SECONDS = 30

# Function with English name, bilingual implementation
function process_order(order_id, customer_email):
    # Validate input
    యెడల order_id == null:
        print "Error: Order ID required"
        return false
    ముగింపు

    # Get order from database
    order = database.query("SELECT * FROM orders WHERE id = ?", [order_id])

    యెడల order == null:
        చెప్పు "ఆర్డర్ కనుగొనబడలేదు"
        return false
    ముగింపు

    # Process payment (English developer wrote this)
    payment_success = call process_payment(order.amount)

    if payment_success:
        print "Payment successful"
        చెప్పు "చెల్లింపు విజయవంతమైంది"
        return true
    else:
        చెప్పు "చెల్లింపు విఫలమైంది"
        return false
    end
end

export process_order
```

**Why this works:**
- English variable names (order_id, customer_email, payment_success)
- Bilingual keywords (యెడల, if, చెప్పు, print)
- Bilingual messages (English logs, Telugu user messages)
- Clear, maintainable, collaborative

---

### ❌ AVOID: Hard to Maintain

```python
# All Telugu variables with no context
పీడీఐ = "12345"
సీఈఎం = "test@example.com"
పీఎస్ = false

యెడల పీడీఐ == null:
    చెప్పు "error"
ముగింపు

# Problem: What do these abbreviations mean?
# Hard for anyone (Telugu or English) to understand!
```

**Better:**
```python
order_id = "12345"  # or ఆర్డర్_ఐడి if you prefer Telugu
customer_email = "test@example.com"
payment_success = false

యెడల order_id == null:
    చెప్పు "ఆర్డర్ ఐడి అవసరం"
ముగింపు
```

---

## Tools and Editor Support (Future)

**Coming in v2.0:**
- VS Code extension with Telugu keyword highlighting
- Auto-completion for both Telugu and English
- Variable name transliteration suggestions
- Linting rules for naming conventions

---

## Conclusion

**Recommended Default for Most Projects:**
```python
# ✅ Best Practice: English variables + Telugu keywords

user_age = 25
user_name = "రాము"
is_verified = true

యెడల user_age > 18:
    చెప్పు "Welcome, " + user_name

    if is_verified:
        print "Account verified"
    else:
        చెప్పు "దయచేసి మీ ఖాతాను ధృవీకరించండి"
    end
ముగింపు
```

**This balances:**
- ✅ Telugu language learning (keywords)
- ✅ English developer collaboration (variables)
- ✅ Production readiness (searchable, maintainable)
- ✅ Best of both worlds

---

**Last Updated:** November 30, 2025
**Version:** lipi-lang v0.5
**Status:** Living document - will evolve with community feedback
