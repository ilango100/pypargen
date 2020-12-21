# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
from pypargen import lr1


@pytest.fixture
def item():
    return lr1.Item('a', ['b', 'c'], 0, '"a"')


def test_item_str_repr(item):
    assert str(item) == '[a -> . b c, "a"]'
    assert repr(item) == '<[a -> . b c, "a"]>'


def test_item_copy(item):
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
    return lr1.LR1Grammar([('S', ['"a"', 'S', '"a"']),
                           ('S', ['"b"', 'S', '"b"']), ('S', ['"c"'])])


def test_closure_palindrome(palindrome):
    items = set([lr1.Item('S', ['"a"', 'S', '"a"'], 0, '"a"')])
    closure = palindrome.closure(items)
    assert closure == items

    items = set([lr1.Item('S', ['"a"', 'S', '"a"'], 1, '"a"')])
    closure = palindrome.closure(items)
    true_closure = items.copy()
    true_closure.add(lr1.Item('S', ['"a"', 'S', '"a"'], 0, '"a"'))
    true_closure.add(lr1.Item('S', ['"b"', 'S', '"b"'], 0, '"a"'))
    true_closure.add(lr1.Item('S', ['"c"'], 0, '"a"'))
    assert closure == true_closure

    items = set([lr1.Item('S', ['"a"', 'S', '"a"'], 2, '"a"')])
    closure = palindrome.closure(items)
    assert closure == items

    items = set([lr1.Item('S', ['"a"', 'S', '"a"'], 3, '"a"')])
    closure = palindrome.closure(items)
    assert closure == items


def test_goto_palindrome(palindrome):
    items = set([lr1.Item('S', ['"a"', 'S', '"a"'], 0, '"a"')])
    goto = palindrome.goto(items, '"a"')
    true_goto = set([lr1.Item('S', ['"a"', 'S', '"a"'], 1, '"a"')])
    true_goto = palindrome.closure(true_goto)
    assert goto == true_goto

    items = set([lr1.Item('S', ['"a"', 'S', '"a"'], 1, '"a"')])
    goto = palindrome.goto(items, 'S')
    true_goto = set([lr1.Item('S', ['"a"', 'S', '"a"'], 2, '"a"')])
    assert goto == true_goto

    items = set([lr1.Item('S', ['"a"', 'S', '"a"'], 2, '"a"')])
    goto = palindrome.goto(items, '"a"')
    true_goto = set([lr1.Item('S', ['"a"', 'S', '"a"'], 3, '"a"')])
    assert goto == true_goto

    items = set([lr1.Item('S', ['"a"', 'S', '"a"'], 3, '"a"')])
    goto = palindrome.goto(items, '"a"')
    true_goto = set()
    assert goto == true_goto
