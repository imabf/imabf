"""Tech-stack chips -> stack.svg. Edit GROUPS and re-run."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"
GROUPS = [
    ("Languages", "#58a6ff", ["Python", "JavaScript", "C#", "Bash", "SQL"]),
    ("Backend", "#39d353", ["Node.js", "Express", "FastAPI", "REST APIs", "Async pub/sub"]),
    ("AI / LLM", "#f778ba", ["Ollama", "Local LLMs", "Output validation"]),
    ("Data", "#bc8cff", ["SQLite", "MySQL", "Oracle SQL", "Firebase"]),
    ("Craft", "#ffa657", ["pytest", "Git", "Linux", "Ansible", "Agile", "UML"]),
]
W, X0, ROW = 860, 28, 46
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def main():
    out, i = [], 0
    for r, (title, col, items) in enumerate(GROUPS):
        y = 66 + r * ROW
        out.append(f'<text x="{X0}" y="{y + 5}" class="g" fill="{col}">{title}</text>')
        x = 150
        for it in items:
            w = 14 + 8.4 * len(it)
            out.append(
                f'<g class="p" style="animation-delay:{i * 0.07:.2f}s"><rect x="{x:.0f}" y="{y - 14}" width="{w:.0f}" height="28" rx="14" '
                f'fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".6"/>'
                f'<text x="{x + w / 2:.0f}" y="{y + 5}" text-anchor="middle" class="c">{escape(it)}</text></g>')
            x += w + 10
            i += 1
    H = 66 + len(GROUPS) * ROW + 4
    anim = "" if STATIC else (
        "@keyframes pop{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
        ".p{opacity:0;animation:pop .4s ease-out forwards}"
        "@media (prefers-reduced-motion:reduce){.p{animation:none;opacity:1}}")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Tech stack">
<style>text{{font-family:{FONT};font-size:13px}}.g{{font-weight:700}}.c{{fill:#c9d1d9}}.t{{font-size:12px;fill:#7d8590}}{anim}</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="#0d1117" stroke="#30363d"/>
<circle cx="20" cy="19" r="5" fill="#ff5f57"/><circle cx="37" cy="19" r="5" fill="#febc2e"/><circle cx="54" cy="19" r="5" fill="#28c840"/>
<text x="{W / 2}" y="23" class="t" text-anchor="middle">imabf@github: ~/stack</text>
<line x1="0" y1="36" x2="{W}" y2="36" stroke="#30363d"/>
{"".join(out)}
</svg>
'''
    (ROOT / "stack.svg").write_text(svg)
    print("wrote stack.svg")


if __name__ == "__main__":
    main()
