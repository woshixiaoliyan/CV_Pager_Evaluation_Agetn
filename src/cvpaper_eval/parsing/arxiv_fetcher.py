from __future__ import annotations

import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from ..models import PaperMeta, PaperSource

_NS = {"a": "http://www.w3.org/2005/Atom"}
_HEADERS = {"User-Agent": "cvpaper-eval/0.1 (academic research demo)"}


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
    with urllib.request.urlopen(urllib.request.Request(api_url, headers=_HEADERS)) as resp:
        meta = _parse_meta(resp.read(), arxiv_id)
    pdf_path = dest_dir / f"{arxiv_id}.pdf"
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    with urllib.request.urlopen(urllib.request.Request(pdf_url, headers=_HEADERS)) as resp:
        pdf_path.write_bytes(resp.read())
    return meta, pdf_path
