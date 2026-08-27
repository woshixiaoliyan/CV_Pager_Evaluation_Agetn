from __future__ import annotations

import re

from ..models import Metric


def _value_candidates(value: float) -> list[str]:
    cands = [f"{value:g}"]
    if value != int(value):
        cands.append(f"{value:.2f}")
        cands.append(f"{value:.1f}")
    cands.append(str(value))
    seen: set[str] = set()
    out: list[str] = []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _referenced_table(tables: list[dict], loc: str) -> list[list[str]] | None:
    m = re.search(r"TABLE\s*(\d+)", loc, re.IGNORECASE)
    if not m:
        return None
    target = int(m.group(1))
    for t in tables:
        tm = re.search(r"TABLE\s*(\d+)", str(t.get("id", "")), re.IGNORECASE)
        if tm and int(tm.group(1)) == target:
            cells: list[list[str]] = []
            for r in t.get("rows", []):
                row = [str(c) for c in r.get("cells", [])]
                row.append(str(r.get("header", "")))
                cells.append(row)
            return cells
    return None


def metric_has_evidence(metric: Metric, text: str, tables: list[dict]) -> bool:
    """数值必须能在其引用的表格或论文文本中定位，否则视为不可信（防幻觉）。"""
    cands = _value_candidates(metric.value)
    table_cells = _referenced_table(tables, metric.source_location)
    if table_cells is not None:
        joined = " ".join(" ".join(row) for row in table_cells)
        for c in cands:
            if c in joined:
                return True
    for c in cands:
        if c in text:
            return True
    return False