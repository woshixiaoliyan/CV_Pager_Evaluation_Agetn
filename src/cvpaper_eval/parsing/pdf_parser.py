from __future__ import annotations

import fitz


def _clean_cells(cells: list) -> list[str]:
    return ["" if c is None else str(c).strip() for c in cells]


def flatten_table_rows(rows: list[list]) -> list[dict]:
    """把 pymupdf extract() 的二维数组转成 {header, cells} 行记录。

    首行视为表头；None 转空串；空表头或全空行丢弃。
    """
    if not rows:
        return []
    header = " ".join(c for c in _clean_cells(rows[0]) if c)
    if not header:
        return []
    out: list[dict] = []
    for row in rows[1:]:
        cells = _clean_cells(row)
        if not any(cells):
            continue
        out.append({"header": header, "cells": cells})
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