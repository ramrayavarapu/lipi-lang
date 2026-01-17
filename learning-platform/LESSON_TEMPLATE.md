# Lesson Template Guide | పాఠం టెంప్లేట్ గైడ్

Complete guide for creating new lessons in the Lipi-Lang Learning Platform.

## 📋 Overview | పరిచయం

This guide shows you how to add new lessons to the learning platform. Each lesson is a JavaScript object added to the `lessons` array in `lessons.js`.

## 🎯 Lesson Structure | పాఠం నిర్మాణం

Every lesson must have these fields:

```javascript
{
    id: 0,                    // Unique lesson number (0, 1, 2, ...)
    title: "",                // English title
    titleTe: "",              // Telugu title
    description: "",          // English description
    descriptionTe: "",        // Telugu description
    xp: 0,                    // XP points awarded
    objectives: [],           // Learning objectives (array)
    visual: "",               // HTML for visual demo
    codeTelugu: "",           // Telugu code example
    codeEnglish: "",          // English code example
    practiceTemplate: "",     // Starter code for practice
    transpilations: {}        // Python, JS, C# equivalents
}
```

## 📝 Complete Template | పూర్తి టెంప్లేట్

Copy this template to create a new lesson:

```javascript
{
    // LESSON IDENTIFICATION
    id: 3,  // Next available number (0, 1, 2 are used)

    // TITLES
    title: "Your Lesson Title in English",
    titleTe: "తెలుగులో మీ పాఠం శీర్షిక",

    // DESCRIPTIONS
    description: "Brief explanation of what students will learn in this lesson. Keep it concise but informative.",
    descriptionTe: "విద్యార్థులు ఈ పాఠంలో ఏమి నేర్చుకుంటారో క్లుప్త వివరణ. దీన్ని సంక్షిప్తంగా కానీ సమాచారంగా ఉంచండి.",

    // XP POINTS
    xp: 25,  // Increase for more advanced lessons (10, 15, 20, 25, 30...)

    // LEARNING OBJECTIVES (Bilingual bullet points)
    objectives: [
        "First objective in English | మొదటి లక్ష్యం తెలుగులో",
        "Second objective in English | రెండవ లక్ష్యం తెలుగులో",
        "Third objective in English | మూడవ లక్ష్యం తెలుగులో",
        "Fourth objective in English | నాలుగవ లక్ష్యం తెలుగులో"
    ],

    // VISUAL DEMONSTRATION (HTML/CSS)
    visual: `
        <div style="text-align: center;">
            <h4>Visual Title | దృశ్య శీర్షిక</h4>
            <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
                <!-- Add your visual demonstration HTML here -->
                <div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">
                    Your visual content
                </div>
            </div>
            <p style="margin-top: 20px; color: #666;">
                Explanation in English<br>
                తెలుగులో వివరణ
            </p>
        </div>
    `,

    // TELUGU CODE EXAMPLE
    codeTelugu: `# తెలుగు కోడ్ ఉదాహరణ
# Write your Telugu lipi-lang code here
పేరు = "ఉదాహరణ"
చెప్పు పేరు`,

    // ENGLISH CODE EXAMPLE
    codeEnglish: `# English code example
# Write your English lipi-lang code here
name = "example"
print name`,

    // PRACTICE TEMPLATE
    practiceTemplate: `# Try it yourself! | మీరే ప్రయత్నించండి!
# Starter code with comments
పేరు = "మీ కోడ్ ఇక్కడ"`,

    // TRANSPILATIONS TO OTHER LANGUAGES
    transpilations: {
        python: `# Python equivalent
# Show how this would look in Python
name = "example"
print(name)`,

        javascript: `// JavaScript equivalent
// Show how this would look in JavaScript
const name = "example";
console.log(name);`,

        csharp: `// C# equivalent
// Show how this would look in C#
string name = "example";
Console.WriteLine(name);`
    }
}
```

## 🎨 Visual Demonstration Tips | దృశ్య ప్రదర్శన చిట్కాలు

The `visual` field should contain HTML that illustrates the concept. Use:

### Example 1: Box Diagram
```javascript
visual: `
    <div style="text-align: center;">
        <h4>Concept Name | భావన పేరు</h4>
        <div style="display: flex; justify-content: center; gap: 20px;">
            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; border: 2px solid #667eea;">
                <strong>Label</strong><br>
                <span style="font-size: 24px;">📦</span><br>
                Content
            </div>
        </div>
    </div>
`
```

### Example 2: Flow Diagram
```javascript
visual: `
    <div style="text-align: center;">
        <div style="background: #fff3e0; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <strong>Start Point</strong>
        </div>
        <div style="font-size: 30px;">⬇️</div>
        <div style="background: #e8f5e9; padding: 15px; border-radius: 10px;">
            <strong>End Point</strong>
        </div>
    </div>
`
```

### Example 3: Comparison Table
```javascript
visual: `
    <div style="max-width: 600px; margin: 0 auto;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f5f5f5;">
                <th style="padding: 10px; border: 1px solid #ddd;">Telugu</th>
                <th style="padding: 10px; border: 1px solid #ddd;">English</th>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">తెలుగు</td>
                <td style="padding: 10px; border: 1px solid #ddd;">English</td>
            </tr>
        </table>
    </div>
`
```

## 💻 Code Example Guidelines | కోడ్ ఉదాహరణ మార్గదర్శకాలు

### Best Practices for Code Examples:

1. **Keep it Simple**: Focus on one concept per lesson
2. **Use Comments**: Explain what each part does
3. **Show Real Use Cases**: Use practical examples
4. **Be Consistent**: Use similar variable names in Telugu and English versions

### Good Example:
```javascript
codeTelugu: `# ఫంక్షన్ ఉదాహరణ
పనిచేయి శుభాకాంక్షలు(పేరు):
    చెప్పు "నమస్తే, " + పేరు + "!"
ముగింపు

శుభాకాంక్షలు("రాము")`,

codeEnglish: `# Function example
function greet(name):
    print "Hello, " + name + "!"
end

greet("Ramu")`
```

### Avoid:
```javascript
// Too complex for beginners
codeTelugu: `పనిచేయి సంక్లిష్టం(a, b, c, d):
    ఒకవేళ a > b:
        వరకు c < d:
            ...
        ముగింపు
    ముగింపు
ముగింపు`
```

## 🎓 Complete Real Example | పూర్తి నిజమైన ఉదాహరణ

Here's a complete lesson for teaching functions:

```javascript
{
    id: 3,
    title: "Functions & Procedures",
    titleTe: "ఫంక్షన్లు మరియు ప్రొసీజర్లు",
    description: "Learn how to create reusable blocks of code with functions. Understand parameters, return values, and how to organize your code better.",
    descriptionTe: "ఫంక్షన్లతో పునర్వినియోగపరచదగిన కోడ్ బ్లాక్‌లను ఎలా సృష్టించాలో నేర్చుకోండి. పారామితులు, రిటర్న్ విలువలు మరియు మీ కోడ్‌ను మెరుగ్గా ఎలా నిర్వహించాలో అర్థం చేసుకోండి.",
    xp: 25,
    objectives: [
        "Understand what functions are | ఫంక్షన్లు అంటే ఏమిటో అర్థం చేసుకోవడం",
        "Create functions with పనిచేయి/function | పనిచేయి/function తో ఫంక్షన్లు సృష్టించడం",
        "Use parameters and return values | పారామితులు మరియు రిటర్న్ విలువలను ఉపయోగించడం",
        "Call functions and use results | ఫంక్షన్లను కాల్ చేయడం మరియు ఫలితాలను ఉపయోగించడం"
    ],
    visual: `
        <div style="text-align: center;">
            <h4>Function Concept | ఫంక్షన్ భావన</h4>
            <div style="max-width: 500px; margin: 20px auto;">
                <div style="background: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <strong>Input | ఇన్‌పుట్:</strong> పారామితులు (Parameters)
                </div>
                <div style="font-size: 30px; margin: 10px 0;">⬇️</div>
                <div style="background: #fff3e0; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 3px solid #ff9800;">
                    <strong>Function Body | ఫంక్షన్ బాడీ</strong><br>
                    Process data<br>
                    డేటాను ప్రాసెస్ చేయండి
                </div>
                <div style="font-size: 30px; margin: 10px 0;">⬇️</div>
                <div style="background: #e8f5e9; padding: 15px; border-radius: 10px;">
                    <strong>Output | అవుట్‌పుట్:</strong> రిటర్న్ విలువ (Return Value)
                </div>
            </div>
            <p style="margin-top: 20px; color: #666;">
                Functions are reusable code blocks that take input and produce output<br>
                ఫంక్షన్లు పునర్వినియోగపరచదగిన కోడ్ బ్లాక్‌లు ఇన్‌పుట్ తీసుకొని అవుట్‌పుట్ ఉత్పత్తి చేస్తాయి
            </p>
        </div>
    `,
    codeTelugu: `# ఫంక్షన్ నిర్వచనం
పనిచేయి కూడిక(సంఖ్య1, సంఖ్య2):
    మొత్తం = సంఖ్య1 + సంఖ్య2
    రిటర్న్ మొత్తం
ముగింపు

# ఫంక్షన్ ఉపయోగం
ఫలితం = కూడిక(10, 5)
చెప్పు "మొత్తం: " + ఫలితం`,
    codeEnglish: `# Function definition
function add(num1, num2):
    total = num1 + num2
    return total
end

# Using the function
result = add(10, 5)
print "Total: " + result`,
    practiceTemplate: `# Create your own function! | మీ స్వంత ఫంక్షన్ సృష్టించండి!

పనిచేయి గుణకారం(a, b):
    # Add your code here
    # మీ కోడ్ ఇక్కడ జోడించండి
ముగింపు

# Test your function
ఫలితం = గుణకారం(4, 5)
చెప్పు ఫలితం`,
    transpilations: {
        python: `# Python equivalent
def add(num1, num2):
    total = num1 + num2
    return total

result = add(10, 5)
print(f"Total: {result}")`,
        javascript: `// JavaScript equivalent
function add(num1, num2) {
    const total = num1 + num2;
    return total;
}

const result = add(10, 5);
console.log("Total: " + result);`,
        csharp: `// C# equivalent
int Add(int num1, int num2) {
    int total = num1 + num2;
    return total;
}

int result = Add(10, 5);
Console.WriteLine("Total: " + result);`
    }
}
```

## 📍 Where to Add Your Lesson | మీ పాఠాన్ని ఎక్కడ జోడించాలి

1. Open `lessons.js`
2. Find the `lessons` array
3. Add your lesson object at the end (before the closing `]`)
4. Make sure to add a comma after the previous lesson

```javascript
const lessons = [
    { /* Lesson 0 */ },
    { /* Lesson 1 */ },
    { /* Lesson 2 */ },
    { /* YOUR NEW LESSON HERE */ }  // Don't forget comma before this!
];
```

## 🎯 XP Point Guidelines | XP పాయింట్ల మార్గదర్శకాలు

Assign XP based on lesson difficulty:

- **10 XP**: Basic concepts (variables, print)
- **15 XP**: Intermediate concepts (conditionals, operators)
- **20 XP**: Advanced basics (loops, arrays)
- **25 XP**: Complex topics (functions, error handling)
- **30+ XP**: Advanced topics (OOP, databases)

## ✅ Checklist Before Publishing | ప్రచురించే ముందు తనిఖీ జాబితా

- [ ] All required fields filled
- [ ] Telugu and English content provided
- [ ] XP points appropriate for difficulty
- [ ] Visual demonstration is clear and helpful
- [ ] Code examples work and are tested
- [ ] Transpilations are accurate
- [ ] Practice template provides good starting point
- [ ] Objectives clearly state learning goals
- [ ] No syntax errors in JavaScript object
- [ ] Tested in browser

## 🔄 Testing Your Lesson | మీ పాఠాన్ని పరీక్షించడం

After adding your lesson:

1. Open `index.html` in a browser
2. Check if the lesson appears in the sidebar
3. Click on the lesson and verify:
   - Title displays correctly
   - Description is readable
   - Visual demonstration shows properly
   - Code examples have correct formatting
   - Transpiler buttons work
   - Practice editor loads template
4. Complete the lesson and verify XP is awarded
5. Check that next lesson unlocks (if any)

## 📚 Advanced Tips | ఆధునాతన చిట్కాలు

### Tip 1: Interactive Visuals
Use JavaScript in your visual HTML:
```javascript
visual: `
    <div id="interactive-demo">
        <button onclick="this.nextElementSibling.style.display='block'">
            Click to reveal
        </button>
        <div style="display:none;">
            Hidden content!
        </div>
    </div>
`
```

### Tip 2: Multi-Step Examples
Show progression in code:
```javascript
codeTelugu: `# Step 1: Define variable
పేరు = "రాము"

# Step 2: Use in function
పనిచేయి శుభాకాంక్షలు():
    చెప్పు "నమస్తే, " + పేరు
ముగింపు

# Step 3: Call function
శుభాకాంక్షలు()`
```

### Tip 3: Common Mistakes Section
Add a note about common errors:
```javascript
description: "Learn about loops. Note: Remember to increment your counter, or the loop will run forever!",
```

## 🆘 Need Help? | సహాయం అవసరమా?

- Review existing lessons in `lessons.js` for reference
- Check `QUICK_REFERENCE.md` for valid lipi-lang syntax
- Test frequently while building
- Keep content bilingual and accessible

---

**Happy lesson creating! | సంతోషంగా పాఠం సృష్టించండి!**
