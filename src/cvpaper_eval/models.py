from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class PaperSource(str, Enum):
    PDF = "pdf"
    ARXIV = "arxiv"
    TEXT = "text"


class PaperMeta(BaseModel):
    title: str = ""
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    venue: str = ""
    arxiv_id: str = ""
    source: PaperSource = PaperSource.TEXT


class Section(BaseModel):
    id: str
    heading: str
    text: str


class TableRow(BaseModel):
    header: str
    cells: list[str] = Field(default_factory=list)


class Table(BaseModel):
    id: str
    rows: list[TableRow] = Field(default_factory=list)


class MetricDirection(str, Enum):
    HIGHER = "higher"
    LOWER = "lower"


class Metric(BaseModel):
    metric_id: str
    task: str = ""
    dataset: str = ""
    metric_name: str
    metric_variant: str = ""
    value: float
    direction: MetricDirection = MetricDirection.HIGHER
    method_key: str = ""
    source_location: str = ""
    normalization_note: str = ""


class ComparisonType(str, Enum):
    VS_BASELINE = "vs_baseline"
    VS_SOTA = "vs_sota"
    COVERAGE = "coverage"
    CONSISTENCY = "consistency"
    STATISTICS = "statistics"


class Comparison(BaseModel):
    comparison_id: str
    metric_ids: list[str] = Field(default_factory=list)
    type: ComparisonType
    conclusion: str
    evidence_locations: list[str] = Field(default_factory=list)


class DimensionStatus(str, Enum):
    EVALUATED = "evaluated"
    NOT_APPLICABLE = "not_applicable"
    REVIEW = "review"
    NOT_EVALUATED = "not_evaluated"


class DimensionScore(BaseModel):
    cluster_id: str
    dimension: str
    score: float | None = None
    confidence: Literal["high", "medium", "low"] = "medium"
    evidence: list[str] = Field(default_factory=list)
    status: DimensionStatus = DimensionStatus.EVALUATED


class Summary(BaseModel):
    weighted_score: float | None = None
    weights: dict[str, float] = Field(default_factory=dict)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    conclusion: str = ""
    caveats: list[str] = Field(default_factory=list)


class EvalReport(BaseModel):
    paper: PaperMeta
    sections: list[Section] = Field(default_factory=list)
    tables: list[Table] = Field(default_factory=list)
    metrics: list[Metric] = Field(default_factory=list)
    comparisons: list[Comparison] = Field(default_factory=list)
    dimension_scores: list[DimensionScore] = Field(default_factory=list)
    summary: Summary | None = None
