# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import NamedTuple


class Rule(NamedTuple):
    """Rule is a representation of a grammar rule."""
    lhs: str
    rhs: list[str]

    def __hash__(self) -> int:
        return hash((self.lhs, tuple(self.rhs)))

    def __str__(self) -> str:
        return "\t-> ".join([self.lhs, ' '.join(self.rhs) if self.rhs else 'ϵ'])

    def __repr__(self) -> str:
        return f"<{self.__str__()}>"
