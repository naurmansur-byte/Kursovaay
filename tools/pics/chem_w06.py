"""Рисунки недели 6 химии (course/week-06/pics/*.png): модель атома, s- и p-орбитали, порядок заполнения, периодические тенденции.

Факты — по выжимке course/textbooks/chem-06-atom.md (Х8 § 1–4, 30–34; Х10-1 § 1–9). Схемы условные, масштаб не соблюдён.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w06.py
"""
from __future__ import annotations

import math

from common import GREY, INK, LIGHT_BLUE, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-06' / 'pics'
BLUE, LBLUE, NEUTRON, TINT, AMBER = '#3A57A7', '#C9D6F0', '#BDB6AA', '#FBE3E4', '#C79A1B'

DEFS = (f'<defs><radialGradient id="cloud"><stop offset="0" stop-color="{LBLUE}" stop-opacity=".95"/>'
        f'<stop offset=".7" stop-color="{LBLUE}" stop-opacity=".45"/><stop offset="1" stop-color="{LBLUE}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="ball" cx=".38" cy=".35"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".55"/></radialGradient></defs>')


def nuclide(x: float, y: float, sym: str, a: str, z: str, size: int = 64) -> str:
    """Запись нуклида: массовое число сверху, заряд снизу, слева от символа."""
    small = size * 0.5
    return (f'<text x="{x:.0f}" y="{y - size * 0.42:.0f}" text-anchor="end" style="font-size:{small:.0f}px;font-weight:800">{a}</text>'
            f'<text x="{x:.0f}" y="{y + size * 0.12:.0f}" text-anchor="end" style="font-size:{small:.0f}px;font-weight:800;fill:{RED}">{z}</text>'
            f'<text x="{x + 6:.0f}" y="{y:.0f}" style="font-size:{size}px;font-weight:800">{sym}</text>')


def atom_model() -> str:
    s = DEFS + text(700, 60, 'Модель атома: ядро и электронная оболочка', 'h', 'middle')
    cx, cy = 360, 470
    s += f'<circle cx="{cx}" cy="{cy}" r="290" fill="url(#cloud)"/>'
    for ang, r in ((20, 210), (140, 170), (250, 230), (350, 130), (80, 250), (200, 90), (290, 200), (170, 260), (40, 140)):
        x, y = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{BLUE}"/><text x="{x + 14:.0f}" y="{y - 8:.0f}" class="cap" style="fill:{BLUE}">e⁻</text>'
    # ядро: 9 p и 10 n
    pts = [(0, 0), (22, 4), (-20, 8), (6, -22), (-10, -18), (14, 24), (-18, -2), (28, -16), (-4, 26), (26, 14),
           (-28, 18), (10, -8), (-6, 12), (18, -28), (-24, -20), (34, 2), (-32, -6), (2, 36), (-14, 30)]
    for k, (dx, dy) in enumerate(pts):
        fill = RED if k % 2 == 0 else NEUTRON
        s += f'<circle cx="{cx + dx}" cy="{cy + dy}" r="15" fill="{fill}" stroke="#fff" stroke-width="2"/>'
    s += f'<path d="M{cx + 40} {cy - 30} L 620 250" stroke="{INK}" stroke-width="2.5"/>'
    s += text(630, 240, 'ядро: протоны p и нейтроны n', 's') + text(630, 272, 'почти вся масса атома — в ядре', 'cap')
    s += text(cx, 800, 'облако — где вероятнее найти электрон;', 'cap', 'middle') + text(cx, 830, 'точных траекторий нет, масштаб не соблюдён', 'cap', 'middle')
    # таблица частиц
    x0, y0 = 760, 330
    rows = [('частица', 'заряд', 'где'), ('протон p', '+1', 'ядро'), ('нейтрон n', '0', 'ядро'), ('электрон e⁻', '−1', 'оболочка')]
    colors = [None, RED, NEUTRON, BLUE]
    for i, row in enumerate(rows):
        y = y0 + i * 58
        if i:
            s += f'<circle cx="{x0 + 14}" cy="{y - 9}" r="12" fill="{colors[i]}"/>'
        for j, (cell, xo) in enumerate(zip(row, (40, 300, 420))):
            s += text(x0 + xo, y, cell, 'cap' if i == 0 else 't')
    s += f'<path d="M{x0} {y0 + 18} H {x0 + 600}" stroke="{GREY}" stroke-width="2"/>'
    # формулы
    s += f'<rect x="{x0}" y="590" width="600" height="250" rx="16" fill="{PAPER}"/>'
    s += nuclide(x0 + 90, 680, 'F', '19', '9', 72)
    s += text(x0 + 180, 650, 'A = 19 — массовое число (p + n)', 's') + text(x0 + 180, 690, 'Z = 9 — заряд ядра, число p', 's', fill=RED)
    s += text(x0 + 40, 760, 'N = A − Z = 19 − 9 = 10 нейтронов', 't')
    s += text(x0 + 40, 805, 'атом нейтрален: e = p = 9', 't')
    return s


def lobe_pair(cx: float, cy: float, ang: float, length: float = 120, width: float = 52) -> str:
    """p-орбиталь: две «капли» навстречу от ядра под углом ang."""
    out = ''
    for sign in (1, -1):
        a = math.radians(ang)
        ex, ey = cx + sign * length * math.cos(a), cy + sign * length * math.sin(a)
        nx, ny = -math.sin(a) * width, math.cos(a) * width
        mx, my = cx + sign * length * 0.55 * math.cos(a), cy + sign * length * 0.55 * math.sin(a)
        out += (f'<path d="M{cx} {cy} C {mx + nx:.0f} {my + ny:.0f} {ex + nx * 0.9:.0f} {ey + ny * 0.9:.0f} {ex:.0f} {ey:.0f} '
                f'C {ex - nx * 0.9:.0f} {ey - ny * 0.9:.0f} {mx - nx:.0f} {my - ny:.0f} {cx} {cy} Z" fill="url(#ball)" stroke="{BLUE}" stroke-width="3"/>')
    return out


def axes(cx: float, cy: float, r: float = 150) -> str:
    s = ''
    for (dx, dy, name) in ((1, 0, 'x'), (0, -1, 'y'), (-0.62, 0.62, 'z')):
        s += f'<path d="M{cx - dx * r:.0f} {cy - dy * r:.0f} L {cx + dx * r:.0f} {cy + dy * r:.0f}" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 6"/>'
        s += text(cx + dx * (r + 18), cy + dy * (r + 18) + 8, name, 'cap', 'middle')
    return s


def sp_orbitals() -> str:
    s = DEFS + text(800, 60, 'Формы орбиталей: s — шар, p — гантели', 'h', 'middle')
    panels = [('s', None, 's-орбиталь: шар'), ('px', 0, 'pₓ — вдоль x'), ('py', 90, 'p_y — вдоль y'), ('pz', 135, 'p_z — вдоль z')]
    for k, (name, ang, cap) in enumerate(panels):
        cx, cy = 200 + k * 400, 330
        s += axes(cx, cy)
        if ang is None:
            s += f'<circle cx="{cx}" cy="{cy}" r="95" fill="url(#ball)" stroke="{BLUE}" stroke-width="3"/>'
        else:
            s += lobe_pair(cx, cy, ang)
        s += f'<circle cx="{cx}" cy="{cy}" r="6" fill="{RED}"/>'
        label = {'s': 's-орбиталь — шар', 'px': 'p-орбиталь вдоль x', 'py': 'p-орбиталь вдоль y', 'pz': 'p-орбиталь вдоль z'}[name]
        s += text(cx, 540, label, 't', 'middle')
    s += text(200, 580, '1 орбиталь на подуровне', 'cap', 'middle') + text(1000, 580, '3 орбитали на p-подуровне, одинаковые по энергии', 'cap', 'middle')
    s += f'<rect x="40" y="610" width="1520" height="70" rx="14" fill="{PAPER}"/>'
    s += text(800, 655, 'Орбиталь — область, где электрон находится с вероятностью около 90 %. Это не путь движения.', 's', 'middle')
    return s


def cell_box(x: float, y: float, arrows: str, w: int = 56) -> str:
    """Клетка орбитали со стрелками: '' / 'u' / 'ud'."""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{w}" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    if 'u' in arrows:
        ax = x + (w * 0.36 if 'd' in arrows else w / 2)
        s += f'<path d="M{ax} {y + w - 10} V {y + 12} M{ax - 8} {y + 22} L {ax} {y + 12} L {ax + 8} {y + 22}" stroke="{RED}" stroke-width="4" fill="none"/>'
    if 'd' in arrows:
        ax = x + w * 0.64
        s += f'<path d="M{ax} {y + 10} V {y + w - 12} M{ax - 8} {y + w - 22} L {ax} {y + w - 12} L {ax + 8} {y + w - 22}" stroke="{BLUE}" stroke-width="4" fill="none"/>'
    return s


def filling_order() -> str:
    s = text(800, 60, 'Порядок заполнения подуровней', 'h', 'middle')
    seq = [('1s', 1, 0), ('2s', 2, 0), ('2p', 2, 1), ('3s', 3, 0), ('3p', 3, 1), ('4s', 4, 0), ('3d', 3, 2), ('4p', 4, 1)]
    x0, y0, w, gap = 60, 120, 150, 41
    for k, (name, n, l) in enumerate(seq):
        x = x0 + k * (w + gap)
        hot = name in ('4s', '3d')
        s += f'<rect x="{x}" y="{y0}" width="{w}" height="110" rx="16" fill="{TINT if hot else PAPER}" stroke="{RED if hot else INK}" stroke-width="{4 if hot else 3}"/>'
        s += f'<text x="{x + w / 2}" y="{y0 + 66}" text-anchor="middle" style="font-size:48px;font-weight:800">{name}</text>'
        s += text(x + w / 2, y0 + 150, f'n + l = {n + l}', 's', 'middle', RED if hot else None)
        if k < len(seq) - 1:
            s += arrow(x + w + 4, y0 + 55, x + w + gap - 4, y0 + 55, INK, 4)
    s += text(800, 330, '4s (4 + 0 = 4) заполняется раньше 3d (3 + 2 = 5)', 't', 'middle', RED)
    # три правила
    cards = [('Принцип Паули', 'на орбитали не больше', 'двух электронов', 'с противоположными спинами'),
             ('Правило Хунда', 'на подуровне электроны сначала', 'занимают свободные орбитали', 'по одному, спины параллельны'),
             ('Правило Клечковского', 'подуровни заполняются', 'по росту суммы n + l;', 'при равной сумме — меньшее n')]
    for k, (title, *lines) in enumerate(cards):
        x = 60 + k * 500
        s += f'<rect x="{x}" y="390" width="460" height="400" rx="18" fill="#fff" stroke="{INK}" stroke-width="3"/>'
        s += text(x + 230, 440, title, 't', 'middle')
        s += ''.join(text(x + 230, 485 + j * 34, ln, 's', 'middle') for j, ln in enumerate(lines))
    # Паули: верно / неверно
    s += cell_box(150, 640, 'ud') + text(178, 730, 'верно', 'cap', 'middle')
    s += cell_box(330, 640, 'u') + f'<path d="M{330 + 36} 650 V 686 M{358} 660 L {366} 650 L {374} 660" stroke="{RED}" stroke-width="4" fill="none"/>'
    s += f'<path d="M318 628 L 398 708 M398 628 L 318 708" stroke="{GREY}" stroke-width="4"/>' + text(358, 730, 'два ↑ — нельзя', 'cap', 'middle')
    # Хунд: кислород 2p⁴
    s += text(790, 620, chem('O: 1s²2s²2p⁴'), 't', 'middle')
    for j, a in enumerate(('ud', 'u', 'u')):
        s += cell_box(706 + j * 56, 650, a)
    s += text(790, 740, 'два одиночных ↑ — параллельно', 'cap', 'middle')
    # Клечковский: пары с равной суммой
    s += text(1290, 640, '3p: 3 + 1 = 4', 't', 'middle') + text(1290, 680, '4s: 4 + 0 = 4', 't', 'middle')
    s += text(1290, 730, 'сумма равна → 3p раньше', 'cap', 'middle')
    return s


TABLE = [['H', '', '', '', '', '', '', 'He'],
         ['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne'],
         ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar'],
         ['K', 'Ca', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'],
         ['Rb', 'Sr', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe'],
         ['Cs', 'Ba', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'],
         ['Fr', 'Ra', '', '', '', '', '', '']]


def periodic_trends() -> str:
    s = text(800, 60, 'Периодические тенденции (главные подгруппы)', 'h', 'middle')
    x0, y0, c = 300, 170, 82
    groups = ['IA', 'IIA', 'IIIA', 'IVA', 'VA', 'VIA', 'VIIA', 'VIIIA']
    for j, g in enumerate(groups):
        s += text(x0 + j * c + c / 2, y0 - 14, g, 'cap', 'middle')
    for i, row in enumerate(TABLE):
        s += text(x0 - 16, y0 + i * c + c / 2 + 9, str(i + 1), 'cap', 'end')
        for j, el in enumerate(row):
            if not el:
                continue
            fill = '#FFE0C2' if el == 'Fr' else ('#D9E3F7' if el == 'F' else '#fff')
            s += f'<rect x="{x0 + j * c}" y="{y0 + i * c}" width="{c - 6}" height="{c - 6}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
            s += text(x0 + j * c + (c - 6) / 2, y0 + i * c + c / 2 + 6, el, 't', 'middle')
    # стрелка по периоду
    right = x0 + 8 * c
    s += arrow(x0, 110, right - 10, 110, RED, 6)
    s += text(right + 20, 92, 'в периоде слева направо:', 's') + text(right + 20, 124, 'радиус ↓, металличность ↓,', 's') + text(right + 20, 156, 'энергия ионизации ↑', 's')
    # стрелка по группе
    bottom = y0 + 7 * c
    s += arrow(250, y0, 250, bottom - 10, BLUE, 6)
    s += text(230, 300, 'в группе', 's', 'end') + text(230, 332, 'сверху вниз:', 's', 'end')
    s += text(230, 380, 'радиус ↑', 's', 'end', BLUE) + text(230, 412, 'металличность ↑', 's', 'end', BLUE) + text(230, 444, 'энергия', 's', 'end', BLUE) + text(230, 476, 'ионизации ↓', 's', 'end', BLUE)
    for k, (fill, cap) in enumerate((('#D9E3F7', 'F — самый неметаллический'), ('#FFE0C2', 'Fr — самый металлический'))):
        y = y0 + 3 * c + k * 56
        s += f'<rect x="{right + 20}" y="{y}" width="36" height="36" rx="6" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        s += text(right + 70, y + 27, cap, 's')
    # оксиды 3-го периода
    yb = bottom + 70
    s += text(800, yb, 'Высшие оксиды 3-го периода: характер меняется слева направо', 't', 'middle')
    ox = [('Na₂O', 'основный', '#D9E3F7'), ('MgO', 'основный', '#D9E3F7'), ('Al₂O₃', 'амфотерный', '#F7EFC8'), ('SiO₂', 'кислотный', TINT),
          ('P₂O₅', 'кислотный', TINT), ('SO₃', 'кислотный', TINT), ('Cl₂O₇', 'кислотный', TINT)]
    w = 196
    for k, (f, kind, fill) in enumerate(ox):
        x = 60 + k * (w + 10)
        s += f'<rect x="{x}" y="{yb + 24}" width="{w}" height="110" rx="14" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        s += text(x + w / 2, yb + 74, chem(f), 'f', 'middle') + text(x + w / 2, yb + 116, kind, 's', 'middle')
    s += text(800, yb + 180, 'Это общие тенденции, есть исключения: например, энергия ионизации Al меньше, чем у Mg.', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'atom-model.png': (atom_model(), 1400, 880),
        's-p-orbitals.png': (sp_orbitals(), 1600, 710),
        'filling-order.png': (filling_order(), 1600, 830),
        'periodic-trends.png': (periodic_trends(), 1600, 1030),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
