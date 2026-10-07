"""Tests for WCA scrambler compliance, cancellation prevention, and move validity."""

import pytest
from engine.constants import (
    Face,
    FACE_TO_AXIS,
)
from engine.cube import Cube
from engine.moves import parse_move
from engine.scrambler import (
    DEFAULT_SCRAMBLE_LENGTH,
    generate_scramble,
    get_valid_next_faces,
    Scrambler,
    VALID_TURNS,
    validate_scramble,
)


class TestScrambleGeneration:
    """Validates length, format, and structure of generated scrambles."""

    def test_default_scramble_length_is_twenty(self) -> None:
        """Default scramble length must be 20 moves."""
        scramble = generate_scramble()
        moves = scramble.split()
        assert len(moves) == DEFAULT_SCRAMBLE_LENGTH
        assert len(moves) == 20

    @pytest.mark.parametrize("length", [1, 5, 12, 25, 30])
    def test_custom_scramble_lengths(self, length: int) -> None:
        """Custom scramble lengths are strictly respected."""
        scramble = generate_scramble(length=length)
        moves = scramble.split()
        assert len(moves) == length

    def test_zero_length_scramble(self) -> None:
        """Zero length produces an empty string."""
        assert generate_scramble(length=0) == ""

    def test_negative_length_raises_error(self) -> None:
        """Negative length must raise ValueError."""
        with pytest.raises(ValueError):
            generate_scramble(length=-1)

    def test_all_moves_are_valid_singmaster_outer_turns(self) -> None:
        """Every generated token must be an outer face turn with valid modifier."""
        scramble = generate_scramble(length=50, seed=123)
        moves = scramble.split()
        valid_faces = {f.value for f in Face}
        for token in moves:
            base, modifier = parse_move(token)
            assert base in valid_faces, f"Invalid face '{base}' in token '{token}'"
            assert modifier in VALID_TURNS, f"Invalid modifier '{modifier}' in token '{token}'"


class TestCancellationPrevention:
    """Verifies that scrambles are free of consecutive and axis cancellations."""

    def test_no_consecutive_same_face_moves(self) -> None:
        """Never allow consecutive moves on the same face (e.g. no R R' or R R2)."""
        scramble = generate_scramble(length=100, seed=42)
        moves = scramble.split()
        for i in range(1, len(moves)):
            base_prev, _ = parse_move(moves[i - 1])
            base_curr, _ = parse_move(moves[i])
            assert base_prev != base_curr, (
                f"Consecutive same face found: '{moves[i - 1]}' followed by '{moves[i]}'"
            )

    def test_no_opposite_parallel_face_sandwich_cancellations(self) -> None:
        """Never allow 3 consecutive moves on the same axis (e.g. no R L R)."""
        scramble = generate_scramble(length=100, seed=42)
        moves = scramble.split()
        for i in range(2, len(moves)):
            f0 = Face(parse_move(moves[i - 2])[0])
            f1 = Face(parse_move(moves[i - 1])[0])
            f2 = Face(parse_move(moves[i])[0])

            a0 = FACE_TO_AXIS[f0]
            a1 = FACE_TO_AXIS[f1]
            a2 = FACE_TO_AXIS[f2]
            assert not (a0 == a1 == a2), (
                f"Conflicting axis cancellation sequence: {moves[i - 2]} {moves[i - 1]} {moves[i]}"
            )

    def test_opposite_face_pair_is_permitted_with_separation(self) -> None:
        """Adjacent opposite face turns like R L are permitted if followed by a different axis."""
        # Next faces after [R, L] must NOT include R or L
        valid_after_rl = get_valid_next_faces([Face.R, Face.L])
        assert Face.R not in valid_after_rl
        assert Face.L not in valid_after_rl
        assert set(valid_after_rl) == {Face.U, Face.D, Face.F, Face.B}

    def test_validator_detects_consecutive_violation(self) -> None:
        """Validator rejects scrambles with consecutive moves on the same face."""
        assert not validate_scramble("R R'")
        assert not validate_scramble("U U2")
        assert not validate_scramble("F' F")

    def test_validator_detects_sandwich_violation(self) -> None:
        """Validator rejects scrambles with 3 consecutive moves on the same axis."""
        assert not validate_scramble("R L R")
        assert not validate_scramble("R L R'")
        assert not validate_scramble("U D U2")
        assert not validate_scramble("F B F'")

    def test_validator_accepts_valid_scramble(self) -> None:
        """Validator accepts properly separated scrambles."""
        assert validate_scramble("R U R' U'")
        assert validate_scramble("R L U D F B")
        assert validate_scramble("D2 F' R2 B L2 U' R")


class TestDeterminismAndStress:
    """Verifies deterministic seeding and validates 1,000 randomized scrambles."""

    def test_seeding_reproducibility(self) -> None:
        """Identical seeds produce identical scrambles."""
        scramble1 = generate_scramble(length=20, seed=999)
        scramble2 = generate_scramble(length=20, seed=999)
        assert scramble1 == scramble2

    def test_different_seeds_produce_different_scrambles(self) -> None:
        """Different seeds produce distinct scrambles."""
        scramble1 = generate_scramble(length=20, seed=1)
        scramble2 = generate_scramble(length=20, seed=2)
        assert scramble1 != scramble2

    def test_statistical_stress_validation(self) -> None:
        """Generates 1,000 scrambles and asserts 100% pass WCA validation."""
        for s in range(1000):
            scramble = generate_scramble(length=20, seed=s)
            assert validate_scramble(scramble), f"Scramble failed validation: {scramble}"

    def test_scramble_cube_application(self) -> None:
        """Scrambler class properly produces an unsolved state on a clean cube."""
        scrambler = Scrambler(seed=42)
        scramble_str, scrambled_cube = scrambler.scramble_cube()

        assert len(scramble_str.split()) == DEFAULT_SCRAMBLE_LENGTH
        assert validate_scramble(scramble_str)
        assert not scrambled_cube.is_solved()

        # Inverting the scramble must restore the solved state
        inverted_moves = []
        for token in reversed(scramble_str.split()):
            base, mod = parse_move(token)
            if mod == "":
                inv_mod = "'"
            elif mod == "'":
                inv_mod = ""
            else:
                inv_mod = "2"
            inverted_moves.append(f"{base}{inv_mod}")

        restored_cube = scrambled_cube.clone().apply_sequence(" ".join(inverted_moves))
        assert restored_cube.is_solved()
