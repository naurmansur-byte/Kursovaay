"""Рисунки недели 10 химии (course/week-10/pics/*.png): электродный потенциал, ряд напряжений, элемент Даниэля — Якоби,
свинцовый аккумулятор, электролиз CuCl₂, правила продуктов электролиза, электролиз раствора NaCl.

Факты — по выжимке course/textbooks/chem-10-electrolysis.md (Х10-1 § 47–51). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w10.py
"""
from __future__ import annotations

from common import GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-10' / 'pics'
BLUE, WATER, METAL, CU, PB = '#3A57A7', '#E4EEF8', '#9AA3AD', '#C46A3A', '#6E7480'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def beaker(x, y, w, h, fill=WATER, level=0.25):
    s = f'<rect x="{x}" y="{y + h * level}" width="{w}" height="{h * (1 - level)}" fill="{fill}"/>'
    return s + f'<path d="M{x} {y} V {y + h} H {x + w} V {y}" fill="none" stroke="{INK}" stroke-width="4"/>'


def plate(x, y, w, h, fill, label=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
    if label:
        s += text(x + w / 2, y - 12, chem(label), 't', 'middle')
    return s


def ion(x, y, s, col):
    return f'<circle cx="{x}" cy="{y}" r="28" fill="#fff" stroke="{col}" stroke-width="3"/>' + text(x, y + 8, chem(s), 'cap', 'middle', col)


def battery(cx, y):
    """Внешний источник тока: длинная черта +, короткая −."""
    return (f'<rect x="{cx - 30}" y="{y - 30}" width="60" height="60" fill="#fff"/>'
            f'<path d="M{cx - 10} {y - 28} V {y + 28} M{cx + 10} {y - 14} V {y + 14}" stroke="{INK}" stroke-width="6"/>')


# 1. Электродный потенциал --------------------------------------------------------------------------
def electrode_potential() -> str:
    s = text(750, 56, 'Электродный потенциал и водородный электрод', 'h', 'middle')
    s += beaker(80, 130, 480, 400)
    s += plate(280, 110, 70, 360, METAL, 'металл')
    for k in range(6):
        y = 250 + k * 36
        s += text(268, y + 8, '−', 't', 'middle', BLUE) + text(362, y + 8, '−', 't', 'middle', BLUE)
        s += f'<circle cx="225" cy="{y}" r="15" fill="#fff" stroke="{RED}" stroke-width="3"/>' + text(225, y + 7, '+', 'cap', 'middle', RED)
        s += f'<circle cx="405" cy="{y}" r="15" fill="#fff" stroke="{RED}" stroke-width="3"/>' + text(405, y + 7, '+', 'cap', 'middle', RED)
    s += text(320, 580, chem('Me⁰ ⇄ Meⁿ⁺ + ne⁻'), 't', 'middle')
    s += lines_at(320, 625, ['двойной электрический слой:', 'электроны на металле, катионы в растворе'], 'cap')
    # водородный электрод
    s += beaker(820, 130, 480, 400)
    s += plate(1030, 250, 60, 200, '#D8DCE2', 'Pt')
    s += f'<path d="M1000 110 V 380 Q 1000 420 1030 420" fill="none" stroke="{GREY}" stroke-width="10"/>'
    for k in range(6):
        s += f'<circle cx="{1040 + (k % 2) * 30}" cy="{430 - k * 30}" r="7" fill="#fff" stroke="{BLUE}" stroke-width="2"/>'
    s += text(940, 110, chem('H₂'), 't', 'end', BLUE)
    s += text(1060, 505, chem('[H⁺] = 1 моль/л'), 's', 'middle')
    s += text(1060, 580, 'E° = 0 В (принято)', 't', 'middle', RED)
    s += lines_at(1060, 625, ['стандарт для сравнения;', 'платина в реакции не участвует'], 'cap')
    return s


# 2. Ряд напряжений -------------------------------------------------------------------------------
def voltage_series() -> str:
    s = text(800, 56, 'Электрохимический ряд напряжений металлов', 'h', 'middle')
    row = [('Li', '−3,05'), ('K', '−2,92'), ('Ba', '−2,90'), ('Ca', '−2,87'), ('Na', '−2,71'), ('Mg', '−2,36'), ('Al', '−1,66'),
           ('Mn', '−1,18'), ('Zn', '−0,76'), ('Cr', '−0,74'), ('Fe', '−0,44'), ('Ni', '−0,25'), ('Sn', ''), ('Pb', ''), ('H', '0'),
           ('Cu', '+0,34'), ('Hg', ''), ('Ag', '+0,80'), ('Au', '')]
    w = 80
    x0 = 40
    for k, (el, e) in enumerate(row):
        x = x0 + k * w
        fill = '#FDECEC' if el == 'H' else ('#EAF1E4' if k > 14 else '#fff')
        s += f'<rect x="{x}" y="160" width="{w - 6}" height="80" rx="10" fill="{fill}" stroke="{RED if el == "H" else INK}" stroke-width="{3 if el == "H" else 2}"/>'
        s += text(x + (w - 6) / 2, 212, el, 't', 'middle', RED if el == 'H' else INK)
        if e:
            s += text(x + (w - 6) / 2, 275, e, 'cap', 'middle', INK)
    s += text(40, 140, 'E°, В', 'cap', 'start')
    s += arrow(60, 330, 1540, 330, INK, 5) + text(800, 365, 'E° растёт → восстановительная активность металлов уменьшается', 's', 'middle')
    xh = x0 + 14 * w
    s += f'<path d="M{x0} 420 H {xh - 10}" stroke="{BLUE}" stroke-width="4"/><path d="M{x0} 410 V 430 M{xh - 10} 410 V 430" stroke="{BLUE}" stroke-width="4"/>'
    s += text((x0 + xh) / 2, 460, 'E° < 0: вытесняют водород из кислот', 's', 'middle', BLUE)
    s += f'<path d="M{x0} 500 H {x0 + 5 * w - 10}" stroke="{RED}" stroke-width="4"/>'
    s += text(x0, 535, 'Li … Na: в водном растворе', 'cap', 'start', RED) + text(x0, 563, 'прежде всего реагируют с водой', 'cap', 'start', RED)
    s += text(1160, 500, 'Металл вытесняет из солей металлы,', 's', 'middle') + text(1160, 535, 'стоящие правее (с большим E°)', 's', 'middle')
    s += text(1160, 563, chem('Fe + CuSO₄ = FeSO₄ + Cu'), 'cap', 'middle')
    return s


# 3. Элемент Даниэля — Якоби ---------------------------------------------------------------------------
def daniell_cell() -> str:
    s = text(750, 56, 'Гальванический элемент Даниэля — Якоби', 'h', 'middle')
    s += beaker(300, 220, 900, 380, level=0.2)
    s += f'<path d="M750 296 V 600" stroke="{GREY}" stroke-width="10" stroke-dasharray="12 8"/>'
    s += text(750, 640, 'пористая перегородка', 'cap', 'middle')
    s += plate(440, 180, 70, 330, METAL, 'Zn') + plate(990, 180, 70, 330, CU, 'Cu')
    s += text(520, 580, chem('ZnSO₄'), 's', 'middle') + text(980, 580, chem('CuSO₄'), 's', 'middle')
    s += f'<path d="M475 180 V 120 H 1025 V 180" fill="none" stroke="{INK}" stroke-width="4"/>'
    s += f'<circle cx="750" cy="120" r="26" fill="#F7D23E" stroke="{INK}" stroke-width="4"/>'
    for x in (560, 640, 840, 920):
        s += arrow(x, 100, x + 50, 100, BLUE, 4)
    s += text(625, 80, chem('e⁻'), 's', 'middle', BLUE) + text(905, 80, chem('e⁻'), 's', 'middle', BLUE)
    s += ion(600, 380, 'Zn²⁺', RED) + arrow(520, 380, 568, 380, RED, 3)
    s += ion(900, 420, 'Cu²⁺', RED) + arrow(932, 420, 982, 420, RED, 3)
    s += arrow(840, 480, 670, 480, BLUE, 4) + text(755, 515, chem('SO₄²⁻ → к аноду'), 'cap', 'middle', BLUE)
    s += lines_at(150, 300, ['анод (−)', 'окисление:', 'Zn⁰ − 2e⁻ → Zn²⁺'], 's', 'middle', 36, None)
    s += lines_at(1350, 300, ['катод (+)', 'восстановление:', 'Cu²⁺ + 2e⁻ → Cu⁰'], 's', 'middle', 36, None)
    s += text(750, 700, chem('Zn | ZnSO₄ || CuSO₄ | Cu;  Zn + Cu²⁺ = Zn²⁺ + Cu;  ЭДС = E(катода) − E(анода)'), 't', 'middle')
    return s


# 4. Свинцовый аккумулятор ------------------------------------------------------------------------
def lead_panel(x, title, charge):
    s = text(x + 340, 95, title, 't', 'middle', RED if charge else INK)
    s += beaker(x + 100, 200, 480, 320, '#EEF3E6', 0.2)
    s += plate(x + 200, 180, 60, 280, PB) + plate(x + 420, 180, 60, 280, '#5A3E2B')
    s += text(x + 230, 495, chem('PbSO₄ → Pb' if charge else 'Pb'), 's', 'middle')
    s += text(x + 450, 495, chem('PbSO₄ → PbO₂' if charge else 'PbO₂'), 's', 'middle')
    s += text(x + 340, 400, chem('H₂SO₄'), 's', 'middle')
    s += f'<path d="M{x + 230} 180 V 150 H {x + 450} V 180" fill="none" stroke="{INK}" stroke-width="4"/>'
    if charge:
        s += battery(x + 340, 150)
        s += lines_at(x + 340, 570, ['катод: PbSO₄ + 2e⁻ → Pb + SO₄²⁻', 'анод: PbSO₄ + 2H₂O − 2e⁻ → PbO₂ + SO₄²⁻ + 4H⁺',
                                    'ток — от внешнего источника;', 'электрическая энергия → химическая'], 's')
    else:
        s += f'<circle cx="{x + 340}" cy="150" r="22" fill="#F7D23E" stroke="{INK}" stroke-width="3"/>'
        s += arrow(x + 255, 134, x + 300, 134, BLUE, 3) + arrow(x + 380, 134, x + 425, 134, BLUE, 3)
        s += text(x + 240, 128, chem('e⁻'), 's', 'middle', BLUE) + text(x + 440, 128, chem('e⁻'), 's', 'middle', BLUE)
        s += lines_at(x + 340, 570, ['Pb + PbO₂ + 2SO₄²⁻ + 4H⁺ → 2PbSO₄ + 2H₂O', 'электроны идут от Pb к PbO₂;', 'химическая энергия → электрическая'], 's')
    return s


def lead_battery() -> str:
    s = text(800, 50, 'Свинцовый аккумулятор: разрядка и зарядка', 'h', 'middle')
    s += lead_panel(40, 'Разрядка', False) + lead_panel(820, 'Зарядка', True)
    s += f'<path d="M800 160 V 640" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 8"/>'
    return s


# 5. Электролиз CuCl₂ ---------------------------------------------------------------------------
def cell(x, y, w, h, sol, left_label, right_label):
    s = beaker(x, y, w, h, level=0.2)
    s += plate(x + w * 0.22, y - 40, 44, h * 0.8, '#3C3C3C') + plate(x + w * 0.72, y - 40, 44, h * 0.8, '#3C3C3C')
    lx, rx = x + w * 0.22 + 22, x + w * 0.72 + 22
    s += f'<path d="M{lx} {y - 40} V {y - 100} H {rx} V {y - 40}" fill="none" stroke="{INK}" stroke-width="4"/>' + battery((lx + rx) / 2, y - 100)
    s += text(lx, y - 115, '−', 'h', 'middle', BLUE) + text(rx, y - 115, '+', 'h', 'middle', RED)
    s += text(x + w / 2, y + h - 20, chem(sol), 's', 'middle')
    s += lines_at(lx, y + h + 50, left_label, 's')
    s += lines_at(rx, y + h + 50, right_label, 's')
    return s, lx, rx


def cucl2_electrolysis() -> str:
    s = text(700, 56, chem('Электролиз раствора CuCl₂ (инертные электроды)'), 'h', 'middle')
    c, lx, rx = cell(250, 260, 900, 330, 'CuCl₂ ⇄ Cu²⁺ + 2Cl⁻', ['катод (−): восстановление', 'Cu²⁺ + 2e⁻ → Cu⁰ (медь)'],
                     ['анод (+): окисление', '2Cl⁻ − 2e⁻ → Cl₂ (хлор)'])
    s += c
    s += f'<rect x="{lx - 26}" y="300" width="52" height="200" fill="none" stroke="{CU}" stroke-width="8"/>'
    for k in range(5):
        s += f'<circle cx="{rx + (k % 2) * 16 - 8}" cy="{480 - k * 36}" r="8" fill="#E9F5C8" stroke="#7A8F2A" stroke-width="2"/>'
    s += ion(640, 420, 'Cu²⁺', RED) + arrow(615, 420, lx + 40, 420, RED, 3)
    s += ion(760, 470, 'Cl⁻', BLUE) + arrow(785, 470, rx - 40, 470, BLUE, 3)
    s += text(700, 760, chem('Суммарно: CuCl₂ → Cu + Cl₂ (энергия — от внешнего источника)'), 't', 'middle')
    return s


# 6. Правила продуктов -----------------------------------------------------------------------------
def product_rules() -> str:
    s = text(800, 56, 'Что выделяется при электролизе водных растворов', 'h', 'middle')
    s += text(400, 125, 'Катод (−): по катиону металла', 't', 'middle', BLUE)
    groups = [('Li, K, Ca, Na, Mg, Al', 'только H₂ из воды', '2H₂O + 2e⁻ → H₂ + 2OH⁻', '#FDECEC'),
              ('Mn, Zn, Fe, Ni, Sn, Pb', 'металл и H₂', 'Zn²⁺ + 2e⁻ → Zn и H₂', '#FFF4D6'),
              ('Cu, Hg, Ag, Pt, Au', 'только металл', 'Cu²⁺ + 2e⁻ → Cu', '#EAF1E4')]
    for k, (els, res, eq, fill) in enumerate(groups):
        y = 160 + k * 150
        s += f'<rect x="60" y="{y}" width="680" height="130" rx="16" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        s += text(90, y + 45, els, 't') + text(90, y + 85, chem(res), 's', 'start', RED) + text(90, y + 117, chem(eq), 'cap', 'start', INK)
    s += text(400, 650, 'в смеси первым восстанавливается металл правее в ряду', 'cap', 'middle')
    s += text(1200, 125, 'Анод (+), инертный: по аниону', 't', 'middle', RED)
    an = ['I⁻', 'Br⁻', 'S²⁻', 'Cl⁻', 'H₂O', 'F⁻', 'SO₄²⁻', 'NO₃⁻', 'PO₄³⁻']
    for k, a in enumerate(an):
        x = 830 + k * 80
        fill = '#FDECEC' if a == 'H₂O' else ('#fff' if k < 4 else '#EEF1F5')
        s += f'<rect x="{x}" y="170" width="72" height="70" rx="10" fill="{fill}" stroke="{INK}" stroke-width="2"/>' + text(x + 36, 214, chem(a), 's', 'middle')
    s += arrow(840, 280, 1540, 280, INK, 4) + text(1190, 315, 'способность окисляться убывает', 'cap', 'middle')
    s += f'<rect x="830" y="350" width="330" height="200" rx="16" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    s += lines_at(995, 395, ['до воды:', 'окисляется сам анион', '2Cl⁻ − 2e⁻ → Cl₂', '(I₂, Br₂, S)'], 's', step=36)
    s += f'<rect x="1190" y="350" width="370" height="200" rx="16" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    s += lines_at(1375, 395, ['после воды:', 'анион не окисляется,', 'окисляется вода:', '2H₂O − 4e⁻ → O₂ + 4H⁺'], 's', step=36)
    s += text(1190, 650, chem('Li … Al — только электролизом расплавов'), 'cap', 'middle')
    return s


# 7. Электролиз раствора NaCl ----------------------------------------------------------------------
def nacl_electrolysis() -> str:
    s = text(700, 56, 'Электролиз раствора NaCl', 'h', 'middle')
    c, lx, rx = cell(250, 260, 900, 330, 'NaCl → Na⁺ + Cl⁻;  вода', ['катод (−):', '2H₂O + 2e⁻ → H₂ + 2OH⁻'], ['анод (+):', '2Cl⁻ − 2e⁻ → Cl₂'])
    s += c
    for k in range(5):
        s += f'<circle cx="{lx + (k % 2) * 16 - 8}" cy="{480 - k * 36}" r="8" fill="#fff" stroke="{BLUE}" stroke-width="2"/>'
        s += f'<circle cx="{rx + (k % 2) * 16 - 8}" cy="{480 - k * 36}" r="8" fill="#E9F5C8" stroke="#7A8F2A" stroke-width="2"/>'
    s += text(lx + 60, 305, chem('H₂'), 't', 'start', BLUE) + text(rx - 60, 305, chem('Cl₂'), 't', 'end', '#5E7A1A')
    s += ion(lx + 110, 430, 'Na⁺', RED) + ion(lx + 180, 390, 'OH⁻', BLUE)
    s += text(lx + 145, 500, 'у катода — NaOH', 'cap', 'middle', BLUE)
    s += text(700, 760, chem('2NaCl + 2H₂O → H₂ + Cl₂ + 2NaOH;  Na⁺ в растворе не восстанавливается'), 't', 'middle')
    s += text(700, 800, chem('Сравни: из расплава NaCl — Na и Cl₂'), 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'electrode-potential.png': (electrode_potential(), 1500, 670),
        'voltage-series.png': (voltage_series(), 1600, 600),
        'daniell-cell.png': (daniell_cell(), 1500, 730),
        'lead-battery.png': (lead_battery(), 1600, 690),
        'cucl2-electrolysis.png': (cucl2_electrolysis(), 1400, 790),
        'product-rules.png': (product_rules(), 1600, 680),
        'nacl-electrolysis.png': (nacl_electrolysis(), 1400, 830),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
