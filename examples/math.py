# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

"""This example shows how to build a simple desk calculator with parser
for basic math operations. It supports addition, subtraction, multiplication,
division and brackets, with proper precedence."""

import pypargen as pgen
import sys

math_rules = [("atom", ['"[1-9][0-9]*"']), ("atom", [r'"\("', "sub", r'"\)"']),
              ("div", ["div", '"/"', "atom"]), ("div", ["atom"]),
              ("mul", ["mul", r'"\*"', "div"]), ("mul", ["div"]),
              ("add", ["add", r'"+"', "mul"]), ("add", ["mul"]),
              ("sub", ["sub", '"-"', "add"]), ("sub", ["add"]),
              ("expr", ["sub", r'"\n\n*"'])]

math = pgen.Grammar(math_rules, "expr")


def convnum(a):
    return int(a)


def bracket(a, b, c):
    print(a, b, c)
    return b


def div(a, _, b):
    return a / b


def mul(a, _, b):
    return a * b


def add(a, _, b):
    return a + b


def sub(a, _, b):
    return a - b


def nop(a, *_):
    return a


callbacks = [convnum, bracket, div, nop, mul, nop, add, nop, sub, nop, nop]
parser = pgen.Parser(math, callbacks, pgen.Lexer, whitespaces=" \t")

result = parser.parse(sys.stdin)

print(result)
