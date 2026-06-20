#!/usr/bin/env python3
"""
高考专业选择指南 —— 整合构建脚本
将所有 Markdown 内容按层级整合为屏幕优化的单页 HTML，支持浏览器阅读。
"""

import re
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
MAJORS_DIR = DOCS / "majors"

MAJOR_ORDER = [
    "computer-science", "artificial-intelligence", "data-science",
    "software-engineering", "cyber-security", "microelectronics",
    "automation", "robotics",
]

MAJOR_NAMES = {
    "computer-science": "计算机科学与技术",
    "artificial-intelligence": "人工智能",
    "data-science": "数据科学与大数据技术",
    "software-engineering": "软件工程",
    "cyber-security": "网络空间安全",
    "microelectronics": "微电子科学与工程",
    "automation": "自动化",
    "robotics": "机器人工程",
}


def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_combined_markdown() -> str:
    """整合所有 Markdown 内容为单个文档"""
    parts = []

    # Part 1: 导读（README）
    readme = read_file(ROOT / "README.md")
    # 移除开头的 H1 标题行和紧随的引用行
    readme = re.sub(
        r'^# 高考专业选择指南.*?\n\n>.*?\n\n',
        '',
        readme,
        count=1,
        flags=re.DOTALL
    )
    readme = readme.strip()
    parts.append("# 第一部分：导读与决策框架\n\n")
    parts.append(readme)
    parts.append("\n\n")

    # Part 2: 学科门类总览
    overview = read_file(DOCS / "overview.md")
    overview = re.sub(r"^# 学科门类总览", "", overview, count=1).strip()
    parts.append("# 第二部分：学科门类总览\n\n")
    parts.append(overview)
    parts.append("\n\n")

    # Part 3: 专业快速对比
    index_md = read_file(MAJORS_DIR / "INDEX.md")
    index_md = re.sub(r"^# 专业索引.*$", "", index_md, count=1).strip()
    index_md = re.sub(
        r"### 各专业解读进度.*?(?=\n---|\Z)", "", index_md, flags=re.DOTALL
    )
    parts.append("# 第三部分：专业快速对比\n\n")
    parts.append(index_md)
    parts.append("\n\n")

    # Part 4: 各专业深度解读
    parts.append("# 第四部分：专业深度解读\n\n")
    for i, major_id in enumerate(MAJOR_ORDER):
        major_md = read_file(MAJORS_DIR / f"{major_id}.md")
        major_md = re.sub(r"^# ", "## ", major_md, count=1)
        parts.append(major_md)
        parts.append("\n\n")

    return "\n".join(parts)


def md_to_html(md_text: str) -> str:
    """Markdown → HTML"""
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "nl2br"]
    )
    return md.convert(md_text)


CSS = """
/* ===== 全局 ===== */
:root {
  --blue: #2563eb;
  --blue-light: #eff6ff;
  --text: #1e293b;
  --text-muted: #64748b;
  --bg: #f8fafc;
  --border: #e2e8f0;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.85;
  color: var(--text);
  background: #fff;
  -webkit-font-smoothing: antialiased;
}

/* ===== 容器 ===== */
.container {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ===== 封面 ===== */
.cover {
  text-align: center;
  padding: 100px 24px 80px;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  margin-bottom: 48px;
}
.cover h1 {
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 16px;
  letter-spacing: 2px;
}
.cover .subtitle {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 8px;
}
.cover .date {
  font-size: 14px;
  opacity: 0.65;
  margin-top: 24px;
}

/* ===== 目录 ===== */
.toc {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 32px 36px;
  margin-bottom: 48px;
}
.toc h2 {
  font-size: 22px;
  text-align: center;
  border-bottom: 2px solid var(--blue);
  padding-bottom: 12px;
  margin-bottom: 20px;
}
.toc ul { list-style: none; padding: 0; }
.toc li { margin: 4px 0; }
.toc a {
  color: var(--text);
  text-decoration: none;
  display: block;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.15s;
}
.toc a:hover { background: #e0e7ff; color: var(--blue); }
.toc .toc-h2 { font-weight: 600; font-size: 15px; margin-top: 12px; }
.toc .toc-h3 { padding-left: 24px; font-size: 14px; color: var(--text-muted); }
.toc .toc-part { font-weight: 700; font-size: 15px; margin-top: 16px; color: var(--blue); }

/* ===== 正文排版 ===== */
.content { padding-bottom: 80px; }

h1 {
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
  border-bottom: 3px solid var(--blue);
  padding-bottom: 10px;
  margin: 56px 0 28px;
}

h2 {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 44px 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

h3 {
  font-size: 18px;
  font-weight: 600;
  color: #334155;
  margin: 32px 0 12px;
}

h4 {
  font-size: 16px;
  font-weight: 600;
  color: #475569;
  margin: 24px 0 8px;
}

p { margin: 10px 0; }

/* ===== 表格 ===== */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 18px 0;
  font-size: 14px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
thead th, table th {
  background: var(--blue);
  color: #fff;
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
}
table td {
  padding: 9px 12px;
  border-bottom: 1px solid var(--border);
}
table tbody tr:nth-child(even) td {
  background: #f8fafc;
}
table tbody tr:hover td {
  background: #eff6ff;
}

/* ===== 引用块 ===== */
blockquote {
  border-left: 4px solid var(--blue);
  background: var(--blue-light);
  padding: 14px 20px;
  margin: 18px 0;
  border-radius: 0 8px 8px 0;
  color: #334155;
  font-size: 14px;
}

/* ===== 代码 ===== */
code {
  font-family: "SF Mono", "Menlo", "Monaco", monospace;
  font-size: 13px;
  background: #f1f5f9;
  color: #e11d48;
  padding: 2px 6px;
  border-radius: 4px;
}
pre {
  background: #1e293b;
  color: #e2e8f0;
  padding: 18px 22px;
  border-radius: 10px;
  font-size: 13px;
  overflow-x: auto;
  line-height: 1.6;
  margin: 18px 0;
}
pre code {
  background: none;
  color: inherit;
  padding: 0;
}

/* ===== 列表 ===== */
ul, ol { padding-left: 1.4em; margin: 8px 0; }
li { margin-bottom: 4px; }

/* ===== 分隔线 ===== */
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 40px 0;
}

/* ===== 链接 ===== */
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ===== 强调 ===== */
strong { color: #0f172a; font-weight: 700; }

/* ===== 回到顶部 ===== */
.back-to-top {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 44px;
  height: 44px;
  background: var(--blue);
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(37,99,235,0.3);
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 100;
}
.back-to-top.visible { opacity: 1; }

/* ===== 打印样式 ===== */
@media print {
  .back-to-top { display: none; }
  body { font-size: 11pt; line-height: 1.7; }
  .container { max-width: 100%; padding: 0; }
  .cover { padding: 40px 24px; background: none; color: var(--text); }
  .cover h1 { font-size: 24pt; color: var(--text); }
  h1 { page-break-before: always; font-size: 18pt; }
  h1:first-of-type { page-break-before: avoid; }
  h2 { font-size: 14pt; }
  h3 { font-size: 12pt; }
  table { font-size: 9pt; }
  table th { background: #ddd; color: #000; }
  .toc { background: none; border: 1px solid #ccc; }
  pre { background: #f5f5f5; color: #333; border: 1px solid #ddd; }
}

/* ===== 响应式 ===== */
@media (max-width: 640px) {
  .container { padding: 0 16px; }
  h1 { font-size: 22px; }
  h2 { font-size: 18px; }
  table { font-size: 12px; }
  table th, table td { padding: 6px 8px; }
  .cover { padding: 60px 16px 48px; }
  .cover h1 { font-size: 26px; }
}
"""


def build_toc(html_body: str) -> str:
    """从 HTML 中提取标题，生成可点击的目录"""
    headings = re.findall(
        r'<h([12])[^>]*>(.+?)</h\1>',
        html_body,
        re.DOTALL
    )

    toc_html = ['<nav class="toc"><h2>目 录</h2><ul>']

    for level, title in headings:
        # 清理 HTML 标签得到纯文本
        clean = re.sub(r'<[^>]+>', '', title).strip()
        # 生成锚点 ID（和 markdown toc 扩展一致）
        anchor = re.sub(r'[^\w\- ]', '', clean)
        anchor = anchor.strip().lower().replace(' ', '-')
        # 在实际 HTML 中插入 id
        html_body = html_body.replace(
            f'<h{level}>{title}</h{level}>',
            f'<h{level} id="{anchor}">{title}</h{level}>',
            1
        )

        css_class = 'toc-h2' if level == '1' else 'toc-h3'
        toc_html.append(
            f'<li class="{css_class}"><a href="#{anchor}">{clean}</a></li>'
        )

    toc_html.append('</ul></nav>')
    return '\n'.join(toc_html), html_body


def build_html(html_body: str) -> str:
    """生成完整 HTML"""

    # 先生成目录，同时给标题加锚点
    toc_nav, html_body = build_toc(html_body)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>高考专业选择指南 — AI 时代下的专业抉择</title>
<style>
{CSS}
</style>
</head>
<body>

<div class="cover">
<h1>高考专业选择指南</h1>
<p class="subtitle">AI 时代下的专业抉择</p>
<p class="subtitle" style="font-size:15px;opacity:0.75;">—— 从芯片到应用，8 个核心专业的全景解读 ——</p>
<p class="date">2026 年 6 月</p>
</div>

<div class="container">
{toc_nav}

<div class="content">
{html_body}
</div>
</div>

<button class="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="回到顶部">↑</button>

<script>
// 回到顶部按钮显示/隐藏
window.addEventListener('scroll', function() {{
  var btn = document.querySelector('.back-to-top');
  if (window.scrollY > 600) {{
    btn.classList.add('visible');
  }} else {{
    btn.classList.remove('visible');
  }}
}});
</script>

</body>
</html>"""


def main():
    print("📝 整合 Markdown 文档...")
    combined_md = build_combined_markdown()

    md_path = ROOT / "高考专业选择指南_完整版.md"
    md_path.write_text(combined_md, encoding="utf-8")
    print(f"  ✓ Markdown: {md_path.name}")

    print("🌐 转换为 HTML（含可点击目录）...")
    html_body = md_to_html(combined_md)
    full_html = build_html(html_body)

    html_path = ROOT / "index.html"
    html_path.write_text(full_html, encoding="utf-8")
    print(f"  ✓ HTML: {html_path.name}")

    char_count = len(combined_md)
    print(f"\n📊 ~{char_count:,} 字符 | 8 个专业 | 4 大部分")
    print(f"✨ 浏览器打开 → {html_path}")


if __name__ == "__main__":
    main()
