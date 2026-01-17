// Lipi-Lang Learning Platform - Main Application Logic

// Constants
const STORAGE_KEY = 'lipiLangProgress';
const DEFAULT_STATE = {
    currentLesson: -1,
    completedLessons: [],
    currentXP: 0,
    currentLevel: 1,
    unlockedLessons: [0] // First lesson is always unlocked
};

// State management
let state = { ...DEFAULT_STATE };

// Validation helper functions
const Validators = {
    /**
     * Validate state object structure
     * @param {Object} stateObj - State object to validate
     * @returns {boolean} True if valid
     */
    isValidState(stateObj) {
        if (!stateObj || typeof stateObj !== 'object') return false;

        const requiredKeys = ['currentLesson', 'completedLessons', 'currentXP', 'currentLevel', 'unlockedLessons'];
        const hasAllKeys = requiredKeys.every(key => key in stateObj);
        if (!hasAllKeys) return false;

        // Type validation
        if (typeof stateObj.currentLesson !== 'number') return false;
        if (!Array.isArray(stateObj.completedLessons)) return false;
        if (typeof stateObj.currentXP !== 'number' || stateObj.currentXP < 0) return false;
        if (typeof stateObj.currentLevel !== 'number' || stateObj.currentLevel < 1) return false;
        if (!Array.isArray(stateObj.unlockedLessons)) return false;

        return true;
    },

    /**
     * Sanitize and fix state object
     * @param {Object} stateObj - State object to sanitize
     * @returns {Object} Sanitized state
     */
    sanitizeState(stateObj) {
        const sanitized = { ...DEFAULT_STATE };

        if (this.isValidState(stateObj)) {
            sanitized.currentLesson = Math.max(-1, Math.min(stateObj.currentLesson, lessons.length - 1));
            sanitized.completedLessons = stateObj.completedLessons.filter(id =>
                typeof id === 'number' && id >= 0 && id < lessons.length
            );
            sanitized.currentXP = Math.max(0, stateObj.currentXP);
            sanitized.currentLevel = Math.max(1, Math.min(5, stateObj.currentLevel));
            sanitized.unlockedLessons = stateObj.unlockedLessons.filter(id =>
                typeof id === 'number' && id >= 0 && id < lessons.length
            );

            // Ensure first lesson is always unlocked
            if (!sanitized.unlockedLessons.includes(0)) {
                sanitized.unlockedLessons.unshift(0);
            }
        }

        return sanitized;
    }
};

// DOM Helper functions
const DOMHelpers = {
    /**
     * Safely get element by ID
     * @param {string} id - Element ID
     * @returns {HTMLElement|null} Element or null
     */
    getElement(id) {
        const element = document.getElementById(id);
        if (!element) {
            console.warn(`Element not found: ${id}`);
        }
        return element;
    },

    /**
     * Safely set text content
     * @param {string} id - Element ID
     * @param {string} text - Text to set
     */
    setText(id, text) {
        const element = this.getElement(id);
        if (element) {
            element.textContent = String(text);
        }
    },

    /**
     * Safely set HTML content
     * @param {string} id - Element ID
     * @param {string} html - HTML to set
     */
    setHTML(id, html) {
        const element = this.getElement(id);
        if (element) {
            element.innerHTML = html;
        }
    },

    /**
     * Safely add class to element
     * @param {string} id - Element ID
     * @param {string} className - Class name to add
     */
    addClass(id, className) {
        const element = this.getElement(id);
        if (element) {
            element.classList.add(className);
        }
    },

    /**
     * Safely remove class from element
     * @param {string} id - Element ID
     * @param {string} className - Class name to remove
     */
    removeClass(id, className) {
        const element = this.getElement(id);
        if (element) {
            element.classList.remove(className);
        }
    }
};

// Load state from localStorage
function loadState() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            const parsedState = JSON.parse(saved);
            state = Validators.sanitizeState(parsedState);
            console.log('✅ State loaded from localStorage');
        } else {
            state = { ...DEFAULT_STATE };
            console.log('📝 Using default state');
        }
    } catch (error) {
        console.error('❌ Error loading state:', error);
        state = { ...DEFAULT_STATE };
        showNotification('⚠️ Progress could not be loaded. Starting fresh.', 'warning');
    }
    updateUI();
}

// Save state to localStorage
function saveState() {
    try {
        // Validate before saving
        if (!Validators.isValidState(state)) {
            console.error('❌ Invalid state, cannot save:', state);
            return;
        }
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        console.log('💾 State saved to localStorage');
    } catch (error) {
        console.error('❌ Error saving state:', error);
        if (error.name === 'QuotaExceededError') {
            showNotification('⚠️ Storage quota exceeded! Clear browser data.', 'warning');
        } else {
            showNotification('⚠️ Could not save progress', 'warning');
        }
    }
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
    // Validate lesson ID type
    if (typeof lessonId !== 'number') {
        console.error('Invalid lesson ID type:', typeof lessonId);
        showNotification('❌ Invalid lesson ID', 'error');
        return;
    }

    // Use LessonManager to safely get lesson
    const lesson = typeof LessonManager !== 'undefined'
        ? LessonManager.getLesson(lessonId)
        : lessons.find(l => l.id === lessonId);

    if (!lesson) {
        console.error('Lesson not found:', lessonId);
        showNotification(`❌ Lesson ${lessonId} not found`, 'error');
        return;
    }

    // Check if lesson is unlocked
    if (!state.unlockedLessons.includes(lessonId)) {
        showNotification('🔒 This lesson is locked! Complete previous lessons first.', 'warning');
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
