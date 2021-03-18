# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import io
from typing import Callable, Optional

from pypargen.base.lexer import BaseLexer
from pypargen.lexer.pyre import PyRELexer
from pypargen.base.parser import BaseParser
from pypargen.base.token import Token
from pypargen.lr1.grammar import Grammar


class Parser(BaseParser):
    """Parser is an LR(1) parser"""

    def __init__(self,
                 grammar: Grammar,
                 callbacks: list[Callable],
                 lexerClass: type[BaseLexer] = PyRELexer,
                 whitespaces: Optional[str] = None):
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
        super().__init__(grammar, lexerClass, whitespaces)
        self.table = grammar.parse_table()
        self.callbacks = callbacks

    def parse(self, inpt: io.RawIOBase) -> any:
        """Start parsing the input stream and provide the final result from\
        callbacks."""
        lexer = self.lexerClass(self.grammar.terminals, inpt, self.whitespaces)
        states = [0]
        tokens = [None]

        token = lexer.nextToken(
            [x for x in self.table[0] if x.startswith('"')])
        while True:
            if (nxt := self.table[states[-1]].get(token.type, None)) is None:
                if token.type == '$':
                    raise EOFError("Unexpected EOF")
                raise SyntaxError("Unexpected token",
                                  ("input", 0, 0, token.type))
            if isinstance(nxt, int):
                states.append(nxt)
                tokens.append(token)

                # Read the next token
                token = lexer.nextToken(
                    [x for x in self.table[nxt] if x.startswith('"')])
                continue

            if nxt == 'c':
                assert len(states) == len(tokens) == 2
                return tokens[1].content

            # Get the reduction rule
            rule_num = int(nxt[1:])
            rule = self.grammar[rule_num]

            # Get RHS tokens and pop them off the stack
            rhs_len = -len(rule.rhs) if rule.rhs else len(tokens)
            rhs_tokens = tokens[rhs_len:]
            tokens = tokens[:rhs_len]
            states = states[:rhs_len]

            # Reduce RHS to LHS with callback
            lhs_content = self.callbacks[rule_num](
                *[x.content for x in rhs_tokens])
            lhs_token = Token(rule.lhs, lhs_content)
            tokens.append(lhs_token)

            # Goto
            nxt = self.table[states[-1]][rule.lhs]
            states.append(nxt)


__all__ = ["Parser"]
