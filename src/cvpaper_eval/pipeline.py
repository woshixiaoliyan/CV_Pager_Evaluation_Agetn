from __future__ import annotations

from typing import Literal

from .comparison.comparator import build_comparisons
from .config import Settings
from .extraction.metric_extractor import extract_metrics
from .extraction.qualitative_extractor import extract_qualitative
from .extraction.validation import validate_metric
from .knowledge_base import load_knowledge_base
from .llm import LLMClient
from .models import (
    DimensionScore,
    DimensionStatus,
    EvalReport,
    PaperMeta,
    Section,
    Table,
)
from .parsing.arxiv_fetcher import fetch_arxiv
from .parsing.pdf_parser import parse_pdf
from .parsing.section_splitter import split_sections
from .scoring.dimension_scorer import build_summary, score_dimensions


def _parse_source(source: str, source_kind: str, settings: Settings) -> tuple[PaperMeta, list[Section], list[Table]]:
    if source_kind == "text":
        meta = PaperMeta(title="", source="text")
        sections = split_sections(source)
        return meta, sections, []
    if source_kind == "pdf":
        text, raw_tables = parse_pdf(source)
        sections = split_sections(text)
        return PaperMeta(title="", source="pdf"), sections, [Table(**t) for t in raw_tables]
    if source_kind == "arxiv":
        meta, pdf_path = fetch_arxiv(source.strip(), settings.tmp_dir)
        text, raw_tables = parse_pdf(str(pdf_path))
        sections = split_sections(text)
        return meta, sections, [Table(**t) for t in raw_tables]
    raise ValueError(f"unknown source_kind: {source_kind}")


def run_evaluation(source: str, source_kind: Literal["pdf", "arxiv", "text"], settings: Settings) -> EvalReport:
    chat = LLMClient(settings)
    kb = load_knowledge_base(settings.kb_path)
    meta, sections, tables = _parse_source(source, source_kind, settings)
    full_text = "\n".join(s.text for s in sections)
    raw_tables = [t.model_dump() for t in tables]
    metrics = extract_metrics(chat, full_text, raw_tables, kb)
    metrics = [m for m in metrics if not validate_metric(m)]
    comparisons = build_comparisons(metrics)
    qualitative = extract_qualitative(chat, full_text, kb)
    scores = score_dimensions(chat, comparisons, qualitative, kb)
    for i, item in enumerate(kb.get("not_evaluated_dimensions", [])):
        scores.append(DimensionScore(cluster_id=f"NE-{i:02d}", dimension=item["name"], status=DimensionStatus.NOT_EVALUATED))
    for i, item in enumerate(kb.get("review_dimensions", [])):
        scores.append(DimensionScore(cluster_id=f"RV-{i:02d}", dimension=item["name"], status=DimensionStatus.REVIEW))
    summary = build_summary(scores)
    return EvalReport(
        paper=meta,
        sections=sections,
        tables=tables,
        metrics=metrics,
        comparisons=comparisons,
        dimension_scores=scores,
        summary=summary,
    )
