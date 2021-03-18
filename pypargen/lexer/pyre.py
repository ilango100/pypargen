# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import Optional
import re
import io

from pypargen.base.token import Token
from pypargen.base.lexer import BaseLexer, UnexpectedCharacter,\
        UnregisteredTerminal


class PyRELexer(BaseLexer):
    """Lexical tokenizer based on re library."""

    def __init__(self,
                 terminals: list[str],
                 inpt: io.RawIOBase,
                 whitespaces: Optional[str] = None):
        """Initialize lexer with terminals to be looked for and input stream"""
        super().__init__(terminals, inpt, whitespaces)
        self._patterns = {patt: re.compile(patt[1:-1]) for patt in terminals}

        self.ws_pattern = re.compile("")
        if self.whitespaces:
            self.ws_pattern = re.compile(f"[{self.whitespaces}]*")

        # Read the whole input (No other way to use re)
        self.str = inpt.read()
        if hasattr(self.str, "decode"):
            self.str = self.str.decode()
        self.pos = 0
        self.stopped = False

    def nextToken(self, terminals: Optional[list[str]] = None) -> Token:
        if self.stopped:
            raise StopIteration

        # First, skip whitespaces
        if ws := self.ws_pattern.match(self.str, self.pos):
            self.pos = ws.end()

        # Generate the last token as $
        if self.pos >= len(self.str):
            self.stopped = True
            return Token('$', None)

        # Check for active patterns
        if not terminals:
            terminals = self.terminals

        # Passing terminals changes "active" terminals to look for
        for patt in terminals:
            if patt not in self.terminals:
                raise UnregisteredTerminal(patt)
            if match := self._patterns[patt].match(self.str, self.pos):
                term = match.group(0)
                self.pos += len(term)
                return Token(patt, term)
        raise UnexpectedCharacter(self.str[self.pos], self.pos, terminals)
