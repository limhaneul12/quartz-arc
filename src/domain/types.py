from __future__ import annotations
from dataclasses import dataclass

from typing import NewType, Literal, Final


# == 의미 타입 (의미를 이름으로 고정) ==
# 이미 검증은 경계에서 끝 내부에는 값만 보관함
UrlStr = NewType("UrlStr", str)
TitleStr = NewType("TitleStr", str)
EpochMs = NewType("EpochMs", int)
FreshMin = NewType("FreshMin", int)
Votes = NewType("Votes", int)
Reputation = NewType("Reputation", float)
LangCode = Literal["ko", "en", "ja", "zh"]


# == 도메인 모델 ==
@dataclass(frozen=True, slots=True)
class News:
    url: UrlStr
    title: TitleStr
    published_ms: EpochMs
    lang: LangCode
    source_rep: Reputation
    freshness_min: FreshMin
    votes: Votes


# 선택: 도메인 상수/경계치(필요 시)
FRESHNESS_RECENT_MIN: Final[int] = 60  # 예: 60분 이내면 '최근'으로 본다 (비즈 규칙 예시)
