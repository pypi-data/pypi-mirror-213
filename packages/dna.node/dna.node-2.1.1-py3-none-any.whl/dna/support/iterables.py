from __future__ import annotations

from typing import Union, TypeVar, Optional
from collections.abc import Iterable, Iterator, Callable, Generator

import itertools
from heapq import heappush
from collections import defaultdict

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

def get0(iterable): return iterable[0]
def get1(iterable): return iterable[1]

def mean(iterable) -> float:
    if not isinstance(iterable, list) and not isinstance(iterable, tuple):
        iterable = list(iterable)
    return sum(iterable) / len(iterable)

def first(iterable:Iterable[T], *, default:Optional[T]=None) -> Optional[T]:
    return next(iter(iterable), default)

def find(iterable:Iterable[T], key:K, *, keyer:Optional[Callable[[T],K]]=None) -> Optional[T]:
    for elm in iterable:
        item = keyer(elm) if keyer else elm
        if key == item:
            return elm
    return None

def find_cond(iterable:Iterable[T], cond:Callable[[T], bool]) -> Optional[T]:
    for elm in iterable:
        if cond(elm):
            return elm
    return None

def argfind(iterable:Iterable[T], key:K, *, keyer:Optional[Callable[[T],K]]=None) -> tuple[int,Optional[T]]:
    for idx, elm in enumerate(iterable):
        item = keyer(elm) if keyer else elm
        if key == item:
            return idx, elm
    return -1, None

def flatmap(func, iterable):
    return itertools.chain.from_iterable(map(func, iterable))

def flatten(iterable):
    return itertools.chain.from_iterable(iterable)

def buffer(list:list[object], count:int, skip:int=None, min_length:int=0) -> Generator[list[T], None, None]:
    if skip and skip <= 0:
        raise ValueError(f"invalid skip: {skip}")
    if min_length > count:
        raise ValueError(f"invalid: min_length({min_length}) > count({count})")
    
    idx = 0
    length = len(list)
    skip = count if skip is None else skip
    while idx < length:
        upper = min(length, idx + count)
        if upper - idx < min_length:
            break
        yield list[idx:upper]
        idx += skip

def buffer_iterable(list:Iterable[T], count:int, skip:int=None) -> Generator[list[T], None, None]:
    skip = count if skip is None else skip
    if skip <= 0:
        raise ValueError(f"invalid skip: {skip}")
    
    iterator = iter(list)
    buffer = []
    try:
        while True:
            buffer.append(next(iterator))
            if len(buffer) >= count:
                yield buffer.copy()
                buffer = buffer[skip:]
    except StopIteration as expected:
        if buffer:
            yield buffer
            
def groupby(list:Iterable[T], key_func:Callable[[T],K], *, value_func:Optional[Callable[[T],V]]=None) -> dict[K,list[Union[T,V]]]:
    def default_get_value(value): return value
    
    if value_func is None:
        value_func = default_get_value
        
    groups:dict[K,list[T]] = dict()
    for v in list:
        grp_key = key_func(v)
        if grp_key not in groups:
            groups[grp_key] = []
        groups[grp_key].append(value_func(v))
    return groups

def difference(left:Iterable[T], right:Iterable[T], *, key:Callable[[T],V]=lambda t:t) -> Generator[T, None, None]:
    return (v1 for v1 in left if find(right, key=key(v1), keyer=key) is None)


class PeekableIterator(Iterator):
    def __init__(self, iter:Iterator[T]) -> None:
        self.head:T = None
        self.iter = iter
        self.peeked = False
    
    def peek(self) -> T:
        if not self.peeked:
            self.peeked = True
            self.head = next(self.iter)
        return self.head
    
    def __next__(self):
        if self.peeked:
            self.peeked = False
            return self.head
        else:
            return next(self.iter)
        
def to_peekable(iter:Iterator[T]) -> PeekableIterator[T]:
    if not isinstance(iter, PeekableIterator):
        return PeekableIterator(iter)
    else:
        return iter

if __name__ == '__main__':
    list = list(range(10))
    for b in buffer(list, 3, 2, min_length=2):
        print(b)