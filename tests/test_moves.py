"""Tests for move definitions, invertibility, permutation cycles, and slice equivalence."""

import pytest
from engine.constants import (
    Face,
    NUM_FACELETS,
    SOLVED_COLOR_STRING,
    SOLVED_FACELET_STRING,
)
from engine.cube import Cube
from engine.moves import (
    compose_permutations,
    get_move_permutation,
    identity_permutation,
    invert_permutation,
    MOVE_PERMUTATIONS,
    power_permutation,
)


class TestPermutationIntegrity:
    """Mathematical validation of the underlying permutation arrays."""

    def test_all_permutations_are_bijections(self) -> None:
        """Every registered move permutation must be a bijection of 0..53."""
        for notation, perm in MOVE_PERMUTATIONS.items():
            assert len(perm) == NUM_FACELETS, f"{notation} length != {NUM_FACELETS}"
            assert set(perm) == set(range(NUM_FACELETS)), (
                f"{notation} is not a valid bijection of facelet indices"
            )

    def test_inverses_compose_to_identity(self) -> None:
        """Composing any move with its inverse must yield the identity permutation."""
        ident = identity_permutation()
        for base in ["U", "D", "F", "B", "L", "R", "M", "E", "S", "x", "y", "z"]:
            cw = get_move_permutation(base)
            ccw = get_move_permutation(f"{base}'")
            inv_cw = invert_permutation(cw)
            assert ccw == inv_cw, f"Computed inverse of {base} differs from {base}'"
            assert compose_permutations(cw, ccw) == ident, f"{base} * {base}' != ID"
            assert compose_permutations(ccw, cw) == ident, f"{base}' * {base} != ID"

    def test_half_turn_is_order_two(self) -> None:
        """Composing any half-turn with itself must yield the identity permutation."""
        ident = identity_permutation()
        for base in ["U", "D", "F", "B", "L", "R", "M", "E", "S", "x", "y", "z"]:
            double_perm = get_move_permutation(f"{base}2")
            assert compose_permutations(double_perm, double_perm) == ident, (
                f"{base}2 * {base}2 != ID"
            )


class TestOrderCycles:
    """Validates finite group order cycles for moves and standard algorithms."""

    def test_outer_face_quarter_turns_order_four(self) -> None:
        """Applying any quarter turn 4 times must return to the solved state."""
        for face in ["U", "D", "F", "B", "L", "R"]:
            cube = Cube()
            for _ in range(4):
                cube.apply_move(face)
            assert cube.is_solved(), f"{face} * 4 did not return to solved state"

    def test_r_order_four(self) -> None:
        """Requirement: (R) * 4 == Solved."""
        cube = Cube()
        for _ in range(4):
            cube.apply_move("R")
        assert cube.is_solved()

    def test_r2_order_two(self) -> None:
        """Requirement: (R2) * 2 == Solved."""
        cube = Cube()
        for _ in range(2):
            cube.apply_move("R2")
        assert cube.is_solved()

    def test_m_slice_order_four(self) -> None:
        """Requirement: (M) * 4 == Solved."""
        cube = Cube()
        for _ in range(4):
            cube.apply_move("M")
        assert cube.is_solved()

    def test_x_rotation_order_four(self) -> None:
        """Requirement: (x) * 4 == Solved."""
        cube = Cube()
        for _ in range(4):
            cube.apply_move("x")
        assert cube.is_solved()

    def test_y_and_z_rotations_order_four(self) -> None:
        """Whole-cube rotations y and z must have order 4."""
        for rot in ["y", "z"]:
            cube = Cube()
            for _ in range(4):
                cube.apply_move(rot)
            assert cube.is_solved(), f"{rot} * 4 did not return to solved state"

    def test_e_and_s_slices_order_four(self) -> None:
        """Slice turns E and S must have order 4."""
        for slice_move in ["E", "S"]:
            cube = Cube()
            for _ in range(4):
                cube.apply_move(slice_move)
            assert cube.is_solved(), f"{slice_move} * 4 did not return to solved state"

    def test_sexy_move_order_six(self) -> None:
        """Requirement: (R U R' U') * 6 == Solved."""
        cube = Cube()
        cube.apply_sequence("(R U R' U') * 6")
        assert cube.is_solved()

        # Intermediate repetitions must NOT be solved
        c1 = Cube().apply_sequence("R U R' U'")
        assert not c1.is_solved()
        c3 = Cube().apply_sequence("(R U R' U') * 3")
        assert not c3.is_solved()

    def test_sune_order_six(self) -> None:
        """CFOP Sune algorithm has order 6."""
        sune = "R U R' U R U2 R'"
        cube = Cube()
        cube.apply_sequence(f"({sune}) * 6")
        assert cube.is_solved()

    def test_t_perm_order_two(self) -> None:
        """PLL T-Permutation is an involution (order 2)."""
        t_perm = "R U R' U' R' F R2 U' R' U' R U R' F'"
        cube = Cube()
        cube.apply_sequence(f"({t_perm}) * 2")
        assert cube.is_solved()

    def test_jb_perm_order_two(self) -> None:
        """PLL Jb-Permutation is an involution (order 2)."""
        jb_perm = "R U R' F' R U R' U' R' F R2 U' R' U'"
        cube = Cube()
        cube.apply_sequence(f"({jb_perm}) * 2")
        assert cube.is_solved()

    def test_superflip_order_two(self) -> None:
        """The 20-move Superflip algorithm has order 2."""
        superflip = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
        cube = Cube()
        cube.apply_sequence(superflip)
        assert not cube.is_solved()
        cube.apply_sequence(superflip)
        assert cube.is_solved()


class TestMoveInversesAndCancellations:
    """Verifies inverse cancellation sequences."""

    def test_move_inverse_cancellations_requirement(self) -> None:
        """Requirement: cube.apply_sequence("R U F").apply_sequence("F' U' R'") == Solved."""
        cube = Cube()
        result = cube.apply_sequence("R U F").apply_sequence("F' U' R'")
        assert result.is_solved()
        assert result == Cube()

    def test_single_move_inverses(self) -> None:
        """Individual moves followed by their inverses cancel completely."""
        moves = ["U", "D", "F", "B", "L", "R", "M", "E", "S", "x", "y", "z", "Rw", "Uw"]
        for m in moves:
            cube = Cube()
            cube.apply_move(m).apply_move(f"{m}'")
            assert cube.is_solved(), f"{m} followed by {m}' failed to cancel"

    def test_arbitrary_algorithm_inverse(self) -> None:
        """An arbitrary complex sequence followed by its exact reversed inverse cancels."""
        algo = "R2 U' F2 D B' L2 U R U' L' F2 B"
        inv_algo = "B' F2 L U R' U' L2 B D' F2 U R2"
        cube = Cube()
        cube.apply_sequence(algo)
        assert not cube.is_solved()
        cube.apply_sequence(inv_algo)
        assert cube.is_solved()


class TestSliceEquivalences:
    """Validates slice move behavior against outer face turns and rotations."""

    def test_m_slice_equivalence(self) -> None:
        """Requirement: M must match R L' x' (or x' R L') state behavior.

        Because x = R M' L', we have M = R L' x' (and M = x' R L').
        """
        cube_m = Cube().apply_move("M")
        cube_equiv = Cube().apply_sequence("R L' x'")
        assert cube_m == cube_equiv, "M did not match R L' x'"

        cube_equiv_alt = Cube().apply_sequence("x' R L'")
        assert cube_m == cube_equiv_alt, "M did not match x' R L'"

    def test_m_prime_equivalence(self) -> None:
        """M' must match R' L x."""
        cube_m_prime = Cube().apply_move("M'")
        cube_equiv = Cube().apply_sequence("R' L x")
        assert cube_m_prime == cube_equiv

    def test_e_slice_equivalence(self) -> None:
        """E follows D direction: E matches U D' y'."""
        cube_e = Cube().apply_move("E")
        cube_equiv = Cube().apply_sequence("U D' y'")
        assert cube_e == cube_equiv

    def test_s_slice_equivalence(self) -> None:
        """S follows F direction: S matches F' B z."""
        cube_s = Cube().apply_move("S")
        cube_equiv = Cube().apply_sequence("F' B z")
        assert cube_s == cube_equiv

    def test_wide_moves_equivalence(self) -> None:
        """Rw and Lw wide moves match outer face plus slice turns."""
        assert Cube().apply_move("Rw") == Cube().apply_sequence("R M'")
        assert Cube().apply_move("Lw") == Cube().apply_sequence("L M")
        assert Cube().apply_move("Uw") == Cube().apply_sequence("U E'")
        assert Cube().apply_move("Dw") == Cube().apply_sequence("D E")
        assert Cube().apply_move("Fw") == Cube().apply_sequence("F S")
        assert Cube().apply_move("Bw") == Cube().apply_sequence("B S'")

    def test_lowercase_wide_move_aliases(self) -> None:
        """Lowercase notation (r, l, u, d, f, b) maps to wide moves."""
        assert Cube().apply_move("r") == Cube().apply_move("Rw")
        assert Cube().apply_move("l") == Cube().apply_move("Lw")
        assert Cube().apply_move("u") == Cube().apply_move("Uw")
        assert Cube().apply_move("d") == Cube().apply_move("Dw")
        assert Cube().apply_move("f") == Cube().apply_move("Fw")
        assert Cube().apply_move("b") == Cube().apply_move("Bw")


class TestCubeStateAndIsolation:
    """Validates Cube cloning, isolation, string conversions, and solved checks."""

    def test_initial_state_is_solved(self) -> None:
        cube = Cube()
        assert cube.is_solved()
        assert cube.to_facelet_string() == SOLVED_FACELET_STRING
        assert cube.to_color_string() == SOLVED_COLOR_STRING

    def test_clone_creates_isolated_instance(self) -> None:
        original = Cube()
        clone = original.clone()
        assert clone == original
        assert clone is not original

        # Mutate clone; original must remain untouched
        clone.apply_move("R")
        assert not clone.is_solved()
        assert original.is_solved()

    def test_is_solved_with_allow_rotation(self) -> None:
        cube = Cube().apply_move("x")
        # In canonical reference frame, it is not solved
        assert not cube.is_solved(allow_rotation=False)
        # With allow_rotation=True, faces are still monochromatic
        assert cube.is_solved(allow_rotation=True)

        # After a non-rotation turn, both must return False
        cube.apply_move("R")
        assert not cube.is_solved(allow_rotation=False)
        assert not cube.is_solved(allow_rotation=True)

    def test_invalid_state_length_raises(self) -> None:
        with pytest.raises(ValueError):
            Cube("UUUU")

    def test_invalid_move_raises(self) -> None:
        cube = Cube()
        with pytest.raises(ValueError):
            cube.apply_move("INVALID")
