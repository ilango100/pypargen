# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
import io
from pypargen import lexer


def test_lexer():
    terminals = ['"a"', '"b"']
    input = "aabb"
    inputbuf = io.StringIO(input)
    lexer1 = lexer.Lexer(terminals, inputbuf)

    tokens = list(lexer1)

    assert ''.join(map(lambda x: x.content, tokens[:-1])) == input

    true_token_types = [0, 0, 1, 1]
    assert [x.type for x in tokens
            ] == [terminals[i] for i in true_token_types] + ['$']


def test_math():
    terminals = [
        '"[1-9][0-9]*"', r'"\("', r'"\)"', '"/"', r'"\*"', r'"\+"', '"-"'
    ]
    input = "(1+2)/(4-1)"
    inputbuf = io.BytesIO(input.encode())
    lexer1 = lexer.Lexer(terminals, inputbuf)

    tokens = list(lexer1)

    assert ''.join(map(lambda x: x.content, tokens[:-1])) == input

    true_token_types = [1, 0, 5, 0, 2, 3, 1, 0, 6, 0, 2]
    assert [x.type for x in tokens
            ] == [terminals[i] for i in true_token_types] + ['$']


@pytest.mark.xfail(strict=True, raises=lexer.InvalidCharacter)
def test_invalid():
    terminals = ['"a"', '"b"']
    input = "aabxab"
    inputbuf = io.StringIO(input)
    lexer1 = lexer.Lexer(terminals, inputbuf)

    list(lexer1)
