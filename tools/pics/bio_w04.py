"""Рисунки недели 4 биологии (course/biology/week-04/pics/*.png): АТФ, этапы энергетического обмена, митохондрия,
хлоропласт, фазы фотосинтеза, сравнение дыхания и фотосинтеза.

Факты — по выжимке course/textbooks/bio-04-metabolism.md (Б7а, Б9, Б10-1, Б11-1). АТФ: 2 + 36 = 38.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w04.py
"""
from __future__ import annotations

import math

from common import (GREEN, GREY, INK, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, PAPER, RED, ROOT, arrow, chem, dna_loop, lab, render,
                    ribosomes, text)

OUT = ROOT / 'course' / 'biology' / 'week-04' / 'pics'
BLUE, ORANGE = '#3A57A7', '#D9822B'


def pentagon(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    return [(cx + r * math.cos(math.radians(-90 + 72 * i)), cy + r * math.sin(math.radians(-90 + 72 * i))) for i in range(5)]


def poly(pts: list[tuple[float, float]], fill: str, stroke: str, w: float = 5) -> str:
    return f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'


def nucleotide_chain(x: float, y: float, k: float, n_p: int) -> str:
    """Аденин — рибоза — n фосфатов (между фосфатами ~). k — масштаб. Возвращает SVG."""
    s = ''
    ax, rx = x, x + 210 * k
    p_x = [rx + 180 * k + i * 160 * k for i in range(n_p)]
    pent = pentagon(rx, y, 70 * k)
    s += f'<line x1="{ax + 90 * k:.0f}" y1="{y}" x2="{pent[4][0]:.0f}" y2="{pent[4][1]:.0f}" stroke="{INK}" stroke-width="{6 * k:.1f}"/>'
    s += f'<line x1="{pent[1][0]:.0f}" y1="{pent[1][1]:.0f}" x2="{p_x[0] - 50 * k:.0f}" y2="{y}" stroke="{INK}" stroke-width="{6 * k:.1f}"/>'
    for a, b in zip(p_x, p_x[1:]):
        s += f'<line x1="{a + 50 * k:.0f}" y1="{y}" x2="{b - 50 * k:.0f}" y2="{y}" stroke="{RED}" stroke-width="{6 * k:.1f}"/>'
        s += f'<text x="{(a + b) / 2:.0f}" y="{y - 14 * k:.0f}" text-anchor="middle" style="font-size:{60 * k:.0f}px;font-weight:800;fill:{RED}">~</text>'
    s += f'<rect x="{ax - 90 * k:.0f}" y="{y - 55 * k:.0f}" width="{180 * k:.0f}" height="{110 * k:.0f}" rx="{14 * k:.0f}" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="5"/>'
    s += poly(pent, LIGHT_GREEN, GREEN)
    s += ''.join(f'<circle cx="{px:.0f}" cy="{y}" r="{50 * k:.0f}" fill="{LIGHT_YELLOW}" stroke="{ORANGE}" stroke-width="5"/>'
                 f'<text x="{px:.0f}" y="{y + 14 * k:.0f}" text-anchor="middle" style="font-size:{40 * k:.0f}px;font-weight:800">Ф</text>' for px in p_x)
    return s


def atp() -> str:
    s = text(800, 55, 'АТФ — аденозинтрифосфорная кислота', 'h', 'middle')
    s += nucleotide_chain(210, 220, 1, 3)
    s += text(210, 330, 'аденин', 's', 'middle') + text(420, 330, 'рибоза', 's', 'middle')
    s += f'<path d="M550 300 v14 H970 v-14" fill="none" stroke="{INK}" stroke-width="3"/>' + text(760, 350, 'три остатка фосфорной кислоты', 's', 'middle')
    s += text(1080, 210, '~', 'f', 'start', RED) + text(1130, 205, 'макроэргическая связь', 's') + text(1130, 240, '(термин Ф. Липмана)', 'cap')
    s += f'<line x1="40" y1="410" x2="1560" y2="410" stroke="#DEDAD1" stroke-width="3"/>'
    s += text(60, 470, 'Отщепление последнего остатка фосфорной кислоты:', 't')
    s += nucleotide_chain(150, 570, 0.62, 2)
    s += text(560, 584, '+', 'f', 'middle')
    s += f'<circle cx="660" cy="570" r="31" fill="{LIGHT_YELLOW}" stroke="{ORANGE}" stroke-width="5"/>' + text(660, 580, 'Ф', 't', 'middle')
    s += text(740, 584, '+', 'f', 'middle') + text(790, 584, 'энергия', 't', 'start', RED)
    s += text(290, 650, 'АДФ', 't', 'middle') + text(660, 650, 'фосфат', 's', 'middle')
    s += text(1040, 560, chem('АТФ + H₂O → АДФ + H₃PO₄'), 't') + text(1040, 600, 'энергия идёт на работу клетки', 's')
    return s


def energy_stages() -> str:
    s = text(800, 55, 'Три этапа энергетического обмена', 'h', 'middle')
    stages = [('1. Подготовительный', ['вне клеток:', 'пищеварительный тракт'],
               ['белки → аминокислоты', 'полисахариды → простые сахара', 'жиры → глицерин', 'и жирные кислоты'], None, []),
              ('2. Бескислородный', ['гликолиз, в цитоплазме,', 'без кислорода'],
               ['глюкоза (6 C) →', '2 ПВК (3 C)'], '2 АТФ', ['без кислорода в мышцах:', 'ПВК → молочная кислота']),
              ('3. Кислородный', ['в митохондриях,', 'нужен кислород'],
               [chem('ПВК → CO₂ + H₂O'), 'цикл Кребса (матрикс),', 'дыхательная цепь (кристы)'], '36 АТФ', [])]
    for k, (title, where, lines, yield_, note) in enumerate(stages):
        x0 = 30 + k * 530
        s += f'<rect x="{x0}" y="100" width="480" height="470" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/>'
        s += f'<path d="M{x0} 160 V116 a16 16 0 0 1 16 -16 H{x0 + 464} a16 16 0 0 1 16 16 V160 Z" fill="{GREEN}"/>'
        s += text(x0 + 26, 142, title, 'w')
        s += ''.join(text(x0 + 240, 200 + j * 30, ln, 'cap', 'middle') for j, ln in enumerate(where))
        s += ''.join(text(x0 + 240, 290 + j * 38, ln, 's', 'middle') for j, ln in enumerate(lines))
        if yield_:
            s += f'<rect x="{x0 + 140}" y="425" width="200" height="66" rx="33" fill="{RED}"/>' + text(x0 + 240, 469, yield_, 't', 'middle', '#fff')
        s += ''.join(text(x0 + 240, 522 + j * 28, ln, 'cap', 'middle') for j, ln in enumerate(note))
        if k < 2:
            s += arrow(x0 + 484, 335, x0 + 526, 335, INK, 5)
    s += f'<rect x="330" y="610" width="940" height="90" rx="45" fill="{PAPER}" stroke="{RED}" stroke-width="4"/>'
    s += text(800, 667, 'На 1 молекулу глюкозы: 2 + 36 = 38 АТФ', 'h', 'middle')
    return s


def mitochondrion() -> str:
    s = text(800, 55, 'Митохондрия', 'h', 'middle')
    cx, cy, rx, ry = 780, 400, 560, 230
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#F6D2BF" stroke="#B4532A" stroke-width="7"/>'
    irx, iry = rx - 30, ry - 30
    edge = lambda x, sign: cy + sign * iry * math.sqrt(max(0.0, 1 - ((x - cx) / irx) ** 2))  # noqa: E731
    top_folds, bottom_folds = [420, 580, 740, 900, 1060], [500, 660, 820, 980, 1140]
    pts = []
    for x in range(cx - irx, cx + irx + 1, 10):
        for f in top_folds:
            if x <= f - 14 < x + 10:
                pts += [(f - 14, edge(f - 14, -1)), (f - 14, cy - 15), (f + 14, cy - 15), (f + 14, edge(f + 14, -1))]
        if not any(f - 14 <= x <= f + 14 for f in top_folds):
            pts.append((x, edge(x, -1)))
    for x in range(cx + irx, cx - irx - 1, -10):
        for f in bottom_folds:
            if x - 10 < f + 14 <= x:
                pts += [(f + 14, edge(f + 14, 1)), (f + 14, cy + 15), (f - 14, cy + 15), (f - 14, edge(f - 14, 1))]
        if not any(f - 14 <= x <= f + 14 for f in bottom_folds):
            pts.append((x, edge(x, 1)))
    s += poly(pts, '#FFF4EC', '#B4532A', 5)
    # АТФ-синтетаза — «грибки» на кристах со стороны матрикса
    for f, sign in [(t, -1) for t in top_folds] + [(b, 1) for b in bottom_folds]:
        ymid = cy + sign * 60
        for side in (-1, 1):
            x = f + side * 14
            s += f'<line x1="{x}" y1="{ymid}" x2="{x + side * 14}" y2="{ymid}" stroke="{BLUE}" stroke-width="3"/><circle cx="{x + side * 20}" cy="{ymid}" r="7" fill="{BLUE}"/>'
    s += dna_loop(340, 400, 38) + ribosomes([(300, 330), (330, 470), (395, 345), (1230, 380), (1250, 440), (1210, 470), (1195, 335)])
    s += (f'<path d="M1018 300 a 38 38 0 1 1 -2 -30" fill="none" stroke="{GREEN}" stroke-width="5"/>'
          + arrow(1014, 273, 1017, 265, GREEN, 3))
    s += lab(cx - 200, cy - ry + 3, 300, 120, 'наружная мембрана')
    s += lab(740, cy - 60, 800, 120, 'внутренняя мембрана — кристы:')
    s += text(800, 152, 'дыхательная цепь и АТФ-синтетаза', 'cap', 'middle')
    s += lab(980, 300, 1250, 120, 'матрикс: цикл Кребса')
    s += lab(340, 420, 300, 700, 'кольцевая ДНК') + lab(1250, 440, 1390, 700, 'рибосомы')
    s += text(780, 770, chem('O₂ — конечный акцептор электронов: соединяется с протонами, образуется вода'), 's', 'middle')
    return s


def chloroplast() -> str:
    s = text(800, 55, 'Хлоропласт', 'h', 'middle')
    cx, cy, rx, ry = 780, 400, 580, 240
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#E8F3E2" stroke="#1F5E36" stroke-width="5"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx - 14}" ry="{ry - 14}" fill="#EEF7E9" stroke="#1F5E36" stroke-width="4"/>'
    grana = [(440, 330), (640, 450), (840, 320), (1040, 440), (1180, 340)]
    for (a, b), (c, d) in zip(grana, grana[1:]):
        s += f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#2E8B57" stroke-width="5"/>'
    for gx, gy in grana:
        for j in range(6):
            s += f'<rect x="{gx - 50}" y="{gy - 60 + j * 20}" width="100" height="16" rx="8" fill="#5DAA6F" stroke="#1F5E36" stroke-width="2.5"/>'
    s += dna_loop(560, 560 - 30, 34) + ribosomes([(700, 560), (735, 545), (930, 520), (960, 560), (330, 430), (360, 470)])
    s += lab(cx - 260, cy - ry + 4, 330, 120, 'двойная оболочка')
    s += lab(840, 262, 860, 120, 'грана — стопка тилакоидов')
    s += lab(1180, 300, 1390, 170, 'тилакоид: световая фаза')
    s += lab(1080, 520, 1180, 720, 'строма: цикл Кальвина')
    s += lab(560, 548, 500, 720, 'кольцевая ДНК, РНК, рибосомы')
    return s


def photosynthesis_phases() -> str:
    s = text(800, 55, 'Две фазы фотосинтеза', 'h', 'middle')
    boxes = [(140, 'Световая фаза', 'мембраны тилакоидов', ['фотолиз воды:', chem('2H₂O → 4H⁺ + 4e⁻ + O₂'), 'синтез АТФ и НАДФ·H'], '#5DAA6F'),
             (900, 'Темновая фаза', 'строма · цикл Кальвина', [chem('фиксация CO₂'), 'на энергии АТФ и НАДФ·H', 'синтез глюкозы'], '#2E8B57')]
    for x0, title, where, lines, color in boxes:
        s += f'<rect x="{x0}" y="230" width="560" height="330" rx="18" fill="#fff" stroke="{color}" stroke-width="6"/>'
        s += f'<path d="M{x0} 296 V248 a18 18 0 0 1 18 -18 H{x0 + 542} a18 18 0 0 1 18 18 V296 Z" fill="{color}"/>'
        s += text(x0 + 28, 274, title, 'w') + text(x0 + 280, 340, where, 's', 'middle', GREY)
        s += ''.join(text(x0 + 280, 400 + j * 44, ln, 't', 'middle') for j, ln in enumerate(lines))
    # входы и выходы
    sun = 230, 140
    s += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="34" fill="#F7CB2D"/>' + ''.join(
        f'<line x1="{sun[0] + 46 * math.cos(a):.0f}" y1="{sun[1] + 46 * math.sin(a):.0f}" x2="{sun[0] + 62 * math.cos(a):.0f}" '
        f'y2="{sun[1] + 62 * math.sin(a):.0f}" stroke="#F7CB2D" stroke-width="6"/>' for a in [k * math.pi / 4 for k in range(8)])
    s += text(310, 150, 'свет', 't') + arrow(250, 185, 290, 222, ORANGE, 5)
    s += text(470, 150, chem('H₂O'), 't', 'middle') + arrow(470, 165, 470, 222, BLUE, 5)
    s += arrow(600, 222, 600, 140, BLUE, 5) + text(600, 120, chem('O₂ — из воды'), 't', 'middle')
    s += arrow(706, 395, 894, 395, RED, 7) + text(800, 375, 'АТФ,', 's', 'middle') + text(800, 440, 'НАДФ·H', 's', 'middle')
    s += text(1180, 150, chem('CO₂'), 't', 'middle') + arrow(1180, 165, 1180, 222, BLUE, 5)
    s += arrow(1180, 566, 1180, 640, GREEN, 6) + text(1180, 680, 'глюкоза (органические вещества)', 't', 'middle')
    s += text(420, 620, 'только на свету', 's', 'middle', GREY) + text(1200, 610, 'свет не нужен', 's', 'start', GREY)
    return s


def respiration_vs_photosynthesis() -> str:
    s = text(800, 55, 'Дыхание и фотосинтез', 'h', 'middle')
    cols = [(40, 300), (360, 590), (970, 590)]
    head = ['', 'Клеточное дыхание', 'Фотосинтез']
    rows = [('Где', ['цитоплазма и митохондрии;', 'во всех клетках'], ['хлоропласты', 'зелёных клеток']),
            ('Расходуется', [chem('органические вещества (глюкоза)'), chem('и O₂')], [chem('CO₂ и H₂O'), 'энергия света']),
            ('Образуется', [chem('CO₂ и H₂O')], [chem('глюкоза и O₂')]),
            ('Энергия', ['освобождается из', 'органических веществ'], ['света запасается', 'в органических веществах']),
            ('АТФ', ['образуется: 38', 'на 1 молекулу глюкозы'], ['образуется в световой фазе,', 'тратится в темновой'])]
    for (x, w), h, color in zip(cols, head, (None, ORANGE, GREEN)):
        if h:
            s += f'<rect x="{x}" y="100" width="{w}" height="64" rx="12" fill="{color}"/>' + text(x + w / 2, 143, h, 'w', 'middle')
    for k, (name, a, b) in enumerate(rows):
        y = 180 + k * 104
        s += f'<rect x="40" y="{y}" width="1520" height="96" rx="12" fill="{PAPER if k % 2 == 0 else "#fff"}"/>'
        s += text(64, y + 58, name, 't')
        for (x, w), cell in zip(cols[1:], (a, b)):
            top = y + 48 - (len(cell) - 1) * 17 + 9
            s += ''.join(text(x + w / 2, top + j * 34, ln, 's', 'middle') for j, ln in enumerate(cell))
    s += text(800, 735, 'Растения тоже дышат: в зелёных клетках на свету идут оба процесса.', 't', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'atp.png': (atp(), 1600, 690),
        'energy-stages.png': (energy_stages(), 1600, 730),
        'mitochondrion.png': (mitochondrion(), 1600, 800),
        'chloroplast.png': (chloroplast(), 1600, 760),
        'photosynthesis-phases.png': (photosynthesis_phases(), 1600, 710),
        'respiration-photosynthesis.png': (respiration_vs_photosynthesis(), 1600, 770),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
