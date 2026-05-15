const AUTH_KEY = 'mathsBoosterUsers';
const PROGRESS_KEY = 'mathsBoosterProgress';

const activityBank = {
    '5-7': [
        { id: 'counting-1', title: 'Counting Basics', question: 'What is 3 + 2?', answer: 5 },
        { id: 'numbers-1', title: 'Number Friends', question: 'What is 6 - 1?', answer: 5 }
    ],
    '8-10': [
        { id: 'tables-1', title: 'Times Tables', question: 'What is 4 × 3?', answer: 12 },
        { id: 'division-1', title: 'Division Start', question: 'What is 18 ÷ 3?', answer: 6 }
    ],
    '11-13': [
        { id: 'fractions-1', title: 'Fraction Foundations', question: 'What is 1/2 of 14?', answer: 7 },
        { id: 'algebra-1', title: 'Algebra Step', question: 'If x + 5 = 11, what is x?', answer: 6 }
    ]
};

let activeUser = null;
let activeActivity = null;

function getEl(id) {
    return document.getElementById(id);
}

function sanitizeName(value) {
    return String(value || '').trim().replace(/\s+/g, ' ').slice(0, 40);
}

function readJSON(key, fallback) {
    try {
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : fallback;
    } catch {
        return fallback;
    }
}

function writeJSON(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function getUsers() {
    return readJSON(AUTH_KEY, {});
}

function saveUsers(users) {
    writeJSON(AUTH_KEY, users);
}

function getProgressMap() {
    return readJSON(PROGRESS_KEY, {});
}

function saveProgressMap(progress) {
    writeJSON(PROGRESS_KEY, progress);
}

function setAuthMessage(message) {
    getEl('auth-message').textContent = message;
}

function showSectionsAfterLogin() {
    getEl('dashboard-section').classList.remove('hidden');
    getEl('activity-section').classList.remove('hidden');
}

function updateDashboard() {
    const progressMap = getProgressMap();
    const stats = progressMap[activeUser] || { attempted: 0, correct: 0 };
    getEl('welcome-message').textContent = `Welcome, ${activeUser}!`;
    getEl('progress-summary').textContent = `Attempted: ${stats.attempted}, Correct: ${stats.correct}`;
}

function loadActivities(ageGroup) {
    const select = getEl('activity-select');
    select.innerHTML = '';

    (activityBank[ageGroup] || []).forEach((activity, index) => {
        const option = document.createElement('option');
        option.value = activity.id;
        option.textContent = `${index + 1}. ${activity.title}`;
        select.appendChild(option);
    });
}

function registerUser() {
    const username = sanitizeName(getEl('username').value);
    const ageGroup = getEl('age-group').value;

    if (!username || !ageGroup) {
        setAuthMessage('Please enter name and age group to register.');
        return;
    }

    const users = getUsers();
    users[username] = { ageGroup };
    saveUsers(users);
    setAuthMessage('Registered successfully. You can now login.');
}

function loginUser() {
    const username = sanitizeName(getEl('username').value);
    const users = getUsers();

    if (!username || !users[username]) {
        setAuthMessage('User not found. Please register first.');
        return;
    }

    activeUser = username;
    const ageGroup = users[username].ageGroup;

    showSectionsAfterLogin();
    loadActivities(ageGroup);
    updateDashboard();
    setAuthMessage('Login successful.');
}

function startActivity() {
    if (!activeUser) {
        setAuthMessage('Please login to start an activity.');
        return;
    }

    const users = getUsers();
    const selected = getEl('activity-select').value;
    const ageGroup = users[activeUser].ageGroup;
    activeActivity = (activityBank[ageGroup] || []).find(item => item.id === selected) || null;

    if (!activeActivity) {
        getEl('exercise-feedback').textContent = 'Please select an activity.';
        return;
    }

    getEl('exercise-title').textContent = activeActivity.title;
    getEl('exercise-question').textContent = activeActivity.question;
    getEl('answer-input').value = '';
    getEl('exercise-feedback').textContent = '';
    getEl('exercise-section').classList.remove('hidden');
}

function submitAnswer() {
    if (!activeUser || !activeActivity) {
        getEl('exercise-feedback').textContent = 'Start an activity first.';
        return;
    }

    const guess = Number(getEl('answer-input').value);
    if (!Number.isFinite(guess)) {
        getEl('exercise-feedback').textContent = 'Enter a valid number.';
        return;
    }

    const progressMap = getProgressMap();
    const userProgress = progressMap[activeUser] || { attempted: 0, correct: 0 };
    userProgress.attempted += 1;

    if (guess === activeActivity.answer) {
        userProgress.correct += 1;
        getEl('exercise-feedback').textContent = 'Great job! Correct answer ✅';
    } else {
        getEl('exercise-feedback').textContent = `Keep trying! Correct answer: ${activeActivity.answer}`;
    }

    progressMap[activeUser] = userProgress;
    saveProgressMap(progressMap);
    updateDashboard();
}

function bootstrap() {
    getEl('register-btn').addEventListener('click', registerUser);
    getEl('login-btn').addEventListener('click', loginUser);
    getEl('start-activity-btn').addEventListener('click', startActivity);
    getEl('submit-answer-btn').addEventListener('click', submitAnswer);
}

document.addEventListener('DOMContentLoaded', bootstrap);
