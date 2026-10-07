"""Advanced parser for Singmaster notation, commutators, conjugates, and repetitions.

Supports:
- Basic sequences: `R U R' U'`
- Multipliers: `(R U R' U')3` or `(R U R' U') * 3`
- Commutators: `[R U R', D]` -> `R U R' D R U' R' D'`
- Conjugates: `[R: U]` -> `R U R'`
- Nested brackets: `[[R: U], D]`
"""

import re
from typing import List, Optional

from engine.moves import parse_move


def invert_move_token(token: str) -> str:
    """Inverts a single move token (e.g., 'R' -> 'R'', 'U2' -> 'U2', 'F'' -> 'F')."""
    base, mod = parse_move(token)
    if mod == "":
        inv_mod = "'"
    elif mod == "'":
        inv_mod = ""
    else:  # "2" or "2'"
        inv_mod = "2"
    return f"{base}{inv_mod}"


class ASTNode:
    """Base class for parsed algorithm nodes."""
    def expand(self) -> List[str]:
        raise NotImplementedError

    def invert(self) -> List[str]:
        raise NotImplementedError


class MoveNode(ASTNode):
    """A single face turn or rotation."""
    def __init__(self, move_str: str) -> None:
        self.move = move_str

    def expand(self) -> List[str]:
        return [self.move]

    def invert(self) -> List[str]:
        return [invert_move_token(self.move)]


class SequenceNode(ASTNode):
    """A linear sequence of nodes."""
    def __init__(self, children: List[ASTNode]) -> None:
        self.children = children

    def expand(self) -> List[str]:
        result = []
        for child in self.children:
            result.extend(child.expand())
        return result

    def invert(self) -> List[str]:
        result = []
        for child in reversed(self.children):
            result.extend(child.invert())
        return result


class RepeatedNode(ASTNode):
    """A node that is repeated N times."""
    def __init__(self, child: ASTNode, count: int) -> None:
        self.child = child
        self.count = count

    def expand(self) -> List[str]:
        result = []
        child_expanded = self.child.expand()
        for _ in range(self.count):
            result.extend(child_expanded)
        return result

    def invert(self) -> List[str]:
        result = []
        child_inverted = self.child.invert()
        for _ in range(self.count):
            result.extend(child_inverted)
        return result


class CommutatorNode(ASTNode):
    """A commutator [A, B] which expands to A B A' B'."""
    def __init__(self, a: ASTNode, b: ASTNode) -> None:
        self.a = a
        self.b = b

    def expand(self) -> List[str]:
        return self.a.expand() + self.b.expand() + self.a.invert() + self.b.invert()

    def invert(self) -> List[str]:
        # Inverse of [A, B] = (A B A' B')' = B A B' A' = [B, A]
        return self.b.expand() + self.a.expand() + self.b.invert() + self.a.invert()


class ConjugateNode(ASTNode):
    """A conjugate [A: B] which expands to A B A'."""
    def __init__(self, a: ASTNode, b: ASTNode) -> None:
        self.a = a
        self.b = b

    def expand(self) -> List[str]:
        return self.a.expand() + self.b.expand() + self.a.invert()

    def invert(self) -> List[str]:
        # Inverse of [A: B] = (A B A')' = A B' A' = [A: B']
        return self.a.expand() + self.b.invert() + self.a.invert()


class AlgorithmParser:
    """Recursive descent parser for speedcubing notation."""

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = self._lex(source)
        self.pos = 0

    def _lex(self, source: str) -> List[str]:
        """Splits the source string into parsable tokens."""
        s = re.sub(r"(//|#).*?$", "", source, flags=re.MULTILINE)
        for char in "()[],:":
            s = s.replace(char, f" {char} ")
        return s.split()

    def _peek(self) -> Optional[str]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _consume(self) -> Optional[str]:
        token = self._peek()
        if token is not None:
            self.pos += 1
        return token

    def parse(self) -> SequenceNode:
        """Parses the entire token stream into a SequenceNode."""
        nodes = self._parse_sequence_until([None])
        if self.pos < len(self.tokens):
            raise ValueError(f"Unexpected token at position {self.pos}: {self._peek()}")
        return SequenceNode(nodes)

    def _parse_sequence_until(self, stop_tokens: List[Optional[str]]) -> List[ASTNode]:
        nodes: List[ASTNode] = []
        while True:
            token = self._peek()
            if token in stop_tokens:
                break
            
            if token == "(":
                self._consume()  # Consume '('
                inner_nodes = self._parse_sequence_until([")"])
                if self._consume() != ")":
                    raise ValueError("Expected ')' to close group")
                
                group_node = SequenceNode(inner_nodes)
                # Check for multiplier
                count = 1
                next_tok = self._peek()
                if next_tok == "*":
                    self._consume()
                    count_tok = self._consume()
                    if count_tok is None or not count_tok.isdigit():
                        raise ValueError("Expected number after '*'")
                    count = int(count_tok)
                elif next_tok is not None and next_tok.isdigit():
                    count = int(self._consume())
                    
                if count != 1:
                    nodes.append(RepeatedNode(group_node, count))
                else:
                    nodes.append(group_node)
                    
            elif token == "[":
                self._consume()  # Consume '['
                a_nodes = self._parse_sequence_until([",", ":"])
                sep = self._consume()
                if sep not in [",", ":"]:
                    raise ValueError("Expected ',' or ':' inside '[' ']' block")
                
                b_nodes = self._parse_sequence_until(["]"])
                if self._consume() != "]":
                    raise ValueError("Expected ']' to close block")
                
                a_node = SequenceNode(a_nodes)
                b_node = SequenceNode(b_nodes)
                
                block_node: ASTNode
                if sep == ",":
                    block_node = CommutatorNode(a_node, b_node)
                else:
                    block_node = ConjugateNode(a_node, b_node)
                    
                # Commutators/Conjugates can also have multipliers!
                count = 1
                next_tok = self._peek()
                if next_tok == "*":
                    self._consume()
                    count_tok = self._consume()
                    if count_tok is None or not count_tok.isdigit():
                        raise ValueError("Expected number after '*'")
                    count = int(count_tok)
                elif next_tok is not None and next_tok.isdigit():
                    count = int(self._consume())
                    
                if count != 1:
                    nodes.append(RepeatedNode(block_node, count))
                else:
                    nodes.append(block_node)
                    
            elif token in [")", "]", ",", ":", "*"]:
                raise ValueError(f"Unexpected punctuation: {token}")
            else:
                # Must be a move token
                self._consume()
                nodes.append(MoveNode(token))
                
        return nodes


def parse_algorithm(algorithm: str) -> List[str]:
    """Parses advanced algorithm strings and returns a flattened list of moves."""
    parser = AlgorithmParser(algorithm)
    ast = parser.parse()
    return ast.expand()

def invert_algorithm(algorithm: str) -> List[str]:
    """Parses an algorithm and returns the flattened inverted list of moves."""
    parser = AlgorithmParser(algorithm)
    ast = parser.parse()
    return ast.invert()
