"""Рисунки недели 18 биологии (course/biology/week-18/pics/*.png): лестница таксонов, пять царств, грибы, отделы растений,
однодольные и двудольные, типы беспозвоночных, классы членистоногих, классы позвоночных, схема дихотомического ключа.

Факты — по выжимке course/textbooks/bio-18-diversity-systematics.md (Б7м § 9–12; Б7а § 8–10; Б8 § 6–9; Б9 § 3).
Схемы условные. Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w18.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    return _text(x, y, chem(s), cls, anchor, fill)

OUT = ROOT / 'course' / 'biology' / 'week-18' / 'pics'
BLUE, ORANGE, PURPLE, BROWN, LEAF = '#3A57A7', '#D98A2B', '#8E44AD', '#8A5A2B', '#5DAA6F'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32, color=color))


def leaf(cx, cy, rx, ry, rot, fill=LEAF):
    return f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx:.0f} {cy:.0f})" fill="{fill}" stroke="#1F5E36" stroke-width="2"/>'


# 1. Лестница таксонов -----------------------------------------------------------------------------
def taxa_ladder():
    s = text(900, 52, 'Таксоны: от царства до вида', 'h', 'middle')
    s += card(30, 90, 1060, 900) + card(1120, 90, 650, 900)
    plants = ['Царство', 'Отдел', 'Класс', 'Порядок', 'Семейство', 'Род', 'Вид']
    animals = ['Царство', 'Тип', 'Класс', 'Отряд', 'Семейство', 'Род', 'Вид']
    s += text(300, 150, 'Растения', 't', 'middle', GREEN) + text(800, 150, 'Животные', 't', 'middle', BLUE)
    for k, (p, a) in enumerate(zip(plants, animals)):
        y = 220 + k * 110
        diff = p != a
        w = 380 - k * 30
        s += box(300, y, w, 76, p, '#FBE3E4' if diff else '#fff', RED if diff else INK, 't')
        s += box(800, y, w, 76, a, '#FBE3E4' if diff else '#fff', RED if diff else INK, 't')
    s += text(550, 970, 'сверху — самый крупный таксон, внизу — вид, наименьший', 's', 'middle')
    s += text(1445, 150, 'Сосна обыкновенная', 't', 'middle', GREEN)
    s += lines_at(1445, 200, ['Растения → Голосеменные', '→ Хвойные → Хвойные', '→ Сосновые → Сосна', '→ Сосна обыкновенная'], 's', step=38)
    s += text(1445, 420, 'Архар', 't', 'middle', BLUE)
    s += lines_at(1445, 470, ['Животные → Хордовые', '→ Млекопитающие', '→ Парнокопытные → Полорогие', '→ Горные бараны → Архар'], 's', step=38)
    s += lines_at(1445, 720, ['Бинарное название:', 'первое слово — род,', 'вид — оба слова', '(лютик едкий, Homo sapiens)'], 's', step=38, color=RED)
    return s


# 2. Пять царств -------------------------------------------------------------------------------------
def kingdoms():
    s = text(900, 52, 'Пять царств живой природы', 'h', 'middle')
    items = [('Вирусы', '#9A9A9A', ['неклеточные', 'размножаются только', 'в живых клетках']),
             ('Прокариоты', BLUE, ['нет оформленного', 'ядра; одноклеточные;', 'появились первыми']),
             ('Грибы', BROWN, ['хитин, гликоген;', 'всасывают вещества;', 'неподвижны']),
             ('Растения', GREEN, ['хлорофилл,', 'фотосинтез;', 'неподвижны']),
             ('Животные', ORANGE, ['готовая пища;', 'подвижны;', '~2 млн видов'])]
    for k, (name, col, rows) in enumerate(items):
        x = 30 + k * 350
        s += card(x, 90, 330, 640)
        cx = x + 165
        if k == 0:
            s += f'<polygon points="{cx},200 {cx + 50},230 {cx + 50},290 {cx},320 {cx - 50},290 {cx - 50},230" fill="none" stroke="{col}" stroke-width="6"/>'
            s += f'<line x1="{cx}" y1="320" x2="{cx}" y2="370" stroke="{col}" stroke-width="6"/>'
        elif k == 1:
            s += f'<rect x="{cx - 80}" y="220" width="160" height="90" rx="45" fill="#E3EEF7" stroke="{col}" stroke-width="5"/>'
            s += f'<path d="M{cx - 40} 265 q 20 -25 40 0 t 40 0" fill="none" stroke="{col}" stroke-width="4"/>'
        elif k == 2:
            s += f'<path d="M{cx - 80} 260 Q {cx} 170 {cx + 80} 260 Z" fill="{col}"/><rect x="{cx - 18}" y="258" width="36" height="90" fill="#E8D8C0" stroke="{INK}" stroke-width="2"/>'
        elif k == 3:
            s += f'<line x1="{cx}" y1="370" x2="{cx}" y2="200" stroke="{GREEN}" stroke-width="7"/>' + leaf(cx - 40, 260, 45, 20, -30) + leaf(cx + 40, 300, 45, 20, 30)
        else:
            s += f'<ellipse cx="{cx}" cy="290" rx="80" ry="50" fill="{col}"/><circle cx="{cx + 85}" cy="250" r="34" fill="{col}"/>'
            s += ''.join(f'<line x1="{cx + dx}" y1="330" x2="{cx + dx}" y2="375" stroke="{col}" stroke-width="10"/>' for dx in (-50, -20, 30, 60))
        s += text(cx, 440, name, 't', 'middle', col)
        s += lines_at(cx, 500, rows, 's', step=36)
    s += text(900, 780, 'Грибы, растения и животные — эукариоты: клетки с ядром', 't', 'middle')
    return s


# 3. Грибы --------------------------------------------------------------------------------------
def fungi():
    s = text(900, 52, 'Грибы: мукор, пеницилл, дрожжи, шляпочные', 'h', 'middle')
    for k in range(4):
        s += card(30 + k * 440, 90, 420, 760)
    # мукор: одна ветвистая клетка, много ядер, чёрные головки
    cx = 240
    s += f'<path d="M{cx - 150} 560 H {cx + 150} M{cx - 90} 560 V 300 M{cx} 560 V 260 M{cx + 90} 560 V 320" fill="none" stroke="#C9C2B4" stroke-width="12" stroke-linecap="round"/>'
    for x, y in ((cx - 90, 285), (cx, 245), (cx + 90, 305)):
        s += f'<circle cx="{x}" cy="{y}" r="26" fill="{INK}"/>'
    for j in range(9):
        s += f'<circle cx="{cx - 130 + j * 30}" cy="560" r="4" fill="{BLUE}"/>'
    s += text(cx, 160, 'Мукор', 't', 'middle') + lines_at(cx, 650, ['одна многоядерная', 'клетка; белая плесень;', 'споры чёрные'], 's', step=36)
    # пеницилл: перегородки, кисточки
    cx = 680
    s += f'<path d="M{cx - 150} 560 H {cx + 150} M{cx} 560 V 300" fill="none" stroke="#7FA88A" stroke-width="12" stroke-linecap="round"/>'
    s += ''.join(f'<line x1="{cx - 150 + j * 50}" y1="548" x2="{cx - 150 + j * 50}" y2="572" stroke="{INK}" stroke-width="3"/>' for j in range(7))
    for dx in (-40, -15, 15, 40):
        s += f'<line x1="{cx}" y1="300" x2="{cx + dx}" y2="250" stroke="#7FA88A" stroke-width="7"/>'
        s += ''.join(f'<circle cx="{cx + dx * 1.1}" cy="{240 - j * 18}" r="7" fill="#3E8E78"/>' for j in range(4))
    s += text(cx, 160, 'Пеницилл', 't', 'middle') + lines_at(cx, 650, ['многоклеточный,', 'сине-зелёный;', 'пенициллин'], 's', step=36)
    # дрожжи: почкующиеся клетки
    cx = 1120
    for x, y, r in ((cx - 50, 380, 60), (cx + 60, 340, 45), (cx + 20, 470, 50)):
        s += f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.8:.0f}" fill="#F3E3C9" stroke="{INK}" stroke-width="3"/>'
    s += f'<ellipse cx="{cx + 108}" cy="300" rx="22" ry="18" fill="#F3E3C9" stroke="{INK}" stroke-width="3"/>'
    s += text(cx + 150, 270, 'почка', 's', 'start', RED)
    s += text(cx, 160, 'Дрожжи', 't', 'middle') + lines_at(cx, 650, ['одноклеточные;', 'почкование;', 'сахар → спирт + CO₂'], 's', step=36)
    # шляпочный
    cx = 1560
    s += f'<path d="M{cx - 130} 330 Q {cx} 180 {cx + 130} 330 Z" fill="#B5652B" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="{cx - 25}" y="330" width="50" height="170" fill="#EFE3CE" stroke="{INK}" stroke-width="3"/>'
    s += ''.join(f'<path d="M{cx} 500 q {dx} 30 {dx * 2} 60" fill="none" stroke="#BDB8AE" stroke-width="4"/>' for dx in (-60, -30, 30, 60))
    s += text(cx + 140, 300, 'шляпка', 's') + text(cx + 40, 430, 'ножка', 's') + text(cx, 600, 'грибница', 's', 'middle', GREY)
    s += text(cx, 160, 'Шляпочные', 't', 'middle') + lines_at(cx, 650, ['плодовое тело из', 'грибницы; споры', 'под шляпкой'], 's', step=36)
    s += text(900, 900, 'Как у животных: хитин, гликоген, нет хлоропластов. Как у растений: неподвижны, растут всю жизнь, всасывают', 's', 'middle')
    return s


# 4. Отделы растений ----------------------------------------------------------------------------------
def plant_divisions():
    s = text(900, 52, 'Отделы растений: от водорослей к цветковым', 'h', 'middle')
    for k in range(5):
        s += card(30 + k * 350, 90, 330, 820)
    base = 600
    # водоросль
    cx = 195
    s += f'<rect x="{cx - 140}" y="330" width="280" height="300" fill="#DCEBF5"/>'
    s += f'<path d="M{cx} {base} C {cx - 60} 500 {cx + 60} 450 {cx - 10} 360 C {cx + 70} 420 {cx + 40} 520 {cx + 20} {base}" fill="{LEAF}" stroke="#1F5E36" stroke-width="3"/>'
    # мох
    cx = 545
    s += f'<line x1="{cx}" y1="{base}" x2="{cx}" y2="430" stroke="{GREEN}" stroke-width="7"/>'
    s += ''.join(leaf(cx + (14 if j % 2 else -14), base - 20 - j * 25, 16, 6, 40 if j % 2 else -40) for j in range(6))
    s += f'<line x1="{cx}" y1="430" x2="{cx + 10}" y2="300" stroke="{BROWN}" stroke-width="3"/><ellipse cx="{cx + 12}" cy="290" rx="12" ry="22" fill="{BROWN}"/>'
    s += ''.join(f'<path d="M{cx} {base} l {dx} 40" stroke="{GREY}" stroke-width="2"/>' for dx in (-20, -8, 6, 18))
    s += text(cx + 30, 300, 'коробочка', 'cap') + text(cx + 30, base + 50, 'ризоиды', 'cap')
    # папоротник
    cx = 895
    s += f'<path d="M{cx - 120} {base + 10} H {cx + 120}" stroke="{BROWN}" stroke-width="12"/>' + text(cx, base + 50, 'корневище', 'cap', 'middle')
    for dx in (-60, 0, 60):
        s += f'<path d="M{cx + dx} {base} Q {cx + dx * 1.6} 420 {cx + dx * 2.2} 330" fill="none" stroke="{GREEN}" stroke-width="5"/>'
        s += ''.join(leaf(cx + dx + (dx * 0.4 + 0.1) * t / 4 + (18 if j % 2 else -18), base - 30 - t * 30, 20, 7, 60 if j % 2 else -60) for j, t in enumerate(range(8)))
    s += ''.join(f'<circle cx="{cx - 20 + j * 20}" cy="{base - 120}" r="5" fill="{BROWN}"/>' for j in range(3)) + text(cx, 300, 'спорангии', 'cap', 'middle')
    # голосеменное
    cx = 1245
    s += f'<line x1="{cx - 110}" y1="420" x2="{cx + 110}" y2="420" stroke="{BROWN}" stroke-width="10"/>'
    s += ''.join(f'<line x1="{cx - 100 + j * 20}" y1="420" x2="{cx - 110 + j * 20}" y2="{390 if j % 2 else 450}" stroke="{GREEN}" stroke-width="3"/>' for j in range(11))
    s += f'<ellipse cx="{cx + 40}" cy="510" rx="34" ry="60" fill="#B5652B" stroke="{INK}" stroke-width="3"/>'
    s += ''.join(f'<path d="M{cx + 10} {470 + j * 20} q 30 10 60 0" fill="none" stroke="{INK}" stroke-width="2"/>' for j in range(4))
    s += text(cx + 40, 610, 'шишка', 'cap', 'middle') + text(cx - 60, 380, 'хвоя', 'cap', 'middle')
    # цветковое
    cx = 1595
    s += f'<line x1="{cx}" y1="{base}" x2="{cx}" y2="330" stroke="{GREEN}" stroke-width="7"/>' + leaf(cx - 40, 480, 40, 15, -20) + leaf(cx + 40, 520, 40, 15, 20)
    for j in range(5):
        a = 2 * math.pi * j / 5 - math.pi / 2
        s += f'<ellipse cx="{cx + 30 * math.cos(a):.0f}" cy="{300 + 30 * math.sin(a):.0f}" rx="22" ry="14" transform="rotate({math.degrees(a):.0f} {cx + 30 * math.cos(a):.0f} {300 + 30 * math.sin(a):.0f})" fill="#F2A7C3" stroke="{INK}" stroke-width="2"/>'
    s += f'<circle cx="{cx}" cy="300" r="12" fill="#F6D27A"/>'
    s += f'<ellipse cx="{cx + 60}" cy="420" rx="18" ry="26" fill="{RED}" stroke="{INK}" stroke-width="2"/>' + text(cx + 90, 430, 'плод', 'cap')
    names = [('Водоросли', ['низшие: слоевище,', 'нет органов']), ('Моховидные', ['ризоиды, нет корней;', 'споры']),
             ('Папоротники', ['корневище, проводящие', 'ткани; споры']), ('Голосеменные', ['первые семена,', 'шишки, хвоя']),
             ('Покрытосеменные', ['цветок и плод;', 'семяпочка в завязи'])]
    for k, (n, rows) in enumerate(names):
        cx = 195 + k * 350
        s += text(cx, 160, n, 't', 'middle') + lines_at(cx, 760, rows, 's', step=36)
    s += arrow(120, 870, 1680, 870, GREEN, 5) + text(900, 855, 'усложнение: споровые → семенные', 'cap', 'middle')
    return s


# 5. Однодольные и двудольные ------------------------------------------------------------------------
def monocot_dicot():
    s = text(900, 52, 'Однодольные и двудольные', 'h', 'middle')
    s += card(30, 90, 860, 1000) + card(910, 90, 860, 1000)
    s += text(460, 145, 'Однодольные', 't', 'middle', BLUE) + text(1340, 145, 'Двудольные', 't', 'middle', GREEN)
    for col, mono in ((460, True), (1340, False)):
        # семя
        s += f'<ellipse cx="{col - 230}" cy="280" rx="70" ry="90" fill="#F3E3C9" stroke="{INK}" stroke-width="3"/>'
        if mono:
            s += f'<ellipse cx="{col - 250}" cy="280" rx="30" ry="70" fill="#E8C547" stroke="{INK}" stroke-width="2"/>'
        else:
            s += f'<ellipse cx="{col - 255}" cy="280" rx="32" ry="75" fill="#E8C547" stroke="{INK}" stroke-width="2"/><ellipse cx="{col - 205}" cy="280" rx="32" ry="75" fill="#E8C547" stroke="{INK}" stroke-width="2"/>'
        s += lines_at(col - 230, 420, ['1 семядоля' if mono else '2 семядоли', 'в семени'], 's', step=30)
        # корень
        if mono:
            s += ''.join(f'<path d="M{col} 210 q {dx} 80 {dx * 1.5} 170" fill="none" stroke="{BROWN}" stroke-width="5"/>' for dx in (-50, -25, 0, 25, 50))
        else:
            s += f'<line x1="{col}" y1="210" x2="{col}" y2="390" stroke="{BROWN}" stroke-width="9"/>'
            s += ''.join(f'<line x1="{col}" y1="{240 + j * 35}" x2="{col + (40 if j % 2 else -40)}" y2="{270 + j * 35}" stroke="{BROWN}" stroke-width="4"/>' for j in range(4))
        s += lines_at(col, 420, ['мочковатый' if mono else 'стержневой', 'корень'], 's', step=30)
        # лист
        lx = col + 230
        if mono:
            s += f'<path d="M{lx} 200 Q {lx + 50} 300 {lx} 390 Q {lx - 50} 300 {lx} 200 Z" fill="{LEAF}" stroke="#1F5E36" stroke-width="3"/>'
            s += ''.join(f'<path d="M{lx} 205 Q {lx + dx} 300 {lx} 385" fill="none" stroke="#1F5E36" stroke-width="2"/>' for dx in (-25, -10, 10, 25))
        else:
            s += f'<ellipse cx="{lx}" cy="295" rx="70" ry="95" fill="{LEAF}" stroke="#1F5E36" stroke-width="3"/><line x1="{lx}" y1="200" x2="{lx}" y2="390" stroke="#1F5E36" stroke-width="3"/>'
            s += ''.join(f'<line x1="{lx}" y1="{230 + j * 30}" x2="{lx + (50 if j % 2 else -50)}" y2="{210 + j * 30}" stroke="#1F5E36" stroke-width="2"/>' for j in range(5))
        s += lines_at(lx, 420, ['параллельное' if mono else 'сетчатое', 'жилкование'], 's', step=30)
        # цветок
        n = 3 if mono else 5
        for j in range(n * (2 if mono else 1)):
            a = 2 * math.pi * j / (n * (2 if mono else 1)) - math.pi / 2
            px, py = col + 70 * math.cos(a), 600 + 70 * math.sin(a)
            s += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="44" ry="24" transform="rotate({math.degrees(a):.0f} {px:.0f} {py:.0f})" fill="#F2A7C3" stroke="{INK}" stroke-width="2"/>'
        if not mono:
            for j in range(5):
                a = 2 * math.pi * (j + 0.5) / 5 - math.pi / 2
                s += f'<path d="M{col + 95 * math.cos(a):.0f} {600 + 95 * math.sin(a):.0f} l {12 * math.cos(a):.0f} {12 * math.sin(a):.0f}" stroke="{GREEN}" stroke-width="10"/>'
        s += f'<circle cx="{col}" cy="600" r="22" fill="#F6D27A"/>'
        s += text(col, 730, 'части цветка по 3, нет чашечки' if mono else 'части по 4–5, чашечка и венчик', 's', 'middle')
        s += lines_at(col, 820, ['нет камбия — травы; листья простые', 'злаки, лилии, тюльпаны, лук'] if mono else
                      ['есть камбий — травы, кустарники, деревья', 'горох, подсолнечник, яблоня, капуста'], 's', step=40)
    s += text(900, 1050, 'Класс определяют по нескольким признакам сразу', 't', 'middle', RED)
    return s


# 6. Беспозвоночные --------------------------------------------------------------------------------
def invertebrates():
    s = text(900, 52, 'Типы беспозвоночных по усложнению', 'h', 'middle')
    items = [('Простейшие', 'одна клетка'), ('Губки', 'первые многоклеточные'), ('Кишечнополостные', '2 слоя, лучевая симметрия'),
             ('Плоские черви', '3 слоя клеток'), ('Круглые черви', 'полость тела'), ('Кольчатые черви', 'сегменты, кровеносная система'),
             ('Моллюски', 'мантия, раковина'), ('Членистоногие', 'хитин, членистые ноги')]
    for k, (n, f) in enumerate(items):
        col, row = k % 4, k // 4
        x, y = 30 + col * 440, 100 + row * 420
        s += card(x, y, 420, 390)
        cx, cy = x + 210, y + 150
        if k == 0:
            s += f'<path d="M{cx - 70} {cy} q 30 -70 80 -40 q 60 10 40 60 q -20 50 -80 30 q -50 -10 -40 -50 Z" fill="#DCEBF5" stroke="{BLUE}" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="14" fill="{BLUE}"/>'
        elif k == 1:
            s += f'<path d="M{cx - 50} {cy + 70} L {cx - 40} {cy - 70} H {cx + 40} L {cx + 50} {cy + 70} Z" fill="#F3E39A" stroke="{INK}" stroke-width="3"/>'
            s += ''.join(f'<circle cx="{cx - 25 + (j % 3) * 25}" cy="{cy - 40 + (j // 3) * 40}" r="7" fill="#fff"/>' for j in range(9))
        elif k == 2:
            s += f'<path d="M{cx - 70} {cy} Q {cx} {cy - 100} {cx + 70} {cy} Z" fill="#E6D3EE" stroke="{PURPLE}" stroke-width="3"/>'
            s += ''.join(f'<path d="M{cx - 60 + j * 30} {cy} q 8 40 0 80" fill="none" stroke="{PURPLE}" stroke-width="3"/>' for j in range(5))
        elif k == 3:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="100" ry="30" fill="#F6D2BF" stroke="{INK}" stroke-width="3"/>'
        elif k == 4:
            s += f'<path d="M{cx - 110} {cy} q 55 -40 110 0 t 110 0" fill="none" stroke="#C9A27A" stroke-width="16" stroke-linecap="round"/>'
        elif k == 5:
            s += ''.join(f'<ellipse cx="{cx - 100 + j * 25}" cy="{cy}" rx="14" ry="22" fill="#D88A8A" stroke="{INK}" stroke-width="2"/>' for j in range(9))
        elif k == 6:
            s += f'<path d="M{cx - 90} {cy + 40} H {cx + 80} Q {cx + 100} {cy} {cx + 60} {cy + 10}" fill="#CFC6B6" stroke="{INK}" stroke-width="3"/>'
            s += f'<path d="M{cx - 40} {cy + 30} a 50 50 0 1 1 60 -30" fill="#E8C547" stroke="{INK}" stroke-width="3"/>'
        else:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="70" ry="35" fill="#B5652B" stroke="{INK}" stroke-width="3"/>'
            s += ''.join(f'<path d="M{cx - 40 + j * 40} {cy + 30} l -20 40 l 10 20" fill="none" stroke="{INK}" stroke-width="4"/>' for j in range(3))
        s += text(cx, y + 280, n, 't', 'middle') + text(cx, y + 330, f, 's', 'middle', GREY)
        if k < 7 and col < 3:
            s += arrow(x + 412, y + 150, x + 448, y + 150, GREEN, 4)
    return s


# 7. Членистоногие ---------------------------------------------------------------------------------
def arthropods():
    s = text(900, 52, 'Членистоногие: считай ноги и усики', 'h', 'middle')
    for k in range(3):
        s += card(30 + k * 590, 90, 560, 800)
    # рак
    cx, cy = 310, 430
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="70" ry="45" fill="#D86A4A" stroke="{INK}" stroke-width="3"/>'
    s += ''.join(f'<ellipse cx="{cx}" cy="{cy + 50 + j * 30}" rx="{50 - j * 6}" ry="16" fill="#D86A4A" stroke="{INK}" stroke-width="2"/>' for j in range(4))
    for dx in (-1, 1):
        s += f'<path d="M{cx + 20 * dx} {cy - 40} q {60 * dx} -100 {140 * dx} -150" fill="none" stroke="{INK}" stroke-width="3"/>'
        s += f'<path d="M{cx + 10 * dx} {cy - 45} q {30 * dx} -60 {60 * dx} -80" fill="none" stroke="{INK}" stroke-width="3"/>'
        s += ''.join(f'<path d="M{cx + 60 * dx} {cy - 10 + j * 18} l {60 * dx} 20" stroke="{INK}" stroke-width="4"/>' for j in range(5))
    s += text(cx, 160, 'Ракообразные', 't', 'middle') + lines_at(cx, 740, ['2 пары усиков', 'головогрудь + брюшко', 'жабры, в основном водные'], 's', step=36)
    # паук
    cx, cy = 900, 430
    s += f'<circle cx="{cx}" cy="{cy - 40}" r="45" fill="#3B3833"/><ellipse cx="{cx}" cy="{cy + 60}" rx="65" ry="75" fill="#3B3833"/>'
    for dx in (-1, 1):
        for j in range(4):
            s += f'<path d="M{cx + 30 * dx} {cy - 60 + j * 18} q {80 * dx} {-40 + j * 20} {150 * dx} {20 + j * 40}" fill="none" stroke="#3B3833" stroke-width="6"/>'
    s += text(cx, 160, 'Паукообразные', 't', 'middle') + lines_at(cx, 740, ['4 пары ног, усиков нет', 'головогрудь + брюшко', 'пауки, клещи, скорпионы'], 's', step=36)
    # насекомое
    cx, cy = 1490, 430
    s += f'<circle cx="{cx}" cy="{cy - 110}" r="30" fill="#5D7A3A"/><ellipse cx="{cx}" cy="{cy - 30}" rx="40" ry="50" fill="#5D7A3A"/><ellipse cx="{cx}" cy="{cy + 100}" rx="45" ry="80" fill="#5D7A3A"/>'
    s += leaf(cx - 90, cy - 20, 90, 30, 25, '#DCEBF5') + leaf(cx + 90, cy - 20, 90, 30, -25, '#DCEBF5')
    for dx in (-1, 1):
        s += f'<path d="M{cx + 12 * dx} {cy - 135} q {20 * dx} -60 {70 * dx} -80" fill="none" stroke="{INK}" stroke-width="4"/>'
        for j in range(3):
            s += f'<path d="M{cx + 35 * dx} {cy - 50 + j * 30} l {90 * dx} {-10 + j * 30}" stroke="{INK}" stroke-width="5"/>'
    s += text(cx, 160, 'Насекомые', 't', 'middle') + lines_at(cx, 740, ['3 пары ног, 1 пара усиков', 'голова, грудь, брюшко', 'обычно 2 пары крыльев'], 's', step=36)
    return s


# 8. Позвоночные -----------------------------------------------------------------------------------
def vertebrates():
    s = text(900, 52, 'Хордовые: классы позвоночных', 'h', 'middle')
    items = [('Рыбы', BLUE, ['жабры, чешуя,', 'плавники']), ('Земноводные', GREEN, ['голая слизистая кожа;', 'головастик в воде']),
             ('Пресмыкающиеся', BROWN, ['чешуя, щитки;', 'полностью на суше']), ('Птицы', ORANGE, ['перья, крылья,', 'клюв без зубов']),
             ('Млекопитающие', RED, ['шерсть, молочные', 'железы'])]
    for k, (n, col, rows) in enumerate(items):
        x = 30 + k * 350
        s += card(x, 90, 330, 620)
        cx, cy = x + 165, 300
        if k == 0:
            s += f'<path d="M{cx - 90} {cy} Q {cx} {cy - 70} {cx + 70} {cy} Q {cx} {cy + 70} {cx - 90} {cy} Z" fill="{col}"/><path d="M{cx + 60} {cy} l 50 -40 v 80 Z" fill="{col}"/>'
        elif k == 1:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="80" ry="55" fill="{col}"/><circle cx="{cx - 40}" cy="{cy - 50}" r="16" fill="{col}"/><circle cx="{cx + 40}" cy="{cy - 50}" r="16" fill="{col}"/>'
        elif k == 2:
            s += f'<path d="M{cx - 110} {cy} Q {cx} {cy - 40} {cx + 110} {cy + 10} Q {cx} {cy + 30} {cx - 110} {cy} Z" fill="{col}"/>'
            s += ''.join(f'<line x1="{cx + dx}" y1="{cy + 10}" x2="{cx + dx - 15}" y2="{cy + 45}" stroke="{col}" stroke-width="8"/>' for dx in (-50, 40))
        elif k == 3:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="70" ry="45" fill="{col}"/><circle cx="{cx + 70}" cy="{cy - 40}" r="28" fill="{col}"/><path d="M{cx + 95} {cy - 45} l 35 8 l -35 8 Z" fill="#E8C547"/>'
            s += leaf(cx - 20, cy - 30, 70, 22, -20, '#F0B98A')
        else:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="85" ry="50" fill="{col}"/><circle cx="{cx + 85}" cy="{cy - 35}" r="34" fill="{col}"/>'
            s += ''.join(f'<line x1="{cx + dx}" y1="{cy + 40}" x2="{cx + dx}" y2="{cy + 90}" stroke="{col}" stroke-width="12"/>' for dx in (-55, -25, 30, 60))
        s += text(cx, 470, n, 't', 'middle', col) + lines_at(cx, 530, rows, 's', step=36)
    s += lines_at(900, 770, ['Хордовые: хорда (у позвоночных — позвоночник), жаберные щели, нервная трубка',
                             'Первые наземные позвоночные — земноводные; полностью освоили сушу пресмыкающиеся'], 's', step=40)
    return s


# 9. Дихотомический ключ ------------------------------------------------------------------------------
def dichotomous_key():
    s = text(900, 52, 'Дихотомический ключ: теза и антитеза', 'h', 'middle')
    s += card(30, 90, 1740, 960)
    steps = [('1. Тело покрыто перьями', 'птицы', '0. Перьев нет'), ('2. Шерсть и молочные железы', 'млекопитающие', '0. Шерсти нет'),
             ('3. Всю жизнь жабры, плавники', 'рыбы', '0. Взрослые дышат лёгкими'),
             ('4. Голая слизистая кожа', 'земноводные', '0. Чешуя, щитки, панцирь')]
    for k, (thesis, res, anti) in enumerate(steps):
        y = 170 + k * 200
        s += box(380, y, 560, 80, thesis, '#E3EEF7')
        s += arrow(665, y, 820, y, GREEN, 5) + box(980, y, 300, 70, res, '#E2F1E6', cls='t')
        s += box(380, y + 90, 560, 70, anti, '#FBE3E4')
        if k < 3:
            s += arrow(380, y + 126, 380, y + 160, RED, 5)
        else:
            s += arrow(665, y + 90, 820, y + 90, RED, 5) + box(980, y + 90, 300, 70, 'пресмыкающиеся', '#E2F1E6', cls='t')
    s += lines_at(1450, 300, ['теза — утверждение,', 'антитеза («0») —', 'противоположное;', 'к организму подходит', 'только одна', 'из двух'], 's', step=40)
    s += lines_at(1450, 620, ['ящерица:', '1 (0) → 2 (0) → 3 (0)', '→ 4 (0) →', 'пресмыкающиеся'], 's', step=40, color=BLUE)
    s += text(900, 1010, 'Ключи предложил Ж. Б. Ламарк (1778)', 's', 'middle', GREY)
    return s


if __name__ == '__main__':
    jobs = {
        'taxa-ladder.png': (taxa_ladder(), 1800, 1020),
        'kingdoms.png': (kingdoms(), 1800, 830),
        'fungi.png': (fungi(), 1800, 940),
        'plant-divisions.png': (plant_divisions(), 1800, 940),
        'monocot-dicot.png': (monocot_dicot(), 1800, 1110),
        'invertebrates.png': (invertebrates(), 1800, 940),
        'arthropods.png': (arthropods(), 1800, 920),
        'vertebrates.png': (vertebrates(), 1800, 860),
        'dichotomous-key.png': (dichotomous_key(), 1800, 1080),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
