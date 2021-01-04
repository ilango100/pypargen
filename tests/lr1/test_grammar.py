# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
from pypargen.lr1 import grammar


@pytest.fixture
def item():
    return grammar.Item('a', ['b', 'c'], 0, '"a"')


def test_item_str_repr(item: grammar.Item):
    assert str(item) == '[a -> . b c, "a"]'
    assert repr(item) == '<[a -> . b c, "a"]>'


def test_item_copy(item: grammar.Item):
    item2 = item.copy()
    assert item.lhs == item2.lhs
    assert item.rhs == item2.rhs
    assert item.pos == item2.pos
    assert item.lookahead == item2.lookahead
    assert hash(item) == hash(item2)
    assert item == item2

    assert not item.done
    assert not item2.done
    item2.pos += 2
    assert item2.done


@pytest.fixture
def palindrome():
    return grammar.Grammar([('S', ['"a"', 'S', '"a"']),
                            ('S', ['"b"', 'S', '"b"']), ('S', ['"c"'])])


def test_closure_palindrome(palindrome: grammar.Grammar):
    items = [grammar.Item('S', ['"a"', 'S', '"a"'], 0, '"a"')]
    closure = palindrome.closure(items)
    assert closure == items

    items = [grammar.Item('S', ['"a"', 'S', '"a"'], 1, '"a"')]
    closure = palindrome.closure(items)
    true_closure = items.copy()
    true_closure.append(grammar.Item('S', ['"a"', 'S', '"a"'], 0, '"a"'))
    true_closure.append(grammar.Item('S', ['"b"', 'S', '"b"'], 0, '"a"'))
    true_closure.append(grammar.Item('S', ['"c"'], 0, '"a"'))
    assert closure == true_closure

    items = [grammar.Item('S', ['"a"', 'S', '"a"'], 2, '"a"')]
    closure = palindrome.closure(items)
    assert closure == items

    items = [grammar.Item('S', ['"a"', 'S', '"a"'], 3, '"a"')]
    closure = palindrome.closure(items)
    assert closure == items


def test_goto_palindrome(palindrome: grammar.Grammar):
    items = [grammar.Item('S', ['"a"', 'S', '"a"'], 0, '"a"')]
    goto = palindrome.goto(items, '"a"')
    true_goto = [grammar.Item('S', ['"a"', 'S', '"a"'], 1, '"a"')]
    true_goto = palindrome.closure(true_goto)
    assert goto == true_goto

    items = [grammar.Item('S', ['"a"', 'S', '"a"'], 1, '"a"')]
    goto = palindrome.goto(items, 'S')
    true_goto = [grammar.Item('S', ['"a"', 'S', '"a"'], 2, '"a"')]
    assert goto == true_goto

    items = [grammar.Item('S', ['"a"', 'S', '"a"'], 2, '"a"')]
    goto = palindrome.goto(items, '"a"')
    true_goto = [grammar.Item('S', ['"a"', 'S', '"a"'], 3, '"a"')]
    assert goto == true_goto

    items = [grammar.Item('S', ['"a"', 'S', '"a"'], 3, '"a"')]
    goto = palindrome.goto(items, '"a"')
    true_goto = []
    assert goto == true_goto


def test_table_palindrome(palindrome: grammar.Grammar):
    # TODO: Check the parse table
    palindrome.parse_table()


@pytest.mark.xfail(strict=True, raises=grammar.ReduceReduceConflict)
def test_table_lr2():
    rules = [("root", ['a1', 'b', '"x"']), ("root", ['a2', 'b', '"y"']),
             ("a1", ['"a"']), ("a2", ['"a"']), ("b", ['"b"'])]
    grm = grammar.Grammar(rules, "root")
    grm.parse_table()


@pytest.mark.xfail(strict=True, raises=grammar.ShiftReduceConflict)
def test_table_pda():
    palindrome = grammar.Grammar([('S', ['"a"', 'S', '"a"']),
                                  ('S', ['"b"', 'S', '"b"']), ('S', [])])
    palindrome.parse_table()


def test_eps_grammar():
    g = grammar.Grammar([('a', ['b', 'c']), ('b', []), ('b', ['"b"']),
                         ('c', ['c', '"c"']), ('c', ['"c"'])])
    # TODO: Check parse table
    g.parse_table()
