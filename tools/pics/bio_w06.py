"""Рисунки недели 6 биологии (course/biology/week-06/pics/*.png): ксилема и флоэма, кольцевание, состав крови, иммунитет,
совместимость ABO, клапаны сердца, типы сосудов, круги кровообращения.

Факты — по выжимке course/textbooks/bio-06-transport.md (Б7а § 20, Б7м с. 80–84, Б8 § 16–24). Схемы условные, не анатомический атлас.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w06.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, LIGHT_GREEN, PAPER, RED, ROOT, arrow, chem, label, render, text

OUT = ROOT / 'course' / 'biology' / 'week-06' / 'pics'
BLUE, LBLUE, LRED = '#3A57A7', '#DCE6F5', '#FBE3E4'
WOOD, WOOD_LINE, BARK, BARK_LINE = '#F1E2BE', '#B89A5A', '#A7825E', '#6F5236'
PLASMA, CELLS = '#F6DE8A', '#C8343C'


def lbl(px, py, tx, ty, s, color=INK):
    return label(px, py, tx, ty, s, 's', color)


def swatch(x, y, fill, stroke, s, color=INK):
    """Строка легенды: цветной квадрат и подпись."""
    return (f'<rect x="{x}" y="{y - 24}" width="30" height="30" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + text(x + 44, y, s, 's', fill=color))


def lines_at(x, y, rows, cls='s', anchor='middle', step=32):
    """Несколько строк текста: rows — список (строка, цвет | None)."""
    return ''.join(text(x, y + j * step, chem(t), cls, anchor, c) for j, (t, c) in enumerate(rows))


# 1. Ксилема и флоэма ---------------------------------------------------------------------------
def xylem_phloem() -> str:
    s = text(850, 56, 'Ксилема и флоэма: где лежат и что проводят', 'h', 'middle')
    # стебель (поперечный срез)
    cx, cy = 260, 340
    s += text(cx, 130, 'Стебель (срез)', 't', 'middle')
    s += f'<circle cx="{cx}" cy="{cy}" r="180" fill="{BARK}" stroke="{BARK_LINE}" stroke-width="4"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="150" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="120" fill="{WOOD}" stroke="{WOOD_LINE}" stroke-width="3"/>'
    for k in range(26):
        a, r = k * 2.4, 50 + (k * 37) % 60
        s += f'<circle cx="{cx + r * math.cos(a):.0f}" cy="{cy + r * math.sin(a):.0f}" r="7" fill="#fff" stroke="{WOOD_LINE}" stroke-width="2"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="34" fill="#FBF6EA" stroke="{WOOD_LINE}" stroke-width="2"/>'
    s += swatch(110, 590, BARK, BARK_LINE, 'кора')
    s += swatch(110, 634, LIGHT_GREEN, GREEN, 'луб — флоэма', GREEN)
    s += swatch(110, 678, WOOD, WOOD_LINE, 'древесина — ксилема', '#8A6A2A')
    # корень (поперечный срез): ксилема звёздочкой, флоэма между лучами
    cx = 720
    s += text(cx, 130, 'Корень (срез)', 't', 'middle')
    s += f'<circle cx="{cx}" cy="{cy}" r="180" fill="#EFE7D6" stroke="{BARK_LINE}" stroke-width="4"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="115" fill="#F8F3E6" stroke="{GREY}" stroke-width="3"/>'
    star = []
    for k in range(8):
        a = math.radians(k * 45 - 90)
        r = 96 if k % 2 == 0 else 32
        star.append(f'{cx + r * math.cos(a):.0f},{cy + r * math.sin(a):.0f}')
    s += f'<polygon points="{" ".join(star)}" fill="{WOOD}" stroke="{WOOD_LINE}" stroke-width="3"/>'
    for k in range(4):
        a = math.radians(k * 90 - 45)
        s += f'<circle cx="{cx + 66 * math.cos(a):.0f}" cy="{cy + 66 * math.sin(a):.0f}" r="21" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="3"/>'
    s += swatch(560, 590, WOOD, WOOD_LINE, 'ксилема — «звёздочкой»', '#8A6A2A')
    s += swatch(560, 634, LIGHT_GREEN, GREEN, 'флоэма — между её лучами', GREEN)
    s += text(560, 678, 'в центральном цилиндре', 'cap')
    # схема токов
    x1, x2, top, bot = 1200, 1520, 140, 580
    s += f'<rect x="{x1 - 40}" y="{top}" width="80" height="{bot - top}" rx="10" fill="{WOOD}" stroke="{WOOD_LINE}" stroke-width="3"/>'
    for y in range(top + 60, bot, 90):
        s += f'<path d="M{x1 - 40} {y} H {x1 + 40}" stroke="{WOOD_LINE}" stroke-width="2" stroke-dasharray="6 6"/>'
    s += arrow(x1, bot - 30, x1, top + 30, BLUE, 8)
    s += f'<rect x="{x2 - 40}" y="{top}" width="80" height="{bot - top}" rx="10" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="3"/>'
    for y in range(top + 90, bot, 120):
        s += f'<path d="M{x2 - 40} {y} H {x2 + 40}" stroke="{GREEN}" stroke-width="5" stroke-dasharray="4 6"/>'
        s += f'<ellipse cx="{x2 + 54}" cy="{y - 40}" rx="12" ry="26" fill="#fff" stroke="{GREEN}" stroke-width="2"/>'
    s += arrow(x2, 300, x2, bot - 30, GREEN, 8) + arrow(x2, 280, x2, top + 30, GREEN, 5)
    s += lines_at(x1, 620, [('ксилема', '#8A6A2A'), ('сосуды — мёртвые', None), ('вода и соли ↑', BLUE), ('от корня к листьям', BLUE)])
    s += lines_at(x2, 620, [('флоэма', GREEN), ('ситовидные трубки —', None), ('живые, с клетками-', None), ('спутницами', None)])
    s += lines_at(x2, 752, [('сахароза из листа', GREEN), ('к корню и к побегу', GREEN)])
    return s


# 2. Кольцевание ------------------------------------------------------------------------------
def girdling() -> str:
    s = text(650, 56, 'Опыт с кольцеванием', 'h', 'middle')
    x0, w = 560, 60
    jl, jr = x0 - 140, x0 + w + 140
    s += f'<path d="M{jl} 560 L {jl} 880 Q {jl} 900 {jl + 20} 900 L {jr - 20} 900 Q {jr} 900 {jr} 880 L {jr} 560" fill="{LBLUE}" fill-opacity=".6" stroke="{GREY}" stroke-width="4"/>'
    s += f'<path d="M{jl} 640 H {jr}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="10 8"/>'
    s += text(x0 + w / 2, 875, 'вода', 'cap', 'middle')
    ring_top, ring_bot = 470, 530
    s += f'<rect x="{x0}" y="120" width="{w}" height="{ring_top - 120}" fill="{BARK}" stroke="{BARK_LINE}" stroke-width="3"/>'
    s += f'<rect x="{x0 + 8}" y="{ring_top}" width="{w - 16}" height="{ring_bot - ring_top}" fill="{WOOD}" stroke="{WOOD_LINE}" stroke-width="3"/>'
    s += f'<rect x="{x0}" y="{ring_bot}" width="{w}" height="300" fill="{BARK}" stroke="{BARK_LINE}" stroke-width="3"/>'
    s += (f'<path d="M{x0} {ring_top - 70} C {x0 - 26} {ring_top - 50} {x0 - 26} {ring_top - 10} {x0} {ring_top} H {x0 + w} '
          f'C {x0 + w + 26} {ring_top - 10} {x0 + w + 26} {ring_top - 50} {x0 + w} {ring_top - 70} Z" fill="{BARK}" stroke="{BARK_LINE}" stroke-width="3"/>')
    for dx, ang in ((-10, 200), (-6, 160), (w + 10, -20), (w + 6, 20)):
        bx, by = x0 + dx, ring_top - 20
        ex, ey = bx + 60 * math.cos(math.radians(ang)), by + 60 * math.sin(math.radians(ang)) + 40
        s += f'<path d="M{bx} {by} Q {(bx + ex) / 2:.0f} {by + 50} {ex:.0f} {ey:.0f}" fill="none" stroke="{BARK_LINE}" stroke-width="4"/>'
    for lx, ly, rot in ((x0 - 40, 170, -30), (x0 + w + 40, 230, 30), (x0 - 40, 300, -30)):
        s += f'<ellipse cx="{lx}" cy="{ly}" rx="60" ry="24" fill="{GREEN}" opacity=".85" transform="rotate({rot} {lx} {ly})"/>'
    s += arrow(x0 + w / 2, 820, x0 + w / 2, 160, BLUE, 5)
    gx = x0 + w + 120
    s += arrow(gx, 180, gx, ring_top - 40, GREEN, 6)
    s += f'<path d="M{gx - 18} {ring_top - 20} H {gx + 18}" stroke="{RED}" stroke-width="6"/>'
    s += lbl(x0 - 18, ring_top - 40, 380, 400, 'наплыв и придаточные корни')
    s += lbl(x0 + 8, ring_top + 30, 380, 560, 'снято кольцо коры с лубом,')
    s += text(372, 594, 'древесина цела', 's', 'end')
    s += lines_at(gx + 24, 230, [('органические вещества', None), ('идут вниз по лубу', None)], anchor='start')
    s += lines_at(gx + 24, ring_top - 10, [('путь прерван —', RED), ('вещества копятся над кольцом', RED)], anchor='start')
    s += lines_at(jr + 24, 720, [('вода и соли идут вверх', BLUE), ('по древесине (ксилеме)', BLUE)], anchor='start')
    return s


# 3. Состав крови ------------------------------------------------------------------------------
def blood_cells() -> str:
    s = text(800, 56, 'Состав крови человека', 'h', 'middle')
    tx, top, bot, w = 110, 130, 760, 120
    split = top + (bot - top) * 0.55
    s += f'<rect x="{tx}" y="{top}" width="{w}" height="{split - top}" fill="{PLASMA}"/>'
    s += f'<path d="M{tx} {split} H {tx + w} V {bot - 60} A 60 60 0 0 1 {tx} {bot - 60} Z" fill="{CELLS}"/>'
    s += f'<path d="M{tx} {top - 20} V {bot - 60} A 60 60 0 0 0 {tx + w} {bot - 60} V {top - 20}" fill="none" stroke="{INK}" stroke-width="5"/>'
    s += lines_at(tx + w + 20, top + 110, [('плазма — 55 %', None)], 't', 'start')
    s += lines_at(tx + w + 20, top + 146, [('вода, белки,', None), ('в том числе', None), ('фибриноген', None)], 's', 'start')
    s += lines_at(tx + w + 20, split + 110, [('клетки', None), ('крови — 45 %', None)], 't', 'start', 36)
    cards = [('Эритроциты', ['без ядра,', 'двояковогнутый диск;', 'гемоглобин переносит', 'O₂ и CO₂;', 'живут около 120 суток']),
             ('Лейкоциты', ['единственные', 'клетки с ядром;', 'защищают от', 'микроорганизмов']),
             ('Тромбоциты', ['мелкие, без ядра;', 'нужны для', 'свёртывания крови;', 'живут 8–11 суток'])]
    for k, (title, rows) in enumerate(cards):
        x = 470 + k * 375
        s += f'<rect x="{x}" y="140" width="350" height="580" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        s += text(x + 175, 190, title, 't', 'middle')
        cx, cy = x + 175, 300
        if k == 0:
            s += f'<circle cx="{cx}" cy="{cy}" r="74" fill="#E2545B"/><circle cx="{cx}" cy="{cy}" r="34" fill="#F2878B"/>'
            s += (f'<path d="M{cx - 76} {cy + 120} Q {cx - 38} {cy + 92} {cx} {cy + 112} Q {cx + 38} {cy + 92} {cx + 76} {cy + 120} '
                  f'Q {cx + 38} {cy + 148} {cx} {cy + 128} Q {cx - 38} {cy + 148} {cx - 76} {cy + 120} Z" fill="#E2545B"/>')
            s += text(cx, cy + 172, 'вид сбоку', 'cap', 'middle')
        elif k == 1:
            s += f'<circle cx="{cx}" cy="{cy + 20}" r="86" fill="#EEE8F6" stroke="#8C7BB8" stroke-width="3"/>'
            s += ''.join(f'<circle cx="{cx + dx}" cy="{cy + 20 + dy}" r="25" fill="#7D62B5"/>' for dx, dy in ((-30, -10), (12, -26), (28, 18), (-8, 30)))
            s += text(cx, cy + 150, 'ядро', 'cap', 'middle')
        else:
            for dx, dy, r in ((-50, 0, 16), (10, -20, 12), (40, 30, 18), (-20, 60, 13), (60, 80, 11), (-70, 70, 10)):
                s += f'<path d="M{cx + dx - r} {cy + dy} q {r * 0.4} {-r} {r} {-r * 0.8} q {r} {r * 0.3} {r} {r * 0.9} q {-r * 0.6} {r} {-r * 1.2} {r * 0.7} Z" fill="#C9A7D9" stroke="#8E5FA8" stroke-width="2"/>'
        s += lines_at(x + 175, 530, [(r, None) for r in rows])
    s += text(800, 772, 'Все клетки крови образуются в красном костном мозге.', 't', 'middle')
    return s


# 4. Иммунитет ---------------------------------------------------------------------------------
def box(x, y, w, h, title, rows, fill, stroke):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
    s += text(x + w / 2, y + 40, title, 't', 'middle')
    return s + ''.join(text(x + w / 2, y + 78 + j * 32, ln, 's', 'middle') for j, ln in enumerate(rows))


def immunity() -> str:
    s = text(800, 56, 'Виды иммунитета', 'h', 'middle')
    s += box(620, 100, 360, 70, 'Иммунитет', [], PAPER, INK)
    s += box(220, 230, 440, 70, 'Естественный', [], LIGHT_GREEN, GREEN) + box(940, 230, 440, 70, 'Искусственный', [], LBLUE, BLUE)
    s += arrow(740, 170, 480, 228, INK, 4) + arrow(860, 170, 1120, 228, INK, 4)
    leaves = [(40, 'Врождённый', ['передаётся', 'по наследству'], LIGHT_GREEN, GREEN, 440),
              (420, 'Приобретённый', ['после перенесённой', 'болезни (корь, краснуха)'], LIGHT_GREEN, GREEN, 440),
              (820, 'Активный', ['вакцина: убитые или', 'ослабленные возбудители,', 'свои антитела, надолго'], LBLUE, BLUE, 1160),
              (1200, 'Пассивный', ['лечебная сыворотка:', 'готовые антитела,', 'действует недолго'], LBLUE, BLUE, 1160)]
    for x, title, rows, fill, stroke, px in leaves:
        s += box(x, 360, 360, 190, title, rows, fill, stroke)
        s += arrow(px, 300, x + 180, 358, INK, 4)
    s += f'<rect x="40" y="600" width="1520" height="160" rx="16" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    cells = [('Фагоциты', 'захватывают и переваривают', 'частицы (И. И. Мечников)'),
             ('В-лимфоциты', 'вырабатывают антитела;', 'созревают в красном костном мозге'),
             ('Т-лимфоциты', 'клеточный иммунитет; созревают', 'в тимусе; это не фагоциты')]
    for k, (t1, l1, l2) in enumerate(cells):
        x = 60 + k * 500
        s += text(x + 240, 645, t1, 't', 'middle') + text(x + 240, 683, l1, 's', 'middle') + text(x + 240, 715, l2, 's', 'middle')
    return s


# 5. Совместимость ABO -------------------------------------------------------------------------
def abo() -> str:
    s = text(560, 56, 'Переливание эритроцитов: группы ABO', 'h', 'middle')
    ok = {('I', g) for g in ('I', 'II', 'III', 'IV')} | {('II', 'II'), ('II', 'IV'), ('III', 'III'), ('III', 'IV'), ('IV', 'IV')}
    groups = ['I', 'II', 'III', 'IV']
    x0, y0, c = 330, 220, 140
    s += text(x0 + 2 * c, 150, 'получатель →', 't', 'middle')
    s += text(x0 - 150, y0 + 2 * c, 'донор ↓', 't', 'middle')
    for j, g in enumerate(groups):
        s += text(x0 + j * c + c / 2, y0 - 20, g, 't', 'middle')
        s += text(x0 - 30, y0 + j * c + c / 2 + 10, g, 't', 'end')
    for i, d in enumerate(groups):
        for j, r in enumerate(groups):
            good = (d, r) in ok
            x, y = x0 + j * c, y0 + i * c
            s += f'<rect x="{x}" y="{y}" width="{c - 8}" height="{c - 8}" rx="12" fill="{LIGHT_GREEN if good else LRED}" stroke="{GREEN if good else RED}" stroke-width="3"/>'
            mx, my = x + (c - 8) / 2, y + (c - 8) / 2
            if good:
                s += f'<path d="M{mx - 28} {my} L {mx - 6} {my + 24} L {mx + 32} {my - 24}" fill="none" stroke="{GREEN}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
            else:
                s += f'<path d="M{mx - 22} {my - 22} L {mx + 22} {my + 22} M{mx + 22} {my - 22} L {mx - 22} {my + 22}" stroke="{RED}" stroke-width="8" stroke-linecap="round"/>'
    s += text(560, 840, 'I — универсальный донор, IV — универсальный реципиент.', 't', 'middle')
    s += text(560, 882, 'Учебная таблица для эритроцитов, без резус-фактора.', 'cap', 'middle')
    s += text(560, 916, 'Сейчас переливают одногруппную кровь.', 'cap', 'middle')
    return s


# 6. Сердце и клапаны --------------------------------------------------------------------------
def heart(cx: float, cy: float, k: float = 1.0, names: bool = True) -> str:
    """Схема сердца спереди: слева на рисунке — правая сторона тела. Лёгочный ствол и аорта выходят вверх между предсердиями."""
    def R(x, y, w, h, fill, stroke):
        return f'<rect x="{cx + x * k:.0f}" y="{cy + y * k:.0f}" width="{w * k:.0f}" height="{h * k:.0f}" rx="{22 * k:.0f}" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
    s = R(-240, -210, 190, 170, LBLUE, BLUE) + R(50, -210, 190, 170, LRED, RED)
    s += R(-240, -30, 234, 230, LBLUE, BLUE) + R(6, -30, 234, 230, LRED, RED)
    for x0, n, col in ((-145, 3, BLUE), (145, 2, RED)):
        for i in range(n):
            bx = cx + (x0 + (i - (n - 1) / 2) * 30) * k
            s += f'<path d="M{bx - 13 * k:.0f} {cy - 36 * k:.0f} L {bx:.0f} {cy - 4 * k:.0f} L {bx + 13 * k:.0f} {cy - 36 * k:.0f} Z" fill="#fff" stroke="{col}" stroke-width="3"/>'
    for x, col in ((-28, BLUE), (28, RED)):
        s += f'<rect x="{cx + (x - 18) * k:.0f}" y="{cy - 300 * k:.0f}" width="{36 * k:.0f}" height="{272 * k:.0f}" fill="{col}"/>'
        s += f'<path d="M{cx + (x - 18) * k:.0f} {cy - 40 * k:.0f} q {9 * k:.0f} {14 * k:.0f} {18 * k:.0f} 0 q {9 * k:.0f} {14 * k:.0f} {18 * k:.0f} 0" fill="none" stroke="#fff" stroke-width="3"/>'
    if names:
        s += lines_at(cx - 145 * k, cy - 120 * k, [('правое', None), ('предсердие', None)], step=30)
        s += lines_at(cx + 145 * k, cy - 120 * k, [('левое', None), ('предсердие', None)], step=30)
        s += lines_at(cx - 123 * k, cy + 100 * k, [('правый', None), ('желудочек', None)], step=30)
        s += lines_at(cx + 123 * k, cy + 100 * k, [('левый', None), ('желудочек', None)], step=30)
    return s


def heart_valves() -> str:
    s = text(700, 56, 'Сердце человека: камеры и клапаны', 'h', 'middle')
    cx, cy = 700, 500
    s += f'<path d="M{cx - 200} {cy - 210} V {cy - 330}" stroke="{BLUE}" stroke-width="30"/>'
    s += f'<path d="M{cx - 240} {cy - 120} H {cx - 330}" stroke="{BLUE}" stroke-width="30"/>'
    s += f'<path d="M{cx + 240} {cy - 150} H {cx + 330} M{cx + 240} {cy - 90} H {cx + 330}" stroke="{RED}" stroke-width="22"/>'
    s += heart(cx, cy)
    s += lbl(cx - 200, cy - 300, cx - 260, cy - 340, 'полые вены', BLUE)
    s += lbl(cx - 28, cy - 290, cx - 110, cy - 380, 'лёгочный ствол', BLUE)
    s += lbl(cx + 28, cy - 290, cx + 110, cy - 380, 'аорта', RED)
    s += lbl(cx + 330, cy - 90, cx + 380, cy - 20, 'лёгочные вены', RED)
    s += lbl(cx - 145, cy - 20, cx - 330, cy + 40, 'трёхстворчатый', BLUE) + text(cx - 338, cy + 72, 'клапан', 's', 'end', BLUE)
    s += lbl(cx + 145, cy - 20, cx + 330, cy + 60, 'двустворчатый', RED) + text(cx + 338, cy + 92, 'клапан', 's', fill=RED)
    # полулунные: две выноски вниз вдоль перегородки
    s += (f'<path d="M{cx - 28} {cy - 34} L {cx - 16} {cy + 238} M{cx + 28} {cy - 34} L {cx + 16} {cy + 238}" stroke="{INK}" stroke-width="2.5"/>'
          f'<circle cx="{cx - 28}" cy="{cy - 34}" r="5"/><circle cx="{cx + 28}" cy="{cy - 34}" r="5"/>')
    s += text(cx, cy + 270, 'полулунные клапаны (у выхода лёгочного ствола и аорты)', 's', 'middle')
    s += text(cx - 380, cy + 320, '← правая сторона тела', 'cap') + text(cx + 380, cy + 320, 'левая сторона тела →', 'cap', 'end')
    s += text(700, cy + 380, 'Клапаны открываются в одну сторону и не дают крови течь обратно.', 't', 'middle')
    return s


# 7. Типы сосудов ------------------------------------------------------------------------------
def vessel_types() -> str:
    s = text(800, 56, 'Артерия, вена, капилляр', 'h', 'middle')
    cx, cy = 260, 330
    s += f'<circle cx="{cx}" cy="{cy}" r="150" fill="#E9DCC6" stroke="#9C8460" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="128" fill="#E8A0A4" stroke="{RED}" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="62" fill="#F7D9DA" stroke="#B55" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="56" fill="{RED}" opacity=".85"/>'
    s += lbl(cx + 140, cy - 50, cx + 190, cy - 170, 'наружный слой')
    s += lbl(cx + 90, cy + 40, cx + 190, cy + 190, 'толстый мышечный слой')
    s += lines_at(cx, 560, [('Артерия', None)], 't') + lines_at(cx, 594, [('кровь ОТ сердца,', None), ('давление высокое', None)])
    cx = 780
    s += f'<circle cx="{cx - 110}" cy="{cy}" r="110" fill="#E9DCC6" stroke="#9C8460" stroke-width="3"/>'
    s += f'<circle cx="{cx - 110}" cy="{cy}" r="96" fill="#E3B3B5" stroke="{BLUE}" stroke-width="3"/>'
    s += f'<circle cx="{cx - 110}" cy="{cy}" r="80" fill="{BLUE}" opacity=".75"/>'
    s += f'<rect x="{cx + 20}" y="{cy - 70}" width="160" height="140" fill="{BLUE}" opacity=".75" stroke="#9C8460" stroke-width="6"/>'
    s += f'<path d="M{cx + 22} {cy - 64} Q {cx + 90} {cy - 40} {cx + 110} {cy - 4} M{cx + 22} {cy + 64} Q {cx + 90} {cy + 40} {cx + 110} {cy + 4}" fill="none" stroke="#fff" stroke-width="7"/>'
    s += arrow(cx + 40, cy, cx + 170, cy, '#fff', 4)
    s += lbl(cx + 100, cy - 30, cx + 150, cy - 170, 'клапан')
    s += lines_at(cx + 30, 560, [('Вена', None)], 't') + lines_at(cx + 30, 594, [('кровь К сердцу,', None), ('стенка тоньше, есть клапаны', None)])
    cx = 1330
    s += f'<rect x="{cx - 160}" y="{cy - 40}" width="320" height="80" rx="40" fill="#F4C6C8" stroke="{RED}" stroke-width="3"/>'
    s += ''.join(f'<path d="M{cx - 150 + i * 40} {cy - 40} v 80" stroke="{RED}" stroke-width="1.5" opacity=".6"/>' for i in range(1, 8))
    for i in range(5):
        s += f'<ellipse cx="{cx - 110 + i * 55}" cy="{cy}" rx="18" ry="11" fill="#E2545B"/>'
    s += arrow(cx - 90, cy - 50, cx - 90, cy - 130, RED, 4) + arrow(cx + 90, cy - 130, cx + 90, cy - 50, GREY, 4)
    s += text(cx - 100, cy - 145, chem('O₂, вещества'), 'cap', 'end') + text(cx + 80, cy - 145, chem('CO₂, отходы'), 'cap', 'start')
    s += text(cx - 100, cy - 175, 'в ткани', 'cap', 'end') + text(cx + 80, cy - 175, 'из тканей', 'cap', 'start')
    s += lbl(cx + 120, cy + 38, cx + 60, cy + 150, 'стенка — один слой клеток')
    s += lines_at(cx, 560, [('Капилляр', None)], 't') + lines_at(cx, 594, [('обмен веществ и газов,', None), ('кровь течёт медленно', None)])
    return s


# 8. Круги кровообращения ----------------------------------------------------------------------
def tag(x, y, n, color):
    return (f'<circle cx="{x}" cy="{y}" r="24" fill="#fff" stroke="{color}" stroke-width="4"/>'
            f'<text x="{x}" y="{y + 9}" text-anchor="middle" style="font-size:26px;font-weight:800;fill:{color}">{n}</text>')


def tri(x, y, dx, dy, color, size=30):
    """Крупный треугольник-указатель на линии сосуда: (dx, dy) — направление тока."""
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    pts = [(x + ux * size, y + uy * size), (x - ux * size * 0.6 + px * size * 0.8, y - uy * size * 0.6 + py * size * 0.8),
           (x - ux * size * 0.6 - px * size * 0.8, y - uy * size * 0.6 - py * size * 0.8)]
    return f'<polygon points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="{color}" stroke="#fff" stroke-width="3"/>'


def circulation() -> str:
    s = text(700, 56, 'Большой и малый круги кровообращения', 'h', 'middle')
    cx, cy, k = 700, 640, 0.75
    top = cy - 300 * k
    # лёгкие и органы
    s += f'<ellipse cx="{cx}" cy="200" rx="340" ry="85" fill="#F8D7DA" stroke="#C77" stroke-width="3"/>'
    s += text(cx, 195, 'капилляры лёгких', 't', 'middle') + text(cx, 232, 'венозная кровь → артериальная', 'cap', 'middle')
    s += f'<rect x="{cx - 260}" y="990" width="520" height="110" rx="20" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
    s += text(cx, 1035, 'капилляры органов', 't', 'middle') + text(cx, 1072, 'артериальная кровь → венозная', 'cap', 'middle')
    # ① лёгочный ствол: ПЖ → лёгкие
    s += f'<path d="M{cx - 21} {top} C {cx - 21} 330 {cx - 180} 330 {cx - 230} 272" fill="none" stroke="{BLUE}" stroke-width="16"/>'
    s += tri(cx - 190, 300, -1, -0.75, BLUE)
    # ③ аорта и артерии: ЛЖ → органы (вправо и вниз)
    s += (f'<path d="M{cx + 21} {top} C {cx + 21} 360 {cx + 80} 350 {cx + 200} 350 L {cx + 460} 350 C {cx + 560} 350 {cx + 580} 420 {cx + 580} 520 '
          f'L {cx + 580} 860 C {cx + 580} 990 {cx + 450} 1045 {cx + 262} 1045" fill="none" stroke="{RED}" stroke-width="16"/>')
    s += tri(cx + 580, 720, 0, 1, RED) + tri(cx + 380, 1045, -1, 0, RED) + tri(cx + 470, 352, 1, 0, RED)
    # ④ вены и полые вены: органы → ПП (слева и вверх)
    s += (f'<path d="M{cx - 262} 1045 C {cx - 450} 1045 {cx - 580} 990 {cx - 580} 860 L {cx - 580} 600 C {cx - 580} 540 {cx - 420} 546 {cx - 182} 546" '
          f'fill="none" stroke="{BLUE}" stroke-width="16"/>')
    s += tri(cx - 580, 760, 0, -1, BLUE) + tri(cx - 300, 546, 1, 0, BLUE) + tri(cx - 380, 1045, -1, 0, BLUE)
    # ② лёгочные вены: лёгкие → ЛП, поверх аорты (мостик)
    pv = f'M{cx + 230} 272 C {cx + 330} 300 {cx + 330} 420 {cx + 330} 500 C {cx + 330} 540 {cx + 260} 552 {cx + 182} 552'
    s += f'<path d="{pv}" fill="none" stroke="#fff" stroke-width="30"/><path d="{pv}" fill="none" stroke="{RED}" stroke-width="16"/>'
    s += tri(cx + 330, 420, 0, 1, RED)
    s += heart(cx, cy, k, names=False)
    for x, y, t in ((-100, -110, 'ПП'), (100, -110, 'ЛП'), (-112, 100, 'ПЖ'), (112, 100, 'ЛЖ')):
        s += text(cx + x * k, cy + y * k + 10, t, 't', 'middle')
    # номера и названия кругов
    s += tag(cx - 110, 360, 1, BLUE) + tag(cx + 360, 440, 2, RED) + tag(cx + 620, 620, 3, RED) + tag(cx - 620, 620, 4, BLUE)
    s += text(cx, 920, 'большой круг', 'h', 'middle') + text(cx, 320, 'малый круг', 'cap', 'middle')
    # легенда
    rows = [('1', 'лёгочный ствол: из правого желудочка в лёгкие — венозная кровь', BLUE),
            ('2', 'лёгочные вены: из лёгких в левое предсердие — артериальная кровь', RED),
            ('3', 'аорта → артерии: из левого желудочка к органам — артериальная кровь', RED),
            ('4', 'вены → полые вены: от органов в правое предсердие — венозная кровь', BLUE)]
    for j, (n, t, col) in enumerate(rows):
        y = 1160 + j * 44
        s += tag(150, y - 9, n, col) + text(190, y, t, 's')
    s += text(cx, 1360, 'ПП, ЛП — правое и левое предсердия; ПЖ, ЛЖ — правый и левый желудочки', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'xylem-phloem.png': (xylem_phloem(), 1700, 830),
        'girdling.png': (girdling(), 1300, 940),
        'blood-cells.png': (blood_cells(), 1600, 800),
        'immunity.png': (immunity(), 1600, 790),
        'abo-compatibility.png': (abo(), 1120, 950),
        'heart-valves.png': (heart_valves(), 1400, 910),
        'vessel-types.png': (vessel_types(), 1600, 680),
        'circulation.png': (circulation(), 1400, 1390),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
