"""Рисунки недели 13 химии (course/week-13/pics/*.png): металлы в Периодической системе, металлическая решётка,
ряд активности, способы получения металлов, коррозионные пары, известковая вода и CO₂, жёсткость воды.

Факты — по выжимке course/textbooks/chem-13-metals.md (Х9-1 § 21–23, 25–26; Х8 § 14, 55; Х10-2 § 57–59; Х11-2 § 58–59).
Схемы условные. Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w13.py
"""
from __future__ import annotations

import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-13' / 'pics'
BLUE, ORANGE, METAL, NONMET = '#3A57A7', '#D98A2B', '#DCE3F2', '#F7EFC8'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER, stroke=None):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"{st}/>'


# 1. Металлы в Периодической системе ------------------------------------------------------------
ROWS = [
    'H' + ' ' * 16 + 'He',
    'Li Be . . . . . . . . . . B C N O F Ne',
    'Na Mg . . . . . . . . . . Al Si P S Cl Ar',
    'K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr',
    'Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe',
    'Cs Ba * Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn',
    'Fr Ra ** Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og',
]
NONMETALS = {'H', 'He', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Si', 'P', 'S', 'Cl', 'Ar', 'As', 'Se', 'Br', 'Kr',
             'Te', 'I', 'Xe', 'At', 'Rn', 'Ts', 'Og'}


def metal_periodic_table() -> str:
    s = text(800, 50, 'Металлы в Периодической системе', 'h', 'middle')
    x0, y0, c = 140, 100, 72
    grid = [['H'] + [''] * 16 + ['He']] + [r.split() for r in ROWS[1:]]
    for i, row in enumerate(grid):
        for j, sym in enumerate(row):
            if sym in ('', '.'):
                continue
            x, y = x0 + j * c, y0 + i * c
            fill = NONMET if sym in NONMETALS else METAL
            if sym in ('*', '**'):
                fill = METAL
            s += f'<rect x="{x + 2}" y="{y + 2}" width="{c - 4}" height="{c - 4}" rx="8" fill="{fill}"/>'
            lab = {'*': 'La–Lu', '**': 'Ac–Lr'}.get(sym, sym)
            s += text(x + c / 2, y + c / 2 + (9 if len(lab) < 4 else 6), lab, 't' if len(lab) < 4 else 'cap', 'middle')
    # ступенчатая линия B — At
    pts = [(12, 1), (13, 1), (13, 2), (14, 2), (14, 3), (15, 3), (15, 4), (16, 4), (16, 5), (17, 5), (17, 7)]
    d = 'M' + ' L '.join(f'{x0 + a * c} {y0 + b * c}' for a, b in pts)
    s += f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="7" stroke-linejoin="round"/>'
    s += text(x0 + 12.6 * c, y0 + 0.75 * c, 'линия B — At', 't', 'middle', RED)
    s += arrow(70, y0 + 40, 70, y0 + 7 * c - 20, INK, 5)
    s += text(56, y0 + 3.5 * c, 'вниз — сильнее', 'cap', 'middle').replace('text-anchor="middle"', 'text-anchor="middle" transform="rotate(-90 56 352)"')
    s += arrow(x0 + 11 * c, y0 + 7 * c + 40, x0 + 1 * c, y0 + 7 * c + 40, INK, 5)
    s += text(x0 + 6 * c, y0 + 7 * c + 80, 'металлические свойства усиливаются вниз по группе и влево по периоду', 's', 'middle')
    s += f'<rect x="{x0 + 13 * c}" y="{y0 + 7 * c + 100}" width="34" height="34" rx="6" fill="{METAL}"/>' + text(x0 + 13 * c + 46, y0 + 7 * c + 128, 'металлы', 's')
    s += f'<rect x="{x0 + 15.4 * c}" y="{y0 + 7 * c + 100}" width="34" height="34" rx="6" fill="{NONMET}"/>' + text(x0 + 15.4 * c + 46, y0 + 7 * c + 128, 'неметаллы', 's')
    s += text(x0 + 6 * c, y0 + 7 * c + 124, 'все элементы побочных подгрупп, лантаноиды и актиноиды — металлы', 'cap', 'middle')
    return s


# 2. Металлическая решётка ---------------------------------------------------------------------
def ion(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="30" fill="#D9E2F3" stroke="{BLUE}" stroke-width="3"/>'
            + text(cx, cy + 11, '+', 'f', 'middle', BLUE))


def electrons(x0, y0, w, h, n=26, seed=3):
    s, k = '', seed
    for _ in range(n):
        k = (k * 37 + 11) % 997
        ex, ey = x0 + (k % 97) / 97 * w, y0 + ((k * 7) % 89) / 89 * h
        s += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="6" fill="{ORANGE}"/>'
    return s


def metal_lattice() -> str:
    s = text(800, 50, 'Металлическая связь и решётка', 'h', 'middle')
    s += card(40, 90, 740, 470)
    for i in range(4):
        for j in range(5):
            s += ion(140 + j * 130, 170 + i * 105)
    s += electrons(90, 130, 640, 400, 34)
    s += text(410, 610, 'ионы-остовы (+) и обобществлённые электроны', 's', 'middle')
    s += card(820, 90, 740, 210)
    s += text(1190, 130, 'сдвиг слоя — связь сохраняется', 't', 'middle')
    for j in range(6):
        s += ion(900 + j * 105, 190)
        s += ion(950 + j * 105, 250)
    s += arrow(1440, 250, 1530, 250, RED, 4)
    s += card(820, 330, 740, 230)
    s += text(1190, 370, 'ток — направленное движение электронов', 't', 'middle')
    for j in range(6):
        s += ion(900 + j * 105, 450)
    s += ''.join(arrow(880 + j * 105, 505, 940 + j * 105, 505, ORANGE, 3) for j in range(6))
    s += text(840, 545, '−', 'f', 'middle', INK) + text(1540, 545, '+', 'f', 'middle', RED)
    s += text(1190, 610, 'отсюда пластичность, электро- и теплопроводность, блеск', 's', 'middle')
    return s


# 3. Ряд активности ---------------------------------------------------------------------------
SERIES = ['Li', 'K', 'Ba', 'Ca', 'Na', 'Mg', 'Al', 'Mn', 'Zn', 'Cr', 'Fe', 'Sn', 'Pb', '(H)', 'Cu', 'Hg', 'Ag', 'Au']


def metal_activity() -> str:
    s = text(870, 50, 'Ряд активности металлов (в водной среде)', 'h', 'middle')
    x0, w, y = 60, 92, 230
    for k, sym in enumerate(SERIES):
        x = x0 + k * w
        fill = '#FCE3E4' if sym == '(H)' else ('#DCE3F2' if k < 13 else '#EDEAE3')
        s += f'<rect x="{x + 3}" y="{y}" width="{w - 6}" height="80" rx="10" fill="{fill}"/>'
        s += text(x + w / 2, y + 52, sym, 't', 'middle', RED if sym == '(H)' else INK)
    s += arrow(x0, y + 120, x0 + 18 * w, y + 120, GREY, 4)
    s += text(x0 + 9 * w, y + 160, 'восстановительная активность уменьшается', 's', 'middle')
    xh = x0 + 13.5 * w
    s += f'<line x1="{xh}" y1="{y - 120}" x2="{xh}" y2="{y - 6}" stroke="{RED}" stroke-width="4" stroke-dasharray="10 8"/><line x1="{xh}" y1="{y + 86}" x2="{xh}" y2="{y + 104}" stroke="{RED}" stroke-width="4"/>'

    def brace(a, b, yy, txt, col, up=True):
        xa, xb = x0 + a * w + 6, x0 + b * w - 6
        dy = -14 if up else 14
        return (f'<path d="M{xa} {yy} v {dy} H {xb} v {-dy}" fill="none" stroke="{col}" stroke-width="4"/>'
                + text((xa + xb) / 2, yy + (dy * 2 if up else dy * 3), chem(txt), 's', 'middle', col))
    s += brace(0, 5, y - 10, 'с водой при обычных условиях', BLUE)
    s += brace(5, 6, y - 70, 'Mg — при нагревании', ORANGE)
    s += brace(0, 13, y + 200, 'вытесняют H₂ из разбавленных кислот-неокислителей', GREEN, False)
    s += brace(14, 18, y + 200, 'H₂ не вытесняют', GREY, False)
    s += card(60, 520, 1660, 130)
    s += lines_at(890, 570, ['в растворе соли металл вытесняет металлы, стоящие правее (Fe + CuSO₄ → FeSO₄ + Cu);',
                             'Li, K, Ba, Ca, Na для этого не берут — они реагируют с водой раствора'], 's', step=40)
    return s


# 4. Получение металлов -----------------------------------------------------------------------
def metal_production() -> str:
    s = text(820, 50, 'Способы получения металлов', 'h', 'middle')
    cards = [
        (40, 'пирометаллургия', ORANGE, ['восстановление при', 'высокой температуре'],
         ['ZnO + C → Zn + CO', 'Fe₂O₃ + 3CO → 2Fe + 3CO₂', 'WO₃ + 3H₂ → W + 3H₂O', 'Cr₂O₃ + 2Al → 2Cr + Al₂O₃']),
        (570, 'гидрометаллургия', BLUE, ['металл переводят', 'в раствор и извлекают'],
         ['CuO + H₂SO₄ → CuSO₄ + H₂O', 'CuSO₄ + Fe → FeSO₄ + Cu']),
        (1100, 'электрометаллургия', GREEN, ['электролиз расплавов:', 'щелочные, щёлочноземельные, Al'],
         ['2KCl → 2K + Cl₂', '(расплав, электрический ток)']),
    ]
    for x, t, col, how, eqs in cards:
        s += card(x, 100, 500, 440, PAPER, col)
        s += text(x + 250, 150, t, 't', 'middle', col)
        s += lines_at(x + 250, 200, how, 's', step=32)
        s += lines_at(x + 250, 310, eqs, 's', step=46, color=INK)
    s += card(160, 580, 1320, 80, '#fff', INK)
    s += text(820, 632, chem('в основе всех способов: Meⁿ⁺ + ne⁻ → Me⁰ (восстановление)'), 't', 'middle')
    return s


# 5. Коррозионные пары ------------------------------------------------------------------------
def pair(x, left, right, anode_left, title, verdict):
    s = card(x, 90, 720, 470)
    s += text(x + 360, 135, title, 't', 'middle')
    s += f'<path d="M{x + 80} 380 Q {x + 360} 250 {x + 640} 380 Z" fill="#CFE3F3" opacity=".9"/>'
    s += text(x + 360, 345, 'капля электролита', 'cap', 'middle')
    s += f'<rect x="{x + 80}" y="380" width="280" height="70" fill="#B9BCC4" stroke="{INK}" stroke-width="2"/>'
    s += f'<rect x="{x + 360}" y="380" width="280" height="70" fill="{"#C88A57" if right == "Cu" else "#9FB0C8"}" stroke="{INK}" stroke-width="2"/>'
    s += text(x + 220, 425, left, 't', 'middle') + text(x + 500, 425, right, 't', 'middle')
    if anode_left:
        s += arrow(x + 300, 470, x + 420, 470, BLUE, 4) + text(x + 360, 505, 'e⁻', 's', 'middle', BLUE)
        s += text(x + 220, 225, chem('анод: Fe − 2e⁻ → Fe²⁺'), 's', 'middle', RED)
        s += arrow(x + 220, 360, x + 220, 245, RED, 3)
    else:
        s += arrow(x + 420, 470, x + 300, 470, BLUE, 4) + text(x + 360, 505, 'e⁻', 's', 'middle', BLUE)
        s += text(x + 500, 225, chem('анод: Zn − 2e⁻ → Zn²⁺'), 's', 'middle', RED)
        s += arrow(x + 500, 360, x + 500, 245, RED, 3)
    s += text(x + 360, 545, verdict, 's', 'middle', RED if anode_left else GREEN)
    return s


def metal_corrosion() -> str:
    s = text(780, 50, 'Коррозия в контакте металлов: разрушается более активный', 'h', 'middle')
    s += pair(40, 'Fe', 'Cu', True, 'железо в контакте с медью', 'железо разрушается быстрее')
    s += pair(800, 'Fe', 'Zn', False, 'железо в контакте с цинком', 'цинк разрушается, железо защищено')
    s += text(780, 610, 'Электроны идут по металлу от более активного металла к менее активному.', 's', 'middle')
    return s


# 6. Известковая вода и CO₂ ------------------------------------------------------------------
def tube(x, fill, cloudy=False, gas=False):
    s = (f'<path d="M{x} 130 V 400 Q {x} 450 {x + 50} 450 Q {x + 100} 450 {x + 100} 400 V 130" fill="none" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M{x + 4} 200 V 400 Q {x + 4} 446 {x + 50} 446 Q {x + 96} 446 {x + 96} 400 V 200 Z" fill="{fill}"/>')
    if cloudy:
        s += ''.join(f'<circle cx="{x + 15 + (k * 23) % 72}" cy="{215 + (k * 37) % 215}" r="5" fill="#fff" opacity=".9"/>' for k in range(30))
    if gas:
        s += ''.join(f'<circle cx="{x + 30 + (k % 3) * 20}" cy="{180 - (k // 3) * 30}" r="7" fill="none" stroke="{GREY}" stroke-width="2"/>' for k in range(6))
    return s


def limewater_carbon_dioxide() -> str:
    s = text(820, 50, chem('Известковая вода и CO₂: осадок появляется и исчезает'), 'h', 'middle')
    data = [(180, '#E8F1F8', False, False, 'прозрачная', 'Ca(OH)₂'),
            (580, '#D8DEE3', True, False, 'мутнеет', 'CaCO₃↓'),
            (980, '#E8F1F8', False, False, 'снова прозрачная', 'Ca(HCO₃)₂'),
            (1380, '#D8DEE3', True, True, 'снова осадок', 'CaCO₃↓ + CO₂↑')]
    for x, f, cl, g, t, sub in data:
        s += tube(x, f, cl, g)
        s += text(x + 50, 500, t, 't', 'middle') + text(x + 50, 538, chem(sub), 's', 'middle', BLUE)
    steps = [(300, '+ CO₂', 'Ca(OH)₂ + CO₂ → CaCO₃↓ + H₂O'), (700, '+ избыток CO₂', 'CaCO₃ + CO₂ + H₂O → Ca(HCO₃)₂'),
             (1100, 'нагревание', 'Ca(HCO₃)₂ → CaCO₃↓ + CO₂↑ + H₂O')]
    for x, a, eq in steps:
        s += arrow(x, 290, x + 260, 290, GREY, 5) + text(x + 130, 270, chem(a), 's', 'middle', RED)
    for j, (x, a, eq) in enumerate(steps):
        s += text(820, 600 + j * 40, chem(eq), 's', 'middle')
    return s


# 7. Жёсткость воды ---------------------------------------------------------------------------
def water_hardness() -> str:
    s = text(800, 50, chem('Жёсткость воды: ионы Ca²⁺ и Mg²⁺'), 'h', 'middle')
    s += card(40, 100, 740, 300, PAPER, ORANGE) + card(820, 100, 740, 300, PAPER, BLUE)
    s += text(410, 150, 'временная (карбонатная)', 't', 'middle', ORANGE)
    s += lines_at(410, 200, ['гидрокарбонаты Ca(HCO₃)₂, Mg(HCO₃)₂', 'устраняется кипячением:', 'Ca(HCO₃)₂ → CaCO₃↓ + CO₂↑ + H₂O'], 's', step=44)
    s += text(1190, 150, 'постоянная', 't', 'middle', BLUE)
    s += lines_at(1190, 200, ['хлориды и сульфаты Ca и Mg', '(CaCl₂, CaSO₄, MgCl₂, MgSO₄)', 'кипячением не устраняется'], 's', step=44)
    s += card(40, 430, 1520, 200, '#fff', INK)
    s += text(800, 475, 'устраняют оба вида:', 't', 'middle')
    s += lines_at(420, 530, ['сода Na₂CO₃ — осаждение', 'Ca²⁺ + CO₃²⁻ → CaCO₃↓'], 's', step=40)
    s += lines_at(1180, 530, ['катионит — обмен ионов', 'Ca²⁺, Mg²⁺ заменяются на Na⁺'], 's', step=40)
    s += text(800, 680, 'общая жёсткость = временная + постоянная', 's', 'middle', GREY)
    return s


if __name__ == '__main__':
    jobs = {
        'metal-periodic-table.png': (metal_periodic_table(), 1600, 780),
        'metal-lattice.png': (metal_lattice(), 1600, 650),
        'metal-activity.png': (metal_activity(), 1780, 680),
        'metal-production.png': (metal_production(), 1640, 690),
        'metal-corrosion.png': (metal_corrosion(), 1560, 640),
        'limewater-carbon-dioxide.png': (limewater_carbon_dioxide(), 1640, 720),
        'water-hardness.png': (water_hardness(), 1600, 710),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
