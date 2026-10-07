"""Tests for the advanced algorithm parser (commutators, conjugates, multipliers)."""

import pytest
from engine.parser import parse_algorithm, invert_algorithm


def test_parse_basic_sequence() -> None:
    assert parse_algorithm("R U R' U'") == ["R", "U", "R'", "U'"]
    assert parse_algorithm("F2 B2' Lw") == ["F2", "B2'", "Lw"]


def test_parse_multipliers() -> None:
    # Space between closing parenthesis and multiplier
    assert parse_algorithm("(R U) 2") == ["R", "U", "R", "U"]
    # No space
    assert parse_algorithm("(R U)2") == ["R", "U", "R", "U"]
    # With asterisk
    assert parse_algorithm("(R U) * 2") == ["R", "U", "R", "U"]
    # Multiplier 1
    assert parse_algorithm("(R U)") == ["R", "U"]


def test_parse_commutator() -> None:
    # [A, B] -> A B A' B'
    assert parse_algorithm("[R, U]") == ["R", "U", "R'", "U'"]
    # With complex A and B
    assert parse_algorithm("[R U R', D]") == ["R", "U", "R'", "D", "R", "U'", "R'", "D'"]


def test_parse_conjugate() -> None:
    # [A: B] -> A B A'
    assert parse_algorithm("[R: U]") == ["R", "U", "R'"]
    # With complex A and B
    assert parse_algorithm("[R U: D2]") == ["R", "U", "D2", "U'", "R'"]


def test_parse_nested_structures() -> None:
    # Commutator with conjugate inside
    # [[R: U], D] -> [R U R', D] -> R U R' D R U' R' D'
    assert parse_algorithm("[[R: U], D]") == ["R", "U", "R'", "D", "R", "U'", "R'", "D'"]


def test_parse_commutator_with_multiplier() -> None:
    # [R, U]2 -> R U R' U' R U R' U'
    assert parse_algorithm("[R, U]2") == ["R", "U", "R'", "U'", "R", "U", "R'", "U'"]


def test_invert_algorithm() -> None:
    assert invert_algorithm("R U") == ["U'", "R'"]
    assert invert_algorithm("(R U)2") == ["U'", "R'", "U'", "R'"]
    # Inverse of commutator [A, B] is [B, A]
    assert invert_algorithm("[R, U]") == ["U", "R", "U'", "R'"]
    # Inverse of conjugate [A: B] is [A: B']
    assert invert_algorithm("[R: U]") == ["R", "U'", "R'"]


def test_comments_and_whitespace_are_ignored() -> None:
    algo = """
    // Setup
    [R: U] // Conjugate
    # Commutator
    [R, U] 
    """
    expected = ["R", "U", "R'", "R", "U", "R'", "U'"]
    assert parse_algorithm(algo) == expected
