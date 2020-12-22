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
    assert lexer1.terminals == terminals

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
    assert lexer1.terminals == terminals

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
    assert lexer1.terminals == terminals

    list(lexer1)


def test_active():
    terminals = ['"[a-z]"', '"[A-Za-z]"']
    input = "abcAbc"
    inputbuf = io.StringIO(input)
    lexer1 = lexer.Lexer(terminals, inputbuf)

    for i, tok in enumerate(lexer1):
        if tok.type == '$':
            continue
        if i >= 3:
            if i == 3:
                lexer1.terminals = terminals[1:]
            assert lexer1.terminals == terminals[1:]
            assert tok.type == terminals[1]
            assert tok.content == input[i]
        else:
            assert tok.type == terminals[0]
            assert tok.content == input[i]


@pytest.mark.xfail(strict=True, raises=lexer.InvalidActiveTerminal)
def test_active_invalid():
    terminals = ['"[a-z]"', '"[A-Za-z]"']
    input = "abcABC"
    inputbuf = io.StringIO(input)
    lexer1 = lexer.Lexer(terminals, inputbuf)

    for i, tok in enumerate(lexer1):
        if tok.type == '$':
            raise RuntimeError("Should not reach here")
        if i >= 3:
            if i == 3:
                lexer1.terminals = ['"[A-Z]"']
            assert lexer1.terminals != ['"[A-Z]"']
            assert tok.type == terminals[1]
            assert tok.content == input[i]
        else:
            assert tok.type == terminals[0]
            assert tok.content == input[i]
