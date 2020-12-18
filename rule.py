# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import NamedTuple


class Rule(NamedTuple):
    lhs: str
    rhs: list[str]

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs)))

    def __str__(self):
        return ':\t'.join([self.lhs, ' '.join(self.rhs)])

    def __repr__(self):
        return f"<{self.__str__()}>"
