# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import io
from typing import Callable

from pypargen.lr1.grammar import Grammar
from pypargen.lexer import Lexer
from pypargen.token import Token


class Parser:
    """Parser is an LR(1) parser"""

    def __init__(self, grammar: Grammar, callbacks: list[Callable],
                 inpt: io.RawIOBase):
        """Initialize parser with LR(1) grammar, callbacks and input stream

        callbacks is a list of functions that corresponding to the rules.
        For example, if the rules are:
        S -> a S a
        S -> b S b
        S -> c

        The callbacks could be:
        def rule1(a, S, _):
            return a+S

        def rule2(b, S, _):
            return b+S

        def rule3(_):
            return ""

        callbacks = [rule1, rule2, rule3]

        Note that the callbacks should take the same number of arguments as RHS
        and return a single value that will be used for next callback.
        It could be a parse (sub)tree, calculated expression etc."""
        assert len(grammar) == len(callbacks),\
            "Callbacks and grammar must be of same size"
        self.grammar = grammar
        self.table = grammar.parse_table()
        self.callbacks = callbacks
        self.lexer = Lexer(grammar.terminals, inpt)
        self.lexer.terminals = [x for x in self.table[0] if x.startswith('"')]
        self.states = [0]
        self.tokens = [None]

    def parse(self) -> Token:
        """Start parsing the input stream and provide the final result from\
        callbacks."""
        token = next(self.lexer)
        while True:
            if not token:
                token = next(self.lexer)
            nxt = self.table[self.states[-1]][token.type]
            if isinstance(nxt, int):
                self.states.append(nxt)
                self.tokens.append(token)

                # Setup lexer for next token
                self.lexer.terminals = [
                    x for x in self.table[nxt] if x.startswith('"')
                ]
                token = Token('', '')
                continue

            if nxt == 'c':
                assert len(self.states) == len(self.tokens) == 2
                return self.tokens[1].content

            # Get the reduction rule
            rule_num = int(nxt[1:])
            rule = self.grammar[rule_num]

            # Get RHS tokens and pop them off the stack
            rhs_len = -len(rule.rhs) if rule.rhs else len(self.tokens)
            rhs_tokens = self.tokens[rhs_len:]
            self.tokens = self.tokens[:rhs_len]
            self.states = self.states[:rhs_len]

            # Reduce RHS to LHS with callback
            lhs_content = self.callbacks[rule_num](
                *[x.content for x in rhs_tokens])
            lhs_token = Token(rule.lhs, lhs_content)
            self.tokens.append(lhs_token)

            # Goto
            nxt = self.table[self.states[-1]][rule.lhs]
            self.states.append(nxt)


__all__ = ["Parser"]
