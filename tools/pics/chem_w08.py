"""Рисунки недели 8 химии (course/week-08/pics/*.png): проводимость растворов, гидратация, ионные уравнения, pH и индикаторы,
гидролиз, качественные реакции.

Факты — по выжимке course/textbooks/chem-08-electrolytes.md (Х9-1 § 1–12, Х11-2 § 53–55). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w08.py
"""
from __future__ import annotations

import math

from common import GREY, INK, PAPER, RED, ROOT, arrow, chem, render, span, text

OUT = ROOT / 'course' / 'week-08' / 'pics'
BLUE, WATER, O_RED, H_GREY = '#3A57A7', '#E4EEF8', '#E2574C', '#F2F2F2'


def lines_at(x, y, rows, cls='s', anchor='middle', step=32, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def ion(x, y, sign, r=14):
    col = RED if sign == '+' else BLUE
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" stroke="{col}" stroke-width="3"/>'
            + text(x, y + 8, '+' if sign == '+' else '−', 's', 'middle', col))


# 1. Проводимость ----------------------------------------------------------------------------------
def device(x, glow, inside, title, rows):
    """Одинаковый прибор: стакан, два электрода, лампа и источник тока."""
    cx, top, bw, bh = x + 140, 300, 200, 190
    s = ''
    # провода и источник
    s += f'<path d="M{cx - 50} {top + 30} V {top - 140} H {cx + 50} V {top + 30}" fill="none" stroke="{INK}" stroke-width="4"/>'
    s += f'<rect x="{cx + 30}" y="{top - 70}" width="40" height="34" fill="#fff"/>'
    s += f'<path d="M{cx + 30} {top - 62} H {cx + 70} M{cx + 38} {top - 44} H {cx + 62}" stroke="{INK}" stroke-width="5"/>'
    # лампа
    ly = top - 140
    if glow:
        rays = ''.join(f'<path d="M{cx + 40 * math.cos(a):.0f} {ly + 40 * math.sin(a):.0f} L {cx + (40 + 18 * glow) * math.cos(a):.0f} '
                       f'{ly + (40 + 18 * glow) * math.sin(a):.0f}" stroke="#F2B705" stroke-width="5" stroke-linecap="round"/>'
                       for a in [math.pi * (1 + k / 6) for k in range(7)])
        s += rays
    fill = {0: '#fff', 1: '#FBEBB0', 2: '#F7D23E'}[glow]
    s += f'<circle cx="{cx}" cy="{ly}" r="28" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
    # стакан
    if inside != 'dry':
        s += f'<rect x="{cx - bw / 2}" y="{top + 30}" width="{bw}" height="{bh - 30}" fill="{WATER}"/>'
    s += f'<path d="M{cx - bw / 2} {top - 10} V {top + bh} H {cx + bw / 2} V {top - 10}" fill="none" stroke="{INK}" stroke-width="4"/>'
    s += f'<rect x="{cx - 58}" y="{top + 10}" width="16" height="150" fill="#5B5B5B"/><rect x="{cx + 42}" y="{top + 10}" width="16" height="150" fill="#5B5B5B"/>'
    if inside == 'dry':
        for i in range(4):
            for j in range(2):
                gx, gy = cx - 30 + i * 18, top + bh - 40 + j * 18
                s += f'<rect x="{gx - 8}" y="{gy - 8}" width="16" height="16" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    elif inside == 'ions':
        for k, (dx, dy) in enumerate(((-15, 60), (15, 100), (-20, 140), (20, 50), (0, 125), (-5, 85))):
            s += ion(cx + dx, top + dy, '+' if k % 2 else '−', 11)
    elif inside == 'sugar':
        for dx, dy in ((-15, 70), (18, 105), (-10, 140), (10, 60)):
            s += f'<ellipse cx="{cx + dx}" cy="{top + dy}" rx="16" ry="10" fill="#fff" stroke="{GREY}" stroke-width="3"/>'
    elif inside == 'weak':
        for dx, dy in ((-15, 70), (18, 105), (-10, 140), (14, 145)):
            s += f'<ellipse cx="{cx + dx}" cy="{top + dy}" rx="16" ry="10" fill="#fff" stroke="{GREY}" stroke-width="3"/>'
        s += ion(cx + 5, top + 60, '+', 11) + ion(cx - 5, top + 110, '−', 11)
    s += text(cx, top + bh + 50, title, 't', 'middle')
    s += lines_at(cx, top + bh + 88, rows, 'cap')
    return s


def conductivity() -> str:
    s = text(800, 56, 'Проводит ли ток? Один и тот же прибор', 'h', 'middle')
    cases = [(0, 'dry', 'сухой NaCl', ['не горит:', 'ионы в решётке']),
             (0, 'water', 'вода', ['дистиллированная:', 'почти не проводит']),
             (0, 'sugar', 'раствор сахара', ['не горит:', 'только молекулы']),
             (1, 'weak', 'уксусная кислота', ['слабо: ионов мало,', 'слабый электролит']),
             (2, 'ions', 'раствор NaCl', ['горит: подвижные', 'ионы Na⁺ и Cl⁻'])]
    for k, (glow, inside, title, rows) in enumerate(cases):
        s += device(20 + k * 312, glow, inside, title, rows)
    return s


# 2. Гидратация ------------------------------------------------------------------------------------
def water(x, y, ang, toward_o=True):
    """Молекула воды: O в (x, y); атомы H под углом 104,5°, смотрят по направлению ang (радианы)."""
    s = ''
    for d in (-52.25, 52.25):
        a = ang + math.radians(d)
        hx, hy = x + 30 * math.cos(a), y + 30 * math.sin(a)
        s += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{hx:.0f}" y2="{hy:.0f}" stroke="{INK}" stroke-width="3"/>'
        s += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="11" fill="{H_GREY}" stroke="{INK}" stroke-width="2"/>'
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="18" fill="{O_RED}" stroke="{INK}" stroke-width="2"/>'
    return s


def hydrated(cx, cy, sym, o_inward):
    s = f'<circle cx="{cx}" cy="{cy}" r="{40 if sym == "Cl⁻" else 30}" fill="#fff" stroke="{BLUE if sym == "Cl⁻" else RED}" stroke-width="4"/>'
    s += text(cx, cy + 11, chem(sym), 't', 'middle', BLUE if sym == 'Cl⁻' else RED)
    for k in range(6):
        a = k * math.pi / 3 + math.pi / 6
        if o_inward:
            d = 78
            s += water(cx + d * math.cos(a), cy + d * math.sin(a), a)
        else:
            d = 102
            ox, oy = cx + d * math.cos(a), cy + d * math.sin(a)
            # H к иону: один H направлен прямо на центр
            s += water(ox, oy, a + math.pi + math.radians(52.25))
    return s


def hydration() -> str:
    s = text(800, 56, 'Гидратация ионов и ионизация', 'h', 'middle')
    s += hydrated(240, 300, 'Na⁺', True) + text(240, 490, 'к Na⁺ вода обращена кислородом (δ−)', 's', 'middle')
    s += hydrated(720, 300, 'Cl⁻', False) + text(720, 490, 'к Cl⁻ — водородами (δ+)', 's', 'middle')
    # легенда
    s += water(1060, 170, 0) + text(1110, 180, chem('H₂O — диполь, угол 104,5°'), 's')
    s += f'<rect x="1000" y="250" width="560" height="200" rx="16" fill="{PAPER}"/>'
    s += text(1280, 295, 'Полярная молекула HCl:', 't', 'middle')
    s += text(1280, 345, chem('HCl + H₂O → H₃O⁺ + Cl⁻'), 't', 'middle', RED)
    s += lines_at(1280, 390, ['H₃O⁺ — ион оксония;', 'в уравнениях пишут H⁺'], 's')
    s += text(800, 570, chem('NaCl: ионы уже были в решётке → гидратация → диссоциация. HCl: связь ковалентная полярная → ионизация.'), 's', 'middle')
    return s


# 3. Ионные уравнения ------------------------------------------------------------------------------
def ionic_equations() -> str:
    s = text(800, 56, 'Три записи одной реакции', 'h', 'middle')
    rows = [('молекулярное', 'Na₂SO₄ + BaCl₂ = 2NaCl + BaSO₄↓', None),
            ('полное ионное', None, None),
            ('сокращённое', 'Ba²⁺ + SO₄²⁻ = BaSO₄↓', RED)]
    for k, (name, eq, col) in enumerate(rows):
        y = 150 + k * 100
        s += f'<rect x="60" y="{y - 40}" width="1480" height="70" rx="14" fill="{PAPER if k != 2 else "#FDECEC"}"/>'
        s += text(90, y + 6, name, 's', 'start', GREY)
        if eq:
            s += text(330, y + 8, chem(eq), 't', 'start', col)
    g = GREY
    full = (span(chem('2Na⁺'), g) + ' + ' + chem('SO₄²⁻') + ' + ' + chem('Ba²⁺') + ' + ' + span(chem('2Cl⁻'), g)
            + ' = ' + span(chem('2Na⁺'), g) + ' + ' + span(chem('2Cl⁻'), g) + ' + ' + chem('BaSO₄↓'))
    s += text(330, 258, full, 't')
    s += text(1530, 300, 'серые ионы не меняются — их сокращают', 'cap', 'end')
    s += text(800, 440, 'Обмен идёт до конца, если образуется:', 't', 'middle')
    cards = [('осадок', 'Ba²⁺ + SO₄²⁻ = BaSO₄↓'), ('газ', '2H⁺ + S²⁻ = H₂S↑'), ('вода', 'H⁺ + OH⁻ = H₂O')]
    for k, (title, eq) in enumerate(cards):
        x = 100 + k * 480
        s += f'<rect x="{x}" y="470" width="440" height="130" rx="16" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += text(x + 220, 515, title, 't', 'middle', RED) + text(x + 220, 570, chem(eq), 't', 'middle')
    s += text(800, 660, chem('Na₂SO₄ + KCl: все ионы сократились — реакция до конца не идёт.'), 's', 'middle')
    return s


# 4. pH и индикаторы -------------------------------------------------------------------------------
def ph_indicators() -> str:
    s = text(800, 56, 'Шкала pH (25 °C) и индикаторы', 'h', 'middle')
    x0, w, y = 120, 1360, 140
    stops = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in ((0, '#E5484D'), (0.35, '#F5A524'), (0.5, '#7BC67E'), (0.65, '#4BA3C7'), (1, '#5B3FA8')))
    s += f'<defs><linearGradient id="ph">{stops}</linearGradient></defs>'
    s += f'<rect x="{x0}" y="{y}" width="{w}" height="60" rx="10" fill="url(#ph)"/>'
    for v in range(15):
        px = x0 + w * v / 14
        s += f'<line x1="{px:.0f}" y1="{y + 60}" x2="{px:.0f}" y2="{y + 74}" stroke="{INK}" stroke-width="2"/>' + text(px, y + 100, str(v), 's', 'middle')
    s += text(x0 + w * 3.5 / 14, y + 145, 'кислая, pH < 7', 't', 'middle') + text(x0 + w / 2, y + 145, 'нейтр., 7', 't', 'middle')
    s += text(x0 + w * 10.5 / 14, y + 145, 'щелочная, pH > 7', 't', 'middle')
    for v, cap in ((3, chem('HCl 10⁻³ М')), (7.4, 'кровь ≈ 7,4'), (10, chem('NaOH 10⁻⁴ М'))):
        px = x0 + w * v / 14
        s += f'<path d="M{px:.0f} {y - 4} l -10 -18 h 20 Z" fill="{INK}"/>' + text(px, y - 30, cap, 'cap', 'middle', INK)
    s += arrow(x0 + w * 6 / 14, y + 185, x0 + w * 1 / 14, y + 185, RED, 4) + text(x0 + w * 3.5 / 14, y + 220, chem('[H⁺] растёт'), 'cap', 'middle', RED)
    # таблица индикаторов
    ty = 450
    heads = ['кислая', 'нейтральная', 'щелочная']
    colors = [('лакмус', [('#D8343C', 'красный'), ('#8A5BB8', 'фиолетовый'), ('#3159B5', 'синий')]),
              ('метилоранж', [('#F27C8C', 'розовый'), ('#F59A2B', 'оранжевый'), ('#F2D33A', 'жёлтый')]),
              ('фенолфталеин', [(None, 'бесцветный'), (None, 'бесцветный'), ('#C2185B', 'малиновый')])]
    for j, h in enumerate(heads):
        s += text(560 + j * 340, ty - 20, h, 's', 'middle', GREY)
    for i, (name, cells) in enumerate(colors):
        yy = ty + i * 80
        s += text(370, yy + 42, name, 't', 'end')
        for j, (col, cap) in enumerate(cells):
            x = 410 + j * 340
            if col:
                s += f'<rect x="{x}" y="{yy}" width="300" height="62" rx="10" fill="{col}"/>'
                s += text(x + 150, yy + 41, cap, 's', 'middle', '#fff' if col not in ('#F2D33A',) else INK)
            else:
                s += f'<rect x="{x}" y="{yy}" width="300" height="62" rx="10" fill="#fff" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 6"/>'
                s += text(x + 150, yy + 41, cap, 's', 'middle', GREY)
    return s


# 5. Гидролиз --------------------------------------------------------------------------------------
def hydrolysis() -> str:
    s = text(800, 56, 'Гидролиз солей: какой ион слабый?', 'h', 'middle')
    cards = [('NaCl, KNO₃', 'сильное основание + сильная кислота', 'гидролиза нет', None, 'нейтральная, pH = 7', ('#8A5BB8', 'лакмус фиолетовый')),
             ('Na₂CO₃, K₂CO₃', 'сильное основание + слабая кислота', 'по аниону', 'CO₃²⁻ + H₂O ⇄ HCO₃⁻ + OH⁻', 'щелочная, pH > 7', ('#C2185B', 'фенолфталеин малиновый')),
             ('ZnCl₂, FeCl₃', 'слабое основание + сильная кислота', 'по катиону', 'Zn²⁺ + H₂O ⇄ ZnOH⁺ + H⁺', 'кислая, pH < 7', ('#D8343C', 'лакмус красный')),
             ('Al₂S₃', 'слабое основание + слабая кислота', 'полный, необратимый', 'Al₂S₃ + 6H₂O = 2Al(OH)₃↓ + 3H₂S↑', 'в воде не существует', None)]
    for k, (salt, parents, kind, eq, env, ind) in enumerate(cards):
        x = 30 + k * 390
        cx = x + 180
        s += f'<rect x="{x}" y="100" width="360" height="560" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += f'<text x="{cx}" y="165" text-anchor="middle" style="font-size:40px;font-weight:800">{chem(salt)}</text>'
        words = parents.split(' + ')
        s += lines_at(cx, 215, [words[0] + ' +', words[1]], 'cap')
        s += f'<rect x="{x + 20}" y="275" width="320" height="56" rx="12" fill="{PAPER}"/>' + text(cx, 311, kind, 's', 'middle', RED)
        if eq:
            if len(eq) > 26:
                left, right = eq.split(' = ')
                s += lines_at(cx, 385, [left + ' =', right], 's', step=36)
            else:
                s += text(cx, 395, chem(eq), 's', 'middle')
        else:
            s += lines_at(cx, 385, ['ни один ион', 'не связывает воду'], 'cap')
        s += text(cx, 490, env, 't', 'middle')
        if ind:
            s += f'<rect x="{x + 15}" y="530" width="330" height="56" rx="12" fill="{ind[0]}"/>' + text(cx, 567, ind[1], 'cap', 'middle', '#fff')
        else:
            s += lines_at(cx, 545, ['осадок и газ', 'одновременно'], 'cap')
    s += text(800, 710, chem('Ион слабого «родителя» связывает часть воды: остаются лишние OH⁻ (щелочная среда) или H⁺ (кислая).'), 's', 'middle')
    return s


# 6. Качественные реакции --------------------------------------------------------------------------
def flame(cx, base, color):
    return (f'<path d="M{cx} {base - 150} C {cx + 50} {base - 90} {cx + 45} {base - 20} {cx} {base} C {cx - 45} {base - 20} {cx - 50} {base - 90} {cx} {base - 150} Z" '
            f'fill="{color}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{cx - 14}" y="{base}" width="28" height="40" fill="#9A9A9A" stroke="{INK}" stroke-width="2"/>')


def tube(cx, top, fill, sediment=None, h=200):
    s = f'<path d="M{cx - 26} {top} V {top + h - 26} A 26 26 0 0 0 {cx + 26} {top + h - 26} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if sediment:
        s += f'<path d="M{cx - 26} {top + h - 60} V {top + h - 26} A 26 26 0 0 0 {cx + 26} {top + h - 26} V {top + h - 60} Z" fill="{sediment}" stroke="{INK}" stroke-width="2"/>'
    return s


def ion_signatures() -> str:
    s = text(800, 56, 'Как узнать ион: пламя и осадки', 'h', 'middle')
    flames = [('Li⁺', '#C2185B', 'малиновое'), ('Na⁺', '#F4C20D', 'жёлтое'), ('K⁺', '#8E5BD0', 'фиолетовое'),
              ('Ca²⁺', '#C0502E', 'кирпично-красное'), ('Sr²⁺', '#D0103A', 'карминово-красное'), ('Ba²⁺', '#A8C83A', 'жёлто-зелёное')]
    for k, (sym, col, cap) in enumerate(flames):
        cx = 150 + k * 260
        s += flame(cx, 280, col) + text(cx, 370, chem(sym), 't', 'middle') + text(cx, 405, cap, 'cap', 'middle')
    s += text(800, 450, 'K⁺ — пламя рассматривают через кобальтовое стекло', 'cap', 'middle')
    # осадки
    sed = [('Cu²⁺ + OH⁻', '#5BB8E8', 'Cu(OH)₂', 'голубой'), ('Fe²⁺ + OH⁻', '#7FA35A', 'Fe(OH)₂', 'зелёный, буреет'),
           ('Fe³⁺ + OH⁻', '#8B4A1F', 'Fe(OH)₃', 'бурый'), ('Ag⁺ + Cl⁻', '#FFFFFF', 'AgCl', 'белый творожистый'),
           ('Ba²⁺ + SO₄²⁻', '#FFFFFF', 'BaSO₄', 'белый')]
    for k, (pair, col, formula, color) in enumerate(sed):
        cx = 110 + k * 200
        s += tube(cx, 500, WATER, col) + text(cx, 740, chem(pair), 's', 'middle')
        s += text(cx, 776, chem(formula), 'cap', 'middle', INK) + text(cx, 806, color, 'cap', 'middle')
    # Zn/Al
    x = 1010
    s += f'<rect x="{x}" y="480" width="570" height="340" rx="16" fill="{PAPER}"/>'
    s += tube(x + 110, 500, WATER, '#FFFFFF') + arrow(x + 170, 600, x + 380, 600, INK, 4) + tube(x + 450, 500, WATER)
    s += text(x + 275, 575, chem('избыток OH⁻'), 'cap', 'middle')
    s += text(x + 110, 740, chem('Zn²⁺, Al³⁺ + OH⁻'), 's', 'middle') + text(x + 110, 776, 'белый студенистый', 'cap', 'middle')
    s += text(x + 450, 740, 'растворяется', 's', 'middle', RED)
    s += text(x + 450, 776, chem('Cu(OH)₂, Fe(OH)₃ —'), 'cap', 'middle') + text(x + 450, 806, 'не растворяются', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'conductivity.png': (conductivity(), 1600, 640),
        'hydration.png': (hydration(), 1600, 610),
        'ionic-equations.png': (ionic_equations(), 1600, 700),
        'ph-indicators.png': (ph_indicators(), 1600, 700),
        'hydrolysis.png': (hydrolysis(), 1600, 740),
        'ion-signatures.png': (ion_signatures(), 1600, 850),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
