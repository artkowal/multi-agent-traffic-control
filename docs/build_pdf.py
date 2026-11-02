"""Generuje docs/architektura.pdf i docs/img/architektura.svg z docs/architektura.md.

Wymagania: pandoc, mermaid-cli (mmdc), Python + playwright (chromium).
Użycie: python docs/build_pdf.py
"""
import base64
import pathlib
import re
import subprocess
import tempfile

from playwright.sync_api import sync_playwright

DOCS = pathlib.Path(__file__).resolve().parent
SRC = DOCS / "architektura.md"
OUT = DOCS / "architektura.pdf"
SVG = DOCS / "img" / "architektura.svg"

CSS = """
@page { size: A4; margin: 18mm 16mm; }
@page wide { size: A4 landscape; margin: 12mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10pt; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 20pt; margin: 0 0 4pt; }
h2 { font-size: 14pt; margin-top: 18pt; border-bottom: 1px solid #ccc; padding-bottom: 3pt; }
h3 { font-size: 11.5pt; margin-top: 12pt; }
h2, h3 { page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9pt; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background: #f0f0f0; }
code { background: #f3f3f3; padding: 0 3px; border-radius: 3px; font-size: 9pt; }
.diagram-page { page: wide; break-before: page; break-after: page; }
.diagram-page h2 { margin-top: 0; }
.diagram-page img { display: block; max-width: 100%; max-height: 165mm; margin: 0 auto; }
"""

FOOTER = ("<div style='font-size:8px;width:100%;text-align:center;color:#888'>"
          "<span class='pageNumber'></span> / <span class='totalPages'></span></div>")


def render_diagram(mermaid: str, tmp: pathlib.Path) -> bytes:
    mmd = tmp / "d.mmd"
    png = tmp / "d.png"
    mmd.write_text(mermaid, encoding="utf-8")
    SVG.parent.mkdir(exist_ok=True)
    subprocess.run(["mmdc", "-i", mmd, "-o", SVG, "-b", "white"], check=True, capture_output=True)
    subprocess.run(["mmdc", "-i", mmd, "-o", png, "-b", "white", "-s", "3"], check=True, capture_output=True)
    return png.read_bytes()


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    pattern = re.compile(r"## ([^\n]*)\n+```mermaid\n(.*?)```", re.S)

    with tempfile.TemporaryDirectory() as t:
        def repl(m: re.Match) -> str:
            png = base64.b64encode(render_diagram(m.group(2), pathlib.Path(t))).decode()
            return (f'<div class="diagram-page"><h2>{m.group(1)}</h2>'
                    f'<img src="data:image/png;base64,{png}"></div>')

        text = pattern.sub(repl, text)

    body = subprocess.run(["pandoc", "-f", "gfm", "-t", "html"], input=text,
                          capture_output=True, text=True, check=True).stdout
    html = f"<!DOCTYPE html><html lang='pl'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="load")
        page.pdf(path=str(OUT), print_background=True, prefer_css_page_size=True,
                 display_header_footer=True, header_template="<span></span>", footer_template=FOOTER)
        browser.close()
    print(f"OK: {OUT.relative_to(DOCS.parent)}")


if __name__ == "__main__":
    main()
