"""WCA-compliant random move scrambler for 3x3 Rubik's Cube.

Implements cancellation-free move sequence generation adhering to World Cube
Association (WCA) regulations:
- Default length of 20 moves.
- Prohibits consecutive moves on the same face (e.g. no R R' or R R2).
- Prohibits conflicting moves on opposite parallel faces without separation
  (e.g. no R L R or redundant axis cancellations).
"""

from __future__ import annotations

import random
from typing import List, Optional, Sequence, Tuple

from engine.constants import (
    Face,
    FACE_TO_AXIS,
    FaceAxis,
    Turn,
)
from engine.cube import Cube
from engine.moves import parse_move

# Standard modifiers for outer face moves
VALID_TURNS: Tuple[str, ...] = (
    Turn.CLOCKWISE.value,
    Turn.COUNTER_CLOCKWISE.value,
    Turn.HALF_TURN.value,
)

DEFAULT_SCRAMBLE_LENGTH: int = 20


def get_valid_next_faces(face_history: Sequence[Face]) -> List[Face]:
    """Determines all valid faces for the next move given the history.

    Rules:
    1. The immediate previous face cannot be repeated (prevents R R' or R R2).
    2. If the previous two moves were on the same axis (e.g. R then L),
       no further move on that axis is permitted until another axis intervenes
       (prevents R L R, R L L', etc.).
    """
    all_faces = list(Face)
    if not face_history:
        return all_faces

    last_face = face_history[-1]
    last_axis = FACE_TO_AXIS[last_face]

    # Rule 1: No consecutive move on the same face
    valid_faces = [f for f in all_faces if f != last_face]

    # Rule 2: If the previous two moves shared the same axis, ban that entire axis
    if len(face_history) >= 2:
        second_last_axis = FACE_TO_AXIS[face_history[-2]]
        if second_last_axis == last_axis:
            valid_faces = [f for f in valid_faces if FACE_TO_AXIS[f] != last_axis]

    return valid_faces


def generate_scramble(
    length: int = DEFAULT_SCRAMBLE_LENGTH,
    seed: Optional[int] = None,
) -> str:
    """Generates a WCA-compliant random move scramble sequence.

    Args:
        length: Number of moves in the scramble (default 20).
        seed: Optional integer seed for deterministic generation.

    Returns:
        Space-separated Singmaster move string (e.g. "R U2 L' D F2 ...").
    """
    if length < 0:
        raise ValueError("Scramble length cannot be negative")
    if length == 0:
        return ""

    rng = random.Random(seed)
    face_history: List[Face] = []
    move_tokens: List[str] = []

    for _ in range(length):
        valid_faces = get_valid_next_faces(face_history)
        chosen_face = rng.choice(valid_faces)
        chosen_turn = rng.choice(VALID_TURNS)

        face_history.append(chosen_face)
        move_tokens.append(f"{chosen_face.value}{chosen_turn}")

    return " ".join(move_tokens)


def validate_scramble(scramble: str) -> bool:
    """Validates that a scramble string adheres to WCA cancellation rules.

    Checks:
    - Every move is a valid outer face turn (U, D, F, B, L, R with '', ''', '2').
    - No two consecutive moves operate on the same face.
    - No three consecutive moves operate on the same axis (prevents sandwich cancellations like R L R).
    """
    cleaned = scramble.strip()
    if not cleaned:
        return True

    tokens = cleaned.split()
    faces: List[Face] = []

    for token in tokens:
        try:
            base, modifier = parse_move(token)
            face = Face(base)
            if modifier not in VALID_TURNS:
                return False
            faces.append(face)
        except (ValueError, KeyError):
            return False

    # Check cancellation conditions
    for i in range(1, len(faces)):
        # Condition 1: Consecutive same face
        if faces[i] == faces[i - 1]:
            return False

        # Condition 2: 3 consecutive on the same axis (e.g. R L R)
        if i >= 2:
            axis0 = FACE_TO_AXIS[faces[i - 2]]
            axis1 = FACE_TO_AXIS[faces[i - 1]]
            axis2 = FACE_TO_AXIS[faces[i]]
            if axis0 == axis1 == axis2:
                return False

    return True


class Scrambler:
    """Scrambler utility class for generating scrambles and scrambling Cubes."""

    def __init__(self, seed: Optional[int] = None) -> None:
        self._seed = seed

    def generate(self, length: int = DEFAULT_SCRAMBLE_LENGTH) -> str:
        """Generates a scramble using the configured seed."""
        return generate_scramble(length=length, seed=self._seed)

    def scramble_cube(
        self,
        cube: Optional[Cube] = None,
        length: int = DEFAULT_SCRAMBLE_LENGTH,
    ) -> Tuple[str, Cube]:
        """Applies a newly generated scramble to a cube (or fresh cube).

        Returns:
            Tuple of (scramble_string, scrambled_cube).
        """
        target = cube.clone() if cube is not None else Cube()
        scramble_str = self.generate(length=length)
        if scramble_str:
            target.apply_sequence(scramble_str)
        return scramble_str, target
