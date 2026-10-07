"""Tests for the TutorSession API and BFS engine."""

from engine.cube import Cube
from tutor.methods import get_beginner_method
from tutor.session import TutorSession


def test_tutor_session_initialization() -> None:
    method = get_beginner_method()
    session = TutorSession(method)
    
    assert session.is_solved()
    assert session.progress_percentage() == 100.0
    assert "Congratulations!" in session.get_current_instructions()


def test_tutor_session_cross_step() -> None:
    from tutor.methods import get_cfop_method
    method = get_cfop_method()
    cube = Cube()
    
    # Scramble the cross slightly by moving one edge out
    # R moves the White/Red edge out of the cross
    cube.apply_move("R")
    
    session = TutorSession(method, cube)
    
    # Current step should be White Cross.
    assert not session.is_solved()
    
    # It should mention Cross
    assert "Cross" in session.tracker.current_step().name
    
    # Get a hint
    hint = session.get_hint()
    # To restore the White/Red edge, "R'" is the optimal move.
    assert hint == ["R'"]


def test_bfs_search_optimal_cross() -> None:
    from tutor.search import bfs_search
    from tutor.methods.cfop import WhiteCrossStep
    
    cube = Cube()
    # Scramble the cross with 3 moves
    cube.apply_sequence("D' L2 F")
    
    step = WhiteCrossStep()
    assert not step.is_satisfied(cube)
    
    # BFS should find a <=3 move solution to restore the cross
    solution = bfs_search(cube, step, max_depth=4)
    assert solution is not None
    assert len(solution) <= 3
    
    # Apply solution and verify
    for m in solution:
        cube.apply_move(m)
    assert step.is_satisfied(cube)
