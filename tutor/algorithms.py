"""Algorithm dictionaries and matching logic for OLL and PLL hints."""

from typing import Dict, List, Optional, Tuple
from engine.cube import Cube
from engine.parser import parse_algorithm


class AlgorithmMatcher:
    """Matches a cube state to a known set of algorithms by generating signatures."""

    def __init__(self, target_state_cube: Cube, mask_indices: List[int], algorithms: Dict[str, str], color_mapper=None):
        """
        Args:
            target_state_cube: A cube representing the desired end state for these algs.
            mask_indices: A list of facelet indices to consider when matching states.
            algorithms: A dictionary mapping an algorithm name to its string notation.
            color_mapper: Optional function to map colors before hashing (e.g., for OLL we only care if it's yellow).
        """
        self.mask_indices = mask_indices
        self.color_mapper = color_mapper if color_mapper else lambda c: c
        self.signatures: Dict[Tuple[str, ...], str] = {}
        
        # Precompute signatures by applying the INVERSE of each algorithm to the target state
        for name, algo_str in algorithms.items():
            # Test all 4 post-AUFs (Adjust U Face after the algorithm finishes)
            for post_auf in ["", "U", "U2", "U'"]:
                cube = target_state_cube.clone()
                if post_auf:
                    # If the cube needs a post_auf to be solved, the inverse process starts by UNDOING that post_auf
                    inv_post = self._invert_move(post_auf)
                    cube.apply_move(inv_post)
                    
                inv_moves = self._invert_sequence(parse_algorithm(algo_str))
                for move in inv_moves:
                    cube.apply_move(move)
                
                sig = self._get_signature(cube)
                
                # The solution is the algorithm, followed by the required post_auf
                solve_str = f"{algo_str} {post_auf}".strip()
                # We only store the first signature we see (shortest/simplest)
                if sig not in self.signatures:
                    self.signatures[sig] = solve_str

    def _invert_move(self, move: str) -> str:
        from engine.parser import invert_move_token
        return invert_move_token(move)

    def _invert_sequence(self, moves: List[str]) -> List[str]:
        return [self._invert_move(m) for m in reversed(moves)]

    def _get_signature(self, cube: Cube) -> Tuple[str, ...]:
        return tuple(self.color_mapper(cube._state[i]) for i in self.mask_indices)

    def find_match(self, cube: Cube) -> Optional[List[str]]:
        """Returns the optimal algorithm to solve the current masked state, if known."""
        # Test all 4 pre-AUFs (Adjust U Face before algorithm)
        for pre_auf in ["", "U", "U2", "U'"]:
            test_cube = cube.clone()
            if pre_auf:
                test_cube.apply_move(pre_auf)
                
            sig = self._get_signature(test_cube)
            if sig in self.signatures:
                # If we had to do a pre_auf to match the signature, 
                # we must prepend that pre_auf to the returned algorithm.
                algo_str = self.signatures[sig]
                res = []
                if pre_auf:
                    res.append(pre_auf)
                res.extend(parse_algorithm(algo_str))
                return res
        return None


# --- Standard 2-Look Algorithms ---

TWO_LOOK_OLL = {
    # Edges
    "Dot": "F R U R' U' F' f R U R' U' f'",
    "L-Shape": "f R U R' U' f'",
    "Line": "F R U R' U' F'",
    # Corners
    "Sune": "R U R' U R U2 R'",
    "Anti-Sune": "R U2 R' U' R U' R'",
    "H": "F R U R' U' R U R' U' R U R' U' F'",
    "Pi": "R U2 R2 U' R2 U' R2 U2 R",
    "L": "F R' F' r U R U' r'",
    "T": "r U R' U' r' F R F'",
    "U": "R2 D R' U2 R D' R' U2 R'",
}

TWO_LOOK_PLL = {
    # Corners
    "T-Perm": "R U R' U' R' F R2 U' R' U' R U R' F'",
    "Y-Perm": "F R U' R' U' R U R' F' R U R' U' R' F R F'",
    # Edges
    "Ua-Perm": "R U' R U R U R U' R' U' R2",
    "Ub-Perm": "R2 U R U R' U' R' U' R' U R'",
    "H-Perm": "M2 U M2 U2 M2 U M2",
    "Z-Perm": "M2 U M2 U M' U2 M2 U2 M'",
}


def get_oll_mask() -> List[int]:
    """Returns the indices relevant for OLL (U face + top row of adjacent faces)."""
    from engine.constants import FACE_INDICES, Face
    mask = list(FACE_INDICES[Face.U])
    # Top row of F, R, B, L
    mask.extend(FACE_INDICES[Face.F][0:3])
    mask.extend(FACE_INDICES[Face.R][0:3])
    mask.extend(FACE_INDICES[Face.B][0:3])
    mask.extend(FACE_INDICES[Face.L][0:3])
    return mask


def get_pll_mask() -> List[int]:
    """Returns the indices relevant for PLL (same as OLL)."""
    return get_oll_mask()


_oll_matcher: Optional[AlgorithmMatcher] = None
_pll_matcher: Optional[AlgorithmMatcher] = None


def get_oll_hint(cube: Cube) -> Optional[List[str]]:
    global _oll_matcher
    if _oll_matcher is None:
        target = Cube()  # Solved cube is a valid OLL target
        from engine.constants import SOLVED_FACELET_STRING, CENTERS, Face
        yellow = SOLVED_FACELET_STRING[CENTERS[Face.U]]
        mapper = lambda c: c == yellow
        _oll_matcher = AlgorithmMatcher(target, get_oll_mask(), TWO_LOOK_OLL, color_mapper=mapper)
    return _oll_matcher.find_match(cube)


def get_pll_hint(cube: Cube) -> Optional[List[str]]:
    global _pll_matcher
    if _pll_matcher is None:
        target = Cube()  # Solved cube is a valid PLL target
        _pll_matcher = AlgorithmMatcher(target, get_pll_mask(), TWO_LOOK_PLL)
    return _pll_matcher.find_match(cube)
