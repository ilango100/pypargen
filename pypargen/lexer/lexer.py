# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import io
from typing import Optional

from pypargen.base.lexer import BaseLexer, UnexpectedCharacter,\
        UnregisteredTerminal
from pypargen.base.token import Token
from pypargen.lexer import fsm, re


class Lexer(BaseLexer):
    """Lexer built with RE parser and FSM library right inside pypargen."""

    def __init__(self,
                 terminals: list[str],
                 inpt: io.RawIOBase,
                 whitespaces: Optional[str] = None):
        """Initiallize the lexer. Similar to base initialization arguments."""
        super().__init__(terminals, inpt, whitespaces)
        if self.whitespaces:
            self.whitespaces = list(self.whitespaces)
        else:
            self.whitespaces = []
        self._re_parser = re.REParser()
        self.nfa_starts = {}

        # Build the NFA's and combine them
        for term in self.terminals:
            nfa = self._re_parser.parse(term[1:-1])
            nfa.end.token = term
            self.nfa_starts[term] = nfa.start

        self.stopped = False
        self.pos = 0
        self.next_char()

    def next_char(self):
        self.buf = self.input.read(1)
        self.pos += len(self.buf)
        if hasattr(self.buf, 'decode'):
            self.buf = self.buf.decode()

    def nextToken(self, terminals: Optional[list[str]] = None) -> Token:
        """Request next token from the Lexer. Pass optional terminals to look
        for only these terminals."""
        if self.stopped:
            raise StopIteration

        # First, skip whitespaces
        while self.buf in self.whitespaces:
            self.next_char()

        if self.buf == '':
            self.stopped = True
            return Token('$', None)

        if terminals is None:
            terminals = self.terminals
        else:
            for term in terminals:
                if term not in self.terminals:
                    raise UnregisteredTerminal(term)

        state = fsm.DFANode({self.nfa_starts[term] for term in terminals})
        content = ''

        while self.buf != '':
            nstate = state.move(self.buf)
            if not nstate:
                break

            # Next state
            state = nstate
            content += self.buf

            # Read next
            self.next_char()

        if not state.tokens:
            raise UnexpectedCharacter(self.buf, self.pos, terminals)

        for term in terminals:
            if term in state.tokens:
                break
        else:
            raise UnexpectedCharacter(self.buf, self.pos, terminals)

        return Token(term, content)
