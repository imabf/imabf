"""Scrape the public contribution calendar (no token) -> data/contributions.json"""
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

USER = os.environ.get("GH_USER", "kioxr")
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def build_payload(days, user=USER):
    """days: list of {date, count, level} -> payload with derived stats."""
    days = sorted(days, key=lambda d: d["date"])
    total = sum(d["count"] for d in days)

    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)

    current = 0
    tail = days[:-1] if days and days[-1]["count"] == 0 else days  # today may still be empty
    for d in reversed(tail):
        if not d["count"]:
            break
        current += 1

    best = max(days, key=lambda d: d["count"]) if days else None
    monthly = {}
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]

    return {
        "user": user,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total": total,
        "active_days": sum(1 for d in days if d["count"]),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]} if best and best["count"] else None,
        "monthly": monthly,
        "days": days,
    }


def fetch(user=USER):
    import requests
    from bs4 import BeautifulSoup

    r = requests.get(
        f"https://github.com/users/{user}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (profile-art)", "X-Requested-With": "XMLHttpRequest"},
        timeout=30,
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}

    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        m = re.match(r"\s*(\d+|No)\s+contribution", tips.get(td.get("id"), ""))
        count = int(m.group(1)) if m and m.group(1) != "No" else 0
        level = int(td.get("data-level", 0) or 0)
        if count == 0 and level > 0:  # tooltip missing: keep the cell visibly active
            count = level
        days.append({"date": td["data-date"], "count": count, "level": level})
    return days


if __name__ == "__main__":
    days = fetch()
    if len(days) < 300:
        sys.exit(f"Only parsed {len(days)} day cells; GitHub markup may have changed. Keeping old data.")
    payload = build_payload(days)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"{payload['total']} contributions over {len(days)} days -> {OUT}")
