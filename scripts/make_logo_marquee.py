"""Generate an animated scrolling logo marquee from live simple-icons brand logos.

Fetches each brand's vector path from the simple-icons CDN and bakes it into a
self-contained, infinitely scrolling SVG (SMIL animation — no JavaScript), so it
renders anywhere an <img> works, including GitHub profile READMEs.

Regenerate locally whenever you want a fresh snapshot:
    python scripts/make_logo_marquee.py
"""

from __future__ import annotations

import datetime as dt
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "assets" / "logo-marquee.svg"

# ---------------------------------------------------------------- palette ---
BG = "#050816"
CHROME = "#0B1220"
BORDER = "#1F2937"
CYAN = "#22D3EE"
INDIGO = "#818CF8"
FUCHSIA = "#E879F9"

# slug, label, brand color (dark-bg-friendly where the brand mark is near-black)
LOGOS: list[tuple[str, str, str]] = [
    ("typescript", "TypeScript", "#3178C6"),
    ("javascript", "JavaScript", "#F7DF1E"),
    ("python", "Python", "#3776AB"),
    ("c", "C", "#A8B9CC"),
    ("cplusplus", "C++", "#00599C"),
    ("html5", "HTML5", "#E34F26"),
    ("css", "CSS3", "#1572B6"),
    ("gnubash", "Bash", "#4EAA25"),
    ("react", "React", "#61DAFB"),
    ("nextdotjs", "Next.js", "#FFFFFF"),
    ("nodedotjs", "Node.js", "#5FA04E"),
    ("tailwindcss", "Tailwind CSS", "#06B6D4"),
    ("postgresql", "PostgreSQL", "#4169E1"),
    ("prisma", "Prisma", "#5A67D8"),
    ("docker", "Docker", "#2496ED"),
    ("git", "Git", "#F05032"),
    ("linux", "Linux", "#FCC624"),
    ("kalilinux", "Kali Linux", "#557C94"),
    ("numpy", "NumPy", "#5EC8E5"),
    ("pandas", "pandas", "#A78BFA"),
    ("rust", "Rust", "#DEA584"),
    ("solana", "Solana", "#9945FF"),
]

LOGO_HEIGHT = 68
SLOT_WIDTH = 94
SPEED = 90            # px per second (marquee speed)
LOGO_COLOR = "#FFFFFF"   # single light color: guarantees visibility on the dark card


def fetch_icon_path(slug: str) -> str | None:
    """Return the path `d` for a simple-icons slug, or None on failure."""
    url = f"https://cdn.simpleicons.org/{slug}"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        svg = response.read().decode("utf-8")
    match = re.search(r'<path[^>]*\bd="([^"]+)"', svg)
    return match.group(1) if match else None


def chip(label: str, color: str, x: float, y: float) -> str:
    """Fallback: a rounded chip with the label text when the icon can't load."""
    w = 11.5 * len(label) + 18
    return (
        f'<g transform="translate({x:.1f} {y:.1f})">'
        f'<rect width="{w:.1f}" height="24" rx="7" fill="{CHROME}" stroke="{BORDER}"/>'
        f'<text x="{w / 2:.1f}" y="16" fill="{color}" font-family="\'Courier New\', monospace" '
        f'font-size="11" text-anchor="middle">{label}</text></g>'
    )


def build_svg(items: list[tuple[str, str, str, str | None]]) -> str:
    n = len(items)
    seq_width = n * SLOT_WIDTH
    duration = seq_width / SPEED
    scale = LOGO_HEIGHT / 24.0
    top = 88
    center_y = top + (LOGO_HEIGHT / 2)

    copies: list[str] = []
    for copy in range(2):
        for index, (slug, label, color, path_d) in enumerate(items):
            slot_x = copy * seq_width + index * SLOT_WIDTH
            icon_x = slot_x + (SLOT_WIDTH - LOGO_HEIGHT) / 2
            if path_d:
                logo = (
                    f'<g transform="translate({icon_x:.1f} {top:.1f}) scale({scale:.4f})">'
                    f'<title>{label}</title>'
                    f'<path d="{path_d}" fill="{LOGO_COLOR}"/></g>'
                )
            else:
                logo = chip(label, LOGO_COLOR, slot_x, center_y - 12)
            copies.append(logo)

    labels = ", ".join(label for _, label, _, _ in items)
    width = 920
    height = 210

    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Aadithya Vimal — tech stack</title>
  <desc id="desc">Scrolling marquee of the technologies I work with: {labels}. Regenerate locally with scripts/make_logo_marquee.py.</desc>
  <defs>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{CYAN}"/>
      <stop offset="50%" stop-color="{INDIGO}"/>
      <stop offset="100%" stop-color="{FUCHSIA}"/>
    </linearGradient>
    <!-- mask luminance: white = visible, black/transparent = hidden -->
    <linearGradient id="fadeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="7%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="93%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <mask id="fadeMask">
      <rect x="0" y="0" width="{width}" height="{height}" fill="url(#fadeGrad)"/>
    </mask>
  </defs>

  <rect width="{width}" height="{height}" rx="20" fill="{BG}"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="19" stroke="{BORDER}"/>
  <rect x="0" y="0" width="{width}" height="34" rx="20" fill="{CHROME}"/>
  <circle cx="22" cy="17" r="5" fill="#EF4444"/>
  <circle cx="40" cy="17" r="5" fill="#F59E0B"/>
  <circle cx="58" cy="17" r="5" fill="#22C55E"/>
  <text x="{width / 2}" y="22" fill="url(#titleGrad)" font-family="'Courier New', monospace" font-size="12" text-anchor="middle">Aadithya Vimal — stack</text>

  <g mask="url(#fadeMask)">
    <g class="marquee-track">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-{seq_width} 0" dur="{duration:.1f}s" repeatCount="indefinite"/>
      {''.join(copies)}
    </g>
  </g>
</svg>
"""


def main() -> None:
    items: list[tuple[str, str, str, str | None]] = []
    failures = 0
    for slug, label, color in LOGOS:
        try:
            path_d = fetch_icon_path(slug)
        except Exception:
            path_d = None
        if not path_d:
            failures += 1
        items.append((slug, label, color, path_d))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_svg(items), encoding="utf-8")
    print(
        f"wrote {OUTPUT_PATH} ({len(items) - failures} logos, "
        f"{failures} fell back to text chips)"
    )


if __name__ == "__main__":
    main()
