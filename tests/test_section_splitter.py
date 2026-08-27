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
