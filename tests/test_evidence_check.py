from cvpaper_eval.models import Metric
from cvpaper_eval.extraction.evidence_check import metric_has_evidence

def _m(value, loc="TABLE 2", name="mAP"):
    return Metric(metric_id="M-0", task="detection", dataset="COCO", metric_name=name,
                  value=value, method_key="Ours", source_location=loc)

TABLES = [
    {"id": "TABLE 1", "rows": [{"header": "Method mAP", "cells": ["Ours", "0.482"]}]},
    {"id": "TABLE 2", "rows": [{"header": "Method mAP", "cells": ["Ours", "44.9"]}]},
]

def test_value_found_in_referenced_table():
    assert metric_has_evidence(_m(44.9), "some text", TABLES) is True

def test_value_not_found_anywhere():
    assert metric_has_evidence(_m(99.9), "some text without the number", TABLES) is False

def test_value_found_in_text():
    assert metric_has_evidence(_m(0.482), "we reach mAP 0.482 on COCO", TABLES) is True

def test_referenced_table_missing_falls_back_to_text():
    assert metric_has_evidence(_m(3.14, loc="TABLE 99"), "pi is 3.14", TABLES) is True