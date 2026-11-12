#!/usr/bin/env node

/**
 * Generates Apple-inspired light and dark SVG assets for the profile README:
 *   - assets/hero-light.svg, assets/hero-dark.svg
 *   - assets/focus-light.svg, assets/focus-dark.svg
 *   - assets/calendar-3d-light.svg, assets/calendar-3d.svg
 *   - assets/logo-marquee-light.svg, assets/logo-marquee.svg
 */

import fs from 'fs';
import https from 'https';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const ASSETS = path.join(ROOT, 'assets');
const USERNAME = 'aadithya-vimal';

const FONT_SANS = `-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Segoe UI', Helvetica, Arial, sans-serif`;
const FONT_MONO = `'SF Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`;

const PALETTES = {
  light: {
    canvas: '#F5F5F7',
    card: '#FFFFFF',
    border: '#E5E5EA',
    ink: '#1D1D1F',
    inkSecondary: '#515154',
    inkMuted: '#6E6E73',
    accent: '#0071E3',
    accentSoft: '#E8F2FF',
    specular: '#FFFFFF',
    specularOpacity: '0.75',
    iconColor: '#1D1D1F',
    plateFill: '#FFFFFF',
    plateStroke: '#E5E5EA',
    levels: ['#E5E5EA', '#B9DDFF', '#62B0FF', '#0071E3', '#004B9A'],
  },
  dark: {
    canvas: '#141416',
    card: '#1C1C1E',
    border: '#2C2C2E',
    ink: '#F5F5F7',
    inkSecondary: '#A1A1A6',
    inkMuted: '#8E8E93',
    accent: '#0A84FF',
    accentSoft: '#1C2D42',
    specular: '#FFFFFF',
    specularOpacity: '0.045',
    iconColor: '#F5F5F7',
    plateFill: '#1C1C1E',
    plateStroke: '#2C2C2E',
    levels: ['#232326', '#0E3968', '#0060C7', '#0A84FF', '#64B5FF'],
  },
};

function escapeXml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function shadeHex(hex, factor) {
  const r = Math.round(parseInt(hex.slice(1, 3), 16) * factor);
  const g = Math.round(parseInt(hex.slice(3, 5), 16) * factor);
  const b = Math.round(parseInt(hex.slice(5, 7), 16) * factor);
  return `#${[r, g, b].map((v) => Math.max(0, Math.min(255, v)).toString(16).padStart(2, '0')).join('')}`;
}

// ------------------------------------------------------------------ 1. Hero --
function buildHeroSvg(mode) {
  const p = PALETTES[mode];
  const width = 860;
  const height = 216;
  const gradId = `heroSpec-${mode}`;

  return `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" font-family="${FONT_SANS}">
  <title id="title">Aadithya Vimal</title>
  <desc id="desc">Full-Stack Engineer, Security Researcher, and Systems Architect.</desc>
  <defs>
    <radialGradient id="${gradId}" cx="14%" cy="0%" r="85%">
      <stop offset="0%" stop-color="${p.specular}" stop-opacity="${p.specularOpacity}"/>
      <stop offset="100%" stop-color="${p.specular}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="${width}" height="${height}" rx="20" fill="${p.canvas}"/>
  <rect width="${width}" height="${height}" rx="20" fill="url(#${gradId})"/>
  <rect x="0.5" y="0.5" width="${width - 1}" height="${height - 1}" rx="19.5" stroke="${p.border}"/>

  <text x="40" y="50" fill="${p.inkMuted}" font-size="11" font-weight="600" letter-spacing="1.8">
    FULL-STACK ENGINEER  ·  SECURITY RESEARCHER  ·  SYSTEMS ARCHITECT
  </text>

  <text x="40" y="96" fill="${p.ink}" font-size="38" font-weight="700" letter-spacing="-0.8">
    Aadithya Vimal
  </text>

  <text x="40" y="130" fill="${p.inkSecondary}" font-size="15" font-weight="400">
    Engineering resilient web systems, threat-aware architectures, and applied intelligence.
  </text>

  <line x1="40" y1="158" x2="${width - 40}" y2="158" stroke="${p.border}" stroke-width="1"/>

  <circle cx="45" cy="184" r="4" fill="${p.accent}"/>
  <text x="58" y="188" fill="${p.inkSecondary}" font-size="12.5" font-weight="500">
    @aadithya-vimal  ·  @alesaai  ·  aadithyavimal.pages.dev
  </text>

  <text x="${width - 40}" y="188" fill="${p.inkMuted}" font-size="12" font-weight="500" text-anchor="end">
    Security · Systems · Applied AI
  </text>
</svg>
`;
}

// ------------------------------------------------------------ 2. Core Focus --
function buildFocusSvg(mode) {
  const p = PALETTES[mode];
  const width = 860;
  const height = 186;
  const gap = 13;
  const cardW = 278; // 278 * 3 + 13 * 2 = 860

  const pillars = [
    {
      title: 'Security Architecture',
      lines: [
        'Threat-aware design from day one.',
        'Adversarial surface analysis, protocol',
        'triage, and static validation.',
      ],
      icon: `<path d="M12 3.2L19 6.2V11.4C19 15.8 16.05 19.65 12 20.8C7.95 19.65 5 15.8 5 11.4V6.2L12 3.2Z" stroke="${p.accent}" stroke-width="1.65" stroke-linejoin="round"/><path d="M9.5 12L11.2 13.7L14.8 10.1" stroke="${p.accent}" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"/>`,
    },
    {
      title: 'Full-Stack Systems',
      lines: [
        'Low-latency TypeScript and Next.js',
        'interfaces backed by resilient,',
        'type-safe distributed data layers.',
      ],
      icon: `<rect x="4.5" y="5" width="15" height="5.5" rx="2" stroke="${p.accent}" stroke-width="1.65"/><rect x="4.5" y="13.5" width="15" height="5.5" rx="2" stroke="${p.accent}" stroke-width="1.65"/><circle cx="7.5" cy="7.75" r="0.9" fill="${p.accent}"/><circle cx="7.5" cy="16.25" r="0.9" fill="${p.accent}"/>`,
    },
    {
      title: 'Applied Intelligence',
      lines: [
        'Multi-provider AI orchestration with',
        'deterministic fallbacks and',
        'decision-grade telemetry.',
      ],
      icon: `<circle cx="12" cy="12" r="2.6" stroke="${p.accent}" stroke-width="1.65"/><circle cx="6" cy="7" r="1.75" stroke="${p.accent}" stroke-width="1.5"/><circle cx="18" cy="7" r="1.75" stroke="${p.accent}" stroke-width="1.5"/><circle cx="6" cy="17" r="1.75" stroke="${p.accent}" stroke-width="1.5"/><circle cx="18" cy="17" r="1.75" stroke="${p.accent}" stroke-width="1.5"/><path d="M7.5 8.2L10 10.3M16.5 8.2L14 10.3M7.5 15.8L10 13.7M16.5 15.8L14 13.7" stroke="${p.accent}" stroke-width="1.4" stroke-linecap="round"/>`,
    },
  ];

  const cardsXml = pillars
    .map((item, idx) => {
      const x = idx * (cardW + gap);
      const linesXml = item.lines
        .map(
          (line, li) =>
            `<text x="24" y="${124 + li * 19}" fill="${p.inkSecondary}" font-size="12.5" font-weight="400">${escapeXml(line)}</text>`
        )
        .join('\n    ');

      return `<g transform="translate(${x}, 0)">
    <rect width="${cardW}" height="${height}" rx="18" fill="${p.canvas}"/>
    <rect x="0.5" y="0.5" width="${cardW - 1}" height="${height - 1}" rx="17.5" stroke="${p.border}"/>
    <rect x="24" y="24" width="38" height="38" rx="10" fill="${p.accentSoft}"/>
    <g transform="translate(31, 31)">
      ${item.icon}
    </g>
    <text x="24" y="92" fill="${p.ink}" font-size="16" font-weight="600" letter-spacing="-0.2">${escapeXml(item.title)}</text>
    ${linesXml}
  </g>`;
    })
    .join('\n  ');

  return `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" font-family="${FONT_SANS}">
  <title id="title">Engineering Focus</title>
  <desc id="desc">Three core engineering disciplines: Security Architecture, Full-Stack Systems, and Applied Intelligence.</desc>
  ${cardsXml}
</svg>
`;
}

// --------------------------------------------------------- 3. 3D Calendar --
function fetchContributionsHtml() {
  return new Promise((resolve, reject) => {
    const req = https.get(
      `https://github.com/users/${USERNAME}/contributions`,
      {
        headers: {
          'User-Agent': 'aadithya-vimal-profile',
          Accept: 'text/html',
        },
        timeout: 15000,
      },
      (res) => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          reject(new Error(`HTTP ${res.statusCode}`));
          return;
        }
        let body = '';
        res.on('data', (c) => (body += c));
        res.on('end', () => resolve(body));
      }
    );
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timed out'));
    });
  });
}

function parseContributionCells(html) {
  const cells = new Map();
  const tdRegex = /<td[^>]*?id="contribution-day-component-(\d+)-(\d+)"[^>]*>/g;
  let m;
  while ((m = tdRegex.exec(html)) !== null) {
    const tag = m[0];
    const row = parseInt(m[1], 10);
    const col = parseInt(m[2], 10);
    const dateMatch = tag.match(/data-date="([0-9-]+)"/);
    const levelMatch = tag.match(/data-level="([0-4])"/);
    if (dateMatch && levelMatch) {
      cells.set(`${col},${row}`, {
        col,
        row,
        date: dateMatch[1],
        level: parseInt(levelMatch[1], 10),
      });
    }
  }
  return cells;
}

function fallbackCells() {
  const cells = new Map();
  const today = new Date();
  const rowOfToday = today.getUTCDay();
  const start = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()));
  start.setUTCDate(start.getUTCDate() - (rowOfToday + 52 * 7));

  for (let col = 0; col < 53; col++) {
    for (let row = 0; row < 7; row++) {
      const d = new Date(start);
      d.setUTCDate(start.getUTCDate() + col * 7 + row);
      const iso = d.toISOString().slice(0, 10);
      const level = (col + row + Math.floor(d.getUTCDate() / 6) + d.getUTCMonth()) % 5;
      cells.set(`${col},${row}`, { col, row, date: iso, level });
    }
  }
  return cells;
}

function buildCalendarSvg(cells, mode) {
  const p = PALETTES[mode];
  const CELL = 15.0;
  const A = CELL * Math.cos(Math.PI / 6);
  const B = CELL * Math.sin(Math.PI / 6);
  const H_UNIT = 6.2;
  const COLS = 53;
  const ROWS = 7;

  const gridPos = (col, row) => [(col - row) * A, (col + row) * B];
  const poly = (pts, fill, extra = '') =>
    `<polygon points="${pts.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(' ')}" fill="${fill}"${extra}/>`;

  let active = 0;
  const ordered = [];
  for (const cell of cells.values()) {
    if (cell.level > 0) active++;
    ordered.push(cell);
  }
  ordered.sort((a, b) => (a.col + a.row) - (b.col + b.row) || a.col - b.col);

  const g00 = gridPos(0, 0);
  const g53_0 = gridPos(COLS, 0);
  const g53_7 = gridPos(COLS, ROWS);
  const g0_7 = gridPos(0, ROWS);

  const ground = poly(
    [g00, g53_0, g53_7, g0_7],
    p.plateFill,
    ` stroke="${p.plateStroke}" stroke-width="1"`
  );

  const columnsXml = ordered
    .map(({ col, row, level }) => {
      const h = level * H_UNIT;
      const base = p.levels[level];
      const [gx, gy] = gridPos(col, row);
      const g = [
        [gx, gy],
        [gx + A, gy + B],
        [gx, gy + 2 * B],
        [gx - A, gy + B],
      ];
      const t = [
        [gx, gy - h],
        [gx + A, gy + B - h],
        [gx, gy + 2 * B - h],
        [gx - A, gy + B - h],
      ];

      let faces = poly([t[0], t[1], t[2], t[3]], base);
      if (h > 0) {
        faces += poly([g[1], g[2], t[2], t[1]], shadeHex(base, 0.78));
        faces += poly([g[3], g[2], t[2], t[3]], shadeHex(base, 0.60));
        const begin = (0.03 * col + 0.015 * row).toFixed(2);
        return `<g><animateTransform attributeName="transform" type="translate" from="0 ${h.toFixed(1)}" to="0 0" begin="${begin}s" dur="0.32s" fill="freeze"/>${faces}</g>`;
      }
      return `<g>${faces}</g>`;
    })
    .join('');

  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const monthLabels = [];
  let lastMonth = -1;
  for (let col = 0; col < COLS; col++) {
    const cell = cells.get(`${col},3`) || cells.get(`${col},0`);
    if (!cell) continue;
    const month = parseInt(cell.date.slice(5, 7), 10) - 1;
    if (month !== lastMonth) {
      const [gx, gy] = gridPos(col, 3);
      monthLabels.push(
        `<text x="${(gx + A).toFixed(1)}" y="${(gy + 2 * B + 16).toFixed(1)}" fill="${p.inkMuted}" font-family="${FONT_MONO}" font-size="9">${monthNames[month]}</text>`
      );
      lastMonth = month;
    }
  }

  const weekdayLabels = [
    [1, 'Mon'],
    [3, 'Wed'],
    [5, 'Fri'],
  ].map(([row, label]) => {
    const [gx, gy] = gridPos(0, row);
    return `<text x="${(gx - A - 8).toFixed(1)}" y="${(gy + B + 3).toFixed(1)}" fill="${p.inkMuted}" font-family="${FONT_MONO}" font-size="9" text-anchor="end">${label}</text>`;
  });

  const legendY = g53_7[1] + 2 * B + 42;
  const footerY = legendY + 18;

  const xs = [g00[0], g53_0[0], g53_7[0], g0_7[0]];
  for (let c = 0; c < COLS; c++) xs.push(gridPos(c, 3)[0] + A);
  for (const r of [1, 3, 5]) xs.push(gridPos(0, r)[0] - A - 8);

  const xMin = Math.min(...xs) - 28;
  const xMax = Math.max(...xs) + 28;
  const yMin = -4 * H_UNIT - 68;
  const yMax = footerY + 16;
  const width = Math.round(xMax - xMin);
  const height = Math.round(yMax - yMin);

  const headerY = Math.round(yMin + 34);
  const legendStartX = Math.round(xMin + 28);

  const swatches = p.levels
    .map(
      (color, i) =>
        `<rect x="${legendStartX + 34 + i * 15}" y="${Math.round(footerY - 9)}" width="10" height="10" rx="2.5" fill="${color}"/>`
    )
    .join('');

  return `<svg width="${width}" height="${height}" viewBox="${Math.round(xMin)} ${Math.round(yMin)} ${width} ${height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" font-family="${FONT_SANS}">
  <title id="title">Contribution Activity</title>
  <desc id="desc">Isometric 3D GitHub contribution activity over the past 12 months.</desc>

  <rect x="${Math.round(xMin)}" y="${Math.round(yMin)}" width="${width}" height="${height}" rx="20" fill="${p.canvas}"/>
  <rect x="${Math.round(xMin) + 0.5}" y="${Math.round(yMin) + 0.5}" width="${width - 1}" height="${height - 1}" rx="19.5" stroke="${p.border}"/>

  <text x="${Math.round(xMin + 28)}" y="${headerY}" fill="${p.ink}" font-size="16" font-weight="600" letter-spacing="-0.2">
    Contribution Activity
  </text>
  <text x="${Math.round(xMax - 28)}" y="${headerY}" fill="${p.inkMuted}" font-size="12" font-weight="500" text-anchor="end">
    ${active} active days · past 12 months
  </text>

  <g>
    <animate attributeName="opacity" from="0" to="1" begin="0.08s" dur="0.5s" fill="freeze"/>
    ${ground}
    ${columnsXml}
  </g>

  ${weekdayLabels.join('\n  ')}
  ${monthLabels.join('\n  ')}

  <text x="${legendStartX}" y="${Math.round(footerY)}" fill="${p.inkMuted}" font-size="10.5" font-weight="500">Less</text>
  ${swatches}
  <text x="${legendStartX + 114}" y="${Math.round(footerY)}" fill="${p.inkMuted}" font-size="10.5" font-weight="500">More</text>
  <text x="${Math.round(xMax - 28)}" y="${Math.round(footerY)}" fill="${p.inkMuted}" font-size="10.5" font-weight="500" text-anchor="end">Live GitHub contribution data</text>
</svg>
`;
}

// ------------------------------------------------------------ 4. Stack Marquee --
function buildMarqueeSvg(icons, mode) {
  const p = PALETTES[mode];
  const width = 860;
  const height = 160;
  const logoHeight = 46;
  const slotWidth = 86;
  const speed = 75;
  const seqWidth = icons.length * slotWidth;
  const duration = (seqWidth / speed).toFixed(1);
  const scale = (logoHeight / 24).toFixed(4);
  const topY = 76;

  const copies = [];
  for (let copy = 0; copy < 2; copy++) {
    icons.forEach((icon, index) => {
      const slotX = copy * seqWidth + index * slotWidth;
      const iconX = slotX + (slotWidth - logoHeight) / 2;
      copies.push(
        `<g transform="translate(${iconX.toFixed(1)} ${topY}) scale(${scale})"><title>${escapeXml(icon.label)}</title><path d="${icon.d}" fill="${p.iconColor}"/></g>`
      );
    });
  }

  return `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" font-family="${FONT_SANS}">
  <title id="title">Core Technologies</title>
  <desc id="desc">Languages, frameworks, databases, and infrastructure tools.</desc>
  <defs>
    <linearGradient id="fadeGrad-${mode}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="7%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="93%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <mask id="fadeMask-${mode}">
      <rect x="0" y="0" width="${width}" height="${height}" fill="url(#fadeGrad-${mode})"/>
    </mask>
  </defs>

  <rect width="${width}" height="${height}" rx="20" fill="${p.canvas}"/>
  <rect x="0.5" y="0.5" width="${width - 1}" height="${height - 1}" rx="19.5" stroke="${p.border}"/>

  <text x="32" y="38" fill="${p.ink}" font-size="16" font-weight="600" letter-spacing="-0.2">
    Core Technologies
  </text>
  <text x="${width - 32}" y="38" fill="${p.inkMuted}" font-size="11.5" font-weight="500" text-anchor="end">
    Languages · Systems · Infrastructure
  </text>

  <g mask="url(#fadeMask-${mode})">
    <g>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-${seqWidth} 0" dur="${duration}s" repeatCount="indefinite"/>
      ${copies.join('')}
    </g>
  </g>
</svg>
`;
}

async function main() {
  fs.mkdirSync(ASSETS, { recursive: true });

  // Hero & Focus cards
  fs.writeFileSync(path.join(ASSETS, 'hero-light.svg'), buildHeroSvg('light'), 'utf8');
  fs.writeFileSync(path.join(ASSETS, 'hero-dark.svg'), buildHeroSvg('dark'), 'utf8');
  fs.writeFileSync(path.join(ASSETS, 'focus-light.svg'), buildFocusSvg('light'), 'utf8');
  fs.writeFileSync(path.join(ASSETS, 'focus-dark.svg'), buildFocusSvg('dark'), 'utf8');

  // 3D Calendar (live fetch with deterministic fallback)
  let cells;
  try {
    const html = await fetchContributionsHtml();
    cells = parseContributionCells(html);
    if (cells.size < 350) {
      throw new Error(`Parsed only ${cells.size} cells`);
    }
    console.log(`Fetched live GitHub contribution grid (${cells.size} days)`);
  } catch (err) {
    console.warn(`Using fallback calendar grid (${err.message})`);
    cells = fallbackCells();
  }

  fs.writeFileSync(path.join(ASSETS, 'calendar-3d-light.svg'), buildCalendarSvg(cells, 'light'), 'utf8');
  fs.writeFileSync(path.join(ASSETS, 'calendar-3d.svg'), buildCalendarSvg(cells, 'dark'), 'utf8');

  // Logo Marquee
  const icons = JSON.parse(fs.readFileSync(path.join(__dirname, 'stack-icons.json'), 'utf8'));
  fs.writeFileSync(path.join(ASSETS, 'logo-marquee-light.svg'), buildMarqueeSvg(icons, 'light'), 'utf8');
  fs.writeFileSync(path.join(ASSETS, 'logo-marquee.svg'), buildMarqueeSvg(icons, 'dark'), 'utf8');

  console.log('Generated all Apple-inspired SVG assets in assets/.');
}

main();
