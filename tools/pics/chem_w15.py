"""Рисунки недели 15 химии (course/week-15/pics/*.png): аллотропия углерода, известковая вода и избыток CO₂, соотношение
щёлочь : CO₂, круговорот азота, NH₃ и NH₄⁺, синтез аммиака, производство HNO₃, разложение нитратов, аллотропия фосфора,
три ряда фосфатов, минеральные удобрения.

Факты — по выжимке course/textbooks/chem-15-c-si-n-p.md (Х8 § 51–53; Х9-2 § 36–45; Х11-1 § 37–41; Х11-2 § 42–46). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w15.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    return _text(x, y, chem(s), cls, anchor, fill)

OUT = ROOT / 'course' / 'week-15' / 'pics'
BLUE, ORANGE, BROWN, PURPLE = '#3A57A7', '#D98A2B', '#8A5A2B', '#8E44AD'
CARB, WATER, MILK = '#3B3833', '#E3EEF7', '#F4F4F2'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER, stroke=None):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"{st}/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s'):
    rows = label.split('\n')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32))


def tube(cx, top, fill, sediment=None, h=260, sed_h=70, cloudy=False):
    s = f'<path d="M{cx - 34} {top} V {top + h - 34} A 34 34 0 0 0 {cx + 34} {top + h - 34} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if cloudy:
        for k in range(26):
            x = cx - 24 + (k * 37) % 48
            y = top + 40 + (k * 53) % (h - 90)
            s += f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" stroke="#BDB8AE" stroke-width="1.5"/>'
    if sediment:
        s += (f'<path d="M{cx - 34} {top + h - sed_h} V {top + h - 34} A 34 34 0 0 0 {cx + 34} {top + h - 34} V {top + h - sed_h} Z" '
              f'fill="{sediment}" stroke="{INK}" stroke-width="2"/>')
    return s


def atom(x, y, r=16, fill=CARB, label=None, fs=None):
    s = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
    if label:
        s += f'<text x="{x:.0f}" y="{y + r * 0.38:.0f}" text-anchor="middle" style="font: 800 {fs or r}px Manrope; fill:#fff">{label}</text>'
    return s


def bond(x1, y1, x2, y2, w=5, color=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w}"{d}/>'


# 1. Аллотропия углерода ---------------------------------------------------------------------------
def carbon_allotropes():
    s = text(900, 52, 'Аллотропия углерода', 'h', 'middle')
    for x in (30, 620, 1210):
        s += card(x, 90, 560, 760)
    # алмаз: тетраэдрическая сеть (проекция)
    cx, cy = 310, 330
    pts = []
    for row in range(4):
        for col in range(4):
            x = cx - 165 + col * 110 + (55 if row % 2 else 0)
            y = cy - 150 + row * 95
            pts.append((x, y))
    for i, (x1, y1) in enumerate(pts):
        for j, (x2, y2) in enumerate(pts):
            if i < j and 60 < math.hypot(x2 - x1, y2 - y1) < 125:
                s += bond(x1, y1, x2, y2, 4, '#8F897F')
    for x, y in pts:
        s += atom(x, y, 15)
    s += text(310, 140, 'Алмаз', 't', 'middle')
    s += lines_at(310, 600, ['каждый C связан с 4 соседями', '(тетраэдр, sp³)', 'самый твёрдый природный минерал',
                             'не проводит ток, хорошо проводит тепло'], 's', step=34)
    s += text(310, 760, 'огранённый — бриллиант', 'cap', 'middle')
    # графит: слои
    gx, gy = 900, 190
    for layer in range(3):
        y0 = gy + layer * 120
        hexes = []
        for k in range(4):
            hx = gx - 150 + k * 100 + (50 if layer % 2 else 0)
            for a in range(6):
                ang = math.radians(60 * a + 30)
                ang2 = math.radians(60 * (a + 1) + 30)
                x1, y1 = hx + 32 * math.cos(ang), y0 + 18 * math.sin(ang)
                x2, y2 = hx + 32 * math.cos(ang2), y0 + 18 * math.sin(ang2)
                s += bond(x1, y1, x2, y2, 4, INK)
                hexes.append((x1, y1))
        for x, y in hexes:
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{CARB}"/>'
        if layer < 2:
            for k in range(4):
                hx = gx - 150 + k * 100 + (50 if layer % 2 else 0)
                s += bond(hx, y0 + 22, hx + (50 if layer % 2 == 0 else -50) * 0.5, y0 + 98, 2.5, GREY, '6 6')
    s += text(900, 140, 'Графит', 't', 'middle')
    s += lines_at(900, 600, ['слои из шестиугольников (sp²);', 'между слоями связь слабая', 'мягкий, жирный на ощупь',
                             'проводит электрический ток'], 's', step=34)
    s += text(900, 760, 'электроды, грифели карандашей', 'cap', 'middle')
    # фуллерен
    fx, fy, R = 1490, 340, 170
    s += f'<circle cx="{fx}" cy="{fy}" r="{R}" fill="#EFE9DD" stroke="{INK}" stroke-width="4"/>'

    def poly(cx_, cy_, r_, n, rot, fill):
        p = ' '.join(f'{cx_ + r_ * math.cos(math.radians(rot + 360 * k / n)):.0f},{cy_ + r_ * math.sin(math.radians(rot + 360 * k / n)):.0f}'
                     for k in range(n))
        return f'<polygon points="{p}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    s += poly(fx, fy, 46, 5, -90, '#3B3833')
    for k in range(5):
        a = math.radians(-90 + 36 + 72 * k)
        s += poly(fx + 102 * math.cos(a), fy + 102 * math.sin(a), 44, 6, math.degrees(a), '#fff')
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        s += poly(fx + 150 * math.cos(a), fy + 150 * math.sin(a), 22, 5, math.degrees(a) + 180, '#3B3833')
    s += text(1490, 140, 'Фуллерен C₆₀'.replace('₆₀', '<tspan baseline-shift="-0.28em" font-size="68%">60</tspan>'), 't', 'middle')
    s += lines_at(1490, 600, ['«футбольный мяч» из 60 атомов C:', '12 пятиугольников', 'и 20 шестиугольников',
                              'Нобелевская премия 1996'], 's', step=34)
    s += text(1490, 760, 'открыт в 1980-е', 'cap', 'middle')
    s += text(900, 900, 'Алмаз и графит — один элемент C, разное строение; алмаз ↔ графит при ~2000 °C и очень высоком давлении', 'cap', 'middle')
    return s


# 2. Известковая вода и избыток CO₂ -----------------------------------------------------------------
def limewater_excess_co2():
    s = text(880, 52, 'Известковая вода и углекислый газ', 'h', 'middle')
    xs = (300, 880, 1460)
    for x in xs:
        s += card(x - 260, 90, 520, 700)
    s += tube(xs[0], 150, WATER)
    s += tube(xs[1], 150, MILK, cloudy=True)
    s += tube(xs[2], 150, WATER)
    s += arrow(xs[0] + 150, 290, xs[1] - 150, 290, INK, 5) + text((xs[0] + xs[1]) / 2, 260, '+ CO₂'.replace('₂', '<tspan baseline-shift="-0.28em" font-size="68%">2</tspan>'), 't', 'middle')
    s += arrow(xs[1] + 150, 290, xs[2] - 150, 290, INK, 5) + text((xs[1] + xs[2]) / 2, 250, 'ещё CO₂', 't', 'middle') + text((xs[1] + xs[2]) / 2, 330, '(избыток)', 'cap', 'middle')
    s += text(xs[0], 470, 'прозрачная', 't', 'middle') + text(xs[1], 470, 'мутнеет', 't', 'middle', RED) + text(xs[2], 470, 'снова прозрачная', 't', 'middle', GREEN)
    s += lines_at(xs[0], 540, ['Ca(OH)₂ в воде', '(известковая вода)'])
    s += lines_at(xs[1], 540, ['Ca(OH)₂ + CO₂ →', 'CaCO₃↓ + H₂O', 'белый осадок'])
    s += lines_at(xs[2], 540, ['CaCO₃ + CO₂ + H₂O →', 'Ca(HCO₃)₂', 'растворимый гидрокарбонат'])
    s += text(880, 760, 'Помутнение известковой воды — качественная реакция на CO₂', 'cap', 'middle')
    return s


# 3. Соотношение NaOH : CO₂ -------------------------------------------------------------------------
def alkali_co2_ratio():
    s = text(900, 52, 'Какая соль получится: отношение n(NaOH) : n(CO₂)', 'h', 'middle')
    s += card(30, 100, 1740, 620)
    x0, x1, y = 160, 1640, 360

    def X(v):
        return x0 + (x1 - x0) * v / 3
    s += f'<rect x="{X(0):.0f}" y="{y - 30}" width="{X(1) - X(0):.0f}" height="60" fill="#DCEBF5"/>'
    s += f'<rect x="{X(1):.0f}" y="{y - 30}" width="{X(2) - X(1):.0f}" height="60" fill="#E7DDF0"/>'
    s += f'<rect x="{X(2):.0f}" y="{y - 30}" width="{X(3) - X(2):.0f}" height="60" fill="#F3E3C9"/>'
    s += arrow(x0, y, x1 + 40, y, INK, 4)
    for v, lab in ((1, '1'), (2, '2')):
        s += bond(X(v), y - 60, X(v), y + 60, 5, RED)
        s += text(X(v), y + 100, lab, 'f', 'middle', RED)
    s += text(X(0) + 10, y + 100, '0', 't', 'middle', GREY)
    s += text(x1 + 40, y + 100, 'n(NaOH) : n(CO₂)'.replace('₂', '<tspan baseline-shift="-0.28em" font-size="68%">2</tspan>'), 's', 'end')
    s += lines_at(X(0.5), 180, ['меньше 1:', 'NaHCO₃ + лишний CO₂'], 's')
    s += lines_at(X(1), 240, ['ровно 1: NaHCO₃'], 's', color=RED)
    s += lines_at(X(1.5), 180, ['между 1 и 2:', 'смесь NaHCO₃ и Na₂CO₃'], 's')
    s += lines_at(X(2), 240, ['ровно 2: Na₂CO₃'], 's', color=RED)
    s += lines_at(X(2.5), 180, ['больше 2:', 'Na₂CO₃ + лишняя NaOH'], 's')
    s += lines_at(900, 560, ['NaOH + CO₂ → NaHCO₃ (1 : 1)', '2NaOH + CO₂ → Na₂CO₃ + H₂O (2 : 1)'], 't', step=46)
    s += text(900, 680, 'Смесь солей: два уравнения — по натрию и по углероду', 'cap', 'middle')
    return s


# 4. Круговорот азота --------------------------------------------------------------------------------
def nitrogen_cycle():
    s = text(900, 52, 'Круговорот азота', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    s += box(900, 180, 560, 90, 'N₂ атмосферы', '#E3EEF7', BLUE, 't')
    s += box(320, 480, 470, 120, 'Белки растений\nи животных', '#E2F1E6', GREEN, 't')
    s += box(900, 800, 520, 120, 'Аммиак NH₃ (NH₄⁺)\nв почве', '#F3E3C9', BROWN, 't')
    s += box(1480, 480, 470, 120, 'Нитраты NO₃⁻\nв почве', '#F1E4F3', PURPLE, 't')
    s += arrow(700, 230, 420, 410, GREEN, 6)
    s += lines_at(470, 260, ['азотфиксация:', 'клубеньковые бактерии', 'бобовых, азотобактер'], 's', 'end')
    s += arrow(380, 550, 700, 760, BROWN, 6)
    s += lines_at(470, 720, ['аммонификация:', 'гниение белков → NH₃'], 's', 'end')
    s += arrow(1110, 760, 1400, 560, PURPLE, 6)
    s += lines_at(1330, 720, ['нитрификация:', 'NH₃ → нитраты'], 's', 'start')
    s += arrow(1240, 470, 570, 470, GREEN, 5)
    s += text(905, 450, 'растения поглощают нитраты', 's', 'middle')
    s += arrow(1440, 410, 1100, 230, BLUE, 6)
    s += lines_at(1360, 260, ['денитрификация:', 'нитраты → N₂'], 's', 'start')
    s += text(900, 920, 'При грозе из N₂ и O₂ образуются оксиды азота', 'cap', 'middle')
    return s


# 5. NH₃ и NH₄⁺ ---------------------------------------------------------------------------------------
def ammonia_ammonium():
    s = text(880, 52, 'Аммиак и ион аммония', 'h', 'middle')
    s += card(30, 90, 760, 640) + card(970, 90, 760, 640)
    # NH3 пирамида
    nx, ny = 410, 330
    hs = [(300, 470), (410, 500), (530, 455)]
    s += f'<polygon points="{" ".join(f"{x},{y}" for x, y in hs)}" fill="#E3EEF7" stroke="{BLUE}" stroke-width="2" stroke-dasharray="8 6"/>'
    for x, y in hs:
        s += bond(nx, ny, x, y, 6) + atom(x, y, 24, '#fff', None)
        s += f'<text x="{x}" y="{y + 9}" text-anchor="middle" style="font: 800 24px Manrope; fill:{INK}">H</text>'
    s += atom(nx, ny, 34, BLUE, 'N', 30)
    s += f'<ellipse cx="{nx}" cy="{ny - 75}" rx="24" ry="34" fill="#F6D27A" stroke="#B88A1E" stroke-width="3"/>'
    s += f'<circle cx="{nx - 8}" cy="{ny - 80}" r="6" fill="{INK}"/><circle cx="{nx + 8}" cy="{ny - 80}" r="6" fill="{INK}"/>'
    s += text(nx + 60, ny - 110, 'неподелённая', 's', 'start') + text(nx + 60, ny - 78, 'пара электронов', 's', 'start')
    s += text(410, 150, 'NH₃ — треугольная пирамида'.replace('₃', '<tspan baseline-shift="-0.28em" font-size="68%">3</tspan>'), 't', 'middle')
    s += lines_at(410, 600, ['степень окисления N −3;', 'раствор — щелочная среда'], 's')
    s += arrow(800, 380, 950, 380, INK, 6) + text(875, 340, '+ H⁺', 't', 'middle')
    # NH4+
    cx, cy = 1350, 380
    pos = [(1350, 230), (1220, 470), (1350, 520), (1480, 470)]
    for k, (x, y) in enumerate(pos):
        s += bond(cx, cy, x, y, 6, RED if k == 0 else INK)
        s += atom(x, y, 24, '#fff')
        s += f'<text x="{x}" y="{y + 9}" text-anchor="middle" style="font: 800 24px Manrope; fill:{INK}">H</text>'
    s += atom(cx, cy, 34, BLUE, 'N', 30)
    s += text(1350, 150, 'NH₄⁺ — тетраэдр'.replace('₄⁺', '<tspan baseline-shift="-0.28em" font-size="68%">4</tspan><tspan baseline-shift="0.6em" font-size="68%">+</tspan>'), 't', 'middle')
    s += text(1420, 240, 'донорно-акцепторная', 's', 'start', RED) + text(1420, 272, 'связь', 's', 'start', RED)
    s += lines_at(1350, 600, ['пара N + свободная орбиталь H⁺;', 'все 4 связи N–H одинаковы'], 's')
    s += lines_at(880, 790, ['NH₃ + H₂O ⇄ NH₄⁺ + OH⁻;  NH₃ + HCl → NH₄Cl («белый дым»)'], 't')
    return s


# 6. Синтез аммиака ---------------------------------------------------------------------------------
def ammonia_synthesis():
    s = text(900, 52, 'Промышленный синтез аммиака', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    s += box(220, 300, 300, 120, 'N₂ + 3H₂\n(1 : 3)', '#E3EEF7', BLUE, 't')
    s += box(560, 300, 240, 120, 'очистка\nот ядов', '#fff')
    s += box(880, 300, 260, 120, 'компрессор\n15–100 МПа', '#fff')
    s += f'<rect x="1120" y="170" width="200" height="300" rx="20" fill="#F3E3C9" stroke="{BROWN}" stroke-width="4"/>'
    s += lines_at(1220, 230, ['колонна', 'синтеза', 'Fe', '450–500 °C'], 's', step=40)
    s += box(1560, 300, 260, 120, 'холодильник:\nNH₃ → жидкость', '#E2F1E6', GREEN)
    s += arrow(370, 300, 440, 300) + arrow(680, 300, 750, 300) + arrow(1010, 300, 1120, 300) + arrow(1320, 300, 1430, 300)
    s += arrow(1560, 360, 1560, 470, GREEN, 5) + text(1560, 510, 'жидкий NH₃', 't', 'middle', GREEN)
    s += f'<path d="M1560 240 V 140 H 880 V 230" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="14 8"/>'
    s += arrow(880, 200, 880, 236, RED, 5)
    s += text(1220, 125, 'циркуляция: непрореагировавшие N₂ и H₂ возвращаются', 's', 'middle', RED)
    s += lines_at(900, 620, ['N₂ + 3H₂ ⇄ 2NH₃ + 92 кДж'], 'f')
    s += lines_at(900, 700, ['давление повышают — объём газов уменьшается; 450–500 °C — компромисс скорости и выхода;',
                             'за один проход превращается не более 20 % — поэтому газы возвращают в цикл'], 's', step=36)
    return s


# 7. Производство азотной кислоты ------------------------------------------------------------------
def nitric_acid_production():
    s = text(900, 52, 'Получение азотной кислоты из аммиака', 'h', 'middle')
    s += card(30, 90, 1740, 640)
    xs = (230, 690, 1150, 1600)
    labels = [('NH₃', '−3'), ('NO', '+2'), ('NO₂', '+4'), ('HNO₃', '+5')]
    for x, (f, ox) in zip(xs, labels):
        s += f'<circle cx="{x}" cy="260" r="95" fill="#fff" stroke="{INK}" stroke-width="4"/>'
        s += text(x, 278, chem(f), 'f', 'middle')
        s += text(x, 395, 'N: ' + ox, 't', 'middle', BLUE)
    steps = [('1) 4NH₃ + 5O₂ → 4NO + 6H₂O', 'катализатор Pt, ~800 °C'),
             ('2) 2NO + O₂ → 2NO₂', 'бурый газ'),
             ('3) 4NO₂ + O₂ + 2H₂O → 4HNO₃', 'поглощение водой')]
    for k, (eq, cond) in enumerate(steps):
        s += arrow(xs[k] + 100, 260, xs[k + 1] - 100, 260, RED, 6)
        s += text((xs[k] + xs[k + 1]) / 2, 140, cond, 'cap', 'middle')
    for k, (eq, cond) in enumerate(steps):
        s += text(900, 500 + k * 52, chem(eq), 't', 'middle')
    s += text(900, 690, 'Без катализатора аммиак горит до N₂: 4NH₃ + 3O₂ → 2N₂ + 6H₂O'.replace('NH₃', 'NH<tspan baseline-shift="-0.28em" font-size="68%">3</tspan>').replace('O₂', 'O<tspan baseline-shift="-0.28em" font-size="68%">2</tspan>').replace('N₂', 'N<tspan baseline-shift="-0.28em" font-size="68%">2</tspan>').replace('H₂O', 'H<tspan baseline-shift="-0.28em" font-size="68%">2</tspan>O'), 'cap', 'middle')
    return s


# 8. Разложение нитратов ----------------------------------------------------------------------------
def nitrate_decomposition():
    s = text(900, 52, 'Разложение нитратов при нагревании', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    rows = [('K, Na', 'нитрит + O₂', '2NaNO₃ → 2NaNO₂ + O₂', '#E3EEF7'),
            ('от Mg до Cu', 'оксид металла + NO₂ + O₂', '2Cu(NO₃)₂ → 2CuO + 4NO₂ + O₂', '#F3E3C9'),
            ('Ag, Hg', 'металл + NO₂ + O₂', '2AgNO₃ → 2Ag + 2NO₂ + O₂', '#ECECEC'),
            ('NH₄⁺', 'без твёрдого остатка', 'NH₄NO₃ → N₂O + 2H₂O', '#F1E4F3')]
    s += text(250, 160, 'Металл нитрата', 's', 'middle', GREY) + text(760, 160, 'Продукты', 's', 'middle', GREY) + text(1360, 160, 'Пример', 's', 'middle', GREY)
    for k, (m, prod, ex, fill) in enumerate(rows):
        y = 190 + k * 140
        s += f'<rect x="70" y="{y}" width="1660" height="120" rx="14" fill="{fill}"/>'
        s += text(250, y + 72, chem(m), 't', 'middle')
        s += text(760, y + 72, chem(prod), 't', 'middle')
        s += text(1360, y + 72, chem(ex), 't', 'middle')
    s += text(900, 800, 'Чем правее металл в ряду активности, тем «глубже» разложение; бурый газ — NO₂', 'cap', 'middle')
    return s


# 9. Аллотропия фосфора ------------------------------------------------------------------------------
def phosphorus_allotropes():
    s = text(900, 52, 'Аллотропия фосфора', 'h', 'middle')
    data = [('Белый', '#F4F0DE', ['молекулы P₄, режется ножом', 't пл. 44 °C; ρ 1,8 г/см³', 'светится в темноте', 'сильный яд, самовоспламеняется —', 'хранят под водой']),
            ('Красный', '#E9B3A6', ['тёмно-красный порошок', 'ρ 2,3 г/см³', 'не светится, не ядовит', 'загорается при 260 °C;', 'на коробке спичек']),
            ('Чёрный', '#6E6A66', ['похож на графит', 'ρ 2,7 г/см³', 'полупроводник', '', ''])]
    for k, (name, fill, rows) in enumerate(data):
        x = 30 + k * 590
        s += card(x, 90, 560, 760)
        cx, cy = x + 280, 290
        if k == 0:
            pts = [(cx, cy - 110), (cx - 100, cy + 60), (cx + 100, cy + 60), (cx + 15, cy - 5)]
            for i in range(4):
                for j in range(i + 1, 4):
                    s += bond(*pts[i], *pts[j], 6, INK, '10 6' if 3 in (i, j) else None)
            for x_, y_ in pts:
                s += atom(x_, y_, 28, '#E8D98F', None)
                s += f'<text x="{x_:.0f}" y="{y_ + 10:.0f}" text-anchor="middle" style="font: 800 26px Manrope; fill:{INK}">P</text>'
            s += text(cx, cy + 140, 'молекула P₄ (тетраэдр)'.replace('₄', '<tspan baseline-shift="-0.28em" font-size="68%">4</tspan>'), 'cap', 'middle')
        else:
            s += f'<rect x="{cx - 150}" y="{cy - 110}" width="300" height="200" rx="30" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            for j in range(18):
                gx = cx - 120 + (j * 0.618 % 1) * 240
                gy = cy - 80 + (j * 0.414 % 1) * 160
                s += f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="9" fill="{"#B5523F" if k == 1 else "#3E3B38"}"/>'
        s += text(cx, 150, name, 't', 'middle')
        s += lines_at(cx, 500, [r for r in rows if r], 's', step=40)
    s += text(900, 900, 'Белый фосфор получают из фосфоритов в электропечи (~1500 °C): пары фосфора конденсируют под водой', 'cap', 'middle')
    return s


# 10. Три ряда фосфатов ------------------------------------------------------------------------------
def phosphate_series():
    s = text(900, 52, 'Фосфорная кислота и три ряда солей', 'h', 'middle')
    s += card(30, 90, 1740, 640)
    items = [('H₃PO₄', 'кислота', '—'),
             ('H₂PO₄⁻', 'дигидрофосфат', 'NaH₂PO₄ (1 : 1)'),
             ('HPO₄²⁻', 'гидрофосфат', 'Na₂HPO₄ (1 : 2)'),
             ('PO₄³⁻', 'фосфат', 'Na₃PO₄ (1 : 3)')]
    xs = (240, 680, 1120, 1560)
    for k, (ion, name, salt) in enumerate(items):
        s += f'<rect x="{xs[k] - 175}" y="180" width="350" height="190" rx="18" fill="{["#ECECEC", "#E3EEF7", "#E2F1E6", "#F3E3C9"][k]}" stroke="{INK}" stroke-width="3"/>'
        s += text(xs[k], 265, chem(ion), 'f', 'middle')
        s += text(xs[k], 330, name, 't', 'middle')
        s += text(xs[k], 440, chem(salt), 's', 'middle')
        if k < 3:
            s += arrow(xs[k] + 180, 275, xs[k + 1] - 180, 275, RED, 5)
            s += text((xs[k] + xs[k + 1]) / 2, 240, '+OH⁻'.replace('⁻', '<tspan baseline-shift="0.6em" font-size="68%">−</tspan>'), 's', 'middle', RED)
    s += text(900, 530, 'n(H₃PO₄) : n(NaOH) = 1 : 1 → NaH₂PO₄;  1 : 2 → Na₂HPO₄;  1 : 3 → Na₃PO₄'.replace('H₃PO₄', 'H<tspan baseline-shift="-0.28em" font-size="68%">3</tspan>PO<tspan baseline-shift="-0.28em" font-size="68%">4</tspan>').replace('NaH₂PO₄', 'NaH<tspan baseline-shift="-0.28em" font-size="68%">2</tspan>PO<tspan baseline-shift="-0.28em" font-size="68%">4</tspan>').replace('Na₂HPO₄', 'Na<tspan baseline-shift="-0.28em" font-size="68%">2</tspan>HPO<tspan baseline-shift="-0.28em" font-size="68%">4</tspan>').replace('Na₃PO₄', 'Na<tspan baseline-shift="-0.28em" font-size="68%">3</tspan>PO<tspan baseline-shift="-0.28em" font-size="68%">4</tspan>'), 't', 'middle')
    s += text(900, 600, 'Промежуточное соотношение — смесь двух соседних солей', 's', 'middle')
    s += text(900, 680, 'Качественная реакция на PO₄³⁻: с AgNO₃ — жёлтый осадок Ag₃PO₄'.replace('PO₄³⁻', 'PO<tspan baseline-shift="-0.28em" font-size="68%">4</tspan><tspan baseline-shift="0.6em" font-size="68%">3−</tspan>').replace('AgNO₃', 'AgNO<tspan baseline-shift="-0.28em" font-size="68%">3</tspan>').replace('Ag₃PO₄', 'Ag<tspan baseline-shift="-0.28em" font-size="68%">3</tspan>PO<tspan baseline-shift="-0.28em" font-size="68%">4</tspan>'), 'cap', 'middle')
    return s


# 11. Минеральные удобрения ------------------------------------------------------------------------
def mineral_fertilizers():
    s = text(900, 52, 'Минеральные удобрения: N, P, K', 'h', 'middle')
    cols = [('N', 'Азотные', BLUE, ['NH₄NO₃ — аммиачная селитра (35 % N)', 'CO(NH₂)₂ — карбамид (46,7 % N)', '(NH₄)₂SO₄, NH₄Cl', 'NaNO₃, KNO₃ — селитры']),
            ('P', 'Фосфорные', ORANGE, ['Ca(H₂PO₄)₂ — двойной суперфосфат', 'аммофос: NH₄H₂PO₄ + (NH₄)₂HPO₄', 'фосфоритная мука Ca₃(PO₄)₂', '(плохо растворима)']),
            ('K', 'Калийные', PURPLE, ['KCl', 'KNO₃ (и азот, и калий)', 'зола — поташ K₂CO₃', ''])]
    for k, (el, name, color, rows) in enumerate(cols):
        x = 30 + k * 590
        s += card(x, 90, 560, 620)
        s += f'<circle cx="{x + 280}" cy="210" r="70" fill="{color}"/>' + text(x + 280, 238, el, 'f', 'middle', '#fff')
        s += text(x + 280, 330, name, 't', 'middle')
        s += lines_at(x + 280, 400, [r for r in rows if r], 's', step=48)
    s += card(30, 740, 1740, 150, '#F1EDE3')
    s += text(900, 795, 'Казахстан: фосфориты Каратау; завод «Минеральные удобрения» в Таразе; академик А. Б. Бектуров (1901–1985)', 's', 'middle')
    s += text(900, 850, 'Аммиачную селитру не смешивают с известью — выделяется аммиак; избыток азотных удобрений — нитраты в продуктах', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'carbon-allotropes.png': (carbon_allotropes(), 1800, 940),
        'limewater-excess-co2.png': (limewater_excess_co2(), 1760, 820),
        'alkali-co2-ratio.png': (alkali_co2_ratio(), 1800, 750),
        'nitrogen-cycle.png': (nitrogen_cycle(), 1800, 980),
        'ammonia-ammonium.png': (ammonia_ammonium(), 1760, 830),
        'ammonia-synthesis.png': (ammonia_synthesis(), 1800, 880),
        'nitric-acid-production.png': (nitric_acid_production(), 1800, 760),
        'nitrate-decomposition.png': (nitrate_decomposition(), 1800, 880),
        'phosphorus-allotropes.png': (phosphorus_allotropes(), 1800, 940),
        'phosphate-series.png': (phosphate_series(), 1800, 760),
        'mineral-fertilizers.png': (mineral_fertilizers(), 1800, 920),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
