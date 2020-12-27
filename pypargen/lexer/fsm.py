# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only


class NFANode(dict[str, set["NFANode"]]):
    _next_id = 1

    def __new__(cls, token=None, *args, **kwargs):
        node = super().__new__(cls, *args, **kwargs)
        node._id = cls._next_id
        cls._next_id += 1
        node.token = token
        return node

    def __init__(self, *args, **kwargs):
        pass

    def add_transition(self, char: str, nxt: "NFANode"):
        assert len(char) <= 1,\
                "Transition can only be added with single or less character"
        if char in self:
            self[char].add(nxt)
            return
        self[char] = {nxt}

    def __eq__(self, other: "NFANode"):
        return self._id == other._id

    def __ne__(self, other: "NFANode"):
        return self._id != other._id

    def __hash__(self):
        return self._id


class NFA:
    def __init__(self, start: NFANode = None, end: NFANode = None):
        if start is None:
            start = NFANode()
        if end is None:
            end = NFANode()
        self.start = start
        self.end = end


class DFAConflict(Exception):
    def __init__(self, conflicts):
        super().__init__(f"Conflicting tokens found: {conflicts}")


class DFANode(set[NFANode]):

    def __init__(self, nfaNodes: set[NFANode]):
        super().__init__(nfaNodes)
        # Calculate the ϵ-closure of nfaNodes
        stack = list(nfaNodes)
        while stack:
            t = stack.pop(0)
            if '' not in t:
                continue
            for state in t['']:
                if state not in self:
                    self.add(state)
                    stack.insert(0, state)

    def move(self, to: str) -> "DFANode":
        destNodes = set()
        for node in self:
            if to in node:
                destNodes.update(node[to])
        return DFANode(destNodes)

    @property
    def token(self) -> str:
        tokens = [x.token for x in self if x.token]
        if len(tokens) > 1:
            raise DFAConflict(tokens)
        if not tokens:
            return False
        return tokens[0]


class DFA:
    def __init__(self, nfa: NFA):
        self.start = DFANode({nfa.start})
        self.end = nfa.end

    def match(self, string: str) -> tuple[int, str]:
        state = self.start
        i = 0
        for i, c in enumerate(string):
            nstate = state.move(c)
            if not nstate:
                break
            state = nstate
        else:
            i += 1
        if state.token:
            return (state.token, i)
        return False
