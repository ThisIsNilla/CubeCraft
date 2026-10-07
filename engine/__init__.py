"""CubeCraft Core Speedcubing Engine.

Milestone 1: The Core Permutation Engine, Scrambler, and Test Harness.
"""

from engine.constants import (
    CENTER_INDICES,
    COLOR_NAMES,
    COLOR_TO_FACE,
    Color,
    Face,
    FACE_INDICES,
    FACE_ORDER,
    FACE_TO_AXIS,
    FACE_TO_COLOR,
    FaceAxis,
    FACELET_LOOKUP,
    FACELET_NAMES,
    INDEX_TO_FACELET,
    Move,
    NUM_FACELETS,
    OPPOSITE_FACES,
    SOLVED_COLOR_STRING,
    SOLVED_FACELET_STRING,
    Turn,
)
from engine.cube import Cube
from engine.parser import parse_algorithm, invert_algorithm
from engine.moves import (
    compose_permutations,
    get_move_permutation,
    identity_permutation,
    invert_permutation,
    MOVE_PERMUTATIONS,
    normalize_move_token,
    parse_move,
    power_permutation,
)
from engine.scrambler import (
    DEFAULT_SCRAMBLE_LENGTH,
    generate_scramble,
    get_valid_next_faces,
    Scrambler,
    validate_scramble,
)

__all__ = [
    # Constants & Enums
    "Face",
    "Color",
    "Turn",
    "FaceAxis",
    "Move",
    "NUM_FACELETS",
    "FACE_ORDER",
    "FACE_TO_COLOR",
    "COLOR_TO_FACE",
    "COLOR_NAMES",
    "FACE_TO_AXIS",
    "OPPOSITE_FACES",
    "FACE_INDICES",
    "CENTER_INDICES",
    "FACELET_NAMES",
    "FACELET_LOOKUP",
    "INDEX_TO_FACELET",
    "SOLVED_FACELET_STRING",
    "SOLVED_COLOR_STRING",
    # Cube
    "Cube",
    "parse_algorithm",
    "invert_algorithm",
    # Moves & Permutations
    "identity_permutation",
    "compose_permutations",
    "invert_permutation",
    "power_permutation",
    "get_move_permutation",
    "parse_move",
    "normalize_move_token",
    "MOVE_PERMUTATIONS",
    # Scrambler
    "DEFAULT_SCRAMBLE_LENGTH",
    "generate_scramble",
    "validate_scramble",
    "get_valid_next_faces",
    "Scrambler",
]
