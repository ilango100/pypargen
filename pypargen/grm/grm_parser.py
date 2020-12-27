# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only
"""Rules, Grammar and Parser to parse grm format"""

import pypargen as pgen
import io

rules = [
    ("ws", [r'"[ \t][ \t]*"']),
    ("rng", [r'"[a-z]-[a-z]"']),
    ("rng", [r'"[A-Z]-[A-Z]"']),
    ("rng", [r'"[0-9]-[0-9]"']),
    ("chr", [r'"\\"', r'"[\\\"\[\]\(\)\*\|rnt.]"']),
    ("chr", ['"[ !#$%&\'+,-./0-9:;<=>?@A-Z^_`a-z{}~ϵ]"']),
    ("sqc", ["rng"]),
    ("sqc", ["chr"]),
    ("sqs", ["sqs", "sqc"]),
    ("sqs", ["sqc"]),
    ("sq", [r'"\["', "sqs", r'"\]"']),
    ("rd", [r'"\("', "re", r'"\)"']),
    ("rd", [r'"\("', r'"\)"']),
    ("stc", ["sq"]),
    ("stc", ["rd"]),
    ("stc", ["chr"]),
    ("st", ["stc", r'"\*"']),
    ("rec", ["sq"]),
    ("rec", ["rd"]),
    ("rec", ["st"]),
    ("rec", ["chr"]),
    ("res", ["res", "rec"]),
    ("res", ["rec"]),
    ("re", ["re", r'"\|"', "res"]),
    ("re", ["res"]),
    ("term", [r'"\""', "re", r'"\""']),
    ("nont", [r'"[a-zA-Z][a-zA-Z]*"']),
    ("rhsc", ["term"]),
    ("rhsc", ["nont"]),
    ("rhs", ["rhs", "ws", "rhsc"]),
    ("rhs", ["rhsc"]),
    ("stmt", ["nont", "ws", r'"->"', "ws", "rhs", r'"(\r\n|\n)(\r\n|\n)*"']),
    ("stmt", ["nont", "ws", r'"->"', "ws", r'"ϵ"', r'"(\r\n|\n)(\r\n|\n)*"']),
    ("grm", ["grm", "stmt"]),
    ("grm", [])
]

grammar = pgen.lr1.Grammar(rules, "grm")


def join_str(*args):
    return ''.join(args)


# For all the terminal processing
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
    return pgen.Rule(nont, rhs)


def stmt_eps(nont, _ws, _arrow, _ws2, _eps, _nl):
    return pgen.Rule(nont, [])


# For building statement
callbacks += [stmt, stmt_eps]


def grm_append(grm, stmt):
    grm.append(stmt)
    return grm


def grm_init():
    return pgen.lr1.Grammar()


# Final grammar!
callbacks += [grm_append, grm_init]


parser = pgen.lr1.Parser(grammar, callbacks)


__all__ = ["rules", "grammar", "parser"]
