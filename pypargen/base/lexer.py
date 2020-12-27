# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import Iterable
import io

from pypargen.base.token import Token


class UnexpectedCharacter(Exception):
    """Exception thrown when invalid character is seen."""

    def __init__(self, char: str, pos: int):
        """Initalize the exception with the invalid character and character
        position"""
        self.pos = pos
        self.char = char
        super().__init__(
            f"Invalid character '{self.char}' at position {self.pos}")


class BaseLexer:
    """BaseLexer is an abstract class for all the lexers
    The lexer API would be used as:
    ```
    terminals = ['"[a-z]+"', '"[A-Z]+"']
    lexer = Lexer(terminals, sys.stdin)
    tokens = list(lexer)
    ```
    """

    def __init__(self, terminals: list[str], inpt: io.RawIOBase):
        """Initialize lexer with terminals that should be looked for and input
        stream"""
        assert all([x.startswith('"') for x in terminals]), \
            "All terminals must start with a \""

        self.terminals = terminals
        self.input = inpt

    def __iter__(self) -> Iterable:
        return self

    def __next__(self) -> Token:
        "Override the iterator protocol based on the lexer"
        raise NotImplementedError("Use a subclass of BaseLexer")
