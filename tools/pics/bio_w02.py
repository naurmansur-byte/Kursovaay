"""Рисунки недели 2 биологии (course/biology/week-02/pics/*.png): углеводы, нуклеотид, уровни белка, размеры ДНК.

Факты — по выжимке course/textbooks/bio-02-biomolecules.md (Б8, Б9, Б10-1).
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w02.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, PAPER, RED, ROOT, chem, lab, render, smooth, text

OUT = ROOT / 'course' / 'biology' / 'week-02' / 'pics'
BLUE, ORANGE, PURPLE, PINK = '#3A57A7', '#D9822B', '#7A4FA3', '#F8D0D2'


def badge(cx: float, cy: float, s: str, color: str, r: float = 24, size: int = 18) -> str:
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{color}"/>'
            f'<text x="{cx:.0f}" y="{cy + size * 0.36:.0f}" text-anchor="middle" style="font-size:{size}px;font-weight:800;fill:#fff">{s}</text>')


def card(x0: float, y0: float, w: float, h: float, title: str, color: str) -> str:
    return (f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{x0} {y0 + 60} V{y0 + 16} a16 16 0 0 1 16 -16 H{x0 + w - 16} a16 16 0 0 1 16 16 V{y0 + 60} Z" fill="{color}"/>'
            + text(x0 + 26, y0 + 42, title, 'w'))


def chain(x: float, y: float, n: int, letter: str, color: str, step: float = 40, branch: int | None = None) -> str:
    pts = [(x + k * step, y) for k in range(n)]
    if branch is not None:
        bx, by = pts[branch]
        pts_b = [(bx + 28 + k * step, by + 32) for k in range(3)]
        s = ''.join(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{INK}" stroke-width="3"/>'
                    for a, b in zip([pts[branch]] + pts_b[:-1], pts_b))
        pts_all = pts + pts_b
    else:
        s, pts_all = '', pts
    s = f'<line x1="{pts[0][0]:.0f}" y1="{y:.0f}" x2="{pts[-1][0]:.0f}" y2="{y:.0f}" stroke="{INK}" stroke-width="3"/>' + s
    return s + ''.join(badge(px, py, letter, color, 15, 15) for px, py in pts_all)


def carbohydrate_map() -> str:
    s = text(800, 60, 'Углеводы', 'h', 'middle')
    GL, FR, GAL = ('Гл', GREEN), ('Фр', ORANGE), ('Гал', BLUE)
    # Моносахариды
    x0, y0 = 30, 100
    s += card(x0, y0, 500, 620, 'Моносахариды', GREEN) + text(x0 + 26, y0 + 98, 'простые сахара', 'cap')
    s += text(x0 + 26, y0 + 150, 'гексозы — 6 атомов C', 't')
    for k, ((ab, c), name, note) in enumerate([(GL, 'глюкоза', 'виноградный сахар'), (FR, 'фруктоза', 'плодовый сахар, в мёде'),
                                               (GAL, 'галактоза', 'входит в молочный сахар')]):
        y = y0 + 205 + k * 72
        s += badge(x0 + 52, y, ab, c) + text(x0 + 92, y + 2, name, 's') + text(x0 + 92, y + 32, note, 'cap')
    s += text(x0 + 26, y0 + 445, 'пентозы — 5 атомов C', 't')
    for k, (ab, name, note) in enumerate([('Р', 'рибоза', 'в РНК'), ('дР', 'дезоксирибоза', 'в ДНК')]):
        y = y0 + 500 + k * 72
        s += badge(x0 + 52, y, ab, PURPLE) + text(x0 + 92, y + 2, name, 's') + text(x0 + 92, y + 32, note, 'cap')
    # Дисахариды
    x0 = 550
    s += card(x0, y0, 500, 620, 'Дисахариды', GREEN) + text(x0 + 26, y0 + 98, 'два остатка моносахаридов;', 'cap')
    s += text(x0 + 26, y0 + 128, 'гликозидная связь, выделяется вода', 'cap')
    for k, (pair, name, eq, note) in enumerate([((GL, FR), 'сахароза', '= глюкоза + фруктоза', 'тростниковый, свекловичный сахар'),
                                                ((GL, GAL), 'лактоза', '= глюкоза + галактоза', 'молочный сахар')]):
        y = y0 + 195 + k * 150
        s += f'<line x1="{x0 + 52}" y1="{y}" x2="{x0 + 108}" y2="{y}" stroke="{INK}" stroke-width="4"/>'
        s += badge(x0 + 52, y, *pair[0]) + badge(x0 + 108, y, *pair[1]) + text(x0 + 152, y + 10, name, 't')
        s += text(x0 + 26, y + 62, eq, 's') + text(x0 + 26, y + 96, note, 'cap')
    s += text(x0 + 26, y0 + 505, 'мальтоза', 't') + text(x0 + 26, y0 + 540, 'тоже дисахарид', 'cap')
    # Полисахариды
    x0 = 1070
    s += card(x0, y0, 500, 620, 'Полисахариды', GREEN) + text(x0 + 26, y0 + 98, 'множество остатков глюкозы;', 'cap')
    s += text(x0 + 26, y0 + 128, 'в воде не растворяются', 'cap')
    items = [('крахмал — из α-глюкозы', 'запас растений: семена, клубни', 'α', GREEN, None),
             ('гликоген — из α-глюкозы', 'запас животных, человека и грибов', 'α', GREEN, 2),
             ('целлюлоза — из β-глюкозы', 'клеточная стенка растений', 'β', ORANGE, None)]
    for k, (name, note, letter, color, br) in enumerate(items):
        y = y0 + 185 + k * 150
        s += text(x0 + 26, y, name, 's') + text(x0 + 26, y + 32, note, 'cap') + chain(x0 + 50, y + 75, 9 if br is None else 7, letter, color, branch=br)
    s += f'<rect x="30" y="745" width="1540" height="115" rx="14" fill="{PAPER}"/>'
    s += text(60, 790, 'Другие строительные полисахариды (не из обычной глюкозы):', 't')
    s += text(60, 832, 'хитин — наружный скелет членистоногих и клеточная стенка грибов; муреин — клеточная стенка бактерий', 's')
    return s


def nucleotide() -> str:
    s = ''
    rows = [('Нуклеотид ДНК', 'дезоксирибоза', 'А, Т, Г, Ц', 'Т'), ('Нуклеотид РНК', 'рибоза', 'А, У, Г, Ц', 'У')]
    for k, (title, sugar, bases, odd) in enumerate(rows):
        y = 210 + k * 330
        s += text(60, y - 110, title, 'h')
        s += f'<circle cx="470" cy="{y}" r="58" fill="{LIGHT_YELLOW}" stroke="#C7891B" stroke-width="5"/>'
        pent = [(800 + 74 * math.cos(math.radians(-90 + 72 * i)), y + 74 * math.sin(math.radians(-90 + 72 * i))) for i in range(5)]
        s += f'<line x1="528" y1="{y}" x2="{pent[4][0]:.0f}" y2="{pent[4][1]:.0f}" stroke="{INK}" stroke-width="6"/>'
        s += f'<line x1="{pent[1][0]:.0f}" y1="{pent[1][1]:.0f}" x2="1050" y2="{y}" stroke="{INK}" stroke-width="6"/>'
        s += f'<polygon points="{" ".join(f"{px:.0f},{py:.0f}" for px, py in pent)}" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="5"/>'
        s += f'<rect x="1050" y="{y - 55}" width="220" height="110" rx="14" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="5"/>'
        s += text(1160, y + 11, bases.replace(odd, f'<tspan style="fill:{RED}">{odd}</tspan>'), 't', 'middle')
        s += text(470, y + 105, 'остаток', 's', 'middle') + text(470, y + 137, 'фосфорной кислоты', 's', 'middle')
        s += text(800, y + 105, sugar, 's', 'middle', RED) + text(800, y + 137, 'пентоза', 'cap', 'middle')
        s += text(1160, y + 105, 'азотистое основание', 's', 'middle') + text(1160, y + 137, 'одно из четырёх', 'cap', 'middle')
    s += text(800, 760, 'Нуклеотид — одно звено. ДНК и РНК — длинные цепи из многих нуклеотидов.', 't', 'middle')
    return s


def protein_levels() -> str:
    s = text(800, 55, 'Четыре уровня структуры белка', 'h', 'middle')
    titles = ['Первичная', 'Вторичная', 'Третичная', 'Четвертичная']
    desc = [('последовательность', 'аминокислот'), ('α-спираль или β-слой;', 'водородные связи'),
            ('упаковка одной цепи', 'в пространстве (глобула)'), ('несколько субъединиц;', 'гемоглобин: 2 α + 2 β')]
    for k in range(4):
        x0 = 20 + k * 395
        s += f'<rect x="{x0}" y="90" width="375" height="580" rx="16" fill="{PAPER}"/>'
        s += text(x0 + 187, 145, titles[k], 'h', 'middle')
        s += text(x0 + 187, 590, desc[k][0], 's', 'middle') + text(x0 + 187, 624, desc[k][1], 's', 'middle')
    # 1. первичная: цепочка аминокислот
    x0 = 20
    pts = [(x0 + 50 + i * 46, 330 + (25 if i % 2 else -25)) for i in range(7)]
    s += ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="5"/>' for a, b in zip(pts, pts[1:]))
    colors = [LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW, PINK, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_BLUE]
    s += ''.join(f'<circle cx="{px}" cy="{py}" r="20" fill="{c}" stroke="{INK}" stroke-width="3"/>' for (px, py), c in zip(pts, colors))
    s += lab(pts[1][0], pts[1][1] - 20, x0 + 140, 220, 'аминокислоты')
    mx, my = (pts[4][0] + pts[5][0]) / 2, (pts[4][1] + pts[5][1]) / 2
    s += lab(mx, my, x0 + 230, 470, 'пептидная связь')
    # 2. вторичная: α-спираль и β-слой, водородные связи пунктиром
    x0 = 415
    c, d, R, hx = 9, 20, 46, x0 + 70  # спираль сбоку: вытянутая трохоида
    coil = [(hx + c * u / 10 - d * math.sin(u / 10), 245 - R * math.cos(u / 10)) for u in range(0, 315)]
    s += f'<polyline points="{" ".join(f'{a:.1f},{b:.1f}' for a, b in coil)}" fill="none" stroke="{GREEN}" stroke-width="7" stroke-linejoin="round"/>'
    for k in range(4):  # водородные связи — между соседними витками, вдоль оси
        u = 2 * math.pi * k + (1.1 if k % 2 else 2.0)
        xa, ya = hx + c * u - d * math.sin(u), 245 - R * math.cos(u)
        s += f'<line x1="{xa:.0f}" y1="{ya:.0f}" x2="{xa + 2 * math.pi * c:.0f}" y2="{ya:.0f}" stroke="{RED}" stroke-width="3" stroke-dasharray="5 4"/>'
    s += text(x0 + 187, 330, 'α-спираль', 's', 'middle')
    for j in range(3):
        y = 380 + j * 42
        zz = [(x0 + 45 + i * 30, y + (7 if i % 2 else -7)) for i in range(10)]
        s += f'<polyline points="{" ".join(f"{a},{b}" for a, b in zz)}" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linejoin="round"/>'
        if j < 2:
            s += ''.join(f'<line x1="{a}" y1="{y + 9}" x2="{a}" y2="{y + 33}" stroke="{RED}" stroke-width="3" stroke-dasharray="4 3"/>' for a, _ in zz[::2])
    s += text(x0 + 187, 520, 'β-слой', 's', 'middle')
    # 3. третичная: свёрнутая цепь
    x0 = 810
    fold = []  # цепь петляет туда-обратно внутри круга — плотный клубок
    for r in range(6):
        y = 235 + r * 46
        half = (125 ** 2 - (y - 350) ** 2) ** 0.5
        row = [(x0 + 187 + f * half, y + (14 if j % 2 else -10)) for j, f in enumerate((-0.9, -0.35, 0.2, 0.75))]
        fold += row if r % 2 == 0 else row[::-1]
    s += f'<path d="{smooth(fold)}" fill="none" stroke="{GREEN}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    # 4. четвертичная: 4 субъединицы, в каждой — гем
    x0 = 1205
    for i, (dx, dy, name) in enumerate([(-62, -62, 'α'), (62, -62, 'β'), (-62, 62, 'β'), (62, 62, 'α')]):
        cx, cy = x0 + 187 + dx, 360 + dy
        fill, stroke = (LIGHT_GREEN, GREEN) if name == 'α' else (LIGHT_BLUE, BLUE)
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="66" ry="60" transform="rotate({20 * (1 if i % 3 else -1)} {cx} {cy})" fill="{fill}" stroke="{stroke}" stroke-width="5"/>'
        s += text(cx - 14, cy + 12, name, 't', 'middle')
        s += f'<rect x="{cx + 14}" y="{cy - 6}" width="18" height="18" transform="rotate(45 {cx + 23} {cy + 3})" fill="{RED}"/>'
    s += lab(x0 + 187 + 62 + 23, 360 - 62 + 3 - 12, x0 + 300, 215, 'гем')
    return s


def dna_dimensions() -> str:
    s = text(470, 60, 'Двойная спираль ДНК', 'h', 'middle')
    cx, top, turn, amp = 470, 140, 560, 165
    xs = lambda t, sign: cx + sign * amp * math.cos(2 * math.pi * t)  # noqa: E731
    pair_colors = [('#8CC9A0', '#EE9AA2'), ('#9DBDE3', '#E8CF6A')]
    ts = [k / 400 for k in range(-12, 413)]

    def strand(sign: int, front: bool) -> str:
        out, seg = '', []
        for t in ts:
            is_front = (math.sin(2 * math.pi * t) * sign) > 0
            if is_front == front:
                seg.append(f'{xs(t, sign):.1f},{top + turn * t:.1f}')
            elif seg:
                out += f'<polyline points="{" ".join(seg)}" fill="none" stroke="{GREEN if sign > 0 else BLUE}" ' \
                       f'stroke-width="{11 if front else 6}" stroke-opacity="{1 if front else 0.45}" stroke-linecap="round"/>'
                seg = []
        if seg:
            out += f'<polyline points="{" ".join(seg)}" fill="none" stroke="{GREEN if sign > 0 else BLUE}" ' \
                   f'stroke-width="{11 if front else 6}" stroke-opacity="{1 if front else 0.45}" stroke-linecap="round"/>'
        return out
    s += strand(1, False) + strand(-1, False)
    for i in range(11):
        t, y = i / 10, top + 56 * i
        a, b = xs(t, -1), xs(t, 1)
        c1, c2 = pair_colors[i % 2]
        m = (a + b) / 2
        s += f'<line x1="{a:.0f}" y1="{y}" x2="{m:.0f}" y2="{y}" stroke="{c1}" stroke-width="12"/><line x1="{m:.0f}" y1="{y}" x2="{b:.0f}" y2="{y}" stroke="{c2}" stroke-width="12"/>'
    s += strand(1, True) + strand(-1, True)
    t0, t1 = ts[0], ts[-1]
    s += text(xs(t0, 1), top + turn * t0 - 18, '5′', 't', 'middle') + text(xs(t0, -1), top + turn * t0 - 18, '3′', 't', 'middle')
    s += text(xs(t1, 1), top + turn * t1 + 42, '3′', 't', 'middle') + text(xs(t1, -1), top + turn * t1 + 42, '5′', 't', 'middle')
    # размеры
    def vbar(x: float, y1: float, y2: float) -> str:
        return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{INK}" stroke-width="4"/>'
                f'<line x1="{x - 12}" y1="{y1}" x2="{x + 12}" y2="{y1}" stroke="{INK}" stroke-width="4"/>'
                f'<line x1="{x - 12}" y1="{y2}" x2="{x + 12}" y2="{y2}" stroke="{INK}" stroke-width="4"/>')
    guide = lambda x1, x2, y: f'<line x1="{x1:.0f}" y1="{y}" x2="{x2:.0f}" y2="{y}" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 6"/>'  # noqa: E731
    s += guide(xs(0, 1), cx + 240, top) + guide(xs(1, 1), cx + 240, top + turn) + vbar(cx + 240, top, top + turn)
    s += text(cx + 265, 400, '3,4 нм', 't') + text(cx + 265, 436, 'один виток', 's') + text(cx + 265, 468, '= 10 пар', 's')
    y4, y5 = top + 56 * 4, top + 56 * 5
    s += guide(xs(0.4, -1), cx - 240, y4) + guide(xs(0.5, -1), cx - 240, y5) + vbar(cx - 240, y4, y5)
    s += text(cx - 262, y4 + 24, '0,34 нм', 't', 'end') + text(cx - 262, y4 + 56, 'шаг на пару', 'cap', 'end')
    s += (f'<line x1="{cx - amp}" y1="790" x2="{cx + amp}" y2="790" stroke="{INK}" stroke-width="4"/>'
          f'<line x1="{cx - amp}" y1="778" x2="{cx - amp}" y2="802" stroke="{INK}" stroke-width="4"/>'
          f'<line x1="{cx + amp}" y1="778" x2="{cx + amp}" y2="802" stroke="{INK}" stroke-width="4"/>')
    s += text(cx, 835, 'ширина ≈ 2 нм', 's', 'middle')
    # пары оснований
    s += text(1200, 160, 'Пары оснований', 'h', 'middle')
    for k, (l, r, n, cl, cr) in enumerate([('А', 'Т', 2, LIGHT_GREEN, PINK), ('Г', 'Ц', 3, LIGHT_BLUE, LIGHT_YELLOW)]):
        y = 300 + k * 230
        s += f'<rect x="1000" y="{y - 45}" width="120" height="90" rx="12" fill="{cl}" stroke="{INK}" stroke-width="4"/>' + text(1060, y + 12, l, 'f', 'middle')
        s += f'<rect x="1280" y="{y - 45}" width="120" height="90" rx="12" fill="{cr}" stroke="{INK}" stroke-width="4"/>' + text(1340, y + 12, r, 'f', 'middle')
        for j in range(n):
            yy = y + (j - (n - 1) / 2) * 24
            s += f'<line x1="1126" y1="{yy:.0f}" x2="1274" y2="{yy:.0f}" stroke="{RED}" stroke-width="4" stroke-dasharray="8 6"/>'
        s += text(1200, y + 90, f'{n} водородные связи', 's', 'middle')
    s += text(1200, 760, 'Цепи антипараллельны:', 's', 'middle') + text(1200, 795, 'одна 5′ → 3′, другая 3′ → 5′', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'carbohydrate-map.png': (carbohydrate_map(), 1600, 890),
        'nucleotide.png': (nucleotide(), 1600, 800),
        'protein-levels.png': (protein_levels(), 1600, 700),
        'dna-dimensions.png': (dna_dimensions(), 1600, 870),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
