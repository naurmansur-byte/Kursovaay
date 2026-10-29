"""Рисунки недели 20 биологии (course/biology/week-20/pics/*.png): экосистема, цепи и сеть, правило 10 %, пирамиды,
кривые роста, хищник и жертва, зона оптимума, взаимоотношения, круговороты углерода и азота, Харди — Вайнберг,
экологические проблемы.

Факты — по выжимке course/textbooks/bio-20-ecology.md (Б8 § 54–60; Б9 § 4–9; Б11-2 § 57–68, 70). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w20.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    return _text(x, y, chem(s), cls, anchor, fill)

OUT = ROOT / 'course' / 'biology' / 'week-20' / 'pics'
BLUE, ORANGE, BROWN, LEAF, SUN = '#3A57A7', '#D98A2B', '#8A5A2B', '#5DAA6F', '#F2C230'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32, color=color))


def dashed(x1, y1, x2, y2, color=GREY, w=3):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-dasharray="10 8"/>'


def heat(x, y, h=70):
    return (f'<path d="M{x} {y} q 12 -{h / 4:.0f} 0 -{h / 2:.0f} q -12 -{h / 4:.0f} 0 -{h / 2:.0f}" fill="none" stroke="{RED}" stroke-width="4"/>'
            f'<polygon points="{x - 9},{y - h + 6} {x + 9},{y - h + 6} {x},{y - h - 10}" fill="{RED}"/>')


# 1. Экосистема ------------------------------------------------------------------------------------
def ecosystem():
    s = text(900, 52, 'Экосистема: поток энергии и круговорот веществ', 'h', 'middle')
    s += card(30, 90, 1740, 800)
    s += f'<circle cx="150" cy="330" r="70" fill="{SUN}"/>' + text(150, 440, 'Солнце', 's', 'middle')
    xs = [420, 790, 1160, 1530]
    names = ['продуценты|растения', 'консументы I|растительноядные', 'консументы II|хищники', 'консументы III|хищники хищников']
    fills = ['#E2F1E6', '#FFF6E8', '#FDE3E4', '#FDE3E4']
    s += arrow(225, 330, 265, 330, ORANGE, 6)
    for k, (x, n) in enumerate(zip(xs, names)):
        s += box(x, 330, 300, 110, n, fills[k])
        s += heat(x, 270) + text(x + 22, 215, 'теплота', 'cap', 'start', RED)
        if k < 3:
            s += arrow(x + 152, 330, xs[k + 1] - 152, 330, ORANGE, 6)
        s += dashed(x, 385, 1150 + (k - 1.5) * 60, 640)
    s += box(1150, 690, 440, 100, 'редуценты|бактерии и грибы', '#EFE6DA')
    s += box(420, 690, 380, 100, 'минеральные вещества|почвы и воды', '#DCEBF5')
    s += arrow(928, 690, 612, 690, GREEN, 6) + text(770, 670, 'минерализация', 'cap', 'middle', GREEN)
    s += arrow(420, 640, 420, 388, GREEN, 6)
    s += text(1420, 640, 'мёртвые остатки', 'cap', 'start', GREY)
    s += text(900, 800, 'Энергия — поток в одну сторону: Солнце → продуценты → консументы → теплота', 's', 'middle', ORANGE)
    s += text(900, 845, 'Вещества — круговорот: остатки → редуценты → минеральные вещества → продуценты', 's', 'middle', GREEN)
    return s


# 2. Цепи и сеть ------------------------------------------------------------------------------------
def food_chains():
    s = text(900, 52, 'Пастбищная и детритная цепи, пищевая сеть', 'h', 'middle')
    s += card(30, 90, 1740, 900)
    s += text(70, 140, 'Пастбищная — с живых растений', 't', 'start', GREEN)
    g = ['луговой цветок', 'бабочка', 'лягушка', 'уж', 'цапля']
    for k, n in enumerate(g):
        x = 220 + k * 340
        s += box(x, 210, 260, 80, n, '#E2F1E6' if k == 0 else '#fff')
        s += text(x, 280, f'{k + 1}-й уровень', 'cap', 'middle')
        if k < 4:
            s += arrow(x + 132, 210, x + 208, 210, INK, 4)
    s += text(70, 360, 'Детритная — с мёртвой органики', 't', 'start', BROWN)
    d = ['листовая подстилка', 'дождевой червь', 'чёрный дрозд', 'ястреб-перепелятник']
    for k, n in enumerate(d):
        x = 220 + k * 340
        s += box(x, 430, 290, 80, n, '#EFE6DA' if k == 0 else '#fff')
        if k < 3:
            s += arrow(x + 147, 430, x + 193, 430, INK, 4)
    s += f'<line x1="70" y1="520" x2="1730" y2="520" stroke="{GREY}" stroke-width="2"/>'
    s += text(70, 575, 'Пищевая сеть луга', 't')
    nodes = {'трава': (900, 920), 'кузнечик': (450, 790), 'заяц': (900, 790), 'мышь': (1350, 790),
             'лягушка': (450, 650), 'уж': (900, 640), 'лиса': (1350, 640)}
    links = [('трава', 'кузнечик'), ('трава', 'заяц'), ('трава', 'мышь'), ('кузнечик', 'лягушка'), ('лягушка', 'уж'),
             ('мышь', 'уж'), ('заяц', 'лиса'), ('мышь', 'лиса')]
    for a, b in links:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        s += arrow(x1 + ux * 45, y1 + uy * 45, x2 - ux * 45, y2 - uy * 45, GREY, 3)
    for n, (x, y) in nodes.items():
        s += box(x, y, 170, 60, n, '#E2F1E6' if n == 'трава' else '#fff')
    s += lines_at(1580, 840, ['стрелка — от пищи', 'к тому, кто её ест'], 'cap', step=30)
    return s


# 3. Правило 10 % ---------------------------------------------------------------------------------
def ten_percent():
    s = text(900, 52, 'Правило 10 %: лестница энергии', 'h', 'middle')
    s += card(30, 90, 1740, 800)
    steps = [('растения', '1000 кДж', 360, '#E2F1E6'), ('травоядные', '100 кДж', 260, '#FFF6E8'),
             ('хищник', '10 кДж', 180, '#FDE3E4'), ('хищник хищника', '1 кДж', 110, '#FDE3E4')]
    base = 660
    for k, (n, v, h, f) in enumerate(steps):
        x = 260 + k * 420
        s += f'<rect x="{x - 150}" y="{base - h}" width="300" height="{h}" rx="12" fill="{f}" stroke="{INK}" stroke-width="3"/>'
        s += text(x, base - h / 2 + 12, v, 'f' if k < 2 else 't', 'middle')
        s += text(x, base + 45, n, 't', 'middle')
        s += heat(x + 110, base - h - 10, 60)
        if k < 3:
            s += arrow(x + 160, base - h / 2, x + 260, base - steps[k + 1][2] / 2, ORANGE, 6)
            s += text(x + 210, base - h / 2 - 40, '10 %', 't', 'middle', ORANGE)
    s += text(900, 180, '≈ 90 % на каждом уровне — дыхание, движение, тепло тела → теплота', 's', 'middle', RED)
    s += lines_at(900, 780, ['вверх по цепи — делить на 10, вниз — умножать на 10',
                             'переходов на один меньше, чем звеньев · 10 % — среднее значение (от 1 до 30 %)'], 's', step=44)
    return s


# 4. Пирамиды ----------------------------------------------------------------------------------------
def tiers(cx, base, widths, labels, fills, h=90):
    s = ''
    for k, (w, lab, f) in enumerate(zip(widths, labels, fills)):
        y = base - (k + 1) * h
        s += f'<rect x="{cx - w / 2:.0f}" y="{y}" width="{w}" height="{h - 6}" rx="8" fill="{f}" stroke="{INK}" stroke-width="2.5"/>'
        s += text(cx, y + h / 2 + 6, lab, 's', 'middle')
    return s


def pyramids():
    s = text(900, 52, 'Экологические пирамиды', 'h', 'middle')
    titles = [('Энергии', 'всегда правильная', GREEN), ('Чисел: дерево', 'перевёрнута у основания', RED), ('Биомассы в море', 'перевёрнута', RED)]
    data = [([480, 320, 190, 90], ['продуценты', 'консументы I', 'консументы II', 'III'], ['#E2F1E6', '#FFF6E8', '#FDE3E4', '#FDE3E4']),
            ([120, 500, 240], ['1 дуб', '3000 гусениц', '40 синиц'], ['#E2F1E6', '#FFF6E8', '#FDE3E4']),
            ([200, 460], ['фитопланктон', 'зоопланктон'], ['#E2F1E6', '#FFF6E8'])]
    for k, ((t, sub, col), (ws, ls, fs)) in enumerate(zip(titles, data)):
        x = 30 + k * 590
        s += card(x, 90, 560, 720)
        s += text(x + 280, 150, t, 't', 'middle', col) + text(x + 280, 190, sub, 's', 'middle', col)
        s += tiers(x + 280, 640, ws, ls, fs)
    s += text(30 + 280 + 1180, 700, 'фитопланктон быстро размножается —', 's', 'middle')
    s += text(30 + 280 + 1180, 740, 'в данный момент его биомасса мала', 's', 'middle')
    s += text(310, 700, 'энергия убывает', 's', 'middle') + text(310, 740, 'на каждом уровне', 's', 'middle')
    s += text(900, 860, 'Пирамиды чисел и биомассы — «снимок» в данный момент; пирамида энергии — поток за единицу времени', 's', 'middle')
    return s


# 5. Кривые роста -------------------------------------------------------------------------------------
def axes(x0, y0, w, h, xl, yl):
    return (f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{INK}" stroke-width="3"/>'
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h}" stroke="{INK}" stroke-width="3"/>'
            + text(x0 + w, y0 + 40, xl, 'cap', 'end') + text(x0 - 10, y0 - h - 15, yl, 'cap', 'start'))


def poly(points, color, w=6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="{w}"{d}/>'


def growth_curves():
    s = text(900, 52, 'Рост популяции: J- и S-кривые', 'h', 'middle')
    s += card(30, 90, 1100, 800) + card(1150, 90, 620, 800)
    x0, y0, w, h = 120, 780, 950, 600
    s += axes(x0, y0, w, h, 'время', 'численность')
    K = y0 - 420
    s += dashed(x0, K, x0 + w, K, GREY, 3) + text(x0 + w, K - 14, 'несущая ёмкость среды', 's', 'end', GREY)
    S = [(x0 + t * w / 100, y0 - 420 / (1 + math.exp(-(t - 40) / 7))) for t in range(101)]
    J = [(x0 + t * w / 100, y0 - 8 * math.exp(t / 14.5)) for t in range(0, 58)]
    J += [(x0 + 58 * w / 100 + k * 9, y0 - 8 * math.exp(57 / 14.5) + k * 40) for k in range(1, 10)]
    s += poly(S, GREEN) + poly(J, RED)
    s += text(560, 270, 'J-кривая: взлёт — пик — падение', 's', 'start', RED)
    s += text(800, K + 50, 'S-кривая: плато', 's', 'start', GREEN)
    s += text(1460, 160, 'r-стратегия · J', 't', 'middle', RED)
    s += lines_at(1460, 210, ['много потомства, ранняя зрелость,', 'быстрая смена поколений', 'саранча, тли, бактерии,', 'мышевидные грызуны'], 's', step=36)
    s += text(1460, 470, 'K-стратегия · S', 't', 'middle', GREEN)
    s += lines_at(1460, 520, ['мало потомства, забота о нём,', 'долгая жизнь', 'слоны, киты, человекообразные', 'обезьяны, крупные кошачьи'], 's', step=36)
    s += text(1460, 780, 'кривые условные', 'cap', 'middle')
    return s


# 6. Хищник и жертва ---------------------------------------------------------------------------------
def predator_prey():
    s = text(900, 52, 'Хищник и жертва: численность колеблется согласованно', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    x0, y0, w, h = 130, 720, 1560, 520
    s += axes(x0, y0, w, h, 'годы', 'численность')
    hare = [(x0 + t * w / 200, y0 - 230 - 190 * math.sin(2 * math.pi * t / 80)) for t in range(201)]
    lynx = [(x0 + t * w / 200, y0 - 120 - 80 * math.sin(2 * math.pi * (t - 14) / 80)) for t in range(201)]
    s += poly(hare, BLUE) + poly(lynx, RED)
    s += text(300, 170, '— заяц (жертва)', 't', 'start', BLUE) + text(780, 170, '— рысь (хищник)', 't', 'start', RED)
    s += text(1690, 170, 'данные условные', 'cap', 'end')
    s += text(900, 800, 'Пик рыси наступает после пика зайца: хищник и жертва регулируют численность друг друга', 's', 'middle')
    return s


# 7. Зона оптимума ----------------------------------------------------------------------------------
def tolerance():
    s = text(900, 52, 'Экологический фактор: оптимум и пределы выносливости', 'h', 'middle')
    s += card(30, 90, 1740, 780)
    x0, y0, w = 160, 640, 1480
    pts = [(x0 + t * w / 100, y0 - 420 * math.exp(-((t - 50) / 18) ** 2)) for t in range(8, 93)]
    s += f'<rect x="{x0 + 35 * w / 100:.0f}" y="190" width="{30 * w / 100:.0f}" height="{y0 - 190}" fill="#E2F1E6"/>'
    s += f'<rect x="{x0 + 8 * w / 100:.0f}" y="190" width="{27 * w / 100:.0f}" height="{y0 - 190}" fill="#FFF6E8"/>'
    s += f'<rect x="{x0 + 65 * w / 100:.0f}" y="190" width="{27 * w / 100:.0f}" height="{y0 - 190}" fill="#FFF6E8"/>'
    s += f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{INK}" stroke-width="3"/>' + text(x0 + w / 2, y0 + 40, 'температура', 'cap', 'middle')
    s += poly(pts, GREEN)
    s += text(x0 + 50 * w / 100, 240, 'зона оптимума', 't', 'middle', GREEN)
    s += text(x0 + 21 * w / 100, 240, 'угнетение', 's', 'middle', ORANGE) + text(x0 + 79 * w / 100, 240, 'угнетение', 's', 'middle', ORANGE)
    for t, lab in ((8, 'минимум'), (92, 'максимум')):
        x = x0 + t * w / 100
        s += f'<line x1="{x:.0f}" y1="190" x2="{x:.0f}" y2="{y0}" stroke="{RED}" stroke-width="4"/>' + text(x, y0 + 40, lab, 's', 'middle', RED)
    s += text(x0 + 2 * w / 100, 420, 'гибель', 's', 'middle', RED) + text(x0 + 98 * w / 100, 420, 'гибель', 's', 'middle', RED)
    xa, xb = x0 + 8 * w / 100, x0 + 92 * w / 100
    s += f'<line x1="{xa:.0f}" y1="730" x2="{xb:.0f}" y2="730" stroke="{INK}" stroke-width="3"/>'
    s += f'<line x1="{xa:.0f}" y1="715" x2="{xa:.0f}" y2="745" stroke="{INK}" stroke-width="3"/><line x1="{xb:.0f}" y1="715" x2="{xb:.0f}" y2="745" stroke="{INK}" stroke-width="3"/>'
    s += text(900, 780, 'предел выносливости', 't', 'middle')
    s += text(900, 830, 'лимитирующий фактор — тот, что ограничивает жизнь сильнее других', 's', 'middle')
    return s


# 8. Взаимоотношения ------------------------------------------------------------------------------
def interactions():
    s = text(900, 52, 'Типы взаимоотношений: + польза, − вред, 0 безразлично', 'h', 'middle')
    data = [('Мутуализм', '+ +', 'лишайник, микориза;|часто друг без друга не могут', GREEN),
            ('Кооперация', '+ +', 'рак-отшельник и актиния;|необязательная', GREEN),
            ('Комменсализм', '+ 0', 'гиены доедают|добычу львов', BLUE),
            ('Квартирантство', '+ 0', 'мальки под медузой,|рыба-клоун в актинии', BLUE),
            ('Хищничество', '+ −', 'волк и заяц;|каннибализм у щуки', RED),
            ('Паразитизм', '+ −', 'клещи, глисты;|кукушка — гнездовой', RED),
            ('Конкуренция', '− −', 'серые крысы|вытеснили чёрных', ORANGE),
            ('Аменсализм', '− 0', 'одностороннее|отрицательное влияние', GREY),
            ('Нейтрализм', '0 0', 'белки и лоси|в одном лесу', GREY)]
    for k, (n, sg, ex, col) in enumerate(data):
        x = 30 + (k % 3) * 590
        y = 90 + (k // 3) * 290
        s += f'<rect x="{x}" y="{y}" width="560" height="260" rx="18" fill="#fff" stroke="{col}" stroke-width="5"/>'
        s += text(x + 30, y + 60, n, 't', 'start', col) + text(x + 530, y + 70, sg, 'f', 'end', col)
        s += lines_at(x + 30, y + 150, ex.split('|'), 's', 'start', step=38)
    s += text(900, 990, 'Принцип Гаузе (1934): два вида не могут занимать одну экологическую нишу на одной территории', 's', 'middle')
    return s


# 9. Круговорот углерода ---------------------------------------------------------------------------
def carbon_cycle():
    s = text(900, 52, 'Круговорот углерода', 'h', 'middle')
    s += card(30, 90, 1740, 840)
    s += box(900, 170, 360, 80, 'CO₂ атмосферы', '#DCEBF5', cls='t')
    s += box(280, 480, 260, 80, 'растения', '#E2F1E6', cls='t') + box(900, 480, 260, 80, 'животные', '#FFF6E8', cls='t')
    s += box(900, 770, 380, 90, 'остатки|редуценты', '#EFE6DA') + box(1500, 770, 380, 90, 'уголь, нефть, газ,|известняк, мел', '#E9E4D8')
    s += arrow(730, 150, 250, 435, GREEN, 6) + text(380, 270, 'фотосинтез', 't', 'end', GREEN)
    s += arrow(370, 438, 820, 215, RED, 5) + text(600, 370, 'дыхание', 's', 'start', RED)
    s += arrow(412, 480, 765, 480, INK, 5) + text(590, 465, 'питание', 'cap', 'middle')
    s += arrow(900, 438, 900, 215, RED, 5) + text(915, 340, 'дыхание', 's', 'start', RED)
    s += dashed(300, 522, 760, 735) + dashed(900, 522, 900, 722)
    s += text(560, 650, 'остатки', 'cap', 'end')
    s += arrow(1100, 722, 1050, 215, RED, 5) + text(1110, 560, 'гниение', 's', 'start', RED)
    s += f'<line x1="1092" y1="770" x2="1295" y2="770" stroke="{BROWN}" stroke-width="5" stroke-dasharray="12 8"/>'
    s += text(1195, 820, 'миллионы лет', 'cap', 'middle')
    s += arrow(1500, 722, 1090, 175, RED, 5) + text(1380, 450, 'горение', 's', 'start', RED)
    s += text(900, 900, 'Фотосинтез поглощает CO₂; дыхание, гниение, горение и вулканы возвращают его в атмосферу', 's', 'middle')
    return s


# 10. Круговорот азота -----------------------------------------------------------------------------
def nitrogen_cycle():
    s = text(900, 52, 'Круговорот азота', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    s += box(900, 160, 420, 80, 'N₂ воздуха (около 78 %)', '#DCEBF5', cls='t')
    s += box(350, 440, 340, 80, 'нитраты в почве', '#E2F1E6', cls='t')
    s += box(1450, 440, 340, 80, 'аммиак', '#FFF6E8', cls='t')
    s += box(350, 760, 260, 80, 'растения', '#E2F1E6', cls='t') + box(900, 800, 260, 80, 'животные', '#FFF6E8', cls='t')
    s += box(1450, 760, 340, 90, 'остатки,|мочевина', '#EFE6DA')
    s += arrow(690, 160, 280, 398, GREEN, 6)
    s += lines_at(60, 205, ['фиксация:', 'молнии, клубеньковые', 'бактерии, цианобактерии'], 's', 'start', step=34, color=GREEN)
    s += arrow(470, 400, 800, 202, RED, 5)
    s += lines_at(640, 330, ['денитрифицирующие', 'бактерии → N₂'], 's', 'start', step=34, color=RED)
    s += arrow(1278, 440, 522, 440, BLUE, 5) + text(900, 425, 'нитрифицирующие бактерии', 's', 'middle', BLUE)
    s += arrow(350, 482, 350, 718, GREEN, 5) + text(370, 610, 'поглощают', 's', 'start', GREEN)
    s += arrow(482, 772, 768, 795, INK, 4) + arrow(1032, 795, 1278, 772, INK, 4)
    s += arrow(1450, 713, 1450, 482, BROWN, 5) + lines_at(1430, 580, ['аммонифицирующие', 'бактерии'], 's', 'end', step=34, color=BROWN)
    s += text(900, 905, 'Растения усваивают не N₂, а соединения азота — нитраты', 's', 'middle')
    return s


# 11. Харди — Вайнберг -------------------------------------------------------------------------------
def hardy_weinberg():
    s = text(900, 52, 'Закон Харди — Вайнберга', 'h', 'middle')
    s += card(30, 90, 900, 820) + card(950, 90, 820, 820)
    gx, gy, c = 260, 260, 280
    s += text(gx + c, 170, 'сперматозоиды', 's', 'middle', GREY) + text(150, gy + c, 'яйцеклетки', 's', 'middle', GREY).replace('<text', f'<text transform="rotate(-90 150 {gy + c})"')
    for j, (al, fr) in enumerate((('A', 'p'), ('a', 'q'))):
        s += text(gx + c / 2 + j * c, 230, f'{al} ({fr})', 't', 'middle')
        s += text(gx - 20, gy + c / 2 + 10 + j * c, f'{al} ({fr})', 't', 'end')
    cells = [('AA', 'p²', '#FFF6E8'), ('Aa', 'pq', '#DCEBF5'), ('Aa', 'pq', '#DCEBF5'), ('aa', 'q²', '#FDE3E4')]
    for k, (g, f, fill) in enumerate(cells):
        x, y = gx + (k % 2) * c, gy + (k // 2) * c
        s += f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
        s += text(x + c / 2, y + c / 2 - 5, g, 'f', 'middle') + text(x + c / 2, y + c / 2 + 50, f, 't', 'middle')
    s += text(480, 880, 'две клетки pq = 2pq — гетерозиготы Aa', 's', 'middle', BLUE)
    s += box(1360, 200, 640, 80, 'p + q = 1', '#fff', cls='t') + box(1360, 310, 640, 80, 'p² + 2pq + q² = 1', '#fff', cls='t')
    s += lines_at(1360, 430, ['идеальная популяция: большая,', 'скрещивание случайное,', 'нет мутаций, миграций, отбора'], 's', step=36)
    s += text(1360, 600, 'Фенилкетонурия: 1 больной на 10 000', 't', 'middle')
    s += lines_at(1360, 650, ['q² = 0,0001 → q = 0,01; p = 0,99', '2pq ≈ 0,02 — носитель каждый 50-й'], 's', step=40)
    s += text(1360, 810, 'начинай с q² — доли больных aa', 's', 'middle', RED)
    return s


# 12. Экологические проблемы ----------------------------------------------------------------------
def human_impact():
    s = text(900, 52, 'Человек и окружающая среда', 'h', 'middle')
    for k in range(4):
        s += card(30 + (k % 2) * 880, 90 + (k // 2) * 470, 860, 450)
    # парниковый эффект
    s += text(460, 150, 'Парниковый эффект — CO₂', 't', 'middle', RED)
    s += f'<path d="M110 500 A 350 160 0 0 1 810 500 Z" fill="#E2F1E6" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M80 300 Q 460 200 840 300" fill="none" stroke="{GREY}" stroke-width="10" stroke-dasharray="14 10" opacity=".7"/>'
    s += text(780, 270, 'CO₂, метан', 's', 'end', GREY)
    s += arrow(200, 180, 330, 410, SUN, 7) + text(200, 230, 'свет', 's', 'end', ORANGE)
    s += arrow(520, 410, 600, 290, RED, 5) + arrow(600, 290, 640, 395, RED, 5)
    s += text(700, 430, 'тепло задерживается', 's', 'start', RED).replace('x="700"', 'x="560"')
    # озон
    s += text(1340, 150, 'Озоновый слой — фреоны', 't', 'middle', BLUE)
    s += f'<rect x="950" y="260" width="780" height="50" fill="#DCEBF5"/>' + text(1700, 295, 'озон, 15–50 км', 's', 'end', BLUE)
    s += f'<rect x="1380" y="260" width="120" height="50" fill="{PAPER}"/>' + text(1440, 245, 'озоновая дыра', 's', 'middle', RED)
    for x in (1050, 1200, 1620):
        s += arrow(x, 180, x, 255, '#8E44AD', 5)
    s += arrow(1440, 180, 1440, 470, '#8E44AD', 6)
    s += lines_at(1220, 420, ['ультрафиолет повреждает ДНК —', 'больше мутаций'], 's', step=34)
    # ДДТ
    s += text(460, 620, 'Пестициды накапливаются по цепи', 't', 'middle', ORANGE)
    chain = ['вода', 'планктон', 'рыба', 'птица']
    for k, n in enumerate(chain):
        x = 140 + k * 210
        s += f'<rect x="{x - 80}" y="680" width="160" height="160" rx="16" fill="#fff" stroke="{INK}" stroke-width="3"/>'
        for j in range(1 + k * 6):
            s += f'<circle cx="{x - 60 + (j * 37) % 120 + 6}" cy="{700 + (j * 23) % 120 + 6}" r="6" fill="{RED}"/>'
        s += text(x, 880, n, 's', 'middle')
        if k < 3:
            s += arrow(x + 84, 760, x + 126, 760, INK, 4)
    s += text(460, 925, 'точки — концентрация (условно)', 'cap', 'middle')
    # Арал
    s += text(1340, 620, 'Аральское море', 't', 'middle', BROWN)
    s += f'<ellipse cx="1240" cy="770" rx="210" ry="120" fill="none" stroke="{GREY}" stroke-width="4" stroke-dasharray="12 8"/>'
    s += f'<ellipse cx="1170" cy="730" rx="70" ry="45" fill="#7FB3E0"/><ellipse cx="1300" cy="810" rx="90" ry="50" fill="#7FB3E0"/>'
    s += f'<path d="M1720 680 Q 1580 700 1470 720" fill="none" stroke="#3A7FC1" stroke-width="6"/><path d="M1720 880 Q 1580 860 1450 820" fill="none" stroke="#3A7FC1" stroke-width="6"/>'
    s += text(1720, 665, 'Сырдарья', 'cap', 'end') + text(1720, 905, 'Амударья', 'cap', 'end')
    s += arrow(1600, 700, 1640, 760, GREEN, 4) + arrow(1600, 866, 1640, 800, GREEN, 4)
    s += text(1660, 790, 'поля', 's', 'start', GREEN)
    s += lines_at(1250, 950, ['вода рек — на орошение хлопка и риса;', 'море мелеет и делится, ветер несёт соль'], 'cap', step=30)
    return s


if __name__ == '__main__':
    jobs = {
        'ecosystem.png': (ecosystem(), 1800, 920),
        'food-chains.png': (food_chains(), 1800, 1020),
        'ten-percent.png': (ten_percent(), 1800, 920),
        'pyramids.png': (pyramids(), 1800, 900),
        'growth-curves.png': (growth_curves(), 1800, 920),
        'predator-prey.png': (predator_prey(), 1800, 880),
        'tolerance.png': (tolerance(), 1800, 900),
        'interactions.png': (interactions(), 1800, 1020),
        'carbon-cycle.png': (carbon_cycle(), 1800, 960),
        'nitrogen-cycle.png': (nitrogen_cycle(), 1800, 980),
        'hardy-weinberg.png': (hardy_weinberg(), 1800, 940),
        'human-impact.png': (human_impact(), 1800, 1040),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
