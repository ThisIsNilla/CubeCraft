let currentActiveMethod = 'cfop';

let currentSessionId = null;

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
        console.log("Session initialized. ID:", currentSessionId);
        updateUI(data);
    } catch (error) {
        console.error("Failed to init session", error);
    }
}

async function executeNotation(move) {
    if (window.activeTutorial) {
        const expected = window.activeTutorial.solution[window.activeTutorial.currentIndex];
        if (move !== expected) {
            const nextMoveEl = document.getElementById('tutorNextMove');
            nextMoveEl.classList.replace('text-amber-400', 'text-red-400');
            setTimeout(() => {
                if (window.activeTutorial) {
                    nextMoveEl.classList.replace('text-red-400', 'text-amber-400');
                }
            }, 500);
            return; // Block wrong moves
        } else {
            window.activeTutorial.currentIndex++;
            updateTutorUI();
        }
    }

    if (!currentSessionId) return;

    // Update toast UI
    const badge = document.getElementById("lastExecutedMove");
    if (badge) badge.innerText = move;
    
    const toast = document.getElementById("liveMoveBadge");
    if (toast) {
        toast.classList.add("scale-105");
        setTimeout(() => toast.classList.remove("scale-105"), 120);
    }

    try {
        const response = await fetch(`/api/sessions/${currentSessionId}/moves`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sequence: move })
        });
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error("Failed to execute move", error);
    }
}

// Attach to window so HTML buttons can use it
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
            // Prevent same face twice in a row (e.g. F F2)
            if (face === prevFace) continue;
            // Prevent same face separated by its opposite (e.g. R L R2)
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
        updateUI(data);
        
        const badge = document.getElementById("lastExecutedMove");
        if (badge) badge.innerText = "SCRAMBLED";

        const scrambleContainer = document.getElementById("scrambleDisplayContainer");
        const scrambleString = document.getElementById("scrambleDisplayString");
        if (scrambleContainer && scrambleString) {
            scrambleContainer.classList.remove("hidden");
            scrambleString.innerText = sequence;
        }
    } catch (error) {
        console.error("Failed to scramble", error);
    }
}
window.triggerScrambleSequence = window.scrambleCube;

window.requestHint = async function() {
    if (!currentSessionId) return;
    try {
        const response = await fetch(`/api/sessions/${currentSessionId}/hint`);
        if (!response.ok) return;
        const hintData = await response.json();
        
        // Temporarily show hint in the description
        document.getElementById("stepDescription").innerHTML = `<strong>💡 Hint:</strong> Try the sequence <span class="text-blue-600 font-code-mono font-bold">${hintData.hint.join(' ')}</span>`;
    } catch (e) {
        console.error(e);
    }
}



function renderQuestTrack(currentStep) {
    const container = document.getElementById("questTrackContainer");
    if (!container || !window.LESSONS_DATA) return;
    
    const lessons = window.LESSONS_DATA[currentActiveMethod];
    if (!lessons) return;
    
    document.getElementById("questStageCount").innerText = `0/${lessons.length}`;
    container.innerHTML = '';
    
    lessons.forEach((lesson, index) => {
        // Basic match: if the current API step title contains the lesson title (e.g. "White Cross" in "Stage 1: White Cross")
        const isCurrent = lesson.title.toLowerCase().includes(currentStep.toLowerCase()) || currentStep.toLowerCase().includes(lesson.title.toLowerCase().replace(/stage \d+: /g, ''));
        
        const card = document.createElement('div');
        card.className = `p-3 rounded-2xl border ${isCurrent ? 'border-blue-600 bg-blue-50/60 shadow-xs ring-1 ring-blue-600' : 'border-slate-200 bg-white hover:bg-slate-50'} transition-colors flex items-center justify-between cursor-pointer group`;
        card.onclick = () => openLessonModal(currentActiveMethod, index);
        
        card.innerHTML = `
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full ${isCurrent ? 'bg-blue-600 text-white shadow-xs ring-4 ring-blue-100' : 'bg-slate-100 text-slate-500 border border-slate-200 group-hover:bg-blue-50 group-hover:text-blue-600 group-hover:border-blue-200'} flex items-center justify-center text-xs font-black">
                    ${index + 1}
                </div>
                <div>
                    <div class="flex items-center gap-1.5">
                        <h4 class="text-xs ${isCurrent ? 'font-black text-blue-900' : 'font-bold text-slate-800'}">${lesson.title}</h4>
                        ${isCurrent ? '<span class="text-[10px] text-amber-700 font-bold bg-amber-100 px-1.5 rounded">In Progress</span>' : ''}
                    </div>
                    <p class="text-[11px] ${isCurrent ? 'text-blue-700 font-semibold' : 'text-slate-500 font-medium'}">${lesson.description}</p>
                </div>
            </div>
            ${isCurrent ? '<span class="text-[10px] font-black uppercase text-blue-700 px-2.5 py-1 rounded-full bg-white border border-blue-200 shadow-2xs">LEARN</span>' : '<span class="material-symbols-outlined text-slate-400 text-[18px]">chevron_right</span>'}
        `;
        container.appendChild(card);
    });
}

window.openLessonModal = function(method, index) {
    const lesson = window.LESSONS_DATA[method][index];
    if (!lesson) return;
    
    document.getElementById("lessonModalTitle").innerText = lesson.title;
    document.getElementById("lessonModalContent").innerHTML = lesson.htmlContent;
    
    document.getElementById("lessonModal").classList.remove("hidden");
};

window.closeLessonModal = function() {
    document.getElementById("lessonModal").classList.add("hidden");
};

function updateUI(data) {
    if (!data) return;
    
    // Update labels
    const methodBadge = document.getElementById("methodBadge");
    if (methodBadge) methodBadge.innerText = data.method.toUpperCase();
    
    const stepTitle = document.getElementById("stepTitle");
    if (stepTitle) stepTitle.innerText = data.current_step;
    
    const stepDescription = document.getElementById("stepDescription");
    if (stepDescription) stepDescription.innerText = data.instructions || "Keep going! Follow the algorithms for this step.";

    // Update Progress
    const progressPercentage = document.getElementById("progressPercentage");
    if (progressPercentage) progressPercentage.innerText = Math.round(data.progress_percentage) + "%";
    
    const progressBar = document.getElementById("progressBar");
    if (progressBar) progressBar.style.width = Math.round(data.progress_percentage) + "%";

    // Update 3D Cube
    if (window.updateCubeColors && data.facelet_string) {
        window.updateCubeColors(data.facelet_string);
    }
    
    // Update Quest Track UI
    renderQuestTrack(data.current_step);
}

window.addEventListener('DOMContentLoaded', initSession);




window.activeTutorial = null;

window.startGuidedScenario = async function(setupScramble, solutionMoves, title) {
    if (window.closeLessonModal) window.closeLessonModal();
    // Reset session and apply setup
    await initSession();
    await fetch('/api/sessions/' + currentSessionId + '/moves', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ sequence: setupScramble })
    });
    
    window.activeTutorial = {
        title: title,
        solution: solutionMoves,
        currentIndex: 0
    };
    
    document.getElementById('tutorHud').classList.remove('hidden');
    document.getElementById('tutorTitle').innerText = title;
    updateTutorUI();
};

function updateTutorUI() {
    if (!window.activeTutorial) return;
    const tut = window.activeTutorial;
    const nextMoveEl = document.getElementById('tutorNextMove');
    if (tut.currentIndex >= tut.solution.length) {
        nextMoveEl.innerText = "DONE!";
        nextMoveEl.classList.replace('text-amber-400', 'text-emerald-400');
        setTimeout(() => exitTutorMode(), 3000);
        return;
    }
    nextMoveEl.innerText = tut.solution[tut.currentIndex];
    if (nextMoveEl.classList.contains('text-emerald-400')) {
        nextMoveEl.classList.replace('text-emerald-400', 'text-amber-400');
    }
    if (nextMoveEl.classList.contains('text-red-400')) {
        nextMoveEl.classList.replace('text-red-400', 'text-amber-400');
    }
}

window.exitTutorMode = function() {
    window.activeTutorial = null;
    document.getElementById('tutorHud').classList.add('hidden');
};

