"""Tests for OLL and PLL algorithmic detection."""

from engine.cube import Cube
from tutor.algorithms import get_oll_hint, get_pll_hint


def test_oll_sune_detection() -> None:
    cube = Cube()
    # Sune algorithm: R U R' U R U2 R'
    # To set up a Sune, we apply the inverse of Sune to a solved cube.
    cube.apply_sequence("R U2 R' U' R U' R'")
    
    # Check that OLL detection finds Sune
    hint = get_oll_hint(cube)
    assert hint is not None
    
    # We apply the hint and check if OLL is solved
    for move in hint:
        cube.apply_move(move)
        
    # OLL is solved if the entire U face is yellow (center is U5=4)
    # The absolute colors of U face should be the U center color.
    from engine.constants import FACE_INDICES, Face, SOLVED_FACELET_STRING, CENTERS
    yellow = SOLVED_FACELET_STRING[CENTERS[Face.U]]
    for i in FACE_INDICES[Face.U]:
        assert cube._state[i] == yellow


def test_pll_t_perm_detection_with_auf() -> None:
    cube = Cube()
    # Apply a T-Perm, but with a U rotation before and a U' rotation after
    cube.apply_sequence("U R U R' U' R' F R2 U' R' U' R U R' F' U'")
    
    hint = get_pll_hint(cube)
    assert hint is not None
    
    for move in hint:
        cube.apply_move(move)
        
    # The cube should be completely solved
    assert cube.is_solved(allow_rotation=True)


def test_oll_pi_detection_with_auf() -> None:
    cube = Cube()
    # Setup Pi: Inverse of R U2 R2 U' R2 U' R2 U2 R -> R' U2 R2 U R2 U R2 U2 R'
    # Plus an AUF
    cube.apply_sequence("U2 R' U2 R2 U R2 U R2 U2 R'")
    
    hint = get_oll_hint(cube)
    assert hint is not None
    
    for move in hint:
        cube.apply_move(move)
        
    from engine.constants import FACE_INDICES, Face, SOLVED_FACELET_STRING, CENTERS
    yellow = SOLVED_FACELET_STRING[CENTERS[Face.U]]
    for i in FACE_INDICES[Face.U]:
        assert cube._state[i] == yellow
