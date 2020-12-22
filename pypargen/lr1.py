# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import Union

from pypargen.grammar import Grammar
from pypargen.rule import Rule


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


class ShiftReduceConflict(Exception):
    def __init__(self, grm: 'LR1Grammar', items: set[Item], lookahead: str):
        conflicts = [item for item in items if grm.goto([item], lookahead)]
        conflicts += [
            item for item in items if item.done and item.lookahead == lookahead
        ]
        conflicts = set(conflicts)
        msg = '\n'.join(map(str, conflicts))
        super().__init__(f"Shift/Reduce Conflict:\n{msg}\n{lookahead}")


class ReduceReduceConflict(Exception):
    def __init__(self, rule1: Rule, rule2: Rule):
        msg = '\n'.join(map(str, [rule1, rule2]))
        super().__init__(f"Reduce/Reduce Conflict:\n{msg}")


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

    def parse_table(self) -> list[dict[str, Union[int, str]]]:
        init_item = Item("__root__", [self.start, '$'], 0, '$')
        set_of_items = [self.closure(set([init_item]))]

        table = [{}]

        # Dragon book: 4.7.1 Canonical LR(1) Parser
        # Build goto table
        while True:
            added = False
            for idx, items in enumerate(set_of_items):
                for sym in self.terminals.union(self.nonterminals):
                    if (gitems := self.goto(items, sym)):
                        if gitems not in set_of_items:
                            set_of_items.append(gitems)
                            table.append({})
                            added = True
                        table[idx][sym] = set_of_items.index(gitems)
                if added:
                    break
            if not added:
                break

        # Complete filling the goto entries
        for idx, state in enumerate(table):
            for sym in self.terminals.union(self.nonterminals):
                if sym not in table[idx]:
                    if (gitems := self.goto(set_of_items[idx], sym)):
                        table[idx][sym] = set_of_items.index(gitems)

        # Fill the reduction entries
        for idx, items in enumerate(set_of_items):
            for item in items:
                if item.done:

                    # If conflict, raise proper error
                    if (conflict := table[idx].get(item.lookahead, None)):
                        if isinstance(conflict, int):
                            raise ShiftReduceConflict(self, items,
                                                      item.lookahead)

                        else:
                            rule1 = self[int(conflict[1:])]
                            rule2 = Rule(item.lhs, item.rhs)
                            raise ReduceReduceConflict(rule1, rule2)

                    table[idx][item.lookahead] = \
                        f"r{self.index((item.lhs, item.rhs))}"

        return table
