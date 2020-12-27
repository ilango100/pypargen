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
    def terminals(self) -> set[str]:
        """Returns all the terminals found from the grammar"""
        terms = set()
        for _, rhs in self:
            terms = terms.union([x for x in rhs if x.startswith('"')])
        return terms

    @property
    def nonterminals(self) -> set[str]:
        """Returns all the nonterminals from the grammar"""
        return {x for x, _ in self}

    def __str__(self) -> str:
        return '\n'.join(map(str, self)) + '\n'

    def first(self, tokens: list[str]) -> set[str]:
        """Returns the first set for a list of tokens"""
        if (ttokens := tuple(tokens)) in self._firsts:
            return self._firsts[ttokens]

        firsts = set()
        if tokens[0].startswith('"'):
            firsts.add(tokens[0])
            # Memoization
            self._firsts[tuple(tokens)] = firsts
            return firsts

        for lhs, rhs in self:
            if tokens[0] == lhs:
                # Avoid infinite recursion
                # NOTE: Only first RHS token verified
                if not rhs or lhs != rhs[0]:
                    firsts = firsts.union(self.first(rhs))

        if 'ϵ' in firsts:
            firsts.remove('ϵ')
            firsts = firsts.union(self.first(tokens[1:]))

        # Memoization
        self._firsts[tuple(tokens)] = firsts

        return firsts


__all__ = ["Grammar"]
