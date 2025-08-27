# src/core/errors.py
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Final


class ErrorCode(str, Enum):
    INVALID_LANG = "INVALID_LANG"
    TIMEOUT = "TIMEOUT"
    RETRY_EXHAUSTED = "RETRY_EXHAUSTED"


@dataclass(frozen=True, slots=True)
class AppError:
    code: ErrorCode
    message: str


# 선택: 공용 상수(문구 재사용)
ERR_INVALID_LANG: Final[AppError] = AppError(ErrorCode.INVALID_LANG, "unsupported language")
