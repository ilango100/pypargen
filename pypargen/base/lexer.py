# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import Iterable, Optional
import io

from pypargen.base.token import Token


class UnexpectedCharacter(Exception):
    """Exception thrown when invalid character is seen."""

    def __init__(self,
                 char: str,
                 pos: int,
                 expected: Optional[list[str]] = None):
        """Initalize the exception with the invalid character and character
        position"""
        self.pos = pos
        self.char = char
        self.expected = expected

        msg = f"Invalid character '{self.char}' at position {self.pos}"
        if expected is not None:
            msg += f"\nExpected one of: {self.expected}"

        super().__init__(msg)


class UnregisteredTerminal(Exception):
    """Exception thrown when an active terminal passed is unregistered"""
    def __init__(self, terminal: str):
        """Initialize the exception with that invalid terminal"""
        self.terminal = terminal
        super().__init__(f"Unregistered terminal: {self.terminal}")


class BaseLexer:
    """BaseLexer is an abstract class for all the lexers
    The lexer API would be used as:
    ```
    terminals = ['"[a-z]+"', '"[A-Z]+"']
    lexer = Lexer(terminals, sys.stdin)
    tokens = list(lexer)
    pos = lexer.pos
    ```
    """
    def __init__(self,
                 terminals: list[str],
                 inpt: io.RawIOBase,
                 whitespaces: Optional[str] = None):
        """Initialize lexer with terminals that should be looked for and input
        stream. The order of terminals may imply precedence."""
        assert all([x.startswith('"') for x in terminals]), \
            "All terminals must start with a \""

        # Make a copy of terminals so that original changes are not reflected
        self.terminals = terminals.copy()
        self.input = inpt
        self.whitespaces = whitespaces

    def nextToken(self, terminals: Optional[list[str]] = None) -> Token:
        """Override the nextToken method based on the lexer

        The parser can call this method to change the terminals to look for.
        The order of terminals may imply precendence."""
        raise NotImplementedError("Use a subclass of BaseLexer")

    def __iter__(self) -> Iterable[Token]:
        return self

    def __next__(self) -> Token:
        """Implements iterator protocol

        This will simply call nextToken method without terminals argument
        and returns the value. Useful for simple grammars.
        """
        return self.nextToken()
