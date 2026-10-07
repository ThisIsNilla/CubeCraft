"""CFOP Method Step Definitions."""

from engine.cube import Cube
from tutor.framework import BaseStep
from tutor.evaluators import (
    is_white_cross_solved,
    count_solved_white_cross_edges,
    count_solved_f2l_pairs,
)


class WhiteCrossStep(BaseStep):
    def __init__(self):
        super().__init__("White Cross", "Solve the 4 white cross edges around the white center.")

    def is_satisfied(self, cube: Cube) -> bool:
        return is_white_cross_solved(cube)

    def get_guide_text(self, cube: Cube) -> str:
        count = count_solved_white_cross_edges(cube)
        if count == 0:
            return "Let's start the White Cross. Look for an edge piece with white on it."
        elif count < 4:
            return f"You have {count} cross edges solved. Keep going!"
        else:
            return "Cross is solved!"


class F2LPairStep(BaseStep):
    def __init__(self, target_pairs: int):
        super().__init__(
            f"F2L Pair {target_pairs}", 
            f"Solve {target_pairs} First Two Layers corner/edge pairs."
        )
        self.target_pairs = target_pairs

    def is_satisfied(self, cube: Cube) -> bool:
        return count_solved_f2l_pairs(cube) >= self.target_pairs

    def get_guide_text(self, cube: Cube) -> str:
        current = count_solved_f2l_pairs(cube)
        return f"You have {current} F2L pairs solved. Let's find pieces for pair {self.target_pairs}."


class OLLStep(BaseStep):
    def __init__(self):
        super().__init__("OLL", "Orient the Last Layer so the entire top face is yellow.")

    def is_satisfied(self, cube: Cube) -> bool:
        # Check if U face is entirely yellow.
        # Yellow is the U center color.
        from engine.constants import FACE_INDICES, Face, SOLVED_FACELET_STRING, CENTERS
        yellow_color = SOLVED_FACELET_STRING[CENTERS[Face.U]]
        u_indices = FACE_INDICES[Face.U]
        return all(cube._state[i] == yellow_color for i in u_indices)

    def get_guide_text(self, cube: Cube) -> str:
        return "Now it's time for OLL. Look at the yellow pattern on top and apply the appropriate algorithm."


class PLLStep(BaseStep):
    def __init__(self):
        super().__init__("PLL", "Permute the Last Layer to completely solve the cube.")

    def is_satisfied(self, cube: Cube) -> bool:
        # The cube is completely solved (with potential AUF / U rotation allowance).
        return cube.is_solved(allow_rotation=True)

    def get_guide_text(self, cube: Cube) -> str:
        return "Last step! Permute the top layer pieces to match the side faces."
