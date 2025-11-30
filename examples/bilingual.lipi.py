# Lipi v0.5 – Bilingual example (తెలుగు + English)
# This demonstrates Telugu and English keywords working together!

# Telugu variable + English variable
పేరు = "రామ్"
name = "Ram"
వయసు = 25
age = 25

# Telugu print
చెప్పు "🙏 నమస్తే! ఇది బైలింగ్వల్ ప్రోగ్రాం"

# English print
print "This program mixes Telugu and English!"

# Telugu print with English variable
చెప్పు "English name: " + name

# English print with Telugu variable
print "తెలుగు పేరు: " + పేరు

# Telugu if block with English print inside
యెడల వయసు > 18:
    print "Adult (using English inside Telugu if)"
లేకపోతే:
    చెప్పు "యంగ్"
ముగింపు

# English if block with Telugu print inside
if age < 30:
    చెప్పు "యువత (using Telugu inside English if)"
else:
    print "Senior"
end

# Telugu while loop
కౌంట్ = 1
చెప్పు "తెలుగు లూప్:"
వరకు కౌంట్ <= 3:
    చెప్పు "కౌంట్: " + కౌంట్
    కౌంట్ = కౌంట్ + 1
ముగింపు

# English while loop
count = 1
print "English loop:"
while count <= 3:
    print "count: " + count
    count = count + 1
end

# Mixed loop - Telugu keyword with English variable
చెప్పు "మిక్స్డ్ లూప్ (Telugu while + English var):"
counter = 1
వరకు counter <= 3:
    చెప్పు "Mixed counter: " + counter
    counter = counter + 1
ముగింపు

print "ప్రోగ్రాం ముగిసింది! (Program completed!)"
