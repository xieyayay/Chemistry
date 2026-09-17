"""Download the design system's webfonts and generate a self-hosted fonts.css.

Why this exists
---------------
`system.css` pulls Inter and JetBrains Mono from fonts.googleapis.com with
`@import`. Two problems with that in practice:

  1. googleapis.com is unreachable from mainland China, so the fonts silently
     fall back to Arial and the design system's typography is lost.
  2. CSS `@import` blocks rendering -- an unreachable host can leave the page
     blank for seconds.

So we vendor the fonts instead. Only the `latin` subset is fetched: the docs
are Chinese, the CJK glyphs already come from the system fonts (PingFang SC /
Microsoft YaHei), and Google's latin subset covers ASCII, digits and the
arrow glyphs the docs use.

Run after bumping a font version:

    python tools/fetch_fonts.py

It writes docs/fonts/*.woff2 and docs/stylesheets/fonts.css.
"""
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "docs" / "fonts"
OUT_CSS = ROOT / "docs" / "stylesheets" / "fonts.css"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# 只取页面真正用到的字重：Inter 的 400/500/600/700，等宽字体的 400/500
FAMILIES = [
    ("Inter", "Inter:wght@400;500;600;700", {"400", "500", "600", "700"}),
    ("JetBrains Mono", "JetBrains+Mono:wght@400;500", {"400", "500"}),
]

SUBSET = "latin"  # 中文由系统字体兜底，不需要下 CJK 子集


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def main() -> None:
    FONT_DIR.mkdir(parents=True, exist_ok=True)

    rules = []
    total = 0

    for family, spec, weights in FAMILIES:
        css = fetch(f"https://fonts.googleapis.com/css2?family={spec}&display=swap").decode()
        blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{(.*?)\}", css, re.S)

        for subset, body in blocks:
            if subset != SUBSET:
                continue
            weight = re.search(r"font-weight:\s*(\d+)", body).group(1)
            if weight not in weights:
                continue

            src = re.search(r"url\((https://[^)]+\.woff2)\)", body).group(1)
            name = f"{slug(family)}-{weight}.woff2"
            data = fetch(src)
            (FONT_DIR / name).write_bytes(data)
            total += len(data)
            print(f"  {name:<28} {len(data):>6d} bytes")

            rules.append(
                "@font-face {\n"
                f'  font-family: "{family}";\n'
                "  font-style: normal;\n"
                f"  font-weight: {weight};\n"
                "  font-display: swap;\n"
                f'  src: url("../fonts/{name}") format("woff2");\n'
                "}"
            )

    header = (
        "/* ==========================================================================\n"
        "   自托管字体 —— 由 tools/fetch_fonts.py 自动生成，请勿手工编辑\n"
        "   --------------------------------------------------------------------------\n"
        "   源文件：docs/fonts/*.woff2（Inter 与 JetBrains Mono，SIL Open Font License 1.1）\n"
        "   为什么不用 Google Fonts：googleapis.com 在国内不可达，而且 CSS @import\n"
        "   会阻塞渲染。自托管之后站点 100% 自包含，内网断网都能正常显示。\n"
        "   只取了 latin 子集，中文字形由系统字体（苹方 / 微软雅黑）兜底。\n"
        "   改动字体后重新生成：python tools/fetch_fonts.py\n"
        "   ========================================================================== */\n\n"
    )
    OUT_CSS.write_text(header + "\n\n".join(rules) + "\n", encoding="utf-8")

    print(f"\n共 {len(rules)} 个字体文件，{total} bytes = {total / 1024:.0f} KB")
    print(f"写出 {OUT_CSS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
