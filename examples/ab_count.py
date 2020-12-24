# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

"""This example shows how to build a parser that "counts"
the number of occurences of a and b"""

import pypargen as pgen
import sys

g = pgen.lr1.Grammar()
g.append(pgen.Rule('c', ['a', 'b', '"\n\n*"']))
g.append(pgen.Rule('a', ['a', '"a"']))
g.append(pgen.Rule('a', []))
g.append(pgen.Rule('b', ['b', '"b"']))
g.append(pgen.Rule('b', ['"b"']))

# Optional here, (By default, it takes the first rule's LHS as start)
g.start = 'c'


def root(a, b, _):
    return [a, b]


def a_inc(a, _):
    return f"{int(a[:-1]) + 1}a"


def a_init():
    return "0a"


def b_inc(b, _):
    return f"{int(b[:-1]) + 1}b"


def b_init(c):
    return '1b'


callbacks = [root, a_inc, a_init, b_inc, b_init]
parser = pgen.lr1.Parser(g, callbacks, sys.stdin)
counts = parser.parse()

print(counts)
