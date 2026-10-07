"""Constants, Enums, and Mappings for the CubeCraft speedcube engine.

Defines standard Kociemba and Singmaster facelet ordering, color schemes,
face definitions, turn modifiers, and coordinate lookups.
"""

from enum import Enum
from typing import Dict, Final, List, Tuple


class Face(str, Enum):
    """The six outer faces of a 3x3 Rubik's cube."""
    U = "U"  # Up (Top)
    R = "R"  # Right
    F = "F"  # Front
    D = "D"  # Down (Bottom)
    L = "L"  # Left
    B = "B"  # Back


class Color(str, Enum):
    """Standard Western color scheme representation."""
    WHITE = "W"
    RED = "R"
    GREEN = "G"
    YELLOW = "Y"
    ORANGE = "O"
    BLUE = "B"


class Turn(str, Enum):
    """Singmaster turn modifier suffixes."""
    CLOCKWISE = ""
    COUNTER_CLOCKWISE = "'"
    HALF_TURN = "2"


class FaceAxis(str, Enum):
    """Opposite-face spatial axes for WCA cancellation detection."""
    UD = "UD"  # Up / Down axis
    RL = "RL"  # Right / Left axis
    FB = "FB"  # Front / Back axis


# Total facelets on a 3x3 cube
NUM_FACELETS: Final[int] = 54
NUM_FACES: Final[int] = 6
FACELETS_PER_FACE: Final[int] = 9

# Canonical Face Ordering: U, R, F, D, L, B (Indices 0 to 53)
FACE_ORDER: Final[Tuple[Face, ...]] = (
    Face.U,
    Face.R,
    Face.F,
    Face.D,
    Face.L,
    Face.B,
)

# Standard Color Mapping
FACE_TO_COLOR: Final[Dict[Face, Color]] = {
    Face.U: Color.WHITE,
    Face.R: Color.RED,
    Face.F: Color.GREEN,
    Face.D: Color.YELLOW,
    Face.L: Color.ORANGE,
    Face.B: Color.BLUE,
}

COLOR_TO_FACE: Final[Dict[Color, Face]] = {
    color: face for face, color in FACE_TO_COLOR.items()
}

COLOR_NAMES: Final[Dict[Color, str]] = {
    Color.WHITE: "White",
    Color.RED: "Red",
    Color.GREEN: "Green",
    Color.YELLOW: "Yellow",
    Color.ORANGE: "Orange",
    Color.BLUE: "Blue",
}

# Spatial Axis Mapping
FACE_TO_AXIS: Final[Dict[Face, FaceAxis]] = {
    Face.U: FaceAxis.UD,
    Face.D: FaceAxis.UD,
    Face.R: FaceAxis.RL,
    Face.L: FaceAxis.RL,
    Face.F: FaceAxis.FB,
    Face.B: FaceAxis.FB,
}

# Opposite Face Mapping
OPPOSITE_FACES: Final[Dict[Face, Face]] = {
    Face.U: Face.D,
    Face.D: Face.U,
    Face.R: Face.L,
    Face.L: Face.R,
    Face.F: Face.B,
    Face.B: Face.F,
}

# Index ranges for each face (each face has 9 facelets: 0 to 8 relative offset)
FACE_INDICES: Final[Dict[Face, range]] = {
    Face.U: range(0, 9),
    Face.R: range(9, 18),
    Face.F: range(18, 27),
    Face.D: range(27, 36),
    Face.L: range(36, 45),
    Face.B: range(45, 54),
}

# Center facelet index for each face
CENTER_INDICES: Final[Dict[Face, int]] = {
    Face.U: 4,
    Face.R: 13,
    Face.F: 22,
    Face.D: 31,
    Face.L: 40,
    Face.B: 49,
}

# Standard Singmaster / Kociemba Facelet Identifiers: U1..U9, R1..R9, etc.
FACELET_NAMES: Final[Tuple[str, ...]] = tuple(
    f"{face.value}{idx + 1}"
    for face in FACE_ORDER
    for idx in range(FACELETS_PER_FACE)
)

FACELET_LOOKUP: Final[Dict[str, int]] = {
    name: idx for idx, name in enumerate(FACELET_NAMES)
}

INDEX_TO_FACELET: Final[Dict[int, str]] = {
    idx: name for idx, name in enumerate(FACELET_NAMES)
}

# Solved State Strings
SOLVED_FACELET_STRING: Final[str] = "".join(
    face.value * FACELETS_PER_FACE for face in FACE_ORDER
)

SOLVED_COLOR_STRING: Final[str] = "".join(
    FACE_TO_COLOR[face].value * FACELETS_PER_FACE for face in FACE_ORDER
)


class Move(str, Enum):
    """Outer face moves, slice moves, and full-cube rotations."""
    # Outer Face Turns
    U = "U"
    U_PRIME = "U'"
    U2 = "U2"
    D = "D"
    D_PRIME = "D'"
    D2 = "D2"
    R = "R"
    R_PRIME = "R'"
    R2 = "R2"
    L = "L"
    L_PRIME = "L'"
    L2 = "L2"
    F = "F"
    F_PRIME = "F'"
    F2 = "F2"
    B = "B"
    B_PRIME = "B'"
    B2 = "B2"

    # Slice Turns
    M = "M"
    M_PRIME = "M'"
    M2 = "M2"
    E = "E"
    E_PRIME = "E'"
    E2 = "E2"
    S = "S"
    S_PRIME = "S'"
    S2 = "S2"

    # Full Cube Rotations
    X = "x"
    X_PRIME = "x'"
    X2 = "x2"
    Y = "y"
    Y_PRIME = "y'"
    Y2 = "y2"
    Z = "z"
    Z_PRIME = "z'"
    Z2 = "z2"

# --- Piece Index Mappings ---
# Centers (Index of the center facelet)
CENTERS = {
    Face.U: 4,
    Face.R: 13,
    Face.F: 22,
    Face.D: 31,
    Face.L: 40,
    Face.B: 49,
}

# Edges (Tuples of facelet indices)
EDGE_INDICES = {
    "UR": (5, 10),
    "UF": (7, 19),
    "UL": (3, 37),
    "UB": (1, 46),
    "DR": (32, 16),
    "DF": (28, 25),
    "DL": (30, 43),
    "DB": (34, 52),
    "FR": (23, 12),
    "FL": (21, 41),
    "BR": (48, 14),
    "BL": (50, 39),
}

# Corners (Tuples of facelet indices)
CORNER_INDICES = {
    "URF": (8, 9, 20),
    "UFL": (6, 18, 38),
    "ULB": (0, 36, 47),
    "UBR": (2, 45, 11),
    "DFR": (29, 26, 15),
    "DLF": (27, 44, 24),
    "DBL": (33, 53, 42),
    "DRB": (35, 17, 51),
}
