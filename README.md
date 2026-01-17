# lipi-lang | లిపి-భాష
The bilingual (Telugu + English) programming language.
ద్విభాషా (తెలుగు + ఇంగ్లీష్) ప్రోగ్రామింగ్ భాష.

---

## 🎯 తెలుగు విద్యార్థులకు (For Telugu Students)

**మీరు ఇంగ్లీష్ తెలియకపోయినా ప్రోగ్రామింగ్ నేర్చుకోవచ్చు!**

లిపి భాషలో మీరు పూర్తిగా తెలుగులో కోడ్ రాయవచ్చు:

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

**ఎలా ఉపయోగించాలి:**
1. Python 3 ఇన్‌స్టాల్ చేసుకోండి
2. ఈ రిపోజిటరీ డౌన్‌లోడ్ చేసుకోండి
3. `python3 src/lipi.py మీ_ప్రోగ్రామ్.lipi.py` అని రన్ చేయండి

**ముఖ్యమైన కీవర్డ్స్:**
- `చెప్పు` - ప్రింట్ చేయడానికి (output చూపించడానికి)
- `యెడల` - if (షరతు కోసం)
- `లేకపోతే:` - else (లేకపోతే)
- `వరకు` - while loop (పునరావృతం కోసం)
- `ముగింపు` - end (బ్లాక్ ముగించడానికి)

---

## Overview | పరిచయం

**English:** Lipi is a programming language designed to enable Telugu-speaking students to learn programming in their native language, while also supporting English. The unique feature of Lipi is that **Telugu and English can be used together in the same program**, making it easy to transition between languages and collaborate with others.

**తెలుగు:** లిపి అనేది తెలుగు మాట్లాడే విద్యార్థులకు వారి మాతృభాషలో ప్రోగ్రామింగ్ నేర్చుకోవడానికి రూపొందించబడిన ప్రోగ్రామింగ్ భాష. దీని ప్రత్యేకత ఏమిటంటే **ఒకే ప్రోగ్రామ్‌లో తెలుగు మరియు ఇంగ్లీష్‌ని కలిపి ఉపయోగించవచ్చు**, ఇది భాషల మధ్య సులభంగా మారడానికి మరియు ఇతరులతో కలిసి పని చేయడానికి సహాయపడుతుంది.

### Implementation | అమలు

**English:** lipi-lang **v3.0** is an **enterprise-ready interpreter** written in Python that directly executes Telugu/English code with full support for modules, object-oriented programming with inheritance, multiple database backends (SQLite, MySQL, PostgreSQL), file I/O, HTTP APIs, and comprehensive error handling. The interpreter reads `.lipi.py` files, parses Telugu and English keywords, and executes statements immediately. Future versions will introduce compilation and transpilation options for better performance.

**తెలుగు:** lipi-lang **v3.0** అనేది Python లో వ్రాయబడిన **ఎంటర్‌ప్రైజ్-సిద్ధ ఇంటర్ప్రెటర్**, ఇది మాడ్యూల్స్, వారసత్వంతో ఆబ్జెక్ట్-ఓరియెంటెడ్ ప్రోగ్రామింగ్, బహుళ డేటాబేస్ బ్యాకెండ్‌లు (SQLite, MySQL, PostgreSQL), ఫైల్ I/O, HTTP APIలు మరియు సమగ్ర ఎర్రర్ హ్యాండ్లింగ్‌కు పూర్తి మద్దతుతో తెలుగు/ఇంగ్లీష్ కోడ్‌ను నేరుగా అమలు చేస్తుంది. ఇంటర్ప్రెటర్ `.lipi.py` ఫైల్‌లను చదువుతుంది, తెలుగు మరియు ఇంగ్లీష్ కీవర్డ్‌లను పార్స్ చేస్తుంది మరియు వెంటనే స్టేట్‌మెంట్‌లను అమలు చేస్తుంది. భవిష్యత్తు వెర్షన్‌లు మెరుగైన పనితీరు కోసం కంపైలేషన్ మరియు ట్రాన్స్‌పైలేషన్ ఎంపికలను పరిచయం చేస్తాయి.

**Architecture:** Pure Python interpreter → Future: Bytecode VM / JIT / Transpiler to Python/JS

## Features | ఫీచర్లు

✅ **Three Ways to Code: | మూడు విధాలుగా కోడ్ రాయండి:**
1. **Pure Telugu | పూర్తిగా తెలుగు** - Write entirely in Telugu | పూర్తిగా తెలుగులో రాయండి
2. **Pure English | పూర్తిగా ఇంగ్లీష్** - Write entirely in English | పూర్తిగా ఇంగ్లీష్‌లో రాయండి
3. **Bilingual | ద్విభాషా** - Mix Telugu and English keywords in the same program! | ఒకే ప్రోగ్రామ్‌లో తెలుగు మరియు ఇంగ్లీష్ కీవర్డ్‌లను మిక్స్ చేయండి!

✅ **Language Support: | భాషా మద్దతు:**

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

### ✨ NEW in v3.0: Enterprise Features | v3.0లో కొత్తది: ఎంటర్‌ప్రైజ్ ఫీచర్లు

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

### 🎓 Interactive Learning Platform | ఇంటరాక్టివ్ అభ్యాస వేదిక

**NEW!** Learn lipi-lang through our interactive, gamified learning platform!

**English:** We've created a complete learning platform with interactive lessons, XP progression, and visual demonstrations. Perfect for new programmers!

**తెలుగు:** మేము ఇంటరాక్టివ్ పాఠాలు, XP పురోగతి మరియు దృశ్య ప్రదర్శనలతో పూర్తి అభ్యాస వేదికను సృష్టించాము. కొత్త ప్రోగ్రామర్లకు అనువైనది!

**Quick Start:**
```bash
# Open the learning platform
# అభ్యాస వేదికను తెరవండి
cd learning-platform
# Open index.html in your web browser
# మీ వెబ్ బ్రౌజర్‌లో index.html తెరవండి
```

**Features:**
- ✅ 3 interactive lessons (Variables, Conditionals, Loops)
- ✅ Bilingual content (Telugu + English)
- ✅ XP system and level progression
- ✅ Visual demonstrations for each concept
- ✅ Practice editor to try code in browser
- ✅ Progress tracking with LocalStorage
- ✅ No installation needed - runs in browser!

📖 **See:** `learning-platform/README.md` for complete documentation

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
# Mix Telugu and English freely!
పేరు = "రామ్"
name = "Ram"

చెప్పు "నమస్తే!"
print "Hello!"

# Telugu if with English print inside
యెడల వయసు > 18:
    print "Adult"
ముగింపు

# English while with Telugu print inside
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

**v2.0** - Production-ready with File I/O, HTTP/API, and Database connectivity
**v2.0** - ఫైల్ I/O, HTTP/API మరియు డేటాబేస్ కనెక్టివిటీతో ఉత్పత్తి-సిద్ధం

See `examples/v2.0_features.lipi.py` for complete demonstrations!

## Roadmap | రోడ్‌మ్యాప్

**English:** Completed features (v1.0-v2.0):

**తెలుగు:** పూర్తయిన ఫీచర్లు (v1.0-v2.0):

- [x] Functions/procedures | ఫంక్షన్లు/ప్రొసీజర్లు ✅ v1.0
- [x] Arrays & dictionaries | అర్రేలు & డిక్షనరీలు ✅ v1.0
- [x] Error handling (try/catch) | ఎర్రర్ హ్యాండ్లింగ్ ✅ v1.0
- [x] File I/O | ఫైల్ ఇన్‌పుట్/అవుట్‌పుట్ ✅ v2.0
- [x] Database connectivity (SQLite) | డేటాబేస్ కనెక్టివిటీ ✅ v2.0
- [x] HTTP/API support | HTTP/API మద్దతు ✅ v2.0

**English:** Future features (v3.0+):

**తెలుగు:** భవిష్యత్ ఫీచర్లు (v3.0+):

- [ ] Full module import system | పూర్తి మాడ్యూల్ ఇంపోర్ట్ సిస్టమ్
- [ ] Advanced OOP (classes, inheritance) | అధునాతన OOP
- [ ] Multi-database support (MySQL, PostgreSQL) | మల్టీ-డేటాబేస్ మద్దతు
- [ ] Package manager | ప్యాకేజ్ మేనేజర్
- [ ] Native compilation | నేటివ్ కంపైలేషన్
- [ ] More Indian language support (Hindi, Tamil, etc.) | మరిన్ని భారతీయ భాషల మద్దతు (హిందీ, తమిళం, మొదలైనవి)

## Security | భద్రత

**English:** This project includes comprehensive security testing to prevent vulnerabilities:
- ✅ 39 automated tests including security checks
- ✅ Automated security scanner
- ✅ GitHub Actions CI/CD pipeline
- ✅ Pre-commit hooks
- ✅ No code execution vulnerabilities

All code is tested before merge. See [SECURITY.md](docs/SECURITY.md) for details.

**తెలుగు:** ఈ ప్రాజెక్ట్ దుర్బలత్వాలను నిరోధించడానికి సమగ్ర భద్రతా పరీక్షను కలిగి ఉంది:
- ✅ 39 ఆటోమేటెడ్ టెస్ట్‌లు భద్రతా తనిఖీలతో సహా
- ✅ ఆటోమేటెడ్ సెక్యూరిటీ స్కానర్
- ✅ GitHub Actions CI/CD పైప్‌లైన్
- ✅ ప్రీ-కమిట్ హుక్స్
- ✅ కోడ్ ఎగ్జిక్యూషన్ దుర్బలత్వాలు లేవు

## Contributing | సహకారం

**English:** We welcome contributions! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

**Important:** All contributions must pass security tests.

**తెలుగు:** మేము సహకారాన్ని స్వాగతిస్తున్నాము! దయచేసి మార్గదర్శకాల కోసం [CONTRIBUTING.md](docs/CONTRIBUTING.md) చదవండి.

**ముఖ్యమైనది:** అన్ని సహకారాలు భద్రతా పరీక్షలలో ఉత్తీర్ణత సాధించాలి.

## License | లైసెన్స్

MIT License
