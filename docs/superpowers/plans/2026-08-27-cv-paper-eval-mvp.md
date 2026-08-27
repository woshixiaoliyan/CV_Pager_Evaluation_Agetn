# CV 论文宏观评价原型系统（核心引擎）实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建可运行的核心引擎：输入一篇 CV 论文（PDF / arXiv 链接 / 文本），输出证据可追溯的 Markdown + JSON 评价报告（指标抽取→对比→14 维度评分→结论）。

**Architecture:** 确定性流水线：解析层（PDF/arXiv/文本→结构化文本+表格）→ 抽取层（LLM 结构化抽取实验指标与定性证据）→ 对比层（规则化对比分析）→ 评分层（LLM 按知识库 rubric 打分）→ 报告层（Markdown/JSON）。LLM 通过 `ChatJSON` 协议注入，单元测试全部使用 FakeChat，不依赖网络与 API Key。

**Tech Stack:** Python ≥3.11、pydantic ≥2.7、PyMuPDF ≥1.24、openai ≥1.30（DeepSeek 兼容端点）、pytest ≥8。

**Spec:** `docs/superpowers/specs/2026-08-27-cv-paper-eval-mvp-design.md`

## 范围说明

本计划（Plan A）只实现可运行软件核心（对应 spec M3~M5 的软件部分）。语料收集与知识库实证建设（Plan B）、人工标注与质量评估（Plan C）为后续独立计划；本计划用 fixtures 与种子知识库文件保证可独立测试。Agent 编排与 RAG 按 spec 属于 v2，本计划的 `run_evaluation()` 即未来 Agent 编排器的调用入口。

## 全局约束

- Python ≥3.11；所有公共函数必须有类型注解；
- 依赖版本：`pydantic>=2.7`、`PyMuPDF>=1.24`、`openai>=1.30`、`pytest>=8`；
- 所有 LLM 调用必须走 `ChatJSON` 协议（`chat_json(system: str, user: str) -> dict`），强制 `response_format={"type":"json_object"}`；
- 单元测试一律使用 `FakeChat`，禁止真实网络与真实 API Key；arXiv 测试 mock `urllib.request.urlopen`；
- 指标与报告必须保留 `metric_id` / `source_location`，证据链可追溯；
- 知识库 JSON（`knowledge_base/indicators_v1.json`）是维度定义与 rubric 的唯一事实来源；
- 数值校验规则集中在 `extraction/validation.py`，禁止在抽取器中散落；
- 目录结构：`src/cvpaper_eval/`（包）、`tests/`（测试）、`knowledge_base/`（KB 种子文件）。

---

### Task 1: 项目脚手架与数据模型

**Files:**
- Create: `pyproject.toml`
- Create: `src/cvpaper_eval/__init__.py`
- Create: `src/cvpaper_eval/models.py`
- Create: `tests/test_models.py`

**Interfaces:**
- Produces: `models.py` 中的 `PaperMeta`、`Section`、`TableRow`、`Table`、`Metric`、`MetricDirection`、`Comparison`、`ComparisonType`、`DimensionScore`、`DimensionStatus`、`Summary`、`EvalReport`（后续所有任务依赖这些类型）。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_models.py
from cvpaper_eval.models import Metric, MetricDirection, EvalReport, PaperMeta

def test_metric_defaults():
    m = Metric(metric_id="M-001", task="detection", dataset="COCO val2017",
               metric_name="mAP", value=0.482, method_key="Ours", source_location="TABLE 2")
    assert m.direction == MetricDirection.HIGHER

def test_metric_rejects_bad_direction():
    m = Metric(metric_id="M-001", task="detection", dataset="COCO val2017",
               metric_name="FID", value=20.0, direction="lower",
               method_key="Ours", source_location="TABLE 2")
    assert m.direction == MetricDirection.LOWER

def test_report_roundtrip():
    r = EvalReport(paper=PaperMeta(title="T"), sections=[], tables=[], metrics=[],
                   comparisons=[], dimension_scores=[], summary=None)
    assert r.paper.title == "T"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_models.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'cvpaper_eval'`）

- [ ] **Step 3: 创建脚手架与实现**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "cvpaper-eval"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pydantic>=2.7", "PyMuPDF>=1.24", "openai>=1.30"]

[project.optional-dependencies]
dev = ["pytest>=8"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

```python
# src/cvpaper_eval/__init__.py
"""CV 论文宏观评价原型系统。"""
__version__ = "0.1.0"
```

```python
# src/cvpaper_eval/models.py
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pip install -e ".[dev]"` 然后 `pytest tests/test_models.py -v`
Expected: PASS（3 个用例）

- [ ] **Step 5: 提交**

```bash
git add pyproject.toml src/cvpaper_eval/__init__.py src/cvpaper_eval/models.py tests/test_models.py
git commit -m "feat: scaffold project and pydantic data models"
```

---

### Task 2: 配置加载

**Files:**
- Create: `src/cvpaper_eval/config.py`
- Create: `.env.example`
- Create: `tests/test_config.py`

**Interfaces:**
- Produces: `Settings(api_key, base_url, model, temperature, kb_path, tmp_dir)` 与 `load_settings() -> Settings`。默认 `base_url="https://api.deepseek.com"`、`model="deepseek-chat"`、`temperature=0.1`、`kb_path=Path("knowledge_base/indicators_v1.json")`、`tmp_dir=Path(tempfile.gettempdir())/"cvpaper_eval"`。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_config.py
import os
from cvpaper_eval.config import Settings, load_settings

def test_defaults(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    s = load_settings()
    assert s.model == "deepseek-chat"
    assert s.base_url == "https://api.deepseek.com"
    assert s.temperature == 0.1

def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    try:
        load_settings()
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError")
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_config.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'cvpaper_eval.config'`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/config.py
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.1
    kb_path: Path = Path("knowledge_base/indicators_v1.json")
    tmp_dir: Path = Path(tempfile.gettempdir()) / "cvpaper_eval"


def load_settings() -> Settings:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set")
    return Settings(api_key=api_key)
```

```text
# .env.example
DEEPSEEK_API_KEY=sk-your-key
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_config.py -v`
Expected: PASS（2 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/config.py .env.example tests/test_config.py
git commit -m "feat: add settings loading with env key"
```

---

### Task 3: LLM 客户端（DeepSeek provider 抽象）

**Files:**
- Create: `src/cvpaper_eval/llm.py`
- Create: `tests/test_llm.py`

**Interfaces:**
- Consumes: `Settings`（Task 2）
- Produces: `LLMClient`（实现 `chat_json(system: str, user: str) -> dict`）；协议类型 `ChatJSON`（供 FakeChat 与所有抽取/评分模块使用）。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_llm.py
from cvpaper_eval.config import Settings
from cvpaper_eval.llm import LLMClient, ChatJSON

def test_chat_json_parses(monkeypatch):
    calls = {}

    class FakeCompletions:
        def create(self, **kwargs):
            calls["kwargs"] = kwargs
            class Msg:
                content = '{"ok": true}'
            class Choice:
                message = Msg()
            class Resp:
                choices = [Choice()]
            return Resp()

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    monkeypatch.setattr("cvpaper_eval.llm.OpenAI", lambda **kw: FakeChat())
    settings = Settings(api_key="sk-test")
    client = LLMClient(settings)
    assert client.chat_json("sys", "user") == {"ok": True}
    assert calls["kwargs"]["response_format"] == {"type": "json_object"}
    assert calls["kwargs"]["model"] == "deepseek-chat"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_llm.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'cvpaper_eval.llm'`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/llm.py
from __future__ import annotations

import json
from typing import Protocol

from openai import OpenAI

from .config import Settings


class ChatJSON(Protocol):
    def chat_json(self, system: str, user: str) -> dict: ...


class LLMClient:
    def __init__(self, settings: Settings):
        self._client = OpenAI(api_key=settings.api_key, base_url=settings.base_url)
        self._model = settings.model
        self._temperature = settings.temperature

    def chat_json(self, system: str, user: str) -> dict:
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        return json.loads(content)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_llm.py -v`
Expected: PASS（1 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/llm.py tests/test_llm.py
git commit -m "feat: add DeepSeek-compatible LLM client with ChatJSON protocol"
```

---

### Task 4: 知识库加载与种子文件

**Files:**
- Create: `knowledge_base/indicators_v1.json`
- Create: `src/cvpaper_eval/knowledge_base.py`
- Create: `tests/test_knowledge_base.py`

**Interfaces:**
- Produces: `load_knowledge_base(path: Path) -> dict`；种子文件含 `dimensions`（14 项，字段：cluster_id/name/question/criteria_high/criteria_mid/criteria_low/sources/status）、`metric_schema`、`mapping`、`not_evaluated_dimensions`、`review_dimensions`。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_knowledge_base.py
from pathlib import Path
from cvpaper_eval.knowledge_base import load_knowledge_base

def test_seed_kb_loads():
    kb = load_knowledge_base(Path("knowledge_base/indicators_v1.json"))
    dims = kb["dimensions"]
    assert len(dims) == 14
    assert {d["cluster_id"] for d in dims} >= {"CL-001", "CL-009", "CL-015"}
    for d in dims:
        assert d["name"] and d["question"] and d["criteria_high"] and d["criteria_low"]
    assert len(kb["mapping"]) >= 10
    assert kb["metric_schema"]["variant_notes"]["mAP@0.5:0.95"]
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_knowledge_base.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'cvpaper_eval.knowledge_base'`）

- [ ] **Step 3: 实现加载器与种子知识库**

```python
# src/cvpaper_eval/knowledge_base.py
from __future__ import annotations

import json
from pathlib import Path


def load_knowledge_base(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
```

```json
{
  "dimensions": [
    {"cluster_id": "CL-001", "name": "创新性/新颖性", "question": "论文提出的问题、方法或机制与已有工作的差异度如何？", "criteria_high": "提出新问题/新范式/新机制，与已有方法存在本质差异且论证充分", "criteria_mid": "存在明确的改进或组合创新，与已有方法差异可辨", "criteria_low": "主要是参数或工程性调整，缺乏新意", "sources": ["阶段一文献调研：CVPR/ICCV 评审指南与创新性评价研究"], "status": "evaluated"},
    {"cluster_id": "CL-003", "name": "学术贡献度", "question": "论文对领域的贡献是否清晰、可归因、有分量？", "criteria_high": "贡献明确且被实验/分析充分支撑，可独立评估", "criteria_mid": "贡献可辨但部分依赖主观断言", "criteria_low": "贡献模糊或与证据不匹配", "sources": ["阶段一文献调研：论文贡献评价框架"], "status": "evaluated"},
    {"cluster_id": "CL-004", "name": "技术稳健性", "question": "方法在多个基准上的性能提升是否一致、稳定？", "criteria_high": "多数据集/多设置一致提升，波动小", "criteria_mid": "多数基准提升但存在例外", "criteria_low": "提升微弱、不一致或只在单一有利设置出现", "sources": ["阶段一文献调研：技术稳健性维度"], "status": "evaluated"},
    {"cluster_id": "CL-005", "name": "声明-证据一致性", "question": "正文声明（含 SOTA 声明）是否被表格/实验数据支持？", "criteria_high": "所有声明与数据自洽，无夸大", "criteria_mid": "个别表述略有出入但不影响结论", "criteria_low": "声明与数据明显矛盾", "sources": ["阶段一文献调研：声明-证据一致性簇"], "status": "evaluated"},
    {"cluster_id": "CL-006", "name": "实验有效性与偏置控制", "question": "实验设计是否控制了变量、进行了消融、排除偏置？", "criteria_high": "消融完整、控制变量清晰、公平对比", "criteria_mid": "部分消融或对比公平性存疑", "criteria_low": "无消融、对比不公平或设置不透明", "sources": ["阶段一文献调研：实验有效性簇"], "status": "evaluated"},
    {"cluster_id": "CL-007", "name": "泛化性与部署稳健性", "question": "方法在多大范围的数据/任务/场景下验证？", "criteria_high": "跨多数据集/多任务/多领域验证", "criteria_mid": "覆盖 2-3 个数据集或同域迁移", "criteria_low": "单一数据集/单一场景", "sources": ["阶段一文献调研：泛化性簇"], "status": "evaluated"},
    {"cluster_id": "CL-008", "name": "统计严谨性与披露", "question": "是否报告方差、显著性检验、重复实验等统计信息？", "criteria_high": "报告多 seed 均值±方差/显著性检验", "criteria_mid": "部分披露但不够系统", "criteria_low": "仅报告单次数值", "sources": ["阶段一文献调研：统计严谨性簇"], "status": "evaluated"},
    {"cluster_id": "CL-009", "name": "可复现性", "question": "代码、超参、数据版本、训练设置是否足以复现？", "criteria_high": "代码/超参/数据版本齐全且可运行", "criteria_mid": "部分资源或关键设置缺失", "criteria_low": "无任何复现资源", "sources": ["阶段一文献调研：可复现性簇（11 条证据）"], "status": "evaluated"},
    {"cluster_id": "CL-010", "name": "开放性与资源可得性", "question": "数据、模型、代码是否开放可获取？", "criteria_high": "主要资源全部开放", "criteria_mid": "部分资源开放", "criteria_low": "全部私有", "sources": ["阶段一文献调研：开放性与资源可得性簇"], "status": "evaluated"},
    {"cluster_id": "CL-011", "name": "数据集贡献", "question": "论文是否贡献了新的数据集/基准？质量如何？", "criteria_high": "新数据集规模大、标注规范、可获取", "criteria_mid": "新数据集规模有限或质量存疑", "criteria_low": "无数据集贡献", "sources": ["阶段一文献调研：数据集贡献簇"], "status": "evaluated"},
    {"cluster_id": "CL-012", "name": "表述清晰度", "question": "论文结构、写作与图表是否清晰易懂？", "criteria_high": "结构完整、术语一致、图表有效", "criteria_mid": "基本清晰但有局部含糊", "criteria_low": "结构混乱或关键部分难以理解", "sources": ["阶段一文献调研：表述清晰度簇"], "status": "evaluated"},
    {"cluster_id": "CL-013", "name": "相关工作与引用充分性", "question": "相关工作梳理与引用是否充分、准确？", "criteria_high": "覆盖关键文献且定位准确", "criteria_mid": "覆盖基本充分但有遗漏", "criteria_low": "相关工作缺失或引用不当", "sources": ["阶段一文献调研：相关工作簇"], "status": "evaluated"},
    {"cluster_id": "CL-014", "name": "伦理合规", "question": "是否声明潜在伦理/社会风险并给出合规处理？", "criteria_high": "明确伦理声明与风险缓解", "criteria_mid": "提及但较简略", "criteria_low": "无任何伦理考虑", "sources": ["阶段一文献调研：伦理合规簇"], "status": "evaluated"},
    {"cluster_id": "CL-015", "name": "局限性与诚实评估", "question": "是否如实披露方法局限与失败案例？", "criteria_high": "局限清晰、诚实、有边界说明", "criteria_mid": "有局限说明但不够具体", "criteria_low": "无局限性披露或回避失败", "sources": ["阶段一文献调研：局限性簇"], "status": "evaluated"}
  ],
  "metric_schema": {
    "direction_defaults": {"fid": "lower", "kid": "lower", "sfid": "lower", "fvd": "lower", "epe": "lower", "rmse": "lower", "absrel": "lower", "cer": "lower", "ece": "lower", "mce": "lower", "lpips": "lower", "niqe": "lower", "piqe": "lower", "brisque": "lower", "musiq": "lower"},
    "range_hints": {"accuracy": [0, 1], "precision": [0, 1], "recall": [0, 1], "f1": [0, 1], "map": [0, 1], "miou": [0, 1], "iou": [0, 1], "ssim": [0, 1], "psnr": [0, 100], "fid": [0, 1000], "fps": [0, 100000]},
    "variant_notes": {"mAP@0.5": "PASCAL 风格，不可与 mAP@0.5:0.95 混比", "mAP@0.5:0.95": "COCO 风格"}
  },
  "mapping": [
    {"evidence": "relative_improvement_vs_baseline", "dimensions": ["CL-003", "CL-004"]},
    {"evidence": "dataset_coverage", "dimensions": ["CL-007"]},
    {"evidence": "ablation_completeness", "dimensions": ["CL-006", "CL-003"]},
    {"evidence": "statistical_disclosure", "dimensions": ["CL-008"]},
    {"evidence": "table_text_consistency", "dimensions": ["CL-005"]},
    {"evidence": "openness_artifacts", "dimensions": ["CL-009", "CL-010"]},
    {"evidence": "novelty_claims", "dimensions": ["CL-001"]},
    {"evidence": "related_work", "dimensions": ["CL-013"]},
    {"evidence": "ethics_statement", "dimensions": ["CL-014"]},
    {"evidence": "limitations", "dimensions": ["CL-015"]}
  ],
  "not_evaluated_dimensions": [
    {"name": "学科归一化引文影响力", "reason": "需外部引文数据（未联网）"},
    {"name": "引文有效性与边界", "reason": "需外部引文数据（未联网）"},
    {"name": "社会/综合影响力", "reason": "需外部数据且操作化困难"},
    {"name": "文章级影响力指标", "reason": "需外部数据（未联网）"},
    {"name": "Altmetrics", "reason": "需外部数据且可操纵，仅作辅助"},
    {"name": "期刊层指标与边界", "reason": "期刊层信息，非论文自身属性"},
    {"name": "作者层指标", "reason": "作者层信息，非论文自身属性"}
  ],
  "review_dimensions": [
    {"name": "组合新颖性", "reason": "与创新性语义相近但不完全等价，待人工审核"},
    {"name": "作者声望偏差", "reason": "属流程偏差控制项，待人工审核"},
    {"name": "新颖性-影响-性能平衡", "reason": "属权重/决策规则，待人工审核"}
  ]
}
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_knowledge_base.py -v`
Expected: PASS（1 个用例）

- [ ] **Step 5: 提交**

```bash
git add knowledge_base/indicators_v1.json src/cvpaper_eval/knowledge_base.py tests/test_knowledge_base.py
git commit -m "feat: add seed indicator knowledge base v1 with loader"
```

---

### Task 5: PDF 解析与表格扁平化

**Files:**
- Create: `src/cvpaper_eval/parsing/__init__.py`
- Create: `src/cvpaper_eval/parsing/pdf_parser.py`
- Create: `tests/test_pdf_parser.py`

**Interfaces:**
- Produces: `parse_pdf(path: str) -> tuple[str, list[dict]]`（返回全文文本与表格 dict 列表，表格结构 `{"id": str, "rows": [{"header": str, "cells": [str]}]}`）；`flatten_table_rows(rows: list[list[str]]) -> list[dict]`（将 pymupdf `extract()` 的二维数组转成行记录，首行为表头）。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_pdf_parser.py
import fitz
from cvpaper_eval.parsing.pdf_parser import parse_pdf, flatten_table_rows

def test_parse_pdf_extracts_text(tmp_path):
    pdf = tmp_path / "fixture.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Abstract\nWe propose OursNet with mAP 0.482.")
    doc.save(str(pdf))
    doc.close()
    text, tables = parse_pdf(str(pdf))
    assert "mAP 0.482" in text
    assert tables == []

def test_flatten_table_rows():
    rows = [["Method", "mAP", "FPS"], ["Ours", "0.482", "35"], ["Base", "0.421", "40"]]
    out = flatten_table_rows(rows)
    assert out[0]["header"] == "Method mAP FPS"
    assert out[1]["cells"] == ["Ours", "0.482", "35"]
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_pdf_parser.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'cvpaper_eval.parsing.pdf_parser'`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/parsing/__init__.py
"""输入解析层。"""
```

```python
# src/cvpaper_eval/parsing/pdf_parser.py
from __future__ import annotations

import fitz


def flatten_table_rows(rows: list[list[str]]) -> list[dict]:
    """把 pymupdf extract() 的二维数组转成 {header, cells} 行记录，首行视为表头。"""
    if not rows:
        return []
    header = " ".join(str(c).strip() for c in rows[0])
    out: list[dict] = []
    for row in rows[1:]:
        out.append({"header": header, "cells": [str(c).strip() for c in row]})
    return out


def parse_pdf(path: str) -> tuple[str, list[dict]]:
    doc = fitz.open(path)
    text_parts: list[str] = []
    tables: list[dict] = []
    table_index = 0
    for page in doc:
        text_parts.append(page.get_text("text"))
        for raw in page.find_tables().tables:
            table_index += 1
            rows = flatten_table_rows(raw.extract())
            if rows:
                tables.append({"id": f"TABLE {table_index}", "rows": rows})
    doc.close()
    return "\n".join(text_parts), tables
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_pdf_parser.py -v`
Expected: PASS（2 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/parsing/__init__.py src/cvpaper_eval/parsing/pdf_parser.py tests/test_pdf_parser.py
git commit -m "feat: add PDF text/table parsing with flatten helper"
```

---

### Task 6: 章节切分

**Files:**
- Create: `src/cvpaper_eval/parsing/section_splitter.py`
- Create: `tests/test_section_splitter.py`

**Interfaces:**
- Produces: `split_sections(text: str) -> list[Section]`；章节标题识别列表固定为 `["abstract","introduction","related work","method","methodology","experiments","experimental","results","conclusion","appendix","references"]`，匹配行首（可带数字编号），命中后进入新节，`id` 为 `SEC-001` 起递增。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_section_splitter.py
from cvpaper_eval.parsing.section_splitter import split_sections

def test_split_sections():
    text = "Abstract\nWe propose X.\n3. Experiments\nWe test on COCO.\nConclusion\nGood."
    sections = split_sections(text)
    assert sections[0].heading.lower() == "abstract"
    assert sections[0].text == "We propose X."
    assert sections[1].heading.lower() == "experiments"
    assert sections[1].text == "We test on COCO."
    assert sections[2].heading.lower() == "conclusion"
    assert sections[0].id == "SEC-001"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_section_splitter.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'cvpaper_eval.parsing.section_splitter'`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/parsing/section_splitter.py
from __future__ import annotations

import re

from ..models import Section

HEADINGS = [
    "abstract", "introduction", "related work", "method", "methodology",
    "experiments", "experimental", "results", "conclusion", "appendix", "references",
]

_PATTERN = re.compile(r"^\s*(?:\d+(?:\.\d+)*[\.\)\s]*)?(" + "|".join(HEADINGS) + r")\s*$", re.IGNORECASE)


def split_sections(text: str) -> list[Section]:
    lines = text.splitlines()
    sections: list[Section] = []
    current: list[str] = []
    current_heading = "preamble"
    index = 0
    for line in lines:
        m = _PATTERN.match(line)
        if m:
            if current or sections:
                sections.append(Section(id=f"SEC-{index:03d}", heading=current_heading, text="\n".join(current).strip()))
                index += 1
            current_heading = m.group(1)
            current = []
        else:
            current.append(line)
    sections.append(Section(id=f"SEC-{index:03d}", heading=current_heading, text="\n".join(current).strip()))
    return sections
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_section_splitter.py -v`
Expected: PASS（1 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/parsing/section_splitter.py tests/test_section_splitter.py
git commit -m "feat: add section splitter"
```

---

### Task 7: arXiv 获取（元数据 + PDF 下载）

**Files:**
- Create: `src/cvpaper_eval/parsing/arxiv_fetcher.py`
- Create: `tests/test_arxiv_fetcher.py`

**Interfaces:**
- Produces: `fetch_arxiv(arxiv_id: str, dest_dir: Path) -> tuple[PaperMeta, Path]`；元数据解析 arXiv Atom XML（title/authors/year/arxiv_id），PDF 下载到 `dest_dir/<id>.pdf`。测试 mock `urllib.request.urlopen`，禁止真实网络。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_arxiv_fetcher.py
import io
from pathlib import Path
from urllib.error import URLError
import urllib.request
from cvpaper_eval.parsing.arxiv_fetcher import fetch_arxiv

ATOM = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry><title>OursNet: A Test</title>
  <author><name>Alice Zhang</name></author>
  <published>2025-01-01T00:00:00Z</published>
  <id>http://arxiv.org/abs/2501.00001v1</id></entry>
</feed>"""

def test_fetch_arxiv(monkeypatch, tmp_path):
    class FakeResp:
        def __init__(self, data):
            self._data = data
        def read(self):
            return self._data
    def fake_urlopen(url, **kw):
        if "export.arxiv.org" in url:
            return FakeResp(ATOM)
        if "arxiv.org/pdf" in url:
            return FakeResp(b"%PDF-1.4 fake")
        raise URLError(f"unexpected {url}")
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    meta, pdf = fetch_arxiv("2501.00001", tmp_path)
    assert meta.title == "OursNet: A Test"
    assert meta.arxiv_id == "2501.00001"
    assert pdf.exists()
    assert pdf.read_bytes() == b"%PDF-1.4 fake"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_arxiv_fetcher.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'cvpaper_eval.parsing.arxiv_fetcher'`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/parsing/arxiv_fetcher.py
from __future__ import annotations

import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from ..models import PaperMeta, PaperSource

_NS = {"a": "http://www.w3.org/2005/Atom"}


def _parse_meta(atom_xml: bytes, arxiv_id: str) -> PaperMeta:
    root = ET.fromstring(atom_xml)
    entry = root.find("a:entry", _NS)
    if entry is None:
        raise ValueError("arxiv atom feed has no entry")
    title = entry.findtext("a:title", default="", namespaces=_NS).strip()
    authors = [a.findtext("a:name", default="", namespaces=_NS).strip() for a in entry.findall("a:author", _NS)]
    published = entry.findtext("a:published", default="", namespaces=_NS)
    year = int(re.match(r"(\d{4})", published).group(1)) if re.match(r"(\d{4})", published) else None
    return PaperMeta(title=title, authors=authors, year=year, arxiv_id=arxiv_id, source=PaperSource.ARXIV)


def fetch_arxiv(arxiv_id: str, dest_dir: Path) -> tuple[PaperMeta, Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    with urllib.request.urlopen(api_url) as resp:
        meta = _parse_meta(resp.read(), arxiv_id)
    pdf_path = dest_dir / f"{arxiv_id}.pdf"
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    with urllib.request.urlopen(pdf_url) as resp:
        pdf_path.write_bytes(resp.read())
    return meta, pdf_path
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_arxiv_fetcher.py -v`
Expected: PASS（1 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/parsing/arxiv_fetcher.py tests/test_arxiv_fetcher.py
git commit -m "feat: add arXiv metadata fetch and pdf download"
```

---

### Task 8: 实验指标抽取与数值校验

**Files:**
- Create: `src/cvpaper_eval/extraction/__init__.py`
- Create: `src/cvpaper_eval/extraction/validation.py`
- Create: `src/cvpaper_eval/extraction/metric_extractor.py`
- Create: `tests/test_validation.py`
- Create: `tests/test_metric_extractor.py`

**Interfaces:**
- Consumes: `Metric`（Task 1）、`ChatJSON`（Task 3）、`load_knowledge_base`（Task 4）
- Produces: `validate_metric(m: Metric) -> list[str]`；`extract_metrics(chat: ChatJSON, text: str, tables: list[dict], kb: dict) -> list[Metric]`（LLM 返回 `{"metrics": [...]}`，逐条构造 `Metric`，`metric_id` 为 `M-{i:03d}`；方向未指定时按 `kb["metric_schema"]["direction_defaults"]` 推断）。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_validation.py
from cvpaper_eval.models import Metric
from cvpaper_eval.extraction.validation import validate_metric

def test_out_of_range():
    m = Metric(metric_id="M-1", task="detection", dataset="COCO", metric_name="accuracy", value=1.7, method_key="Ours", source_location="T1")
    assert any("out of range" in e for e in validate_metric(m))

def test_missing_dataset_and_location():
    m = Metric(metric_id="M-2", task="detection", dataset="", metric_name="mAP", value=0.5, method_key="Ours", source_location="")
    errors = validate_metric(m)
    assert len(errors) == 2
```

```python
# tests/test_metric_extractor.py
from cvpaper_eval.extraction.metric_extractor import extract_metrics

class FakeChat:
    def chat_json(self, system, user):
        return {"metrics": [
            {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.482, "method_key": "Ours", "source_location": "TABLE 2", "normalization_note": ""},
            {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.421, "method_key": "Faster R-CNN", "source_location": "TABLE 2", "normalization_note": ""}
        ]}

def test_extract_metrics():
    kb = {"metric_schema": {"direction_defaults": {}}}
    metrics = extract_metrics(FakeChat(), "text", [], kb)
    assert len(metrics) == 2
    assert metrics[0].metric_id == "M-000"
    assert metrics[0].value == 0.482
    assert metrics[1].method_key == "Faster R-CNN"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_validation.py tests/test_metric_extractor.py -v`
Expected: FAIL（`ModuleNotFoundError`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/extraction/__init__.py
"""LLM 抽取层。"""
```

```python
# src/cvpaper_eval/extraction/validation.py
from __future__ import annotations

from ..models import Metric

RANGES: dict[str, tuple[float, float]] = {
    "accuracy": (0.0, 1.0),
    "precision": (0.0, 1.0),
    "recall": (0.0, 1.0),
    "f1": (0.0, 1.0),
    "map": (0.0, 1.0),
    "miou": (0.0, 1.0),
    "iou": (0.0, 1.0),
    "ssim": (0.0, 1.0),
    "psnr": (0.0, 100.0),
    "fid": (0.0, 1000.0),
    "fps": (0.0, 100000.0),
}


def validate_metric(metric: Metric) -> list[str]:
    errors: list[str] = []
    key = metric.metric_name.lower()
    if key in RANGES:
        lo, hi = RANGES[key]
        if not (lo <= metric.value <= hi):
            errors.append(f"{metric.metric_name} value {metric.value} out of range [{lo}, {hi}]")
    if not metric.dataset:
        errors.append("dataset is required for comparison")
    if not metric.source_location:
        errors.append("source_location is required for traceability")
    return errors
```

```python
# src/cvpaper_eval/extraction/metric_extractor.py
from __future__ import annotations

import json

from ..llm import ChatJSON
from ..models import Metric, MetricDirection

SYSTEM_PROMPT = (
    "You extract quantitative evaluation metrics from computer vision papers. "
    'Return a JSON object with key "metrics": a list of objects with fields: '
    "task, dataset, metric_name, metric_variant, value (float), direction "
    '("higher" or "lower"), method_key, source_location, normalization_note. '
    "Include every metric found, including baselines and SOTA claims."
)


def _infer_direction(raw: dict, kb: dict) -> MetricDirection:
    explicit = raw.get("direction")
    if explicit in ("higher", "lower"):
        return MetricDirection(explicit)
    defaults = kb.get("metric_schema", {}).get("direction_defaults", {})
    return MetricDirection(defaults.get(raw.get("metric_name", "").lower(), "higher"))


def extract_metrics(chat: ChatJSON, text: str, tables: list[dict], kb: dict) -> list[Metric]:
    user = json.dumps(
        {"text": text[:12000], "tables": tables[:50], "schema": kb.get("metric_schema", {})},
        ensure_ascii=False,
    )
    payload = chat.chat_json(SYSTEM_PROMPT, user)
    metrics: list[Metric] = []
    for i, raw in enumerate(payload.get("metrics", [])):
        try:
            metrics.append(
                Metric(
                    metric_id=f"M-{i:03d}",
                    task=raw.get("task", ""),
                    dataset=raw.get("dataset", ""),
                    metric_name=raw.get("metric_name", ""),
                    metric_variant=raw.get("metric_variant", ""),
                    value=float(raw["value"]),
                    direction=_infer_direction(raw, kb),
                    method_key=raw.get("method_key", ""),
                    source_location=raw.get("source_location", ""),
                    normalization_note=raw.get("normalization_note", ""),
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
    return metrics
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_validation.py tests/test_metric_extractor.py -v`
Expected: PASS（4 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/extraction/__init__.py src/cvpaper_eval/extraction/validation.py src/cvpaper_eval/extraction/metric_extractor.py tests/test_validation.py tests/test_metric_extractor.py
git commit -m "feat: add metric extraction with validation"
```

---

### Task 9: 定性证据抽取（通道一）

**Files:**
- Create: `src/cvpaper_eval/extraction/qualitative_extractor.py`
- Create: `tests/test_qualitative_extractor.py`

**Interfaces:**
- Consumes: `ChatJSON`
- Produces: `extract_qualitative(chat: ChatJSON, text: str, kb: dict) -> dict`；返回键固定为 `novelty_claims`、`limitations`、`openness`、`ethics`、`related_work`、`clarity`，值为证据句列表（每句带 `{"text": str, "location": str}`）。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_qualitative_extractor.py
from cvpaper_eval.extraction.qualitative_extractor import extract_qualitative, KEYS

class FakeChat:
    def chat_json(self, system, user):
        return {"novelty_claims": [{"text": "We propose a new paradigm.", "location": "SEC-001"}],
                "limitations": [], "openness": [], "ethics": [], "related_work": [], "clarity": []}

def test_extract_qualitative_keys():
    out = extract_qualitative(FakeChat(), "text", {})
    assert set(out) == set(KEYS)
    assert out["novelty_claims"][0]["location"] == "SEC-001"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_qualitative_extractor.py -v`
Expected: FAIL（`ModuleNotFoundError`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/extraction/qualitative_extractor.py
from __future__ import annotations

import json

from ..llm import ChatJSON

KEYS = ["novelty_claims", "limitations", "openness", "ethics", "related_work", "clarity"]

SYSTEM_PROMPT = (
    "Extract qualitative evaluation evidence from a computer vision paper. "
    'Return a JSON object with keys: novelty_claims, limitations, openness, ethics, related_work, clarity. '
    'Each value is a list of {"text": str, "location": str}. '
    "Only include sentences actually present in the paper text."
)


def extract_qualitative(chat: ChatJSON, text: str, kb: dict) -> dict:
    user = json.dumps({"text": text[:16000], "dimensions": kb.get("dimensions", [])}, ensure_ascii=False)
    payload = chat.chat_json(SYSTEM_PROMPT, user)
    out = {}
    for key in KEYS:
        items = payload.get(key, [])
        out[key] = [{"text": str(i.get("text", "")), "location": str(i.get("location", ""))} for i in items if isinstance(i, dict)]
    return out
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_qualitative_extractor.py -v`
Expected: PASS（1 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/extraction/qualitative_extractor.py tests/test_qualitative_extractor.py
git commit -m "feat: add qualitative evidence extraction"
```

---

### Task 10: 指标对比分析

**Files:**
- Create: `src/cvpaper_eval/comparison/__init__.py`
- Create: `src/cvpaper_eval/comparison/comparator.py`
- Create: `tests/test_comparator.py`

**Interfaces:**
- Consumes: `Metric`、`Comparison`、`ComparisonType`
- Produces: `build_comparisons(metrics: list[Metric]) -> list[Comparison]`；按 `(task, dataset, metric_name, metric_variant)` 分组，`method_key` 属于 `{"ours","our","this paper","proposed","ours"}` 的为本方法，对组内其他方法生成 `VS_BASELINE`；论文级追加 `COVERAGE`（数据集覆盖）、`CONSISTENCY`（多基准方向一致性）、`STATISTICS`（是否披露均值±方差/显著性词，来自 normalization_note/source_location 文本信号，v1 简化：凡 metric_variant 含 "mean±" 或 "std" 视为披露）。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_comparator.py
from cvpaper_eval.models import Metric, ComparisonType
from cvpaper_eval.comparison.comparator import build_comparisons

def _m(mid, name, value, method, variant="", dataset="COCO val2017"):
    return Metric(metric_id=mid, task="detection", dataset=dataset, metric_name=name,
                  metric_variant=variant, value=value, method_key=method, source_location="TABLE 2")

def test_vs_baseline_delta():
    ms = [_m("M-0", "mAP", 0.482, "Ours"), _m("M-1", "mAP", 0.421, "Faster R-CNN")]
    cmps = build_comparisons(ms)
    vs = [c for c in cmps if c.type == ComparisonType.VS_BASELINE]
    assert len(vs) == 1
    assert "+0.06" in vs[0].conclusion

def test_coverage_and_consistency():
    ms = [_m("M-0", "mAP", 0.5, "Ours", dataset="COCO"), _m("M-1", "mAP", 0.6, "Ours", dataset="VOC")]
    cmps = build_comparisons(ms)
    assert any(c.type == ComparisonType.COVERAGE and "2 datasets" in c.conclusion for c in cmps)
    assert any(c.type == ComparisonType.CONSISTENCY for c in cmps)
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_comparator.py -v`
Expected: FAIL（`ModuleNotFoundError`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/comparison/__init__.py
"""指标对比分析层。"""
```

```python
# src/cvpaper_eval/comparison/comparator.py
from __future__ import annotations

from collections import defaultdict

from ..models import Comparison, ComparisonType, Metric, MetricDirection

OURS_KEYS = {"ours", "our", "this paper", "proposed", "ours"}


def _group_key(m: Metric) -> tuple[str, str, str, str]:
    return (m.task, m.dataset, m.metric_name, m.metric_variant)


def _is_ours(m: Metric) -> bool:
    return m.method_key.strip().lower() in OURS_KEYS


def build_comparisons(metrics: list[Metric]) -> list[Comparison]:
    comparisons: list[Comparison] = []
    groups: dict[tuple, list[Metric]] = defaultdict(list)
    for m in metrics:
        groups[_group_key(m)].append(m)

    for key in sorted(groups):
        group = groups[key]
        ours = [m for m in group if _is_ours(m)]
        others = [m for m in group if not _is_ours(m)]
        for m in ours:
            for other in others:
                delta = m.value - other.value if m.direction == MetricDirection.HIGHER else other.value - m.value
                comparisons.append(
                    Comparison(
                        comparison_id=f"CMP-{len(comparisons) + 1:03d}",
                        metric_ids=[m.metric_id, other.metric_id],
                        type=ComparisonType.VS_BASELINE,
                        conclusion=f"{m.metric_name} {delta:+.2f} vs {other.method_key} ({m.dataset})",
                        evidence_locations=[m.source_location, other.source_location],
                    )
                )

    datasets = sorted({m.dataset for m in metrics if m.dataset})
    if datasets:
        comparisons.append(
            Comparison(
                comparison_id=f"CMP-{len(comparisons) + 1:03d}",
                type=ComparisonType.COVERAGE,
                conclusion=f"covers {len(datasets)} datasets: {', '.join(datasets)}",
            )
        )

    if len(datasets) >= 2:
        comparisons.append(
            Comparison(
                comparison_id=f"CMP-{len(comparisons) + 1:03d}",
                type=ComparisonType.CONSISTENCY,
                conclusion=f"reported across {len(datasets)} datasets",
            )
        )

    disclosed = any("std" in (m.normalization_note + " " + m.metric_variant).lower() for m in metrics)
    comparisons.append(
        Comparison(
            comparison_id=f"CMP-{len(comparisons) + 1:03d}",
            type=ComparisonType.STATISTICS,
            conclusion="reports variance/std disclosure" if disclosed else "no variance/std disclosure detected",
            metric_ids=[m.metric_id for m in metrics],
        )
    )
    return comparisons
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_comparator.py -v`
Expected: PASS（2 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/comparison/__init__.py src/cvpaper_eval/comparison/comparator.py tests/test_comparator.py
git commit -m "feat: add rule-based metric comparator"
```

---

### Task 11: 维度评分与综合结论

**Files:**
- Create: `src/cvpaper_eval/scoring/__init__.py`
- Create: `src/cvpaper_eval/scoring/dimension_scorer.py`
- Create: `tests/test_dimension_scorer.py`

**Interfaces:**
- Consumes: `Comparison`、`DimensionScore`、`Summary`、`ChatJSON`、KB
- Produces: `score_dimensions(chat, comparisons, qualitative, kb) -> list[DimensionScore]`（LLM 返回 `{"dimension_scores":[{"cluster_id","score","confidence","evidence"}]}`，evidence 为字符串列表）；`build_summary(scores: list[DimensionScore], weights: dict[str, float] | None = None) -> Summary`（等权均值或按 cluster_id 权重加权，strengths/weaknesses 取 top/bottom 维度）。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_dimension_scorer.py
from cvpaper_eval.models import Comparison, DimensionScore, Summary
from cvpaper_eval.scoring.dimension_scorer import score_dimensions, build_summary

class FakeChat:
    def chat_json(self, system, user):
        return {"dimension_scores": [
            {"cluster_id": "CL-001", "score": 4, "confidence": "high", "evidence": ["novel mechanism"]},
            {"cluster_id": "CL-004", "score": 3, "confidence": "medium", "evidence": ["+0.06 vs baseline"]}
        ]}

def test_score_dimensions():
    kb = {"dimensions": [
        {"cluster_id": "CL-001", "name": "创新性/新颖性", "status": "evaluated"},
        {"cluster_id": "CL-004", "name": "技术稳健性", "status": "evaluated"}
    ]}
    scores = score_dimensions(FakeChat(), [], {"novelty_claims": []}, kb)
    assert {s.cluster_id for s in scores} == {"CL-001", "CL-004"}
    assert scores[0].score == 4

def test_build_summary_equal_weights():
    scores = [DimensionScore(cluster_id="CL-001", dimension="A", score=4),
              DimensionScore(cluster_id="CL-004", dimension="B", score=2)]
    summary = build_summary(scores)
    assert summary.weighted_score == 3.0
    assert summary.strengths[0] == "A"
    assert summary.weaknesses[0] == "B"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_dimension_scorer.py -v`
Expected: FAIL（`ModuleNotFoundError`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/scoring/__init__.py
"""维度评分与结论层。"""
```

```python
# src/cvpaper_eval/scoring/dimension_scorer.py
from __future__ import annotations

import json

from ..llm import ChatJSON
from ..models import Comparison, DimensionScore, Summary

SYSTEM_PROMPT = (
    "You are an expert reviewer of computer vision papers. Score each dimension 0-5 "
    "using the provided rubric and the evidence. Return JSON: "
    '{"dimension_scores": [{"cluster_id", "score", "confidence", "evidence": [str]}]}. '
    "Never invent evidence; only reuse provided comparisons and qualitative evidence."
)


def score_dimensions(chat: ChatJSON, comparisons: list[Comparison], qualitative: dict, kb: dict) -> list[DimensionScore]:
    dims = [d for d in kb.get("dimensions", []) if d.get("status") == "evaluated"]
    user = json.dumps(
        {
            "comparisons": [c.model_dump() for c in comparisons],
            "qualitative": qualitative,
            "dimensions": dims,
        },
        ensure_ascii=False,
    )
    payload = chat.chat_json(SYSTEM_PROMPT, user)
    raw_scores = payload.get("dimension_scores", [])
    by_id = {d["cluster_id"]: d for d in dims}
    scores: list[DimensionScore] = []
    for raw in raw_scores:
        cid = raw.get("cluster_id")
        if cid not in by_id:
            continue
        scores.append(
            DimensionScore(
                cluster_id=cid,
                dimension=by_id[cid]["name"],
                score=float(raw.get("score", 0)),
                confidence=raw.get("confidence", "medium"),
                evidence=[str(e) for e in raw.get("evidence", [])],
            )
        )
    return scores


def build_summary(scores: list[DimensionScore], weights: dict[str, float] | None = None) -> Summary:
    evaluated = [s for s in scores if s.score is not None]
    if not evaluated:
        return Summary(conclusion="no evaluable dimensions")
    if weights:
        total = sum(weights.get(s.cluster_id, 1.0) for s in evaluated)
        weighted = sum(s.score * weights.get(s.cluster_id, 1.0) for s in evaluated) / total
    else:
        weighted = sum(s.score for s in evaluated) / len(evaluated)
        weights = {s.cluster_id: 1.0 for s in evaluated}
    ranked = sorted(evaluated, key=lambda s: s.score, reverse=True)
    strengths = [f"{s.dimension} ({s.score})" for s in ranked[:3] if s.score >= 3]
    weaknesses = [f"{s.dimension} ({s.score})" for s in ranked[-3:] if s.score < 3]
    conclusion = (
        f"整体评分 {weighted:.2f}/5；主要优势：{('、'.join(strengths)) if strengths else '无明显优势'}；"
        f"主要不足：{('、'.join(weaknesses)) if weaknesses else '无明显不足'}。"
    )
    return Summary(weighted_score=round(weighted, 2), weights=weights, strengths=strengths, weaknesses=weaknesses, conclusion=conclusion)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_dimension_scorer.py -v`
Expected: PASS（2 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/scoring/__init__.py src/cvpaper_eval/scoring/dimension_scorer.py tests/test_dimension_scorer.py
git commit -m "feat: add dimension scoring and summary"
```

---

### Task 12: 报告生成（Markdown + JSON）

**Files:**
- Create: `src/cvpaper_eval/report/__init__.py`
- Create: `src/cvpaper_eval/report/markdown_reporter.py`
- Create: `src/cvpaper_eval/report/json_reporter.py`
- Create: `tests/test_reporters.py`

**Interfaces:**
- Consumes: `EvalReport`
- Produces: `render_markdown(report: EvalReport) -> str`（含元信息、指标表、对比表、维度得分表、优势/不足、综合结论、未评估与待审核清单）；`render_json(report: EvalReport) -> str`（`report.model_dump_json(indent=2)`）。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_reporters.py
import json
from cvpaper_eval.models import EvalReport, PaperMeta, Metric, DimensionScore, Summary, DimensionStatus
from cvpaper_eval.report.markdown_reporter import render_markdown
from cvpaper_eval.report.json_reporter import render_json

def _report():
    return EvalReport(
        paper=PaperMeta(title="T", source="text"),
        metrics=[Metric(metric_id="M-0", metric_name="mAP", value=0.48, method_key="Ours", source_location="T1")],
        dimension_scores=[DimensionScore(cluster_id="CL-001", dimension="创新性", score=4, status=DimensionStatus.EVALUATED),
                          DimensionScore(cluster_id="CL-016", dimension="引文影响力", status=DimensionStatus.NOT_EVALUATED)],
        summary=Summary(weighted_score=4.0, conclusion="ok"),
    )

def test_markdown_contains_sections():
    md = render_markdown(_report())
    assert "# " in md and "mAP" in md and "未评估" in md and "4.0" in md

def test_json_roundtrip():
    data = json.loads(render_json(_report()))
    assert data["paper"]["title"] == "T"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_reporters.py -v`
Expected: FAIL（`ModuleNotFoundError`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/report/__init__.py
"""报告生成层。"""
```

```python
# src/cvpaper_eval/report/markdown_reporter.py
from __future__ import annotations

from ..models import DimensionStatus, EvalReport


def render_markdown(report: EvalReport) -> str:
    lines: list[str] = []
    lines.append(f"# 论文评价报告：{report.paper.title or '(未提供标题)'}")
    lines.append("")
    lines.append(f"- 来源：{report.paper.source.value}；arXiv: {report.paper.arxiv_id or '-'}")
    lines.append(f"- 综合评分：{report.summary.weighted_score if report.summary else '-'}/5")
    lines.append("")
    lines.append("## 实验指标")
    lines.append("")
    lines.append("| ID | 指标 | 数值 | 方法 | 数据集 | 来源 |")
    lines.append("|---|---|---|---|---|---|")
    for m in report.metrics:
        lines.append(f"| {m.metric_id} | {m.metric_name} | {m.value} | {m.method_key} | {m.dataset} | {m.source_location} |")
    lines.append("")
    lines.append("## 对比结论")
    lines.append("")
    for c in report.comparisons:
        lines.append(f"- [{c.type.value}] {c.conclusion}")
    lines.append("")
    lines.append("## 维度得分")
    lines.append("")
    lines.append("| 维度 | 得分 | 置信度 | 证据 |")
    lines.append("|---|---|---|---|")
    for d in report.dimension_scores:
        score = f"{d.score}" if d.score is not None else "-"
        lines.append(f"| {d.dimension} | {score} | {d.confidence} | {'；'.join(d.evidence) or '-'} |")
    lines.append("")
    if report.summary:
        lines.append("## 优势")
        for s in report.summary.strengths:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("## 不足")
        for w in report.summary.weaknesses:
            lines.append(f"- {w}")
        lines.append("")
        lines.append("## 综合结论")
        lines.append("")
        lines.append(report.summary.conclusion)
        lines.append("")
    not_evaluated = [d.dimension for d in report.dimension_scores if d.status == DimensionStatus.NOT_EVALUATED]
    review = [d.dimension for d in report.dimension_scores if d.status == DimensionStatus.REVIEW]
    lines.append("## 未评估 / 待审核")
    lines.append("")
    for name in not_evaluated:
        lines.append(f"- {name}：需外部数据，未评估")
    for name in review:
        lines.append(f"- {name}：争议维度，待人工审核")
    return "\n".join(lines)
```

```python
# src/cvpaper_eval/report/json_reporter.py
from __future__ import annotations

from ..models import EvalReport


def render_json(report: EvalReport) -> str:
    return report.model_dump_json(indent=2)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_reporters.py -v`
Expected: PASS（2 个用例）

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/report/__init__.py src/cvpaper_eval/report/markdown_reporter.py src/cvpaper_eval/report/json_reporter.py tests/test_reporters.py
git commit -m "feat: add markdown and json reporters"
```

---

### Task 13: 流水线与 CLI 端到端

**Files:**
- Create: `src/cvpaper_eval/pipeline.py`
- Create: `src/cvpaper_eval/cli.py`
- Create: `tests/test_pipeline.py`

**Interfaces:**
- Consumes: 全部前序模块
- Produces: `run_evaluation(source: str, source_kind: Literal["pdf","arxiv","text"], settings: Settings) -> EvalReport`；`main()`（argparse：`--input`、`--kind {pdf,arxiv,text}`、`--out-dir`，默认输出 `report.md` 与 `report.json`，要求 `DEEPSEEK_API_KEY` 环境变量）。流水线在评分后追加 `not_evaluated` 与 `review` 维度条目。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_pipeline.py
from pathlib import Path
from cvpaper_eval.config import Settings
from cvpaper_eval.pipeline import run_evaluation

class FakeChat:
    def __init__(self):
        self.calls = 0
    def chat_json(self, system, user):
        self.calls += 1
        if self.calls == 1:
            return {"metrics": [
                {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.482, "method_key": "Ours", "source_location": "TABLE 2", "normalization_note": ""},
                {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.421, "method_key": "Faster R-CNN", "source_location": "TABLE 2", "normalization_note": ""}
            ]}
        if self.calls == 2:
            return {"novelty_claims": [{"text": "new paradigm", "location": "SEC-001"}], "limitations": [], "openness": [], "ethics": [], "related_work": [], "clarity": []}
        return {"dimension_scores": [{"cluster_id": "CL-001", "score": 4, "confidence": "high", "evidence": ["new paradigm"]}]}

def test_run_evaluation_text(monkeypatch, tmp_path):
    from cvpaper_eval import pipeline
    monkeypatch.setattr(pipeline, "LLMClient", lambda settings: FakeChat())
    settings = Settings(api_key="sk-test", kb_path=Path("knowledge_base/indicators_v1.json"))
    text = "Abstract\nWe propose OursNet.\nExperiments\nmAP 0.482 vs 0.421.\nConclusion\nGood."
    report = run_evaluation(text, "text", settings)
    assert len(report.metrics) == 2
    assert report.comparisons
    assert report.summary.weighted_score is not None
    assert any(d.status.value == "not_evaluated" for d in report.dimension_scores)
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_pipeline.py -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'cvpaper_eval.pipeline'`）

- [ ] **Step 3: 实现**

```python
# src/cvpaper_eval/pipeline.py
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
```

```python
# src/cvpaper_eval/cli.py
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
```

- [ ] **Step 4: 运行测试确认通过 + CLI 冒烟**

Run: `pytest tests/test_pipeline.py -v`
Expected: PASS（1 个用例）

Run: `python -m cvpaper_eval.cli --help`
Expected: 显示参数说明

- [ ] **Step 5: 提交**

```bash
git add src/cvpaper_eval/pipeline.py src/cvpaper_eval/cli.py tests/test_pipeline.py
git commit -m "feat: wire pipeline and CLI end-to-end"
```

---

### Task 14: README 与演示说明

**Files:**
- Create: `README.md`
- Create: `outputs/.gitkeep`

**Interfaces:**
- Produces: 项目使用说明（安装、`.env`、三种输入用法、示例命令、输出说明）；空 `outputs/` 占位。

- [ ] **Step 1: 写失败测试（README 存在性）**

```python
# tests/test_readme.py
from pathlib import Path

def test_readme_exists():
    readme = Path("README.md")
    assert readme.exists()
    text = readme.read_text(encoding="utf-8")
    assert "DEEPSEEK_API_KEY" in text
    assert "--kind" in text
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_readme.py -v`
Expected: FAIL（`AssertionError`）

- [ ] **Step 3: 编写 README 与占位**

````markdown
# CV 论文宏观评价原型系统（cvpaper-eval）

输入一篇 CV 论文（PDF / arXiv 链接 / 文本），输出证据可追溯的 Markdown + JSON 评价报告。

## 安装

```bash
pip install -e ".[dev]"
```

## 配置

复制 `.env.example` 为 `.env`（或在环境中设置）：

```text
DEEPSEEK_API_KEY=sk-your-key
```

## 用法

```bash
# 纯文本（文件内为论文全文）
python -m cvpaper_eval.cli --input paper.txt --kind text --out-dir outputs/demo

# PDF
python -m cvpaper_eval.cli --input paper.pdf --kind pdf --out-dir outputs/demo

# arXiv id
python -m cvpaper_eval.cli --input 2501.00001 --kind arxiv --out-dir outputs/demo
```

输出：`outputs/demo/report.md`（人读）与 `outputs/demo/report.json`（机读）。

## 测试

```bash
pytest
```

设计文档见 `docs/superpowers/specs/2026-08-27-cv-paper-eval-mvp-design.md`。
````

```text
# outputs/.gitkeep
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_readme.py -v`
Expected: PASS（1 个用例）

- [ ] **Step 5: 提交**

```bash
git add README.md outputs/.gitkeep tests/test_readme.py
git commit -m "docs: add README and demo notes"
```

---

## 自查记录

- **Spec 覆盖**：spec 第 3 节架构五层全部落实（Task 5-7 解析层、Task 8-9 抽取层、Task 10 对比层、Task 11 评分层、Task 12 报告层、Task 13 流水线/CLI）；spec 第 5 节指标覆盖清单落实为 KB `metric_schema` 与 `validation.py` 范围表；spec 第 6 节 JSON 结构落实为 `models.py`；spec 第 11 节假设落实为 `config.py`（provider 可切换、温度 0.1、权重等权可配置）。
- **占位符扫描**：无 TBD/TODO/“类似 Task N”/“添加错误处理”等空泛表述；每个代码步骤均含完整可运行代码。
- **类型一致性**：`ChatJSON.chat_json(system, user) -> dict` 在 Task 3 定义，Task 8/9/11 的 extractor/scorer 均以该协议注入；`Metric.metric_id`/`source_location` 在 Task 1 定义并在 Task 8/10/12 引用；`DimensionStatus` 在 Task 1 定义并在 Task 12/13 使用；`build_summary` 返回 `Summary`，Task 13 直接挂到 `EvalReport.summary`。
- **后续计划**：Plan B（真实语料收集 + 知识库实证扩充）、Plan C（人工标注 + 抽取/评分质量评估）为独立计划；Agent 编排（v2）以 `run_evaluation()` 为调用入口，接口已就绪。
