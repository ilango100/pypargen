# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
import io
from pypargen.base import parser


def test_base_grammar():
    grammar = parser.BaseGrammar([('a', ['a', 'b']), ('a', []),
                                  ('b', ['"b"'])])
    parsr = parser.BaseParser(grammar)
    assert parsr.grammar == grammar


@pytest.mark.xfail(raises=NotImplementedError)
def test_base_parse_err():
    grammar = parser.BaseGrammar([('a', ['a', 'b']), ('a', []),
                                  ('b', ['"b"'])])
    parsr = parser.BaseParser(grammar)
    inputstr = "aabb"
    inputbuf = io.StringIO(inputstr)
    parsr.parse(inputbuf)
