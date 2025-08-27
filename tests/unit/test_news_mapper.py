# tests/unit/test_news_mapper.py
from __future__ import annotations
from tests.unit._factory import make_raw_news
from mappers.news_mapper import to_domain


def test_mapper_to_domain_happy_path() -> None:
    dto = make_raw_news()
    news = to_domain(dto)
    assert isinstance(news.url, str)
    assert isinstance(news.title, str)
    assert isinstance(news.published_ms, int)
    assert isinstance(news.freshness_min, int)
    assert isinstance(news.votes, int)
    assert isinstance(news.source_rep, float)

    # 값 보존 확인
    assert str(news.url) == str(dto.url)
    assert news.title == dto.title
    assert news.published_ms == dto.published_ms


def test_mapper_has_no_revalidation_side_effects() -> None:
    dto = make_raw_news(source_rep=0.0, votes=0)
    news = to_domain(dto)
    assert news.source_rep == 0.0
    assert news.votes == 0
