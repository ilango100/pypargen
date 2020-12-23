# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

from typing import NamedTuple


class Token(NamedTuple):
    type: str
    content: any

    def __str__(self):
        if self.type.startswith('"'):
            return f"{self.type}(\"{self.content}\")"
        return f"{self.type}({self.content})"

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __bool__(self):
        return bool(self.type)


__all__ = ["Token"]
