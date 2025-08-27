# main.py
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from core.result import Ok, Err, Result
from core.errors import AppError
from pipeline.ingest_news import ingest_one
from services.lang_policy import format_title
from domain.types import News, LangCode


def _load_json(path: str | None) -> Any:
    if path is None or path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _to_public_dict(n: News, *, format_en: bool = True) -> dict[str, Any]:
    """
    도메인 객체 -> 외부로 내보낼 경량 dict (필요 최소만)
    - 내부에서는 도메인 타입 유지, 출력 직전에만 평탄화 (Zero-Cost)
    """
    # dataclass라면 asdict로 안전하게 평탄화
    d = asdict(n) if is_dataclass(n) else dict(n)  # type: ignore[arg-type]
    # 언어별 제목 포맷(서비스 정책) — 유연성 국소화
    if format_en:
        d["title"] = format_title(n.lang, n.title)  # match + assert_never로 완전탐색 보장
    return d


def _handle_payload(
    source: str, payload: Mapping[str, Any], *, format_en: bool
) -> Result[dict, AppError]:
    r = ingest_one(source, payload)  # Quarantine -> StrictDTO(B) -> Domain(C)
    if isinstance(r, Ok):
        return Ok(_to_public_dict(r.value, format_en=format_en))
    return r  # Err 그대로 전달


def _iter_payloads(obj: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(obj, list):
        for item in obj:
            if not isinstance(item, Mapping):
                raise SystemExit("JSON array must contain objects")
            yield item
    elif isinstance(obj, Mapping):
        yield obj
    else:
        raise SystemExit("Input JSON must be an object or an array of objects")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="zaoc-news",
        description="ZAOC News pipeline (Boundary validation + Domain VO + Result flow)",
    )
    p.add_argument("--source", required=True, help="등록된 공급자 이름 (예: alpha, beta)")
    p.add_argument(
        "--input", default="-", help="JSON 파일 경로 (또는 '-' = stdin), obj 또는 [obj,...]"
    )
    p.add_argument("--no-format", action="store_true", help="언어별 title 포맷을 적용하지 않음")
    args = p.parse_args(argv)

    inp = _load_json(args.input)
    format_en = not args.no_format

    ok_count = 0
    err_count = 0

    outputs: list[dict[str, Any]] = []
    for payload in _iter_payloads(inp):
        res = _handle_payload(args.source, payload, format_en=format_en)
        if isinstance(res, Ok):
            ok_count += 1
            outputs.append(res.value)
        else:
            err_count += 1
            # 실패는 값: 표준에러로 구조화 출력
            print(
                json.dumps(
                    {"error": {"code": res.error.code, "message": res.error.message}},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )

    # 결과는 한 번에 JSON으로 표준출력
    if len(outputs) == 1:
        print(json.dumps(outputs[0], ensure_ascii=False))
    else:
        print(json.dumps(outputs, ensure_ascii=False, indent=2))

    # 일부 실패가 있었다면 비-0 종료코드(운영 신호)
    return 0 if err_count == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
