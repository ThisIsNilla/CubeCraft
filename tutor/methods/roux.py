"""Roux Method Step Definitions."""

from engine.cube import Cube
from tutor.framework import BaseStep
from tutor.evaluators import (
    is_roux_first_block_solved,
    is_roux_second_block_solved,
    is_cmll_solved,
    count_oriented_edges
)


class FirstBlockStep(BaseStep):
    def __init__(self):
        super().__init__("First Block", "Build a 1x2x3 block on the left side.")

    def is_satisfied(self, cube: Cube) -> bool:
        return is_roux_first_block_solved(cube)


class SecondBlockStep(BaseStep):
    def __init__(self):
        super().__init__("Second Block", "Build a 1x2x3 block on the right side.")

    def is_satisfied(self, cube: Cube) -> bool:
        return is_roux_second_block_solved(cube)


class CMLLStep(BaseStep):
    def __init__(self):
        super().__init__("CMLL", "Orient and permute the remaining 4 corners.")

    def is_satisfied(self, cube: Cube) -> bool:
        return is_cmll_solved(cube)


class LSEStep(BaseStep):
    def __init__(self):
        super().__init__("Last Six Edges", "Solve the remaining 6 edges using only M and U moves.")

    def is_satisfied(self, cube: Cube) -> bool:
        return cube.is_solved(allow_rotation=True)
