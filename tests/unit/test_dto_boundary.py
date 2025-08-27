# tests/unit/test_dto_boundary.py
from __future__ import annotations
import pytest
from ._factory import make_raw_news


def test_raw_news_ok() -> None:
    dto = make_raw_news()
    assert dto.lang == "en"


def test_future_published_rejected() -> None:
    import time

    now_ms = time.time_ns() // 1_000_000
    with pytest.raises(ValueError):
        make_raw_news(published_ms=now_ms + 10 * 60_000)  # +10분


def test_freshness_inconsistent_rejected() -> None:
    import time

    now_ms = time.time_ns() // 1_000_000
    one_hour_ago = now_ms - 60 * 60_000
    with pytest.raises(ValueError):
        make_raw_news(published_ms=one_hour_ago, freshness_min=999)


def test_strict_types_no_coercion() -> None:
    with pytest.raises(Exception):
        make_raw_news(votes="100")  # type: ignore[arg-type]
