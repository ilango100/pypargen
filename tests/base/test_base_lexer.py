# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
import io
from pypargen.base import lexer


def test_base_terminals():
    terminals = ['"a"', '"b"']
    inpt = "aabb"
    inputbuf = io.StringIO(inpt)
    lex = lexer.BaseLexer(terminals, inputbuf)
    assert lex.terminals == terminals


@pytest.mark.xfail(raises=NotImplementedError)
def test_base_iter_err():
    terminals = ['"a"', '"b"']
    inpt = "aabb"
    inputbuf = io.StringIO(inpt)
    lex = lexer.BaseLexer(terminals, inputbuf)
    list(lex)
