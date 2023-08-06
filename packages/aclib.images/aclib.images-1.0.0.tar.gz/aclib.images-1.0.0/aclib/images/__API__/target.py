from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self, Callable
    from .dotset import Dotset

class TargetList(object):
    @classmethod
    def _new_(cls, *logicgroups: tuple[list[Target]] | tuple[ list[int], list[int], Callable[[int,int], Target] ]) -> Self:
        self = super().__new__(cls)
        self._init_(*logicgroups)
        return self

    def _init_(self, *logicgroups):
        self._logicgroups = [*logicgroups]

    def __new__(cls):
        return cls._new_(([],))

    def __len__(self):
        return sum(len(logicgroup[0]) for logicgroup in self._logicgroups)

    def __getitem__(self, index) -> Target:
        if index < 0:
            index = self.__len__() + index
        if index >= 0:
            for logicgroup in self._logicgroups:
                targetnum = len(logicgroup[0])
                if index < targetnum:
                    if len(logicgroup) == 1:
                        return logicgroup[0][index]
                    return logicgroup[2](logicgroup[0][index], logicgroup[1][index])
                index -= targetnum
        raise IndexError(
            'targetlist index out of range')

    def __repr__(self):
        return f'<{self.__class__.__name__} x{self.__len__()} {list(self)}>'

    def __bool__(self):
        return bool(self.__len__())

    def __add__(self, other) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{type(other).__name__}'")
        return self.__class__._new_(*self._logicgroups, *other._logicgroups)


    def append(self, target: Target):
        if len(self._logicgroups[-1])==3:
            self._logicgroups.append(([],))
        self._logicgroups[-1][0].append(target)

    def join(self, start: int = 0, end: int = None) -> Target:
        selflen = len(self)
        if end is None: end = selflen
        if start < 0: start = max(0, selflen + start)
        if end < 0: end = max(0, selflen + end)
        start, end = min(start, selflen), min(end, selflen)
        if start < end:
            targets = [self[i] for i in range(start, end)]
            name = ''.join(map(lambda t: t.name, targets))
            avgsim = sum(map(lambda t: t.similarity, targets)) / len(targets)
            return Target(name, targets[0].start, targets[-1].end, avgsim)
        else: return Target.none


class TargetMeta(type):
    none = property(lambda self: _none)

    def __new__(mcs, name, base, attr):
        attr['none'] = mcs.none
        return super().__new__(mcs, name, base, attr)

class Target(object, metaclass=TargetMeta):
    none: Target

    @classmethod
    def DotsetTarget(cls, pos: tuple[int,int], dotset: Dotset, similarity) -> Self:
        return cls(dotset.name, pos, (pos[0]+dotset.size[0], pos[1]+dotset.size[1]), similarity)

    def __init__(self, name: str, start: tuple[int,int], end: tuple[int,int], similarity: float):
        self.name = name
        self.start = start
        self.end = end
        self.similarity = similarity

    @property
    def center(self):
        return int((self.start[0] + self.end[0]) / 2), int((self.start[1] + self.end[1]) / 2)

    def __repr__(self):
        if self != self.none:
            keys = ('name', 'start', 'center', 'end', 'similarity')
            values = (getattr(self, k) for k in keys)
            items = '{' + ", ".join([f"{k}: {v.__repr__()}" for k,v in zip(keys, values)]) + '}'
            return f'<{self.__class__.__name__} {items}>'
        else: return f'{self.__class__.__name__}.none'

    def __bool__(self):
        return self != self.none

_none = Target('', (-1,-1), (-1,-1), 0.0)
