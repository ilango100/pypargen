# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import io

from pypargen.lr1 import Grammar, Parser
from pypargen.grm.grammar import grammar
from pypargen.lexer import PyRELexer
from pypargen.base.lexer import BaseLexer
from pypargen.base.rule import Rule


def join_str(*args):
    return ''.join(args)


# For all the terminals processing
callbacks = [join_str] * 26


def nop(a):
    return a


# For direct reductions
callbacks += [nop] * 3


def rhs_append(rhs, _ws, rhsc):
    rhs.append(rhsc)
    return rhs


def rhs_init(rhsc):
    return [rhsc]


# For building RHS
callbacks += [rhs_append, rhs_init]


def stmt(nont, _ws, _arrow, _ws2, rhs, _nl):
    return Rule(nont, rhs)


def stmt_eps(nont, _ws, _arrow, _ws2, _eps, _nl):
    return Rule(nont, [])


# For building statement
callbacks += [stmt, stmt_eps]


def grm_append(grm, stmt):
    grm.append(stmt)
    return grm


def grm_init():
    return Grammar()


# Final grammar!
callbacks += [grm_append, grm_init]


class GrmParser(Parser):
    def __init__(self, lexerClass: type[BaseLexer] = PyRELexer):
        super().__init__(grammar, callbacks, lexerClass)

    def parse(self, inpt: io.RawIOBase) -> Grammar:
        return super().parse(inpt)
