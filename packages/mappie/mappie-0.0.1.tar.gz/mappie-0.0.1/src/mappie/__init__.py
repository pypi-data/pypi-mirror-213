# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
Collections, frozen mappings, and more
"""

from __future__ import annotations

import dataclasses
from abc import abstractmethod
from collections.abc import (
    Callable,
    Collection,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    ValuesView,
)

# We deliberately import Mapping from typing.
# Older Pythons don't have __class_getitem__ at runtime.
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar

if TYPE_CHECKING:
    from typing_extensions import Self

__version__ = "0.0.1"

_T = TypeVar("_T")
_T2 = TypeVar("_T2")


def _copy_dict(mapping: Mapping[_T, _T2] | _UnsafeDict) -> dict[_T, _T2]:
    if isinstance(mapping, _UnsafeDict):
        return mapping.d
    if isinstance(mapping, dict):
        return mapping.copy()
    return {**mapping}


def _copy_list(obj: Iterable[_T]) -> list[_T]:
    if isinstance(obj, list):
        return obj.copy()
    return list(obj)


_MappieT = TypeVar("_MappieT", bound="FrozenMappie")


@dataclasses.dataclass()
class _UnsafeDict:
    d: dict
    validate: bool = True


class FrozenMappie(Generic[_T, _T2], Mapping[_T, _T2]):
    """
    Immutable Mapping class
    """

    __data: dict[_T, _T2]
    _strict_eq = False

    def __new__(cls: type[_MappieT], data: Mapping[_T, _T2] | _UnsafeDict) -> _MappieT:
        self = super().__new__(cls)
        data = _copy_dict(data)
        self.__data = data
        return self

    def __getitem__(self, key: _T) -> _T2:
        return self.__data[key]

    def __iter__(self) -> Iterator[_T]:
        return iter(self.__data)

    def __contains__(self, key) -> bool:
        return key in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def keys(self) -> KeysView[_T]:
        return self.__data.keys()

    def values(self) -> ValuesView[_T2]:
        return self.__data.values()

    def items(self) -> ItemsView[_T, _T2]:
        return self.__data.items()

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.__data!r})"

    def __eq__(self, other: object) -> bool:
        if type(self)._strict_eq and (
            not isinstance(other, FrozenMappie) or not type(other)._strict_eq
        ):
            return False
        if isinstance(other, FrozenMappie):
            other = other.__data
        return self.__data.__eq__(other)

    def __hash__(self) -> int:
        return hash(type(self)) + hash(frozenset(self.items()))

    def __or__(self: _MappieT, other: Mapping[_T, _T2]) -> _MappieT:
        return type(self)({**self, **other})

    @classmethod
    def from_mapping(cls, mapping: Mapping) -> Self:
        return Mappifier(cls).mappify(mapping)


class StrictFrozenMappie(FrozenMappie[_T, _T2]):
    """
    FrozenMappie that enforces strict equality
    """

    _strict_eq = True


class FactoryFrozenMappie(FrozenMappie[_T, _T2]):
    """
    Immutable Mapping class that accepts a `validator` factory to modify values
    """

    @classmethod
    @abstractmethod
    def validator(self, data: dict) -> dict[_T, _T2]:
        ...

    def __new__(cls, data: Mapping | _UnsafeDict):
        validate: bool = True
        new: _UnsafeDict
        if isinstance(data, _UnsafeDict):
            validate = data.validate
            new = data
        if validate:
            new = _UnsafeDict(cls.validator(_copy_dict(data)))
        return super().__new__(cls, new)

    def __or__(self, other: Mapping):
        validated: dict[_T, _T2] = self.validator(_copy_dict(other))
        new: _UnsafeDict = _UnsafeDict({**self, **validated}, False)
        return type(self)(new)


class StrictFactoryFrozenMappie(FactoryFrozenMappie[_T, _T2]):
    """
    FactoryFrozenMappie that enforces strict equality
    """

    _strict_eq = True


class AttrFrozenMappie(FrozenMappie[str, Any]):
    """
    FrozenMappie with attribute access
    """

    def __dir__(self) -> list[str]:
        return [*object.__dir__(self), *self]

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError as exc:  # pragma: no cover
            raise AttributeError(key) from exc


class Mappifier:
    """
    Apply a function to Mappings within a Mapping and Mappings within a
    Sequence into another Mapping.
    Can be used to convert a dictionary into a FrozenMappie.
    """

    def __init__(self, factory: Callable[[Mapping], object]) -> None:
        self.factory: Callable[[Mapping], object] = factory

    def collectify(self, obj: Collection) -> Collection:
        """
        Recurisvely call `self.factory` on each Mapping in a collection.
        """
        if isinstance(obj, Mapping):  # pragma: no cover
            raise TypeError(
                "Use the mappify() method instead of collectify() for Mappings"
            )
        typ = type(obj)
        obj = _copy_list(obj)
        for index, value in enumerate(obj):
            if isinstance(value, Mapping):
                obj[index] = self.mappify(value)
            elif isinstance(value, str):
                pass
            elif isinstance(value, Collection):
                obj[index] = self.collectify(value)
        obj = typ(obj)  # type: ignore[call-arg]
        return obj

    def mappify(self, obj: Mapping[Any, Any]) -> Any:
        obj = _copy_dict(obj)
        for key, value in obj.items():
            if isinstance(value, Mapping):
                obj[key] = self.mappify(value)
            elif isinstance(value, str):
                pass
            elif isinstance(value, Collection):
                obj[key] = self.collectify(value)
        return self.factory(obj)


__all__ = (
    "FrozenMappie",
    "StrictFrozenMappie",
    "FactoryFrozenMappie",
    "StrictFactoryFrozenMappie",
    "FrozenAttrMappie",
    "Mappifier",
)
