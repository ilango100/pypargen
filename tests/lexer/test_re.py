# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from pypargen.lexer import re


def test_re_star():
    compiled = re.compile('a*b')
    assert compiled.match("abc")[1] == 2
    assert compiled.match("aaabcd")[1] == 4
    assert compiled.match("bbc")[1] == 1
    assert not compiled.match("caaab")


def test_re_or():
    compiled = re.compile('a*b|b*a')
    assert compiled.match("abc")[1] == 2
    assert compiled.match("aaabcd")[1] == 4
    assert not compiled.match("caaab")

    assert compiled.match("bbac")[1] == 3
    assert not compiled.match("bbbbb")


def test_re_rdb():
    compiled = re.compile('(abc)*bca')

    assert compiled.match("abcbca")[1] == 6
    assert compiled.match("abcabcbca")[1] == 9
    assert not compiled.match("abbca")


def test_re_sqb():
    compiled = re.compile('s[a-cF-I%$7-9]*')

    assert compiled.match("saI7%")[1] == 5
    assert compiled.match("s$9cIP")[1] == 5
    assert not compiled.match("$97IP")


def test_re_or_empty():
    compiled = re.compile('[0-9][0-9]*(()|.[0-9][0-9]*)')

    assert compiled.match("0.909")[1] == 5
    assert compiled.match("90")[1] == 2
    assert not compiled.match(".29")


def test_esc_chars():
    compiled = re.compile(r'\[*(\r|\n|\t)*\]*')

    assert compiled.match("[[[")[1] == 3
    assert compiled.match("[[[\n\t]]]")[1] == 8
    assert compiled.match("[[[\r\n\r\n]]")[1] == 9
    assert compiled.match("\n\t]]")[1] == 4
    assert compiled.match("s\n\t]]")[1] == 0
    assert compiled.match("")[1] == 0
