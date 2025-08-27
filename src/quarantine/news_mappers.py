# src/quarantine/mappers/news_mappers.py
from __future__ import annotations
from typing import Any

from pydantic import HttpUrl
from quarantine.loose_dto import RawNewsLoose
from schemas.dto import RawNewsDTO
from quarantine.mapper_registry import register


# 예시 1) "alpha" 공급자: link/headline/ts_ms 키 사용
def _alpha_mapper(x: RawNewsLoose) -> RawNewsDTO:
    return RawNewsDTO(
        url=x.get("link") or x["url"],  # 느슨 → 엄격
        title=x.get("headline") or x["title"],
        published_ms=x.get("ts_ms") or x["published_ms"],
        lang=x["lang"],
        source_rep=x.get("source_rep", 0.5),
        freshness_min=x["freshness_min"],
        votes=x.get("votes", 0),
    )


# 예시 2) "beta" 공급자: url/title/published_ms 표준 키 사용
def _beta_mapper(x: RawNewsLoose) -> RawNewsDTO:
    return RawNewsDTO(
        url=x["url"],
        title=x["title"],
        published_ms=x["published_ms"],
        lang=x["lang"],
        source_rep=x.get("source_rep", 0.7),
        freshness_min=x["freshness_min"],
        votes=x.get("votes", 0),
    )


# 등록(모듈 import 시 자동 등록)
register("alpha", _alpha_mapper)
register("beta", _beta_mapper)
