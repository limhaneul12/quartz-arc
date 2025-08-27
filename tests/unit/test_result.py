# tests/unit/test_result.py
from __future__ import annotations
from core.result import Ok, Err, is_ok, is_err, map_, bind, map_err, unwrap_or


def test_ok_flow() -> None:
    r = Ok(2)
    r2 = map_(r, lambda x: x + 3)
    assert is_ok(r2) and r2.value == 5


def test_err_flow() -> None:
    r = Err("boom")
    assert is_err(r)
    assert unwrap_or(r, 10) == 10


def test_bind_chain() -> None:
    def f(x: int):
        return Ok(x + 1)

    def g(x: int):
        return Ok(x * 2)

    r = bind(bind(Ok(1), f), g)
    assert is_ok(r) and r.value == 4


def test_map_err() -> None:
    r = Err({"msg": "x"})
    r2 = map_err(r, lambda e: e["msg"])
    assert is_err(r2) and r2.error == "x"
