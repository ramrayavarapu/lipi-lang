# lipi-lang | లిపి-భాష
The bilingual (Telugu + English) programming language.
ద్విభాషా (తెలుగు + ఇంగ్లీష్) ప్రోగ్రామింగ్ భాష.

> Copyright (c) 2025 Ram Rayavarapu. Licensed under the MIT License.
> కాపీరైట్ (c) 2025 రామ్ రాయవరపు. MIT లైసెన్స్ కింద లైసెన్స్ పొందింది.

---

## తెలుగు విద్యార్థులకు (For Telugu Students)

**మీరు ఇంగ్లీష్ తెలియకపోయినా ప్రోగ్రామింగ్ నేర్చుకోవచ్చు!**
**You can learn programming even without knowing English!**

లిపి భాషలో మీరు పూర్తిగా తెలుగులో కోడ్ రాయవచ్చు:
In Lipi you can write code entirely in Telugu:

```python
పేరు = "రాము"
వయసు = 15

చెప్పు "నమస్తే! నా పేరు: " + పేరు

యెడల వయసు > 18:
    చెప్పు "మీరు పెద్దవారు"
లేకపోతే:
    చెప్పు "మీరు చిన్నవారు"
ముగింపు
```

**ఎలా ఉపయోగించాలి (How to use):**
1. Python 3 ఇన్‌స్టాల్ చేసుకోండి (Install Python 3)
2. ఈ రిపోజిటరీ డౌన్‌లోడ్ చేసుకోండి (Download this repository)
3. `python3 src/lipi.py మీ_ప్రోగ్రామ్.lipi.py` అని రన్ చేయండి (Run the command)

**ముఖ్యమైన కీవర్డ్స్ (Important Keywords):**
- `చెప్పు` - ప్రింట్ చేయడానికి (to print output)
- `యెడల` - if (షరతు కోసం / for conditions)
- `లేకపోతే:` - else (లేకపోతే / otherwise)
- `వరకు` - while loop (పునరావృతం కోసం / for repetition)
- `ముగింపు` - end (బ్లాక్ ముగించడానికి / to close a block)

---

## Overview | పరిచయం

**English:** Lipi is a programming language designed to enable Telugu-speaking students to learn programming in their native language, while also supporting English. The unique feature of Lipi is that **Telugu and English can be used together in the same program**, making it easy to transition between languages and collaborate with others.

**తెలుగు:** లిపి అనేది తెలుగు మాట్లాడే విద్యార్థులకు వారి మాతృభాషలో ప్రోగ్రామింగ్ నేర్చుకోవడానికి రూపొందించబడిన ప్రోగ్రామింగ్ భాష. దీని ప్రత్యేకత ఏమిటంటే **ఒకే ప్రోగ్రామ్‌లో తెలుగు మరియు ఇంగ్లీష్‌ని కలిపి ఉపయోగించవచ్చు**, ఇది భాషల మధ్య సులభంగా మారడానికి మరియు ఇతరులతో కలిసి పని చేయడానికి సహాయపడుతుంది.

### Implementation | అమలు

**English:** lipi-lang **v3.0** is an **enterprise-ready interpreter** written in Python that directly executes Telugu/English code with full support for modules, object-oriented programming with inheritance, multiple database backends (SQLite, MySQL, PostgreSQL), file I/O, HTTP APIs, and comprehensive error handling. The interpreter reads `.lipi.py` files, parses Telugu and English keywords, and executes statements immediately. Future versions will introduce compilation and transpilation options for better performance.

**తెలుగు:** lipi-lang **v3.0** అనేది Python లో వ్రాయబడిన **ఎంటర్‌ప్రైజ్-సిద్ధ ఇంటర్ప్రెటర్**, ఇది మాడ్యూల్స్, వారసత్వంతో ఆబ్జెక్ట్-ఓరియెంటెడ్ ప్రోగ్రామింగ్, బహుళ డేటాబేస్ బ్యాకెండ్‌లు (SQLite, MySQL, PostgreSQL), ఫైల్ I/O, HTTP APIలు మరియు సమగ్ర ఎర్రర్ హ్యాండ్లింగ్‌కు పూర్తి మద్దతుతో తెలుగు/ఇంగ్లీష్ కోడ్‌ను నేరుగా అమలు చేస్తుంది. ఇంటర్ప్రెటర్ `.lipi.py` ఫైల్‌లను చదువుతుంది, తెలుగు మరియు ఇంగ్లీష్ కీవర్డ్‌లను పార్స్ చేస్తుంది మరియు వెంటనే స్టేట్‌మెంట్‌లను అమలు చేస్తుంది. భవిష్యత్తు వెర్షన్‌లు మెరుగైన పనితీరు కోసం కంపైలేషన్ మరియు ట్రాన్స్‌పైలేషన్ ఎంపికలను పరిచయం చేస్తాయి.

**Architecture | నిర్మాణం:** Pure Python interpreter → Future: Bytecode VM / JIT / Transpiler to Python/JS
**నిర్మాణం:** స్వచ్ఛమైన Python ఇంటర్ప్రెటర్ → భవిష్యత్తు: బైట్‌కోడ్ VM / JIT / Python/JS కి ట్రాన్స్‌పైలర్

### Runtime Note | రన్‌టైమ్ గమనిక

**English:** The lipi-lang interpreter runs as a **Python-based CLI tool**. It does **not** run directly in web browsers. The learning platform (under `learning-platform/`) is a separate browser-based HTML/JS application for interactive lessons only; actual Lipi code execution requires Python 3.

**తెలుగు:** లిపి-భాష ఇంటర్ప్రెటర్ **Python-ఆధారిత CLI సాధనం**గా రన్ అవుతుంది. ఇది వెబ్ బ్రౌజర్‌లలో నేరుగా రన్ **కాదు**. అభ్యాస వేదిక (`learning-platform/`) ఇంటరాక్టివ్ పాఠాల కోసం మాత్రమే ప్రత్యేక బ్రౌజర్-ఆధారిత HTML/JS అప్లికేషన్; అసలైన లిపి కోడ్ అమలుకు Python 3 అవసరం.

## Features | ఫీచర్లు

**Three Ways to Code | మూడు విధాలుగా కోడ్ రాయండి:**
1. **Pure Telugu | పూర్తిగా తెలుగు** - Write entirely in Telugu | పూర్తిగా తెలుగులో రాయండి
2. **Pure English | పూర్తిగా ఇంగ్లీష్** - Write entirely in English | పూర్తిగా ఇంగ్లీష్‌లో రాయండి
3. **Bilingual | ద్విభాషా** - Mix Telugu and English keywords in the same program! | ఒకే ప్రోగ్రామ్‌లో తెలుగు మరియు ఇంగ్లీష్ కీవర్డ్‌లను మిక్స్ చేయండి!

**Language Support | భాషా మద్దతు:**

### Basic Keywords | ప్రాథమిక కీవర్డ్లు

| Feature<br/>ఫీచర్ | Telugu<br/>తెలుగు | English<br/>ఇంగ్లీష్ | Meaning<br/>అర్థం |
|---------|--------|---------|---------|
| Print | `చెప్పు` | `print` | ముద్రించు / చూపించు |
| If | `యెడల` | `if` | ఒకవేళ |
| Else | `లేకపోతే:` | `else:` | లేకపోతే |
| While | `వరకు` | `while` | వరకు (లూప్) |
| For | `పునరావృతం` | `for` | పునరావృతం |
| End block | `ముగింపు` | `end` | ముగింపు |
| Function | `పనిచేయి` | `function` | ఫంక్షన్ |
| Return | `రిటర్న్` | `return` | తిరిగి ఇవ్వు |
| Try | `ప్రయత్నించు:` | `try:` | ప్రయత్నించు |
| Catch | `పట్టుకో:` | `catch:` | పట్టుకో |
| Finally | `చివరకు:` | `finally:` | చివరకు |

### v2.0 Features: File & Database Operations | v2.0 ఫీచర్లు: ఫైల్ & డేటాబేస్ కార్యకలాపాలు

| Feature<br/>ఫీచర్ | Telugu<br/>తెలుగు | English<br/>ఇంగ్లీష్ | Usage<br/>ఉపయోగం |
|---------|--------|---------|---------|
| Read File | `ఫైల్_చదువు(path)` | `file_read(path)` | ఫైల్ చదవడం |
| Write File | `ఫైల్_వ్రాయి(path, data)` | `file_write(path, data)` | ఫైల్ రాయడం |
| HTTP GET | `http_పొందు(url)` | `http_get(url)` | API డేటా పొందడం |
| HTTP POST | `http_పంపు(url, data)` | `http_post(url, data)` | API డేటా పంపడం |
| DB Connect (SQLite) | `డేటాబేస్_కనెక్ట్(path)` | `db_connect(path)` | డేటాబేస్ కనెక్ట్ |
| DB Query | `డేటాబేస్_ప్రశ్న(db, sql)` | `db_query(db, sql)` | SQL ప్రశ్నలు |

### v3.0 Enterprise Features | v3.0 ఎంటర్‌ప్రైజ్ ఫీచర్లు

| Feature<br/>ఫీచర్ | Telugu<br/>తెలుగు | English<br/>ఇంగ్లీష్ | Usage<br/>ఉపయోగం |
|---------|--------|---------|---------|
| **Module System** | | | **మాడ్యూల్ సిస్టమ్** |
| Import | `దిగుమతి func from "module"` | `import func from "module"` | మాడ్యూల్స్ ఉపయోగించడం |
| Export | `ఎగుమతి func, var` | `export func, var` | మాడ్యూల్స్ నుండి ఎగుమతి |
| **Object-Oriented Programming** | | | **ఆబ్జెక్ట్-ఓరియెంటెడ్ ప్రోగ్రామింగ్** |
| Class | `క్లాస్ Name:` | `class Name:` | క్లాస్ నిర్వచనం |
| Inheritance | `క్లాస్ Child(Parent):` | `class Child(Parent):` | వారసత్వం |
| Self | `స్వీయ` | `self` | ఇన్‌స్టెన్స్ రిఫరెన్స్ |
| **Enterprise Databases** | | | **ఎంటర్‌ప్రైజ్ డేటాబేసులు** |
| MySQL Connect | `mysql_కనెక్ట్(...)` | `mysql_connect(...)` | MySQL కనెక్షన్ |
| MySQL Query | `mysql_ప్రశ్న(...)` | `mysql_query(...)` | MySQL ప్రశ్నలు |
| PostgreSQL Connect | `postgres_కనెక్ట్(...)` | `postgres_connect(...)` | PostgreSQL కనెక్షన్ |
| PostgreSQL Query | `postgres_ప్రశ్న(...)` | `postgres_query(...)` | PostgreSQL ప్రశ్నలు |

## Quick Start | త్వరిత ప్రారంభం

### Prerequisites | ముందస్తు అవసరాలు

**English:** Python 3.8 or higher is required. The interpreter runs as a CLI tool, not in browsers.

**తెలుగు:** Python 3.8 లేదా అంతకంటే ఎక్కువ అవసరం. ఇంటర్ప్రెటర్ CLI సాధనంగా రన్ అవుతుంది, బ్రౌజర్‌లలో కాదు.

### Installation | ఇన్‌స్టాలేషన్

**English:** Clone the repository and navigate to the directory.

**తెలుగు:** రిపోజిటరీని క్లోన్ చేసి, డైరెక్టరీకి వెళ్లండి.

```bash
git clone https://github.com/ramrayavarapu/lipi-lang.git
cd lipi-lang
```

### Running Programs | ప్రోగ్రామ్‌లను రన్ చేయడం

**English:** Run programs using Python 3.

**తెలుగు:** Python 3 ఉపయోగించి ప్రోగ్రామ్‌లను రన్ చేయండి.

```bash
# Run a Telugu program | తెలుగు ప్రోగ్రామ్ రన్ చేయండి
python3 src/lipi.py examples/hello.lipi.py

# Run an English program | ఇంగ్లీష్ ప్రోగ్రామ్ రన్ చేయండి
python3 src/lipi.py examples/english.lipi.py

# Run a bilingual program | ద్విభాషా ప్రోగ్రామ్ రన్ చేయండి
python3 src/lipi.py examples/bilingual.lipi.py

# Run v2.0 features demo | v2.0 ఫీచర్ల డెమో రన్ చేయండి
python3 src/lipi.py examples/v2.0_features.lipi.py

# Start the interactive REPL | ఇంటరాక్టివ్ REPL ప్రారంభించండి
python3 src/lipi.py

# Run with Telugu error messages (v3.0) | తెలుగు దోష సందేశాలతో రన్ చేయండి (v3.0)
python3 src/lipi.py examples/telugu.lipi.py --lang te

# View help | సహాయం చూడండి
python3 src/lipi.py --help
```

### Interactive Learning Platform | ఇంటరాక్టివ్ అభ్యాస వేదిక

**English:** A separate browser-based learning platform with interactive lessons, XP progression, visual demonstrations, and professional deployment options. This platform teaches Lipi concepts visually but does not execute Lipi code natively; actual code execution requires the Python interpreter above.

**తెలుగు:** ఇంటరాక్టివ్ పాఠాలు, XP పురోగతి మరియు దృశ్య ప్రదర్శనలతో ప్రత్యేక బ్రౌజర్-ఆధారిత అభ్యాస వేదిక. ఈ వేదిక లిపి భావనలను దృశ్యపరంగా బోధిస్తుంది కానీ లిపి కోడ్‌ను స్థానికంగా అమలు చేయదు; అసలైన కోడ్ అమలుకు పైన ఉన్న Python ఇంటర్ప్రెటర్ అవసరం.

**Quick Start | త్వరిత ప్రారంభం:**
```bash
# Open the learning platform | అభ్యాస వేదికను తెరవండి
cd learning-platform
# Open index.html in your web browser | మీ వెబ్ బ్రౌజర్‌లో index.html తెరవండి
```

**Core Features | ప్రధాన ఫీచర్లు:**
- 3 interactive lessons (Variables, Conditionals, Loops) | 3 ఇంటరాక్టివ్ పాఠాలు (వేరియబుల్స్, షరతులు, లూప్స్)
- Bilingual content (Telugu + English) | ద్విభాషా కంటెంట్ (తెలుగు + ఇంగ్లీష్)
- XP system and level progression | XP సిస్టమ్ మరియు స్థాయి పురోగతి
- Visual demonstrations for each concept | ప్రతి భావనకు దృశ్య ప్రదర్శనలు
- Practice editor to try code in browser | బ్రౌజర్‌లో కోడ్ ప్రయత్నించడానికి ప్రాక్టీస్ ఎడిటర్
- Progress tracking with LocalStorage | LocalStorage తో పురోగతి ట్రాకింగ్
- No installation needed - runs in browser! | ఇన్‌స్టాలేషన్ అవసరం లేదు - బ్రౌజర్‌లో రన్ అవుతుంది!

**Production-Ready Features | ఉత్పత్తి-సిద్ధ ఫీచర్లు:**
- **Dark Mode** - Automatic & manual theme switching | **డార్క్ మోడ్** - ఆటోమేటిక్ & మాన్యువల్ థీమ్ మార్పిడి
- **Full Accessibility** - WCAG compliant with ARIA labels | **పూర్తి ప్రాప్యత** - ARIA లేబుల్స్‌తో WCAG అనుకూలత
- **SEO Optimized** - Complete meta tags for discoverability | **SEO ఆప్టిమైజ్డ్** - కనుగొనడానికి పూర్తి మెటా ట్యాగ్‌లు
- **Error Handling** - Comprehensive validation & sanitization | **ఎర్రర్ హ్యాండ్లింగ్** - సమగ్ర ధ్రువీకరణ & శుద్ధీకరణ
- **Responsive Design** - Works on desktop, tablet, mobile | **రెస్పాన్సివ్ డిజైన్** - డెస్క్‌టాప్, టాబ్లెట్, మొబైల్‌లో పనిచేస్తుంది
- **Easy Deployment** - GitHub Pages, Netlify, Vercel ready | **సులభ విస్తరణ** - GitHub Pages, Netlify, Vercel సిద్ధం

**Documentation | డాక్యుమెంటేషన్:**
- [Platform Overview & Setup](learning-platform/README.md) - Complete feature guide | వేదిక అవలోకనం & సెటప్ - పూర్తి ఫీచర్ గైడ్
- [Lipi-Lang Quick Reference](learning-platform/QUICK_REFERENCE.md) - All keywords and syntax | లిపి-భాష త్వరిత సూచన - అన్ని కీవర్డ్‌లు మరియు సింటాక్స్
- [Lesson Creation Guide](learning-platform/LESSON_TEMPLATE.md) - Add your own lessons | పాఠ సృష్టి గైడ్ - మీ స్వంత పాఠాలను జోడించండి
- [Deployment Strategy](learning-platform/DEPLOYMENT_GUIDE.md) - Organizational rollout guide | విస్తరణ వ్యూహం - సంస్థాగత రోల్అవుట్ గైడ్

**Browser Compatibility | బ్రౌజర్ అనుకూలత:**
- Chrome 90+ | Firefox 88+ | Edge 90+ | Safari 14+

## Examples | ఉదాహరణలు

### Telugu Example | తెలుగు ఉదాహరణ
```python
పేరు = "రామ్"
వయసు = 20

చెప్పు "నమస్తే!"
చెప్పు "పేరు: " + పేరు

యెడల వయసు > 18:
    చెప్పు "అడల్ట్"
లేకపోతే:
    చెప్పు "యంగ్"
ముగింపు
```

### English Example | ఇంగ్లీష్ ఉదాహరణ
```python
name = "John"
age = 20

print "Hello!"
print "Name: " + name

if age > 18:
    print "Adult"
else:
    print "Young"
end
```

### Bilingual Example (Telugu + English Together!) | ద్విభాషా ఉదాహరణ (తెలుగు + ఇంగ్లీష్ కలిపి!)
```python
# Mix Telugu and English freely! | తెలుగు మరియు ఇంగ్లీష్ స్వేచ్ఛగా మిక్స్ చేయండి!
పేరు = "రామ్"
name = "Ram"

చెప్పు "నమస్తే!"
print "Hello!"

# Telugu if with English print inside | తెలుగు if లో ఇంగ్లీష్ print
యెడల వయసు > 18:
    print "Adult"
ముగింపు

# English while with Telugu print inside | ఇంగ్లీష్ while లో తెలుగు print
while count < 5:
    చెప్పు "Count: " + count
    count = count + 1
end
```

## Language Syntax | భాషా సింటాక్స్

### Variables | వేరియబుల్స్

**English:** Variables can be in Telugu or English.

**తెలుగు:** వేరియబుల్స్ తెలుగు లేదా ఇంగ్లీష్‌లో ఉండవచ్చు.

```python
పేరు = "value"    # Telugu variable | తెలుగు వేరియబుల్
name = "value"     # English variable | ఇంగ్లీష్ వేరియబుల్
వయసు = 25         # Number | సంఖ్య
```

### Print Statements | ప్రింట్ స్టేట్‌మెంట్స్

**English:** Use `చెప్పు` or `print` to display output.

**తెలుగు:** అవుట్‌పుట్ చూపించడానికి `చెప్పు` లేదా `print` ఉపయోగించండి.

```python
చెప్పు "నమస్తే"     # Telugu print | తెలుగు ప్రింట్
print "Hello"        # English print | ఇంగ్లీష్ ప్రింట్
```

### Conditionals | షరతులు (If/Else)

**English:** Use if/else blocks to make decisions.

**తెలుగు:** నిర్ణయాలు తీసుకోవడానికి if/else బ్లాక్‌లను ఉపయోగించండి.

```python
# Telugu | తెలుగు
యెడల condition:
    # statements | స్టేట్‌మెంట్స్
లేకపోతే:
    # statements | స్టేట్‌మెంట్స్
ముగింపు

# English | ఇంగ్లీష్
if condition:
    # statements | స్టేట్‌మెంట్స్
else:
    # statements | స్టేట్‌మెంట్స్
end
```

### Loops | లూప్స్ (పునరావృతం)

**English:** Repeat code using while loops.

**తెలుగు:** while లూప్స్ ఉపయోగించి కోడ్‌ను పునరావృతం చేయండి.

```python
# Telugu | తెలుగు
వరకు condition:
    # statements | స్టేట్‌మెంట్స్
ముగింపు

# English | ఇంగ్లీష్
while condition:
    # statements | స్టేట్‌మెంట్స్
end
```

## Why Bilingual? | ద్విభాషా ఎందుకు?

**English:**
1. **Accessibility** - Telugu students can learn programming in their native language
2. **Transition** - Easy to transition to English-based programming languages
3. **Collaboration** - Mix languages based on what makes sense for your team
4. **Learning** - Understand programming concepts first, language second

**తెలుగు:**
1. **అందుబాటు** - తెలుగు విద్యార్థులు తమ మాతృభాషలో ప్రోగ్రామింగ్ నేర్చుకోగలరు
2. **మార్పు** - ఇంగ్లీష్ ఆధారిత ప్రోగ్రామింగ్ భాషలకు సులభంగా మారవచ్చు
3. **సహకారం** - మీ టీమ్‌కు అర్థమయ్యే విధంగా భాషలను మిక్స్ చేయండి
4. **నేర్చుకోవడం** - మొదట ప్రోగ్రామింగ్ కాన్సెప్ట్‌లను అర్థం చేసుకోండి, భాష రెండవది

## Current Version | ప్రస్తుత వెర్షన్

**English:** **v3.0** - Enterprise-ready with modules, OOP, multi-database support, file I/O, HTTP/API, and bilingual error messages.

**తెలుగు:** **v3.0** - మాడ్యూల్స్, OOP, మల్టీ-డేటాబేస్ మద్దతు, ఫైల్ I/O, HTTP/API మరియు ద్విభాషా దోష సందేశాలతో ఎంటర్‌ప్రైజ్-సిద్ధం.

See `examples/` for complete demonstrations! | పూర్తి ప్రదర్శనల కోసం `examples/` చూడండి!

## Roadmap | రోడ్‌మ్యాప్

**Completed features | పూర్తయిన ఫీచర్లు (v1.0-v3.0):**

- [x] Functions/procedures | ఫంక్షన్లు/ప్రొసీజర్లు (v1.0)
- [x] Arrays & dictionaries | అర్రేలు & డిక్షనరీలు (v1.0)
- [x] Error handling (try/catch) | ఎర్రర్ హ్యాండ్లింగ్ (v1.0)
- [x] File I/O | ఫైల్ ఇన్‌పుట్/అవుట్‌పుట్ (v2.0)
- [x] Database connectivity (SQLite) | డేటాబేస్ కనెక్టివిటీ (v2.0)
- [x] HTTP/API support | HTTP/API మద్దతు (v2.0)
- [x] Module import system | మాడ్యూల్ ఇంపోర్ట్ సిస్టమ్ (v3.0)
- [x] OOP with inheritance | వారసత్వంతో OOP (v3.0)
- [x] MySQL & PostgreSQL support | MySQL & PostgreSQL మద్దతు (v3.0)
- [x] Bilingual error messages | ద్విభాషా దోష సందేశాలు (v3.0)

**Future features | భవిష్యత్ ఫీచర్లు (v4.0+):**

- [ ] Package manager | ప్యాకేజ్ మేనేజర్
- [ ] Native compilation | నేటివ్ కంపైలేషన్
- [ ] Browser-native execution (Pyodide/WASM) | బ్రౌజర్-స్థానిక అమలు
- [ ] Execution timeout and memory limits | అమలు సమయ పరిమితి మరియు మెమరీ పరిమితులు
- [ ] More Indian language support (Hindi, Tamil, etc.) | మరిన్ని భారతీయ భాషల మద్దతు (హిందీ, తమిళం, మొదలైనవి)

## Security | భద్రత

**English:** This project includes comprehensive security testing to prevent vulnerabilities:
- Automated test suite with security checks
- Automated security scanner
- GitHub Actions CI/CD pipeline
- Pre-commit hooks
- Sandboxed expression evaluation (no `eval()`/`exec()`)
- Path traversal prevention in module imports
- Parameterized database queries to prevent SQL injection
- Python module whitelist to prevent arbitrary imports
- Dunder method access blocked

All code is tested before merge. See [SECURITY.md](docs/SECURITY.md) for details.

**తెలుగు:** ఈ ప్రాజెక్ట్ దుర్బలత్వాలను నిరోధించడానికి సమగ్ర భద్రతా పరీక్షను కలిగి ఉంది:
- భద్రతా తనిఖీలతో ఆటోమేటెడ్ టెస్ట్ సూట్
- ఆటోమేటెడ్ సెక్యూరిటీ స్కానర్
- GitHub Actions CI/CD పైప్‌లైన్
- ప్రీ-కమిట్ హుక్స్
- శాండ్‌బాక్స్‌డ్ ఎక్స్‌ప్రెషన్ మూల్యాంకనం (`eval()`/`exec()` లేదు)
- మాడ్యూల్ ఇంపోర్ట్‌లలో పాత్ ట్రావర్సల్ నివారణ
- SQL ఇంజెక్షన్ నిరోధించడానికి పారామీటరైజ్డ్ డేటాబేస్ ప్రశ్నలు
- ఏకపక్ష ఇంపోర్ట్‌లను నిరోధించడానికి Python మాడ్యూల్ వైట్‌లిస్ట్
- డండర్ మెథడ్ యాక్సెస్ బ్లాక్ చేయబడింది

అన్ని కోడ్ మెర్జ్ కు ముందు పరీక్షించబడుతుంది. వివరాల కోసం [SECURITY.md](docs/SECURITY.md) చూడండి.

### Known Limitations | తెలిసిన పరిమితులు

**English:** The following are known gaps being tracked for future improvement:
- No execution timeout mechanism (infinite loops possible)
- No memory usage limits
- No recursion depth limits
- SQLite `db_query()` does not use parameterized queries (MySQL/PostgreSQL do)
- `file_read()`/`file_write()` lack path sandboxing beyond module imports
- HTTP functions (`http_get()`/`http_post()`) allow unrestricted URL access

**తెలుగు:** భవిష్యత్ మెరుగుదల కోసం ట్రాక్ చేయబడుతున్న తెలిసిన అంతరాలు:
- అమలు సమయ పరిమితి యంత్రాంగం లేదు (అనంత లూప్‌లు సాధ్యం)
- మెమరీ వినియోగ పరిమితులు లేవు
- రికర్షన్ లోతు పరిమితులు లేవు
- SQLite `db_query()` పారామీటరైజ్డ్ ప్రశ్నలను ఉపయోగించదు (MySQL/PostgreSQL ఉపయోగిస్తాయి)
- `file_read()`/`file_write()` మాడ్యూల్ ఇంపోర్ట్‌ల మించి పాత్ శాండ్‌బాక్సింగ్ లేదు
- HTTP ఫంక్షన్లు (`http_get()`/`http_post()`) అపరిమిత URL యాక్సెస్‌ను అనుమతిస్తాయి

## Contributing | సహకారం

**English:** We welcome contributions! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

**Important:** All contributions must pass security tests.

**తెలుగు:** మేము సహకారాన్ని స్వాగతిస్తున్నాము! దయచేసి మార్గదర్శకాల కోసం [CONTRIBUTING.md](docs/CONTRIBUTING.md) చదవండి.

**ముఖ్యమైనది:** అన్ని సహకారాలు భద్రతా పరీక్షలలో ఉత్తీర్ణత సాధించాలి.

## License | లైసెన్స్

**English:** This project is licensed under the [MIT License](LICENSE). Copyright (c) 2025 Ram Rayavarapu. All rights reserved under the terms of the MIT License. You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, provided the copyright notice and permission notice are included in all copies or substantial portions of the software.

**తెలుగు:** ఈ ప్రాజెక్ట్ [MIT లైసెన్స్](LICENSE) కింద లైసెన్స్ పొందింది. కాపీరైట్ (c) 2025 రామ్ రాయవరపు. MIT లైసెన్స్ నిబంధనల ప్రకారం అన్ని హక్కులు రిజర్వ్ చేయబడ్డాయి. కాపీరైట్ నోటీసు మరియు అనుమతి నోటీసు సాఫ్ట్‌వేర్ యొక్క అన్ని కాపీలలో లేదా గణనీయ భాగాలలో చేర్చబడిన పక్షంలో, ఈ సాఫ్ట్‌వేర్‌ను ఉపయోగించడానికి, కాపీ చేయడానికి, సవరించడానికి, విలీనం చేయడానికి, ప్రచురించడానికి, పంపిణీ చేయడానికి, సబ్‌లైసెన్స్ ఇవ్వడానికి మరియు/లేదా అమ్మడానికి మీకు స్వేచ్ఛ ఉంది.
