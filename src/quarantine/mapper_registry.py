# src/quarantine/mapper_registry.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Final, Mapping, Any

from quarantine.loose_dto import RawNewsLoose
from schemas.dto import RawNewsDTO

MapperFn = Callable[[RawNewsLoose], RawNewsDTO]


@dataclass(frozen=True, slots=True)
class SourceMapper:
    name: str
    fn: MapperFn


_REGISTRY: dict[str, SourceMapper] = {}


def register(name: str, fn: MapperFn) -> None:
    _REGISTRY[name] = SourceMapper(name, fn)


def get(name: str) -> SourceMapper:
    return _REGISTRY[name]


def list_sources() -> tuple[str, ...]:
    return tuple(_REGISTRY.keys())
