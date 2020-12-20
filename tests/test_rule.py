from pypargen import rule


def test_str_rule():
    r = rule.Rule('a', ['b', 'c'])
    assert str(r) == "a -> b c"


def test_str_eps():
    r = rule.Rule('a', [])
    assert str(r) == "a -> ϵ"


def test_repr_rule():
    r = rule.Rule('a', ['b', 'c'])
    assert repr(r) == "<a -> b c>"


def test_repr_eps():
    r = rule.Rule('a', [])
    assert repr(r) == "<a -> ϵ>"


def test_hash():
    r1 = rule.Rule('a', ['b', 'c'])
    r2 = rule.Rule('a', [])
    assert hash(r1) != hash(r2)
