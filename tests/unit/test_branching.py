# tests/unit/test_branching.py
from __future__ import annotations
import pytest

from domain.types import LangCode
from services.lang_policy import language_bucket, format_title

ALL: list[LangCode] = ["ko", "en", "ja", "zh"]  # 정적 검사에서도 커버되도록 유지


@pytest.mark.parametrize(
    "lang,expected",
    [
        ("ko", "CJK"),
        ("ja", "CJK"),
        ("zh", "CJK"),
        ("en", "Latin"),
    ],
)
def test_language_bucket_exhaustive(lang: LangCode, expected: str) -> None:
    assert language_bucket(lang) == expected


@pytest.mark.parametrize(
    "lang,title,expected",
    [
        ("ko", "zaoc 뉴스", "zaoc 뉴스"),
        ("ja", "こんにちは zaoc", "こんにちは Zaoc"),
        ("zh", "你好 zaoc", "你好 Zaoc"),
        ("en", "hello zaoc", "Hello Zaoc"),
    ],
)
def test_format_title_exhaustive(lang: LangCode, title: str, expected: str) -> None:
    assert format_title(lang, title) == expected


def test_unreachable_branch_raises_at_runtime() -> None:
    # Literal은 정적 단계에서 걸러지지만, 우리가 고의로 잘못된 인자를 넣으면
    # match의 assert_never가 런타임 예외를 발생시켜 "완전탐색 실패"를 보장한다.
    with pytest.raises(Exception):
        # type: ignore[arg-type]
        language_bucket("fr")  # mypy/Pyrefly에선 정적 에러, 런타임에서도 예외
