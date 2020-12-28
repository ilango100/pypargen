# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
import io
from pypargen.lexer import pyre


def test_lexer():
    terminals = ['"a"', '"b"']
    input = "aabb"
    inputbuf = io.StringIO(input)
    lexer1 = pyre.PyRELexer(terminals, inputbuf)
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
    lexer1 = pyre.PyRELexer(terminals, inputbuf)
    assert lexer1.terminals == terminals

    tokens = list(lexer1)

    assert ''.join(map(lambda x: x.content, tokens[:-1])) == input

    true_token_types = [1, 0, 5, 0, 2, 3, 1, 0, 6, 0, 2]
    assert [x.type for x in tokens
            ] == [terminals[i] for i in true_token_types] + ['$']


@pytest.mark.xfail(strict=True, raises=pyre.UnexpectedCharacter)
def test_invalid():
    terminals = ['"a"', '"b"']
    input = "aabxab"
    inputbuf = io.StringIO(input)
    lexer1 = pyre.PyRELexer(terminals, inputbuf)
    assert lexer1.terminals == terminals

    list(lexer1)


def test_active():
    terminals = ['"[a-z]"', '"[A-Za-z]"']
    inputstr = "abcAbc"
    inputbuf = io.StringIO(inputstr)
    lexer1 = pyre.PyRELexer(terminals, inputbuf)
    i = 0

    while (tok := lexer1.nextToken(terminals)).type != '$':
        if i == 3:
            terminals = terminals[1:]
        assert tok.type == terminals[0]
        assert tok.content == inputstr[i]
        i += 1


@pytest.mark.xfail(strict=True, raises=pyre.UnregisteredTerminal)
def test_active_invalid():
    terminals = ['"[a-z]"', '"[A-Za-z]"']
    inputstr = "abcABC"
    inputbuf = io.StringIO(inputstr)
    lexer1 = pyre.PyRELexer(terminals, inputbuf)
    i = 0

    while (tok := lexer1.nextToken(terminals)).type != '$':
        assert tok.type == terminals[0]
        assert tok.content == inputstr[i]
        i += 1
        if i == 3:
            terminals = ['"[A-Z]"']
    raise RuntimeError("Should not reach here")
