from pathlib import Path

def test_readme_exists():
    readme = Path("README.md")
    assert readme.exists()
    text = readme.read_text(encoding="utf-8")
    assert "DEEPSEEK_API_KEY" in text
    assert "--kind" in text
