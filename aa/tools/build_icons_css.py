"""Generate docs/stylesheets/icons.css from the Lucide SVG set.

Why this exists
---------------
Icons are needed in two places: the theme chrome (mkdocs.yml `theme.icon.*`,
which reads overrides/.icons/lucide/*.svg at build time) and the document
body. MkDocs has no built-in way to inline an icon in body text, and
pymdownx.snippets only substitutes when its marker sits alone on a line --
which is not where icons go.

So we expose the same SVG files as CSS mask classes. In Markdown you write:

    <span class="aa-i aa-i-check"></span>

The mask is filled with `currentColor`, so icons follow the surrounding text
colour automatically.

Run this after adding or changing a file in overrides/.icons/lucide/:

    python tools/build_icons_css.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "overrides" / ".icons" / "lucide"
OUT = ROOT / "docs" / "stylesheets" / "icons.css"

HEADER = """/* ==========================================================================
   图标工具类 —— 由 tools/build_icons_css.py 自动生成，请勿手工编辑
   --------------------------------------------------------------------------
   源图：overrides/.icons/lucide/*.svg（Lucide，ISC，1.75 描边）
   用法：<span class="aa-i aa-i-check"></span>
   图标颜色跟随当前文字颜色（mask + currentColor）。
   改动图标后重新生成：python tools/build_icons_css.py
   ========================================================================== */

.aa-i {
  display: inline-block;
  width: 1.15em;
  height: 1.15em;
  vertical-align: -0.2em;
  flex: none;
  background-color: currentColor;
  -webkit-mask: var(--aa-i) center / contain no-repeat;
  mask: var(--aa-i) center / contain no-repeat;
}

"""


def to_data_uri(svg: str) -> str:
    """Percent-encode just enough to sit safely inside a CSS url()."""
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    svg = re.sub(r"\s+", " ", svg)
    svg = svg.replace('"', "'").replace("#", "%23")
    return f'url("data:image/svg+xml;charset=utf-8,{svg}")'


def main() -> None:
    files = sorted(ICON_DIR.glob("*.svg"))
    if not files:
        raise SystemExit(f"no icons found in {ICON_DIR}")

    rules = []
    for path in files:
        name = path.stem
        rules.append(f".aa-i-{name} {{ --aa-i: {to_data_uri(path.read_text(encoding='utf-8'))}; }}")

    OUT.write_text(HEADER + "\n".join(rules) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(files)} icons)")


if __name__ == "__main__":
    main()
