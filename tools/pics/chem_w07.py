"""Рисунки недели 7 химии (course/week-07/pics/*.png): ЭО, механизмы ковалентной связи, σ и π, формы молекул, решётки, водородная связь.

Факты — по выжимке course/textbooks/chem-07-bonds.md (Х8 § 35–39; Х10-1 § 10–18). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w07.py
"""
from __future__ import annotations

import math

from common import GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-07' / 'pics'
BLUE, LBLUE, TINT, AMBER = '#3A57A7', '#DCE6F5', '#FBE3E4', '#C79A1B'


def atom(x, y, sym, r=34, fill='#fff', stroke=INK, size=32):
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            f'<text x="{x:.0f}" y="{y + size * 0.35:.0f}" text-anchor="middle" style="font-size:{size}px;font-weight:800">{chem(sym)}</text>')


def bond(x1, y1, x2, y2, r1=34, r2=34, w=6, dash=False, color=INK):
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    da = ' stroke-dasharray="10 9"' if dash else ''
    return f'<path d="M{x1 + ux * r1:.0f} {y1 + uy * r1:.0f} L {x2 - ux * r2:.0f} {y2 - uy * r2:.0f}" stroke="{color}" stroke-width="{w}"{da}/>'


def dots(x, y, n=2, color=RED, gap=14):
    return ''.join(f'<circle cx="{x + (k - (n - 1) / 2) * gap:.0f}" cy="{y:.0f}" r="6" fill="{color}"/>' for k in range(n))


# 1. ЭО ------------------------------------------------------------------------------------------
EO = [[('H', 2.1)],
      [('Li', 1.0), ('Be', 1.5), ('B', 2.0), ('C', 2.5), ('N', 3.0), ('O', 3.5), ('F', 4.0)],
      [('Na', 0.9), ('Mg', 1.2), ('Al', 1.5), ('Si', 1.8), ('P', 2.2), ('S', 2.5), ('Cl', 3.0)],
      [('K', 0.8), ('Ca', 1.0), None, None, None, ('Se', 2.4), ('Br', 2.8)]]


def eo_color(v):
    a = (v - 0.7) / 3.3
    r, g, b = (int(255 - (255 - c) * (0.15 + 0.85 * a)) for c in (241, 58, 67))
    return f'#{r:02X}{g:02X}{b:02X}'


def eo_trends() -> str:
    s = text(800, 56, 'Электроотрицательность (шкала Полинга)', 'h', 'middle')
    x0, y0, c = 240, 150, 130
    for i, row in enumerate(EO):
        for j, cell in enumerate(row):
            if not cell:
                continue
            el, v = cell
            x, y = x0 + j * c, y0 + i * c
            s += f'<rect x="{x}" y="{y}" width="{c - 10}" height="{c - 10}" rx="12" fill="{eo_color(v)}" stroke="{INK}" stroke-width="2"/>'
            s += f'<text x="{x + (c - 10) / 2}" y="{y + 56}" text-anchor="middle" style="font-size:40px;font-weight:800">{el}</text>'
            s += text(x + (c - 10) / 2, y + 96, f'{v:.1f}'.replace('.', ','), 't', 'middle')
    right = x0 + 7 * c
    s += arrow(x0, y0 + 4 * c + 20, right - 20, y0 + 4 * c + 20, RED, 7)
    s += text((x0 + right) / 2, y0 + 4 * c + 64, 'в периоде слева направо ЭО растёт', 't', 'middle', RED)
    s += arrow(x0 - 50, y0 + 4 * c - 20, x0 - 50, y0 + 10, RED, 7)
    s += f'<text x="{x0 - 80}" y="{y0 + 2 * c}" text-anchor="middle" transform="rotate(-90 {x0 - 80} {y0 + 2 * c})" style="font-size:30px;font-weight:700;fill:{RED}">в группе снизу вверх</text>'
    bx = right + 40
    s += f'<rect x="{bx}" y="{y0}" width="420" height="{3 * c - 10}" rx="16" fill="{PAPER}"/>'
    rows = [('F — максимум, 4,0', 't', None), ('металлы < 2', 's', None), ('неметаллы > 2', 's', None),
            ('Полярность связи —', 't', None), ('по разности ЭО:', 't', None), ('S–Cl: 3,0 − 2,5 = 0,5', 's', None),
            ('S–O: 3,5 − 2,5 = 1,0', 's', None), ('S–O полярнее', 's', RED)]
    for k, (t, cls, col) in enumerate(rows):
        s += text(bx + 24, y0 + 50 + k * 42 + (24 if k >= 3 else 0), t, cls, fill=col)
    return s


# 2. Механизмы -----------------------------------------------------------------------------------
def bond_mechanisms() -> str:
    s = text(800, 56, 'Как образуется ковалентная связь', 'h', 'middle')
    # обменный: H2
    s += text(270, 130, 'Обменный механизм', 't', 'middle')
    s += atom(120, 230, 'H') + dots(165, 230, 1) + text(205, 242, '+', 't', 'middle') + dots(245, 230, 1, BLUE) + atom(290, 230, 'H')
    s += arrow(340, 230, 390, 230, INK, 4)
    s += atom(430, 230, 'H') + atom(530, 230, 'H') + f'<ellipse cx="480" cy="230" rx="22" ry="16" fill="{TINT}" stroke="{RED}" stroke-width="2"/>' + dots(480, 230, 2, RED, 12)
    s += text(480, 300, 'H₂: пара общая, поровну', 'cap', 'middle')
    # HCl
    s += atom(120, 400, 'H') + dots(165, 400, 1) + text(205, 412, '+', 't', 'middle') + dots(245, 400, 1, BLUE) + atom(295, 400, 'Cl', 40)
    s += arrow(350, 400, 400, 400, INK, 4)
    s += atom(440, 400, 'H') + atom(550, 400, 'Cl', 40) + f'<ellipse cx="502" cy="400" rx="20" ry="16" fill="{TINT}" stroke="{RED}" stroke-width="2"/>' + dots(502, 400, 2, RED, 12)
    s += text(440, 352, 'δ+', 's', 'middle', BLUE) + text(550, 346, 'δ−', 's', 'middle', RED)
    s += text(495, 475, 'HCl: пара смещена к Cl', 'cap', 'middle')
    s += text(330, 540, 'каждый атом даёт по одному электрону', 's', 'middle')
    # донорно-акцепторный: NH4+
    bx = 820
    s += text(bx + 320, 130, 'Донорно-акцепторный механизм', 't', 'middle')
    cx, cy = bx + 120, 300
    s += atom(cx, cy, 'N', 40)
    for ang in (150, 210, 270):
        hx, hy = cx + 110 * math.cos(math.radians(ang)), cy + 110 * math.sin(math.radians(ang))
        s += bond(cx, cy, hx, hy, 40, 30) + atom(hx, hy, 'H', 30, size=28)
    s += dots(cx + 60, cy, 2, RED, 14) + text(cx + 64, cy + 44, 'пара N', 'cap', 'middle', RED)
    s += text(cx + 140, cy + 12, '+', 'f', 'middle')
    s += atom(cx + 230, cy, 'H⁺', 34, size=28) + f'<rect x="{cx + 272}" y="{cy - 18}" width="36" height="36" fill="#fff" stroke="{BLUE}" stroke-width="3"/>'
    s += text(cx + 290, cy + 60, 'свободная', 'cap', 'middle', BLUE) + text(cx + 290, cy + 86, 'орбиталь', 'cap', 'middle', BLUE)
    s += text(cx + 60, cy + 150, 'донор (NH₃)', 's', 'middle') + text(cx + 250, cy + 150, 'акцептор (H⁺)', 's', 'middle')
    s += arrow(bx + 330, cy + 200, bx + 330, cy + 250, INK, 4)
    # NH4+
    nx, ny = bx + 250, 650
    s += atom(nx, ny, 'N', 40)
    for ang in (0, 90, 180, 270):
        hx, hy = nx + 110 * math.cos(math.radians(ang)), ny + 90 * math.sin(math.radians(ang))
        s += bond(nx, ny, hx, hy, 40, 30) + atom(hx, hy, 'H', 30, size=28)
    s += f'<path d="M{nx - 175} {ny - 130} q -20 130 0 260 M{nx + 175} {ny - 130} q 20 130 0 260" fill="none" stroke="{INK}" stroke-width="4"/>'
    s += text(nx + 200, ny - 110, '+', 't')
    s += text(nx + 230, ny - 20, 'все 4 связи', 't') + text(nx + 230, ny + 20, 'N–H равноценны', 't')
    return s


# 3. σ и π ---------------------------------------------------------------------------------------
def lobe(cx, cy, ang, L=90, W=34, fill=LBLUE, stroke=BLUE, op='0.85'):
    a = math.radians(ang)
    ex, ey = cx + L * math.cos(a), cy + L * math.sin(a)
    nx, ny = -math.sin(a) * W, math.cos(a) * W
    mx, my = cx + L * 0.55 * math.cos(a), cy + L * 0.55 * math.sin(a)
    return (f'<path d="M{cx} {cy} C {mx + nx:.0f} {my + ny:.0f} {ex + nx * 0.9:.0f} {ey + ny * 0.9:.0f} {ex:.0f} {ey:.0f} '
            f'C {ex - nx * 0.9:.0f} {ey - ny * 0.9:.0f} {mx - nx:.0f} {my - ny:.0f} {cx} {cy} Z" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="3"/>')


def sigma_pi() -> str:
    s = text(800, 56, 'σ- и π-связи', 'h', 'middle')
    # σ: лобовое перекрывание
    y = 220
    s += text(380, 130, 'σ — перекрывание вдоль линии ядер', 't', 'middle')
    s += f'<path d="M140 {y} H 620" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 8"/>'
    s += lobe(260, y, 180, 70, 30) + lobe(260, y, 0, 110, 36) + lobe(500, y, 0, 70, 30) + lobe(500, y, 180, 110, 36)
    s += f'<ellipse cx="380" cy="{y}" rx="34" ry="22" fill="{RED}" fill-opacity=".55"/>'
    s += f'<circle cx="260" cy="{y}" r="7" fill="{INK}"/><circle cx="500" cy="{y}" r="7" fill="{INK}"/>'
    s += text(380, y + 80, 'область перекрывания — на оси', 'cap', 'middle')
    # π: боковое
    s += text(1180, 130, 'π — боковое перекрывание', 't', 'middle')
    y2 = 230
    s += f'<path d="M940 {y2} H 1420" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 8"/>'
    for x in (1100, 1260):
        s += lobe(x, y2, 270, 90, 34) + lobe(x, y2, 90, 90, 34)
        s += f'<circle cx="{x}" cy="{y2}" r="7" fill="{INK}"/>'
    s += f'<ellipse cx="1180" cy="{y2 - 60}" rx="40" ry="22" fill="{RED}" fill-opacity=".5"/><ellipse cx="1180" cy="{y2 + 60}" rx="40" ry="22" fill="{RED}" fill-opacity=".5"/>'
    s += text(1180, y2 + 140, 'две области — выше и ниже оси', 'cap', 'middle')
    # кратность
    rows = [('одинарная', 'H–H, C–C', '1σ'), ('двойная', 'O=O, C=C', '1σ + 1π'), ('тройная', 'N≡N, C≡C', '1σ + 2π')]
    for k, (name, ex, comp) in enumerate(rows):
        x = 120 + k * 470
        s += f'<rect x="{x}" y="430" width="420" height="200" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        s += text(x + 210, 480, name, 't', 'middle') + text(x + 210, 530, chem(ex), 's', 'middle')
        s += f'<text x="{x + 210}" y="595" text-anchor="middle" style="font-size:44px;font-weight:800;fill:{RED}">{comp}</text>'
    s += text(800, 690, 'В кратной связи σ всегда одна, остальные — π.', 't', 'middle')
    return s


# 4. Формы молекул -------------------------------------------------------------------------------
def lone_pair(x, y, ang):
    a = math.radians(ang)
    px, py = x + 70 * math.cos(a), y + 70 * math.sin(a)
    s = lobe(x, y, ang, 75, 26, '#F7EFC8', AMBER, '0.9')
    return s + dots(px - 8 * math.cos(a), py - 8 * math.sin(a), 2, AMBER, 12)


def hybrid_shapes() -> str:
    s = text(800, 56, 'Гибридизация и форма молекул', 'h', 'middle')
    panels = [('BeCl₂, CO₂', 'sp — линейная', '180°'), ('BF₃', 'sp² — треугольник', '120°'), ('CH₄', 'sp³ — тетраэдр', '109°28′'),
              ('NH₃', 'sp³ — пирамида', '≈ 107°'), ('H₂O', 'sp³ — угловая', '≈ 104,5°')]
    for k, (f, kind, angle) in enumerate(panels):
        cx, cy = 160 + k * 320, 330
        if k == 0:
            s += atom(cx, cy, 'Be', 32, size=26) + bond(cx, cy, cx - 110, cy, 32, 30) + bond(cx, cy, cx + 110, cy, 32, 30)
            s += atom(cx - 110, cy, 'Cl', 30, size=24) + atom(cx + 110, cy, 'Cl', 30, size=24)
        elif k == 1:
            for ang in (-90, 30, 150):
                hx, hy = cx + 110 * math.cos(math.radians(ang)), cy + 110 * math.sin(math.radians(ang))
                s += bond(cx, cy, hx, hy, 32, 30) + atom(hx, hy, 'F', 30, size=26)
            s += atom(cx, cy, 'B', 32, size=28)
        elif k == 2:
            pts = [(0, -115), (-100, 55), (100, 55), (55, 100)]
            for j, (dx, dy) in enumerate(pts):
                s += bond(cx, cy, cx + dx, cy + dy, 32, 26, dash=(j == 3)) + atom(cx + dx, cy + dy, 'H', 26, size=24)
            s += atom(cx, cy, 'C', 32, size=28)
        elif k == 3:
            s += lone_pair(cx, cy, -90)
            for dx, dy in ((-100, 60), (100, 60), (0, 105)):
                s += bond(cx, cy, cx + dx, cy + dy, 32, 26) + atom(cx + dx, cy + dy, 'H', 26, size=24)
            s += atom(cx, cy, 'N', 32, size=28)
        else:
            s += lone_pair(cx, cy, -125) + lone_pair(cx, cy, -55)
            for dx, dy in ((-95, 70), (95, 70)):
                s += bond(cx, cy, cx + dx, cy + dy, 32, 26) + atom(cx + dx, cy + dy, 'H', 26, size=24)
            s += atom(cx, cy, 'O', 32, size=28)
        s += text(cx, 560, chem(f), 't', 'middle') + text(cx, 600, kind, 's', 'middle')
        s += f'<text x="{cx}" y="650" text-anchor="middle" style="font-size:38px;font-weight:800;fill:{RED}">{angle}</text>'
    s += f'<rect x="980" y="690" width="600" height="70" rx="14" fill="#FFF8E1" stroke="{AMBER}" stroke-width="2"/>'
    s += text(1280, 735, 'неподелённые пары сжимают угол', 's', 'middle', AMBER)
    s += text(500, 735, 'у CH₄ все четыре связи равноценны', 's', 'middle')
    return s


# 5. Решётки -------------------------------------------------------------------------------------
def lattice_types() -> str:
    s = text(800, 56, 'Четыре типа кристаллических решёток', 'h', 'middle')
    titles = [('Ионная', 'NaCl, NaF, CaO', ['в узлах — ионы', 'твёрдые, тугоплавкие', 'расплав и раствор', 'проводят ток']),
              ('Атомная', 'алмаз, графит, SiO₂', ['в узлах — атомы', 'ковалентная сеть', 'очень твёрдые,', 'тугоплавкие']),
              ('Молекулярная', 'лёд, CO₂, I₂', ['в узлах — молекулы', 'между ними — слабые', 'силы; летучие,', 'легкоплавкие']),
              ('Металлическая', 'Na, Fe, Al, Cu', ['ионы и атомы металла', '+ свободные электроны', 'проводят ток и тепло,', 'ковкие, блестят'])]
    for k, (title, ex, rows) in enumerate(titles):
        x = 40 + k * 390
        s += f'<rect x="{x}" y="110" width="370" height="760" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += text(x + 185, 160, title, 't', 'middle') + text(x + 185, 198, chem(ex), 's', 'middle', GREY)
        gx, gy = x + 65, 250
        for i in range(4):
            for j in range(4):
                px, py = gx + j * 80, gy + i * 80
                if k == 0:
                    plus = (i + j) % 2 == 0
                    s += f'<circle cx="{px}" cy="{py}" r="{22 if plus else 30}" fill="{TINT if plus else LBLUE}" stroke="{RED if plus else BLUE}" stroke-width="3"/>'
                    s += text(px, py + 9, '+' if plus else '−', 't', 'middle', RED if plus else BLUE)
                elif k == 1:
                    if j < 3:
                        s += f'<path d="M{px} {py} H {px + 80}" stroke="{INK}" stroke-width="4"/>'
                    if i < 3:
                        s += f'<path d="M{px} {py} V {py + 80}" stroke="{INK}" stroke-width="4"/>'
                    s += f'<circle cx="{px}" cy="{py}" r="14" fill="{GREY}"/>'
                elif k == 2:
                    if (i + j) % 2 == 0:
                        s += (f'<path d="M{px - 28} {py} H {px + 28}" stroke="{INK}" stroke-width="3"/>'
                              f'<circle cx="{px - 28}" cy="{py}" r="12" fill="{RED}"/><circle cx="{px}" cy="{py}" r="12" fill="{INK}"/><circle cx="{px + 28}" cy="{py}" r="12" fill="{RED}"/>')
                else:
                    s += f'<circle cx="{px}" cy="{py}" r="24" fill="{LBLUE}" stroke="{BLUE}" stroke-width="3"/>' + text(px, py + 9, '+', 't', 'middle', BLUE)
        if k == 3:
            for i in range(9):
                ex_, ey_ = gx + 40 + (i * 53) % 240, gy + 40 + (i * 97) % 240
                s += f'<circle cx="{ex_}" cy="{ey_}" r="6" fill="{RED}"/>'
            s += text(x + 185, 590, 'e⁻ — «электронный газ»', 'cap', 'middle', RED)
        if k == 2:
            s += text(x + 185, 590, 'молекулы CO₂', 'cap', 'middle')
        for j, r in enumerate(rows):
            s += text(x + 185, 660 + j * 36, chem(r), 's', 'middle')
    return s


# 6. Водородная связь ----------------------------------------------------------------------------
def water(ox, oy, h1, h2):
    s = ''
    for hx, hy in (h1, h2):
        s += bond(ox, oy, hx, hy, 38, 26, 6) + atom(hx, hy, 'H', 26, size=26)
        s += text(hx, hy - 36, 'δ+', 's', 'middle', BLUE)
    s += atom(ox, oy, 'O', 38, size=32) + text(ox - 46, oy - 40, 'δ−', 's', 'middle', RED)
    return s


def hydrogen_bonds() -> str:
    s = text(600, 56, 'Водородная связь между молекулами воды', 'h', 'middle')
    o1 = (300, 380)
    h1a, h1b = (300 + 100, 380 + 40), (300 - 40, 380 + 100)
    s += water(*o1, h1a, h1b)
    o2 = (640, 330)
    s += lone_pair(*o2, 160).replace('fill-opacity="0.9"', 'fill-opacity="0.6"')
    s += water(*o2, (640 + 70, 330 - 80), (640 + 90, 330 + 60))
    s += bond(h1a[0], h1a[1], o2[0], o2[1], 26, 38, 5, dash=True, color=RED)
    s += text(500, 470, 'водородная связь', 't', 'middle', RED) + text(500, 506, '(между молекулами, слабая)', 'cap', 'middle', RED)
    s += text(300, 560, 'O–H внутри молекулы —', 's', 'middle') + text(300, 592, 'ковалентная полярная', 's', 'middle')
    s += f'<rect x="760" y="520" width="400" height="140" rx="14" fill="{PAPER}"/>'
    s += text(960, 566, 'H, связанный с F, O или N,', 's', 'middle') + text(960, 600, 'притягивается к F, O, N', 's', 'middle') + text(960, 634, 'другой молекулы', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'eo-trends.png': (eo_trends(), 1600, 820),
        'bond-mechanisms.png': (bond_mechanisms(), 1600, 820),
        'sigma-pi.png': (sigma_pi(), 1600, 730),
        'hybrid-shapes.png': (hybrid_shapes(), 1600, 790),
        'lattice-types.png': (lattice_types(), 1600, 900),
        'hydrogen-bonds.png': (hydrogen_bonds(), 1200, 700),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
