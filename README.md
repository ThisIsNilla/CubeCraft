# CubeCraft Speedcube Engine

CubeCraft is a modular speedcubing training engine and multi-method tutor (Beginner LBL, CFOP, Roux, ZZ) built in modern Python.

This repository implements **Milestone 1: The Core Permutation Engine, Scrambler, and Test Harness**. It features zero external runtime dependencies, full type annotations, deterministic 54-facet state transitions, and a World Cube Association (WCA) compliant scrambler.

---

## Architecture Overview

```
speedcube-engine/
├── engine/
│   ├── __init__.py       # Public package API exports
│   ├── constants.py      # Facelet indices, colors, and move notation enums
│   ├── cube.py           # Core Cube class (54-facet array, state transitions)
│   ├── moves.py          # Singmaster move definitions (FTM, slices, rotations)
│   └── scrambler.py      # WCA-compliant random state scrambler
├── tests/
│   ├── __init__.py       # Test package marker
│   ├── test_moves.py     # Move invertibility and order cycle tests
│   └── test_scrambler.py # Move validity and cancellation prevention tests
└── README.md             # Setup guide and architecture overview
```

### 1. 54-Facet Coordinate System (`engine/constants.py`)
CubeCraft adopts the standard Kociemba and Singmaster facelet ordering (indices 0 to 53):
- **U1 to U9** (Indices 0 to 8): Up / Top face (White)
- **R1 to R9** (Indices 9 to 17): Right face (Red)
- **F1 to F9** (Indices 18 to 26): Front face (Green)
- **D1 to D9** (Indices 27 to 35): Down / Bottom face (Yellow)
- **L1 to L9** (Indices 36 to 44): Left face (Orange)
- **B1 to B9** (Indices 45 to 53): Back face (Blue)

Each 3x3 face is arranged in row-major order:
```
0 1 2 (Top row)
3 4 5 (Middle row: 4 is center)
6 7 8 (Bottom row)
```

Unfolded ASCII net representation:
```
            U1 U2 U3
            U4 U5 U6
            U7 U8 U9
L1 L2 L3    F1 F2 F3    R1 R2 R3    B1 B2 B3
L4 L5 L6    F4 F5 F6    R4 R5 R6    B4 B5 B6
L7 L8 L9    F7 F8 F9    R7 R8 R9    B7 B8 B9
            D1 D2 D3
            D4 D5 D6
            D7 D8 D9
```

### 2. Permutation Transitions (`engine/moves.py`)
State transitions are executed using deterministic 54-element index permutation arrays where:
```python
new_state[i] = old_state[permutation[i]]
```
All standard Singmaster notations are precomputed:
- **Outer Face Turns**: `U, U', U2, D, D', D2, R, R', R2, L, L', L2, F, F', F2, B, B', B2`
- **Slice Turns**:
  - `M` (Middle: follows `L` direction between L and R)
  - `E` (Equator: follows `D` direction between U and D)
  - `S` (Standing: follows `F` direction between F and B)
  - Full `'` and `2` variations
- **Whole-Cube Rotations**:
  - `x` (rotates entire cube following `R`)
  - `y` (rotates entire cube following `U`)
  - `z` (rotates entire cube following `F`)
  - Full `'` and `2` variations
- **Wide Turns**: `Rw, Lw, Uw, Dw, Fw, Bw` along with lowercase aliases `r, l, u, d, f, b`

### 3. Core Cube Class (`engine/cube.py`)
The `Cube` class encapsulates the 54-facet array and provides fluent execution:
- `apply_move(notation: str)`: Executes a single turn in-place.
- `apply_sequence(algorithm: str)`: Parses space-separated tokens, comments, and repeated groups such as `(R U R' U') * 6`.
- `clone()`: Creates an independent deep copy.
- `is_solved(allow_rotation: bool = False)`: Verifies solved state in canonical reference frame or allows whole-cube rotated monochromatic states.
- `to_facelet_string()` and `to_color_string()`: Serializes state to standard 54-character strings.
- `net_string()`: Generates a 2D ASCII visualization.

### 4. WCA Random Move Scrambler (`engine/scrambler.py`)
Generates 20-move competition-grade scrambles adhering to strict cancellation prevention:
- **Consecutive move prevention**: Prohibits identical face turns in sequence (e.g. `R R'` or `R R2`).
- **Sandwich and axis cancellation prevention**: If two consecutive moves occur along the same axis (e.g. `R L`), no further move on that axis is permitted until another axis intervenes (prevents `R L R`, `R L L'`, `U D U'`, etc.).
- **Reproducible seeding**: Optional seed parameter for reproducible tests and benchmarking.

---

## Quickstart & Usage

### Basic Usage
```python
from engine import Cube, generate_scramble

# 1. Initialize a solved cube
cube = Cube()
print(cube.is_solved())  # True

# 2. Generate a WCA-compliant scramble
scramble = generate_scramble(length=20, seed=42)
print("Scramble:", scramble)
# Example: R U2 L' D F2 ...

# 3. Apply scramble sequence
cube.apply_sequence(scramble)
print(cube.is_solved())  # False

# 4. Display unfolded net
print(cube.net_string())
```

### Fluent Chaining and Algorithm Execution
```python
from engine import Cube

cube = Cube()

# Execute sexy move 6 times
cube.apply_sequence("(R U R' U') * 6")
assert cube.is_solved()

# Fluent chaining
cube.apply_move("R").apply_move("U").apply_move("R'").apply_move("U'")
```

---

## Running Tests

CubeCraft requires only Python 3.9+ standard library and `pytest` for the test harness.

To run the full test suite:
```bash
pytest
```

Or with detailed verbosity:
```bash
pytest -v
```
