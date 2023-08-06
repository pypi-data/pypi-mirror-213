# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT


from __future__ import annotations

from typing import Any, TypeVar

import pytest

from mappie import (
    AttrFrozenMappie,
    FactoryFrozenMappie,
    FrozenMappie,
    StrictFactoryFrozenMappie,
    StrictFrozenMappie,
)

TEST_DICT_1: dict[str, int] = {"1": 1, "2": 2, "3": 3}
TEST_DICT_1_REPR: str = "{'1': 1, '2': 2, '3': 3}"
TEST_DICT_2: dict[str, Any] = {
    "1": TEST_DICT_1,
    "2": [TEST_DICT_1],
    "3": {"value": (TEST_DICT_1,)},
    "4": {("4",)},
    "5": "5",
}
TEST_DICT_2_EXPECTED: StrictFrozenMappie[str, Any] = StrictFrozenMappie(
    {
        "1": StrictFrozenMappie(TEST_DICT_1),
        "2": [StrictFrozenMappie(TEST_DICT_1)],
        "3": StrictFrozenMappie({"value": (StrictFrozenMappie(TEST_DICT_1),)}),
        "4": {("4",)},
        "5": "5",
    }
)
TEST_DICT_3: dict[str, int] = {"a": 1, "b": 2, "c": 3}

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class ExampleFactoryFrozenMappie(FactoryFrozenMappie[_KT, _VT]):
    @classmethod
    def validator(self, data) -> dict[_KT, _VT]:
        return data


class StrictExampleFactoryFrozenMappie(StrictFactoryFrozenMappie[_KT, _VT]):
    @classmethod
    def validator(self, data) -> dict[_KT, _VT]:
        return data


class ExampleFactoryFrozenMappie2(FactoryFrozenMappie[int, str]):
    @classmethod
    def validator(cls, data):
        return {v: k for k, v in data.items()}


@pytest.mark.parametrize(
    "subcls,",
    (
        pytest.param(FrozenMappie),
        pytest.param(StrictFrozenMappie),
        pytest.param(ExampleFactoryFrozenMappie),
        pytest.param(StrictExampleFactoryFrozenMappie),
        pytest.param(AttrFrozenMappie),
    ),
)
def test_frozen_mappie(subcls: type[FrozenMappie]):
    mappie: FrozenMappie[str, int] = subcls(TEST_DICT_1)
    # __getitem__
    assert mappie["1"] == 1
    # __iter__ and keys
    assert list(mappie) == list(mappie.keys()) == ["1", "2", "3"]
    # __contains__
    assert "3" in mappie
    assert "4" not in mappie
    # __len__
    assert len(mappie) == 3
    # values
    assert list(mappie.values()) == [1, 2, 3]
    # items
    assert list(mappie.items()) == list(zip(mappie.keys(), mappie.values()))
    # __repr__
    name = subcls.__name__
    assert repr(mappie) == f"{name}({TEST_DICT_1_REPR})"
    # __eq__
    assert mappie == subcls(mappie)
    if subcls.__name__.startswith("Strict"):
        assert mappie != FrozenMappie(mappie)
        assert mappie != dict(mappie)
    else:
        assert mappie == FrozenMappie(mappie)
        assert mappie == dict(mappie)
    # __hash__
    assert len({mappie, subcls(mappie)}) == 1
    # __or__
    assert mappie | mappie == mappie


def test_factory_frozen_mappie():
    mappie: ExampleFactoryFrozenMappie2 = ExampleFactoryFrozenMappie2(TEST_DICT_1)
    assert list(mappie.keys()) == list(TEST_DICT_1.values())


def test_mappifier():
    mappy: StrictFrozenMappie[str, Any] = StrictFrozenMappie.from_mapping(TEST_DICT_2)
    assert mappy == TEST_DICT_2_EXPECTED


def test_attr_frozen_mappie():
    mappy: AttrFrozenMappie = AttrFrozenMappie(TEST_DICT_3)
    assert mappy.a == 1
    members = dir(mappy)
    assert set(members) & set(mappy) == set(mappy)
