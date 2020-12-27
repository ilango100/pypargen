# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import Iterable
import re
import io

from pypargen.base.token import Token
from pypargen.base.lexer import UnexpectedCharacter, BaseLexer


class PyRELexer(BaseLexer):
    """Lexical tokenizer based on re library."""

    def __init__(self, terminals: list[str], inpt: io.RawIOBase):
        """Initialize lexer with terminals that should be looked for and input
        stream"""
        super().__init__(terminals, inpt)
        self._patterns = {patt: re.compile(patt[1:-1]) for patt in terminals}

        # Read the whole input (No other way to use re)
        self.str = inpt.read()
        if hasattr(self.str, "decode"):
            self.str = self.str.decode()
        self.pos = 0
        self.stopped = False

    def __iter__(self) -> Iterable[Token]:
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
        for patt in self.terminals:
            if match := self._patterns[patt].match(self.str, self.pos):
                term = match.group(0)
                self.pos += len(term)
                return Token(patt, term)
        raise UnexpectedCharacter(self.str[self.pos], self.pos)
