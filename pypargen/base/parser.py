# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import io

from pypargen.base.grammar import BaseGrammar
from pypargen.base.lexer import BaseLexer


class BaseParser:
    """BaseParser is an abstract class for all the parser
    The parser API would be used as:
    ```
    grammar = Grammar(...rules...)
    parser = Parser(grammar)
    parse_tree = parser.parse(sys.stdin)
    ```
    """

    def __init__(self,
                 grammar: BaseGrammar,
                 lexerClass: type[BaseLexer] = BaseLexer):
        "Initialize parser with grammar rules and an optional Lexer Class"
        self.grammar = grammar
        self.lexerClass = lexerClass

    def parse(self, inpt: io.RawIOBase) -> any:
        "Override the parse method based on the parser"
        raise NotImplementedError("Use a subclass of BaseParser")
