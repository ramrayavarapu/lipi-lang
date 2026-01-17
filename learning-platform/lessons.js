// Lesson data for Lipi-Lang Learning Platform
const lessons = [
    // Lesson 1: Variables & Data Types
    {
        id: 0,
        title: "Variables & Data Types",
        titleTe: "వేరియబుల్స్ మరియు డేటా రకాలు",
        description: "Learn how to store and manipulate data using variables in lipi-lang. Understand different data types and how to work with them.",
        descriptionTe: "లిపి-భాషలో వేరియబుల్స్ ఉపయోగించి డేటాను ఎలా నిల్వ చేయాలి మరియు మార్చాలి నేర్చుకోండి. వివిధ డేటా రకాలను మరియు వాటితో ఎలా పనిచేయాలో అర్థం చేసుకోండి.",
        xp: 10,
        objectives: [
            "Understand what variables are | వేరియబుల్స్ అంటే ఏమిటో అర్థం చేసుకోవడం",
            "Learn data types: చరరాశి (string), సంఖ్య (number) | డేటా రకాలు నేర్చుకోవడం",
            "Create and modify variables | వేరియబుల్స్ సృష్టించడం మరియు మార్చడం",
            "Use చెప్పు/print to display values | విలువలను చూపించడానికి చెప్పు/print ఉపయోగించడం"
        ],
        visual: `
            <div style="text-align: center;">
                <h4>Variable Storage | వేరియబుల్ నిల్వ</h4>
                <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
                    <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; border: 2px solid #667eea;">
                        <strong>పేరు</strong> (name)<br>
                        <span style="font-size: 24px;">📦</span><br>
                        "రాము" (string)
                    </div>
                    <div style="background: #f3e5f5; padding: 20px; border-radius: 10px; border: 2px solid #764ba2;">
                        <strong>వయసు</strong> (age)<br>
                        <span style="font-size: 24px;">📦</span><br>
                        25 (number)
                    </div>
                    <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; border: 2px solid #4caf50;">
                        <strong>నగరం</strong> (city)<br>
                        <span style="font-size: 24px;">📦</span><br>
                        "హైదరాబాద్" (string)
                    </div>
                </div>
                <p style="margin-top: 20px; color: #666;">
                    Variables are like labeled boxes that store information<br>
                    వేరియబుల్స్ సమాచారాన్ని నిల్వ చేసే లేబుల్ చేసిన పెట్టెల లాంటివి
                </p>
            </div>
        `,
        codeTelugu: `# వేరియబుల్స్ సృష్టించడం
పేరు = "రాము"
వయసు = 25
నగరం = "హైదరాబాద్"

# విలువలను చూపించడం
చెప్పు "నమస్తే!"
చెప్పు "పేరు: " + పేరు
చెప్పు "వయసు: " + వయసు
చెప్పు "నగరం: " + నగరం`,
        codeEnglish: `# Creating variables
name = "Ramu"
age = 25
city = "Hyderabad"

# Displaying values
print "Hello!"
print "Name: " + name
print "Age: " + age
print "City: " + city`,
        practiceTemplate: `# Try creating your own variables!
# మీ స్వంత వేరియబుల్స్ సృష్టించండి!

పేరు = "మీ పేరు ఇక్కడ"
వయసు = 20

చెప్పు "నా పేరు: " + పేరు
చెప్పు "నా వయసు: " + వయసు`,
        transpilations: {
            python: `# Python equivalent
name = "Ramu"
age = 25
city = "Hyderabad"

print("Hello!")
print(f"Name: {name}")
print(f"Age: {age}")
print(f"City: {city}")`,
            javascript: `// JavaScript equivalent
const name = "Ramu";
const age = 25;
const city = "Hyderabad";

console.log("Hello!");
console.log("Name: " + name);
console.log("Age: " + age);
console.log("City: " + city);`,
            csharp: `// C# equivalent
string name = "Ramu";
int age = 25;
string city = "Hyderabad";

Console.WriteLine("Hello!");
Console.WriteLine("Name: " + name);
Console.WriteLine("Age: " + age);
Console.WriteLine("City: " + city);`
        }
    },

    // Lesson 2: Conditional Statements
    {
        id: 1,
        title: "Conditional Statements",
        titleTe: "షరతులతో నిర్ణయాలు",
        description: "Learn how to make decisions in your code using if-else statements. Control the flow of your program based on conditions.",
        descriptionTe: "if-else స్టేట్‌మెంట్‌లను ఉపయోగించి మీ కోడ్‌లో నిర్ణయాలు ఎలా తీసుకోవాలో నేర్చుకోండి. షరతుల ఆధారంగా మీ ప్రోగ్రామ్ ఫ్లోను నియంత్రించండి.",
        xp: 15,
        objectives: [
            "Understand conditional logic | షరతుల తర్కం అర్థం చేసుకోవడం",
            "Use ఒకవేళ (if) statements | ఒకవేళ స్టేట్‌మెంట్‌లు ఉపయోగించడం",
            "Use లేకపోతే (else) for alternatives | ప్రత్యామ్నాయాల కోసం లేకపోతే ఉపయోగించడం",
            "Compare values with >, <, == operators | >, <, == ఆపరేటర్‌లతో విలువలను పోల్చడం"
        ],
        visual: `
            <div style="text-align: center;">
                <h4>Decision Flow | నిర్ణయ ప్రవాహం</h4>
                <div style="max-width: 500px; margin: 20px auto;">
                    <div style="background: #fff3e0; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                        <strong>Question | ప్రశ్న</strong><br>
                        వయసు > 18? (Age > 18?)
                    </div>
                    <div style="display: flex; gap: 20px; justify-content: center;">
                        <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; flex: 1; border: 3px solid #4caf50;">
                            ✓ YES / అవును<br>
                            <strong>పెద్దవారు</strong><br>
                            (Adult)
                        </div>
                        <div style="background: #ffebee; padding: 20px; border-radius: 10px; flex: 1; border: 3px solid #f44336;">
                            ✗ NO / లేదు<br>
                            <strong>చిన్నవారు</strong><br>
                            (Minor)
                        </div>
                    </div>
                </div>
                <p style="margin-top: 20px; color: #666;">
                    Conditions let your program make smart choices<br>
                    షరతులు మీ ప్రోగ్రామ్‌ను తెలివైన ఎంపికలు చేయడానికి అనుమతిస్తాయి
                </p>
            </div>
        `,
        codeTelugu: `# షరతుల ఉదాహరణ
వయసు = 20

ఒకవేళ వయసు > 18:
    చెప్పు "మీరు పెద్దవారు"
    చెప్పు "మీరు వోటు వేయవచ్చు"
లేకపోతే:
    చెప్పు "మీరు చిన్నవారు"
    చెప్పు "మీరు ఇంకా వోటు వేయలేరు"
ముగింపు`,
        codeEnglish: `# Conditional example
age = 20

if age > 18:
    print "You are an adult"
    print "You can vote"
else:
    print "You are a minor"
    print "You cannot vote yet"
end`,
        practiceTemplate: `# Try writing your own conditions!
# మీ స్వంత షరతులను వ్రాయండి!

మార్కులు = 85

ఒకవేళ మార్కులు >= 90:
    చెప్పు "అద్భుతం! A గ్రేడ్"
లేకపోతే:
    చెప్పు "బాగుంది! B గ్రేడ్"
ముగింపు`,
        transpilations: {
            python: `# Python equivalent
age = 20

if age > 18:
    print("You are an adult")
    print("You can vote")
else:
    print("You are a minor")
    print("You cannot vote yet")`,
            javascript: `// JavaScript equivalent
const age = 20;

if (age > 18) {
    console.log("You are an adult");
    console.log("You can vote");
} else {
    console.log("You are a minor");
    console.log("You cannot vote yet");
}`,
            csharp: `// C# equivalent
int age = 20;

if (age > 18) {
    Console.WriteLine("You are an adult");
    Console.WriteLine("You can vote");
} else {
    Console.WriteLine("You are a minor");
    Console.WriteLine("You cannot vote yet");
}`
        }
    },

    // Lesson 3: Loops & Iteration
    {
        id: 2,
        title: "Loops & Iteration",
        titleTe: "లూప్స్ మరియు పునరావృతం",
        description: "Master the art of repetition in programming. Learn how to use loops to perform tasks multiple times efficiently.",
        descriptionTe: "ప్రోగ్రామింగ్‌లో పునరావృత కళను నేర్చుకోండి. పనులను అనేకసార్లు సమర్థవంతంగా చేయడానికి లూప్‌లను ఎలా ఉపయోగించాలో నేర్చుకోండి.",
        xp: 20,
        objectives: [
            "Understand loop concepts | లూప్ భావనలు అర్థం చేసుకోవడం",
            "Use వరకు (while) loops | వరకు లూప్‌లు ఉపయోగించడం",
            "Use ప్రతి (for) loops | ప్రతి లూప్‌లు ఉపయోగించడం",
            "Iterate over ranges and lists | పరిధులు మరియు జాబితాలపై పునరావృతం చేయడం"
        ],
        visual: `
            <div style="text-align: center;">
                <h4>Loop Execution | లూప్ అమలు</h4>
                <div style="max-width: 600px; margin: 20px auto;">
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                        <strong>Start | ప్రారంభం:</strong> సంఖ్య = 1
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        <div style="background: #f3e5f5; padding: 10px; border-radius: 5px; border-left: 5px solid #764ba2;">
                            🔁 Iteration 1: చెప్పు "1" → సంఖ్య = 2
                        </div>
                        <div style="background: #f3e5f5; padding: 10px; border-radius: 5px; border-left: 5px solid #764ba2;">
                            🔁 Iteration 2: చెప్పు "2" → సంఖ్య = 3
                        </div>
                        <div style="background: #f3e5f5; padding: 10px; border-radius: 5px; border-left: 5px solid #764ba2;">
                            🔁 Iteration 3: చెప్పు "3" → సంఖ్య = 4
                        </div>
                        <div style="background: #f3e5f5; padding: 10px; border-radius: 5px; border-left: 5px solid #764ba2;">
                            🔁 Iteration 4: చెప్పు "4" → సంఖ్య = 5
                        </div>
                        <div style="background: #f3e5f5; padding: 10px; border-radius: 5px; border-left: 5px solid #764ba2;">
                            🔁 Iteration 5: చెప్పు "5" → సంఖ్య = 6
                        </div>
                    </div>
                    <div style="background: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 15px;">
                        <strong>Stop | ఆగు:</strong> సంఖ్య > 5 (Condition false)
                    </div>
                </div>
                <p style="margin-top: 20px; color: #666;">
                    Loops repeat actions until a condition is met<br>
                    షరతు నెరవేరే వరకు లూప్‌లు చర్యలను పునరావృతం చేస్తాయి
                </p>
            </div>
        `,
        codeTelugu: `# వరకు లూప్ (while loop)
సంఖ్య = 1

వరకు సంఖ్య <= 5:
    చెప్పు "సంఖ్య: " + సంఖ్య
    సంఖ్య = సంఖ్య + 1
ముగింపు

# ప్రతి లూప్ (for loop)
ప్రతి ఐ లో పరిధి(1, 6):
    చెప్పు "గణన: " + ఐ
ముగింపు`,
        codeEnglish: `# while loop
number = 1

while number <= 5:
    print "Number: " + number
    number = number + 1
end

# for loop
for i in range(1, 6):
    print "Count: " + i
end`,
        practiceTemplate: `# Practice loops! | లూప్‌లను ప్రాక్టీస్ చేయండి!

# Count from 1 to 10
# 1 నుండి 10 వరకు లెక్కించండి
ప్రతి సంఖ్య లో పరిధి(1, 11):
    చెప్పు "సంఖ్య: " + సంఖ్య
ముగింపు`,
        transpilations: {
            python: `# Python equivalent
# while loop
number = 1

while number <= 5:
    print(f"Number: {number}")
    number = number + 1

# for loop
for i in range(1, 6):
    print(f"Count: {i}")`,
            javascript: `// JavaScript equivalent
// while loop
let number = 1;

while (number <= 5) {
    console.log("Number: " + number);
    number = number + 1;
}

// for loop
for (let i = 1; i <= 5; i++) {
    console.log("Count: " + i);
}`,
            csharp: `// C# equivalent
// while loop
int number = 1;

while (number <= 5) {
    Console.WriteLine("Number: " + number);
    number = number + 1;
}

// for loop
for (int i = 1; i <= 5; i++) {
    Console.WriteLine("Count: " + i);
}`
        }
    }
];

// XP Levels configuration
const levels = [
    { level: 1, xpRequired: 0, xpToNext: 100 },
    { level: 2, xpRequired: 100, xpToNext: 150 },
    { level: 3, xpRequired: 250, xpToNext: 200 },
    { level: 4, xpRequired: 450, xpToNext: 250 },
    { level: 5, xpRequired: 700, xpToNext: Infinity }
];
