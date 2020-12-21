# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from pypargen.rule import Rule


class Grammar(list[Rule]):
    def __init__(self, iterable=(), start=None):
        super().__init__([Rule(*x) for x in iterable])
        self._start = start
        self._firsts = {}

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

    def __str__(self) -> str:
        return '\n'.join(map(str, self))

    def first(self, tokens: list[str]) -> set[str]:
        if (tt := tuple(tokens)) in self._firsts:
            return self._firsts[tt]

        firsts = set()
        if tokens[0].startswith('"'):
            firsts.add(tokens[0])
            return firsts

        if tokens[0] == '$':
            firsts.add('$')
            return firsts

        for token in tokens:
            if token.startswith('"'):
                firsts.add(token)
                break

            new_firsts = set()
            for lhs, rhs in self:
                if token == lhs:
                    if not rhs:
                        new_firsts.add('ϵ')
                        continue

                    # Avoid infinite recursion
                    # NOTE: Only first RHS token verified
                    if lhs != rhs[0]:
                        new_firsts = new_firsts.union(self.first(rhs))
            firsts = firsts.union(new_firsts)
            if 'ϵ' in firsts:
                firsts.remove('ϵ')
                continue
            break
        else:
            if 'ϵ' in new_firsts:
                firsts.add('ϵ')

        # Memoization
        self._firsts[tuple(tokens)] = firsts

        return firsts
