from abc import abstractmethod
import asyncio
from collections.abc import MutableSequence
from typing import overload, Iterable


class AsyncList(MutableSequence):
    def __init__(self):
        super(AsyncList, self).__init__()
        self.__list = []
        self.__event = asyncio.Event()

    def insert(self, index: int, value) -> None:
        self.__list[index] = value
        self.__event.set()

    def clear(self) -> None:
        self.__event.clear()

    @overload
    @abstractmethod
    def __getitem__(self, i: int):
        return self.__list[i]

    @overload
    @abstractmethod
    def __getitem__(self, s: slice):
        return self.__list[s]

    def __getitem__(self, i: int) -> MutableSequence:
        return self.__list[i]

    @overload
    @abstractmethod
    def __setitem__(self, i: int, o) -> None:
        self.__list[i] = o
        self.__event.set()

    @overload
    @abstractmethod
    def __setitem__(self, s: slice, o) -> None:
        self.__list[s] = o
        self.__event.set()

    def __setitem__(self, i: int, o) -> None:
        self.__list[i] = o
        self.__event.set()

    @overload
    @abstractmethod
    def __delitem__(self, i: int) -> None:
        self.__list.__delitem__(i)

    @overload
    @abstractmethod
    def __delitem__(self, i: slice) -> None:
        self.__list.__delitem__(i)

    def __delitem__(self, i: int) -> None:
        self.__list.__delitem__(i)

    def __len__(self) -> int:
        return len(self.__list)
