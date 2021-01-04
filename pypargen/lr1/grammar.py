# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import Union

from pypargen.base.grammar import BaseGrammar
from pypargen.base.rule import Rule


class Item:
    """Item is an LR(1) item"""

    def __init__(self, lhs: str, rhs: list[str], pos: int, lookahead: str):
        """Initialize the grammar item"""
        assert 0 <= pos <= len(rhs), "Dot position out of range"
        self.lhs = lhs
        self.rhs = rhs
        self.pos = pos
        self.lookahead = lookahead

    @property
    def done(self) -> bool:
        """True if the position is at the end"""
        return self.pos >= len(self.rhs)

    def __eq__(self, other: "Item") -> bool:
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

    def copy(self) -> "Item":
        return Item(self.lhs, self.rhs.copy(), self.pos, self.lookahead)


class ShiftReduceConflict(Exception):
    """Exception thrown when Shift/Reduce conflict is found"""

    def __init__(self, grm: "Grammar", items: set[Item], lookahead: str):
        """Initialize exception with conflicting items and lookahead"""
        conflicts = [item for item in items if grm.goto([item], lookahead)]
        conflicts += [
            item for item in items if item.done and item.lookahead == lookahead
        ]
        conflicts = set(conflicts)
        msg = '\n'.join(map(str, conflicts))
        super().__init__(f"Shift/Reduce Conflict:\n{msg}\nlookahead: {lookahead}")


class ReduceReduceConflict(Exception):
    """Exception thrown when Reduce/Reduce conflict is found"""

    def __init__(self, rule1: Rule, rule2: Rule):
        """Initialize exception with conflicting reduction rules"""
        msg = '\n'.join(map(str, [rule1, rule2]))
        super().__init__(f"Reduce/Reduce Conflict:\n{msg}")


class Grammar(BaseGrammar):
    """Grammar is a LR(1) grammar. The parse_table method gives the parsing
    table for the grammar."""

    def closure(self, items: list[Item]) -> list[Item]:
        """Closure calculates the closure a for set of items."""
        assert len(items) == len(set(items)), "Items must not be repeated"

        closure_items = {k: None for k in items}
        new_items = {}
        while True:
            for item in closure_items:
                if item.done:
                    continue
                if item.rhs[item.pos].startswith('"'):
                    continue
                for lhs, rhs in self:
                    if item.rhs[item.pos] == lhs:
                        for lookahead in self.first(item.rhs[item.pos + 1:] +
                                                    [item.lookahead]):
                            if lookahead != 'ϵ':
                                new_items[Item(lhs, rhs, 0, lookahead)] = None
            if set(closure_items).issuperset(new_items):
                break
            closure_items |= new_items
            new_items = {}
        return list(closure_items)

    def goto(self, items: list[Item], token: str) -> list[Item]:
        """Goto calculates the set of items to go to when a token is seen."""
        assert len(items) == len(set(items)), "Items must not be repeated"

        goto = {}
        for item in items:
            if item.done:
                continue

            if item.rhs[item.pos] == token:
                gitem = item.copy()
                gitem.pos += 1
                goto[gitem] = None
        return self.closure(goto)

    def parse_table(self) -> list[dict[str, Union[int, str]]]:
        """parse_table gives the parsing table for the grammar."""
        init_item = Item("__root__", [self.start], 0, '$')
        set_of_items = [self.closure([init_item])]

        table = [{}]
        symbols = self.terminals
        symbols.extend(self.nonterminals)

        # Dragon book: 4.7.1 Canonical LR(1) Parser
        # Build goto table
        while True:
            added = False
            for idx, items in enumerate(set_of_items):
                for sym in symbols:
                    if gitems := self.goto(items, sym):
                        if gitems not in set_of_items:
                            set_of_items.append(gitems)
                            table.append({})
                            added = True
                        table[idx][sym] = set_of_items.index(gitems)
                if added:
                    break
            if not added:
                break

        # Fill the reduction entries
        for idx, items in enumerate(set_of_items):
            for item in items:
                if item.done:

                    # If conflict, raise proper error
                    if conflict := table[idx].get(item.lookahead, None):
                        if isinstance(conflict, int):
                            raise ShiftReduceConflict(self, items,
                                                      item.lookahead)

                        rule1 = self[int(conflict[1:])]
                        rule2 = Rule(item.lhs, item.rhs)
                        raise ReduceReduceConflict(rule1, rule2)

                    if item.lhs == "__root__":
                        table[idx][item.lookahead] = 'c'
                        continue
                    table[idx][item.lookahead] = \
                        f"r{self.index((item.lhs, item.rhs))}"

        return table


__all__ = ["Grammar"]
