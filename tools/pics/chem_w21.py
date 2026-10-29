"""Рисунки недели 21 химии (course/week-21/pics/*.png): классификация углеводов, глюкоза и фруктоза, реакции глюкозы,
крахмал и целлюлоза, гидролиз крахмала, амины, аминокислота и пептид, структуры белка, цветные реакции, ферменты,
таблица распознавания.

Факты — по выжимке course/textbooks/chem-21-carbs-amines-proteins.md (Х9-2 § 67–68; Х11-1 § 14–25). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w21.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render, span
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = chem(s.replace('ₙ', '\x02')).replace('\x02', '<tspan baseline-shift="-0.28em" font-size="68%">n</tspan>')
    return _text(x, y, s, cls, anchor, fill)

OUT = ROOT / 'course' / 'week-21' / 'pics'
BLUE, ORANGE, BROWN, VIOLET = '#3A57A7', '#D98A2B', '#8A5A2B', '#7B3FA0'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32, color=color))


def tube(cx, top, fill, h=300, sediment=None):
    s = f'<path d="M{cx - 34} {top} V {top + h - 34} A 34 34 0 0 0 {cx + 34} {top + h - 34} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if sediment:
        s += (f'<path d="M{cx - 34} {top + h - 70} V {top + h - 34} A 34 34 0 0 0 {cx + 34} {top + h - 34} V {top + h - 70} Z" '
              f'fill="{sediment}" stroke="{INK}" stroke-width="2"/>')
    return s


def hexa(cx, cy, r=26, fill='#F7EFC8', stroke=INK):
    pts = ' '.join(f'{cx + r * math.cos(math.radians(60 * k + 30)):.0f},{cy + r * math.sin(math.radians(60 * k + 30)):.0f}' for k in range(6))
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'


def hex_chain(pts, fill='#F7EFC8', r=24):
    s = ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="3"/>' for a, b in zip(pts, pts[1:]))
    return s + ''.join(hexa(x, y, r, fill) for x, y in pts)


# 1. Классификация углеводов ------------------------------------------------------------------------
def carb_classes():
    s = text(900, 52, 'Углеводы: моно-, ди-, полисахариды', 'h', 'middle')
    cols = [('Моносахариды', 'не гидролизуются', ['глюкоза, фруктоза — C₆H₁₂O₆', 'рибоза — C₅H₁₀O₅', 'дезоксирибоза — C₅H₁₀O₄'], 1),
            ('Дисахариды', '→ 2 моносахарида', ['сахароза = глюкоза + фруктоза', 'мальтоза = 2 глюкозы', 'лактоза = глюкоза + галактоза', 'все — C₁₂H₂₂O₁₁'], 2),
            ('Полисахариды', '→ много моносахаридов', ['крахмал', 'целлюлоза', '(C₆H₁₀O₅)ₙ'], 7)]
    for k, (t, sub, rows, n) in enumerate(cols):
        x = 30 + k * 590
        s += card(x, 90, 540, 680)
        s += text(x + 270, 160, t, 't', 'middle') + text(x + 270, 200, sub, 's', 'middle', GREY)
        pts = [(x + 270 - (n - 1) * 30 + j * 60, 300) for j in range(n)]
        s += hex_chain(pts)
        s += lines_at(x + 270, 420, rows, 's', step=44)
        if k > 0:
            s += arrow(x - 4, 300, x - 44, 300, RED, 6)
    s += text(900, 830, 'Стрелки — гидролиз: полисахарид → дисахарид → моносахариды', 's', 'middle', RED)
    return s


# 2. Глюкоза и фруктоза ---------------------------------------------------------------------------
def chain(cx, top, rows, hl):
    s = ''
    for k, r in enumerate(rows):
        y = top + k * 95
        col = hl.get(k)
        s += text(cx, y, r, 't', 'middle', col)
        if k < len(rows) - 1:
            s += f'<line x1="{cx}" y1="{y + 14}" x2="{cx}" y2="{y + 60}" stroke="{INK}" stroke-width="4"/>'
    return s


def glucose():
    s = text(900, 52, 'Глюкоза и фруктоза — изомеры C₆H₁₂O₆', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 150, 'Глюкоза — альдегидоспирт', 't', 'middle', BLUE)
    s += chain(460, 240, ['CHO', 'H–C–OH', 'HO–C–H', 'H–C–OH', 'H–C–OH', 'CH₂OH'], {0: BLUE})
    s += f'<rect x="380" y="200" width="160" height="56" rx="12" fill="none" stroke="{BLUE}" stroke-width="4"/>'
    s += lines_at(460, 830, ['–CHO и пять групп –OH'], 's')
    s += text(1340, 150, 'Фруктоза — кетоноспирт', 't', 'middle', RED)
    s += chain(1340, 240, ['CH₂OH', 'C=O', 'HO–C–H', 'H–C–OH', 'H–C–OH', 'CH₂OH'], {1: RED})
    s += f'<rect x="1270" y="295" width="140" height="56" rx="12" fill="none" stroke="{RED}" stroke-width="4"/>'
    s += lines_at(1340, 830, ['группа C=O у второго атома C'], 's')
    return s


# 3. Реакции глюкозы ------------------------------------------------------------------------------
def glucose_tests():
    s = text(900, 52, 'Глюкоза: спирт и альдегид в одной молекуле', 'h', 'middle')
    s += card(30, 90, 1740, 800)
    items = [('глюкоза + Cu(OH)₂|без нагревания', '#1F5FD1', None, False, 'ярко-синий раствор', 'несколько –OH'),
             ('глюкоза + Cu(OH)₂|при нагревании', '#7FB3E0', '#C0392B', False, 'красный осадок Cu₂O', 'группа –CHO'),
             ('глюкоза + Ag₂O (NH₃)|нагревание', '#E9EBEE', None, True, 'серебряное зеркало', 'группа –CHO'),
             ('сахароза + Ag₂O (NH₃)|нагревание', '#F7F7F2', None, False, 'реакции нет', 'не альдегид')]
    for k, (title, fill, sed, mirror, res, why) in enumerate(items):
        cx = 250 + k * 430
        s += lines_at(cx, 150, title.split('|'), 's', step=32)
        s += tube(cx, 240, fill, 300, sed)
        if mirror:
            s += f'<path d="M{cx - 34} 260 V 500" stroke="#B8BDC4" stroke-width="10"/><path d="M{cx + 34} 260 V 500" stroke="#E8ECF0" stroke-width="10"/>'
        s += text(cx, 600, res, 't', 'middle', RED if 'нет' in res else INK) + text(cx, 645, why, 's', 'middle', GREY)
    s += lines_at(900, 740, ['без нагревания синий раствор дают и сахароза, и глицерин',
                             'после гидролиза сахароза даёт глюкозу — и тогда зеркало и Cu₂O'], 's', step=44)
    return s


# 4. Крахмал и целлюлоза -------------------------------------------------------------------------
def starch_cellulose():
    s = text(900, 52, 'Крахмал и целлюлоза: одна формула, разное строение', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 150, 'Крахмал — α-глюкоза', 't', 'middle', BLUE)
    s += text(90, 230, 'амилоза — цепь', 's')
    s += hex_chain([(110 + j * 58, 300 + 30 * math.sin(j / 1.6)) for j in range(11)])
    s += text(90, 420, 'амилопектин — ветвится', 's')
    main = [(110 + j * 58, 520) for j in range(11)]
    br1 = [(342, 520 - (j + 1) * 50) for j in range(0)] + [(400 + j * 50, 590 + j * 22) for j in range(1, 5)]
    br2 = [(632 + j * 50, 590 + j * 22) for j in range(1, 3)]
    s += hex_chain(main) + hex_chain([(400, 520)] + br1[0:]) + hex_chain([(632, 520)] + br2)
    s += tube(785, 690, '#1F3FA0', 170) + text(785, 895, 'йод — синий', 's', 'middle', BLUE)
    s += lines_at(380, 770, ['запасное вещество растений', 'в горячей воде — клейстер'], 's', step=36)
    s += text(1340, 150, 'Целлюлоза — β-глюкоза', 't', 'middle', GREEN)
    for r in range(4):
        s += hex_chain([(970 + j * 58, 260 + r * 90) for j in range(13)], '#E2F1E6')
    s += lines_at(1340, 680, ['только линейные цепи лежат', 'параллельно — прочные волокна', 'хлопок, древесина'], 's', step=40)
    s += text(1340, 860, 'с йодом синего цвета нет', 's', 'middle', GREY)
    return s


# 5. Гидролиз крахмала -------------------------------------------------------------------------------
def starch_hydrolysis():
    s = text(900, 52, 'Ступенчатый гидролиз крахмала и брожение', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    steps = [('крахмал', 9), ('декстрины', 4), ('мальтоза', 2), ('глюкоза', 1), ('этанол + CO₂', 0)]
    for k, (n, h) in enumerate(steps):
        x = 200 + k * 350
        if h:
            s += hex_chain([(x - (min(h, 5) - 1) * 26 + j * 52, 260 + (j // 5) * 60 - (j // 5) * 0) for j in range(min(h, 5))] +
                           [], r=22)
            if h > 5:
                s += hex_chain([(x - 3 * 26 + j * 52, 330) for j in range(h - 5)], r=22)
        else:
            s += text(x, 300, 'C₂H₅OH', 't', 'middle', BLUE) + text(x, 345, '+ CO₂↑', 't', 'middle', BLUE)
        s += box(x, 470, 270, 80, n, '#F7EFC8' if k < 4 else '#DCEBF5', cls='t')
        if k < 4:
            s += arrow(x + 138, 470, x + 212, 470, RED if k < 3 else BLUE, 5)
    s += text(725, 560, 'H₂O, H⁺, t (или ферменты)', 's', 'middle', RED) + text(1425, 560, 'дрожжи', 's', 'middle', BLUE)
    s += lines_at(900, 680, ['(C₆H₁₀O₅)ₙ + nH₂O → nC₆H₁₂O₆;  C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂',
                             'расчёт — по звену C₆H₁₀O₅ (M = 162): 1 звено → 1 глюкоза → 2 этанола'], 's', step=46)
    return s


# 6. Амины --------------------------------------------------------------------------------------------
def amines():
    s = text(900, 52, 'Амины и анилин', 'h', 'middle')
    s += card(30, 90, 1740, 360) + card(30, 470, 1740, 420)
    mols = [('первичный', 'CH₃–NH₂', 'метиламин'), ('вторичный', '(C₂H₅)₂NH', 'диэтиламин'), ('третичный', '(CH₃)₃N', 'триметиламин')]
    for k, (t, f, n) in enumerate(mols):
        x = 330 + k * 570
        s += text(x, 160, t, 's', 'middle', GREY) + text(x, 250, f.replace('N', span('N', BLUE)), 'f', 'middle')
        s += text(x, 310, n, 's', 'middle')
    s += text(900, 410, 'Неподелённая пара электронов азота присоединяет H⁺ — амины основания; предельные сильнее аммиака', 's', 'middle', BLUE)
    s += text(900, 530, 'Анилин C₆H₅NH₂', 't', 'middle')
    s += box(300, 640, 300, 90, 'нитробензол|C₆H₅NO₂', '#F7EFC8') + box(900, 640, 300, 90, 'анилин|C₆H₅NH₂', '#fff')
    s += box(1500, 640, 340, 90, '2,4,6-триброманилин|белый осадок', '#F4F1E6')
    s += arrow(455, 640, 745, 640, INK, 5) + text(600, 615, '+6[H], Зинин, 1842', 's', 'middle')
    s += arrow(1055, 640, 1325, 640, INK, 5) + text(1190, 615, '+3Br₂ (бромная вода)', 's', 'middle')
    s += text(900, 780, 'основность: анилин < аммиак < метиламин', 't', 'middle', RED)
    s += text(900, 830, 'кольцо оттягивает пару азота — анилин лакмус не окрашивает', 's', 'middle')
    return s


# 7. Аминокислота и пептид ---------------------------------------------------------------------------
def amino_acid():
    s = text(900, 52, 'Аминокислоты: две группы и пептидная связь', 'h', 'middle')
    s += card(30, 90, 1740, 380) + card(30, 490, 1740, 420)
    s += text(900, 230, span('H₂N', BLUE) + '–CH₂–' + span('COOH', RED), 'f', 'middle')
    s += text(700, 300, 'основная группа', 's', 'middle', BLUE) + text(1100, 300, 'кислотная группа', 's', 'middle', RED)
    s += text(330, 400, '+ HCl → [H₃NCH₂COOH]Cl', 's', 'middle', BLUE) + text(1470, 400, '+ NaOH → H₂NCH₂COONa + H₂O', 's', 'middle', RED)
    s += text(900, 400, 'глицин амфотерен', 't', 'middle')
    s += text(900, 560, 'Глицин + аланин → дипептид + вода', 't', 'middle')
    s += text(900, 660, 'H₂N–CH₂–CO' + span('–OH  +  H–', GREY) + 'NH–CH(CH₃)–COOH', 't', 'middle')
    s += arrow(900, 690, 900, 740, INK, 4)
    s += text(900, 800, 'H₂N–CH₂–' + span('CO–NH', RED) + '–CH(CH₃)–COOH  +  H₂O', 't', 'middle')
    s += text(900, 860, 'пептидная связь –CO–NH–; в пептиде из n остатков — n − 1 связей', 's', 'middle', RED)
    return s


# 8. Структуры белка -----------------------------------------------------------------------------------
def protein_structure():
    s = text(900, 52, 'Четыре структуры белка', 'h', 'middle')
    titles = [('Первичная', 'последовательность|пептидные связи'), ('Вторичная', 'спираль|водородные связи'),
              ('Третичная', 'клубок|–S–S– мостики'), ('Четвертичная', 'несколько цепей|гемоглобин — 4')]
    for k, (t, d) in enumerate(titles):
        x = 30 + k * 440
        cx = x + 205
        s += card(x, 90, 410, 720)
        s += text(cx, 150, t, 't', 'middle')
        if k == 0:
            cols = ['#E57373', '#7FB3E0', '#F2C230', '#5DAA6F', '#B39DDB', '#E57373', '#7FB3E0']
            s += ''.join(f'<circle cx="{cx - 150 + j * 50}" cy="400" r="22" fill="{c}" stroke="{INK}" stroke-width="2"/>' for j, c in enumerate(cols))
        elif k == 1:
            pts = [(cx + 70 * math.sin(t / 6), 230 + t * 3) for t in range(0, 100)]
            s += f'<polyline points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="none" stroke="{BLUE}" stroke-width="8"/>'
        elif k == 2:
            s += f'<path d="M{cx - 90} 300 C {cx - 160} 420, {cx + 40} 520, {cx + 100} 420 S {cx - 20} 260, {cx + 60} 300 S {cx + 120} 480, {cx - 40} 500 S {cx - 140} 360, {cx - 30} 360" fill="none" stroke="{GREEN}" stroke-width="8"/>'
            s += f'<line x1="{cx - 10}" y1="380" x2="{cx + 60}" y2="420" stroke="{ORANGE}" stroke-width="6" stroke-dasharray="6 5"/>'
        else:
            for j, (dx, dy, c) in enumerate(((-60, -60, '#E57373'), (60, -60, '#7FB3E0'), (-60, 60, '#7FB3E0'), (60, 60, '#E57373'))):
                s += f'<circle cx="{cx + dx}" cy="{400 + dy}" r="56" fill="{c}" stroke="{INK}" stroke-width="3" opacity=".9"/>'
        s += lines_at(cx, 640, d.split('|'), 's', step=38)
    s += text(900, 860, 'Денатурация разрушает вторичную, третичную и четвертичную структуры; первичная сохраняется', 's', 'middle', RED)
    return s


# 9. Цветные реакции ----------------------------------------------------------------------------------
def protein_tests():
    s = text(900, 52, 'Белки: цветные реакции и денатурация', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    items = [('NaOH + CuSO₄', '#8E44AD', None, 'фиолетовая окраска', 'биуретовая — пептидные связи'),
             ('конц. HNO₃', '#F2C230', None, 'жёлтая окраска', 'ксантопротеиновая — бензольные кольца'),
             ('нагревание', '#F4F1E6', 'flakes', 'хлопья, белок свернулся', 'денатурация — первичная цела')]
    for k, (r, fill, extra, res, why) in enumerate(items):
        cx = 330 + k * 570
        s += text(cx, 160, 'белок + ' + r, 't', 'middle')
        s += tube(cx, 220, fill, 320)
        if extra:
            s += ''.join(f'<ellipse cx="{cx - 14 + (j * 19) % 30}" cy="{280 + j * 34}" rx="16" ry="9" fill="#fff" stroke="{INK}" stroke-width="2"/>' for j in range(7))
        s += text(cx, 610, res, 't', 'middle') + text(cx, 655, why, 's', 'middle', GREY)
    s += text(900, 780, 'Горение шерсти и шёлка — запах жжёной шерсти; гидролиз белка — до аминокислот', 's', 'middle')
    return s


# 10. Ферменты -----------------------------------------------------------------------------------------
def enzyme():
    s = text(900, 52, 'Ферменты — белковые катализаторы', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 150, 'Замок и ключ', 't', 'middle')
    s += f'<path d="M150 520 V 340 H 330 L 380 400 L 430 340 H 610 V 520 Z" fill="#7FB3E0" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M340 230 H 420 V 300 L 380 350 L 340 300 Z" fill="#F2C230" stroke="{INK}" stroke-width="3"/>'
    s += arrow(380, 300, 380, 330, INK, 3)
    s += text(380, 210, 'вещество', 's', 'middle') + text(380, 570, 'фермент, активный центр', 's', 'middle')
    s += lines_at(460, 680, ['избирательность: одна реакция', 'или группа однотипных', 'каталаза: 2H₂O₂ → 2H₂O + O₂'], 's', step=40)
    x0, y0, w, h = 990, 470, 700, 270
    s += f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{INK}" stroke-width="3"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h}" stroke="{INK}" stroke-width="3"/>'
    tpts = [(x0 + t * w / 80, y0 - h * max(0, math.exp(-((t - 40) / 12) ** 2) if t <= 40 else max(0, 1 - (t - 40) / 30))) for t in range(0, 81)]
    s += f'<polyline points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in tpts)}" fill="none" stroke="{RED}" stroke-width="5"/>'
    s += text(x0 + w / 2, y0 + 40, '≈ 40 °C', 's', 'middle', RED) + text(x0 + 70 * w / 80, y0 + 40, '70 °C', 's', 'middle') + text(x0 + w, y0 + 75, 'температура', 'cap', 'end')
    s += text(x0 + 10, y0 - h - 15, 'активность', 'cap')
    x1, y1 = 990, 830
    s += f'<line x1="{x1}" y1="{y1}" x2="{x1 + w}" y2="{y1}" stroke="{INK}" stroke-width="3"/>'
    for c, col, lab in ((1.75, ORANGE, 'пепсин 1,5–2'), (7, BLUE, 'каталаза ≈ 7')):
        pts = [(x1 + p * w / 14, y1 - 200 * math.exp(-((p - c) / 1.2) ** 2)) for p in [i / 10 for i in range(0, 141)]]
        s += f'<polyline points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="5"/>'
        s += text(x1 + c * w / 14, y1 - 215, lab, 's', 'middle', col)
    s += text(x1 + w, y1 + 40, 'pH', 'cap', 'end')
    return s


# 11. Распознавание и цепочка -------------------------------------------------------------------------
def recognition():
    s = text(900, 52, 'Распознавание и цепочка к анилину', 'h', 'middle')
    s += card(30, 90, 1120, 960) + card(1180, 90, 590, 960)
    rows = [('I₂', 'синее окрашивание', 'крахмал'), ('Cu(OH)₂, без t', 'ярко-синий раствор', 'глюкоза, сахароза'),
            ('Cu(OH)₂, t', 'красный Cu₂O', 'глюкоза'), ('Ag₂O (NH₃), t', 'серебряное зеркало', 'глюкоза'),
            ('NaOH + CuSO₄', 'фиолетовая', 'белки'), ('конц. HNO₃', 'жёлтая', 'белки'),
            ('бромная вода', 'белый осадок', 'анилин, фенол'), ('лакмус', 'синий', 'предельные амины')]
    s += text(200, 150, 'реактив', 's', 'middle', GREY) + text(560, 150, 'признак', 's', 'middle', GREY) + text(920, 150, 'кто даёт', 's', 'middle', GREY)
    for k, (r, f, c) in enumerate(rows):
        y = 220 + k * 100
        s += f'<rect x="60" y="{y - 40}" width="1060" height="84" rx="12" fill="{"#fff" if k % 2 else "#F7F5EF"}"/>'
        s += text(200, y + 10, r, 's', 'middle') + text(560, y + 10, f, 's', 'middle') + text(920, y + 10, c, 's', 'middle', BLUE)
    s += text(590, 1010, 'сахароза и крахмал серебряного зеркала не дают', 's', 'middle', RED)
    chain_ = ['CH₄', 'C₂H₂', 'C₆H₆', 'C₆H₅NO₂', 'C₆H₅NH₂']
    conds = ['1500 °C', '600 °C', 'HNO₃, H₂SO₄ конц.', '[H] — Зинин']
    for k, n in enumerate(chain_):
        y = 170 + k * 200
        s += box(1475, y, 300, 76, n, '#F7EFC8' if k in (0, 4) else '#fff', cls='t')
        if k < 4:
            s += arrow(1475, y + 40, 1475, y + 160, RED, 5) + text(1495, y + 110, conds[k], 's', 'start', BLUE)
    return s


if __name__ == '__main__':
    jobs = {
        'carb-classes.png': (carb_classes(), 1800, 870),
        'glucose.png': (glucose(), 1800, 940),
        'glucose-tests.png': (glucose_tests(), 1800, 920),
        'starch-cellulose.png': (starch_cellulose(), 1800, 940),
        'starch-hydrolysis.png': (starch_hydrolysis(), 1800, 880),
        'amines.png': (amines(), 1800, 920),
        'amino-acid.png': (amino_acid(), 1800, 940),
        'protein-structure.png': (protein_structure(), 1800, 900),
        'protein-tests.png': (protein_tests(), 1800, 880),
        'enzyme.png': (enzyme(), 1800, 940),
        'recognition.png': (recognition(), 1800, 1080),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
