from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import uuid

from engine.cube import Cube
from tutor.session import TutorSession
from tutor.methods import get_beginner_method, get_cfop_method, get_roux_method, get_zz_method
from api.models import SessionCreateRequest, MoveRequest, HintResponse, SessionStateResponse


app = FastAPI(title="CubeCraft API", description="Interactive Speedcubing Tutor Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local frontend development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

# In-memory session store
sessions: Dict[str, TutorSession] = {}


def build_method(name: str):
    name = name.lower()
    if name == "cfop":
        return get_cfop_method()
    elif name == "roux":
        return get_roux_method()
    elif name == "zz":
        return get_zz_method()
    else:
        return get_beginner_method()


def format_state(session_id: str, session: TutorSession) -> SessionStateResponse:
    step = session.tracker.current_step()
    return SessionStateResponse(
        session_id=session_id,
        facelet_string=session.cube.to_facelet_string(),
        method=session.method.name,
        current_step=step.name if step else "Solved",
        instructions=session.get_current_instructions(),
        progress_percentage=session.progress_percentage(),
        is_solved=session.is_solved()
    )


@app.post("/api/sessions", response_model=SessionStateResponse)
def create_session(request: SessionCreateRequest):
    method = build_method(request.method)
    cube = Cube()
    
    if request.scramble_sequence:
        try:
            cube.apply_sequence(request.scramble_sequence)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid scramble sequence: {str(e)}")
            
    session = TutorSession(method, cube)
    session_id = str(uuid.uuid4())
    sessions[session_id] = session
    
    return format_state(session_id, session)


@app.get("/api/sessions/{session_id}", response_model=SessionStateResponse)
def get_session_state(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return format_state(session_id, sessions[session_id])


@app.post("/api/sessions/{session_id}/moves", response_model=SessionStateResponse)
def apply_move(session_id: str, request: MoveRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session = sessions[session_id]
    
    try:
        if request.sequence:
            session.apply_sequence(request.sequence)
        elif request.move:
            session.apply_move(request.move)
        else:
            raise HTTPException(status_code=400, detail="Must provide 'move' or 'sequence'")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return format_state(session_id, session)


@app.get("/api/sessions/{session_id}/hint", response_model=HintResponse)
def get_hint(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session = sessions[session_id]
    hint_sequence = session.get_hint()
    return HintResponse(hint=hint_sequence)
