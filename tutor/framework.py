"""Generic step-tracking framework for speedcubing method tutors.

This framework allows defining modular sequential steps for any cubing method
(CFOP, Roux, ZZ, Beginner's) and evaluating a cube's progress against them.
"""

from typing import List, Optional, Protocol

from engine.cube import Cube


class StepEvaluator(Protocol):
    """Protocol for evaluating a specific step in a solving method."""
    
    @property
    def name(self) -> str:
        """The short name of the step (e.g., 'White Cross', 'F2L')."""
        ...
        
    @property
    def description(self) -> str:
        """Detailed description of what the step accomplishes."""
        ...

    def is_satisfied(self, cube: Cube) -> bool:
        """Evaluates whether the given cube state satisfies this step.
        
        Note: A step is satisfied if its target pieces are solved. It is usually
        implied that previous steps must also remain satisfied.
        """
        ...

    def get_guide_text(self, cube: Cube) -> str:
        """Returns dynamic, context-aware instructions for completing the step."""
        ...


class BaseStep(StepEvaluator):
    """A convenient base class for implementing step evaluators."""
    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name
        
    @property
    def description(self) -> str:
        return self._description
        
    def is_satisfied(self, cube: Cube) -> bool:
        raise NotImplementedError("Subclasses must implement is_satisfied")

    def get_guide_text(self, cube: Cube) -> str:
        return f"Currently working on: {self.name}. {self.description}"


class SolveMethod:
    """Represents a full speedcubing method as an ordered sequence of steps."""
    
    def __init__(self, name: str, steps: List[StepEvaluator]) -> None:
        """Initializes a SolveMethod.
        
        Args:
            name: The name of the method (e.g., 'CFOP', 'Roux').
            steps: An ordered list of StepEvaluator instances representing the stages.
        """
        self.name = name
        self.steps = steps

    def get_step(self, index: int) -> StepEvaluator:
        """Returns the step at the given index."""
        return self.steps[index]
        
    def __len__(self) -> int:
        """Returns the total number of steps in the method."""
        return len(self.steps)


class SolveTracker:
    """Tracks a cube's progress through a specific solving method."""
    
    def __init__(self, method: SolveMethod, cube: Optional[Cube] = None) -> None:
        self.method = method
        self.cube = cube if cube is not None else Cube()

    def update_cube(self, cube: Cube) -> None:
        """Updates the tracker with a new cube state."""
        self.cube = cube

    def current_step_index(self) -> int:
        """Returns the index of the first step that is NOT satisfied.
        
        If all steps are satisfied, returns the length of the method.
        """
        for i, step in enumerate(self.method.steps):
            if not step.is_satisfied(self.cube):
                return i
        return len(self.method)

    def current_step(self) -> Optional[StepEvaluator]:
        """Returns the StepEvaluator for the current active step.
        
        Returns None if the solve is completely finished.
        """
        idx = self.current_step_index()
        if idx < len(self.method):
            return self.method.get_step(idx)
        return None

    def is_solved(self) -> bool:
        """Returns True if the cube has satisfied all method steps."""
        return self.current_step_index() == len(self.method)

    def progress_percentage(self) -> float:
        """Returns the progress as a float between 0.0 and 100.0."""
        total = len(self.method)
        if total == 0:
            return 100.0
        return (self.current_step_index() / total) * 100.0

    def generate_report(self) -> str:
        """Generates a readable status report of the solve progress."""
        idx = self.current_step_index()
        total = len(self.method)
        
        lines = [f"Method: {self.method.name}"]
        lines.append(f"Progress: {idx}/{total} steps completed ({self.progress_percentage():.1f}%)")
        lines.append("-" * 30)
        
        for i, step in enumerate(self.method.steps):
            status = "[x]" if i < idx else "[ ]"
            marker = " <-- CURRENT" if i == idx else ""
            lines.append(f"{status} Step {i+1}: {step.name}{marker}")
            
        if idx == total:
            lines.append("\nSolve complete!")
            
        return "\n".join(lines)
