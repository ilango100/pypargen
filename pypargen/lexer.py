# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import re
import io

from pypargen.base.token import Token


class InvalidCharacter(Exception):
    """Exception thrown when invalid character is seen."""

    def __init__(self, char: str, pos: int):
        """Initalize the exception with the invalid character and character
        position"""
        self.pos = pos
        self.char = char
        super().__init__(
            f"Invalid character '{self.char}' at position {self.pos}")


class InvalidActiveTerminal(Exception):
    """Exception thrown when an active terminal set is invalid"""

    def __init__(self, terminals: set[str]):
        """Initialize the exception with those invalid terminals"""
        self.terminals = terminals
        super().__init__(f"Invalid terminal(s): {self.terminals}")


class Lexer:
    """Lexical tokenizer based on re library."""

    def __init__(self, terminals: list[str], inpt: io.RawIOBase):
        """Initialize lexer with terminals that should be looked for and input
        stream"""
        assert all([x.startswith('"') for x in terminals]), \
            "All terminals must start with a \""

        self._all_terminals = terminals
        self._terminals = terminals
        self._patterns = {patt: re.compile(patt[1:-1]) for patt in terminals}

        # Read the whole input (No other way to use re)
        self.str = inpt.read()
        if hasattr(self.str, "decode"):
            self.str = self.str.decode()
        self.pos = 0
        self.stopped = False

    @property
    def terminals(self):
        """Returns the currently active terminals"""
        return self._terminals

    @terminals.setter
    def terminals(self, terminals: list[str]):
        """Sets the currently active terminals. The set of terminals passed
        must be valid, i.e, passed when initializing."""
        if invalid_terms := set(terminals).difference(self._all_terminals):
            raise InvalidActiveTerminal(invalid_terms)
        self._terminals = terminals

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if self.stopped:
            raise StopIteration

        # Generate the last token as $
        if self.pos >= len(self.str):
            self.stopped = True
            return Token('$', None)

        # Check for active patterns
        # Changing self.terminals changes "active" terminals to look for
        for patt in self._terminals:
            if match := self._patterns[patt].match(self.str, self.pos):
                term = match.group(0)
                self.pos += len(term)
                return Token(patt, term)
        raise InvalidCharacter(self.str[self.pos], self.pos)


__all__ = ["Lexer"]
