# src/core/result.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, NoReturn, TypeVar, Union, overload

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
F = TypeVar("F")


@dataclass(frozen=True, slots=True)
class Ok(Generic[T]):
    value: T


@dataclass(frozen=True, slots=True)
class Err(Generic[E]):
    error: E


Result = Ok[T] | Err[E]

# --- helpers (모두 "값" 변환/조합. 예외 없음) ---


def is_ok(r: Result[T, E]) -> bool:
    return isinstance(r, Ok)


def is_err(r: Result[T, E]) -> bool:
    return isinstance(r, Err)


def map_(r: Result[T, E], f: Callable[[T], U]) -> Result[U, E]:
    return Ok(f(r.value)) if isinstance(r, Ok) else r  # type: ignore[return-value]


def map_err(r: Result[T, E], f: Callable[[E], F]) -> Result[T, F]:
    return Err(f(r.error)) if isinstance(r, Err) else r  # type: ignore[return-value]


def bind(r: Result[T, E], f: Callable[[T], Result[U, E]]) -> Result[U, E]:
    return f(r.value) if isinstance(r, Ok) else r  # type: ignore[return-value]


def or_else(r: Result[T, E], f: Callable[[E], Result[T, F]]) -> Result[T, F]:
    return f(r.error) if isinstance(r, Err) else r  # type: ignore[return-value]


@overload
def unwrap_or(r: Result[T, E], default: T) -> T: ...
@overload
def unwrap_or(r: Result[T, E], default: Callable[[], T]) -> T: ...
def unwrap_or(r: Result[T, E], default):  # type: ignore[override]
    if isinstance(default, Callable):
        return r.value if isinstance(r, Ok) else default()
    return r.value if isinstance(r, Ok) else default


def expect(r: Result[T, E], msg: str) -> T:
    if isinstance(r, Ok):
        return r.value
    # 실패도 값으로 다루지만, 테스트/스모크 등에서 단언이 필요할 때만 사용
    raise AssertionError(f"{msg}: {r.error}")


def never(_: NoReturn) -> NoReturn:
    # 분기 완전탐색에서 '도달 불가'를 명시할 때 사용 가능
    raise AssertionError("unreachable")
