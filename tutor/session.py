"""TutorSession API for orchestrating the interactive guide."""

from typing import List, Optional
from engine.cube import Cube
from tutor.framework import SolveMethod, SolveTracker
from tutor.search import bfs_search


class TutorSession:
    """Stateful orchestrator for the interactive backend API."""

    def __init__(self, method: SolveMethod, cube: Optional[Cube] = None):
        self.method = method
        self.cube = cube if cube else Cube()
        self.tracker = SolveTracker(self.method, self.cube)

    def apply_move(self, move: str) -> None:
        """Applies a single move to the session cube and updates the tracker."""
        self.cube.apply_move(move)
        # Tracker reads from self.cube implicitly since it holds the reference

    def apply_sequence(self, sequence: str) -> None:
        """Applies an algorithm to the session cube."""
        self.cube.apply_sequence(sequence)

    def get_current_instructions(self) -> str:
        """Returns the dynamic guide text for the current active step."""
        step = self.tracker.current_step()
        if step is None:
            return "Congratulations! The cube is completely solved."
        return step.get_guide_text(self.cube)

    def get_hint(self) -> List[str]:
        """Generates the optimal next sequence of moves using BFS or alg lookups.
        
        Returns:
            A list of moves (e.g. ['R', 'U', 'R'']), or an empty list if no hint
            can be found within the reasonable depth limit.
        """
        step = self.tracker.current_step()
        if step is None:
            return []
            
        # Algorithmic fast-paths
        if step.name == "OLL":
            from tutor.algorithms import get_oll_hint
            hint = get_oll_hint(self.cube)
            if hint: return hint
        elif step.name == "PLL":
            from tutor.algorithms import get_pll_hint
            hint = get_pll_hint(self.cube)
            if hint: return hint
            
        # Run BFS up to depth 6 for fast, responsive UI interaction.
        # Can be increased if running asynchronously.
        solution = bfs_search(self.cube, step, max_depth=6)
        return solution if solution is not None else []

    def is_solved(self) -> bool:
        """Returns True if the entire method has been completed."""
        return self.tracker.is_solved()
        
    def progress_percentage(self) -> float:
        return self.tracker.progress_percentage()
