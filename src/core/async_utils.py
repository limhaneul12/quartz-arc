# src/core/async_utils.py
from __future__ import annotations
import asyncio
from collections.abc import Callable, Awaitable
from dataclasses import dataclass
from typing import TypeVar

from core.result import Ok, Err, Result
from core.errors import AppError, ErrorCode

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    attempts: int = 3
    base_delay_s: float = 0.2
    factor: float = 2.0  # 지수 백오프


async def with_timeout(coro: Awaitable[T], timeout_s: float) -> Result[T, AppError]:
    try:
        val = await asyncio.wait_for(coro, timeout=timeout_s)
        return Ok(val)
    except asyncio.TimeoutError:
        return Err(AppError(ErrorCode.TIMEOUT, f"timeout after {timeout_s}s"))


async def with_retry(
    fn: Callable[[], Awaitable[Result[T, AppError]]], policy: RetryPolicy = RetryPolicy()
) -> Result[T, AppError]:
    delay = policy.base_delay_s
    for attempt in range(1, policy.attempts + 1):
        res = await fn()
        if isinstance(res, Ok):
            return res
        if attempt == policy.attempts:
            return Err(
                AppError(
                    ErrorCode.RETRY_EXHAUSTED, f"attempts={policy.attempts}, last={res.error.code}"
                )
            )
        await asyncio.sleep(delay)
        delay *= policy.factor
    # 논리상 도달 불가
    return Err(AppError(ErrorCode.RETRY_EXHAUSTED, "unexpected"))
