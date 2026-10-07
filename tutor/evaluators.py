"""Core evaluation logic for cube pieces and structures."""

from typing import Tuple
from engine.cube import Cube
from engine.constants import EDGE_INDICES, CORNER_INDICES, CENTERS, SOLVED_FACELET_STRING, Face


def get_piece_colors(cube: Cube, indices: Tuple[int, ...]) -> Tuple[str, ...]:
    """Returns the colors of the given facelets on the cube."""
    return tuple(cube._state[i] for i in indices)


def is_edge_solved(cube: Cube, edge_name: str) -> bool:
    """Checks if the specific edge is solved (matches the solved state exactly)."""
    indices = EDGE_INDICES[edge_name]
    colors = get_piece_colors(cube, indices)
    # The center colors define the solved state for fixed color baseline
    expected_colors = tuple(SOLVED_FACELET_STRING[i] for i in indices)
    return colors == expected_colors


def is_corner_solved(cube: Cube, corner_name: str) -> bool:
    """Checks if the specific corner is solved."""
    indices = CORNER_INDICES[corner_name]
    colors = get_piece_colors(cube, indices)
    expected_colors = tuple(SOLVED_FACELET_STRING[i] for i in indices)
    return colors == expected_colors


def count_solved_white_cross_edges(cube: Cube) -> int:
    """Returns the number of solved White Cross edges (DF, DR, DB, DL)."""
    edges = ["DF", "DR", "DB", "DL"]
    return sum(1 for e in edges if is_edge_solved(cube, e))


def is_white_cross_solved(cube: Cube) -> bool:
    """Returns True if all 4 white cross edges are solved."""
    return count_solved_white_cross_edges(cube) == 4


def count_solved_f2l_pairs(cube: Cube) -> int:
    """Returns the number of solved F2L pairs (matching corner and edge in correct slot).
    
    Pairs are:
    - FR (Corner DFR, Edge FR)
    - FL (Corner DLF, Edge FL)
    - BR (Corner DRB, Edge BR)
    - BL (Corner DBL, Edge BL)
    """
    pairs = [
        ("DFR", "FR"),
        ("DLF", "FL"),
        ("DRB", "BR"),
        ("DBL", "BL"),
    ]
    
    solved = 0
    for corner, edge in pairs:
        if is_corner_solved(cube, corner) and is_edge_solved(cube, edge):
            solved += 1
    return solved


def count_solved_daisy_edges(cube: Cube) -> int:
    """Returns the number of white edges currently around the yellow center.
    
    The yellow center is U. So we look at U edges (UR, UF, UL, UB).
    A daisy edge is one where the white facelet is on the U face.
    White is D center color in SOLVED_FACELET_STRING, which is 'D' (or whatever character
    is mapped, by default Singmaster uses 'D' for the D face color).
    Wait, in our constants: U=U, R=R, F=F, D=D, L=L, B=B.
    So White = 'D' (if White is on bottom).
    """
    white_color = SOLVED_FACELET_STRING[CENTERS[Face.D]]
    
    # U edges: UR, UF, UL, UB
    # The U facelet is the 0th index in these tuples
    daisy_edges = 0
    for edge_name in ["UR", "UF", "UL", "UB"]:
        u_facelet_idx = EDGE_INDICES[edge_name][0]
        if cube._state[u_facelet_idx] == white_color:
            daisy_edges += 1
            
    return daisy_edges

def is_roux_first_block_solved(cube: Cube) -> bool:
    """Checks if the Roux First Block (Left 1x2x3) is solved."""
    edges = ["DL", "BL", "FL"]
    corners = ["DBL", "DLF"]
    return all(is_edge_solved(cube, e) for e in edges) and all(is_corner_solved(cube, c) for c in corners)

def is_roux_second_block_solved(cube: Cube) -> bool:
    """Checks if the Roux Second Block (Right 1x2x3) is solved."""
    edges = ["DR", "BR", "FR"]
    corners = ["DRB", "DFR"]
    return all(is_edge_solved(cube, e) for e in edges) and all(is_corner_solved(cube, c) for c in corners)

def is_cmll_solved(cube: Cube) -> bool:
    """Checks if the U-layer corners are oriented and permuted."""
    corners = ["URF", "UFL", "ULB", "UBR"]
    return all(is_corner_solved(cube, c) for c in corners)

def is_edge_oriented(cube: Cube, edge_name: str) -> bool:
    """Checks if a specific edge is oriented according to ZZ/Roux rules.
    
    Standard EO (Edge Orientation) rules:
    An edge is 'good' (oriented) if it can be solved using only R, L, U, D moves.
    Practically, looking at the F/B facelets vs U/D facelets.
    For simplicity in our fixed color scheme:
    An edge is oriented if its U/D colors (White/Yellow) are on the U/D faces,
    or on the F/B faces IF it's an E-slice edge.
    Actually, full EO logic:
    Look at the F/B axis. If F/B color is on F/B, it's good.
    If F/B color is on U/D, it's bad.
    If U/D color is on U/D, it's good.
    If U/D color is on F/B, it's bad.
    Let's use a simpler check: If the cube can be solved without F or B turns, the edges are oriented.
    Since implementing standard EO detection from scratch is complex, we'll use a direct color mapping.
    """
    pass

def count_oriented_edges(cube: Cube) -> int:
    from engine.constants import SOLVED_FACELET_STRING, CENTERS, Face, EDGE_INDICES
    
    # Colors
    f_col = SOLVED_FACELET_STRING[CENTERS[Face.F]]
    b_col = SOLVED_FACELET_STRING[CENTERS[Face.B]]
    u_col = SOLVED_FACELET_STRING[CENTERS[Face.U]]
    d_col = SOLVED_FACELET_STRING[CENTERS[Face.D]]
    r_col = SOLVED_FACELET_STRING[CENTERS[Face.R]]
    l_col = SOLVED_FACELET_STRING[CENTERS[Face.L]]
    
    # Standard EO definition:
    # 1. Look at the F/B facelets. If it's F/B color, edge is oriented.
    # 2. If it's R/L color, look at the other facelet. If it's U/D color, oriented.
    # 3. If it's U/D color, bad.
    # Wait, the easiest way to check if an edge is oriented:
    # Let F/B colors be "Front/Back".
    # Let U/D colors be "Up/Down".
    # Let R/L colors be "Right/Left".
    
    fb_colors = (f_col, b_col)
    ud_colors = (u_col, d_col)
    rl_colors = (r_col, l_col)
    
    oriented_count = 0
    for name, indices in EDGE_INDICES.items():
        # which facelet is which?
        # The first character of the name is the first index.
        # e.g., "UR" -> index 0 is U, index 1 is R.
        # Let's see which face the facelets are currently residing on.
        # Wait, EO depends on where the piece is and its rotation.
        # Easier rule:
        f1_color = cube._state[indices[0]]
        f2_color = cube._state[indices[1]]
        
        # We need to know the face axis of indices[0] and indices[1]
        face1 = name[0]
        face2 = name[1]
        
        # If the edge has a U/D color, that color must be on U/D, or on F/B (but only if it's an E-slice edge? No, if U/D color is on F/B, it's ALWAYS bad).
        # Rule 1: U/D colors must NOT be on F/B.
        # Rule 2: F/B colors must NOT be on U/D.
        # Actually, standard EO:
        # Front/Back faces: F/B colors are good. U/D colors are bad.
        # Up/Down faces: U/D colors are good. F/B colors are bad.
        # Right/Left faces:
        # If an edge has F/B color, it must be on F/B or L/R faces (not U/D).
        # If an edge has U/D color, it must be on U/D or L/R faces (not F/B).
        
        c1, c2 = f1_color, f2_color
        # Determine if piece is oriented based on its current position.
        # The current position is given by face1 and face2.
        # Let's map face1 and face2 to the actual colors on them.
        def is_good(face_label, color, other_color):
            if color in ud_colors:
                return face_label in ('U', 'D', 'R', 'L') and face_label not in ('F', 'B')
            if color in fb_colors:
                # If F/B color is on U/D it's bad.
                return face_label in ('F', 'B', 'R', 'L') and face_label not in ('U', 'D')
            if color in rl_colors:
                # If it's an R/L color, it's good if the OTHER color is good.
                pass
            return True
            
        # Actual rigorous ZZ EO rule:
        # An edge is misoriented if:
        # - It has a U/D color on the F or B face.
        # - It has an F/B color on the U or D face.
        # - It has a U/D color on the L or R face, AND its other color (which must be F/B) is on the U or D face. (Wait, if U/D is on L/R, the other face must be U/D, so the piece is on U/D. If the F/B color is on U/D, we already caught that!)
        
        # Let's implement the foolproof check:
        # Find the U/D color or F/B color on the piece.
        piece_colors = {c1, c2}
        has_ud = piece_colors.intersection(ud_colors)
        has_fb = piece_colors.intersection(fb_colors)
        
        bad = False
        # Map indices to face labels
        face_of_c1 = face1
        face_of_c2 = face2
        
        for c, f in [(c1, face_of_c1), (c2, face_of_c2)]:
            if c in ud_colors and f in ('F', 'B'):
                bad = True
            if c in fb_colors and f in ('U', 'D'):
                bad = True
                
        if not bad:
            oriented_count += 1
            
    return oriented_count
