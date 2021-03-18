# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only
"""This example shows how to build a json parser"""

import pypargen as pgen
import sys
import pathlib

grm_parser = pgen.GrmParser(pgen.Lexer)
with (pathlib.Path(__file__).parent / "json.grm").open() as fp:
    json_grm = grm_parser.parse(fp)


def nop(a):
    return a


callbacks = [nop] * 4


def true(_):
    return True


def false(_):
    return False


def null(_):
    return None


callbacks += [true, false, null]


def kvpair(key, _colon, val):
    return (key, val)


def kvpairs_append(kvpairs, _comma, kvpair):
    key, val = kvpair
    kvpairs[key] = val
    return kvpairs


def kvpairs_init(kvpair):
    key, val = kvpair
    return {key: val}


def object_empty(_left, _right):
    return {}


def object_filled(_left, kvpairs, _right):
    return kvpairs


callbacks += [
    kvpair, kvpairs_append, kvpairs_init, object_empty, object_filled
]


def vals_append(vals, _comma, val):
    vals.append(val)
    return vals


def vals_init(val):
    return [val]


def array_empty(_left, _right):
    return []


def array_filled(_left, vals, _right):
    return vals


callbacks += [vals_append, vals_init, array_empty, array_filled]


def hx(hstr):
    return chr(int(hstr, 16))


def esc(_bks, echr):
    if echr not in "bfnrt":
        return echr
    if echr == 'b':
        return '\b'
    if echr == 'f':
        return '\f'
    if echr == 'n':
        return '\n'
    if echr == 'r':
        return '\r'
    if echr == 't':
        return '\t'


def hxesc(_bks, _u, hx):
    return hx


def str_join(*args):
    return ''.join(args)


def string(_left, string1, _right):
    return string1


callbacks += [hx, esc, hxesc, nop]
callbacks += [str_join] * 2
callbacks += [string]

# Number
callbacks += [float]

json_parser = pgen.Parser(json_grm,
                          callbacks,
                          pgen.Lexer,
                          whitespaces=" \t\r\n")

parsed = json_parser.parse(sys.stdin)
print(parsed)
