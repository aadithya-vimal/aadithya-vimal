from pathlib import Path
import html


ROOT = Path(__file__).resolve().parents[1]
ASCII_PATH = ROOT / "assets" / "ascii-portrait.txt"
OUTPUT_PATH = ROOT / "assets" / "aadithya-ascii.svg"


def main() -> None:
    lines = ASCII_PATH.read_text(encoding="utf-8").splitlines()
    text_nodes = []
    base_x = 22
    base_y = 62
    step = 14
    for index, line in enumerate(lines):
      safe = html.escape(line)
      begin = 0.05 + index * 0.07
      y = base_y + index * step
      text_nodes.append(
          f'    <text x="{base_x}" y="{y}" opacity="0">{safe}'
          f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.2s" fill="freeze"/></text>'
      )

    svg = f"""<svg width="370" height="420" viewBox="0 0 370 420" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Aadithya Vimal ASCII portrait</title>
  <desc id="desc">Monochrome terminal styled ASCII portrait with animated text reveal.</desc>
  <defs>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22D3EE"/>
      <stop offset="50%" stop-color="#818CF8"/>
      <stop offset="100%" stop-color="#E879F9"/>
    </linearGradient>
  </defs>
  <rect width="370" height="420" rx="18" fill="#050816"/>
  <rect x="1" y="1" width="368" height="418" rx="17" stroke="#1F2937"/>
  <rect x="0" y="0" width="370" height="34" rx="18" fill="#0B1220"/>
  <circle cx="22" cy="17" r="5" fill="#EF4444"/>
  <circle cx="40" cy="17" r="5" fill="#F59E0B"/>
  <circle cx="58" cy="17" r="5" fill="#22C55E"/>
  <text x="185" y="22" fill="url(#titleGrad)" font-family="'Courier New', monospace" font-size="12" text-anchor="middle">Aadithya Vimal — portrait</text>

  <g fill="#E5E7EB" font-family="'Courier New', monospace" font-size="10" xml:space="preserve">
{chr(10).join(text_nodes)}
  </g>

  <g>
    <text x="22" y="330" fill="#67E8F9" font-family="'Courier New', monospace" font-size="12">name: Aadithya Vimal</text>
    <text x="22" y="352" fill="#C4B5FD" font-family="'Courier New', monospace" font-size="12">role: full-stack developer</text>
    <text x="22" y="374" fill="#93C5FD" font-family="'Courier New', monospace" font-size="12">focus: security · data · real-time</text>
    <rect x="22" y="389" width="11" height="14" fill="#22D3EE">
      <animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
"""
    OUTPUT_PATH.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
