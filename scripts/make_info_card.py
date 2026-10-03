"""Hand-authored neofetch-style card -> info-card.svg. Edit ROWS and re-run."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"

USER, HOST = "kioxr", "github"
ROWS = [  # (key, value) - None draws a blank line
    ("Name", "Ahmad Almashhadani"),
    ("Role", "Software Engineer"),
    ("Edu", "B.Sc. Computer Science, Qatar University"),
    ("Focus", "Backend systems · APIs · clean, tested, maintainable code"),
    None,
    ("Langs", "Python, JavaScript, C#, Bash, SQL"),
    ("Web", "Node.js, Express.js, REST APIs"),
    ("Data", "MySQL, SQLite, Firebase, Oracle SQL"),
    ("Practice", "Agile, UML, Git, system design, code review"),
    None,
    ("Built", "ResiWare: LLM-powered threat-detection system"),
    ("Contact", "abfmashhadani@gmail.com"),
]

BG, BORDER, TEXT, MUTED = "#0d1117", "#30363d", "#c9d1d9", "#7d8590"
KEY, ACCENT = "#58a6ff", "#39d353"
SWATCH = ["#ff7b72", "#ffa657", "#e3b341", "#39d353", "#58a6ff", "#bc8cff", "#f778ba", "#c9d1d9"]
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
W, X, KX, LH, TOP = 860, 28, 128, 23, 66


def main():
    out, y, i = [], TOP, 0

    def line(body, yy):
        nonlocal i
        out.append(f'<g class="l" style="animation-delay:{i * 0.09:.2f}s">{body}</g>')
        i += 1

    line(f'<text x="{X}" y="{y}" class="h"><tspan fill="{ACCENT}">{USER}</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{ACCENT}">{HOST}</tspan></text>', y)
    y += 10
    line(f'<line x1="{X}" y1="{y}" x2="{X + 120}" y2="{y}" stroke="{MUTED}" stroke-dasharray="4 3"/>', y)
    y += LH
    for row in ROWS:
        if row:
            k, v = row
            line(f'<text x="{X}" y="{y}"><tspan class="k">{escape(k)}</tspan></text>'
                 f'<text x="{KX}" y="{y}">{escape(v)}</text>', y)
        y += LH if row else LH // 2
    y += 4
    sw = "".join(f'<rect x="{X + n * 26}" y="{y - 12}" width="20" height="14" rx="3" fill="{c}"/>' for n, c in enumerate(SWATCH))
    line(sw, y)
    H = y + 26

    anim = "" if STATIC else (
        "@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}"
        ".l{opacity:0;animation:in .4s ease-out forwards}"
        "@media (prefers-reduced-motion:reduce){.l{animation:none;opacity:1}}"
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="About {USER}">
<style>
text{{font-family:{FONT};font-size:14px;fill:{TEXT}}}
.t{{font-size:12px}}.h{{font-size:15px;font-weight:700}}.k{{fill:{KEY};font-weight:700}}
{anim}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<circle cx="20" cy="19" r="5" fill="#ff5f57"/><circle cx="37" cy="19" r="5" fill="#febc2e"/><circle cx="54" cy="19" r="5" fill="#28c840"/>
<text x="{W / 2}" y="23" class="t" text-anchor="middle">{USER}@{HOST}: ~ neofetch</text>
<line x1="0" y1="36" x2="{W}" y2="36" stroke="{BORDER}"/>
{"".join(out)}
</svg>
'''
    (ROOT / "info-card.svg").write_text(svg)
    print("wrote info-card.svg")


if __name__ == "__main__":
    main()
