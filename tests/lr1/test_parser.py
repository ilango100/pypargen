# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import io
import pytest
from pypargen.lr1 import parser, grammar


@pytest.fixture
def math():
    math_rules = [("atom", ['"[1-9][0-9]*"']),
                  ("atom", [r'"\("', "sub", r'"\)"']),
                  ("div", ["div", '"/"', "atom"]), ("div", ["atom"]),
                  ("mul", ["mul", r'"\*"', "div"]), ("mul", ["div"]),
                  ("add", ["add", r'"\+"', "mul"]), ("add", ["mul"]),
                  ("sub", ["sub", '"-"', "add"]), ("sub", ["add"])]
    return grammar.Grammar(math_rules, "sub")


def test_math(math: grammar.Grammar):
    def convnum(a):
        return int(a)

    def brac(_, a, b):
        return a

    def div(a, _, b):
        return a / b

    def mul(a, _, b):
        return a * b

    def add(a, _, b):
        return a + b

    def sub(a, _, b):
        return a - b

    def nop(a):
        return a

    functions = [convnum, brac, div, nop, mul, nop, add, nop, sub, nop]
    input_str = "5+1-3*4/2"
    true_result = eval(input_str)
    inputbuf = io.StringIO(input_str)
    p = parser.Parser(math, functions)
    assert abs(p.parse(inputbuf) - true_result) <= 1e-6


def test_palindrome():
    palindrome = grammar.Grammar([('S', ['"a"', 'S', '"a"']),
                                  ('S', ['"b"', 'S', '"b"']), ('S', ['"c"'])])

    def half(a, S=None, b=None):
        if b:
            return a + S
        return ""

    functions = [half] * 3
    input_str = "bbacabb"
    inputbuf = io.StringIO(input_str)

    p = parser.Parser(palindrome, functions)
    assert p.parse(inputbuf) == "bba"


@pytest.mark.xfail(strict=True)
def test_palindrome_invalid():
    palindrome = grammar.Grammar([('S', ['"a"', 'S', '"a"']),
                                  ('S', ['"b"', 'S', '"b"']), ('S', ['"c"'])])

    def half(a, S=None, b=None):
        if b:
            return a + S
        return ""

    functions = [half] * 3
    input_str = "abacabb"
    inputbuf = io.StringIO(input_str)

    p = parser.Parser(palindrome, functions)
    assert p.parse(inputbuf) == "aba"


@pytest.mark.xfail(strict=True, raises=EOFError)
def test_eof_error():
    palindrome = grammar.Grammar([('S', ['"a"', 'S', '"a"']),
                                  ('S', ['"b"', 'S', '"b"']), ('S', ['"c"'])])

    def nop(*args):
        pass

    functions = [nop] * 3
    input_str = "abacab"
    inputbuf = io.StringIO(input_str)

    p = parser.Parser(palindrome, functions)
    assert p.parse(inputbuf) == "aba"


def test_eps_grammar():
    g = grammar.Grammar([('a', ['b', 'c']), ('b', []), ('b', ['"b"']),
                         ('c', ['c', '"c"']), ('c', ['"c"'])])

    def reducer(*args):
        return list(args)

    p = parser.Parser(g, [reducer] * len(g))
    assert p.parse(io.StringIO("ccc")) == [[], [[['c'], 'c'], 'c']]
