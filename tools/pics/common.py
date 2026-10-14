"""Общие детали схем для уроков: SVG на белом фоне, шрифты бренда, подписи с выносками, масштабные линейки, клетки.

Схемы рисуются в SVG (viewBox в пикселях), страница рендерится Chrome в PNG (tools/youtube/art.py::shot).
Цвета: чернила #151515, биология #1F7A4A, химия #F13A43, серый #8F897F.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools' / 'youtube')]
from art import shot  # noqa: E402

INK, GREEN, RED, GREY, PAPER = '#151515', '#1F7A4A', '#F13A43', '#8F897F', '#F3F0E8'
LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW = '#D9EEDF', '#DCEBF5', '#F7EFC8'
FONTS = (ROOT / 'content/brand/fonts').as_uri()

CSS = f"""
@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0400-045F; }}
@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-latin-wght-normal.woff2') format('woff2'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0400-045F; }}
@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-latin-wght-normal.woff2') format('woff2'); }}
html, body {{ margin: 0; background: #fff; }}
svg {{ display: block; }}
text {{ font-family: 'Manrope'; fill: {INK}; }}
.t {{ font-size: 30px; font-weight: 700; }}
.s {{ font-size: 25px; font-weight: 700; fill: #3B3833; }}
.h {{ font-family: 'Unbounded'; font-size: 34px; font-weight: 800; }}
.cap {{ font-size: 24px; font-weight: 700; fill: {GREY}; }}
"""


def render(svg: str, w: int, h: int, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    page = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body {{ width:{w}px; height:{h}px; }}</style></head>'
            f'<body><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{svg}</svg></body></html>')
    shot(page, w, h, out)


def text(x: float, y: float, s: str, cls: str = 't', anchor: str = 'start', fill: str | None = None) -> str:
    f = f' style="fill:{fill}"' if fill else ''
    return f'<text x="{x:.0f}" y="{y:.0f}" class="{cls}" text-anchor="{anchor}"{f}>{s}</text>'


def label(px: float, py: float, tx: float, ty: float, s: str, cls: str = 't', color: str = INK) -> str:
    """Выноска: точка на объекте (px, py), линия к подписи (tx, ty)."""
    anchor = 'end' if tx < px else 'start'
    dx = -8 if anchor == 'end' else 8
    return (f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{tx:.0f}" y2="{ty - 8:.0f}" stroke="{color}" stroke-width="2.5"/>'
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{color}"/>' + text(tx + dx, ty, s, cls, anchor))


def ruler(x: float, y: float, length: float, caption: str, color: str = INK) -> str:
    """Масштабная линейка: отрезок с засечками и подписью под ним."""
    return (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + length:.0f}" y2="{y:.0f}" stroke="{color}" stroke-width="6"/>'
            f'<line x1="{x:.0f}" y1="{y - 16:.0f}" x2="{x:.0f}" y2="{y + 16:.0f}" stroke="{color}" stroke-width="5"/>'
            f'<line x1="{x + length:.0f}" y1="{y - 16:.0f}" x2="{x + length:.0f}" y2="{y + 16:.0f}" stroke="{color}" stroke-width="5"/>'
            + text(x + length / 2, y + 50, caption, 't', 'middle'))


def elongated_cell(x: float, y: float, length: float, height: float = 110, fill: str = LIGHT_GREEN, stroke: str = GREEN,
                   nucleus: bool = True) -> str:
    """Вытянутая схематическая клетка от x до x+length (для задач на масштаб)."""
    r = height / 2
    nuc = (f'<ellipse cx="{x + length * 0.42:.0f}" cy="{y:.0f}" rx="{height * 0.32:.0f}" ry="{height * 0.24:.0f}" '
           f'fill="#B9DCC4" stroke="{stroke}" stroke-width="3"/>') if nucleus else ''
    return (f'<rect x="{x:.0f}" y="{y - r:.0f}" width="{length:.0f}" height="{height:.0f}" rx="{r:.0f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="5"/>' + nuc)


def ends(x1: float, x2: float, y: float, color: str = GREY) -> str:
    """Пунктирные вертикали — границы длины объекта."""
    return ''.join(f'<line x1="{x:.0f}" y1="{y - 90:.0f}" x2="{x:.0f}" y2="{y + 90:.0f}" stroke="{color}" stroke-width="2.5" '
                   f'stroke-dasharray="8 8"/>' for x in (x1, x2))


def mito(cx: float, cy: float, rx: float = 30, ry: float = 15, rot: float = 0) -> str:
    """Митохондрия: овал с кристами."""
    folds = ''.join(f'<path d="M{cx - rx * 0.7 + k * rx * 0.35:.0f} {cy - ry * 0.6:.0f} q {rx * 0.1:.0f} {ry * 0.6:.0f} 0 {ry * 1.2:.0f}" '
                    f'fill="none" stroke="#B4532A" stroke-width="2"/>' for k in range(5))
    return (f'<g transform="rotate({rot} {cx:.0f} {cy:.0f})"><ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx}" ry="{ry}" fill="#F6D2BF" '
            f'stroke="#B4532A" stroke-width="3"/>{folds}</g>')


def chloro(cx: float, cy: float, rx: float = 26, ry: float = 14, rot: float = 0) -> str:
    """Хлоропласт: зелёный овал со стопками тилакоидов."""
    stacks = ''.join(f'<line x1="{cx - rx * 0.6 + k * rx * 0.4:.0f}" y1="{cy - ry * 0.45:.0f}" x2="{cx - rx * 0.6 + k * rx * 0.4:.0f}" '
                     f'y2="{cy + ry * 0.45:.0f}" stroke="#0F4D2C" stroke-width="4"/>' for k in range(4))
    return (f'<g transform="rotate({rot} {cx:.0f} {cy:.0f})"><ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx}" ry="{ry}" fill="#5DAA6F" '
            f'stroke="#1F5E36" stroke-width="3"/>{stacks}</g>')


def ribosomes(points: list[tuple[float, float]]) -> str:
    return ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{INK}"/>' for x, y in points)


def dna_loop(cx: float, cy: float, r: float = 40) -> str:
    """Кольцевая ДНК бактерии — извитая петля."""
    pts = []
    for k in range(73):
        a = 2 * math.pi * k / 72
        rr = r + 7 * math.sin(7 * a)
        pts.append(f'{cx + rr * math.cos(a):.1f} {cy + 0.6 * rr * math.sin(a):.1f}')
    return f'<path d="M{" L".join(pts)} Z" fill="none" stroke="#3A57A7" stroke-width="4"/>'


def nucleus(cx: float, cy: float, r: float = 50) -> str:
    """Ядро с оболочкой и хроматином (ДНК)."""
    chrom = ''.join(f'<path d="M{cx - r * 0.5 + k * r * 0.25:.0f} {cy - r * 0.35:.0f} q {r * 0.2:.0f} {r * 0.3:.0f} 0 {r * 0.7:.0f}" '
                    f'fill="none" stroke="#3A57A7" stroke-width="3"/>' for k in range(5))
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="#E3E4F4" stroke="#3A57A7" stroke-width="4"/>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r - 7}" fill="none" stroke="#3A57A7" stroke-width="2" stroke-dasharray="6 5"/>' + chrom)


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = INK, w: float = 5) -> str:
    ang = math.atan2(y2 - y1, x2 - x1)
    a1, a2 = ang + 2.6, ang - 2.6
    head = f'{x2:.0f},{y2:.0f} {x2 + 22 * math.cos(a1):.0f},{y2 + 22 * math.sin(a1):.0f} {x2 + 22 * math.cos(a2):.0f},{y2 + 22 * math.sin(a2):.0f}'
    return (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2 - 14 * math.cos(ang):.0f}" y2="{y2 - 14 * math.sin(ang):.0f}" stroke="{color}" '
            f'stroke-width="{w}"/><polygon points="{head}" fill="{color}"/>')
