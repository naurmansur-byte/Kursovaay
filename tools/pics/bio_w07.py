"""Рисунки недели 7 биологии (course/biology/week-07/pics/*.png): органы газообмена, дыхательные пути, альвеола, вдох и выдох,
состав воздуха, объёмы лёгких.

Факты — по выжимке course/textbooks/bio-07-gas-exchange.md (Б7а § 25–28, Б7м § 27, Б8 § 25–27). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w07.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, LIGHT_GREEN, PAPER, RED, ROOT, arrow, chem, label, render, smooth, text

OUT = ROOT / 'course' / 'biology' / 'week-07' / 'pics'
BLUE, LBLUE, LRED, PINK, PINK_LINE = '#3A57A7', '#DCE6F5', '#FBE3E4', '#F6C9C2', '#B85C4E'


def lbl(px, py, tx, ty, s, color=INK):
    return label(px, py, tx, ty, s, 's', color)


def lines_at(x, y, rows, cls='s', anchor='middle', step=32, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


# 1. Органы газообмена -----------------------------------------------------------------------------
def gas_exchange_groups() -> str:
    s = text(800, 56, 'Где идёт газообмен у разных организмов', 'h', 'middle')
    cards = [('Растение', ['устьица листа,', 'чечевички стебля']),
             ('Насекомое', ['дыхальца →', 'трахеи к тканям']),
             ('Рыба', ['жабры: обмен', 'в жаберных', 'лепестках']),
             ('Лягушка', ['лёгкие', 'и кожа']),
             ('Птица', ['лёгкие + воздушные', 'мешки; обмен —', 'в лёгких'])]
    for k, (title, rows) in enumerate(cards):
        x = 30 + k * 310
        cx, cy = x + 145, 280
        s += f'<rect x="{x}" y="100" width="290" height="500" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += text(cx, 150, title, 't', 'middle')
        if k == 0:
            s += f'<path d="M{cx - 100} {cy + 60} Q {cx} {cy - 140} {cx + 100} {cy + 60} Q {cx} {cy + 120} {cx - 100} {cy + 60} Z" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="3"/>'
            for dx, dy in ((-40, 30), (10, 0), (50, 40), (-10, 60), (30, -30)):
                s += f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="11" ry="7" fill="#fff" stroke="{GREEN}" stroke-width="2"/><path d="M{cx + dx - 9} {cy + dy} H {cx + dx + 9}" stroke="{GREEN}" stroke-width="2"/>'
        elif k == 1:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="110" ry="50" fill="#F7EFC8" stroke="#8A6A2A" stroke-width="3"/>'
            for dx in (-60, -20, 20, 60):
                s += f'<circle cx="{cx + dx}" cy="{cy + 48}" r="7" fill="{INK}"/>'
                s += f'<path d="M{cx + dx} {cy + 42} q 10 -40 -10 -70" fill="none" stroke="{BLUE}" stroke-width="3"/>'
            s += f'<path d="M{cx - 90} {cy - 25} H {cx + 90}" stroke="{BLUE}" stroke-width="4"/>'
        elif k == 2:
            s += f'<path d="M{cx - 120} {cy} Q {cx - 30} {cy - 70} {cx + 70} {cy} Q {cx - 30} {cy + 70} {cx - 120} {cy} Z" fill="{LBLUE}" stroke="{BLUE}" stroke-width="3"/>'
            s += f'<path d="M{cx + 70} {cy} L {cx + 120} {cy - 40} L {cx + 120} {cy + 40} Z" fill="{LBLUE}" stroke="{BLUE}" stroke-width="3"/>'
            for i in range(5):
                s += f'<path d="M{cx - 70 + i * 7} {cy - 30 + i * 3} q 12 30 0 60" fill="none" stroke="{RED}" stroke-width="3"/>'
            s += f'<circle cx="{cx - 95}" cy="{cy - 10}" r="6" fill="{INK}"/>'
        elif k == 3:
            s += f'<ellipse cx="{cx}" cy="{cy + 10}" rx="90" ry="60" fill="#CFE8C3" stroke="{GREEN}" stroke-width="3"/>'
            s += f'<ellipse cx="{cx - 30}" cy="{cy + 10}" rx="22" ry="34" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="2"/><ellipse cx="{cx + 30}" cy="{cy + 10}" rx="22" ry="34" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="2"/>'
            s += f'<circle cx="{cx - 40}" cy="{cy - 50}" r="16" fill="#CFE8C3" stroke="{GREEN}" stroke-width="3"/><circle cx="{cx + 40}" cy="{cy - 50}" r="16" fill="#CFE8C3" stroke="{GREEN}" stroke-width="3"/>'
        else:
            s += f'<ellipse cx="{cx - 25}" cy="{cy}" rx="30" ry="45" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="3"/><ellipse cx="{cx + 25}" cy="{cy}" rx="30" ry="45" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="3"/>'
            for dx, dy in ((-90, -40), (90, -40), (-95, 50), (95, 50)):
                s += f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="34" ry="26" fill="#fff" stroke="{BLUE}" stroke-width="3" stroke-dasharray="6 5"/>'
            s += text(cx, cy + 110, 'двойное дыхание', 'cap', 'middle', BLUE)
        s += lines_at(cx, 470, rows)
    return s


# 2. Дыхательные пути ------------------------------------------------------------------------------
def human_airways() -> str:
    s = text(600, 56, 'Дыхательная система человека', 'h', 'middle')
    # лёгкие
    s += f'<path d="{smooth([(470, 380), (380, 470), (350, 700), (420, 830), (520, 820), (560, 600), (540, 420)], True)}" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="4"/>'
    s += f'<path d="{smooth([(730, 380), (820, 470), (850, 700), (780, 830), (680, 820), (640, 600), (660, 420)], True)}" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="4"/>'
    # нос, глотка, гортань
    s += f'<path d="M520 130 Q 600 100 660 150 L 640 200 Q 600 180 560 200 Z" fill="#F3D3C8" stroke="{PINK_LINE}" stroke-width="3"/>'
    s += f'<path d="M600 190 L 600 300" stroke="{PINK_LINE}" stroke-width="30"/>'
    s += f'<path d="M585 250 q 30 -20 40 10" fill="none" stroke="{RED}" stroke-width="5"/>'
    s += f'<rect x="578" y="290" width="44" height="40" rx="8" fill="#E8C0A8" stroke="{PINK_LINE}" stroke-width="3"/>'
    # трахея с полукольцами
    s += f'<rect x="585" y="330" width="30" height="170" fill="#F3E6D8" stroke="#9C8460" stroke-width="2"/>'
    for y in range(340, 500, 16):
        s += f'<path d="M585 {y} H 615" stroke="#9C8460" stroke-width="5"/>'
    # бронхи и бронхиолы
    s += f'<path d="M600 500 L 520 560 L 470 640 M600 500 L 680 560 L 730 640" fill="none" stroke="#9C8460" stroke-width="12" stroke-linecap="round"/>'
    for sx, sy, d in ((470, 640, -1), (730, 640, 1)):
        for k in range(3):
            ex, ey = sx + d * (20 + k * 25), sy + 40 + k * 30
            s += f'<path d="M{sx} {sy} L {ex} {ey}" stroke="#9C8460" stroke-width="5"/>'
            s += ''.join(f'<circle cx="{ex + d * (dx)}" cy="{ey + dy}" r="7" fill="#fff" stroke="{RED}" stroke-width="2"/>' for dx, dy in ((0, 10), (10, 0), (-6, 12)))
    s += lbl(560, 160, 330, 140, 'носовая полость')
    s += lbl(600, 230, 330, 230, 'глотка')
    s += lbl(620, 258, 880, 230, 'надгортанник', RED)
    s += lbl(620, 310, 880, 300, 'гортань')
    s += lbl(615, 420, 880, 400, 'трахея:') + text(888, 432, 'хрящевые полукольца', 's', 'start')
    s += lbl(540, 548, 330, 520, 'главные бронхи')
    s += lbl(705, 690, 880, 680, 'бронхиолы')
    s += lbl(487, 720, 330, 760, 'альвеолы', RED)
    s += text(600, 900, 'Надгортанник при глотании закрывает вход в гортань.', 't', 'middle')
    return s


# 3. Альвеола и капилляр ---------------------------------------------------------------------------
def alveolus_capillary() -> str:
    s = text(600, 56, 'Газообмен в альвеоле', 'h', 'middle')
    s += f'<circle cx="420" cy="330" r="190" fill="#F8E7E3" stroke="{PINK_LINE}" stroke-width="5"/>'
    s += text(420, 300, 'альвеола', 't', 'middle') + text(420, 340, 'воздух', 's', 'middle', GREY)
    # капилляр огибает
    s += f'<path d="M180 570 C 380 600 640 560 700 380 C 740 260 720 160 660 100" fill="none" stroke="{BLUE}" stroke-width="44" stroke-linecap="round"/>'
    s += f'<path d="M700 380 C 740 260 720 160 660 100" fill="none" stroke="{RED}" stroke-width="44" stroke-linecap="round"/>'
    s += f'<path d="M180 570 C 380 600 640 560 700 380" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="8 10"/>'
    s += arrow(230, 575, 300, 584, '#fff', 5) + arrow(690, 220, 680, 150, '#fff', 5)
    s += text(180, 640, 'венозная кровь', 's', 'middle', BLUE) + text(705, 110, 'артериальная кровь', 's', 'start', RED)
    # стрелки газов
    s += arrow(470, 420, 545, 515, RED, 7) + text(455, 470, chem('O₂'), 't', 'end', RED)
    s += arrow(650, 450, 560, 380, GREY, 7) + text(560, 345, chem('CO₂'), 't', 'middle', GREY)
    s += f'<rect x="800" y="420" width="360" height="160" rx="16" fill="{PAPER}"/>'
    s += lines_at(980, 466, ['стенки альвеолы и капилляра', 'тонкие — газы проходят', 'диффузией'], 's')
    return s


# 4. Вдох и выдох ----------------------------------------------------------------------------------
def chest(cx, cy, big, label_text):
    w, h = (190, 230) if big else (160, 210)
    outline = f'M{cx - w} {cy + h} Q {cx - w - 30} {cy - h + 60} {cx} {cy - h} Q {cx + w + 30} {cy - h + 60} {cx + w} {cy + h}'
    cid = f'chest{cx}'
    s = f'<clipPath id="{cid}"><path d="{outline} Z"/></clipPath><path d="{outline}" fill="#FBF6EA" stroke="#9C8460" stroke-width="5"/><g clip-path="url(#{cid})">'
    for k in range(5):
        y = cy - h + 80 + k * 60
        tilt = -18 if big else 18
        s += f'<path d="M{cx - w - 40} {y + tilt} Q {cx} {y - 20} {cx + w + 40} {y + tilt}" fill="none" stroke="#C9B48A" stroke-width="6"/>'
    s += '</g>'
    s += f'<ellipse cx="{cx - 80}" cy="{cy + 10}" rx="{70 if big else 55}" ry="{140 if big else 115}" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="3"/>'
    s += f'<ellipse cx="{cx + 80}" cy="{cy + 10}" rx="{70 if big else 55}" ry="{140 if big else 115}" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="3"/>'
    dy = cy + h + (10 if big else -40)
    if big:
        s += f'<path d="M{cx - w} {dy} Q {cx} {dy - 30} {cx + w} {dy}" fill="none" stroke="{RED}" stroke-width="10"/>'
    else:
        s += f'<path d="M{cx - w} {dy + 40} Q {cx} {dy - 90} {cx + w} {dy + 40}" fill="none" stroke="{RED}" stroke-width="10"/>'
    s += text(cx, cy - h - 30, label_text, 'h', 'middle')
    return s


def ventilation() -> str:
    s = text(800, 56, 'Механизм вдоха и выдоха', 'h', 'middle')
    s += chest(400, 380, True, 'Вдох')
    s += arrow(400, 640, 400, 700, RED, 7) + text(470, 700, 'диафрагма опускается', 's', 'start', RED)
    s += arrow(180, 300, 150, 250, INK, 5) + arrow(620, 300, 650, 250, INK, 5)
    s += lines_at(400, 760, ['мышцы сокращаются, объём ↑,', 'давление в лёгких ниже атмосферного —', 'воздух входит'], 's')
    s += chest(1200, 380, False, 'Выдох')
    s += arrow(1200, 660, 1200, 560, RED, 7) + text(1225, 650, 'диафрагма поднимается', 's', 'start', RED)
    s += arrow(1000, 250, 1020, 300, INK, 5) + arrow(1400, 250, 1380, 300, INK, 5)
    s += lines_at(1200, 760, ['мышцы расслабляются, объём ↓,', 'давление выше атмосферного —', 'воздух выходит; спокойный выдох пассивный'], 's')
    return s


# 5. Состав воздуха --------------------------------------------------------------------------------
def air_composition() -> str:
    s = text(650, 56, 'Состав вдыхаемого и выдыхаемого воздуха', 'h', 'middle')
    rows = [('O₂', 20.95, 16.0, '20,95 %', '16 %', '−4,95'), ('CO₂', 0.03, 4.0, '0,03 %', '4 %', '+3,97')]
    base, scale = 600, 17
    for k, (gas, a, b, ta, tb, diff) in enumerate(rows):
        x = 170 + k * 560
        s += text(x + 165, 150, gas.replace('₂', '<tspan baseline-shift="-0.28em" font-size="68%">2</tspan>'), 'h', 'middle')
        for j, (v, t, col, cap) in enumerate(((a, ta, LBLUE, 'вдыхаемый'), (b, tb, LRED, 'выдыхаемый'))):
            bx = x + j * 180
            h = max(v * scale, 6)
            s += f'<rect x="{bx}" y="{base - h}" width="150" height="{h}" fill="{col}" stroke="{INK}" stroke-width="2"/>'
            s += text(bx + 75, base - h - 14, t, 't', 'middle') + text(bx + 75, base + 36, cap, 'cap', 'middle')
        s += text(x + 165, base + 90, f'разность {diff} п. п.', 's', 'middle', RED)
    s += f'<path d="M130 {base} H 1170" stroke="{INK}" stroke-width="3"/>'
    s += text(650, base + 150, 'Азот (около 78 %) при дыхании практически не меняется.', 't', 'middle')
    return s


# 6. Объёмы лёгких ---------------------------------------------------------------------------------
def lung_volumes() -> str:
    s = text(650, 56, 'Объёмы лёгких', 'h', 'middle')
    x0, top = 140, 120
    parts = [('глубокий вдох сверх спокойного', 170, '#E8EEF8'), ('дыхательный объём ≈ 0,5 л', 70, '#BFD0EE'),
             ('резервный объём выдоха', 150, '#E8EEF8'), ('остаточный объём', 120, '#EFE7D6')]
    y = top
    for name, h, fill in parts:
        s += f'<rect x="{x0}" y="{y}" width="160" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        s += text(x0 + 180, y + h / 2 + 9, name, 's')
        y += h
    zt, zb = top, top + 170 + 70 + 150
    s += f'<path d="M{x0 - 20} {zt} H {x0 - 40} V {zb} H {x0 - 20}" fill="none" stroke="{RED}" stroke-width="4"/>'
    s += f'<text x="{x0 - 60}" y="{(zt + zb) / 2}" text-anchor="middle" transform="rotate(-90 {x0 - 60} {(zt + zb) / 2})" style="font-size:30px;font-weight:800;fill:{RED}">ЖЕЛ</text>'
    # спирограмма на той же шкале
    gx, gw = 760, 480
    s += f'<rect x="{gx}" y="{top - 20}" width="{gw}" height="{zb - top + 40}" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    mid = top + 170 + 35
    pts = []
    for i in range(240):
        x = gx + 15 + i * 1.9
        if 120 <= i < 170:
            ph = (i - 120) / 50
            yv = mid - 205 * math.sin(ph * 2 * math.pi) if ph < 0.5 else mid + 185 * math.sin((ph - 0.5) * 2 * math.pi)
        else:
            yv = mid - 35 * math.sin(i / 20 * 2 * math.pi)
        pts.append(f'{x:.0f},{yv:.0f}')
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{BLUE}" stroke-width="4"/>'
    s += text(gx + 15 + 132 * 1.9 - 16, top + 25, 'глубокий вдох', 'cap', 'end')
    s += text(gx + 15 + 158 * 1.9 - 16, zb - 10, 'максимальный выдох', 'cap', 'end')
    s += text(gx + 125, mid + 85, 'спокойное дыхание', 'cap', 'middle')
    s += text(650, zb + 180, 'ЖЕЛ — максимальный выдох после самого глубокого вдоха; остаточный объём в неё не входит.', 's', 'middle')
    s += text(650, zb + 220, 'Измеряют спирометром.', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'gas-exchange-groups.png': (gas_exchange_groups(), 1600, 630),
        'human-airways.png': (human_airways(), 1200, 940),
        'alveolus-capillary.png': (alveolus_capillary(), 1200, 700),
        'ventilation.png': (ventilation(), 1600, 880),
        'air-composition.png': (air_composition(), 1300, 820),
        'lung-volumes.png': (lung_volumes(), 1300, 770),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
