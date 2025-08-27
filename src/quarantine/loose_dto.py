# src/quarantine/loose_dto.py
from __future__ import annotations
from typing import Any, Mapping, TypedDict, NotRequired


# 각 소스(크롤러/서드파티)마다 제각각 들어오는 raw payload를
# 최대한 느슨하게 수용하는 형태. (모든 필드 Optional/다형 key)
class RawNewsLoose(TypedDict, total=False):
    url: str
    link: str  # 다른 소스에서 url 키가 link로 들어오는 경우
    title: str
    headline: str  # 동의어
    ts_ms: int
    published_ms: int
    lang: str
    source_rep: float
    freshness_min: int
    votes: int


def loose_from_mapping(m: Mapping[str, Any]) -> RawNewsLoose:
    # 외부 입력은 dict-like면 무엇이든 허용 (검증 X, 변환만)
    return RawNewsLoose(**{k: m[k] for k in m.keys()})
