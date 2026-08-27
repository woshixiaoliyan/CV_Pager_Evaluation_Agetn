from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_settings
from .pipeline import run_evaluation
from .report.json_reporter import render_json
from .report.markdown_reporter import render_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="CV 论文宏观评价原型系统")
    parser.add_argument("--input", required=True, help="PDF 路径 / arXiv id / 论文文本文件路径")
    parser.add_argument("--kind", choices=["pdf", "arxiv", "text"], required=True)
    parser.add_argument("--out-dir", default="outputs", help="输出目录（默认 outputs）")
    args = parser.parse_args()

    settings = load_settings()
    if args.kind == "text":
        source = Path(args.input).read_text(encoding="utf-8")
    else:
        source = args.input
    report = run_evaluation(source, args.kind, settings)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.md").write_text(render_markdown(report), encoding="utf-8")
    (out_dir / "report.json").write_text(render_json(report), encoding="utf-8")
    print(f"report written to {out_dir / 'report.md'} and {out_dir / 'report.json'}")


if __name__ == "__main__":
    main()
