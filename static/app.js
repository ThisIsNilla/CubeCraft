let currentSessionId = null;

async function initSession() {
    try {
        const response = await fetch('/api/sessions', { method: 'POST' });
        const data = await response.json();
        currentSessionId = data.session_id;
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
            body: JSON.stringify({ moves: move })
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
    const moves = ["R", "U", "R'", "U'", "F", "B", "L", "D", "R2", "U2", "F2", "D2", "L2", "B2"];
    let scramble = [];
    for(let i=0; i<20; i++) {
        scramble.push(moves[Math.floor(Math.random() * moves.length)]);
    }
    
    try {
        const response = await fetch(`/api/sessions/${currentSessionId}/moves`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ moves: scramble.join(" ") })
        });
        const data = await response.json();
        updateUI(data);
        
        const badge = document.getElementById("lastExecutedMove");
        if (badge) badge.innerText = "SCRAMBLED";
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
        document.getElementById("stepDescription").innerHTML = `<strong>💡 Hint:</strong> Try the move <span class="text-blue-600 font-code-mono font-bold">${hintData.optimal_moves[0] || 'Already solved'}</span>`;
    } catch (e) {
        console.error(e);
    }
}

function updateUI(data) {
    if (!data.instructions) return;
    
    const { method, step_name, description } = data.instructions;
    
    document.getElementById("methodBadge").innerText = method;
    document.getElementById("stepTitle").innerText = step_name;
    document.getElementById("stepDescription").innerText = description || "Keep going! Follow the algorithms for this step.";
    
    // For the UI preview, we don't fully update the 3D cube colors yet, 
    // but the backend integration is live!
}

window.addEventListener('DOMContentLoaded', initSession);
