"""Рисунки недели 22 химии (course/week-22/pics/*.png): строение полимеров, полимеризация, вулканизация, капрон,
волокна, пластики и среда, качественные реакции, генетическая связь, алгоритм вывода формулы.

Факты — по выжимке course/textbooks/chem-22-polymers-synthesis.md (Х11-1 § 30–36). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w22.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render, span
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = chem(s.replace('ₙ', '\x02')).replace('\x02', '<tspan baseline-shift="-0.28em" font-size="68%">n</tspan>')
    return _text(x, y, s, cls, anchor, fill)

OUT = ROOT / 'course' / 'week-22' / 'pics'
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


def bead(x, y, r=16, fill='#F7EFC8'):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'


def chain(pts, fill='#F7EFC8', r=16, w=4):
    s = ''.join(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{INK}" stroke-width="{w}"/>' for a, b in zip(pts, pts[1:]))
    return s + ''.join(bead(x, y, r, fill) for x, y in pts)


# 1. Строение полимеров ------------------------------------------------------------------------------
def polymer_structure():
    s = text(900, 52, 'Полимер: мономер, звено, строение', 'h', 'middle')
    s += card(30, 90, 1740, 330)
    s += text(200, 160, 'мономер', 't', 'middle') + text(200, 260, 'CH₂=CH₂', 'f', 'middle') + text(200, 320, 'этилен', 's', 'middle', GREY)
    s += arrow(340, 250, 470, 250, INK, 5) + text(405, 230, 'n', 't', 'middle')
    s += text(700, 160, 'звено', 't', 'middle') + text(700, 260, '–CH₂–CH₂–', 'f', 'middle') + text(700, 320, 'M = 28', 's', 'middle', GREY)
    s += arrow(930, 250, 1060, 250, INK, 5)
    s += text(1400, 160, 'макромолекула', 't', 'middle') + text(1400, 260, '(–CH₂–CH₂–)ₙ', 'f', 'middle')
    s += text(1400, 320, 'n = M(полимера) : M(звена)', 's', 'middle', RED)
    items = [('Линейное', 'ПЭ низкого давления,|натуральный каучук, целлюлоза'),
             ('Разветвлённое', 'ПЭ высокого давления,|крахмал (амилопектин)'),
             ('Сетчатое', 'резина,|фенолформальдегидные смолы')]
    for k, (t, d) in enumerate(items):
        x = 30 + k * 590
        s += card(x, 440, 560, 470)
        cx = x + 280
        s += text(cx, 500, t, 't', 'middle')
        if k == 0:
            s += chain([(cx - 220 + j * 44, 640 + 18 * math.sin(j)) for j in range(11)])
        elif k == 1:
            s += chain([(cx - 220 + j * 44, 640) for j in range(11)]) + chain([(cx - 88, 640), (cx - 60, 600), (cx - 30, 565)]) + chain([(cx + 88, 640), (cx + 115, 680), (cx + 145, 715)])
        else:
            for r in range(3):
                s += chain([(cx - 200 + j * 50, 580 + r * 60) for j in range(9)])
            for j in (1, 4, 7):
                s += f'<line x1="{cx - 200 + j * 50}" y1="580" x2="{cx - 200 + j * 50}" y2="700" stroke="{RED}" stroke-width="5"/>'
        s += lines_at(cx, 800, d.split('|'), 's', step=34)
    return s


# 2. Полимеризация -----------------------------------------------------------------------------------
def polymerization():
    s = text(900, 52, 'Полимеризация: двойная связь раскрывается', 'h', 'middle')
    s += card(30, 90, 1740, 300)
    s += text(400, 200, 'nCH₂=CH₂', 'f', 'middle') + arrow(600, 185, 780, 185, INK, 5) + text(690, 160, 't, p, кат.', 's', 'middle', BLUE)
    s += text(1000, 200, '(–CH₂–CH₂–)ₙ', 'f', 'middle')
    s += text(400, 300, 'nCH₂=CH–CH₃', 'f', 'middle') + arrow(600, 285, 780, 285, INK, 5)
    s += text(1040, 300, '(–CH₂–CH(CH₃)–)ₙ', 'f', 'middle')
    s += lines_at(1520, 220, ['без побочных продуктов;', 'звено = мономер по составу;', 'масса сохраняется'], 's', step=36, color=RED)
    rows = [('Полиэтилен', 'CH₂=CH₂', 'плёнки, трубы, тара'), ('Полипропилен', 'CH₂=CH–CH₃', 'трубы, мешки; лёгкий, прочный'),
            ('ПВХ', 'CH₂=CHCl', 'линолеум, трубы; при горении — HCl'), ('Полистирол', 'C₆H₅–CH=CH₂', 'изоляция, пенопласт'),
            ('Тефлон', 'CF₂=CF₂', 'посуда, детали; очень стоек'), ('Органическое стекло', 'метилметакрилат', 'прозрачное, не хрупкое')]
    s += card(30, 410, 1740, 560)
    s += text(330, 470, 'полимер', 's', 'middle', GREY) + text(830, 470, 'мономер', 's', 'middle', GREY) + text(1390, 470, 'применение, свойства', 's', 'middle', GREY)
    for k, (a, b, c) in enumerate(rows):
        y = 540 + k * 70
        s += f'<rect x="60" y="{y - 32}" width="1680" height="62" rx="10" fill="{"#fff" if k % 2 else "#F7F5EF"}"/>'
        s += text(330, y + 10, a, 't', 'middle') + text(830, y + 10, b, 't', 'middle', BLUE) + text(1390, y + 10, c, 's', 'middle')
    return s


# 3. Вулканизация -----------------------------------------------------------------------------------
def vulcanization():
    s = text(900, 52, 'Вулканизация: каучук → резина', 'h', 'middle')
    s += card(30, 90, 760, 760) + card(1010, 90, 760, 760)
    s += text(410, 150, 'Каучук — линейные цепи', 't', 'middle')
    for r in range(4):
        s += f'<polyline points="{" ".join(f"{80 + j * 40},{260 + r * 110 + 20 * math.sin(j + r):.0f}" for j in range(17))}" fill="none" stroke="{GREEN}" stroke-width="7"/>'
    s += lines_at(410, 760, ['мягкий, липкий в жару,', 'хрупкий на холоде'], 's', step=34)
    s += arrow(810, 470, 990, 470, RED, 7) + text(900, 440, '+ S, t', 't', 'middle', RED)
    s += text(1390, 150, 'Резина — сетка', 't', 'middle')
    for r in range(4):
        s += f'<polyline points="{" ".join(f"{1060 + j * 40},{260 + r * 110 + 20 * math.sin(j + r):.0f}" for j in range(17))}" fill="none" stroke="{GREEN}" stroke-width="7"/>'
    for r in range(3):
        for j in (3, 8, 13):
            x = 1060 + j * 40
            y1 = 260 + r * 110 + 20 * math.sin(j + r)
            y2 = 260 + (r + 1) * 110 + 20 * math.sin(j + r + 1)
            s += f'<line x1="{x}" y1="{y1:.0f}" x2="{x}" y2="{y2:.0f}" stroke="{ORANGE}" stroke-width="6"/>'
            s += text(x + 12, (y1 + y2) / 2 + 8, '–S–S–', 'cap', 'start').replace('class="cap"', 'class="cap" style="fill:#D98A2B"') if j == 8 and r == 1 else ''
    s += lines_at(1390, 760, ['мостики –S–S– сшивают цепи:', 'прочнее и упругая; + сажа'], 's', step=34)
    s += text(900, 900, 'Эбонит — больше 30 % серы: твёрдый, не эластичный', 's', 'middle')
    return s


# 4. Капрон -------------------------------------------------------------------------------------------
def caprone():
    s = text(900, 52, 'Поликонденсация: капрон', 'h', 'middle')
    s += card(30, 90, 1740, 780)
    s += text(900, 170, 'ε-аминокапроновая кислота: две функциональные группы', 't', 'middle')
    for k in range(3):
        x = 330 + k * 560
        s += text(x, 280, span('H₂N', BLUE) + '–(CH₂)₅–' + span('COOH', RED), 't', 'middle')
    s += f'<path d="M495 300 Q 530 360 610 300" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 6"/>'
    s += f'<path d="M1055 300 Q 1090 360 1170 300" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 6"/>'
    s += text(553, 395, '− H₂O', 's', 'middle', GREY) + text(1113, 395, '− H₂O', 's', 'middle', GREY)
    s += arrow(900, 430, 900, 500, INK, 5)
    s += text(900, 570, '…–NH–(CH₂)₅–' + span('CO–NH', RED) + '–(CH₂)₅–' + span('CO–NH', RED) + '–(CH₂)₅–CO–…', 't', 'middle')
    s += text(900, 660, 'nH₂N(CH₂)₅COOH → [–NH(CH₂)₅CO–]ₙ + nH₂O', 't', 'middle')
    s += lines_at(900, 740, ['на каждое звено выделяется молекула воды — масса полимера меньше массы мономера',
                             'капрон — полиамид (группа –CO–NH–): не мнётся, но не выносит горячего утюга'], 's', step=42)
    return s


# 5. Волокна ---------------------------------------------------------------------------------------------
def fibers():
    s = text(900, 52, 'Волокна', 'h', 'middle')
    s += box(900, 150, 300, 70, 'волокна', '#F7EFC8', cls='t')
    cols = [('Природные', ['растительные — хлопок, лён', '(целлюлоза)', 'животные — шерсть, шёлк', '(белки)'], GREEN),
            ('Искусственные', ['из природных полимеров', 'химической переработкой:', 'вискозное, ацетатное'], ORANGE),
            ('Синтетические', ['из синтетических полимеров:', 'полиамиды –CO–NH– —', 'капрон, нейлон, кевлар;', 'полиэфир –COO– — лавсан'], BLUE)]
    for k, (t, rows, col) in enumerate(cols):
        cx = 300 + k * 600
        s += arrow(900, 188, cx, 300, GREY, 4)
        s += f'<rect x="{cx - 270}" y="310" width="540" height="420" rx="18" fill="#fff" stroke="{col}" stroke-width="5"/>'
        s += text(cx, 370, t, 't', 'middle', col)
        s += lines_at(cx, 440, rows, 's', step=42)
    s += text(900, 800, 'Искусственные — из целлюлозы, синтетические — из полимеров, полученных синтезом', 's', 'middle', RED)
    return s


# 6. Пластик и среда ----------------------------------------------------------------------------------
def plastic_environment():
    s = text(900, 52, 'Пластики и окружающая среда', 'h', 'middle')
    s += card(30, 90, 860, 780) + card(910, 90, 860, 780)
    s += f'<path d="M300 300 h 80 v 40 q 40 20 40 60 v 280 q 0 30 -30 30 h -100 q -30 0 -30 -30 v -280 q 0 -40 40 -60 z" fill="#DCEBF5" stroke="{INK}" stroke-width="4"/>'
    s += f'<circle cx="620" cy="480" r="130" fill="#fff" stroke="{INK}" stroke-width="5"/><line x1="620" y1="480" x2="620" y2="380" stroke="{RED}" stroke-width="6"/><line x1="620" y1="480" x2="690" y2="520" stroke="{INK}" stroke-width="6"/>'
    s += text(620, 670, '100–500 лет', 'f', 'middle', RED)
    s += lines_at(460, 760, ['не разлагается природными факторами;', 'при сжигании — диоксины, кислотные газы'], 's', step=36)
    s += text(1340, 160, 'Что делать', 't', 'middle', GREEN)
    rows = ['переработка и повторное использование', 'бумажные пакеты — целлюлоза быстро разлагается', 'биоразлагаемые пластики',
            'ограничение одноразовых пакетов, налоги', 'не сжигать пластик']
    for k, r in enumerate(rows):
        y = 260 + k * 110
        s += f'<circle cx="980" cy="{y - 8}" r="14" fill="{GREEN}"/>' + text(1010, y, r, 's')
    s += text(1340, 820, 'Казахстан: заводы в Атырау и Павлодаре', 's', 'middle', GREY)
    return s


# 7. Качественные реакции ---------------------------------------------------------------------------
def qualitative():
    s = text(900, 52, 'Качественные реакции органических веществ', 'h', 'middle')
    s += card(30, 90, 1740, 1000)
    rows = [('Бромная вода', 'обесцвечивание', 'алкены, алкины'), ('Бромная вода', 'белый осадок', 'фенол, анилин'),
            ('KMnO₄', 'обесцвечивание, бурый осадок', 'алкены, алкины'), ('FeCl₃', 'фиолетовое', 'фенол'),
            ('Cu(OH)₂, без t', 'ярко-синий раствор', 'многоатомные спирты, глюкоза'), ('Cu(OH)₂, t', 'красный Cu₂O', 'альдегиды, глюкоза'),
            ('Ag₂O (NH₃), t', 'серебряное зеркало', 'альдегиды, глюкоза, HCOOH'), ('Лакмус', 'красный / синий', 'кислоты / амины'),
            ('I₂', 'синее', 'крахмал'), ('NaOH + CuSO₄', 'фиолетовое', 'белки'), ('Конц. HNO₃', 'жёлтое', 'белки')]
    s += text(330, 150, 'реактив', 's', 'middle', GREY) + text(860, 150, 'признак', 's', 'middle', GREY) + text(1400, 150, 'кто даёт', 's', 'middle', GREY)
    for k, (r, f, c) in enumerate(rows):
        y = 215 + k * 78
        s += f'<rect x="60" y="{y - 34}" width="1680" height="70" rx="10" fill="{"#fff" if k % 2 else "#F7F5EF"}"/>'
        s += text(330, y + 10, r, 't', 'middle') + text(860, y + 10, f, 's', 'middle') + text(1400, y + 10, c, 's', 'middle', BLUE)
    s += text(900, 1060, 'бензол бромную воду не обесцвечивает; одним Cu(OH)₂ различают глицерин, альдегид и белок', 's', 'middle', RED)
    return s


# 8. Генетическая связь ----------------------------------------------------------------------------
def genetic_link():
    s = text(900, 52, 'Генетическая связь органических веществ', 'h', 'middle')
    s += card(30, 90, 1740, 360) + card(30, 470, 1740, 560)
    s += text(900, 145, 'Генетический ряд метана', 't', 'middle')
    ring = ['C', 'CH₄', 'CH₃Cl', 'CH₃OH', 'HCHO', 'HCOOH']
    conds = ['H₂, кат.', 'Cl₂, свет', 'KOH водн.', 'CuO, t', 'Ag₂O, t']
    for k, n in enumerate(ring):
        x = 160 + k * 296
        s += box(x, 260, 200, 70, n, '#F7EFC8' if k in (0, 5) else '#fff', cls='t')
        if k < 5:
            s += arrow(x + 102, 260, x + 194, 260, RED, 4) + text(x + 148, 325, conds[k], 'cap', 'middle')
    s += text(900, 410, 'алкан → галогеналкан → спирт → альдегид → кислота', 's', 'middle', BLUE)
    s += text(900, 525, 'Важнейшие превращения', 't', 'middle')
    nodes = {'метан': (200, 640), 'ацетилен': (560, 640), 'ацетальдегид': (960, 580), 'уксусная к-та': (1400, 580),
             'винилхлорид': (960, 700), 'ПВХ': (1400, 700), 'бензол': (560, 840), 'нитробензол': (960, 840), 'анилин': (1400, 840),
             'этанол': (200, 960), 'бутадиен': (560, 960), 'каучук': (960, 960)}
    links = [('метан', 'ацетилен'), ('ацетилен', 'ацетальдегид'), ('ацетальдегид', 'уксусная к-та'), ('ацетилен', 'винилхлорид'),
             ('винилхлорид', 'ПВХ'), ('ацетилен', 'бензол'), ('бензол', 'нитробензол'), ('нитробензол', 'анилин'),
             ('этанол', 'бутадиен'), ('бутадиен', 'каучук')]
    for a, b in links:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        s += arrow(x1 + ux * 120, y1 + uy * 36, x2 - ux * 120, y2 - uy * 36, GREY, 4)
    s += text(1400, 970, 'этанол → этилен → ПЭ', 's', 'middle', GREY)
    for n, (x, y) in nodes.items():
        s += box(x, y, 220, 64, n, '#E2F1E6' if n in ('ПВХ', 'каучук') else '#fff')
    return s


# 9. Алгоритм вывода формулы -----------------------------------------------------------------------
def formula_algorithm():
    s = text(900, 52, 'Как вывести формулу органического вещества', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    s += box(450, 200, 620, 110, 'массовые доли|n = ω(C)/12 : ω(H)/1 : ω(O)/16', '#FFF6E8')
    s += box(1350, 200, 620, 110, 'продукты горения|n(C) = n(CO₂); n(H) = 2n(H₂O)', '#DCEBF5')
    s += arrow(450, 258, 820, 352, INK, 4) + arrow(1350, 258, 980, 352, INK, 4)
    s += text(1700, 300, 'm(O) = m − m(C) − m(H)', 's', 'end', RED)
    s += box(900, 400, 520, 80, 'простейшая формула', '#fff', cls='t')
    s += arrow(900, 442, 900, 518, INK, 4)
    s += box(900, 560, 700, 80, 'M = D · M(газа): H₂ — 2, He — 4, воздух — 29', '#fff')
    s += arrow(900, 602, 900, 678, INK, 4)
    s += box(900, 720, 600, 80, 'истинная формула (кратность)', '#fff', cls='t')
    s += arrow(900, 762, 900, 818, INK, 4)
    s += box(900, 870, 1100, 80, 'класс по свойствам: NaHCO₃ — кислота; зеркало — альдегид; Br₂ — C=C', '#E2F1E6')
    s += lines_at(260, 560, ['CH₂O:', 'M 30 — формальдегид', 'M 60 — уксусная кислота', 'M 180 — глюкоза'], 's', 'middle', step=38, color=GREY)
    return s


if __name__ == '__main__':
    jobs = {
        'polymer-structure.png': (polymer_structure(), 1800, 940),
        'polymerization.png': (polymerization(), 1800, 1000),
        'vulcanization.png': (vulcanization(), 1800, 940),
        'caprone.png': (caprone(), 1800, 900),
        'fibers.png': (fibers(), 1800, 860),
        'plastic-environment.png': (plastic_environment(), 1800, 900),
        'qualitative.png': (qualitative(), 1800, 1110),
        'genetic-link.png': (genetic_link(), 1800, 1060),
        'formula-algorithm.png': (formula_algorithm(), 1800, 980),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
