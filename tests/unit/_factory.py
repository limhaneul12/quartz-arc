# tests/unit/_factory.py
from __future__ import annotations
import time
from schemas.dto import RawNewsDTO


def make_raw_news(**overrides):
    now_ms = time.time_ns() // 1_000_000
    base = dict(
        url="https://example.com/n/1",
        title="Hello ZAOC",
        published_ms=now_ms - 10 * 60_000,  # 10분 전
        lang="en",
        source_rep=0.8,
        freshness_min=10,
        votes=5,
    )
    base.update(overrides)
    return RawNewsDTO(**base)
