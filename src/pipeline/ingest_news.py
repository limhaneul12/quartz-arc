# src/pipeline/ingest_news.py
from __future__ import annotations
from typing import Mapping, Any, cast

from quarantine.loose_dto import loose_from_mapping
from quarantine.mapper_registry import get
from mappers.news_mapper import to_domain  # DTO→도메인
from core.result import Ok, Err, Result
from core.errors import AppError, ErrorCode
from domain.types import News


def ingest_one(source: str, payload: Mapping[str, Any]) -> Result[News, AppError]:
    try:
        loose = loose_from_mapping(payload)  # 매우 느슨
        strict_dto = get(source).fn(loose)  # 공급자별 변환 + B단계 검증 (1회)
        news = to_domain(strict_dto)  # Zero-Cost 형변환
        return Ok(news)
    except KeyError as e:
        return Err(AppError(ErrorCode.INVALID_LANG, f"missing key: {e}"))
    except Exception as e:
        return Err(AppError(ErrorCode.RETRY_EXHAUSTED, f"ingest error: {e!r}"))
