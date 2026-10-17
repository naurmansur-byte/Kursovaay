"""Рисунки недели 12 биологии (course/biology/week-12/pics/*.png): строение хромосомы, типы хромосом, кариотип человека,
клеточный цикл, фазы митоза, фазы мейоза, кроссинговер, гаметогенез с n/c.

Факты — по выжимке course/textbooks/bio-12-cell-division.md (Б9 § 30–32; Б10-1 § 24; Б10-2 с. 4–13; Б11-1 § 27–28). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w12.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, label, render, text

OUT = ROOT / 'course' / 'biology' / 'week-12' / 'pics'
MOM, DAD, BLUE, ORANGE = '#E0656B', '#4A6FC7', '#3A57A7', '#D98A2B'
CELL, NUC = '#FBF6EE', '#F1E7F3'


def lbl(px, py, tx, ty, s, color=INK):
    return label(px, py, tx, ty, chem(s), 's', color)


def lines_at(x, y, rows, cls='s', anchor='middle', step=32, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER, stroke=None):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"{st}/>'


def bar(x, top, L, color, w):
    return f'<rect x="{x - w / 2:.1f}" y="{top:.1f}" width="{w}" height="{L}" rx="{w / 2:.1f}" fill="{color}"/>'


def chrom(cx, cy, L, color, frac=0.4, rep=True, ang=0, w=14, gap=3):
    """Хромосома с центром (cx, cy): rep=True — две сестринские хроматиды, иначе одна."""
    top = cy - L / 2
    yc = top + frac * L
    if rep:
        d = w / 2 + gap / 2
        body = bar(cx - d, top, L, color, w) + bar(cx + d, top, L, color, w)
        body += f'<ellipse cx="{cx}" cy="{yc:.1f}" rx="{w + gap / 2:.1f}" ry="{w * 0.45:.1f}" fill="{INK}" opacity=".55"/>'
    else:
        body = bar(cx, top, L, color, w) + f'<ellipse cx="{cx}" cy="{yc:.1f}" rx="{w * 0.62:.1f}" ry="{w * 0.4:.1f}" fill="{INK}" opacity=".55"/>'
    return f'<g transform="rotate({ang} {cx} {cy})">{body}</g>' if ang else body


def cellbody(cx, cy, rx, ry, nucleus=False, nr=0):
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{CELL}" stroke="{INK}" stroke-width="3"/>'
    if nucleus:
        s += f'<circle cx="{cx}" cy="{cy}" r="{nr}" fill="{NUC}" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
    return s


def spindle(px, py, targets, color=GREY):
    return ''.join(f'<line x1="{px}" y1="{py}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{color}" stroke-width="2"/>' for tx, ty in targets)


def pole(x, y):
    return f'<circle cx="{x}" cy="{y}" r="7" fill="{INK}"/>'


# 1. Строение хромосомы -----------------------------------------------------------------------
def chromosome_structure() -> str:
    s = text(800, 50, 'Строение хромосомы после репликации', 'h', 'middle')
    cx, cy, L, w = 380, 380, 440, 46
    top = cy - L / 2
    yc = top + 0.38 * L
    s += bar(cx - 26, top, L, MOM, w) + bar(cx + 26, top, L, MOM, w)
    s += f'<ellipse cx="{cx}" cy="{yc}" rx="54" ry="20" fill="{INK}" opacity=".55"/>'
    for yy in (top + 8, top + L - 8):
        s += f'<rect x="{cx - 50}" y="{yy - 8}" width="100" height="16" rx="8" fill="{ORANGE}"/>'
    s += lbl(cx - 26, top + L - 40, 250, top + L + 40, 'хроматида')
    s += lbl(cx + 26, top + 300, 520, top + 330, 'сестринская хроматида')
    s += lbl(cx + 40, yc, 520, yc + 8, 'центромера (первичная перетяжка)')
    s += lbl(cx + 46, top + 12, 520, top + 20, 'теломеры — концы хромосомы', ORANGE)
    s += f'<path d="M{cx - 70} {top} V {yc - 22}" stroke="{GREY}" stroke-width="4"/>' + text(cx - 84, (top + yc) / 2 + 8, 'короткое плечо', 's', 'end')
    s += f'<path d="M{cx - 70} {yc + 22} V {top + L}" stroke="{GREY}" stroke-width="4"/>' + text(cx - 84, (yc + top + L) / 2 + 8, 'длинное плечо', 's', 'end')
    # спутничная хромосома
    x2, t2 = 1130, 140
    s += bar(x2 - 14, t2, 40, DAD, 24) + bar(x2 + 14, t2, 40, DAD, 24)
    s += bar(x2 - 14, t2 + 60, 210, DAD, 24) + bar(x2 + 14, t2 + 60, 210, DAD, 24)
    s += f'<line x1="{x2 - 14}" y1="{t2 + 40}" x2="{x2 - 14}" y2="{t2 + 60}" stroke="{DAD}" stroke-width="5"/>'
    s += f'<line x1="{x2 + 14}" y1="{t2 + 40}" x2="{x2 + 14}" y2="{t2 + 60}" stroke="{DAD}" stroke-width="5"/>'
    s += f'<ellipse cx="{x2}" cy="{t2 + 100}" rx="30" ry="11" fill="{INK}" opacity=".55"/>'
    s += lbl(x2 + 26, t2 + 20, 1250, t2 + 26, 'спутник')
    s += lbl(x2 + 26, t2 + 50, 1250, t2 + 70, 'вторичная перетяжка')
    s += lbl(x2 + 30, t2 + 100, 1250, t2 + 114, 'центромера')
    # гомологи
    s += card(1000, 420, 560, 300)
    s += text(1280, 460, 'пара гомологичных хромосом', 't', 'middle')
    s += chrom(1200, 580, 180, MOM, 0.38, True, 0, 18, 4) + chrom(1360, 580, 180, DAD, 0.38, True, 0, 18, 4)
    s += text(1200, 700, 'от матери', 's', 'middle', MOM) + text(1360, 700, 'от отца', 's', 'middle', DAD)
    s += text(800, 770, 'Сестринские хроматиды — копии одной ДНК; гомологи — две разные хромосомы одной пары.', 's', 'middle')
    return s


# 2. Типы хромосом ----------------------------------------------------------------------------
def chromosome_types() -> str:
    s = text(890, 50, 'Типы хромосом по положению центромеры', 'h', 'middle')
    items = [(0.5, 'метацентрическая', 'плечи равны'), (0.33, 'субметацентрическая', 'плечи неравны'),
             (0.1, 'акроцентрическая', 'одно плечо очень короткое'), (0.0, 'телоцентрическая', 'центромера на конце')]
    for k, (f, name, note) in enumerate(items):
        cx = 180 + k * 360
        L, top = 300, 130
        s += bar(cx - 15, top, L, DAD, 26) + bar(cx + 15, top, L, DAD, 26)
        yc = top + max(f * L, 10)
        s += f'<ellipse cx="{cx}" cy="{yc}" rx="32" ry="12" fill="{INK}" opacity=".6"/>'
        s += text(cx, 500, name, 't', 'middle') + text(cx, 536, note, 's', 'middle')
    x5 = 1610
    s += bar(x5 - 15, 130, 34, MOM, 26) + bar(x5 + 15, 130, 34, MOM, 26)
    s += f'<line x1="{x5 - 15}" y1="164" x2="{x5 - 15}" y2="184" stroke="{MOM}" stroke-width="5"/><line x1="{x5 + 15}" y1="164" x2="{x5 + 15}" y2="184" stroke="{MOM}" stroke-width="5"/>'
    s += bar(x5 - 15, 184, 246, MOM, 26) + bar(x5 + 15, 184, 246, MOM, 26)
    s += f'<ellipse cx="{x5}" cy="{205}" rx="32" ry="12" fill="{INK}" opacity=".6"/>'
    s += text(x5, 500, 'спутничная', 't', 'middle') + text(x5, 536, 'спутник за вторичной', 's', 'middle') + text(x5, 566, 'перетяжкой', 's', 'middle')
    s += f'<line x1="1440" y1="110" x2="1440" y2="580" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 8"/>'
    s += text(890, 620, 'Спутник — дополнительный признак строения, а не пятое положение центромеры.', 'cap', 'middle')
    return s


# 3. Кариотип человека ------------------------------------------------------------------------
LENS = [92, 89, 81, 78, 75, 71, 66, 61, 58, 56, 56, 55, 47, 45, 43, 40, 38, 35, 31, 31, 26, 27]
ACRO = {13, 14, 15, 21, 22}


def mini(cx, base, L, color, frac):
    top = base - L
    yc = top + frac * L
    return (bar(cx - 5, top, L, color, 9) + bar(cx + 5, top, L, color, 9)
            + f'<ellipse cx="{cx}" cy="{yc:.1f}" rx="11" ry="4" fill="{INK}" opacity=".55"/>')


def idiogram(x0, title, sex):
    s = card(x0, 90, 760, 600) + text(x0 + 380, 135, title, 't', 'middle')
    for k in range(22):
        n = k + 1
        col, row = k % 8, k // 8
        cx = x0 + 60 + col * 92
        base = 270 + row * 150
        f = 0.12 if n in ACRO else (0.45 if n in (1, 3, 16, 19, 20) else 0.32)
        s += mini(cx - 12, base, LENS[k], MOM, f) + mini(cx + 12, base, LENS[k], DAD, f)
        s += text(cx, base + 30, str(n), 'cap', 'middle')
    cx, base = x0 + 60 + 6 * 92, 570
    if sex == 'XX':
        s += mini(cx - 12, base, 70, MOM, 0.38) + mini(cx + 12, base, 70, DAD, 0.38)
        s += text(cx, base + 30, 'XX', 'cap', 'middle', RED)
    else:
        s += mini(cx - 12, base, 70, MOM, 0.38) + mini(cx + 12, base, 26, DAD, 0.28)
        s += text(cx, base + 30, 'XY', 'cap', 'middle', RED)
    s += text(x0 + 380, 660, f'22 пары аутосом + {sex} = 46 хромосом (2n)', 's', 'middle')
    return s


def human_karyotype() -> str:
    s = text(800, 50, 'Кариотип человека: 2n = 46, в гамете n = 23', 'h', 'middle')
    s += idiogram(30, 'женский', 'XX') + idiogram(810, 'мужской', 'XY')
    s += text(800, 735, 'X и Y различаются по размеру и строению; хромосомы показаны в метафазе (двухроматидные).', 'cap', 'middle')
    return s


# 4. Клеточный цикл ---------------------------------------------------------------------------
def pt(cx, cy, r, a):
    return cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a))


def sector(cx, cy, a0, a1, r0, r1, fill):
    x1, y1 = pt(cx, cy, r1, a0)
    x2, y2 = pt(cx, cy, r1, a1)
    x3, y3 = pt(cx, cy, r0, a1)
    x4, y4 = pt(cx, cy, r0, a0)
    big = 1 if a1 - a0 > 180 else 0
    return (f'<path d="M{x1:.1f} {y1:.1f} A {r1} {r1} 0 {big} 1 {x2:.1f} {y2:.1f} L {x3:.1f} {y3:.1f} '
            f'A {r0} {r0} 0 {big} 0 {x4:.1f} {y4:.1f} Z" fill="{fill}" stroke="#fff" stroke-width="6"/>')


def cell_cycle() -> str:
    s = text(760, 50, 'Клеточный (митотический) цикл', 'h', 'middle')
    cx, cy, r0, r1 = 400, 420, 150, 260
    secs = [(0, 160, '#F6D7A7', 'G₁'), (160, 250, '#F3B6B9', 'S'), (250, 310, '#C9D8F2', 'G₂'), (310, 360, '#BFE3C8', 'митоз')]
    for a0, a1, f, t in secs:
        s += sector(cx, cy, a0, a1, r0, r1, f)
        mx, my = pt(cx, cy, (r0 + r1) / 2, (a0 + a1) / 2)
        s += text(mx, my + 12, chem(t), 'f' if t != 'митоз' else 't', 'middle')
    s += text(cx, cy - 6, 'интерфаза', 's', 'middle') + text(cx, cy + 26, chem('G₁ + S + G₂'), 's', 'middle')
    for a in range(20, 350, 40):
        x1, y1 = pt(cx, cy, r1 + 22, a)
        x2, y2 = pt(cx, cy, r1 + 22, a + 16)
        s += arrow(x1, y1, x2, y2, GREY, 3)
    gx, gy = pt(cx, cy, r1, 75)
    s += arrow(gx, gy, 760, 360, INK, 4)
    s += card(770, 300, 300, 110, '#fff', INK)
    s += text(920, 345, chem('G₀'), 'f', 'middle') + text(920, 390, 'вне цикла деления', 's', 'middle')
    s += lines_at(920, 450, ['обмен веществ и функции', 'клетки сохраняются'], 'cap', step=30)
    s += card(1100, 110, 400, 590)
    rows = [('G₁', 'рост, синтез веществ', '2n2c'), ('S', 'репликация ДНК', '2n2c → 2n4c'), ('G₂', 'подготовка к делению', '2n4c'),
            ('митоз', '+ цитокинез → 2 клетки', '2n2c в каждой')]
    for j, (t, a, b) in enumerate(rows):
        y = 170 + j * 135
        s += text(1130, y, chem(t), 't', 'start', RED if t == 'S' else INK)
        s += text(1130, y + 36, a, 's') + text(1130, y + 70, chem(b), 's', 'start', BLUE)
    s += text(770, 760, 'В S удваивается ДНК, число хромосом не меняется. Длительности секторов условные.', 's', 'middle')
    return s


# 5. Митоз -------------------------------------------------------------------------------------
PAIRS = [(70, MOM, 0.38), (70, DAD, 0.38), (44, MOM, 0.3), (44, DAD, 0.3)]


def mitosis_phases() -> str:
    s = text(850, 50, 'Митоз: четыре фазы (схема для 2n = 4)', 'h', 'middle')
    rx, ry, y = 165, 160, 300
    xs = [200, 600, 1000, 1440]
    # профаза
    cx = xs[0]
    s += cellbody(cx, y, rx, ry, True, 110)
    for (L, col, f), (dx, dy, a) in zip(PAIRS, [(-45, -30, 20), (40, -40, -25), (-40, 60, -10), (45, 55, 30)]):
        s += chrom(cx + dx, y + dy, L, col, f, True, a)
    s += pole(cx - 140, y) + pole(cx + 140, y)
    # метафаза
    cx = xs[1]
    s += cellbody(cx, y, rx, ry)
    ys = [y - 100, y - 20, y + 50, y + 105]
    s += spindle(cx - 145, y, [(cx - 9, yy) for yy in ys]) + spindle(cx + 145, y, [(cx + 9, yy) for yy in ys])
    for (L, col, f), yy in zip(PAIRS, ys):
        s += chrom(cx, yy, L, col, 0.5, True)
    s += pole(cx - 145, y) + pole(cx + 145, y)
    s += f'<line x1="{cx}" y1="{y - 150}" x2="{cx}" y2="{y + 150}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 6"/>'
    # анафаза
    cx = xs[2]
    s += cellbody(cx, y, rx + 10, ry - 10)
    ys = [y - 90, y - 20, y + 45, y + 95]
    for side in (-1, 1):
        px = cx + side * 150
        tx = cx + side * 75
        s += spindle(px, y, [(tx, yy) for yy in ys])
        for (L, col, f), yy in zip(PAIRS, ys):
            s += chrom(tx, yy, L, col, 0.5, False)
        s += pole(px, y)
    # телофаза
    cx = xs[3]
    s += (f'<path d="M{cx} {y - 120} C {cx - 60} {y - 175} {cx - 210} {y - 150} {cx - 210} {y} C {cx - 210} {y + 150} {cx - 60} {y + 175} {cx} {y + 120} '
          f'C {cx + 60} {y + 175} {cx + 210} {y + 150} {cx + 210} {y} C {cx + 210} {y - 150} {cx + 60} {y - 175} {cx} {y - 120} Z" '
          f'fill="{CELL}" stroke="{INK}" stroke-width="3"/>')
    for side in (-1, 1):
        nx = cx + side * 105
        s += f'<circle cx="{nx}" cy="{y}" r="80" fill="{NUC}" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
        for (L, col, f), (dx, dy) in zip(PAIRS, [(-30, -25), (25, -30), (-25, 40), (30, 35)]):
            s += chrom(nx + dx, y + dy, L * 0.8, col, f, False, 15, 10)
    labels = [('профаза', ['хромосомы спирализуются,', 'оболочка ядра исчезает'], '2n4c'),
              ('метафаза', ['хромосомы на экваторе,', 'нити веретена у центромер'], '2n4c'),
              ('анафаза', ['сестринские хроматиды', 'расходятся к полюсам'], 'вся клетка 4n4c; у полюса 2n2c'),
              ('телофаза', ['ядра восстанавливаются,', 'цитокинез'], '→ 2 клетки по 2n2c')]
    for cx, (t, rows, f) in zip(xs, labels):
        s += text(cx, 510, t, 't', 'middle') + lines_at(cx, 548, rows, 'cap', step=28) + text(cx, 625, chem(f), 's', 'middle', BLUE)
    s += text(850, 690, 'Цвет — материнская и отцовская хромосомы пары; сестринские хроматиды одного цвета.', 'cap', 'middle')
    return s


# 6. Мейоз -------------------------------------------------------------------------------------
def small_cell(cx, cy, r=78):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CELL}" stroke="{INK}" stroke-width="3"/>'


def meiosis_phases() -> str:
    s = text(840, 46, 'Мейоз: два деления после одной репликации (2n = 4)', 'h', 'middle')
    xs = [200, 610, 1020, 1460]
    y1, y2 = 290, 740
    s += text(30, y1 - 150, 'Мейоз I — расходятся гомологи', 't', 'start', RED)
    s += text(30, y2 - 150, 'Мейоз II — расходятся сестринские хроматиды', 't', 'start', BLUE)
    A, B = 64, 40
    # профаза I: биваленты
    cx = xs[0]
    s += cellbody(cx, y1, 165, 130, True, 105)
    s += chrom(cx - 50, y1 - 5, A, MOM, 0.38, True, 15) + chrom(cx - 18, y1 - 5, A, DAD, 0.38, True, 15)
    s += chrom(cx + 30, y1 + 20, B, MOM, 0.3, True, -20) + chrom(cx + 58, y1 + 20, B, DAD, 0.3, True, -20)
    # метафаза I
    cx = xs[1]
    s += cellbody(cx, y1, 165, 130)
    s += spindle(cx - 145, y1, [(cx - 22, y1 - 45), (cx - 22, y1 + 55)]) + spindle(cx + 145, y1, [(cx + 22, y1 - 45), (cx + 22, y1 + 55)])
    s += chrom(cx - 22, y1 - 45, A, MOM, 0.5) + chrom(cx + 22, y1 - 45, A, DAD, 0.5)
    s += chrom(cx - 22, y1 + 55, B, DAD, 0.5) + chrom(cx + 22, y1 + 55, B, MOM, 0.5)
    s += pole(cx - 145, y1) + pole(cx + 145, y1)
    s += f'<line x1="{cx}" y1="{y1 - 125}" x2="{cx}" y2="{y1 + 125}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 6"/>'
    # анафаза I
    cx = xs[2]
    s += cellbody(cx, y1, 175, 125)
    s += spindle(cx - 150, y1, [(cx - 85, y1 - 40), (cx - 85, y1 + 50)]) + spindle(cx + 150, y1, [(cx + 85, y1 - 40), (cx + 85, y1 + 50)])
    s += chrom(cx - 85, y1 - 40, A, MOM, 0.5) + chrom(cx - 85, y1 + 50, B, DAD, 0.5)
    s += chrom(cx + 85, y1 - 40, A, DAD, 0.5) + chrom(cx + 85, y1 + 50, B, MOM, 0.5)
    s += pole(cx - 150, y1) + pole(cx + 150, y1)
    # телофаза I
    cx = xs[3]
    for side, (ca, cb) in ((-1, (MOM, DAD)), (1, (DAD, MOM))):
        s += small_cell(cx + side * 88, y1, 84)
        s += chrom(cx + side * 88 - 20, y1 - 5, A, ca, 0.38, True, 10) + chrom(cx + side * 88 + 24, y1 + 10, B, cb, 0.3, True, -15)
    # мейоз II
    cells = [(MOM, DAD), (DAD, MOM)]
    # профаза II
    cx = xs[0]
    for side, (ca, cb) in zip((-1, 1), cells):
        s += small_cell(cx + side * 88, y2, 80)
        s += chrom(cx + side * 88 - 20, y2, A, ca, 0.38, True, 10) + chrom(cx + side * 88 + 24, y2 + 10, B, cb, 0.3, True, -15)
    # метафаза II
    cx = xs[1]
    for side, (ca, cb) in zip((-1, 1), cells):
        c = cx + side * 88
        s += small_cell(c, y2, 80)
        s += f'<line x1="{c}" y1="{y2 - 75}" x2="{c}" y2="{y2 + 75}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 6"/>'
        s += chrom(c, y2 - 25, A, ca, 0.5) + chrom(c, y2 + 38, B, cb, 0.5)
    # анафаза II
    cx = xs[2]
    for side, (ca, cb) in zip((-1, 1), cells):
        c = cx + side * 90
        s += f'<ellipse cx="{c}" cy="{y2}" rx="86" ry="74" fill="{CELL}" stroke="{INK}" stroke-width="3"/>'
        for d in (-1, 1):
            s += chrom(c + d * 42, y2 - 22, A, ca, 0.5, False) + chrom(c + d * 42, y2 + 38, B, cb, 0.5, False)
    # телофаза II — четыре клетки
    cx = xs[3]
    for k, (ca, cb) in enumerate([(MOM, DAD), (MOM, DAD), (DAD, MOM), (DAD, MOM)]):
        c, yy = cx - 75 + (k % 2) * 150, y2 - 62 + (k // 2) * 124
        s += small_cell(c, yy, 58)
        s += chrom(c - 14, yy, A * 0.8, ca, 0.38, False, 0, 10) + chrom(c + 16, yy + 6, B * 0.8, cb, 0.3, False, 0, 10)
    t1 = [('профаза I', 'конъюгация, кроссинговер', '2n4c'), ('метафаза I', 'пары гомологов на экваторе', '2n4c'),
          ('анафаза I', 'гомологи к полюсам', 'хроматиды вместе'), ('телофаза I', 'две клетки', 'n2c в каждой')]
    t2 = [('профаза II', 'без новой репликации', 'n2c'), ('метафаза II', 'хромосомы на экваторе', 'n2c'),
          ('анафаза II', 'хроматиды к полюсам', ''), ('телофаза II', 'четыре клетки', 'nc в каждой')]
    for cx, (t, a, b) in zip(xs, t1):
        s += text(cx, y1 + 170, t, 't', 'middle') + text(cx, y1 + 204, a, 'cap', 'middle') + text(cx, y1 + 236, chem(b), 's', 'middle', BLUE)
    for cx, (t, a, b) in zip(xs, t2):
        s += text(cx, y2 + 170, t, 't', 'middle') + text(cx, y2 + 204, a, 'cap', 'middle') + text(cx, y2 + 236, chem(b), 's', 'middle', BLUE)
    s += text(840, 1030, 'Перед мейозом I — одна репликация (2n4c); между I и II ДНК не удваивается.', 's', 'middle')
    return s


# 7. Кроссинговер ------------------------------------------------------------------------------
def crossing_over() -> str:
    s = text(760, 50, 'Конъюгация и кроссинговер (профаза I)', 'h', 'middle')
    L, w, top = 300, 26, 130
    # 1. гомологи
    x = 160
    for k, col in enumerate((MOM, MOM, DAD, DAD)):
        s += bar(x + k * 34 + (24 if k > 1 else 0), top, L, col, w)
    s += text(x + 64, top + L + 50, 'два гомолога,', 's', 'middle') + text(x + 64, top + L + 82, 'по две хроматиды', 's', 'middle')
    s += arrow(330, 200, 450, 200, GREY, 5)
    # 2. конъюгация с перекрёстом несестринских хроматид
    x = 560
    s += bar(x, top, L, MOM, w) + bar(x + 102, top, L, DAD, w)
    s += (f'<path d="M{x + 34} {top + 13} V {top + 150} L {x + 68} {top + 210} V {top + L - 13}" stroke="{MOM}" stroke-width="{w}" '
          f'stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    s += (f'<path d="M{x + 68} {top + 13} V {top + 150} L {x + 34} {top + 210} V {top + L - 13}" stroke="{DAD}" stroke-width="{w}" '
          f'stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    s += lbl(x + 51, top + 180, x + 220, top + 190, 'перекрёст несестринских')
    s += text(x + 228, top + 222, 'хроматид', 's', 'start')
    s += text(x + 51, top + L + 50, 'конъюгация:', 's', 'middle') + text(x + 51, top + L + 82, 'гомологи сближены', 's', 'middle')
    s += arrow(960, 200, 1060, 200, GREY, 5)
    # 3. результат
    x = 1140
    cut = top + 180
    cols = [(MOM, MOM), (MOM, DAD), (DAD, MOM), (DAD, DAD)]
    for k, (c1, c2) in enumerate(cols):
        xx = x + k * 34 + (24 if k > 1 else 0)
        s += bar(xx, top, L, c2, w)
        s += f'<rect x="{xx - w / 2}" y="{top}" width="{w}" height="{cut - top}" rx="{w / 2}" fill="{c1}"/>'
        s += f'<rect x="{xx - w / 2}" y="{cut - 14}" width="{w}" height="14" fill="{c1}"/>'
    s += text(x + 64, top + L + 50, 'хроматиды с новыми', 's', 'middle') + text(x + 64, top + L + 82, 'сочетаниями участков', 's', 'middle')
    s += text(760, 610, 'Обмениваются участками несестринские хроматиды гомологов → комбинативная изменчивость.', 's', 'middle')
    return s


# 8. Гаметогенез --------------------------------------------------------------------------------
def gcell(cx, cy, r, fill, txt=''):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
    return s + (text(cx, cy + 8, chem(txt), 'cap', 'middle', INK) if txt else '')


def sperm(cx, cy):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="13" ry="18" fill="{DAD}"/>'
            f'<path d="M{cx} {cy + 18} q -10 20 0 40 q 10 20 0 40" stroke="{DAD}" stroke-width="4" fill="none"/>')


def gametogenesis() -> str:
    s = text(900, 46, 'Гаметогенез: стадии и набор хромосом / ДНК', 'h', 'middle')
    stages = [(150, 'размножение', 'митоз'), (300, 'рост', 'репликация ДНК'), (460, 'созревание', 'мейоз I'),
              (640, '', 'мейоз II'), (810, 'формирование', 'только у сперматозоидов')]
    for y, a, b in stages:
        s += f'<line x1="30" y1="{y + 70}" x2="1770" y2="{y + 70}" stroke="#E4DDD0" stroke-width="2"/>'
        if a:
            s += text(40, y + 4, a, 't')
        s += text(40, y + 38, b, 'cap')
    s += text(620, 90, 'сперматогенез (семенники)', 't', 'middle', DAD)
    s += text(1340, 90, 'оогенез (яичники)', 't', 'middle', MOM)
    # сперматогенез
    xs1 = [620]
    s += gcell(620, 150, 46, '#DCE6F7', '2n2c') + text(700, 158, 'сперматогонии', 's')
    s += arrow(620, 200, 620, 250, GREY, 4)
    s += gcell(620, 300, 56, '#DCE6F7', '2n4c') + text(690, 308, 'сперматоцит I', 's')
    s += arrow(600, 358, 520, 420, GREY, 4) + arrow(640, 358, 720, 420, GREY, 4)
    for x in (500, 740):
        s += gcell(x, 460, 42, '#DCE6F7', 'n2c')
    s += text(795, 468, 'сперматоциты II', 's')
    for k, x in enumerate((420, 560, 680, 820)):
        s += arrow(500 if k < 2 else 740, 505, x, 600, GREY, 3)
        s += gcell(x, 640, 34, '#DCE6F7', 'nc')
    s += text(620, 705, 'четыре сперматиды', 's', 'middle')
    for x in (420, 560, 680, 820):
        s += sperm(x, 780)
    s += text(620, 915, chem('4 сперматозоида, nc'), 's', 'middle', DAD)
    # оогенез
    s += gcell(1340, 150, 46, '#F8DEDF', '2n2c') + text(1420, 158, 'оогонии', 's')
    s += arrow(1340, 200, 1340, 240, GREY, 4)
    s += gcell(1340, 300, 64, '#F8DEDF', '2n4c') + text(1415, 308, 'овоцит I', 's')
    s += arrow(1340, 366, 1310, 404, GREY, 4) + arrow(1380, 360, 1500, 430, GREY, 3)
    s += gcell(1290, 460, 56, '#F8DEDF', 'n2c') + text(1215, 468, 'овоцит II', 's', 'end')
    s += gcell(1520, 460, 20, '#F8DEDF') + text(1550, 468, 'полярное тельце', 'cap')
    s += arrow(1290, 518, 1290, 580, GREY, 4) + arrow(1320, 512, 1420, 620, GREY, 3) + arrow(1520, 482, 1520, 618, GREY, 3)
    s += arrow(1530, 480, 1610, 618, GREY, 3)
    s += gcell(1290, 640, 56, '#F8DEDF', 'nc') + text(1215, 648, 'яйцеклетка', 's', 'end')
    for x in (1440, 1520, 1610):
        s += gcell(x, 640, 18, '#F8DEDF')
    s += text(1525, 700, 'три полярных тельца', 'cap', 'middle')
    s += text(1400, 760, '1 яйцеклетка + 3 полярных тельца', 's', 'middle', MOM)
    s += text(1400, 792, '(завершённая учебная модель)', 'cap', 'middle')
    s += text(900, 958, 'Мейоз начинает клетка I порядка; между мейозом I и II ДНК не удваивается.', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'chromosome-structure.png': (chromosome_structure(), 1600, 800),
        'chromosome-types.png': (chromosome_types(), 1790, 650),
        'human-karyotype.png': (human_karyotype(), 1600, 760),
        'cell-cycle.png': (cell_cycle(), 1540, 790),
        'mitosis-phases.png': (mitosis_phases(), 1700, 720),
        'meiosis-phases.png': (meiosis_phases(), 1680, 1060),
        'crossing-over.png': (crossing_over(), 1520, 640),
        'gametogenesis.png': (gametogenesis(), 1800, 985),
    }
    only = set(__import__('sys').argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
