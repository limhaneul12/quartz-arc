# src/adapters/lang_adapter.py
from __future__ import annotations
from typing import cast

from core.result import Ok, Err, Result
from core.errors import AppError, ErrorCode
from domain.types import LangCode

# 외부 입력을 내부 LangCode로 정규화 (경계 전용)
_NORMALIZE = {
    "ko": "ko",
    "kr": "ko",
    "en": "en",
    "us": "en",
    "gb": "en",
    "ja": "ja",
    "jp": "ja",
    "zh": "zh",
    "cn": "zh",
}


def to_lang_code(raw: str) -> Result[LangCode, AppError]:
    key = (raw or "").strip().lower()
    norm = _NORMALIZE.get(key)
    if norm is None:
        return Err(AppError(ErrorCode.INVALID_LANG, f"unsupported: {raw!r}"))
    # DTO에서 Literal 검증을 통과한 효과를 모사: 정적 힌트를 위해 cast
    return Ok(cast(LangCode, norm))
