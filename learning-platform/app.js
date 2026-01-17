// Lipi-Lang Learning Platform - Main Application Logic

// State management
let state = {
    currentLesson: -1,
    completedLessons: [],
    currentXP: 0,
    currentLevel: 1,
    unlockedLessons: [0] // First lesson is always unlocked
};

// Load state from localStorage
function loadState() {
    const saved = localStorage.getItem('lipiLangProgress');
    if (saved) {
        state = JSON.parse(saved);
    }
    updateUI();
}

// Save state to localStorage
function saveState() {
    localStorage.setItem('lipiLangProgress', JSON.stringify(state));
}

// Update UI elements based on current state
function updateUI() {
    // Update XP and Level display
    document.getElementById('current-xp').textContent = state.currentXP;
    document.getElementById('current-level').textContent = state.currentLevel;

    const currentLevelData = levels[state.currentLevel - 1];
    if (currentLevelData) {
        document.getElementById('next-level-xp').textContent = currentLevelData.xpToNext === Infinity
            ? 'MAX'
            : currentLevelData.xpRequired + currentLevelData.xpToNext;
    }

    // Update lesson buttons
    const lessonButtons = document.querySelectorAll('.lesson-btn');
    lessonButtons.forEach((btn, index) => {
        const lessonId = parseInt(btn.dataset.lesson);

        // Remove all state classes
        btn.classList.remove('active', 'completed', 'locked');

        // Add appropriate class
        if (state.completedLessons.includes(lessonId)) {
            btn.classList.add('completed');
        } else if (state.currentLesson === lessonId) {
            btn.classList.add('active');
        } else if (!state.unlockedLessons.includes(lessonId)) {
            btn.classList.add('locked');
        }

        // Enable/disable button
        btn.disabled = !state.unlockedLessons.includes(lessonId);
    });

    // Update progress bar
    const completedCount = state.completedLessons.length;
    const totalLessons = lessons.length;
    const progressPercent = (completedCount / totalLessons) * 100;

    document.getElementById('progress-fill').style.width = progressPercent + '%';
    document.getElementById('progress-text').textContent =
        `${completedCount} / ${totalLessons} Lessons Completed`;
}

// Load a specific lesson
function loadLesson(lessonId) {
    // Check if lesson is unlocked
    if (!state.unlockedLessons.includes(lessonId)) {
        showNotification('🔒 This lesson is locked! Complete previous lessons first.', 'warning');
        return;
    }

    const lesson = lessons[lessonId];
    if (!lesson) {
        console.error('Lesson not found:', lessonId);
        return;
    }

    state.currentLesson = lessonId;
    saveState();
    updateUI();

    // Render lesson content
    const template = document.getElementById('lesson-template').textContent;
    const content = renderTemplate(template, {
        lessonId: lesson.id,
        title: lesson.title,
        titleTe: lesson.titleTe,
        description: lesson.description,
        descriptionTe: lesson.descriptionTe,
        objectives: lesson.objectives.map(obj => `<li>${obj}</li>`).join(''),
        visual: lesson.visual,
        codeTelugu: lesson.codeTelugu,
        codeEnglish: lesson.codeEnglish,
        practiceTemplate: lesson.practiceTemplate
    });

    document.getElementById('lesson-content').innerHTML = content;

    // Scroll to top
    window.scrollTo(0, 0);
}

// Simple template renderer
function renderTemplate(template, data) {
    let result = template;
    for (const [key, value] of Object.entries(data)) {
        const regex = new RegExp(`{{${key}}}`, 'g');
        result = result.replace(regex, value);
    }
    return result;
}

// Complete current lesson
function completeLesson(lessonId) {
    // Check if already completed
    if (state.completedLessons.includes(lessonId)) {
        showNotification('✓ You already completed this lesson!', 'info');
        return;
    }

    const lesson = lessons[lessonId];

    // Award XP
    state.currentXP += lesson.xp;
    state.completedLessons.push(lessonId);

    // Check for level up
    checkLevelUp();

    // Unlock next lesson
    const nextLessonId = lessonId + 1;
    if (nextLessonId < lessons.length && !state.unlockedLessons.includes(nextLessonId)) {
        state.unlockedLessons.push(nextLessonId);
        showNotification(`🎉 Lesson completed! +${lesson.xp} XP. Next lesson unlocked!`, 'success');
    } else {
        showNotification(`🎉 Lesson completed! +${lesson.xp} XP`, 'success');
    }

    saveState();
    updateUI();
}

// Check if player leveled up
function checkLevelUp() {
    const currentLevelData = levels[state.currentLevel - 1];
    const nextLevelData = levels[state.currentLevel];

    if (nextLevelData && state.currentXP >= nextLevelData.xpRequired) {
        state.currentLevel++;
        showNotification(`🎊 LEVEL UP! You are now Level ${state.currentLevel}!`, 'success');
    }
}

// Navigate to next lesson
function nextLesson() {
    const nextId = state.currentLesson + 1;
    if (nextId < lessons.length) {
        loadLesson(nextId);
    }
}

// Navigate to previous lesson
function previousLesson() {
    const prevId = state.currentLesson - 1;
    if (prevId >= 0) {
        loadLesson(prevId);
    }
}

// Show transpiled code
function showTranspiled(language, lessonId) {
    const lesson = lessons[lessonId];
    const output = document.getElementById('transpiled-output');

    if (lesson.transpilations[language]) {
        output.textContent = lesson.transpilations[language];
        output.classList.add('show');
    }
}

// Simple lipi-lang interpreter for practice editor
function runCode() {
    const code = document.getElementById('practice-editor').value;
    const outputArea = document.getElementById('output-area');

    outputArea.classList.add('show');
    outputArea.textContent = 'Running...\n';

    try {
        // Simple interpreter - handles basic print/చెప్పు statements
        const lines = code.split('\n');
        let output = '';
        let variables = {};

        for (let line of lines) {
            line = line.trim();

            // Skip comments and empty lines
            if (line.startsWith('#') || line === '') continue;

            // Variable assignment
            if (line.includes('=')) {
                const [varName, value] = line.split('=').map(s => s.trim());
                // Remove quotes from strings
                let processedValue = value.replace(/["']/g, '');
                // Try to convert to number
                if (!isNaN(processedValue)) {
                    processedValue = Number(processedValue);
                }
                variables[varName] = processedValue;
            }
            // Print statements (చెప్పు or print)
            else if (line.startsWith('చెప్పు ') || line.startsWith('print ')) {
                let content = line.replace(/^(చెప్పు|print)\s+/, '');

                // Handle string concatenation
                if (content.includes('+')) {
                    const parts = content.split('+').map(p => p.trim());
                    let result = '';
                    for (let part of parts) {
                        if (part.startsWith('"') || part.startsWith("'")) {
                            result += part.replace(/["']/g, '');
                        } else if (variables[part] !== undefined) {
                            result += variables[part];
                        } else {
                            result += part;
                        }
                    }
                    output += result + '\n';
                } else {
                    // Simple print
                    content = content.replace(/["']/g, '');
                    if (variables[content] !== undefined) {
                        output += variables[content] + '\n';
                    } else {
                        output += content + '\n';
                    }
                }
            }
        }

        outputArea.textContent = output || '(No output)';
    } catch (error) {
        outputArea.textContent = 'Error: ' + error.message;
    }
}

// Show notification
function showNotification(message, type = 'success') {
    // Remove existing notification
    const existing = document.querySelector('.success-notification');
    if (existing) {
        existing.remove();
    }

    // Create notification
    const notification = document.createElement('div');
    notification.className = 'success-notification';
    notification.textContent = message;
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('hide');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Load saved progress
    loadState();

    // Add lesson button click handlers
    const lessonButtons = document.querySelectorAll('.lesson-btn');
    lessonButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const lessonId = parseInt(this.dataset.lesson);
            loadLesson(lessonId);
        });
    });

    // Show welcome screen or last lesson
    if (state.currentLesson >= 0) {
        loadLesson(state.currentLesson);
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to run code
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const editor = document.getElementById('practice-editor');
        if (editor && document.activeElement === editor) {
            runCode();
        }
    }

    // Arrow keys for navigation (when not in editor)
    if (document.activeElement.tagName !== 'TEXTAREA') {
        if (e.key === 'ArrowRight') {
            nextLesson();
        } else if (e.key === 'ArrowLeft') {
            previousLesson();
        }
    }
});
