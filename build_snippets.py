#!/usr/bin/env python3
"""为每个专业生成 HTML 片段，供交互式网页内嵌显示"""
import re
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
MAJORS_DIR = ROOT / "docs" / "majors"
OUT_DIR = ROOT / "data" / "html"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MAJOR_ORDER = [
    "computer-science", "artificial-intelligence", "data-science",
    "software-engineering", "cyber-security", "microelectronics",
    "automation", "robotics",
]

md = markdown.Markdown(extensions=["tables", "fenced_code"])

for mid in MAJOR_ORDER:
    src = MAJORS_DIR / f"{mid}.md"
    text = src.read_text(encoding="utf-8")

    # 去掉首行 H1 标题和更新日期
    text = re.sub(r'^# .*?\n\n>.*?\n\n', '', text, count=1, flags=re.DOTALL)

    # 转换
    html = md.convert(text)

    # 包裹成干净的片段
    snippet = f"""<div class="major-full-content">
{html}
</div>"""

    out_path = OUT_DIR / f"{mid}.html"
    out_path.write_text(snippet, encoding="utf-8")
    print(f"  ✓ {mid}.html")

print(f"\n生成完成 → {OUT_DIR}")
