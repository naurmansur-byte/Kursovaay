"""Рисунки недели 15 биологии (course/biology/week-15/pics/*.png): семь пар признаков гороха, опыт Менделя по поколениям,
чистота гамет, моногибридная и дигибридная решётки Пеннета, неполное доминирование, анализирующее скрещивание.

Факты — по выжимке course/textbooks/bio-15-mendel.md (Б9 § 33–37; Б10-2 § 69–70). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w15.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, render, text

OUT = ROOT / 'course' / 'biology' / 'week-15' / 'pics'
YEL, GRN, PUR, WHT = '#E8C547', '#6FAE4E', '#8E4FA8', '#FFFFFF'
DOM, REC = '#2F3E73', '#F08A3C'                  # доминантная и рецессивная аллель
PINK, REDF = '#F2A7C3', '#D8344A'


def panel(x, y, w, h, title=None, sub=None, fill=PAPER):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'
    if title:
        s += text(x + w / 2, y + 44, title, 't', 'middle')
    if sub:
        s += text(x + w / 2, y + 78, sub, 'cap', 'middle')
    return s


def seed(cx, cy, color, wrinkled=False, r=34):
    if not wrinkled:
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
    pts = []
    for k in range(60):
        a = 2 * math.pi * k / 60
        rr = r * (0.86 + 0.12 * math.sin(7 * a))
        pts.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{color}" stroke="{INK}" stroke-width="3"/>'


def flower(cx, cy, color, r=22):
    s = ''
    for k in range(5):
        a = 2 * math.pi * k / 5 - math.pi / 2
        s += (f'<ellipse cx="{cx + r * math.cos(a):.1f}" cy="{cy + r * math.sin(a):.1f}" rx="{r * 0.75:.0f}" ry="{r * 0.55:.0f}" '
              f'transform="rotate({math.degrees(a):.0f} {cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f})" fill="{color}" stroke="{INK}" stroke-width="2.5"/>')
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r * 0.4:.0f}" fill="#F6D27A" stroke="{INK}" stroke-width="2"/>'


def pod(cx, cy, color, constricted=False, w=130, h=40):
    if not constricted:
        return f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="{h / 2}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
    s = ''
    for k in range(4):
        x = cx - w / 2 + w / 8 + k * w / 4
        s += f'<ellipse cx="{x:.0f}" cy="{cy}" rx="{w / 8 + 4:.0f}" ry="{h / 2 - 4:.0f}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
    return s


def plant(x, ybase, height, flowers='top', fcolor=WHT):
    s = f'<line x1="{x}" y1="{ybase}" x2="{x}" y2="{ybase - height}" stroke="{GREEN}" stroke-width="6"/>'
    for k in range(1, 4):
        y = ybase - height * k / 4
        side = 1 if k % 2 else -1
        s += f'<ellipse cx="{x + side * 22}" cy="{y + 6}" rx="20" ry="9" fill="{GRN}" stroke="{GREEN}" stroke-width="2"/>'
        if flowers == 'axil':
            s += flower(x - side * 26, y - 4, fcolor, 11)
    if flowers == 'top':
        s += flower(x, ybase - height - 14, fcolor, 13)
    return s


def chip(x, y, g, w=118, h=58, fill='#fff'):
    """Генотип в рамке; A/a — латиница, доминантные заглавные — тёмно-синие, рецессивные — оранжевые."""
    letters = ''.join(f'<tspan style="fill:{DOM if c.isupper() else REC}">{c}</tspan>' for c in g)
    return (f'<rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{x:.0f}" y="{y + 11:.0f}" class="t" text-anchor="middle">{letters}</text>')


# 1. Семь пар признаков гороха ----------------------------------------------------------------------
def pea_traits():
    s = text(900, 54, 'Семь пар альтернативных признаков гороха в опытах Менделя', 'h', 'middle')
    s += panel(30, 90, 1740, 1000)
    s += text(620, 140, 'Доминантный', 't', 'middle', DOM) + text(1200, 140, 'Рецессивный', 't', 'middle', REC)
    rows = [
        ('Окраска семян', seed(620, 0, YEL), 'жёлтая', seed(1200, 0, GRN), 'зелёная'),
        ('Форма семян', seed(620, 0, YEL), 'гладкая', seed(1200, 0, YEL, True), 'морщинистая'),
        ('Окраска венчика', flower(620, 0, PUR), 'пурпурная', flower(1200, 0, WHT), 'белая'),
        ('Рост (стебель)', None, 'нормальный (высокий)', None, 'карликовый'),
        ('Окраска незрелого боба', pod(620, 0, GRN), 'зелёная', pod(1200, 0, YEL), 'жёлтая'),
        ('Форма боба', pod(620, 0, GRN), 'вздутый', pod(1200, 0, GRN, True), 'с перетяжками'),
        ('Расположение цветков', None, 'пазушные (вдоль стебля)', None, 'верхушечные'),
    ]
    for k, (name, d_ico, d_txt, r_ico, r_txt) in enumerate(rows):
        y = 220 + k * 120
        if k % 2 == 0:
            s += f'<rect x="60" y="{y - 56}" width="1680" height="112" rx="12" fill="#fff" opacity="0.7"/>'
        s += text(90, y + 10, f'{k + 1}. {name}', 't')
        for cx, ico, txt in ((620, d_ico, d_txt), (1200, r_ico, r_txt)):
            if ico is not None:
                s += f'<g transform="translate(0 {y})">{ico}</g>'
            elif name.startswith('Рост'):
                hgt = 90 if cx == 620 else 40
                s += plant(cx, y + 48, hgt, 'none')
            else:
                s += plant(cx, y + 50, 86, 'axil' if cx == 620 else 'top', WHT)
            s += text(cx + 95, y + 10, txt, 's')
    s += text(900, 1060, 'Горох самоопыляется → чистые линии · у гороха 2n = 14 (7 пар хромосом)', 'cap', 'middle')
    return s


# 2. Опыт Менделя: P → F₁ → F₂ ------------------------------------------------------------------------
def mendel_generations():
    s = text(900, 54, 'Моногибридное скрещивание: P → F₁ → F₂', 'h', 'middle')
    s += panel(30, 90, 1180, 880)
    # P
    s += text(80, 190, 'P', 'f') + seed(330, 170, YEL) + chip(330, 250, 'AA') + text(470, 185, '×', 'f', 'middle')
    s += seed(610, 170, GRN) + chip(610, 250, 'aa')
    s += text(330, 125, 'жёлтые', 'cap', 'middle') + text(610, 125, 'зелёные', 'cap', 'middle') + text(830, 185, 'чистые линии', 'cap')
    s += text(80, 345, 'G', 'f') + chip(330, 330, 'A', 80) + chip(610, 330, 'a', 80)
    s += arrow(470, 375, 470, 430)
    # F1
    s += text(80, 495, 'F₁', 'f')
    for k in range(4):
        s += seed(300 + k * 110, 475, YEL, r=30)
    s += chip(520, 550, 'Aa') + text(760, 475, 'все жёлтые Aa:', 't') + text(760, 515, 'единообразие (1-й закон)', 'cap')
    s += text(470, 625, 'самоопыление F₁: Aa × Aa', 's', 'middle') + arrow(470, 640, 470, 690)
    # F2
    s += text(80, 775, 'F₂', 'f')
    for k, (g, c) in enumerate((('AA', YEL), ('Aa', YEL), ('Aa', YEL), ('aa', GRN))):
        x = 290 + k * 150
        s += seed(x, 750, c, r=32) + chip(x, 830, g, 100)
    s += text(1170, 760, '3 жёлтых : 1 зелёный', 't', 'end') + text(1170, 800, 'по фенотипу', 'cap', 'end')
    s += text(1170, 850, '1 AA : 2 Aa : 1 aa', 't', 'end') + text(1170, 890, 'по генотипу (2-й закон)', 'cap', 'end')
    # наблюдение
    s += panel(1240, 90, 530, 880, 'Наблюдение Менделя', 'опыт по форме семян')
    s += seed(1400, 290, YEL) + text(1450, 300, '5474 гладких', 't')
    s += seed(1400, 390, YEL, True) + text(1450, 400, '1850 морщинистых', 't')
    s += text(1505, 490, 'всего 7324', 't', 'middle') + text(1505, 540, '≈ 2,96 : 1', 'f', 'middle')
    s += text(1505, 625, 'близко к 3 : 1, но не точно:', 's', 'middle')
    s += text(1505, 665, 'выборка конечна', 's', 'middle')
    s += text(1505, 790, '3 : 1 — теория', 'cap', 'middle') + text(1505, 825, 'для каждого потомка', 'cap', 'middle')
    s += text(1505, 860, 'вероятность aa = 1/4', 'cap', 'middle')
    return s


# 3. Чистота гамет ----------------------------------------------------------------------------------------
def chrom(x, y, allele, h=150, double=False):
    col = DOM if allele.isupper() else REC
    s = ''
    xs = (x - 9, x + 9) if double else (x,)
    for xx in xs:
        s += f'<rect x="{xx - 8}" y="{y - h / 2}" width="16" height="{h}" rx="8" fill="#C9C3B6" stroke="{INK}" stroke-width="2"/>'
        s += f'<rect x="{xx - 8}" y="{y - 12}" width="16" height="24" fill="{col}"/>'
    return s + text(x + (32 if double else 22), y + 10, allele, 't', 'start', col)


def gamete_purity():
    s = text(900, 54, 'Гипотеза чистоты гамет: в гамете одна аллель каждого гена', 'h', 'middle')
    s += panel(30, 90, 1740, 760)
    # клетка Aa
    s += f'<circle cx="250" cy="430" r="170" fill="#EAF4EC" stroke="{GREEN}" stroke-width="5"/>'
    s += chrom(205, 430, 'A', double=True) + chrom(295, 430, 'a', double=True)
    s += text(250, 650, 'клетка Aa (2n)', 't', 'middle') + text(250, 690, 'гомологи — A и a', 'cap', 'middle')
    s += text(250, 725, 'в одном участке (локусе)', 'cap', 'middle')
    s += arrow(440, 430, 600, 430) + text(520, 405, 'мейоз', 's', 'middle')
    # гаметы
    for k, al in enumerate('AAaa'):
        y = 210 + k * 150
        s += f'<circle cx="720" cy="{y}" r="62" fill="#FFF7E0" stroke="{INK}" stroke-width="3"/>' + chrom(720, y, al, 80)
    s += text(720, 815, 'гаметы (n): A или a', 't', 'middle')
    s += text(900, 220, 'в каждой гамете —', 's') + text(900, 260, 'одна аллель гена', 's')
    s += text(900, 300, '(гамета «чиста»)', 'cap')
    s += arrow(1110, 430, 1260, 430) + text(1185, 405, 'оплодотворение', 's', 'middle')
    s += f'<circle cx="1480" cy="430" r="150" fill="#EAF4EC" stroke="{GREEN}" stroke-width="5"/>'
    s += chrom(1440, 430, 'A') + chrom(1520, 430, 'a')
    s += text(1480, 630, 'зигота Aa (2n)', 't', 'middle') + text(1480, 670, 'пара аллелей восстановлена:', 'cap', 'middle')
    s += text(1480, 705, 'одна от матери, одна от отца', 'cap', 'middle')
    return s


# 4. Моногибридная решётка ------------------------------------------------------------------------------
def grid(x0, y0, gam_r, gam_c, cell, color_of, w=180, h=120):
    s = ''
    for j, g in enumerate(gam_c):
        s += chip(x0 + w * (j + 1) + w / 2, y0 + h / 2, g, 90, 54, '#FFF7E0')
    for i, g in enumerate(gam_r):
        s += chip(x0 + w / 2, y0 + h * (i + 1) + h / 2, g, 90, 54, '#FFF7E0')
        for j, g2 in enumerate(gam_c):
            geno = cell(g, g2)
            x, y = x0 + w * (j + 1), y0 + h * (i + 1)
            s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color_of(geno)}" stroke="{INK}" stroke-width="2.5"/>'
            letters = ''.join(f'<tspan style="fill:{DOM if c.isupper() else REC}">{c}</tspan>' for c in geno)
            s += f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + 11:.0f}" class="t" text-anchor="middle">{letters}</text>'
    return s


def mono_cell(a, b):
    return ''.join(sorted(a + b, key=lambda c: (c.lower(), c.islower())))


def monohybrid_punnett():
    s = text(650, 54, 'Решётка Пеннета: Aa × Aa', 'h', 'middle')
    s += panel(30, 90, 1240, 900)
    s += text(570, 160, '♂ гаметы', 's', 'middle') + text(130, 470, '♀', 's', 'middle') + text(130, 505, 'гаметы', 'cap', 'middle')
    s += grid(170, 170, 'Aa', 'Aa', mono_cell, lambda g: '#FBEFB8' if 'A' in g else '#D6EBCB', 200, 150)
    s += text(1030, 300, 'Генотипы:', 't', 'middle') + text(1030, 350, '1 AA : 2 Aa : 1 aa', 't', 'middle')
    s += text(1030, 470, 'Фенотипы:', 't', 'middle') + text(1030, 520, '3 доминантных', 't', 'middle', DOM)
    s += text(1030, 560, ': 1 рецессивный', 't', 'middle', REC)
    s += text(1030, 640, 'при полном доминировании', 'cap', 'middle')
    s += text(650, 860, 'Каждая клетка — одно равновероятное сочетание гамет (1/4)', 's', 'middle')
    s += text(650, 905, 'P(aa) = 1/4 · P(A_) = 3/4 · P(Aa) = 1/2', 'cap', 'middle')
    return s


# 5. Дигибридная решётка ---------------------------------------------------------------------------------
def di_cell(a, b):
    g = a + b
    A = ''.join(sorted([c for c in g if c in 'Aa'], key=lambda c: c.islower()))
    B = ''.join(sorted([c for c in g if c in 'Bb'], key=lambda c: c.islower()))
    return A + B


def di_color(g):
    a, b = 'A' in g, 'B' in g
    return {(True, True): '#FBEFB8', (True, False): '#F6C99A', (False, True): '#D6EBCB', (False, False): '#B9C8E6'}[(a, b)]


def dihybrid_punnett():
    s = text(900, 54, 'Дигибридное скрещивание: AaBb × AaBb', 'h', 'middle')
    s += panel(30, 90, 1740, 1130)
    gam = ['AB', 'Ab', 'aB', 'ab']
    s += text(660, 145, '♂ гаметы: AB, Ab, aB, ab — по 1/4', 's', 'middle') + text(185, 300, '♀ гаметы', 'cap', 'middle')
    s += grid(90, 165, gam, gam, di_cell, di_color, 190, 160)
    lx = 1170
    s += text(lx, 230, 'A — жёлтые, a — зелёные', 's') + text(lx, 270, 'B — гладкие, b — морщинистые', 's')
    s += text(lx, 305, 'гены в разных парах хромосом', 'cap')
    for k, (col, name, n) in enumerate((('#FBEFB8', 'A_B_ жёлтые гладкие', 9), ('#F6C99A', 'A_bb жёлтые морщинистые', 3),
                                         ('#D6EBCB', 'aaB_ зелёные гладкие', 3), ('#B9C8E6', 'aabb зелёные морщинистые', 1))):
        y = 400 + k * 90
        s += f'<rect x="{lx}" y="{y - 34}" width="56" height="48" rx="8" fill="{col}" stroke="{INK}" stroke-width="2"/>'
        s += text(lx + 76, y, f'{n} — {name}', 't')
    s += text(lx, 800, 'Фенотипы 9 : 3 : 3 : 1', 'f')
    s += text(lx, 870, '16 сочетаний гамет →', 's') + text(lx, 910, '9 генотипов, 4 фенотипа', 's')
    s += text(lx, 980, '(3-й закон — независимое', 'cap') + text(lx, 1015, 'наследование)', 'cap')
    s += text(lx, 1090, 'Мендель: 315 : 101 : 108 : 32', 'cap') + text(lx, 1125, '(всего 556 семян)', 'cap')
    return s


# 6. Неполное доминирование -----------------------------------------------------------------------------
def incomplete_dominance():
    s = text(900, 54, 'Неполное доминирование: ночная красавица', 'h', 'middle')
    s += panel(30, 90, 1740, 860)
    s += text(80, 210, 'P', 'f') + flower(360, 190, REDF, 34) + chip(360, 285, 'AA') + text(520, 205, '×', 'f', 'middle')
    s += flower(680, 190, WHT, 34) + chip(680, 285, 'aa')
    s += text(360, 128, 'красная', 's', 'middle') + text(680, 128, 'белая', 's', 'middle')
    s += arrow(520, 320, 520, 380)
    s += text(80, 460, 'F₁', 'f')
    for k in range(4):
        s += flower(300 + k * 120, 440, PINK, 28)
    s += chip(480, 525, 'Aa') + text(900, 445, 'все розовые — промежуточный признак;', 't') + text(900, 490, 'F₁ единообразно', 'cap')
    s += text(520, 600, 'Aa × Aa', 's', 'middle') + arrow(520, 615, 520, 665)
    s += text(80, 760, 'F₂', 'f')
    for k, (g, c, n) in enumerate((('AA', REDF, 'красная'), ('Aa', PINK, 'розовая'), ('Aa', PINK, 'розовая'), ('aa', WHT, 'белая'))):
        x = 290 + k * 170
        s += flower(x, 740, c, 30) + chip(x, 825, g, 100) + text(x, 890, n, 'cap', 'middle')
    s += text(1720, 740, '1 красная : 2 розовые : 1 белая', 't', 'end')
    s += text(1720, 790, 'фенотипы = генотипам: 1 : 2 : 1', 'cap', 'end')
    s += text(1720, 840, '(при полном доминировании было бы 3 : 1)', 'cap', 'end')
    return s


# 7. Анализирующее скрещивание ---------------------------------------------------------------------------
def testcross():
    s = text(900, 54, 'Анализирующее скрещивание: A_ × aa', 'h', 'middle')
    s += panel(30, 90, 1740, 900)
    s += text(900, 150, 'Исследуемая особь с доминантным признаком (AA или Aa?) × рецессивная гомозигота aa (тестер)', 's', 'middle')
    for k, (title, gam, kids, verdict) in enumerate((
            ('AA × aa', ('A',), ('Aa', 'Aa', 'Aa', 'Aa'), 'все потомки доминантные'),
            ('Aa × aa', ('A', 'a'), ('Aa', 'aa', 'Aa', 'aa'), '1 доминантный : 1 рецессивный'))):
        x0 = 70 + k * 860
        s += panel(x0, 190, 800, 620, title, None, '#fff')
        s += text(x0 + 60, 330, 'G:', 't')
        for j, g in enumerate(gam):
            s += chip(x0 + 200 + j * 120, 320, g, 80)
        s += text(x0 + 470, 330, '×', 't') + chip(x0 + 600, 320, 'a', 80)
        s += arrow(x0 + 400, 370, x0 + 400, 430)
        for j, g in enumerate(kids):
            x = x0 + 130 + j * 180
            s += seed(x, 500, YEL if 'A' in g else GRN, r=36) + chip(x, 585, g, 100)
        s += text(x0 + 400, 690, verdict, 't', 'middle')
        s += text(x0 + 400, 740, 'вывод: особь AA' if k == 0 else 'вывод: особь Aa', 'f' if False else 't', 'middle', DOM if k == 0 else REC)
    s += text(900, 870, 'Хотя бы один рецессивный потомок → исследуемая особь точно Aa.', 't', 'middle')
    s += text(900, 920, 'Если в малой выборке все потомки доминантные — это довод за AA, но не доказательство.', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'pea-traits.png': (pea_traits(), 1800, 1110),
        'mendel-generations.png': (mendel_generations(), 1800, 1000),
        'gamete-purity.png': (gamete_purity(), 1800, 880),
        'monohybrid-punnett.png': (monohybrid_punnett(), 1300, 1010),
        'dihybrid-punnett.png': (dihybrid_punnett(), 1800, 1240),
        'incomplete-dominance.png': (incomplete_dominance(), 1800, 970),
        'testcross.png': (testcross(), 1800, 1010),
    }
    only = set(__import__('sys').argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
