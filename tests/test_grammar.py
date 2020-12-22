# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
from pypargen import grammar


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_empty_grammar():
    empty = grammar.Grammar()
    empty.start


def test_palindrome():
    palindrome = grammar.Grammar([('S', ['"a"', 'S', '"a"']),
                                  ('S', ['"b"', 'S', '"b"']), ('S', [])])
    assert palindrome.start == 'S'
    assert palindrome.terminals == {'"a"', '"b"'}
    assert palindrome.nonterminals == {'S'}
    assert palindrome.first(['S']) == {'"a"', '"b"', 'ϵ'}
    assert str(palindrome) == """S -> "a" S "a"
S -> "b" S "b"
S -> ϵ"""


def test_math():
    math_rules = [("atom", ['"[1-9][0-9]*"']),
                  ("atom", [r'"\("', "sub", r'"\)"']),
                  ("div", ["div", '"/"', "atom"]), ("div", ["atom"]),
                  ("mul", ["mul", r'"\*"', "div"]), ("mul", ["div"]),
                  ("add", ["add", r'"\+"', "mul"]), ("add", ["mul"]),
                  ("sub", ["sub", '"-"', "add"]), ("sub", ["add"])]
    math = grammar.Grammar(math_rules, 'sub')
    assert math.start == 'sub'
    assert math.terminals == {
        '"[1-9][0-9]*"', r'"\("', r'"\)"', '"/"', r'"\*"', r'"\+"', '"-"'
    }
    assert math.nonterminals == {"atom", "div", "mul", "add", "sub"}
    assert math.first(["sub"]) == {'"[1-9][0-9]*"', r'"\("'}
    assert math.first(["add"]) == {'"[1-9][0-9]*"', r'"\("'}
    assert math.first(["mul"]) == {'"[1-9][0-9]*"', r'"\("'}
    assert math.first(["div"]) == {'"[1-9][0-9]*"', r'"\("'}
    assert math.first(["atom"]) == {'"[1-9][0-9]*"', r'"\("'}


def test_eps_first():
    rules = [('a', []), ('b', []), ('c', ['a', 'b', '"a"'])]
    grm = grammar.Grammar(rules)

    assert grm.first(['a']) == set(['ϵ'])
    assert grm.first(['b']) == set(['ϵ'])
    assert grm.first(['c']) == set(['"a"'])


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_reserved():
    grammar.Grammar([('__root__', ['"a"', 'S', '"a"']),
                     ('__root__', ['"b"', 'S', '"b"']), ('__root__', ['"c"'])])


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_invalid_start():
    grammar.Grammar([('S', ['"a"', 'S', '"a"']), ('S', ['"b"', 'S', '"b"']),
                     ('S', [])], 'T')
