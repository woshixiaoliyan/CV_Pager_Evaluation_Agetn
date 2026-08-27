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
    index = 1
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
