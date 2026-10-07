"""Tests for Roux and ZZ method step evaluations."""

from engine.cube import Cube
from tutor.methods import get_roux_method, get_zz_method
from tutor.session import TutorSession

def test_roux_first_block() -> None:
    method = get_roux_method()
    cube = Cube()
    
    # Solved cube satisfies Roux First Block
    assert method.steps[0].is_satisfied(cube)
    
    # Break left block
    cube.apply_move("L")
    assert not method.steps[0].is_satisfied(cube)

def test_zz_eo_line() -> None:
    method = get_zz_method()
    cube = Cube()
    
    # Solved cube satisfies EOLine
    assert method.steps[0].is_satisfied(cube)
    
    # F turn misorients 4 edges (UR, UF, UL, DF) and displaces DF
    cube.apply_move("F")
    assert not method.steps[0].is_satisfied(cube)
    
    # U turn preserves EO but displaces edges. Wait, EOLine also requires DF and DB to be placed.
    cube.apply_move("F'") # restore
    cube.apply_move("U") 
    # EO is preserved (12 edges oriented), but DF and DB are still placed? 
    # Yes, U does not affect DF and DB.
    # So EOLine should STILL be satisfied!
    assert method.steps[0].is_satisfied(cube)
