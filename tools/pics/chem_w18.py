"""Рисунки недели 18 химии (course/week-18/pics/*.png): этилен и цис-транс, правило Марковникова, обесцвечивание
бромной воды и KMnO₄, полимеризация, вулканизация, ацетилен, бензол и ксилолы, ректификационная колонна,
крекинг и коксование, справочная карта условий.

Факты — по выжимке course/textbooks/chem-18-unsaturated-arenes-oil.md (Х9-2 § 56–62; Х10-2 § 70–82; Х11-1 § 1–3).
Схемы условные. Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w18.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = chem(s).replace('ₙ', '<tspan baseline-shift="-0.28em" font-size="68%">n</tspan>')
    return _text(x, y, s, cls, anchor, fill)

OUT = ROOT / 'course' / 'week-18' / 'pics'
BLUE, ORANGE, PURPLE = '#3A57A7', '#D98A2B', '#8E44AD'
CC, HC, CLC, BRW, KMN = '#3B3833', '#F4F1E6', '#B9D65C', '#C8742A', '#8E2C8E'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s'):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32))


def atom(x, y, label='C', r=24, fill=CC, color='#fff', fs=None):
    fs = fs or (r if len(label) < 3 else r * 0.62)
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{x:.0f}" y="{y + fs * 0.36:.0f}" text-anchor="middle" style="font: 800 {fs:.0f}px Manrope; fill:{color}">{chem(label)}</text>')


def bond(x1, y1, x2, y2, w=5, color=INK, n=1):
    if n == 1:
        return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w}"/>'
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ox, oy = -dy / L * 10, dx / L * 10      # смещение параллельных черт кратной связи
    ks = (-0.6, 0.6) if n == 2 else (-1, 0, 1)
    return ''.join(f'<line x1="{x1 + ox * k:.0f}" y1="{y1 + oy * k:.0f}" x2="{x2 + ox * k:.0f}" y2="{y2 + oy * k:.0f}" '
                   f'stroke="{color}" stroke-width="{w - 1}"/>' for k in ks)


def tube(cx, top, fill, h=240):
    return f'<path d="M{cx - 30} {top} V {top + h - 30} A 30 30 0 0 0 {cx + 30} {top + h - 30} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'


# 1. Этилен и цис-транс --------------------------------------------------------------------------
def ethylene_cis_trans():
    s = text(900, 52, 'Двойная связь: σ + π; цис- и транс-бутен-2', 'h', 'middle')
    s += card(30, 90, 820, 820) + card(880, 90, 890, 820)
    s += text(440, 140, 'Этилен C₂H₄', 't', 'middle')
    c1, c2 = (330, 470), (550, 470)
    s += f'<ellipse cx="440" cy="400" rx="150" ry="45" fill="{BLUE}" opacity=".25"/><ellipse cx="440" cy="540" rx="150" ry="45" fill="{BLUE}" opacity=".25"/>'
    s += text(620, 380, 'π-облако', 's', 'start', BLUE)
    for (cx, cy), sgn in ((c1, -1), (c2, 1)):
        for ang in (150, 210) if sgn < 0 else (30, -30):
            hx, hy = cx + 130 * math.cos(math.radians(ang)), cy - 130 * math.sin(math.radians(ang))
            s += bond(cx, cy, hx, hy) + atom(hx, hy, 'H', 26, HC, INK)
    s += bond(*c1, *c2, 7, INK, 2) + atom(*c1, 'C', 34) + atom(*c2, 'C', 34)
    s += text(440, 445, 'σ + π', 's', 'middle', RED)
    s += lines_at(440, 700, ['атомы C — sp², углы 120°, все атомы в одной плоскости',
                             'C=C 0,134 нм; вращения вокруг двойной связи нет'], 's', step=40)
    for k, (title, up) in enumerate((('цис-бутен-2', True), ('транс-бутен-2', False))):
        x0 = 1040 + k * 420
        s += text(x0 + 80, 160, title, 't', 'middle')
        a, b = (x0, 420), (x0 + 160, 420)
        s += bond(*a, *b, 6, INK, 2)
        s += bond(*a, a[0] - 70, a[1] - 110) + atom(a[0] - 70, a[1] - 110, 'CH₃', 36, '#5D9BD5')
        s += bond(*a, a[0] - 70, a[1] + 110) + atom(a[0] - 70, a[1] + 110, 'H', 24, HC, INK)
        yb = b[1] - 110 if up else b[1] + 110
        yh = b[1] + 110 if up else b[1] - 110
        s += bond(*b, b[0] + 70, yb) + atom(b[0] + 70, yb, 'CH₃', 36, '#5D9BD5')
        s += bond(*b, b[0] + 70, yh) + atom(b[0] + 70, yh, 'H', 24, HC, INK)
        s += atom(*a, 'C', 28) + atom(*b, 'C', 28)
        s += lines_at(x0 + 80, 640, ['метилы по одну' if up else 'метилы по разные', 'сторону' if up else 'стороны'], 's', step=34)
    s += lines_at(1325, 760, ['у бутена-1 и пропена цис-транс нет:', 'у одного атома C двойной связи два H'], 's', step=40, color=RED)
    return s


# 2. Правило Марковникова ----------------------------------------------------------------------------
def markovnikov():
    s = text(900, 52, 'Правило Марковникова (1869)', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    s += text(450, 150, 'пропен + HCl', 't', 'middle')
    xs = (180, 400, 620)
    s += bond(xs[0], 330, xs[1], 330, 6) + bond(xs[1], 330, xs[2], 330, 6, INK, 2)
    for x, lbl in zip(xs, ('CH₃', 'CH', 'CH₂')):
        s += atom(x, 330, lbl, 50, CC, '#fff', 30)
    s += text(400, 420, 'один H', 's', 'middle', GREY) + text(620, 420, 'два H', 's', 'middle', BLUE)
    s += atom(400, 210, 'Cl', 34, '#B9D65C', INK) + atom(620, 210, 'H', 30, HC, INK)
    s += arrow(400, 246, 400, 272, GREEN, 5) + arrow(620, 242, 620, 272, BLUE, 5)
    s += arrow(780, 260, 960, 260, INK, 6)
    s += text(1350, 180, 'CH₃–CHCl–CH₃', 'f', 'middle', GREEN) + text(1350, 240, '2-хлорпропан', 't', 'middle')
    s += text(1350, 380, 'CH₃–CH₂–CH₂Cl', 't', 'middle', GREY) + text(1350, 425, '1-хлорпропан не образуется', 's', 'middle', RED)
    s += f'<line x1="1180" y1="370" x2="1520" y2="370" stroke="{RED}" stroke-width="5"/>'
    s += f'<rect x="200" y="560" width="1400" height="120" rx="16" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    s += lines_at(900, 610, ['При присоединении HX и воды к несимметричному алкену водород идёт к атому C,',
                             'у которого больше атомов водорода'], 't', step=44)
    s += text(900, 780, 'пропен + H₂O (H₂SO₄) → пропанол-2', 's', 'middle')
    return s


# 3. Обесцвечивание --------------------------------------------------------------------------------
def decolorization():
    s = text(900, 52, 'Что обесцвечивает бромную воду и раствор KMnO₄', 'h', 'middle')
    s += card(30, 90, 1740, 800)
    subs = [('этилен', True, True), ('бензол', False, False), ('толуол', False, True), ('гексан', False, False), ('полиэтилен', False, False)]
    s += text(80, 300, 'бромная вода', 't', 'start', BRW) + text(80, 620, 'раствор KMnO₄', 't', 'start', KMN)
    for k, (name, br, km) in enumerate(subs):
        cx = 470 + k * 280
        s += text(cx, 150, name, 't', 'middle')
        s += tube(cx, 180, '#F3F1EA' if br else '#F0C48A')
        s += text(cx, 470, 'да' if br else 'нет', 't', 'middle', GREEN if br else RED)
        s += tube(cx, 500, '#F3F1EA' if km else '#C99BD8')
        s += text(cx, 790, 'да' if km else 'нет', 't', 'middle', GREEN if km else RED)
    s += text(900, 850, 'Бесцветная пробирка — окраска исчезла: в молекуле есть кратная связь (у толуола окисляется боковая цепь)', 's', 'middle')
    return s


# 4. Полимеризация ----------------------------------------------------------------------------------
def polymerization():
    s = text(900, 52, 'Полимеризация этилена', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    for k in range(3):
        x = 140 + k * 170
        s += text(x, 260, 'CH₂=CH₂', 't', 'middle')
    s += text(310, 330, 'n молекул мономера', 's', 'middle', GREY)
    s += arrow(600, 250, 760, 250, INK, 6) + text(680, 220, 't, p, кат.', 's', 'middle')
    chain = f'…–CH₂–CH₂–<tspan style="fill:{RED}">CH₂–CH₂</tspan>–CH₂–CH₂–…'
    s += text(1240, 262, chain, 't', 'middle')
    s += text(1240, 330, 'звено –CH₂–CH₂– (выделено)', 's', 'middle', RED)
    s += text(900, 470, 'nCH₂=CH₂ → (–CH₂–CH₂–)ₙ', 'f', 'middle')
    s += text(900, 560, 'степень полимеризации n = M(полимера) / M(звена)', 't', 'middle')
    s += lines_at(900, 650, ['полиэтилен — термопласт, предельный: бромную воду не обесцвечивает',
                             'полипропилен — из пропилена; ПВХ — из винилхлорида CH₂=CHCl'], 's', step=44)
    return s


# 5. Вулканизация -----------------------------------------------------------------------------------
def wave(x0, y0, length, color):
    pts = ' '.join(f'{x0 + t:.0f},{y0 + 18 * math.sin(t / 40):.0f}' for t in range(0, length, 8))
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round"/>'


def vulcanization():
    s = text(900, 52, 'Вулканизация: каучук + сера → резина', 'h', 'middle')
    s += card(30, 90, 840, 700) + card(930, 90, 840, 700)
    s += text(450, 140, 'Каучук: отдельные цепи', 't', 'middle')
    for k in range(4):
        s += wave(90, 240 + k * 120, 720, '#B9853A')
    s += text(1350, 140, 'Резина: цепи сшиты серой', 't', 'middle')
    for k in range(4):
        s += wave(990, 240 + k * 120, 720, '#7A5A2B')
    for k in range(3):
        for j in range(4):
            x = 1060 + j * 180 + (k % 2) * 70
            y1, y2 = 258 + k * 120, 222 + (k + 1) * 120
            s += f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#E8C547" stroke-width="7"/>'
            s += f'<circle cx="{x}" cy="{(y1 + y2) / 2:.0f}" r="16" fill="#E8C547" stroke="{INK}" stroke-width="2"/>'
            s += text(x, (y1 + y2) / 2 + 8, 'S', 's', 'middle')
    s += lines_at(450, 730, ['натуральный каучук — цис-полиизопрен'], 's')
    s += lines_at(1350, 730, ['сульфидные мостики; много серы — эбонит'], 's')
    return s


# 6. Ацетилен --------------------------------------------------------------------------------------
def acetylene():
    s = text(900, 52, 'Ацетилен C₂H₂: тройная связь и получение', 'h', 'middle')
    s += card(30, 90, 900, 760) + card(960, 90, 810, 760)
    y = 360
    s += f'<ellipse cx="480" cy="{y}" rx="140" ry="70" fill="{BLUE}" opacity=".18"/><ellipse cx="480" cy="{y}" rx="70" ry="120" fill="{RED}" opacity=".15"/>'
    s += bond(160, y, 370, y) + bond(590, y, 800, y) + bond(370, y, 590, y, 6, INK, 3)
    s += atom(160, y, 'H', 30, HC, INK) + atom(370, y, 'C', 36) + atom(590, y, 'C', 36) + atom(800, y, 'H', 30, HC, INK)
    s += text(480, 230, '180° — молекула линейная', 't', 'middle')
    s += lines_at(480, 560, ['C≡C = 1 σ + 2 π; атомы C — sp', 'длина 0,120 нм — короче и прочнее двойной',
                             'цис-транс-изомерии нет'], 's', step=44)
    # получение
    s += text(1365, 140, 'CaC₂ + 2H₂O → C₂H₂ + Ca(OH)₂', 't', 'middle')
    s += f'<circle cx="1300" cy="520" r="120" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="1270" y="330" width="60" height="80" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M1240 230 H1360 L1320 290 V340 H1280 V290 Z" fill="#DCEBF5" stroke="{INK}" stroke-width="3"/>'
    s += text(1390, 260, 'вода', 's')
    s += ''.join(f'<rect x="{1240 + j * 28}" y="{580 - (j % 2) * 14}" width="22" height="22" fill="#7A7A7A" stroke="{INK}" stroke-width="1.5"/>' for j in range(5))
    s += text(1420, 600, 'CaC₂', 's')
    s += f'<path d="M1330 360 H1560 V480" fill="none" stroke="{INK}" stroke-width="10"/><path d="M1330 360 H1560 V480" fill="none" stroke="#fff" stroke-width="4"/>'
    s += text(1600, 470, 'C₂H₂', 't')
    s += lines_at(1365, 740, ['ацетилен — бесцветный газ, легче воздуха;', 'горит пламенем около 3000 °C — сварка'], 's', step=40)
    return s


# 7. Бензол и ксилолы --------------------------------------------------------------------------------
def hexagon(cx, cy, r=110, circle=True, subs=None):
    pts = [(cx + r * math.cos(math.radians(90 + 60 * k)), cy - r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    s = f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="#fff" stroke="{INK}" stroke-width="6"/>'
    if circle:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r * 0.58:.0f}" fill="none" stroke="{INK}" stroke-width="5"/>'
    for k in subs or []:
        x, y = pts[k - 1]
        ex, ey = cx + (x - cx) * 1.55, cy + (y - cy) * 1.55
        s += bond(x, y, ex, ey, 5) + text(ex, ey + (-10 if ey < cy else 30), 'CH₃', 's', 'middle')
    return s


def benzene_xylenes():
    s = text(900, 52, 'Бензол: ароматическая связь; ксилолы C₈H₁₀', 'h', 'middle')
    s += card(30, 90, 1740, 520) + card(30, 640, 1740, 400)
    s += f'<ellipse cx="450" cy="250" rx="170" ry="40" fill="{BLUE}" opacity=".25"/><ellipse cx="450" cy="490" rx="170" ry="40" fill="{BLUE}" opacity=".25"/>'
    s += hexagon(450, 370, 120)
    s += text(450, 590, 'единое π-облако над и под кольцом', 's', 'middle', BLUE)
    s += lines_at(1200, 220, ['C₆H₆: все атомы C — sp², углы 120°', '12 σ-связей в одной плоскости',
                              'все связи C–C одинаковые — 0,140 нм', 'между одинарной (0,154) и двойной (0,134)',
                              'поэтому бромную воду и KMnO₄', 'бензол не обесцвечивает'], 't', step=58)
    s += text(450, 150, 'Фарадей, 1825; формула — Кекуле, 1865', 'cap', 'middle')
    for k, (name, subs) in enumerate((('орто-ксилол (1,2)', [1, 2]), ('мета-ксилол (1,3)', [1, 3]), ('пара-ксилол (1,4)', [1, 4]))):
        cx = 330 + k * 560
        s += hexagon(cx, 850, 65, True, subs)
        s += text(cx, 1025, name, 't', 'middle')
    s += text(900, 685, 'C₈H₁₀ — четыре арена: этилбензол и три ксилола', 's', 'middle')
    return s


# 8. Ректификационная колонна -----------------------------------------------------------------------
def distillation_column():
    s = text(900, 52, 'Перегонка нефти — физический процесс', 'h', 'middle')
    s += card(30, 90, 1740, 960)
    s += f'<rect x="760" y="140" width="240" height="800" rx="30" fill="#F7EFC8" stroke="{INK}" stroke-width="4"/>'
    fr = [('бензин', '40–200 °C', 'автомобили', '#F3E39A'), ('лигроин', '150–250 °C', 'тракторы', '#EBCF76'),
          ('керосин', '180–300 °C', 'самолёты', '#DDB357'), ('газойль', '250–350 °C', 'дизельное топливо', '#C9923D'),
          ('мазут', 'выше 350 °C', 'котельное топливо; масла, гудрон', '#7A5A2B')]
    for k, (n, t, use, col) in enumerate(fr):
        y = 210 + k * 155
        s += f'<line x1="770" y1="{y + 40}" x2="990" y2="{y + 40}" stroke="{GREY}" stroke-width="3"/>'
        s += arrow(1000, y, 1160, y, INK, 4)
        s += f'<rect x="1170" y="{y - 40}" width="80" height="80" rx="10" fill="{col}" stroke="{INK}" stroke-width="2"/>'
        s += text(1280, y - 6, n + ' · ' + t, 't') + text(1280, y + 30, use, 's', 'start', GREY)
    s += box(400, 860, 400, 110, 'трубчатая печь|320–350 °C', '#F6D2BF', cls='t')
    s += arrow(600, 860, 755, 860, RED, 6)
    s += text(400, 720, 'нефть', 'f', 'middle') + arrow(400, 740, 400, 800, INK, 5)
    s += lines_at(400, 300, ['вверху — лёгкие фракции', 'с низкой t кип;', 'внизу — тяжёлые'], 's', step=40)
    s += arrow(880, 920, 880, 180, BLUE, 3)
    s += text(880, 1000, 'бензина при перегонке — не больше 20 %', 's', 'middle')
    return s


# 9. Крекинг и коксование ---------------------------------------------------------------------------
def cracking_coking():
    s = text(900, 52, 'Крекинг и коксование', 'h', 'middle')
    s += card(30, 90, 1740, 400) + card(30, 520, 1740, 480)
    s += text(900, 145, 'Крекинг — химический процесс: расщепление молекул (В. Г. Шухов)', 't', 'middle')
    s += f'<rect x="120" y="230" width="640" height="60" rx="30" fill="#7A5A2B"/>' + text(440, 272, 'C₁₆H₃₄', 't', 'middle', '#fff')
    s += arrow(790, 260, 930, 260, RED, 6) + text(860, 230, 't', 's', 'middle', RED)
    s += f'<rect x="960" y="190" width="320" height="56" rx="28" fill="#DDB357"/>' + text(1120, 230, 'C₈H₁₈ — алкан', 's', 'middle')
    s += f'<rect x="960" y="280" width="320" height="56" rx="28" fill="#F3E39A"/>' + text(1120, 320, 'C₈H₁₆ — алкен', 's', 'middle')
    s += lines_at(1520, 250, ['C: 16 = 8 + 8', 'H: 34 = 18 + 16'], 's', step=40)
    s += text(900, 440, 'бензина до 65–70 %; в бензине крекинга есть непредельные углеводороды', 's', 'middle')
    s += text(900, 575, 'Коксование: уголь нагревают без доступа воздуха до 900–1050 °C', 't', 'middle')
    s += box(330, 760, 340, 110, 'уголь|без воздуха', '#E0DAD0', cls='t')
    prods = [('кокс', 'металлургия'), ('каменноугольная смола', 'бензол, толуол, фенол'), ('аммиачная вода', 'удобрения'), ('коксовый газ', 'H₂, CH₄, CO — топливо')]
    for k, (n, u) in enumerate(prods):
        y = 650 + k * 92
        s += arrow(510, 760, 775, y, INK, 4)
        s += box(1130, y, 690, 76, f'{n} — {u}', '#fff')
    return s


# 10. Справочная карта условий ---------------------------------------------------------------------
def conditions_map():
    s = text(900, 52, 'Справочная карта: условие → реакция', 'h', 'middle')
    s += card(30, 90, 1740, 1000)
    rows = [('свет (hν)', 'замещение галогеном: алканы, C₅–C₆ циклы; бензол — присоединение (гексахлоран)', ORANGE),
            ('FeCl₃ / FeBr₃', 'замещение в кольце: бензол, толуол', BLUE),
            ('конц. HNO₃ + H₂SO₄', 'нитрование: бензол → нитробензол; толуол → тротил', RED),
            ('Ni, Pt, Pd', 'гидрирование: алкены, алкины, диены; бензол — при нагреве и давлении', GREY),
            ('H₂SO₄ / H₃PO₄', 'гидратация алкенов → спирты', GREEN),
            ('HgSO₄', 'Кучеров: ацетилен + вода → уксусный альдегид', PURPLE),
            ('600 °C', 'тримеризация: 3C₂H₂ → C₆H₆', '#7A5A2B'),
            ('t, p, катализатор', 'полимеризация: этилен, пропилен, винилхлорид, диены, стирол', INK)]
    for k, (cond, what, col) in enumerate(rows):
        y = 170 + k * 88
        s += f'<rect x="80" y="{y - 34}" width="380" height="66" rx="12" fill="{col}"/>' + text(270, y + 9, cond, 's', 'middle', '#fff')
        s += arrow(470, y, 540, y, INK, 4) + text(560, y + 9, what, 's')
    y0 = 900
    s += text(900, y0 - 10, 'Обесцвечивают: бромная вода — алкены, диены, алкины, стирол; KMnO₄ — они же и толуол', 't', 'middle')
    s += text(900, y0 + 50, 'Не обесцвечивают ни то, ни другое: алканы, циклоалканы C₅–C₆, бензол, полиэтилен', 't', 'middle', RED)
    return s


if __name__ == '__main__':
    jobs = {
        'ethylene-cis-trans.png': (ethylene_cis_trans(), 1800, 940),
        'markovnikov.png': (markovnikov(), 1800, 880),
        'decolorization.png': (decolorization(), 1800, 920),
        'polymerization.png': (polymerization(), 1800, 880),
        'vulcanization.png': (vulcanization(), 1800, 820),
        'acetylene.png': (acetylene(), 1800, 880),
        'benzene-xylenes.png': (benzene_xylenes(), 1800, 1070),
        'distillation-column.png': (distillation_column(), 1800, 1080),
        'cracking-coking.png': (cracking_coking(), 1800, 1030),
        'conditions-map.png': (conditions_map(), 1800, 1120),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
