from __future__ import annotations

from typing import Annotated, ClassVar, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    model_validator,
    StrictFloat,
    StrictInt,
    StrictStr,
)
import time


Lang = Literal["ko", "en", "ja", "zh"]

PublishedMs = Annotated[
    StrictInt,
    Field(ge=1_600_000_000_000, description="Unix timestamp in milliseconds"),
]
SourceRep = Annotated[StrictFloat, Field(ge=0.0, le=1.0, description="신뢰 0~1")]
FreshnessMin = Annotated[StrictInt, Field(ge=0, description="발행 후 경과 시간(분)")]
Votes = Annotated[StrictInt, Field(ge=0, description="커뮤니티 반응 수치")]


class RawNewsDTO(BaseModel):
    """
    -> 외부 세계 내부 진입 직전 경계 전용 DTO
        - 딱 한 번 강력하게 검증
        - 도메인 계층으로는 Pydantic을 절대 들여보내지 않음
    """

    # 모호성/암묵 변환 차단 + 불필요 금지 + 불변 유지
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        frozen=True,  # DTO 불변으로 (경계 이후에 값 오염 방지)
    )

    url: HttpUrl
    title: StrictStr
    published_ms: PublishedMs
    lang: Lang
    source_rep: SourceRep
    freshness_min: FreshnessMin
    votes: Votes

    _FRESHNESS_TOLERANCE_MIN: ClassVar[int] = 10

    @model_validator(mode="after")
    def _cross_field_checks(self) -> Self:
        now_ms = time.time_ns() // 1_000_000

        if self.published_ms > now_ms + 5 * 60_000:
            raise ValueError("published_ms 미래값 오류 (허용 5분)")

        # 2) freshness_min 일관성 검증 (외부가 주는 값 신뢰 최소화)
        expected_min: int = max(0, int((now_ms - self.published_ms) // 60_000))
        delta: int = abs(expected_min - self.freshness_min)
        if delta > self._FRESHNESS_TOLERANCE_MIN:
            raise ValueError(
                f"freshness_min 일관성 오류: 예상값≈{expected_min}±{self._FRESHNESS_TOLERANCE_MIN}, "
                f"실제값 {self.freshness_min}"
            )

        return self
