"""Рисунки недели 17 химии (course/week-17/pics/*.png): тетраэдр метана и зигзаг, пять формул пропана, классификация,
типы атомов C, изомеры бутана и пентана, алгоритм названия, хлорирование метана, циклоалканы и цис-транс, вывод формулы.

Факты — по выжимке course/textbooks/chem-17-organic-alkanes.md (Х9-2 § 49–55; Х10-2 § 60–69). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w17.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = chem(s).replace('ₙ', '<tspan baseline-shift="-0.28em" font-size="68%">n</tspan>')
    return _text(x, y, s, cls, anchor, fill)

OUT = ROOT / 'course' / 'week-17' / 'pics'
BLUE, ORANGE, PURPLE = '#3A57A7', '#D98A2B', '#8E44AD'
CC, HC = '#3B3833', '#F4F1E6'                      # атомы углерода и водорода


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s'):
    rows = label.split('\n')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32))


def atom(x, y, label='C', r=24, fill=CC, color='#fff', stroke=INK):
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'
            f'<text x="{x:.0f}" y="{y + r * 0.36:.0f}" text-anchor="middle" style="font: 800 {r}px Manrope; fill:{color}">{label}</text>')


def bond(x1, y1, x2, y2, w=5, color=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w}"{d}/>'


def skeleton(pts, edges, colors=None, r=24, labels=None):
    s = ''.join(bond(*pts[a], *pts[b]) for a, b in edges)
    for k, (x, y) in enumerate(pts):
        s += atom(x, y, (labels or {}).get(k, 'C'), r, (colors or {}).get(k, CC))
    return s


# 1. Тетраэдр метана и зигзаг -----------------------------------------------------------------------
def methane_tetrahedron():
    s = text(900, 52, 'Углерод в алканах: тетраэдр и зигзаг', 'h', 'middle')
    s += card(30, 90, 840, 700) + card(900, 90, 870, 700)
    c = (450, 420)
    hs = [(450, 170), (240, 560), (640, 600), (560, 470)]
    for a, b in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
        s += bond(*hs[a], *hs[b], 2.5, GREY, '10 8')
    for k, h in enumerate(hs):
        s += bond(*c, *h, 6 if k != 3 else 4, INK, None if k != 3 else '12 6')
    for h in hs:
        s += atom(*h, 'H', 30, HC, INK)
    s += atom(*c, 'C', 36)
    s += f'<path d="M450 330 A 90 90 0 0 0 373 465" fill="none" stroke="{RED}" stroke-width="4"/>'
    s += text(330, 360, '109°28′', 't', 'end', RED)
    s += lines_at(450, 700, ['CH₄: атом C — sp³, четыре связи к вершинам тетраэдра', 'молекула объёмная, а не плоская'], 's', step=36)
    pts = [(1000 + k * 165, 360 if k % 2 else 470) for k in range(5)]
    s += skeleton(pts, [(k, k + 1) for k in range(4)], r=32)
    s += f'<path d="M1135 375 A 50 50 0 0 0 1194 380" fill="none" stroke="{RED}" stroke-width="4"/>'
    s += text(1165, 300, '109°28′', 's', 'middle', RED)
    s += text(1082, 560, 'C–C 0,154 нм', 's', 'middle')
    s += text(1335, 160, 'Цепь из пяти атомов C', 't', 'middle')
    s += lines_at(1335, 650, ['угол между связями 109°28′,', 'поэтому цепь — зигзаг, а не прямая;', 'вокруг C–C возможно вращение'], 's', step=36)
    return s


# 2. Пять формул пропана ----------------------------------------------------------------------------
def propane_formulas():
    s = text(900, 52, 'Пропан: пять видов формул', 'h', 'middle')
    titles = ['Молекулярная', 'Простейшая', 'Развёрнутая', 'Сокращённая', 'Скелетная']
    xs = [30, 370, 710, 1110, 1450]
    ws = [320, 320, 380, 320, 320]
    for x, w, t in zip(xs, ws, titles):
        s += card(x, 90, w, 600) + text(x + w / 2, 140, t, 't', 'middle')
    s += text(190, 400, 'C₃H₈', 'f', 'middle') + lines_at(190, 520, ['состав', 'молекулы'], 's')
    s += text(530, 400, 'C₃H₈', 'f', 'middle') + lines_at(530, 520, ['отношение атомов;', 'у пропана совпадает', 'с молекулярной'], 's')
    cx = [800, 900, 1000]
    for x in cx:
        s += text(x, 410, 'C', 't', 'middle')
        s += bond(x, 360, x, 330, 3) + text(x, 320, 'H', 's', 'middle')
        s += bond(x, 420, x, 450, 3) + text(x, 478, 'H', 's', 'middle')
    s += bond(812, 400, 888, 400, 3) + bond(912, 400, 988, 400, 3)
    s += bond(770, 400, 745, 400, 3) + text(732, 409, 'H', 's', 'middle')
    s += bond(1030, 400, 1055, 400, 3) + text(1068, 409, 'H', 's', 'middle')
    s += lines_at(900, 560, ['каждая связь —', 'чёрточкой'], 's')
    s += text(1270, 410, 'CH₃–CH₂–CH₃', 't', 'middle') + lines_at(1270, 520, ['чёрточками —', 'только связи C–C'], 's')
    s += f'<polyline points="1520,440 1610,360 1700,440" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += lines_at(1610, 520, ['только цепь C:', 'концы и изломы —', 'атомы углерода'], 's')
    s += text(900, 760, 'Простейшая формула отличается от молекулярной не всегда: у гексана C₆H₁₄ она C₃H₇', 's', 'middle')
    return s


# 3. Классификация --------------------------------------------------------------------------------
def organic_classification():
    s = text(900, 52, 'Классификация органических веществ', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    s += box(900, 160, 420, 70, 'Органические вещества', '#F7EFC8', cls='t')
    s += box(520, 290, 360, 70, 'Углеводороды (C, H)', '#fff', cls='t')
    s += box(1360, 290, 520, 70, 'Производные углеводородов', '#fff', cls='t')
    s += bond(900, 195, 520, 255, 3) + bond(900, 195, 1360, 255, 3)
    s += box(300, 430, 340, 70, 'Ациклические', '#E3EEF7', cls='t') + box(740, 430, 340, 70, 'Циклические', '#E2F1E6', cls='t')
    s += bond(520, 325, 300, 395, 3) + bond(520, 325, 740, 395, 3)
    for k, (n, ex) in enumerate((('алканы', 'CH₄'), ('алкены', 'C₂H₄'), ('алкадиены', 'C₃H₄'), ('алкины', 'C₂H₂'))):
        y = 540 + k * 85
        s += box(300, y, 340, 66, f'{n} · {ex}')
        s += bond(300, 465 if k == 0 else y - 52, 300, y - 33, 3)
    for k, (n, ex) in enumerate((('циклоалканы', 'C₃H₆'), ('арены', 'C₆H₆'))):
        y = 540 + k * 85
        s += box(740, y, 340, 66, f'{n} · {ex}')
        s += bond(740, 465 if k == 0 else y - 52, 740, y - 33, 3)
    groups = [('–OH', 'спирты, фенолы'), ('–CHO', 'альдегиды'), ('>C=O', 'кетоны'), ('–COOH', 'карбоновые кислоты'),
              ('–COO–', 'сложные эфиры'), ('–NH₂', 'амины'), ('–NO₂', 'нитросоединения')]
    for k, (g, cl) in enumerate(groups):
        y = 400 + k * 70
        s += f'<rect x="1130" y="{y - 30}" width="150" height="56" rx="10" fill="#fff" stroke="{RED}" stroke-width="3"/>'
        s += text(1205, y + 8, g, 't', 'middle', RED) + text(1300, y + 8, cl, 's')
    s += bond(1360, 325, 1360, 365, 3)
    s += lines_at(900, 915, ['предельные — только одинарные связи C–C; непредельные — есть двойные или тройные'], 'cap')
    return s


# 4. Типы атомов углерода -------------------------------------------------------------------------
def carbon_atom_types():
    s = text(900, 52, 'Первичный, вторичный, третичный, четвертичный атом C', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    P, S2, T, Q = '#5D9BD5', GREEN, ORANGE, RED
    # 2,2,3-триметилпентан: C1–C2–C3–C4–C5; метилы: два у C2, один у C3
    pts = [(330, 460), (560, 460), (790, 460), (1020, 460), (1250, 460), (560, 260), (560, 660), (790, 660)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 5), (1, 6), (2, 7)]
    colors = {0: P, 1: Q, 2: T, 3: S2, 4: P, 5: P, 6: P, 7: P}
    s += skeleton(pts, edges, colors, r=40)
    for k, n in enumerate(('1', '2', '3', '4', '5')):
        s += text(pts[k][0] + 34, pts[k][1] - 46, n, 's', 'middle', GREY)
    legend = [(P, 'первичный — 1 соседний C'), (S2, 'вторичный — 2 соседних C'), (T, 'третичный — 3 соседних C'), (Q, 'четвертичный — 4 соседних C')]
    for k, (c, t) in enumerate(legend):
        y = 250 + k * 90
        s += f'<circle cx="1360" cy="{y}" r="22" fill="{c}" stroke="{INK}" stroke-width="2.5"/>' + text(1395, y + 9, t, 's')
    s += text(900, 790, '2,2,3-триметилпентан: считаем соседние атомы C, а не атомы H', 't', 'middle')
    return s


# 5. Изомеры бутана и пентана ---------------------------------------------------------------------
def isomers_bp():
    s = text(900, 52, 'Изомеры: одна формула — разное строение', 'h', 'middle')
    s += card(30, 90, 640, 760) + card(700, 90, 1070, 760)
    s += text(350, 140, 'C₄H₁₀ — 2 изомера', 't', 'middle')
    s += skeleton([(130, 290), (230, 290), (330, 290), (430, 290)], [(0, 1), (1, 2), (2, 3)], r=26)
    s += text(280, 370, 'н-бутан', 't', 'middle') + text(280, 410, 't кип −0,5 °C', 's', 'middle')
    s += skeleton([(180, 600), (280, 600), (380, 600), (280, 500)], [(0, 1), (1, 2), (1, 3)], r=26)
    s += text(280, 680, '2-метилпропан (изобутан)', 't', 'middle') + text(280, 720, 't кип −11,4 °C', 's', 'middle', RED)
    s += text(1235, 140, 'C₅H₁₂ — 3 изомера', 't', 'middle')
    s += skeleton([(760 + k * 80, 330) for k in range(5)], [(k, k + 1) for k in range(4)], r=24)
    s += text(920, 410, 'н-пентан', 't', 'middle')
    s += skeleton([(1170, 330), (1250, 330), (1330, 330), (1410, 330), (1250, 250)], [(0, 1), (1, 2), (2, 3), (1, 4)], r=24)
    s += text(1290, 410, '2-метилбутан', 't', 'middle')
    s += skeleton([(1500, 330), (1580, 330), (1660, 330), (1580, 250), (1580, 410)], [(0, 1), (1, 2), (1, 3), (1, 4)], r=24)
    s += text(1580, 480, '2,2-диметилпропан', 't', 'middle')
    s += arrow(800, 580, 1700, 580, RED, 6)
    s += text(1250, 560, 'разветвление растёт → температура кипения ниже', 's', 'middle', RED)
    s += lines_at(1235, 680, ['Число изомеров: C₆ — 5, C₇ — 9, C₈ — 18, C₁₀ — 75', 'у метана, этана и пропана изомеров нет'], 's', step=40)
    return s


# 6. Алгоритм названия ------------------------------------------------------------------------------
def naming_algorithm():
    s = text(900, 52, 'Название по шагам: 2,3-диметилпентан', 'h', 'middle')
    s += card(30, 90, 1740, 880)
    # CH3–CH2–CH(CH3)–CH(CH3)–CH3, нумерация справа
    pts = [(260, 330), (460, 330), (660, 330), (860, 330), (1060, 330), (660, 170), (860, 170)]
    s += f'<rect x="215" y="285" width="890" height="90" rx="45" fill="#F7EFC8"/>'
    s += skeleton(pts, [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (3, 6)], {5: '#5D9BD5', 6: '#5D9BD5'}, r=34,
                  labels={0: 'C', 1: 'C', 2: 'C', 3: 'C', 4: 'C', 5: 'C', 6: 'C'})
    for k, n in enumerate(('5', '4', '3', '2', '1')):
        s += text(pts[k][0], 420, n, 't', 'middle', RED)
    s += text(1180, 180, 'метил', 's', 'start', '#5D9BD5') + bond(890, 170, 1170, 172, 2, '#5D9BD5', '6 6')
    steps = ['1) главная цепь — 5 атомов C (выделена)', '2) нумерация справа: заместители у C-2 и C-3 (слева было бы 3 и 4)',
             '3) два метила: ди-, номера 2,3', '4) один вид заместителей — алфавит не нужен; сумма 5 — наименьшая',
             '5) цепь из пяти C — пентан → 2,3-диметилпентан']
    s += lines_at(140, 540, steps, 's', 'start', step=52)
    s += text(900, 900, 'Главная цепь — самая длинная; нумерация — с конца, ближе к разветвлению', 't', 'middle')
    return s


# 7. Хлорирование метана ----------------------------------------------------------------------------
def mol_box(cx, cy, h_count):
    pos = [(cx, cy - 90), (cx + 90, cy), (cx, cy + 90), (cx - 90, cy)]
    s = ''.join(bond(cx, cy, x, y, 4) for x, y in pos) + atom(cx, cy, 'C', 34)
    for k, (x, y) in enumerate(pos):
        is_h = k < h_count
        s += atom(x, y, 'H' if is_h else 'Cl', 26 if is_h else 30, HC if is_h else '#B9D65C', INK)
    return s


def methane_chlorination():
    s = text(900, 52, 'Хлорирование метана на свету — четыре ступени', 'h', 'middle')
    s += card(30, 90, 1740, 680)
    names = [('CH₄', 'метан'), ('CH₃Cl', 'хлорметан'), ('CH₂Cl₂', 'дихлорметан'), ('CHCl₃', 'хлороформ'), ('CCl₄', 'тетрахлорметан')]
    for k, (f, n) in enumerate(names):
        cx = 170 + k * 365
        s += mol_box(cx, 330, 4 - k)
        s += text(cx, 500, f, 't', 'middle') + text(cx, 540, n, 's', 'middle')
        if k < 4:
            s += arrow(cx + 125, 330, cx + 235, 330, RED, 5)
            s += text(cx + 182, 300, '+Cl₂, hν', 's', 'middle', RED)
            s += text(cx + 182, 380, '−HCl', 's', 'middle', GREY)
    s += lines_at(900, 640, ['на каждой ступени один атом H замещается на Cl и выделяется HCl',
                             'механизм радикально-цепной; CHCl₃ — хлороформ, CCl₄ — тетрахлорметан'], 's', step=40)
    return s


# 8. Циклоалканы ------------------------------------------------------------------------------------
def polygon(cx, cy, n, r, fill='#fff', color=INK):
    pts = [(cx + r * math.cos(-math.pi / 2 + 2 * math.pi * k / n), cy + r * math.sin(-math.pi / 2 + 2 * math.pi * k / n)) for k in range(n)]
    return f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="{fill}" stroke="{color}" stroke-width="7" stroke-linejoin="round"/>', pts


def cycloalkanes():
    s = text(900, 52, 'Циклоалканы CₙH₂ₙ (n ≥ 3)', 'h', 'middle')
    s += card(30, 90, 1740, 520)
    items = [(3, 'циклопропан', 'C₃H₆', 'газ'), (4, 'циклобутан', 'C₄H₈', 'газ'), (5, 'циклопентан', 'C₅H₁₀', 'жидкость'), (6, 'циклогексан', 'C₆H₁₂', 'жидкость')]
    for k, (n, name, f, st) in enumerate(items):
        cx = 250 + k * 430
        poly, pts = polygon(cx, 280, n, 95, '#FBE3E4' if n < 5 else '#E2F1E6', RED if n < 5 else GREEN)
        s += poly
        s += text(cx, 440, name, 't', 'middle') + text(cx, 480, f + ' · ' + st, 's', 'middle')
    s += text(465, 560, 'напряжённые углы → цикл раскрывается (присоединение)', 's', 'middle', RED)
    s += text(1325, 560, 'углы почти 109°28′ → замещение, как у алканов', 's', 'middle', GREEN)
    s += card(30, 640, 1740, 400)
    s += text(900, 690, '1,2-диметилциклопропан: цис- и транс-изомеры', 't', 'middle')
    for k, (title, up2) in enumerate((('цис: метилы по одну сторону плоскости', True), ('транс: метилы по разные стороны', False))):
        x0 = 450 + k * 900
        tri = [(x0 - 110, 900), (x0 + 110, 900), (x0, 820)]
        s += f'<polygon points="{" ".join(f"{x},{y}" for x, y in tri)}" fill="#F3E3C9" stroke="{INK}" stroke-width="5"/>'
        s += f'<line x1="{x0 - 170}" y1="860" x2="{x0 + 170}" y2="860" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 8"/>'
        s += bond(x0 - 110, 900, x0 - 110, 790, 4) + text(x0 - 110, 775, 'CH₃', 's', 'middle')
        if up2:
            s += bond(x0 + 110, 900, x0 + 110, 790, 4) + text(x0 + 110, 775, 'CH₃', 's', 'middle')
        else:
            s += bond(x0 + 110, 900, x0 + 110, 945, 4) + text(x0 + 110, 975, 'CH₃', 's', 'middle')
        s += text(x0, 1022, title, 's', 'middle')
    return s


# 9. Вывод формулы ---------------------------------------------------------------------------------
def formula_derivation():
    s = text(900, 52, 'Вывод молекулярной формулы', 'h', 'middle')
    s += card(30, 90, 1740, 820)
    s += box(260, 230, 380, 110, 'ω(C), ω(H)\nиз анализа', '#E3EEF7', cls='t')
    s += box(260, 450, 380, 110, 'продукты сгорания\nCO₂ и H₂O', '#E3EEF7', cls='t')
    s += box(800, 230, 420, 110, 'C : H = ω(C)/12 : ω(H)/1\nделим на меньшее', '#fff')
    s += box(800, 450, 420, 130, 'n(C) = n(CO₂)\nn(H) = 2n(H₂O)\nпроверить кислород', '#fff')
    s += box(1360, 340, 400, 100, 'простейшая\nформула', '#F7EFC8', cls='t')
    s += arrow(452, 230, 588, 230, INK, 5) + arrow(452, 450, 588, 450, INK, 5)
    s += arrow(1012, 240, 1158, 320, INK, 5) + arrow(1012, 440, 1158, 360, INK, 5)
    s += box(800, 700, 560, 130, 'M = 2·D(H₂) = 29·D(возд)\n= 4·D(He) = 22,4·ρ', '#E2F1E6')
    s += box(1360, 700, 400, 130, 'молекулярная формула:\nмножитель =\nM / M(простейшей)', '#F3E3C9')
    s += arrow(1360, 392, 1360, 632, INK, 5) + arrow(1082, 700, 1158, 700, INK, 5)
    s += text(900, 870, 'ω(C) = 85,7 % у всех CₙH₂ₙ — без молярной массы формулу не найти', 's', 'middle', RED)
    return s


if __name__ == '__main__':
    jobs = {
        'methane-tetrahedron.png': (methane_tetrahedron(), 1800, 820),
        'propane-formulas.png': (propane_formulas(), 1800, 800),
        'organic-classification.png': (organic_classification(), 1800, 980),
        'carbon-atom-types.png': (carbon_atom_types(), 1800, 880),
        'isomers-bp.png': (isomers_bp(), 1800, 880),
        'naming-algorithm.png': (naming_algorithm(), 1800, 1000),
        'methane-chlorination.png': (methane_chlorination(), 1800, 800),
        'cycloalkanes.png': (cycloalkanes(), 1800, 1070),
        'formula-derivation.png': (formula_derivation(), 1800, 940),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
