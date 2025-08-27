# tests/unit/test_domain_types.py
from __future__ import annotations
import pytest
from domain.types import News, UrlStr, TitleStr, EpochMs, FreshMin, Votes, Reputation


def test_news_value_object_shape() -> None:
    n = News(
        url=UrlStr("https://x.y"),
        title=TitleStr("T"),
        published_ms=EpochMs(1_700_000_000_000),
        lang="ko",
        source_rep=Reputation(0.3),
        freshness_min=FreshMin(5),
        votes=Votes(1),
    )
    # ✅ NewType은 런타임에 원시 타입과 동일하므로 원시 타입을 확인
    assert isinstance(n.url, str)
    assert isinstance(n.title, str)
    assert isinstance(n.published_ms, int)
    assert isinstance(n.freshness_min, int)
    assert isinstance(n.votes, int)
    assert isinstance(n.source_rep, float)


def test_news_is_immutable() -> None:
    n = News(
        url=UrlStr("https://x.y"),
        title=TitleStr("T"),
        published_ms=EpochMs(1_700_000_000_000),
        lang="en",
        source_rep=Reputation(0.9),
        freshness_min=FreshMin(10),
        votes=Votes(3),
    )
    with pytest.raises(Exception):
        # dataclass(frozen=True) -> 재할당 불가
        # type: ignore[attr-defined]
        n.votes = Votes(10)
