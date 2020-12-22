# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from pypargen import token


def test_token():
    tok = token.Token("terminal", "hello")
    assert str(tok) == "terminal(hello)"
    assert repr(tok) == "<terminal(hello)>"

    tok = token.Token('"[1-9][0-9]*"', "23")
    assert str(tok) == '"[1-9][0-9]*"("23")'
    assert repr(tok) == '<"[1-9][0-9]*"("23")>'
