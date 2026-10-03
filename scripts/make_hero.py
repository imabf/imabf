"""Animated hero banner -> hero.svg (gradient, code rain, cycling tagline). Edit LINES and re-run."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"

NAME = "Ahmad Almashhadani"
LINES = [
    "Building reliable backend systems",
    "Designing clean, well-tested APIs",
    "Clean APIs. Tested code. Shipped.",
]
W, H = 860, 220
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
RAIN = ["const build = () => ship();", "def handle(req): ...", "git commit -m 'ship it'",
        "SELECT * FROM impact;", "app.get('/api', handler)", "assert result == expected",
        "class Service: ...", "npm run test && deploy", "async function run() {}", "return Ok(data)"]


def main():
    rain = []
    for i, t in enumerate(RAIN):
        x = 20 + (i * 83) % 820
        d = 5 + (i % 4)
        rain.append(f'<text class="r" x="{x}" y="0" style="animation-duration:{d}s;animation-delay:-{i * 0.9:.1f}s">{escape(t)}</text>')
    n = len(LINES)
    dur = 4 * n
    tag = []
    for i, line in enumerate(LINES):
        a, b = i / n, (i + 1) / n
        kt = f"0;{a:.3f};{a + .03:.3f};{b - .04:.3f};{b - .01:.3f};1"
        vals = "0;0;1;1;0;0"
        if STATIC:
            tag.append(f'<text x="430" y="150" class="tag" text-anchor="middle" opacity="{1 if i == 0 else 0}">&gt; {line}</text>')
        else:
            tag.append(
                f'<text x="430" y="150" class="tag" text-anchor="middle" opacity="0">&gt; {line}'
                f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></text>')
    anim = "" if STATIC else (
        "@keyframes fall{from{transform:translateY(-10px);opacity:0}15%{opacity:.5}to{transform:translateY(240px);opacity:0}}"
        ".r{animation:fall linear infinite}"
        "@keyframes glow{0%,100%{opacity:.8}50%{opacity:1}}.nm{animation:glow 3s ease-in-out infinite}"
        "@media (prefers-reduced-motion:reduce){.r,.nm{animation:none}}")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}, Software Engineer">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset=".55" stop-color="#101a2e"/><stop offset="1" stop-color="#0d2a1f"/></linearGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#58a6ff"/><stop offset=".5" stop-color="#bc8cff"/><stop offset="1" stop-color="#39d353"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<style>
text{{font-family:{FONT}}}
.r{{font-size:11px;fill:#39d353;opacity:0}}
.nm{{font-size:44px;font-weight:800;fill:url(#nm)}}
.tag{{font-size:19px;fill:#c9d1d9}}
.sub{{font-size:12px;fill:#7d8590;letter-spacing:3px}}
{anim}
</style>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{"".join(rain)}
<rect width="{W}" height="{H}" fill="#0d1117" opacity=".35"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="#30363d"/>
<text x="430" y="82" class="nm" text-anchor="middle">{NAME}</text>
<text x="430" y="108" class="sub" text-anchor="middle">SOFTWARE ENGINEER</text>
{"".join(tag)}
</svg>
'''
    (ROOT / "hero.svg").write_text(svg)
    print("wrote hero.svg")


if __name__ == "__main__":
    main()
