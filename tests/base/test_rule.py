# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from pypargen.base import rule


def test_str_rule():
    r = rule.Rule('a', ['b', 'c'])
    assert str(r) == "a\t-> b c"


def test_str_eps():
    r = rule.Rule('a', [])
    assert str(r) == "a\t-> ϵ"


def test_repr_rule():
    r = rule.Rule('a', ['b', 'c'])
    assert repr(r) == "<a\t-> b c>"


def test_repr_eps():
    r = rule.Rule('a', [])
    assert repr(r) == "<a\t-> ϵ>"


def test_hash():
    r1 = rule.Rule('a', ['b', 'c'])
    r2 = rule.Rule('a', [])
    assert hash(r1) != hash(r2)
