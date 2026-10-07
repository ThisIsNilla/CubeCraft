"""Core Cube class representing a 3x3 Rubik's cube state and transitions.

Follows standard Kociemba / Singmaster facelet ordering (54 facets):
U1..U9, R1..R9, F1..F9, D1..D9, L1..L9, B1..B9 (Indices 0 to 53).
"""

from __future__ import annotations

import re
from typing import List, Sequence, Tuple, Union

from engine.constants import (
    CENTER_INDICES,
    COLOR_TO_FACE,
    Color,
    Face,
    FACE_INDICES,
    FACE_ORDER,
    FACE_TO_COLOR,
    NUM_FACELETS,
    SOLVED_COLOR_STRING,
    SOLVED_FACELET_STRING,
)
from engine.moves import get_move_permutation
from engine.parser import parse_algorithm


class Cube:
    """Represents a 3x3x3 Rubik's Cube state using a 54-facelet array.

    Facets 0..8:   Up (U) face
    Facets 9..17:  Right (R) face
    Facets 18..26: Front (F) face
    Facets 27..35: Down (D) face
    Facets 36..44: Left (L) face
    Facets 45..53: Back (B) face
    """

    def __init__(self, state: Union[Sequence[str], str, None] = None) -> None:
        """Initializes cube state.

        Defaults to solved reference state if None.
        """
        if state is None:
            self._state: List[str] = list(SOLVED_FACELET_STRING)
        elif isinstance(state, str):
            if len(state) != NUM_FACELETS:
                raise ValueError(
                    f"State string must have exactly {NUM_FACELETS} facelets, got {len(state)}"
                )
            self._state = list(state)
        elif isinstance(state, (list, tuple)):
            if len(state) != NUM_FACELETS:
                raise ValueError(
                    f"State sequence must have exactly {NUM_FACELETS} facelets, got {len(state)}"
                )
            self._state = [str(x) for x in state]
        else:
            raise TypeError(f"Unsupported state type: {type(state)}")

    @classmethod
    def from_colors(cls, color_string: str) -> Cube:
        """Creates a Cube from a 54-character Western color string (W, R, G, Y, O, B)."""
        if len(color_string) != NUM_FACELETS:
            raise ValueError(
                f"Color string must have {NUM_FACELETS} characters, got {len(color_string)}"
            )
        facelets = [
            COLOR_TO_FACE[Color(char)].value if char in [c.value for c in Color] else char
            for char in color_string
        ]
        return cls(facelets)

    @property
    def state(self) -> Tuple[str, ...]:
        """Immutable view of current 54 facelet values."""
        return tuple(self._state)

    def clone(self) -> Cube:
        """Creates an independent deep copy of this Cube."""
        return Cube(list(self._state))

    def reset(self) -> Cube:
        """Resets the cube to the solved reference state."""
        self._state = list(SOLVED_FACELET_STRING)
        return self

    def apply_move(self, notation: str) -> Cube:
        """Applies a single Singmaster move notation in-place.

        Returns self for fluent method chaining.
        """
        perm = get_move_permutation(notation)
        self._state = [self._state[perm[i]] for i in range(NUM_FACELETS)]
        return self

    def apply_sequence(self, algorithm: str) -> Cube:
        """Applies a sequence of Singmaster moves to the cube.

        Returns self for fluent method chaining.
        """
        moves = parse_algorithm(algorithm)
        for move in moves:
            self.apply_move(move)
        return self

    def is_solved(self, allow_rotation: bool = False) -> bool:
        """Checks if the cube is currently in a solved state.

        Args:
            allow_rotation: If False (default), the cube must match the canonical
                reference orientation (U=White/U, R=Red/R, etc.).
                If True, allows any whole-cube orientation as long as every face
                is monochromatic and all 6 face colors are distinct.
        """
        if not allow_rotation:
            current = self.to_facelet_string()
            if current == SOLVED_FACELET_STRING:
                return True
            if current == SOLVED_COLOR_STRING:
                return True
            # Check if canonical faces match their respective solved letters/colors
            canonical_match = True
            for face in FACE_ORDER:
                face_chars = [self._state[i] for i in FACE_INDICES[face]]
                expected_char = face.value
                expected_color = FACE_TO_COLOR[face].value
                if not all(c == expected_char or c == expected_color for c in face_chars):
                    canonical_match = False
                    break
            if canonical_match:
                return True
            return False

        # If allow_rotation is True:
        # Check that all 9 facelets on each of the 6 faces are identical
        seen_face_values = set()
        for face in FACE_ORDER:
            face_chars = [self._state[i] for i in FACE_INDICES[face]]
            first_char = face_chars[0]
            if not all(c == first_char for c in face_chars):
                return False
            seen_face_values.add(first_char)

        # All 6 faces must have distinct facelet values
        return len(seen_face_values) == 6

    def to_facelet_string(self) -> str:
        """Returns 54-character string of face letters (U, R, F, D, L, B)."""
        return "".join(self._state)

    def to_color_string(self) -> str:
        """Returns 54-character string mapped to standard Western colors (W, R, G, Y, O, B)."""
        result = []
        for char in self._state:
            # If already a Color enum value
            if char in [c.value for c in Color]:
                result.append(char)
            # If a Face enum value
            elif char in [f.value for f in Face]:
                result.append(FACE_TO_COLOR[Face(char)].value)
            else:
                result.append(char)
        return "".join(result)

    def face_facelets(self, face: Face) -> List[str]:
        """Returns the 9 facelets belonging to the specified face."""
        return [self._state[i] for i in FACE_INDICES[face]]

    def face_2d(self, face: Face) -> List[List[str]]:
        """Returns the 3x3 grid of facelets for the specified face."""
        items = self.face_facelets(face)
        return [items[0:3], items[3:6], items[6:9]]

    def center_facelet(self, face: Face) -> str:
        """Returns the center facelet for the specified face."""
        return self._state[CENTER_INDICES[face]]

    def net_string(self) -> str:
        """Returns an ASCII unfolded net representation of the cube.

                 U U U
                 U U U
                 U U U
           L L L F F F R R R B B B
           L L L F F F R R R B B B
           L L L F F F R R R B B B
                 D D D
                 D D D
                 D D D
        """
        u = self.face_2d(Face.U)
        l = self.face_2d(Face.L)
        f = self.face_2d(Face.F)
        r = self.face_2d(Face.R)
        b = self.face_2d(Face.B)
        d = self.face_2d(Face.D)

        lines: List[str] = []
        # U face
        for row in u:
            lines.append("      " + " ".join(row))
        # Lateral faces (L, F, R, B)
        for r_idx in range(3):
            line = (
                " ".join(l[r_idx])
                + " "
                + " ".join(f[r_idx])
                + " "
                + " ".join(r[r_idx])
                + " "
                + " ".join(b[r_idx])
            )
            lines.append(line)
        # D face
        for row in d:
            lines.append("      " + " ".join(row))

        return "\n".join(lines)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cube):
            return self._state == other._state
        if isinstance(other, str):
            return (
                self.to_facelet_string() == other or self.to_color_string() == other
            )
        if isinstance(other, (list, tuple)):
            return list(self._state) == list(other)
        return False

    def __repr__(self) -> str:
        return f"Cube('{self.to_facelet_string()}')"

    def __str__(self) -> str:
        return self.net_string()
