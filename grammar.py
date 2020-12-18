# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from rule import Rule


class Grammar(list[Rule]):
    def __init__(self, iterable=(), start=None):
        super().__init__([Rule(*x) for x in iterable])
        self._start = start

    @property
    def start(self) -> str:
        if self._start:
            return self._start
        else:
            assert len(self) >= 1, "No rules added to the grammar yet"
            return self[0].lhs

    @property
    def terminals(self) -> set[str]:
        terms = set()
        for _, rhs in self:
            terms = terms.union([x for x in rhs if x.startswith('"')])
        return terms

    @property
    def nonterminals(self) -> set[str]:
        return set([x for x, _ in self])

    def __str__(self):
        return '\n'.join(map(str, self))
