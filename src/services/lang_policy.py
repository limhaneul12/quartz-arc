from __future__ import annotations

from typing import Literal, assert_never, Never, cast

from domain.types import LangCode

Bucket = Literal["CJK", "Latin"]


def language_bucket(lang: LangCode) -> Bucket:
    """
    LangCode -> 글꼴/공백/폭 규칙 등을 위해 CJK/Latin 버킷 분류
    분기 누락 시 mypy가 탐지, 런타임에서도 assert_never가 폭발.
    """
    match lang:
        case "ko" | "ja" | "zh":
            return "CJK"
        case "en":
            return "Latin"
        case _ as unreachable:
            assert_never(cast(Never, unreachable))


def format_title(lang: LangCode, title: str) -> str:
    """
    언어별 간단 포맷 예시:
      - CJK: 원형 유지
      - EN : Title Case (데모용, 실제 규칙은 팀 정책에 맞춰 교체)
    """
    match lang:
        case "ko" | "ja" | "zh":
            return title
        case "en":
            return title.title()
        case _ as unreachable:
            assert_never(cast(Never, unreachable))
