# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from pypargen.base.rule import Rule


class BaseGrammar(list[Rule]):
    """Grammar defines a context free grammar. It is simply a list of rules."""

    def __init__(self, iterable=(), start=None):
        """Create grammar with iterable of rules.
        A rule can either be a tuple of lhs (str) and rhs (list of str)
        or the Rule object."""
        super().__init__([Rule(*x) for x in iterable])
        assert "__root__" not in self.nonterminals, \
            "__root__ is a reserved nonterminal"
        if start:
            assert start in self.nonterminals,\
                    "Start symbol must be valid nonterminal"
        self._start = start
        self._firsts = {('$', ): {'$'}, (): {'ϵ'}}

    @property
    def start(self) -> str:
        """Returns the start symbol for the grammar."""
        if self._start:
            return self._start
        assert len(self) >= 1, "No rules added to the grammar yet"
        return self[0].lhs

    @start.setter
    def start(self, start: str):
        """Sets the start symbol for the grammar. Checks for validity"""
        assert start in self.nonterminals,\
            "Start symbol must be a valid nonterminal"
        self._start = start

    @property
    def terminals(self) -> list[str]:
        """Returns all the terminals found from the grammar"""
        terms = []
        for _, rhs in self:
            for tok in rhs:
                if tok.startswith('"') and tok not in terms:
                    terms.append(tok)
        return terms

    @property
    def nonterminals(self) -> list[str]:
        """Returns all the nonterminals from the grammar"""
        nonterms = []
        for lhs, _ in self:
            if lhs not in nonterms:
                nonterms.append(lhs)
        return nonterms

    def __str__(self) -> str:
        return '\n'.join(map(str, self)) + '\n'

    def first(self, tokens: list[str]) -> list[str]:
        """Returns the first set for a list of tokens"""
        if (ttokens := tuple(tokens)) in self._firsts:
            return self._firsts[ttokens]

        if tokens[0].startswith('"'):
            firsts = [tokens[0]]
            # Memoization
            self._firsts[tuple(tokens)] = firsts
            return firsts

        firsts = []
        for lhs, rhs in self:
            if tokens[0] == lhs:
                recursive = False
                # NOTE: Only first RHS token verified
                if rhs and lhs == rhs[0]:
                    # Left recursive, check if empty
                    for lhsi, rhsi in self:
                        if lhsi == lhs and len(rhsi) <= 0:
                            recursive = True
                            break
                    if not recursive:
                        # Recursive without epsilon rule
                        continue

                for f in self.first(rhs[1:] if recursive else rhs):
                    if f not in firsts:
                        firsts.append(f)

        if 'ϵ' in firsts:
            firsts.remove('ϵ')
            for f in self.first(tokens[1:]):
                if f not in firsts:
                    firsts.append(f)

        # Memoization
        self._firsts[tuple(tokens)] = firsts

        return firsts
