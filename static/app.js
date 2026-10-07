let currentSessionId = null;

async function initSession() {
    try {
        const activeMethod = localStorage.getItem('activeMethod') || 'cfop';
        console.log("Initializing session with method:", activeMethod);
        
        const response = await fetch('/api/sessions', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ method: activeMethod })
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
    const moves = ["R", "U", "F", "B", "L", "D", "R'", "U'", "F'", "B'", "L'", "D'", "R2", "U2", "F2", "B2", "L2", "D2"];
    let scramble = [];
    for(let i=0; i<20; i++) {
        scramble.push(moves[Math.floor(Math.random() * moves.length)]);
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
}

window.addEventListener('DOMContentLoaded', initSession);
