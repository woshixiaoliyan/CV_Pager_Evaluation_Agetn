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
