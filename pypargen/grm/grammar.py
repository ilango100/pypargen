# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from pypargen.lr1 import Grammar

rules = [
    ("ws", [r'"[ \t][ \t]*"']),
    ("rng", [r'"[a-z]-[a-z]"']),
    ("rng", [r'"[A-Z]-[A-Z]"']),
    ("rng", [r'"[0-9]-[0-9]"']),
    ("chr", [r'"\\"', r'"[\\\"\[\]\(\)\*\|rnt.]"']),
    ("chr", ['"[ !#$%&\'+,-./0-9:;<=>?@A-Z^_`a-z{}~ϵ]"']),
    ("sqc", ["rng"]),
    ("sqc", ["chr"]),
    ("sqs", ["sqs", "sqc"]),
    ("sqs", ["sqc"]),
    ("sq", [r'"\["', "sqs", r'"\]"']),
    ("rd", [r'"\("', "re", r'"\)"']),
    ("rd", [r'"\("', r'"\)"']),
    ("stc", ["sq"]),
    ("stc", ["rd"]),
    ("stc", ["chr"]),
    ("st", ["stc", r'"\*"']),
    ("rec", ["sq"]),
    ("rec", ["rd"]),
    ("rec", ["st"]),
    ("rec", ["chr"]),
    ("res", ["res", "rec"]),
    ("res", ["rec"]),
    ("re", ["re", r'"\|"', "res"]),
    ("re", ["res"]),
    ("term", [r'"\""', "re", r'"\""']),
    ("nont", [r'"[a-zA-Z][a-zA-Z]*"']),
    ("rhsc", ["term"]),
    ("rhsc", ["nont"]),
    ("rhs", ["rhs", "ws", "rhsc"]),
    ("rhs", ["rhsc"]),
    ("stmt", ["nont", "ws", r'"->"', "ws", "rhs", r'"(\r\n|\n)(\r\n|\n)*"']),
    ("stmt", ["nont", "ws", r'"->"', "ws", r'"ϵ"', r'"(\r\n|\n)(\r\n|\n)*"']),
    ("grm", ["grm", "stmt"]),
    ("grm", [])
]  # yapf: disable

grammar = Grammar(rules, "grm")
