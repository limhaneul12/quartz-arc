from __future__ import annotations

from schemas.dto import RawNewsDTO
from domain.types import (
    News,
    EpochMs,
    FreshMin,
    Reputation,
    TitleStr,
    UrlStr,
    Votes,
)


# 경계에서 이미 검증이 완료 되었으니..
# 여기서는 형 변환만 수행하고 추가 검증은 금지함
def to_domain(dto: RawNewsDTO) -> News:
    return News(
        url=UrlStr(str(dto.url)),  # HttpUrl → str 의미 타입
        title=TitleStr(dto.title),
        published_ms=EpochMs(dto.published_ms),
        lang=dto.lang,
        source_rep=Reputation(dto.source_rep),
        freshness_min=FreshMin(dto.freshness_min),
        votes=Votes(dto.votes),
    )
