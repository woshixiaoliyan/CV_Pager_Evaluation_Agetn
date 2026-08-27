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
    assert out[0]["cells"] == ["Ours", "0.482", "35"]


def test_flatten_table_rows_ignores_none_and_empty():
    rows = [["Method", "mAP", None], ["Ours", "0.482", None], [None, None, None]]
    out = flatten_table_rows(rows)
    assert len(out) == 1
    assert out[0]["cells"] == ["Ours", "0.482", ""]