"""Breadth-First Search engine for generating optimal hints."""

from typing import List, Optional
from collections import deque
from engine.cube import Cube
from tutor.framework import StepEvaluator


# Standard outer face quarter and half turns
DEFAULT_MOVES = [
    "U", "U'", "U2",
    "D", "D'", "D2",
    "F", "F'", "F2",
    "B", "B'", "B2",
    "L", "L'", "L2",
    "R", "R'", "R2"
]


def bfs_search(cube: Cube, target_step: StepEvaluator, max_depth: int = 8, allowed_moves: List[str] = None) -> Optional[List[str]]:
    """Performs a Breadth-First Search to find the shortest sequence to satisfy the step.
    
    Args:
        cube: The current state of the cube.
        target_step: The evaluator whose is_satisfied() we want to trigger.
        max_depth: Maximum number of moves to explore (defaults to 8 for fast Cross solutions).
        allowed_moves: List of move strings to branch on (defaults to outer face turns).
        
    Returns:
        A list of move strings (e.g., ["R", "U", "R'"]) if a solution is found, or None.
    """
    if target_step.is_satisfied(cube):
        return []

    if allowed_moves is None:
        allowed_moves = DEFAULT_MOVES

    # Queue stores tuples of (cube_state_string, list_of_moves_so_far)
    initial_state = cube.to_facelet_string()
    queue = deque([(initial_state, [])])
    
    # Visited set to avoid cycles and redundant paths
    visited = {initial_state}
    
    # We need a working cube object to apply moves to avoid constant instantiation
    # But since we evaluate strings, we can just deserialize, or use the working cube.
    # Actually, apply_move is fast, but doing it in a tight loop is key.
    
    while queue:
        current_state_str, path = queue.popleft()
        
        if len(path) >= max_depth:
            continue
            
        # Reconstruct cube state
        working_cube = Cube()
        working_cube._state = list(current_state_str)
        
        # Last move face to prevent redundant moves (e.g., R followed by R')
        last_move_face = path[-1][0] if path else None

        for move in allowed_moves:
            # Simple pruning: don't turn the same face twice in a row
            if move[0] == last_move_face:
                continue

            # Apply move
            next_cube = working_cube.clone()
            next_cube.apply_move(move)
            
            # Check if target is satisfied
            if target_step.is_satisfied(next_cube):
                return path + [move]
                
            next_state_str = next_cube.to_facelet_string()
            if next_state_str not in visited:
                visited.add(next_state_str)
                queue.append((next_state_str, path + [move]))

    return None
