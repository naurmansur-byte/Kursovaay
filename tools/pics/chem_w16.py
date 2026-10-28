"""Рисунки недели 16 химии (course/week-16/pics/*.png): свойства галогенов, вытеснение галогенов, получение хлора,
осадки на анионы, озонатор и озоновый слой, формы серы и флотация, степени окисления серы, серная кислота,
контактный способ.

Факты — по выжимке course/textbooks/chem-16-o-s-halogens.md (Х8 § 29; Х9-1 § 12; Х9-2 § 28–34; Х10-2 § 54–55;
Х11-2 § 47–51). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w16.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    return _text(x, y, chem(s), cls, anchor, fill)

OUT = ROOT / 'course' / 'week-16' / 'pics'
BLUE, ORANGE, BROWN, PURPLE = '#3A57A7', '#D98A2B', '#8A5A2B', '#8E44AD'
WATER, SULFUR, F2, CL2, BR2 = '#E3EEF7', '#F2CF3A', '#F4EFA6', '#CAD65C', '#8B3A1A'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER, stroke=None):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"{st}/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s'):
    rows = label.split('\n')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32))


def tube(cx, top, fill, sediment=None, h=260, sed_h=70):
    s = f'<path d="M{cx - 34} {top} V {top + h - 34} A 34 34 0 0 0 {cx + 34} {top + h - 34} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if sediment:
        s += (f'<path d="M{cx - 34} {top + h - sed_h} V {top + h - 34} A 34 34 0 0 0 {cx + 34} {top + h - 34} V {top + h - sed_h} Z" '
              f'fill="{sediment}" stroke="{INK}" stroke-width="2"/>')
        for k in range(9):
            s += f'<circle cx="{cx - 22 + (k * 11) % 44}" cy="{top + h - sed_h + 12 + (k * 17) % (sed_h - 30)}" r="4" fill="#fff" opacity=".55"/>'
    return s


def flask(cx, bottom, r=95, neck=50, fill='#fff', level=None, liquid=None):
    """Круглодонная колба: шар радиуса r с центром над bottom, горло вверх."""
    cy = bottom - r
    s = ''
    if liquid and level:
        s += (f'<clipPath id="fl{cx}{bottom}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
              f'<rect x="{cx - r}" y="{bottom - level}" width="{2 * r}" height="{level}" fill="{liquid}" clip-path="url(#fl{cx}{bottom})"/>')
    s = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="3"/>' + s
         + f'<rect x="{cx - 22}" y="{cy - r - neck + 6}" width="44" height="{neck}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
         + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="3"/>')
    return s


def flame(cx, top):
    return (f'<path d="M{cx} {top} C {cx + 30} {top + 30} {cx + 26} {top + 70} {cx} {top + 78} C {cx - 26} {top + 70} {cx - 30} {top + 30} {cx} {top} Z" '
            f'fill="{ORANGE}" stroke="{RED}" stroke-width="3"/>'
            f'<rect x="{cx - 34}" y="{top + 78}" width="68" height="34" rx="6" fill="#BDB8AE" stroke="{INK}" stroke-width="3"/>')


def bubbles(cx, top, bottom, n=7, spread=24, r=7):
    return ''.join(f'<circle cx="{cx - spread + (k * 37) % (2 * spread)}" cy="{bottom - (k + 0.5) * (bottom - top) / n:.0f}" r="{r}" '
                   f'fill="#fff" stroke="{INK}" stroke-width="2"/>' for k in range(n))


def atom(x, y, r=16, fill=INK, label=None, fs=None, color='#fff'):
    s = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
    if label:
        s += f'<text x="{x:.0f}" y="{y + r * 0.38:.0f}" text-anchor="middle" style="font: 800 {fs or r}px Manrope; fill:{color}">{label}</text>'
    return s


# 1. Галогены: состояние, цвет и изменение свойств ---------------------------------------------------
def halogen_properties():
    s = text(900, 52, 'Галогены: от фтора к йоду', 'h', 'middle')
    items = [('F₂', 'фтор', 'бледно-жёлтый газ', 'gas', F2),
             ('Cl₂', 'хлор', 'жёлто-зелёный газ', 'gas', CL2),
             ('Br₂', 'бром', 'бурая жидкость', 'liquid', BR2),
             ('I₂', 'йод', 'серо-чёрные кристаллы,\nфиолетовый пар', 'solid', '#3B3833')]
    for k, (f, name, state, kind, color) in enumerate(items):
        x = 30 + k * 440
        s += card(x, 90, 410, 560)
        cx = x + 205
        if kind == 'gas':
            s += flask(cx, 430, 105, 55, color)
        elif kind == 'liquid':
            s += flask(cx, 430, 105, 55, '#E9C9B8', 80, color)
        else:
            s += flask(cx, 430, 105, 55, '#E6D3EE')
            for j in range(7):
                px, py = cx - 48 + j * 16, 412 - (j % 3) * 8
                s += f'<polygon points="{px},{py} {px + 14},{py - 9} {px + 22},{py + 4} {px + 8},{py + 12}" fill="#3B3833" stroke="{INK}" stroke-width="1.5"/>'
        s += text(cx, 500, f, 'f', 'middle')
        s += text(cx, 548, name, 't', 'middle')
        s += lines_at(cx, 592, state.split('\n'), 's', step=32)
    s += text(900, 700, 'У всех на внешнем уровне 7 электронов (ns²np⁵) — до завершения не хватает одного', 't', 'middle')
    rows = [('радиус атома, плотность, температуры плавления и кипения', 'растут', GREEN),
            ('окислительная способность и электроотрицательность', 'уменьшаются', RED)]
    for j, (what, how, color) in enumerate(rows):
        y = 790 + j * 80
        s += arrow(60, y, 1740, y, color, 6)
        s += text(900, y - 16, f'F → I: {what} — {how}', 's', 'middle', color)
    return s


# 2. Вытеснение галогенов из растворов солей ---------------------------------------------------------
def halogen_displacement():
    s = text(900, 52, 'Более активный галоген вытесняет менее активный', 'h', 'middle')
    s += card(30, 90, 1740, 720)
    tubes = [('Cl₂ + 2KBr', '2KCl + Br₂', '#E8A35A', True),
             ('Cl₂ + 2KI', '2KCl + I₂', '#9A5B2E', True),
             ('Br₂ + 2KI', '2KBr + I₂', '#9A5B2E', True),
             ('I₂ + KBr', 'реакции нет', '#E6D3EE', False)]
    for k, (left, right, color, ok) in enumerate(tubes):
        cx = 190 + k * 370
        s += text(cx, 150, left, 't', 'middle')
        s += tube(cx, 180, color, h=250)
        s += text(cx, 490, ('→ ' if ok else '') + right, 't', 'middle', INK if ok else RED)
        if not ok:
            s += (f'<line x1="{cx - 50}" y1="{230}" x2="{cx + 50}" y2="{370}" stroke="{RED}" stroke-width="8"/>'
                  f'<line x1="{cx + 50}" y1="{230}" x2="{cx - 50}" y2="{370}" stroke="{RED}" stroke-width="8"/>')
    s += f'<rect x="1500" y="130" width="250" height="400" rx="16" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    s += text(1625, 175, 'йод + крахмал', 's', 'middle')
    s += tube(1625, 200, '#2E3F9E', h=230)
    s += text(1625, 490, 'синее', 't', 'middle', BLUE)
    s += text(900, 610, 'Окислительная способность:  F₂ > Cl₂ > Br₂ > I₂', 't', 'middle')
    s += text(900, 670, 'Галоген вытесняет только те галогены, которые стоят правее в этом ряду', 's', 'middle')
    s += text(900, 760, 'Фтор в водном растворе реагирует с водой, поэтому в опытах вытеснения его не используют', 'cap', 'middle')
    return s


# 3. Получение хлора в лаборатории -------------------------------------------------------------------
def chlorine_lab():
    s = text(900, 52, 'Получение хлора в лаборатории', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    # капельная воронка с HCl над колбой
    s += flask(330, 560, 120, 70, '#fff', 70, '#E8E4DA')
    s += ''.join(f'<circle cx="{290 + k * 16}" cy="{548 - (k % 2) * 8}" r="7" fill="#3B3833"/>' for k in range(6))
    s += f'<path d="M290 230 H370 L345 290 V330 H315 V290 Z" fill="{WATER}" stroke="{INK}" stroke-width="3"/>'
    s += f'<line x1="330" y1="330" x2="330" y2="410" stroke="{INK}" stroke-width="4"/>'
    s += f'<line x1="300" y1="250" x2="360" y2="250" stroke="{INK}" stroke-width="2"/>'
    s += text(400, 260, 'HCl (конц.)', 's')
    s += text(195, 520, 'MnO₂', 's', 'end')
    s += flame(330, 580)
    s += text(330, 735, 'нагревание', 's', 'middle')
    # газоотвод в цилиндр (хлор тяжелее воздуха — сосуд горлом вверх)
    s += f'<rect x="540" y="430" width="120" height="250" rx="8" fill="{CL2}" opacity=".85" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M352 360 H600 V650" fill="none" stroke="{INK}" stroke-width="10"/>'
    s += f'<path d="M352 360 H600 V650" fill="none" stroke="#fff" stroke-width="4"/>'
    s += text(570, 560, 'Cl₂', 't', 'middle')
    s += text(600, 720, 'хлор тяжелее воздуха —', 's', 'middle')
    s += text(600, 752, 'сосуд горлом вверх', 's', 'middle')
    # уравнение и баланс
    s += f'<rect x="820" y="170" width="910" height="560" rx="16" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    s += text(1275, 240, 'MnO₂ + 4HCl → MnCl₂ + Cl₂↑ + 2H₂O', 't', 'middle')
    s += text(1275, 330, 'Mn⁺⁴ + 2e⁻ → Mn⁺²   окислитель MnO₂', 's', 'middle', RED)
    s += text(1275, 380, '2Cl⁻ − 2e⁻ → Cl₂⁰   восстановитель HCl', 's', 'middle', BLUE)
    s += text(1275, 470, 'MnO₂ : Cl₂ = 1 : 1', 't', 'middle')
    s += text(1275, 560, 'Хлор — жёлто-зелёный ядовитый газ', 's', 'middle')
    s += text(1275, 600, 'с удушливым запахом', 's', 'middle')
    s += text(1275, 680, 'Опыт показывает преподаватель; дома не повторять', 'cap', 'middle')
    return s


# 4. Осадки: галогениды серебра и сульфат бария ------------------------------------------------------
def anion_precipitates():
    s = text(900, 52, 'Качественные реакции: цвет осадка', 'h', 'middle')
    s += card(30, 90, 1740, 720)
    items = [('Ag⁺ + Cl⁻', 'AgCl', 'белый', '#F7F7F5'),
             ('Ag⁺ + Br⁻', 'AgBr', 'желтоватый', '#F2E7B0'),
             ('Ag⁺ + I⁻', 'AgI', 'жёлтый', '#EDCB3C'),
             ('Ba²⁺ + SO₄²⁻', 'BaSO₄', 'белый', '#F7F7F5')]
    for k, (ions, f, color_name, color) in enumerate(items):
        cx = 260 + k * 430
        s += text(cx, 160, 'реактив: ' + ('AgNO₃' if k < 3 else 'BaCl₂'), 's', 'middle', GREY)
        s += text(cx, 210, ions, 't', 'middle')
        s += tube(cx, 240, '#F1F5F8', color, h=300, sed_h=110)
        s += text(cx, 600, f + '↓', 'f', 'middle')
        s += text(cx, 650, color_name, 't', 'middle')
    s += text(900, 740, 'Цвет оценивают вместе со средой и составом раствора: Ag₃PO₄ тоже жёлтый', 's', 'middle')
    return s


# 5. Озонатор и озоновый слой -----------------------------------------------------------------------
def ozone_layer():
    s = text(900, 52, 'Озон: получение и озоновый слой', 'h', 'middle')
    s += card(30, 90, 840, 800) + card(900, 90, 870, 800)
    # озонатор: две пластины и разряд
    s += text(450, 150, 'Озонатор: электрический разряд', 't', 'middle')
    s += f'<rect x="170" y="230" width="560" height="26" fill="{GREY}"/><rect x="170" y="420" width="560" height="26" fill="{GREY}"/>'
    for k in range(6):
        x = 220 + k * 92
        s += f'<polyline points="{x},258 {x + 18},300 {x - 6},335 {x + 16},375 {x},418" fill="none" stroke="{BLUE}" stroke-width="4"/>'
    s += arrow(70, 338, 165, 338, INK, 5) + arrow(735, 338, 830, 338, INK, 5)
    # молекулы
    s += atom(150, 540, 26, RED, 'O', 24) + atom(196, 540, 26, RED, 'O', 24)
    s += text(173, 610, 'O₂', 't', 'middle')
    s += atom(640, 560, 26, RED, 'O', 24) + atom(686, 520, 26, RED, 'O', 24) + atom(732, 560, 26, RED, 'O', 24)
    s += text(686, 620, 'O₃', 't', 'middle')
    s += text(420, 560, '3O₂ → 2O₃', 'f', 'middle')
    s += lines_at(450, 700, ['O₂ и O₃ — аллотропные формы кислорода', 'O₃ — голубой газ, в 1,5 раза тяжелее O₂ (48 и 32)',
                             'обеззараживает воду и воздух'], 's', step=40)
    # Земля и слой
    s += text(1335, 150, 'Озоновый слой', 't', 'middle')
    s += f'<path d="M920 880 Q1335 640 1750 880 Z" fill="#9CC9A8" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M920 520 Q1335 300 1750 520" fill="none" stroke="{BLUE}" stroke-width="34" opacity=".35"/>'
    s += f'<circle cx="1680" cy="190" r="42" fill="{SULFUR}" stroke="{ORANGE}" stroke-width="4"/>'
    for x in (1170, 1335, 1500):
        t = (x - 920) / 830
        by = 520 - 440 * t * (1 - t)
        s += arrow(x + 120, 190, x, by - 24, PURPLE, 4)
        s += (f'<line x1="{x - 15}" y1="{by - 15:.0f}" x2="{x + 15}" y2="{by + 15:.0f}" stroke="{RED}" stroke-width="5"/>'
              f'<line x1="{x + 15}" y1="{by - 15:.0f}" x2="{x - 15}" y2="{by + 15:.0f}" stroke="{RED}" stroke-width="5"/>')
    s += text(1060, 210, 'УФ-излучение', 's', 'middle', PURPLE)
    s += text(1335, 570, 'на высоте около 25 км слой задерживает ультрафиолет', 's', 'middle')
    s += lines_at(1335, 630, ['«2–3 мм» — такой толщины был бы слой,', 'если собрать весь озон при обычных условиях',
                              'Разрушают фреоны и оксиды азота;', 'озоновая дыра — 1985, над Антарктидой'], 'cap', step=36)
    return s


# 6. Сера: S₈, пластическая сера, флотация -----------------------------------------------------------
def sulfur_forms():
    s = text(900, 52, 'Сера: кристаллическая, пластическая, флотация', 'h', 'middle')
    for x in (30, 620, 1210):
        s += card(x, 90, 560, 760)
    # S8 — кольцо «короной»
    cx, cy = 310, 360
    pts = [(cx + (138 if k % 2 else 118) * math.cos(2 * math.pi * k / 8), cy + (138 if k % 2 else 118) * math.sin(2 * math.pi * k / 8))
           for k in range(8)]
    for k in range(8):
        x1, y1 = pts[k]
        x2, y2 = pts[(k + 1) % 8]
        s += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{INK}" stroke-width="6"/>'
    for x, y in pts:
        s += atom(x, y, 26, SULFUR, 'S', 24, INK)
    s += text(310, 160, 'кольцо S₈', 't', 'middle')
    s += lines_at(310, 560, ['обычная кристаллическая сера:', 'циклические молекулы S₈,', 'жёлтые кристаллы,', 't пл. 112,8 °C'], 's', step=40)
    # пластическая сера — цепи
    s += text(900, 160, 'пластическая сера', 't', 'middle')
    for j in range(3):
        y0 = 260 + j * 90
        ps = [(680 + k * 55, y0 + (22 if k % 2 else -22)) for k in range(9)]
        s += f'<polyline points="{" ".join(f"{x},{y}" for x, y in ps)}" fill="none" stroke="{INK}" stroke-width="5"/>'
        s += ''.join(atom(x, y, 14, '#C9A227') for x, y in ps)
    s += lines_at(900, 560, ['длинные цепи атомов S;', 'получается, если расплав', 'серы вылить в холодную воду'], 's', step=40)
    # флотация
    s += text(1490, 160, 'флотация руды', 't', 'middle')
    s += f'<rect x="1300" y="200" width="380" height="330" rx="10" fill="{WATER}" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="1300" y="200" width="380" height="50" fill="#F4F1E6" stroke="{INK}" stroke-width="2"/>'
    for k in range(9):
        bx, by = 1340 + (k * 47) % 300, 290 + (k * 61) % 200
        s += f'<circle cx="{bx}" cy="{by}" r="16" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += f'<rect x="{bx + 8}" y="{by - 22}" width="13" height="13" fill="{SULFUR}" stroke="{INK}" stroke-width="1.5"/>'
    s += ''.join(f'<polygon points="{1330 + k * 40},528 {1342 + k * 40},506 {1356 + k * 40},528" fill="{GREY}"/>' for k in range(8))
    s += lines_at(1490, 600, ['частицы минерала не смачиваются', 'водой и всплывают с пузырьками;', 'пустая порода оседает'], 's', step=40)
    s += lines_at(1490, 740, ['порошок серы плавает из-за', 'несмачиваемости, а не потому,', 'что сера легче воды'], 'cap', step=32)
    return s


# 7. Степени окисления серы и свойства ---------------------------------------------------------------
def sulfur_redox():
    s = text(900, 52, 'Степень окисления серы → свойства в ОВР', 'h', 'middle')
    s += card(30, 90, 1740, 700)
    xs = {-2: 260, 0: 640, 4: 1060, 6: 1480}
    s += arrow(120, 330, 1700, 330, INK, 5)
    for v, x in xs.items():
        s += f'<line x1="{x}" y1="310" x2="{x}" y2="350" stroke="{INK}" stroke-width="5"/>'
        s += text(x, 395, f'{v:+d}' if v else '0', 'f', 'middle')
    names = {-2: 'H₂S, сульфиды', 0: 'S', 4: 'SO₂, H₂SO₃, сульфиты', 6: 'SO₃, H₂SO₄, сульфаты'}
    for v, n in names.items():
        s += text(xs[v], 460, n, 't', 'middle')
    roles = {-2: ('только восстановитель', BLUE), 0: ('и окислитель, и восстановитель', INK),
             4: ('и окислитель, и восстановитель', INK), 6: ('только окислитель', RED)}
    for v, (r, c) in roles.items():
        s += lines_at(xs[v], 530, r.replace(', и ', ' и\n').split('\n'), 's', step=34, color=c)
    # стрелки возможных переходов
    s += arrow(260, 270, 380, 200, BLUE, 5) + text(330, 180, 'отдаёт e⁻', 's', 'middle', BLUE)
    s += arrow(1060, 270, 960, 200, RED, 5) + arrow(1060, 270, 1160, 200, BLUE, 5)
    s += text(1060, 180, 'обе роли', 's', 'middle')
    s += arrow(1480, 270, 1360, 200, RED, 5) + text(1420, 180, 'принимает e⁻', 's', 'middle', RED)
    s += text(900, 620, 'SO₂ — восстановитель: 2SO₂ + O₂ ⇄ 2SO₃;   окислитель: SO₂ + 2H₂S → 3S + 2H₂O', 's', 'middle')
    s += text(900, 690, 'В пирите FeS₂ у серы степень окисления −1 — это не обычный сульфид S⁻²', 'cap', 'middle')
    return s


# 8. Серная кислота: металлы, пассивация, разбавление ------------------------------------------------
def sulfuric_acid():
    s = text(900, 52, 'Серная кислота: разбавленная и концентрированная', 'h', 'middle')
    for x in (30, 620, 1210):
        s += card(x, 90, 560, 780)
    # 1: Zn с разбавленной и Cu с концентрированной
    s += text(310, 150, 'металл + кислота', 't', 'middle')
    s += tube(190, 190, WATER, h=260) + f'<rect x="170" y="390" width="40" height="40" fill="{GREY}" stroke="{INK}" stroke-width="2"/>'
    s += bubbles(190, 220, 380, 6, 16, 6)
    s += text(190, 500, 'Zn + разб.', 's', 'middle') + text(190, 535, '→ H₂↑', 't', 'middle')
    s += tube(430, 190, '#F2EEE2', h=260) + f'<rect x="410" y="390" width="40" height="40" fill="{BROWN}" stroke="{INK}" stroke-width="2"/>'
    s += bubbles(430, 220, 380, 6, 16, 6)
    s += flame(430, 470)
    s += text(430, 625, 'Cu + конц., t', 's', 'middle') + text(430, 660, '→ SO₂↑', 't', 'middle', RED)
    s += lines_at(310, 740, ['Cu + 2H₂SO₄ → CuSO₄ + SO₂ + 2H₂O', 'водород с Cu не выделяется'], 's', step=40)
    # 2: пассивация
    s += text(900, 150, 'пассивация', 't', 'middle')
    s += tube(900, 190, '#F2EEE2', h=300)
    s += f'<rect x="878" y="300" width="44" height="160" fill="{GREY}" stroke="{BLUE}" stroke-width="6"/>'
    s += text(900, 545, 'Fe или Al', 's', 'middle')
    s += lines_at(900, 620, ['холодная концентрированная', 'H₂SO₄: на поверхности —', 'защитная плёнка,', 'реакция не идёт'], 's', step=40)
    # 3: разбавление
    s += text(1490, 150, 'разбавление', 't', 'middle')
    s += f'<path d="M1370 320 V520 Q1370 540 1390 540 H1590 Q1610 540 1610 520 V320" fill="none" stroke="{INK}" stroke-width="4"/>'
    s += f'<rect x="1374" y="400" width="232" height="136" fill="{WATER}"/>'
    s += text(1490, 480, 'вода', 's', 'middle')
    s += f'<g transform="rotate(35 1560 230)"><rect x="1525" y="180" width="70" height="110" rx="6" fill="#F2EEE2" stroke="{INK}" stroke-width="3"/></g>'
    s += f'<path d="M1520 290 Q1500 340 1494 400" fill="none" stroke="#C8BFA8" stroke-width="7"/>'
    s += text(1640, 220, 'H₂SO₄', 's')
    s += text(1490, 620, 'кислоту — в воду!', 't', 'middle', RED)
    s += lines_at(1490, 680, ['сильный разогрев;', 'конц. H₂SO₄ ≈ 1,84 г/см³'], 's', step=40)
    return s


# 9. Контактный способ получения серной кислоты ------------------------------------------------------
def contact_process():
    s = text(900, 52, 'Контактный способ получения серной кислоты', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    top = [(160, 'пирит FeS₂\nдробление,\nфлотация', '#F1EDE3'),
           (480, 'печь\nкипящего слоя\n~800 °C', '#F6D2BF'),
           (830, 'очистка газа:\nциклон,\nэлектрофильтр', '#ECECEC'),
           (1180, 'сушильная\nбашня\n(конц. H₂SO₄)', '#ECECEC'),
           (1550, 'контактный\nаппарат V₂O₅\n400–500 °C', '#F7EFC8')]
    for x, lbl, fill in top:
        s += box(x, 250, 250, 170, lbl, fill)
    for (x1, *_), (x2, *_) in zip(top, top[1:]):
        s += arrow(x1 + 128, 250, x2 - 128, 250, INK, 5)
    s += text(480, 380, '4FeS₂ + 11O₂ → 2Fe₂O₃ + 8SO₂', 's', 'middle')
    s += arrow(480, 395, 480, 450, GREY, 4) + text(480, 485, 'огарок Fe₂O₃ → металлургия', 'cap', 'middle')
    s += text(1550, 380, '2SO₂ + O₂ ⇄ 2SO₃ + Q', 's', 'middle')
    s += text(1550, 420, 'теплообменник', 'cap', 'middle')
    s += arrow(1550, 440, 1550, 560, INK, 5)
    s += box(1550, 640, 300, 150, 'поглотительная\nбашня\n98 %-я H₂SO₄', '#E3EEF7')
    s += arrow(1395, 640, 1180, 640, INK, 5)
    s += box(1040, 640, 260, 130, 'олеум\nH₂SO₄·nSO₃', '#F3E3C9')
    s += lines_at(560, 590, ['SO₃ поглощают серной кислотой, а не водой:', 'с водой образуется сернокислотный туман'], 's', step=40)
    s += lines_at(560, 720, ['400–500 °C — компромисс скорости и выхода:', 'реакция экзотермическая и обратимая'], 's', step=40)
    s += text(900, 880, 'По сере: FeS₂ → 2SO₂ → 2SO₃ → 2H₂SO₄', 't', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'halogen-properties.png': (halogen_properties(), 1800, 920),
        'halogen-displacement.png': (halogen_displacement(), 1800, 840),
        'chlorine-lab.png': (chlorine_lab(), 1800, 880),
        'anion-precipitates.png': (anion_precipitates(), 1800, 840),
        'ozone-layer.png': (ozone_layer(), 1800, 920),
        'sulfur-forms.png': (sulfur_forms(), 1800, 880),
        'sulfur-redox.png': (sulfur_redox(), 1800, 820),
        'sulfuric-acid.png': (sulfuric_acid(), 1800, 900),
        'contact-process.png': (contact_process(), 1800, 980),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
