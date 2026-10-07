from typing import List, Optional
from pydantic import BaseModel, Field

class SessionCreateRequest(BaseModel):
    method: str = Field(
        default="beginner", 
        description="The solving method to use (e.g., 'beginner', 'cfop', 'roux', 'zz')."
    )
    scramble_sequence: Optional[str] = Field(
        default=None, 
        description="Optional initial scramble to apply to the cube."
    )

class MoveRequest(BaseModel):
    move: Optional[str] = Field(default=None, description="A single Singmaster move (e.g., 'R').")
    sequence: Optional[str] = Field(default=None, description="A space-separated sequence of moves (e.g., 'R U R'').")

class HintResponse(BaseModel):
    hint: List[str] = Field(description="Optimal sequence of moves to complete the current step.")

class SessionStateResponse(BaseModel):
    session_id: str
    facelet_string: str
    method: str
    current_step: str
    instructions: str
    progress_percentage: float
    is_solved: bool
