# CV 论文宏观评价原型系统（cvpaper-eval）

输入一篇 CV 论文（PDF / arXiv 链接 / 文本），输出证据可追溯的 Markdown + JSON 评价报告。

## 安装

```bash
pip install -e ".[dev]"
```

## 配置

复制 `.env.example` 为 `.env`（或在环境中设置）：

```text
DEEPSEEK_API_KEY=sk-your-key
```

## 用法

```bash
# 纯文本（文件内为论文全文）
python -m cvpaper_eval.cli --input paper.txt --kind text --out-dir outputs/demo

# PDF
python -m cvpaper_eval.cli --input paper.pdf --kind pdf --out-dir outputs/demo

# arXiv id
python -m cvpaper_eval.cli --input 2501.00001 --kind arxiv --out-dir outputs/demo
```

输出：`outputs/demo/report.md`（人读）与 `outputs/demo/report.json`（机读）。

## 测试

```bash
pytest
```

设计文档见 `docs/superpowers/specs/2026-08-27-cv-paper-eval-mvp-design.md`。
