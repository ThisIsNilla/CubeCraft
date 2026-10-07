"""Beginner's Method Step Definitions."""

from engine.cube import Cube
from tutor.framework import BaseStep
from tutor.evaluators import (
    count_solved_daisy_edges,
    is_white_cross_solved,
    count_solved_white_cross_edges,
    count_solved_f2l_pairs,
    is_corner_solved,
    is_edge_solved,
)


class DaisyStep(BaseStep):
    def __init__(self):
        super().__init__("Daisy", "Surround the yellow center with 4 white edges.")

    def is_satisfied(self, cube: Cube) -> bool:
        return count_solved_daisy_edges(cube) == 4 or is_white_cross_solved(cube)

    def get_guide_text(self, cube: Cube) -> str:
        count = count_solved_daisy_edges(cube)
        return f"You have {count} white edges forming the Daisy. Find another and bring it to the top."


# We can reuse WhiteCrossStep from CFOP, but redefine it here for clarity if needed.
# For simplicity, we'll just import and use it in the method assembly, or rewrite it:
class WhiteCrossStep(BaseStep):
    def __init__(self):
        super().__init__("White Cross", "Move the daisy edges to the white center, matching the side colors.")

    def is_satisfied(self, cube: Cube) -> bool:
        return is_white_cross_solved(cube)

    def get_guide_text(self, cube: Cube) -> str:
        count = count_solved_white_cross_edges(cube)
        return f"You have {count} cross edges perfectly aligned. Line up the next daisy edge and turn it 180 degrees!"


class FirstLayerCornerStep(BaseStep):
    def __init__(self, target_count: int):
        super().__init__(f"First Layer Corners ({target_count}/4)", "Insert white corners to finish the first layer.")
        self.target_count = target_count

    def is_satisfied(self, cube: Cube) -> bool:
        corners = ["DFR", "DLF", "DBL", "DRB"]
        solved = sum(1 for c in corners if is_corner_solved(cube, c))
        return solved >= self.target_count

    def get_guide_text(self, cube: Cube) -> str:
        return f"Find a corner with White on it, put it above its slot, and do the Sexy Move until it's inserted!"


class SecondLayerEdgeStep(BaseStep):
    def __init__(self, target_count: int):
        super().__init__(f"Second Layer Edges ({target_count}/4)", "Insert the middle layer edges.")
        self.target_count = target_count

    def is_satisfied(self, cube: Cube) -> bool:
        edges = ["FR", "FL", "BL", "BR"]
        solved = sum(1 for e in edges if is_edge_solved(cube, e))
        return solved >= self.target_count

    def get_guide_text(self, cube: Cube) -> str:
        return "Find an edge without Yellow on the top layer, line it up with the center, and use the Left or Right insertion algorithm."


class YellowCrossStep(BaseStep):
    def __init__(self):
        super().__init__("Yellow Cross", "Orient the top layer edges to form a yellow cross.")

    def is_satisfied(self, cube: Cube) -> bool:
        from engine.constants import SOLVED_FACELET_STRING, CENTERS, Face, EDGE_INDICES
        yellow_color = SOLVED_FACELET_STRING[CENTERS[Face.U]]
        u_edges = ["UR", "UF", "UL", "UB"]
        for edge_name in u_edges:
            u_facelet_idx = EDGE_INDICES[edge_name][0]
            if cube._state[u_facelet_idx] != yellow_color:
                return False
        return True

    def get_guide_text(self, cube: Cube) -> str:
        return "Do F (R U R' U') F' to progress from the Dot, to the L-shape, to the Line, to the Cross."


class YellowFaceStep(BaseStep):
    def __init__(self):
        super().__init__("Yellow Face", "Orient the top layer corners so the whole top face is yellow.")

    def is_satisfied(self, cube: Cube) -> bool:
        from engine.constants import SOLVED_FACELET_STRING, CENTERS, Face, FACE_INDICES
        yellow_color = SOLVED_FACELET_STRING[CENTERS[Face.U]]
        u_indices = FACE_INDICES[Face.U]
        return all(cube._state[i] == yellow_color for i in u_indices)

    def get_guide_text(self, cube: Cube) -> str:
        return "Turn the cube upside down (yellow on bottom) and use the Sexy Move to orient each corner."


class PLLStep(BaseStep):
    def __init__(self):
        super().__init__("Final Permutation", "Permute the last layer to solve the cube.")

    def is_satisfied(self, cube: Cube) -> bool:
        return cube.is_solved(allow_rotation=True)

    def get_guide_text(self, cube: Cube) -> str:
        return "Match the corners, then use the edge cycling algorithm to finish the solve!"
