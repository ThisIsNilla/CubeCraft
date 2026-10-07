let currentSessionId = null;
let currentActiveMethod = 'cfop';
let currentModuleIdx = -1;
let currentLessonIdx = -1;

async function initSession() {
    try {
        currentActiveMethod = localStorage.getItem('activeMethod') || 'cfop';
        console.log("Initializing session with method:", currentActiveMethod);
        
        const response = await fetch('/api/sessions', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ method: currentActiveMethod })
        });
        const data = await response.json();
        currentSessionId = data.session_id;
        updateUI(data, null);
        loadCourseTOC();
    } catch (error) {
        console.error("Failed to init session", error);
    }
}

async function executeNotation(move) {
    if (!currentSessionId) return;

    // Update toast UI
    const badge = document.getElementById("lastExecutedMove");
    if (badge) badge.innerText = move;
    
    const toast = document.getElementById("liveMoveBadge");
    if (toast) {
        toast.classList.remove("opacity-0", "translate-y-4");
        toast.classList.add("opacity-100", "translate-y-0");
        clearTimeout(window.toastTimeout);
        window.toastTimeout = setTimeout(() => {
            toast.classList.remove("opacity-100", "translate-y-0");
            toast.classList.add("opacity-0", "translate-y-4");
        }, 1500);
    }

    try {
        const response = await fetch(`/api/sessions/${currentSessionId}/moves`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sequence: move })
        });
        const data = await response.json();
        updateUI(data, move);
    } catch (error) {
        console.error("Failed to execute move", error);
    }
}
window.executeNotation = executeNotation;

window.scrambleCube = async function() {
    if (!currentSessionId) return;
    
    const faces = ['U', 'D', 'F', 'B', 'L', 'R'];
    const modifiers = ['', "'", '2'];
    const opposites = { 'U':'D', 'D':'U', 'F':'B', 'B':'F', 'L':'R', 'R':'L' };
    
    let scramble = [];
    let prevFace = '';
    let prevPrevFace = '';
    
    for(let i=0; i<20; i++) {
        let face;
        while (true) {
            face = faces[Math.floor(Math.random() * faces.length)];
            if (face === prevFace) continue;
            if (face === prevPrevFace && opposites[face] === prevFace) continue;
            break;
        }
        let mod = modifiers[Math.floor(Math.random() * modifiers.length)];
        scramble.push(face + mod);
        prevPrevFace = prevFace;
        prevFace = face;
    }
    
    try {
        const sequence = scramble.join(" ");
        const response = await fetch(`/api/sessions/${currentSessionId}/moves`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sequence: sequence })
        });
        const data = await response.json();
        updateUI(data, sequence);
        
        const badge = document.getElementById("lastExecutedMove");
        if (badge) badge.innerText = "SCRAMBLED";
        
        const container = document.getElementById("scrambleDisplayContainer");
        const str = document.getElementById("scrambleDisplayString");
        if (container && str) {
            str.innerText = sequence;
            container.classList.remove("hidden");
        }
    } catch (error) {
        console.error("Failed to scramble", error);
    }
}

function updateUI(data, lastMove) {
    if (!data) return;
    
    const methodBadge = document.getElementById("methodBadge");
    if (methodBadge) methodBadge.innerText = data.method.toUpperCase();
    
    // We update the cube animation
    if (window.animateCubeMove && data.facelet_string) {
        window.animateCubeMove(lastMove, data.facelet_string);
    } else if (window.updateCubeColors && data.facelet_string) {
        window.updateCubeColors(data.facelet_string);
    }
}

// ==========================================
// COURSE PLAYER LOGIC
// ==========================================

function loadCourseTOC() {
    const data = window.COURSE_DATA[currentActiveMethod];
    if (!data) return;
    
    document.getElementById("courseTitle").innerText = data.title;
    document.getElementById("btnBackToToc").style.display = "none";
    document.getElementById("activeLessonView").classList.add("hidden");
    const tocView = document.getElementById("courseTocView");
    tocView.classList.remove("hidden");
    tocView.innerHTML = '';
    
    data.modules.forEach((mod, idx) => {
        const card = document.createElement('div');
        card.className = "p-4 rounded-2xl border border-slate-200 bg-white hover:bg-slate-50 transition-colors cursor-pointer group shadow-xs";
        card.onclick = () => loadLesson(idx, 0);
        card.innerHTML = `
            <div class="flex items-center justify-between">
                <div>
                    <h4 class="text-sm font-extrabold text-slate-800 group-hover:text-blue-700 transition-colors">${mod.title}</h4>
                    <p class="text-xs text-slate-500 font-medium mt-1">${mod.lessons.length} Lessons</p>
                </div>
                <span class="material-symbols-outlined text-slate-400 group-hover:text-blue-600">chevron_right</span>
            </div>
        `;
        tocView.appendChild(card);
    });
}
window.loadCourseTOC = loadCourseTOC;

function loadLesson(moduleIdx, lessonIdx) {
    const data = window.COURSE_DATA[currentActiveMethod];
    const mod = data.modules[moduleIdx];
    if (!mod) return;
    const lesson = mod.lessons[lessonIdx];
    if (!lesson) return;
    
    currentModuleIdx = moduleIdx;
    currentLessonIdx = lessonIdx;
    
    document.getElementById("courseTocView").classList.add("hidden");
    document.getElementById("activeLessonView").classList.remove("hidden");
    document.getElementById("btnBackToToc").style.display = "block";
    document.getElementById("courseTitle").innerText = mod.title;
    
    document.getElementById("lessonTitle").innerText = lesson.title;
    document.getElementById("lessonContent").innerHTML = lesson.content;
    
    const actionBox = document.getElementById("lessonActionBox");
    if (lesson.setupScramble || lesson.algorithm) {
        actionBox.classList.remove("hidden");
        document.getElementById("lessonSetup").innerText = lesson.setupScramble || "Solved Cube";
        document.getElementById("lessonAlgo").innerText = lesson.algorithm || "N/A";
    } else {
        actionBox.classList.add("hidden");
    }
    
    // Navigation
    document.getElementById("lessonProgressIndicator").innerText = `${lessonIdx + 1} / ${mod.lessons.length}`;
    
    const btnPrev = document.getElementById("btnPrevLesson");
    if (lessonIdx > 0) {
        btnPrev.style.visibility = "visible";
    } else {
        btnPrev.style.visibility = "hidden";
    }
    
    const btnNext = document.getElementById("btnNextLesson");
    if (lessonIdx < mod.lessons.length - 1) {
        btnNext.innerText = "Next ➔";
        btnNext.onclick = () => loadLesson(moduleIdx, lessonIdx + 1);
    } else {
        btnNext.innerText = "Finish Module ➔";
        btnNext.onclick = () => loadCourseTOC();
    }
}
window.loadLesson = loadLesson;
window.nextLesson = () => { /* assigned dynamically */ };
window.prevLesson = () => {
    if (currentLessonIdx > 0) loadLesson(currentModuleIdx, currentLessonIdx - 1);
};

window.play3DDemo = async function() {
    const data = window.COURSE_DATA[currentActiveMethod];
    const lesson = data.modules[currentModuleIdx].lessons[currentLessonIdx];
    if (!lesson || !lesson.algorithm) return;

    // First reset and apply setup
    await fetch('/api/sessions', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ method: currentActiveMethod, scramble_sequence: lesson.setupScramble })
    }).then(res => res.json()).then(d => {
        currentSessionId = d.session_id;
        if (window.updateCubeColors) window.updateCubeColors(d.facelet_string);
    });
    
    // Now execute algorithm moves one by one
    const moves = lesson.algorithm.trim().split(/\s+/);
    for (let i = 0; i < moves.length; i++) {
        await new Promise(r => setTimeout(r, 800)); // wait for animation
        await executeNotation(moves[i]);
    }
}

window.addEventListener('DOMContentLoaded', initSession);
