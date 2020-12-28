# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
from pypargen.lexer import fsm


def test_nfa_node_id():
    a = fsm.NFANode()
    b = fsm.NFANode()
    c = fsm.NFANode()
    d = fsm.NFANode()
    assert a != b != c != d
    assert a == a
    assert b == b
    assert c == c
    assert d == d
    assert hash(a) != hash(b) != hash(c) != hash(d)


def test_nfa_node_transition():
    start = fsm.NFANode()
    start.add_transition('a', fsm.NFANode('atok'))
    start.add_transition('b', fsm.NFANode())
    start.add_transition('c', fsm.NFANode())
    start.add_transitions('c', [fsm.NFANode(), fsm.NFANode(), fsm.NFANode()])
    assert list(start.keys()) == list("abc")
    assert start not in start['a']
    assert start not in start['b']
    assert start not in start['c']
    assert len(start['c']) == 4
    a = list(start['a'])[0]
    assert a.token == 'atok'
    assert not list(start['b'])[0].token


def test_nfa_node_multi_chars_transition():
    start = fsm.NFANode()
    start.add_chars_transition('hello', fsm.NFANode('got'))
    assert set(start.keys()) == set('hello')
    assert start['h'] == start['e'] == start['l'] == start['o']


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_nfa_node_transition_invalid():
    start = fsm.NFANode()
    start.add_transition('hello', fsm.NFANode())


def test_nfa():
    nfa = fsm.NFA()
    nfa.start.add_transition('a', nfa.end)
    nfa.start.add_transition('b', nfa.end)
    nfa.start.add_transition('c', nfa.end)
    nfa.start.add_transition('c', nfa.end)
    nfa.start.add_transition('c', nfa.end)

    assert list(nfa.start.keys()) == list("abc")
    assert nfa.end in nfa.start['a']
    assert nfa.end in nfa.start['b']
    assert nfa.end in nfa.start['c']
    assert len(nfa.start['c']) == 1


def test_dfa_node():
    a = fsm.NFANode()
    b = fsm.NFANode()
    c = fsm.NFANode()
    d = fsm.NFANode('atok')
    a.add_transition('', b)
    b.add_transition('', c)
    c.add_transition('a', d)

    dfanode = fsm.DFANode({a})
    assert b in dfanode
    assert c in dfanode
    assert d not in dfanode
    assert d in dfanode.move('a')
    assert len(dfanode.move('a')) == 1
    assert not dfanode.tokens
    assert dfanode.move('a').tokens == {"atok"}


def test_dfa_node_multi_tokens():
    a = fsm.NFANode()
    b = fsm.NFANode('b')
    c = fsm.NFANode('c')
    a.add_transition('a', b)
    a.add_transition('a', c)

    dfanode = fsm.DFANode({a})
    assert dfanode.move('a').tokens == {'b', 'c'}


def test_dfa():
    nfa = fsm.NFA(end=fsm.NFANode("end"))
    a = fsm.NFANode()
    b = fsm.NFANode()
    c = fsm.NFANode()
    d = fsm.NFANode()

    a.add_transition('', b)
    b.add_transition('', c)
    c.add_transition('a', d)

    nfa.start.add_transition('a', a)
    d.add_transition('d', nfa.end)
    nfa.end.add_transition('a', d)

    dfa = fsm.DFA(nfa)
    assert dfa.match("aad") == ({"end"}, 3)
    assert dfa.match("aadaddd") == ({"end"}, 5)
    assert not dfa.match("aaa")
    assert not dfa.match("a")


def test_dfa_empty():
    nfa = fsm.NFA()
    nfa.start.add_transition('', nfa.end)
    nfa.end.token = "empty"

    dfa = fsm.DFA(nfa)

    assert dfa.match("hello")[1] == 0
    assert dfa.match("")[1] == 0
    assert dfa.match("abcd")[1] == 0


def test_combine_dfa():
    hello = fsm.NFA()
    h = fsm.NFANode()
    e = fsm.NFANode()
    l1 = fsm.NFANode()
    l2 = fsm.NFANode()

    hello.start.add_transition('h', h)
    h.add_transition('e', e)
    e.add_transition('l', l1)
    l1.add_transition('l', l2)
    l2.add_transition('o', hello.end)
    hello.end.token = "hello"

    hola = fsm.NFA()
    h = fsm.NFANode()
    o = fsm.NFANode()
    l1 = fsm.NFANode()

    hola.start.add_transition('h', h)
    h.add_transition('o', o)
    o.add_transition('l', l1)
    l1.add_transition('a', hola.end)
    hola.end.token = "hola"

    hellohola = fsm.NFA()
    hellohola.start.add_transitions('', [hello.start, hola.start])

    hhDFA = fsm.DFA(hellohola)

    assert hhDFA.match('holahello') == ({'hola'}, 4)
    assert hhDFA.match('hellohola') == ({'hello'}, 5)
    assert not hhDFA.match('helo')
