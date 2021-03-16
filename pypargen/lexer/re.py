# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

"""This file contains parser and DFA constructor for regular expressions.
The goal of this module is not to compete with Python RE, but provide a
performant regular expression engine for Lexer purposes, though this module
can be used for regular expressions compilation and matching
"""

import io

from pypargen.base.lexer import BaseLexer
from pypargen.grm.grammar import rules
from pypargen.lr1.parser import Grammar, Parser
from pypargen.lexer import fsm, pyre


def nop(a: any):
    return a


callbacks = [nop]


def rng(chr_rng: str) -> str:
    frm, _, to = chr_rng
    assert frm <= to, "Range item invalid"
    return ''.join(map(chr, range(ord(frm), ord(to) + 1)))


callbacks += [rng] * 3


def char(char: str, esc_char: str = None) -> str:
    if char == '\\':
        char = esc_char
    if esc_char == 'r':
        char = '\r'
    if esc_char == 'n':
        char = '\n'
    if esc_char == 't':
        char = '\t'
    return char


callbacks += [char] * 2

# sqc -> rng | chr
callbacks += [nop] * 2


def sqs(sqs: str, sqc: str = ''):
    return sqs + sqc


callbacks += [sqs] * 2


def sq(_left, sqs, _right) -> fsm.NFA:
    nfa = fsm.NFA()
    for c in sqs:
        nfa.start.add_transition(c, nfa.end)
    return nfa


callbacks += [sq]


def rd(_left: str, re: fsm.NFA, _right: str):
    return re


def rd_empty(_left: str, _right: str) -> fsm.NFA:
    empty = fsm.NFA()
    empty.start.add_transition('', empty.end)
    return empty


callbacks += [rd, rd_empty]

# stc -> sq | rd
callbacks += [nop] * 2


# stc -> chr
def char_to_nfa(char: str) -> fsm.NFA:
    nfa = fsm.NFA()
    nfa.start.add_transition(char, nfa.end)
    return nfa


callbacks += [char_to_nfa]


def st(stc: fsm.NFA, _star) -> fsm.NFA:
    nfa = fsm.NFA()
    nfa.start.add_transition('', stc.start)
    stc.end.add_transition('', nfa.end)
    nfa.start.add_transition('', nfa.end)
    stc.end.add_transition('', stc.start)
    return nfa


callbacks += [st]

# rec -> sq | rd | st
callbacks += [nop] * 3

# rec -> chr
callbacks += [char_to_nfa]


def res_append(res: fsm.NFA, rec: fsm.NFA) -> fsm.NFA:
    res.end.add_transition('', rec.start)
    return fsm.NFA(res.start, rec.end)


# res -> res rec | recc
callbacks += [res_append, nop]


def re(re: fsm.NFA, _or: str, res: fsm.NFA) -> fsm.NFA:
    nfa = fsm.NFA()
    nfa.start.add_transition('', re.start)
    nfa.start.add_transition('', res.start)
    re.end.add_transition('', nfa.end)
    res.end.add_transition('', nfa.end)
    return nfa


# re -> re "\|" res | res
callbacks += [re, nop]


re_rules = rules[:len(callbacks)]
re_grm = Grammar(re_rules, "re")


class REParser(Parser):
    """Regular Expression parser. This parser supports only basic
    meta-characters: |, *, (, ), [, ]
    Other meta-characters like ., +, ? are taken literally.

    It is simpler to implement these meta-characters with supported ones:
    (ab)+ -> ab(ab)*
    [0-9]*(.[0-9][0-9]*)? -> [0-9]*((.[0-9][0-9]*)|())
    . -> [ !#$%&'+,-./0-9:;<=>?@A-Z^_`a-z{}~]

    The regular expression must never be an empty string, to indicate empty
    pattern, use "()".
    """

    def __init__(self, lexerClass: type[BaseLexer] = pyre.PyRELexer):
        "Initialize the parser. See help(BaseParser) for more details"
        super().__init__(re_grm, callbacks, lexerClass)

    def parse(self, re: str) -> fsm.NFA:
        "Parse the regular expression from the string"
        return super().parse(io.StringIO(re))


compiler = None


def compile(re: str) -> fsm.DFA:
    """Compile a regular expression into a DFA. The compiled DFA provides
    match method to match a string:
    ```
    dfa = re.compile("a*b")
    dfa.match("aaabb") # returns ({"match"}, 4)
    ```
    """
    global compiler
    if not compiler:
        compiler = REParser()
    nfa = compiler.parse(re)
    nfa.end.token = "match"
    return fsm.DFA(nfa)
