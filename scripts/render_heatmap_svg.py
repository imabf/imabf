"""data/contributions.json -> contrib-heatmap.svg (animated once on load, then frozen)."""
import datetime as dt
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BG, BORDER, TEXT, MUTED, ACCENT = "#0d1117", "#30363d", "#c9d1d9", "#7d8590", "#39d353"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
CELL, GAP = 12, 3
STEP = CELL + GAP
W, LEFT, TOP = 860, 46, 62


def main():
    data = json.loads((ROOT / "data" / "contributions.json").read_text())
    days = data["days"]
    first = dt.date.fromisoformat(days[0]["date"])
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # back to Sunday
    best = data["best_day"]["count"] if data.get("best_day") else 0

    cells, months, seen, max_col = [], [], set(), 0
    for d in days:
        date = dt.date.fromisoformat(d["date"])
        off = (date - start).days
        col, row = off // 7, off % 7
        max_col = max(max_col, col)
        level = d["level"]
        if best >= 4 and d["count"] == best:
            level = 5  # neon top end for the best day
        x, y = LEFT + col * STEP, TOP + row * STEP
        n = d["count"]
        tip = f"{n if n else 'No'} contribution{'' if n == 1 else 's'} on {date:%b} {date.day}, {date.year}"
        cells.append(
            f'<rect class="c d{col + row}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
            f'fill="{PALETTE[level]}"><title>{tip}</title></rect>'
        )
        key = (date.year, date.month)
        if key not in seen and date.day <= 7 and row == 0:
            seen.add(key)
            months.append(f'<text x="{x}" y="{TOP - 9}" class="m">{date:%b}</text>')

    labels = "".join(
        f'<text x="{LEFT - 8}" y="{TOP + r * STEP + 10}" class="m" text-anchor="end">{t}</text>'
        for r, t in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )

    grid_bottom = TOP + 7 * STEP
    H = grid_bottom + 62
    lx = LEFT + (max_col + 1) * STEP - GAP - (len(PALETTE) * STEP + 74)
    legend = f'<text x="{lx}" y="{grid_bottom + 22}" class="m">Less</text>'
    for i, c in enumerate(PALETTE):
        legend += f'<rect x="{lx + 34 + i * STEP}" y="{grid_bottom + 12}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>'
    legend += f'<text x="{lx + 40 + len(PALETTE) * STEP}" y="{grid_bottom + 22}" class="m">More</text>'

    stats = [f'<tspan class="hi">{data["total"]:,}</tspan> contributions in the last year']
    stats.append(f'<tspan class="hi">{data["active_days"]}</tspan> active days')
    stats.append(f'longest streak <tspan class="hi">{data["longest_streak"]}d</tspan>')
    if data.get("best_day"):
        bd = dt.date.fromisoformat(data["best_day"]["date"])
        stats.append(f'best day <tspan class="hi">{data["best_day"]["count"]}</tspan> ({bd:%b} {bd.day})')
    footer = f'<text x="{LEFT}" y="{grid_bottom + 46}" class="s f">' + '  <tspan class="sep">·</tspan>  '.join(stats) + "</text>"

    diag = max_col + 7
    if STATIC:
        anim = ""
    else:
        anim = (
            "@keyframes drop{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:none}}"
            "@keyframes fade{from{opacity:0}to{opacity:1}}"
            ".c{opacity:0;animation:drop .45s ease-out forwards}"
            f".f{{opacity:0;animation:fade .6s ease-out {diag * 0.028 + 0.3:.2f}s forwards}}"
            + "".join(f".d{i}{{animation-delay:{i * 0.028:.3f}s}}" for i in range(diag))
            + "@media (prefers-reduced-motion:reduce){.c,.f{animation:none;opacity:1}}"
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{data["total"]} contributions in the last year by {data["user"]}">
<style>
text{{font-family:{FONT};font-size:11px;fill:{MUTED}}}
.t{{font-size:12px;fill:{TEXT}}}.s{{font-size:12px;fill:{MUTED}}}.hi{{fill:{ACCENT};font-weight:600}}.sep{{fill:{BORDER}}}
{anim}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<circle cx="20" cy="19" r="5" fill="#ff5f57"/><circle cx="37" cy="19" r="5" fill="#febc2e"/><circle cx="54" cy="19" r="5" fill="#28c840"/>
<text x="{W / 2}" y="23" class="t" text-anchor="middle">{data["user"]}@github: ~/contributions</text>
<line x1="0" y1="36" x2="{W}" y2="36" stroke="{BORDER}"/>
{"".join(months)}{labels}
{"".join(cells)}
<g class="f">{legend}</g>
{footer}
</svg>
'''
    (ROOT / "contrib-heatmap.svg").write_text(svg)
    print("wrote contrib-heatmap.svg")


if __name__ == "__main__":
    main()
