"""Move definitions and 54-element deterministic permutation matrices.

Supports:
- Outer face turns: U, D, F, B, L, R and their ', 2 variations
- Slice turns: M (follows L), E (follows D), S (follows F) and their ', 2 variations
- Whole-cube rotations: x (follows R), y (follows U), z (follows F) and their ', 2 variations
- Wide turns: Rw, Lw, Uw, Dw, Fw, Bw (and lowercase aliases r, l, u, d, f, b)
"""

from typing import Dict, List, Sequence, Tuple
from engine.constants import NUM_FACELETS


def identity_permutation() -> List[int]:
    """Returns the identity permutation for 54 facelets."""
    return list(range(NUM_FACELETS))


def compose_permutations(p1: Sequence[int], p2: Sequence[int]) -> List[int]:
    """Composes two permutations such that applying p1 followed by p2

    produces the resulting permutation.
    If new1[i] = old[p1[i]] and new2[i] = new1[p2[i]],
    then new2[i] = old[p1[p2[i]]].
    """
    return [p1[p2[i]] for i in range(NUM_FACELETS)]


def invert_permutation(perm: Sequence[int]) -> List[int]:
    """Computes the inverse of a 54-element permutation."""
    inv = [0] * NUM_FACELETS
    for i, p in enumerate(perm):
        inv[p] = i
    return inv


def power_permutation(perm: Sequence[int], n: int) -> List[int]:
    """Raises a permutation to the power of n."""
    result = identity_permutation()
    for _ in range(n):
        result = compose_permutations(result, perm)
    return result


def _cycle_face_clockwise(perm: List[int], offset: int) -> None:
    """Applies a 90-degree clockwise rotation to a 3x3 face at offset.

    Face indices relative to offset:
    0 1 2       6 3 0
    3 4 5  -->  7 4 1
    6 7 8       8 5 2
    """
    face_map = (6, 3, 0, 7, 4, 1, 8, 5, 2)
    old = list(perm)
    for i in range(9):
        perm[offset + i] = old[offset + face_map[i]]


def _build_u_perm() -> List[int]:
    """Constructs clockwise U face permutation."""
    p = identity_permutation()
    _cycle_face_clockwise(p, 0)
    # Lateral face top rows:
    # F(18,19,20) <- R(9,10,11) <- B(45,46,47) <- L(36,37,38) <- F
    p[18], p[19], p[20] = 9, 10, 11
    p[36], p[37], p[38] = 18, 19, 20
    p[45], p[46], p[47] = 36, 37, 38
    p[9], p[10], p[11] = 45, 46, 47
    return p


def _build_d_perm() -> List[int]:
    """Constructs clockwise D face permutation."""
    p = identity_permutation()
    _cycle_face_clockwise(p, 27)
    # Looking from bottom: F -> R -> B -> L -> F
    p[15], p[16], p[17] = 24, 25, 26
    p[51], p[52], p[53] = 15, 16, 17
    p[42], p[43], p[44] = 51, 52, 53
    p[24], p[25], p[26] = 42, 43, 44
    return p


def _build_f_perm() -> List[int]:
    """Constructs clockwise F face permutation."""
    p = identity_permutation()
    _cycle_face_clockwise(p, 18)
    # Disjoint 4-cycles on outer layer:
    p[9], p[29], p[44], p[6] = 6, 9, 29, 44
    p[12], p[28], p[41], p[7] = 7, 12, 28, 41
    p[15], p[27], p[38], p[8] = 8, 15, 27, 38
    return p


def _build_b_perm() -> List[int]:
    """Constructs clockwise B face permutation."""
    p = identity_permutation()
    _cycle_face_clockwise(p, 45)
    # Disjoint 4-cycles on outer layer:
    p[36], p[33], p[17], p[2] = 2, 36, 33, 17
    p[0], p[42], p[35], p[11] = 11, 0, 42, 35
    p[39], p[34], p[14], p[1] = 1, 39, 34, 14
    return p


def _build_l_perm() -> List[int]:
    """Constructs clockwise L face permutation."""
    p = identity_permutation()
    _cycle_face_clockwise(p, 36)
    # Disjoint 4-cycles on outer layer:
    p[18], p[27], p[53], p[0] = 0, 18, 27, 53
    p[6], p[24], p[33], p[47] = 47, 6, 24, 33
    p[21], p[30], p[50], p[3] = 3, 21, 30, 50
    return p


def _build_r_perm() -> List[int]:
    """Constructs clockwise R face permutation."""
    p = identity_permutation()
    _cycle_face_clockwise(p, 9)
    # Disjoint 4-cycles on outer layer:
    p[45], p[35], p[26], p[8] = 8, 45, 35, 26
    p[2], p[51], p[29], p[20] = 20, 2, 51, 29
    p[48], p[32], p[23], p[5] = 5, 48, 32, 23
    return p


def _build_m_perm() -> List[int]:
    """Constructs M slice permutation (follows L direction).

    Affects middle column of U, F, D, B.
    """
    p = identity_permutation()
    p[19], p[28], p[52], p[1] = 1, 19, 28, 52
    p[22], p[31], p[49], p[4] = 4, 22, 31, 49
    p[25], p[34], p[46], p[7] = 7, 25, 34, 46
    return p


def _build_e_perm() -> List[int]:
    """Constructs E slice permutation (follows D direction).

    Affects middle row of F, R, B, L.
    """
    p = identity_permutation()
    p[12], p[48], p[39], p[21] = 21, 12, 48, 39
    p[13], p[49], p[40], p[22] = 22, 13, 49, 40
    p[14], p[50], p[41], p[23] = 23, 14, 50, 41
    return p


def _build_s_perm() -> List[int]:
    """Constructs S slice permutation (follows F direction).

    Affects middle ring of U, R, D, L.
    """
    p = identity_permutation()
    p[10], p[32], p[43], p[3] = 3, 10, 32, 43
    p[13], p[31], p[40], p[4] = 4, 13, 31, 40
    p[16], p[30], p[37], p[5] = 5, 16, 30, 37
    return p


# Precompute base permutations
BASE_PERMUTATIONS: Dict[str, List[int]] = {
    "U": _build_u_perm(),
    "D": _build_d_perm(),
    "F": _build_f_perm(),
    "B": _build_b_perm(),
    "L": _build_l_perm(),
    "R": _build_r_perm(),
    "M": _build_m_perm(),
    "E": _build_e_perm(),
    "S": _build_s_perm(),
}

# Rotations defined as compositions of outer faces and slices on disjoint layers:
# x follows R: R + M' + L'
_m_prime = power_permutation(BASE_PERMUTATIONS["M"], 3)
_l_prime = power_permutation(BASE_PERMUTATIONS["L"], 3)
BASE_PERMUTATIONS["x"] = compose_permutations(
    compose_permutations(BASE_PERMUTATIONS["R"], _m_prime), _l_prime
)

# y follows U: U + E' + D'
_e_prime = power_permutation(BASE_PERMUTATIONS["E"], 3)
_d_prime = power_permutation(BASE_PERMUTATIONS["D"], 3)
BASE_PERMUTATIONS["y"] = compose_permutations(
    compose_permutations(BASE_PERMUTATIONS["U"], _e_prime), _d_prime
)

# z follows F: F + S + B'
_b_prime = power_permutation(BASE_PERMUTATIONS["B"], 3)
BASE_PERMUTATIONS["z"] = compose_permutations(
    compose_permutations(BASE_PERMUTATIONS["F"], BASE_PERMUTATIONS["S"]), _b_prime
)

# Wide Moves:
# Rw = R + M'
BASE_PERMUTATIONS["Rw"] = compose_permutations(BASE_PERMUTATIONS["R"], _m_prime)
# Lw = L + M
BASE_PERMUTATIONS["Lw"] = compose_permutations(
    BASE_PERMUTATIONS["L"], BASE_PERMUTATIONS["M"]
)
# Uw = U + E'
BASE_PERMUTATIONS["Uw"] = compose_permutations(BASE_PERMUTATIONS["U"], _e_prime)
# Dw = D + E
BASE_PERMUTATIONS["Dw"] = compose_permutations(
    BASE_PERMUTATIONS["D"], BASE_PERMUTATIONS["E"]
)
# Fw = F + S
BASE_PERMUTATIONS["Fw"] = compose_permutations(
    BASE_PERMUTATIONS["F"], BASE_PERMUTATIONS["S"]
)
# Bw = B + S'
_s_prime = power_permutation(BASE_PERMUTATIONS["S"], 3)
BASE_PERMUTATIONS["Bw"] = compose_permutations(BASE_PERMUTATIONS["B"], _s_prime)

# Lowercase wide move aliases
BASE_PERMUTATIONS["r"] = BASE_PERMUTATIONS["Rw"]
BASE_PERMUTATIONS["l"] = BASE_PERMUTATIONS["Lw"]
BASE_PERMUTATIONS["u"] = BASE_PERMUTATIONS["Uw"]
BASE_PERMUTATIONS["d"] = BASE_PERMUTATIONS["Dw"]
BASE_PERMUTATIONS["f"] = BASE_PERMUTATIONS["Fw"]
BASE_PERMUTATIONS["b"] = BASE_PERMUTATIONS["Bw"]


def _generate_all_permutations() -> Dict[str, List[int]]:
    """Generates all move permutations including inverses and half-turns."""
    all_perms: Dict[str, List[int]] = {}
    for base_name, base_perm in BASE_PERMUTATIONS.items():
        p_cw = base_perm
        p_double = power_permutation(p_cw, 2)
        p_ccw = power_permutation(p_cw, 3)

        all_perms[base_name] = p_cw
        all_perms[f"{base_name}'"] = p_ccw
        all_perms[f"{base_name}2"] = p_double
        # Alternative notation variants
        all_perms[f"{base_name}2'"] = p_double
    return all_perms


MOVE_PERMUTATIONS: Dict[str, List[int]] = _generate_all_permutations()


def normalize_move_token(token: str) -> str:
    """Normalizes move string, standardizing quotes and spaces."""
    cleaned = token.strip().replace("’", "'").replace("`", "'")
    return cleaned


def parse_move(token: str) -> Tuple[str, str]:
    """Splits a move token into its base move and turn modifier.

    Examples:
    - "R" -> ("R", "")
    - "U'" -> ("U", "'")
    - "F2" -> ("F", "2")
    - "Rw2" -> ("Rw", "2")
    """
    token = normalize_move_token(token)
    if not token:
        raise ValueError("Cannot parse empty move token")

    if token.endswith("2'") or token.endswith("2"):
        return token[:-2] if token.endswith("2'") else token[:-1], "2"
    elif token.endswith("'"):
        return token[:-1], "'"
    else:
        return token, ""


def get_move_permutation(notation: str) -> List[int]:
    """Retrieves the precomputed 54-element permutation array for any valid move."""
    token = normalize_move_token(notation)
    if token in MOVE_PERMUTATIONS:
        return MOVE_PERMUTATIONS[token]
    raise ValueError(f"Unknown or unsupported move notation: '{notation}'")
