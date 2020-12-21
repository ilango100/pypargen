# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from pypargen.grammar import Grammar


class Item:
    def __init__(self, lhs: str, rhs: list[str], pos: int, lookahead: str):
        assert pos >= 0 and pos <= len(rhs), "Dot position out of range"
        self.lhs = lhs
        self.rhs = rhs
        self.pos = pos
        self.lookahead = lookahead

    @property
    def done(self) -> bool:
        return self.pos >= len(self.rhs)

    def __eq__(self, other: 'Item') -> bool:
        return self.lhs == other.lhs and self.rhs == other.rhs and \
                self.pos == other.pos and self.lookahead == other.lookahead

    def __hash__(self) -> int:
        return hash((self.lhs, tuple(self.rhs), self.pos, self.lookahead))

    def __str__(self) -> str:
        rhs = self.rhs.copy()
        rhs.insert(self.pos, '.')
        return f"[{self.lhs} -> {' '.join(rhs)}, {self.lookahead}]"

    def __repr__(self) -> str:
        return f"<{self.__str__()}>"

    def copy(self) -> 'Item':
        return Item(self.lhs, self.rhs.copy(), self.pos, self.lookahead)


class LR1Grammar(Grammar):

    def closure(self, items: set[Item]) -> set[Item]:
        closure_items = items.copy()
        new_items = set()
        while True:
            for item in closure_items:
                if item.done:
                    continue
                if item.rhs[item.pos].startswith('"'):
                    continue
                for lhs, rhs in self:
                    if item.rhs[item.pos] == lhs:
                        for la in self.first(item.rhs[item.pos + 1:] +
                                             [item.lookahead]):
                            if la != 'ϵ':
                                new_items.add(Item(lhs, rhs, 0, la))
            if closure_items.issuperset(new_items):
                break
            else:
                closure_items = closure_items.union(new_items)
                new_items = set()
        return closure_items

    def goto(self, items: set[Item], token: str) -> set[Item]:
        goto = set()
        for item in items:
            if item.done:
                continue

            if item.rhs[item.pos] == token:
                gitem = item.copy()
                gitem.pos += 1
                goto.add(gitem)
        return self.closure(goto)
