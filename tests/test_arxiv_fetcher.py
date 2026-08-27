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
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
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
