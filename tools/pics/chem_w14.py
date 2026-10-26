"""Рисунки недели 14 химии (course/week-14/pics/*.png): оксидная плёнка Al, амфотерность Al(OH)₃, d-блок и «провал» электрона,
оксиды хрома, строение комплекса K₄[Fe(CN)₆], доменная печь, цвета гидроксидов.

Факты — по выжимке course/textbooks/chem-14-al-transition.md (Х9-1 § 27, Х11-2 § 60–61, Х9-1 § 11). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w14.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-14' / 'pics'
BLUE, ORANGE, AL, FILM = '#3A57A7', '#D98A2B', '#C9CED6', '#E8B33A'
WATER, ACID, ALK = '#DCEBF5', '#F8DEDF', '#E6DDF3'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER, stroke=None):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"{st}/>'


def beaker(cx, base, w, h, level, fill):
    x0, top = cx - w / 2, base - h
    lh = h * level
    return (f'<rect x="{x0 + 5:.0f}" y="{base - lh:.0f}" width="{w - 10:.0f}" height="{lh - 5:.0f}" rx="10" fill="{fill}"/>'
            f'<path d="M{x0 - 10:.0f} {top:.0f} H{x0:.0f} V{base - 14:.0f} a14 14 0 0 0 14 14 H{x0 + w - 14:.0f} a14 14 0 0 0 14 -14 '
            f'V{top:.0f} H{x0 + w + 10:.0f}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')


def bubbles(cx, y0, n=5, spread=40):
    return ''.join(f'<circle cx="{cx + (k % 3 - 1) * spread / 2 + (k * 7) % 11:.0f}" cy="{y0 - k * 26}" r="{7 + k % 3 * 2}" fill="#fff" stroke="{BLUE}" stroke-width="2.5"/>'
                   for k in range(n))


def tube(cx, top, fill, sediment=None, h=230, sed_h=70):
    s = f'<path d="M{cx - 30} {top} V {top + h - 30} A 30 30 0 0 0 {cx + 30} {top + h - 30} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if sediment:
        s += (f'<path d="M{cx - 30} {top + h - sed_h} V {top + h - 30} A 30 30 0 0 0 {cx + 30} {top + h - 30} V {top + h - sed_h} Z" '
              f'fill="{sediment}" stroke="{INK}" stroke-width="2"/>')
    return s


# 1. Оксидная плёнка алюминия ---------------------------------------------------------------------
def al_plate(cx, base, film=True, thick=False, broken=False):
    s = f'<rect x="{cx - 26}" y="{base - 150}" width="52" height="150" fill="{AL}" stroke="{INK}" stroke-width="3"/>'
    if film:
        w = 10 if thick else 6
        dash = ' stroke-dasharray="16 10"' if broken else ''
        s += f'<rect x="{cx - 26 - w / 2}" y="{base - 150 - w / 2}" width="{52 + w}" height="{150 + w}" fill="none" stroke="{FILM}" stroke-width="{w}"{dash}/>'
    return s


def al_oxide_film() -> str:
    s = text(900, 52, 'Алюминий и его оксидная плёнка', 'h', 'middle')
    xs = [230, 670, 1110, 1550]
    panels = [
        (['В воде'], WATER, dict(film=True), ['плёнка Al₂O₃ цела —', 'реакции не видно', '(даже в кипящей воде)'], None),
        (['Плёнку нарушили'], WATER, dict(film=True, broken=True), ['2Al + 6H₂O →', '2Al(OH)₃ + 3H₂↑'], 'gas'),
        (['Разбавленные', 'HCl, H₂SO₄'], ACID, dict(film=False), ['2Al + 6HCl →', '2AlCl₃ + 3H₂↑'], 'gas'),
        (['Концентрированные', 'H₂SO₄, HNO₃'], ACID, dict(film=True, thick=True), ['пассивация: прочная', 'плёнка — кислоты', 'возят в Al-цистернах'], None),
    ]
    for x, (title, fill, kw, rows, gas) in zip(xs, panels):
        s += card(x - 205, 90, 410, 620)
        s += lines_at(x, 140, title, 't', step=38)
        s += beaker(x, 470, 220, 250, 0.8, fill) + al_plate(x, 455, **kw)
        if gas:
            s += bubbles(x + 55, 400) + bubbles(x - 60, 380, 4)
        s += lines_at(x, 545, rows, 's', step=36, color=RED if gas else INK)
    s += f'<rect x="80" y="745" width="40" height="20" fill="none" stroke="{FILM}" stroke-width="6"/>' + text(135, 763, chem('жёлтым — плёнка Al₂O₃'), 's')
    s += text(1720, 763, 'Без плёнки алюминий активен; плёнка защищает его от воды и концентрированных кислот', 'cap', 'end')
    return s


# 2. Амфотерность Al(OH)₃ ------------------------------------------------------------------------
def al_hydroxide_amphoterism() -> str:
    s = text(900, 52, chem('Al(OH)₃ — амфотерный гидроксид'), 'h', 'middle')
    # исходный раствор → осадок
    s += card(60, 100, 420, 560) + text(270, 150, chem('AlCl₃ + NaOH'), 't', 'middle') + text(270, 186, 'по каплям', 'cap', 'middle')
    s += tube(270, 230, '#F7F7F7', '#DADADA', h=260, sed_h=90) + text(345, 440, 'осадок', 'cap')
    s += lines_at(270, 560, ['AlCl₃ + 3NaOH →', 'Al(OH)₃↓ + 3NaCl', 'белый осадок'], 's', step=34)
    s += arrow(490, 300, 620, 220, GREY, 5) + text(520, 225, chem('+ HCl'), 's', 'middle')
    s += arrow(490, 460, 620, 560, GREY, 5) + text(590, 480, '+ NaOH', 's', 'middle')
    # с кислотой
    s += card(640, 100, 1100, 250, '#fff', RED)
    s += tube(730, 125, ACID, h=200) + text(820, 175, 'В избытке кислоты осадок растворяется', 't')
    s += text(820, 230, chem('Al(OH)₃ + 3HCl → AlCl₃ + 3H₂O'), 't', 'start', RED)
    s += text(820, 280, chem('Al(OH)₃ + 3H⁺ → Al³⁺ + 3H₂O  — свойства основания'), 's')
    # со щёлочью
    s += card(640, 420, 1100, 250, '#fff', BLUE)
    s += tube(730, 445, ALK, h=200) + text(820, 495, 'В избытке щёлочи осадок растворяется', 't')
    s += text(820, 550, chem('Al(OH)₃ + NaOH → Na[Al(OH)₄]'), 't', 'start', BLUE)
    s += text(820, 600, chem('в растворе — гидроксокомплекс; при сплавлении — NaAlO₂'), 's')
    s += text(900, 720, 'Осадок Al(OH)₃ выпадает, а в избытке кислоты или щёлочи растворяется.', 's', 'middle')
    return s


# 3. d-блок и «провал» электрона ------------------------------------------------------------------
ROW4 = ['K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr']


def d_block() -> str:
    s = text(900, 52, '4-й период: s-, d- и p-элементы', 'h', 'middle')
    x0, w, y = 70, 92, 120
    for k, el in enumerate(ROW4):
        blk = 's' if k < 2 else 'd' if k < 12 else 'p'
        fill = {'s': '#F8DEDF', 'd': '#DCE6F7', 'p': '#F7EFC8'}[blk]
        stroke = RED if el in ('Cr', 'Cu') else INK
        sw = 6 if el in ('Cr', 'Cu', 'Zn') else 2
        s += f'<rect x="{x0 + k * w}" y="{y}" width="{w - 6}" height="90" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        s += text(x0 + k * w + (w - 6) / 2, y + 58, el, 't', 'middle')
    for a, b, lab, col in ((0, 2, 's-элементы', RED), (2, 12, 'd-элементы (переходные металлы): заполняется 3d', BLUE), (12, 18, 'p-элементы', ORANGE)):
        s += f'<line x1="{x0 + a * w}" y1="{y + 110}" x2="{x0 + b * w - 6}" y2="{y + 110}" stroke="{col}" stroke-width="5"/>'
        s += text(x0 + (a + b) * w / 2, y + 145, lab, 's', 'middle', col)

    def boxes(x, yy, d, s4, title, note, col):
        out = card(x, yy, 760, 220, '#fff', col) + text(x + 30, yy + 50, title, 't', 'start', col)
        for i in range(5):
            bx = x + 40 + i * 66
            out += f'<rect x="{bx}" y="{yy + 90}" width="60" height="60" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            arr = d[i]
            out += ''.join(text(bx + 18 + j * 24, yy + 132, '↑' if j == 0 else '↓', 't', 'middle') for j in range(arr))
        out += text(x + 40 + 165, yy + 182, '3d', 's', 'middle')
        bx = x + 440
        out += f'<rect x="{bx}" y="{yy + 90}" width="60" height="60" fill="#fff" stroke="{INK}" stroke-width="3"/>'
        out += text(bx + 30, yy + 132, '↑' if s4 == 1 else '↑↓', 't', 'middle') + text(bx + 30, yy + 182, '4s', 's', 'middle')
        out += lines_at(x + 640, yy + 115, note, 's', step=34)
        return out
    s += boxes(60, 330, [1, 1, 1, 1, 1], 1, chem('Cr: 3d⁵4s¹ (не 3d⁴4s²)'), ['один электрон', 'с 4s на 3d —', '«провал»'], RED)
    s += boxes(880, 330, [2, 2, 2, 2, 2], 1, chem('Cu: 3d¹⁰4s¹ (не 3d⁹4s²)'), ['3d заполнен', 'полностью —', '«провал»'], RED)
    s += card(60, 580, 1640, 120, '#F3F0E8')
    s += text(90, 625, chem('Степени окисления переменные: Cr +2, +3, +6; Cu +1, +2; высшая — по номеру группы (Mn до +7).'), 's')
    s += text(90, 670, chem('Zn: 3d¹⁰4s² — d-элемент с заполненным d-подуровнем, степень окисления только +2.'), 's', 'start', BLUE)
    return s


# 4. Оксиды хрома -----------------------------------------------------------------------------------
def chromium_oxides() -> str:
    s = text(870, 52, 'Оксиды хрома: степень окисления и свойства', 'h', 'middle')
    data = [('CrO', '+2', 'основный', RED, ['CrO и Cr(OH)₂ —', 'основные']),
            ('Cr₂O₃', '+3', 'амфотерный', ORANGE, ['Cr₂O₃ и Cr(OH)₃ —', 'амфотерные']),
            ('CrO₃', '+6', 'кислотный', BLUE, ['CrO₃, H₂CrO₄, H₂Cr₂O₇ —', 'кислотные'])]
    for k, (f, ox, kind, col, rows) in enumerate(data):
        x = 90 + k * 560
        s += card(x, 110, 500, 430, '#fff', col)
        s += text(x + 250, 220, chem(f), 'f', 'middle')
        s += f'<rect x="{x + 170}" y="{250}" width="160" height="56" rx="28" fill="{col}"/>' + text(x + 250, 290, chem(f'Cr {ox}'), 't', 'middle', '#fff')
        s += text(x + 250, 370, kind, 'h', 'middle', col)
        s += lines_at(x + 250, 440, rows, 's')
    s += arrow(150, 610, 1580, 610, INK, 6)
    s += text(865, 660, 'степень окисления растёт: основные свойства ослабевают, кислотные усиливаются', 't', 'middle')
    return s


# 5. Строение комплекса K₄[Fe(CN)₆] ---------------------------------------------------------------------
def complex_spheres() -> str:
    s = text(870, 52, chem('Строение комплексной соли K₄[Fe(CN)₆]'), 'h', 'middle')
    cx, cy = 560, 430
    s += f'<rect x="{cx - 270}" y="{cy - 270}" width="540" height="540" rx="40" fill="#EEF3FB" stroke="{BLUE}" stroke-width="5" stroke-dasharray="18 10"/>'
    for k in range(6):
        a = math.radians(90 + k * 60)
        x, y = cx + 175 * math.cos(a), cy - 175 * math.sin(a)
        s += f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{GREY}" stroke-width="4"/>'
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="48" fill="#fff" stroke="{GREEN}" stroke-width="4"/>' + text(x, y + 10, chem('CN⁻'), 's', 'middle', GREEN)
    s += f'<circle cx="{cx}" cy="{cy}" r="62" fill="{RED}"/>' + text(cx, cy + 12, chem('Fe²⁺'), 't', 'middle', '#fff')
    for (x, y) in ((190, 170), (930, 170), (190, 700), (930, 700)):
        s += f'<circle cx="{x}" cy="{y}" r="42" fill="#F7EFC8" stroke="{ORANGE}" stroke-width="4"/>' + text(x, y + 10, chem('K⁺'), 's', 'middle', ORANGE)
    rows = [
        (RED, 'комплексообразователь — ион Fe²⁺'),
        (GREEN, 'лиганды — 6 ионов CN⁻ (координационное число 6)'),
        (BLUE, 'внутренняя сфера — [Fe(CN)₆]⁴⁻: +2 + 6·(−1) = −4'),
        (ORANGE, 'внешняя сфера — 4 иона K⁺'),
    ]
    for k, (col, t) in enumerate(rows):
        y = 230 + k * 110
        s += f'<rect x="1040" y="{y - 30}" width="34" height="34" rx="6" fill="{col}"/>' + text(1095, y, chem(t), 's')
    s += card(1040, 680, 660, 110, '#F3F0E8')
    s += text(1370, 725, chem('В воде: K₄[Fe(CN)₆] → 4K⁺ + [Fe(CN)₆]⁴⁻'), 's', 'middle')
    s += text(1370, 768, 'гексацианоферрат(II) калия, «жёлтая кровяная соль»', 'cap', 'middle')
    return s


# 6. Доменная печь -----------------------------------------------------------------------------------
def blast_furnace() -> str:
    s = text(900, 52, 'Доменная печь: получение чугуна', 'h', 'middle')
    # корпус: шире к середине, сужается книзу
    pts = [(470, 150), (650, 150), (760, 560), (720, 760), (720, 900), (400, 900), (400, 760), (360, 560)]
    s += f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="#F3E3C8" stroke="{INK}" stroke-width="5"/>'
    s += f'<rect x="403" y="830" width="314" height="67" fill="#E06A3A"/>' + text(560, 875, 'чугун', 't', 'middle', '#fff')
    s += f'<rect x="403" y="785" width="314" height="45" fill="#B7A27A"/>' + text(560, 817, 'шлак', 's', 'middle')
    # загрузка и газ
    s += arrow(560, 125, 560, 150, INK, 5) + text(560, 112, 'руда, кокс, флюс (известняк)', 's', 'middle')
    s += arrow(650, 160, 770, 135, GREY, 4) + text(790, 140, 'колошниковый газ', 's')
    for y in (700, 740):
        s += arrow(260, y, 395, y, BLUE, 5)
    s += text(250, 690, 'воздух,', 's', 'end', BLUE) + text(250, 725, 'обогащённый O₂', 's', 'end', BLUE)
    s += arrow(720, 880, 860, 880, '#E06A3A', 5) + arrow(720, 806, 860, 806, '#8A7650', 4)
    # подписи процессов (справа)
    rows = [
        (230, 'Сверху вниз опускается шихта, навстречу снизу поднимается CO:', INK),
        (290, '3Fe₂O₃ + CO → 2Fe₃O₄ + CO₂', BLUE),
        (340, 'Fe₃O₄ + CO → 3FeO + CO₂', BLUE),
        (390, 'FeO + CO → Fe + CO₂', BLUE),
        (450, 'при 900–1000 °C и коксом: FeO + C → Fe + CO', BLUE),
        (520, 'Флюс: CaCO₃ → CaO + CO₂;  CaO + SiO₂ → CaSiO₃ (шлак)', ORANGE),
        (590, 'Fe + C → цементит Fe₃C; науглероженное железо', RED),
        (630, 'плавится около 1200 °C — жидкий чугун', RED),
        (720, 'Внизу горит кокс: C + O₂ → CO₂;  CO₂ + C → 2CO', INK),
    ]
    for y, t, col in rows:
        s += text(900, y, chem(t), 's', 'start', col)
    s += text(900, 806, 'шлак легче — сверху, защищает чугун от окисления', 'cap')
    s += text(900, 880, 'чугун — основной продукт', 'cap')
    s += text(900, 940, 'Восстановитель — CO (и кокс), не CO₂. Флюс нужен, чтобы пустая порода ушла в шлак.', 's', 'middle')
    return s


# 7. Цвета гидроксидов -----------------------------------------------------------------------------------
def hydroxide_colours() -> str:
    s = text(800, 52, 'Цвета осадков гидроксидов (повторение)', 'h', 'middle')
    data = [('Cu(OH)₂', 'голубой', '#7FB3E6', 'Cu²⁺ + 2OH⁻ → Cu(OH)₂↓'),
            ('Fe(OH)₂', 'зеленоватый (свежий)', '#9CC59A', 'Fe²⁺ + 2OH⁻ → Fe(OH)₂↓'),
            ('Fe(OH)₃', 'бурый', '#9B5A2E', 'Fe³⁺ + 3OH⁻ → Fe(OH)₃↓')]
    for k, (f, colname, col, eq) in enumerate(data):
        x = 280 + k * 520
        s += card(x - 230, 100, 460, 600)
        s += tube(x, 150, '#F4F7FA', col, h=300, sed_h=120)
        s += text(x, 520, chem(f), 'f', 'middle')
        s += text(x, 580, colname, 't', 'middle')
        s += text(x, 640, chem(eq), 's', 'middle')
    s += text(800, 760, 'Осадки получают действием щёлочи на растворы солей.', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'al-oxide-film.png': (al_oxide_film(), 1780, 790),
        'al-hydroxide-amphoterism.png': (al_hydroxide_amphoterism(), 1800, 760),
        'd-block.png': (d_block(), 1760, 730),
        'chromium-oxides.png': (chromium_oxides(), 1740, 700),
        'complex-spheres.png': (complex_spheres(), 1760, 820),
        'blast-furnace.png': (blast_furnace(), 1800, 980),
        'hydroxide-colours.png': (hydroxide_colours(), 1600, 800),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
