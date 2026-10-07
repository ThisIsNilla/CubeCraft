"""ZZ Method Step Definitions."""

from engine.cube import Cube
from tutor.framework import BaseStep
from tutor.evaluators import (
    count_oriented_edges,
    is_edge_solved,
    count_solved_f2l_pairs
)


class EOLineStep(BaseStep):
    def __init__(self):
        super().__init__("EOLine", "Orient all 12 edges and place the DF and DB edges.")

    def is_satisfied(self, cube: Cube) -> bool:
        if count_oriented_edges(cube) != 12:
            return False
        return is_edge_solved(cube, "DF") and is_edge_solved(cube, "DB")


class ZZF2LStep(BaseStep):
    def __init__(self):
        super().__init__("ZZ F2L", "Solve the left and right 1x2x3 blocks using only R, L, U.")

    def is_satisfied(self, cube: Cube) -> bool:
        # F2L is solved if all 4 pairs are solved
        return count_solved_f2l_pairs(cube) == 4


class LLStep(BaseStep):
    def __init__(self):
        super().__init__("Last Layer", "Solve the remaining Last Layer pieces.")

    def is_satisfied(self, cube: Cube) -> bool:
        return cube.is_solved(allow_rotation=True)
