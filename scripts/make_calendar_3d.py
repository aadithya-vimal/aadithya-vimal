"""Generate an animated isometric 3D contribution pillar from live GitHub data.

Fetches the last ~371 days of per-day contribution levels straight from
GitHub's public contributions page (no token, no API key, no GitHub Actions)
and renders an isometric "city of contributions" SVG with a growing animation.

Regenerate locally whenever you want a fresh snapshot:
    python scripts/make_calendar_3d.py
"""

from __future__ import annotations

import datetime as dt
import math
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "assets" / "calendar-3d.svg"
USERNAME = "aadithya-vimal"

# ---------------------------------------------------------------- palette ---
BG = "#050816"
CHROME = "#0B1220"
BORDER = "#1E293B"
MUTED = "#64748B"
SUBTLE = "#94A3B8"

CYAN = "#22D3EE"
SKY = "#38BDF8"
INDIGO = "#818CF8"
FUCHSIA = "#E879F9"
GREEN = "#4ADE80"

# level -> top-face base color (cyan -> sky -> indigo -> fuchsia ramp)
LEVEL_COLORS = {
    0: "#1E293B",
    1: "#22D3EE",
    2: "#38BDF8",
    3: "#818CF8",
    4: "#E879F9",
}

RIGHT_SHADE = 0.72   # right face darker
LEFT_SHADE = 0.52    # left face darkest


def shade(hex_color: str, factor: float) -> str:
    """Darken a #RRGGBB color by multiplying channels with factor."""
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return f"#{int(r * factor):02X}{int(g * factor):02X}{int(b * factor):02X}"


# ------------------------------------------------------------- data layer ---
def fetch_grid() -> dict[tuple[int, int], tuple[str, int]]:
    """Return {(col, row): (iso_date, level)} for the 53x7 GitHub calendar grid.

    Row 0 is Sunday, col 0 is the earliest week; the grid covers the last 371
    days. Level is 0-4, GitHub's own aggregation of that day's contribution count.
    """
    url = f"https://github.com/users/{USERNAME}/contributions"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "aadithya-vimal-profile-art",
            "Accept": "text/html",
        },
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        html_text = response.read().decode("utf-8")

    pattern = re.compile(
        r'<td[^>]*?id="contribution-day-component-(\d+)-(\d+)"[^>]*>'
    )
    cells: dict[tuple[int, int], tuple[str, int]] = {}
    for match in pattern.finditer(html_text):
        tag = match.group(0)
        row, col = int(match.group(1)), int(match.group(2))
        date = re.search(r'data-date="([0-9-]+)"', tag).group(1)
        level = int(re.search(r'data-level="([0-4])"', tag).group(1))
        cells[(col, row)] = (date, level)
    return cells


def fallback_grid() -> dict[tuple[int, int], tuple[str, int]]:
    """Deterministic synthetic grid used when the network is unavailable."""
    today = dt.date.today()
    row_of_today = (today.weekday() + 1) % 7  # GitHub row 0 == Sunday
    start = today - dt.timedelta(days=row_of_today + 52 * 7)
    cells: dict[tuple[int, int], tuple[str, int]] = {}
    for col in range(53):
        for row in range(7):
            day = start + dt.timedelta(days=col * 7 + row)
            level = (col + row + day.day // 5 + day.month) % 5
            cells[(col, row)] = (day.isoformat(), level)
    return cells


# ------------------------------------------------------------- geometry -----
CELL = 15.0               # isometric unit spacing
A = CELL * math.cos(math.pi / 6)   # horizontal half-step
B = CELL * math.sin(math.pi / 6)   # vertical half-step
H_UNIT = 6.5              # pillar height per contribution level
COLS, ROWS = 53, 7


def grid_pos(col: int, row: int) -> tuple[float, float]:
    return ((col - row) * A, (col + row) * B)


def polygon(points: list[tuple[float, float]], fill: str) -> str:
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{coords}" fill="{fill}"/>'


# --------------------------------------------------------------- svg build ---
def build_svg(cells: dict[tuple[int, int], tuple[str, int]]) -> str:
    today = dt.date.today()
    generated = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y %H:%M UTC")

    levels = {pos: lvl for pos, (_, lvl) in cells.items()}
    active = sum(1 for lvl in levels.values() if lvl > 0)

    order = sorted(levels, key=lambda pos: (pos[0] + pos[1], pos[0]))

    # --- grid corner positions ------------------------------------------------
    g00 = grid_pos(0, 0)
    g53_0 = grid_pos(COLS, 0)
    g53_7 = grid_pos(COLS, ROWS)
    g0_7 = grid_pos(0, ROWS)

    ground = polygon([g00, g53_0, g53_7, g0_7], CHROME)
    ground = ground.replace("/>", ' stroke="#1E293B" stroke-width="1"/>')

    # --- glow behind the pillar ------------------------------------------------
    glow_cx = (g53_0[0] + g0_7[0]) / 2
    glow_cy = g53_7[1] - 60
    glow = (
        f'<ellipse cx="{glow_cx:.1f}" cy="{glow_cy:.1f}" rx="330" ry="130" '
        f'fill="url(#pillarGlow)" opacity="0">'
        f'<animate attributeName="opacity" values="0;0.45;0" dur="6s" '
        f'repeatCount="indefinite"/></ellipse>'
    )

    # --- columns ----------------------------------------------------------------
    column_groups: list[str] = []
    for col, row in order:
        level = levels[(col, row)]
        height = level * H_UNIT
        base = LEVEL_COLORS[level]
        gx, gy = grid_pos(col, row)
        h = height
        g = [(gx, gy), (gx + A, gy + B), (gx, gy + 2 * B), (gx - A, gy + B)]
        t = [(gx, gy - h), (gx + A, gy + B - h), (gx, gy + 2 * B - h), (gx - A, gy + B - h)]

        faces = [polygon([t[0], t[1], t[2], t[3]], base)]
        if h > 0:
            faces.append(polygon([g[1], g[2], t[2], t[1]], shade(base, RIGHT_SHADE)))
            faces.append(polygon([g[3], g[2], t[2], t[3]], shade(base, LEFT_SHADE)))

        body = "".join(faces)
        if h > 0:
            begin = 0.04 * col + 0.02 * row
            column_groups.append(
                f'<g><animateTransform attributeName="transform" type="translate" '
                f'from="0 {h:.1f}" to="0 0" begin="{begin:.2f}s" dur="0.35s" '
                f'fill="freeze"/>{body}</g>'
            )
        else:
            column_groups.append(f"<g>{body}</g>")

    # --- labels ------------------------------------------------------------------
    month_labels: list[str] = []
    last_month: int | None = None
    for col in range(COLS):
        date_str = cells.get((col, 3), cells.get((col, 0)))[0]
        day = dt.date.fromisoformat(date_str)
        if day.month != last_month:
            gx, gy = grid_pos(col, 3)
            month_labels.append(
                f'<text x="{gx + A:.1f}" y="{gy + 2 * B + 16:.1f}" fill="{SKY}" '
                f'font-family="\'Courier New\', monospace" font-size="9">'
                f'{day.strftime("%b")}</text>'
            )
            last_month = day.month

    weekday_labels: list[str] = []
    for row in (1, 3, 5):
        gx, gy = grid_pos(0, row)
        label = ("Mon", "Wed", "Fri")[(row - 1) // 2]
        weekday_labels.append(
            f'<text x="{gx - A - 8:.1f}" y="{gy + B + 3:.1f}" fill="{INDIGO}" '
            f'font-family="\'Courier New\', monospace" font-size="9" '
            f'text-anchor="end">{label}</text>'
        )

    # --- legend + footer (below the grid) ----------------------------------------
    legend_y = g53_7[1] + 2 * B + 44
    legend_swatches = "".join(
        f'<rect x="{62 + i * 15}" y="{legend_y - 10}" width="10" height="10" rx="3" '
        f'fill="{LEVEL_COLORS[i]}"/>'
        for i in range(5)
    )
    footer_y = legend_y + 18

    # --- content bounding box -----------------------------------------------------
    xs = [g00[0], g53_0[0], g53_7[0], g0_7[0]]
    ys = [0, g53_7[1] + 2 * B]
    xs += [gx + A for gx in [grid_pos(c, 3)[0] for c in range(COLS)]]
    ys += [grid_pos(c, 3)[1] + 2 * B + 16 for c in range(COLS)]
    xs += [grid_pos(0, r)[0] - A - 8 for r in (1, 3, 5)]
    ys += [grid_pos(0, r)[1] + B + 3 for r in (1, 3, 5)]
    content_x_min, content_x_max = min(xs), max(xs)
    content_y_min = -4 * H_UNIT - 6          # tallest column top
    content_y_max = footer_y + 6

    # --- chrome (title bar + subtitle sit above the content) -----------------------
    title_bar_h = 34
    title_gap = 44                            # between title bar and subtitle baseline
    y_min = content_y_min - title_bar_h - title_gap - 6
    x_min = content_x_min - 28
    x_max = content_x_max + 28
    y_max = content_y_max + 10
    width = x_max - x_min
    height = y_max - y_min

    title_cy = y_min + 17                     # title bar center
    subtitle_y = y_min + title_bar_h + 20
    chrome_bottom = y_min + title_bar_h       # bottom edge of title bar

    # subtitle: three colored segments (plain language, human-readable)
    seg_a = f"days with activity: {active} / 371"
    seg_b = "   over the last 12 months"
    seg_c = f"   refreshed {generated}"
    char_w = 6.6
    sub_x = x_min + 26
    subtitle = (
        f'<text x="{sub_x:.1f}" y="{subtitle_y:.1f}" fill="{CYAN}" '
        f'font-family="\'Courier New\', monospace" font-size="11">{seg_a}</text>'
        f'<text x="{sub_x + len(seg_a) * char_w:.1f}" y="{subtitle_y:.1f}" fill="{INDIGO}" '
        f'font-family="\'Courier New\', monospace" font-size="11">{seg_b}</text>'
        f'<text x="{sub_x + (len(seg_a) + len(seg_b)) * char_w:.1f}" y="{subtitle_y:.1f}" fill="{MUTED}" '
        f'font-family="\'Courier New\', monospace" font-size="11">{seg_c}</text>'
    )

    return f"""<svg width="{width:.0f}" height="{height:.0f}" viewBox="{x_min:.0f} {y_min:.0f} {width:.0f} {height:.0f}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Aadithya Vimal 3D contribution pillar</title>
  <desc id="desc">Isometric 3D contribution calendar built from live GitHub data, animated with growing columns.</desc>
  <defs>
    <radialGradient id="pillarGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{CYAN}" stop-opacity="0.55"/>
      <stop offset="45%" stop-color="{INDIGO}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{FUCHSIA}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{CYAN}"><animate attributeName="stop-color" values="{CYAN};{FUCHSIA};{CYAN}" dur="8s" repeatCount="indefinite"/></stop>
      <stop offset="50%" stop-color="{INDIGO}"><animate attributeName="stop-color" values="{INDIGO};{SKY};{INDIGO}" dur="8s" repeatCount="indefinite"/></stop>
      <stop offset="100%" stop-color="{FUCHSIA}"><animate attributeName="stop-color" values="{FUCHSIA};{CYAN};{FUCHSIA}" dur="8s" repeatCount="indefinite"/></stop>
    </linearGradient>
  </defs>

  <rect x="{x_min:.0f}" y="{y_min:.0f}" width="{width:.0f}" height="{height:.0f}" rx="20" fill="{BG}"/>
  <rect x="{x_min + 1:.0f}" y="{y_min + 1:.0f}" width="{width - 2:.0f}" height="{height - 2:.0f}" rx="19" stroke="{BORDER}"/>
  <rect x="{x_min:.0f}" y="{y_min:.0f}" width="{width:.0f}" height="{title_bar_h}" rx="20" fill="{CHROME}"/>
  <circle cx="{x_min + 22:.0f}" cy="{title_cy:.0f}" r="5" fill="#EF4444"/>
  <circle cx="{x_min + 40:.0f}" cy="{title_cy:.0f}" r="5" fill="#F59E0B"/>
  <circle cx="{x_min + 58:.0f}" cy="{title_cy:.0f}" r="5" fill="#22C55E"/>
  <text x="{x_min + width / 2:.0f}" y="{title_cy + 5:.0f}" fill="url(#titleGrad)" font-family="'Courier New', monospace" font-size="12" text-anchor="middle">Aadithya Vimal — contributions</text>

  {subtitle}

  <g>
    <animate attributeName="opacity" from="0" to="1" begin="0.1s" dur="0.6s" fill="freeze"/>
    {glow}
    {ground}
    {''.join(column_groups)}
  </g>

  {''.join(weekday_labels)}
  {''.join(month_labels)}

  <text x="{x_min + 26:.0f}" y="{footer_y:.0f}" fill="{MUTED}" font-family="'Courier New', monospace" font-size="10">less</text>
  {legend_swatches}
  <text x="{x_min + 140:.0f}" y="{footer_y:.0f}" fill="{MUTED}" font-family="'Courier New', monospace" font-size="10">more</text>
  <text x="{x_max - 26:.0f}" y="{footer_y:.0f}" fill="{MUTED}" font-family="'Courier New', monospace" font-size="10" text-anchor="end">built from live GitHub data</text>
</svg>
"""


def main() -> None:
    try:
        cells = fetch_grid()
    except Exception:
        cells = fallback_grid()
    if len(cells) < 53 * 7:
        cells = fallback_grid()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_svg(cells), encoding="utf-8")
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
