"""Рисунки недели 20 химии (course/week-20/pics/*.png): названия кислот, карбоксильная группа и димер, пять пробирок
с уксусной кислотой, муравьиная кислота, этерификация, строение жира, гидролиз и гидрирование, мыло, мыло и СМС,
таблица распознавания.

Факты — по выжимке course/textbooks/chem-20-acids-esters-fats.md (Х9-2 § 64–66; Х11-1 § 9–13). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w20.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render, span
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = s.replace('ₙ₊₁', '').replace('ₙ', '')
    s = chem(s).replace('', '<tspan baseline-shift="-0.28em" font-size="68%">n+1</tspan>')
    return _text(x, y, s.replace('', '<tspan baseline-shift="-0.28em" font-size="68%">n</tspan>'), cls, anchor, fill)

OUT = ROOT / 'course' / 'week-20' / 'pics'
BLUE, ORANGE, BROWN = '#3A57A7', '#D98A2B', '#8A5A2B'
CC, HC, OC = '#3B3833', '#F4F1E6', '#E04B4B'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32, color=color))


def tube(cx, top, fill, h=280, sediment=None):
    s = f'<path d="M{cx - 34} {top} V {top + h - 34} A 34 34 0 0 0 {cx + 34} {top + h - 34} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if sediment:
        s += (f'<path d="M{cx - 34} {top + h - 70} V {top + h - 34} A 34 34 0 0 0 {cx + 34} {top + h - 34} V {top + h - 70} Z" '
              f'fill="{sediment}" stroke="{INK}" stroke-width="2"/>')
    return s


def bubbles(cx, top, n=6):
    return ''.join(f'<circle cx="{cx - 16 + (j * 13) % 34}" cy="{top + 30 + j * 32}" r="{6 + j % 3 * 2}" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                   for j in range(n))


def atom(x, y, label, r=26, fill=CC, color='#fff'):
    fs = r if len(label) < 3 else r * 0.62
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{x:.0f}" y="{y + fs * 0.36:.0f}" text-anchor="middle" style="font: 800 {fs:.0f}px Manrope; fill:{color}">{chem(label)}</text>')


def bond(x1, y1, x2, y2, w=5, color=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w}"{d}/>'


def dbond(x1, y1, x2, y2, off=9, color=INK):
    ang = math.atan2(y2 - y1, x2 - x1)
    dx, dy = -math.sin(ang) * off, math.cos(ang) * off
    return bond(x1 + dx, y1 + dy, x2 + dx, y2 + dy, 5, color) + bond(x1 - dx, y1 - dy, x2 - dx, y2 - dy, 5, color)


def zigzag(x0, y0, n, step=36, amp=16, color=INK, kink_at=None):
    """Углеводородная цепь зигзагом; kink_at — номер звена, после которого цепь уходит вниз (связь C=C)."""
    pts, x, y, dy = [(x0, y0)], x0, y0, 0
    s = ''
    for k in range(n):
        if kink_at is not None and k == kink_at:
            dy = 12
        nx, ny = x + step * (0.82 if dy else 1), y + dy + (amp if k % 2 == 0 else -amp)
        if kink_at is not None and k == kink_at:
            s += dbond(x, y, nx, ny, 6, RED)
        else:
            s += bond(x, y, nx, ny, 4, color)
        x, y = nx, ny
        pts.append((x, y))
    return s


# 1. Названия кислот ---------------------------------------------------------------------------------
def acid_names():
    s = text(900, 52, 'Названия карбоновых кислот', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    cols = (360, 760, 1130, 1500)
    for x, h in zip(cols, ('формула', 'систематическое', 'тривиальное', 'соли')):
        s += text(x, 150, h, 's', 'middle', GREY)
    rows = [('C₁', 'HCOOH', 'метановая', 'муравьиная', 'формиаты'), ('C₂', 'CH₃COOH', 'этановая', 'уксусная', 'ацетаты'),
            ('C₃', 'C₂H₅COOH', 'пропановая', 'пропионовая', 'пропионаты'), ('C₄', 'C₃H₇COOH', 'бутановая', 'масляная', '—'),
            ('C₅', 'C₄H₉COOH', 'пентановая', 'валериановая', '—'), (None,) * 5,
            ('C₁₆', 'C₁₅H₃₁COOH', 'гексадекановая', 'пальмитиновая', '—'), ('C₁₈', 'C₁₇H₃₅COOH', 'октадекановая', 'стеариновая', 'стеараты')]
    for k, r in enumerate(rows):
        y = 220 + k * 88
        if r[0] is None:
            s += text(900, y + 12, 'высшие кислоты — в жирах', 's', 'middle', GREY)
            continue
        s += f'<rect x="60" y="{y - 38}" width="1680" height="76" rx="12" fill="{"#fff" if k % 2 else "#F7F5EF"}"/>'
        s += f'<rect x="80" y="{y - 30}" width="{70 + min(k, 4) * 28}" height="60" rx="10" fill="{RED}" opacity="{0.25 + 0.1 * min(k, 6):.2f}"/>'
        s += text(115, y + 11, r[0], 't', 'middle')
        s += text(cols[0], y + 11, r[1], 't', 'middle') + text(cols[1], y + 11, r[2], 's', 'middle')
        s += text(cols[2], y + 11, r[3], 't', 'middle', RED) + text(cols[3], y + 11, r[4], 's', 'middle', BLUE)
    s += text(900, 920, 'CₙH₂ₙ₊₁COOH = CₙH₂ₙO₂ · нумерация с атома C группы COOH · число атомов C считают вместе с COOH', 's', 'middle')
    return s


# 2. Карбоксильная группа и димер ----------------------------------------------------------------------
def carboxyl():
    s = text(900, 52, 'Карбоксильная группа и водородные связи', 'h', 'middle')
    s += card(30, 90, 740, 760) + card(790, 90, 980, 760)
    s += text(400, 150, '–COOH = C=O + –OH', 't', 'middle')
    R, C, O1, O2, H = (130, 450), (300, 450), (420, 320), (440, 540), (580, 540)
    s += bond(*R, *C) + dbond(*C, *O1) + bond(*C, *O2) + bond(*O2, *H)
    s += atom(*R, 'R', 30, '#9A958C') + atom(*C, 'C', 34) + atom(*O1, 'O', 30, OC) + atom(*O2, 'O', 30, OC) + atom(*H, 'H', 22, HC, INK)
    s += f'<rect x="250" y="270" width="230" height="230" rx="20" fill="none" stroke="{BLUE}" stroke-width="4" stroke-dasharray="12 8"/>'
    s += f'<rect x="395" y="490" width="235" height="105" rx="20" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="12 8"/>'
    s += text(500, 300, 'карбонильная C=O', 's', 'start', BLUE) + text(630, 640, 'гидроксильная –OH', 's', 'end', RED)
    s += lines_at(400, 720, ['связь O–H сильно полярна', 'атом H подвижен — кислотные свойства'], 's', step=38)
    s += text(1280, 150, 'Димер уксусной кислоты', 't', 'middle')
    for sg, cx in ((1, 1060), (-1, 1500)):
        Ca, Oa, Ob = (cx, 450), (cx + sg * 90, 450 - sg * 80), (cx + sg * 90, 450 + sg * 80)
        Hb = (Ob[0] + sg * 70, Ob[1])
        s += bond(cx - sg * 130, 450, *Ca) + dbond(*Ca, *Oa) + bond(*Ca, *Ob) + bond(*Ob, *Hb)
        s += atom(cx - sg * 130, 450, 'CH₃', 36, '#9A958C') + atom(*Ca, 'C', 30) + atom(*Oa, 'O', 28, OC) + atom(*Ob, 'O', 28, OC)
        s += atom(*Hb, 'H', 20, HC, INK)
    s += bond(1220, 530, 1390, 530, 4, BLUE, '8 7') + bond(1340, 370, 1170, 370, 4, BLUE, '8 7')
    s += lines_at(1280, 650, ['две водородные связи (пунктир) прочнее, чем у спиртов', 'молекулы кислоты объединяются в пары — димеры'], 's', step=40)
    return s


# 3. Пять пробирок ----------------------------------------------------------------------------------
def acetic_tests():
    s = text(900, 52, 'Уксусная кислота — как минеральная кислота', 'h', 'middle')
    s += card(30, 90, 1740, 800)
    items = [('лакмус', '#E57373', 'красный', None, False, 'H⁺ в растворе'),
             ('Mg', '#EEF3F6', 'пузырьки H₂', '#9AA0A6', True, '(CH₃COO)₂Mg + H₂↑'),
             ('MgO', '#EEF3F6', 'оксид растворяется', '#FFFFFF', False, '(CH₃COO)₂Mg + H₂O'),
             ('NaOH', '#EEF3F6', 'нейтрализация', None, False, 'CH₃COONa + H₂O'),
             ('Na₂CO₃', '#EEF3F6', 'пузырьки CO₂', None, True, 'CH₃COONa + H₂O + CO₂↑')]
    for k, (reag, fill, obs, sed, gas, prod) in enumerate(items):
        cx = 220 + k * 340
        s += text(cx, 170, '+ ' + reag, 't', 'middle')
        s += tube(cx, 210, fill, 300, sed)
        if gas:
            s += bubbles(cx, 230)
        s += text(cx, 580, obs, 's', 'middle', RED if gas else INK)
        s += text(cx, 625, prod, 'cap', 'middle')
    s += lines_at(900, 720, ['во всех реакциях образуется соль — ацетат',
                             '2 моль CH₃COOH → 1 моль H₂ (с Mg) и 1 моль CO₂ (с Na₂CO₃); с NaHCO₃ — 1 : 1'], 's', step=44)
    return s


# 4. Муравьиная кислота ----------------------------------------------------------------------------
def formic_acid():
    s = text(900, 52, 'Муравьиная кислота: и кислота, и альдегид', 'h', 'middle')
    s += card(30, 90, 800, 760) + card(850, 90, 920, 760)
    H1, C, O1, O2, H2 = (170, 470), (330, 470), (330, 310), (490, 470), (630, 470)
    s += bond(*H1, *C) + dbond(*C, *O1) + bond(*C, *O2) + bond(*O2, *H2)
    s += atom(*H1, 'H', 24, HC, INK) + atom(*C, 'C', 34) + atom(*O1, 'O', 30, OC) + atom(*O2, 'O', 30, OC) + atom(*H2, 'H', 24, HC, INK)
    s += f'<rect x="125" y="255" width="260" height="265" rx="20" fill="none" stroke="{BLUE}" stroke-width="4" stroke-dasharray="12 8"/>'
    s += f'<rect x="280" y="240" width="395" height="300" rx="24" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="4 8"/>'
    s += text(125, 230, 'альдегидная H–C=O', 's', 'start', BLUE) + text(675, 580, 'карбоксильная –COOH', 's', 'end', RED)
    s += lines_at(430, 690, ['самая сильная в ряду предельных', 'одноосновных кислот'], 's', step=38)
    s += text(1080, 160, 'Ag₂O (NH₃), t', 't', 'middle') + text(1540, 160, 'конц. H₂SO₄, t', 't', 'middle')
    s += tube(1080, 210, '#E9EBEE', 300)
    s += f'<path d="M1046 230 V 470" stroke="#B8BDC4" stroke-width="10"/><path d="M1114 230 V 470" stroke="#E8ECF0" stroke-width="10"/>'
    s += tube(1540, 210, '#F7EFC8', 300) + bubbles(1540, 230) + text(1600, 250, 'CO↑', 't', 'start', RED)
    s += text(1080, 570, 'серебряное зеркало', 's', 'middle') + text(1540, 570, 'выделяется CO', 's', 'middle')
    s += lines_at(1310, 670, ['HCOOH + Ag₂O → CO₂ + H₂O + 2Ag↓', 'HCOOH → CO↑ + H₂O', 'уксусная кислота этих реакций не даёт'], 's', step=44)
    return s


# 5. Этерификация ------------------------------------------------------------------------------------
def esterification():
    s = text(900, 52, 'Этерификация: кислота + спирт ⇄ эфир + вода', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    s += text(230, 250, 'CH₃CO' + span('OH', RED), 'f', 'middle') + text(440, 250, '+', 'f', 'middle')
    s += text(650, 250, span('H', RED) + 'OC₂H₅', 'f', 'middle')
    s += text(230, 320, 'уксусная кислота', 's', 'middle', GREY) + text(650, 320, 'этанол', 's', 'middle', GREY)
    s += f'<path d="M820 215 H 1010 M 990 200 L 1012 215" stroke="{INK}" stroke-width="5" fill="none"/>'
    s += f'<path d="M1010 245 H 820 M 840 260 L 818 245" stroke="{INK}" stroke-width="5" fill="none"/>'
    s += text(915, 180, 'H₂SO₄ (конц.), t', 's', 'middle', BLUE)
    s += text(1270, 250, 'CH₃COOC₂H₅', 'f', 'middle') + text(1500, 250, '+', 'f', 'middle') + text(1620, 250, 'H₂O', 'f', 'middle', RED)
    s += text(1270, 320, 'этилацетат', 's', 'middle', GREY)
    s += f'<path d="M300 345 Q 450 450 610 345" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="8 7"/>'
    s += text(455, 470, 'OH от кислоты + H от спирта = вода', 's', 'middle', RED)
    s += lines_at(1270, 420, ['реакция обратима; H₂SO₄ — катализатор и связывает воду',
                             'обратная реакция — гидролиз; щелочной гидролиз — омыление'], 's', step=42)
    s += text(900, 630, 'Название эфира: сначала спирт, потом кислота', 't', 'middle')
    ex = [('CH₃COOC₂H₅', 'этил', 'ацетат'), ('HCOOCH₃', 'метил', 'формиат'), ('CH₃COOC₃H₇', 'пропил', 'ацетат'), ('HCOOC₂H₅', 'этил', 'формиат')]
    for k, (f, a, b) in enumerate(ex):
        x = 250 + k * 433
        s += f'<rect x="{x - 190}" y="670" width="380" height="200" rx="16" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += text(x, 730, f, 't', 'middle') + text(x, 800, span(a, BLUE) + span(b, RED), 't', 'middle')
        s += text(x, 845, 'спирт + кислота', 'cap', 'middle')
    return s


# 6. Строение жира -----------------------------------------------------------------------------------
def fat_structure():
    s = text(900, 52, 'Жир — эфир глицерина и трёх высших кислот', 'h', 'middle')
    s += card(30, 90, 1090, 800) + card(1140, 90, 630, 800)
    rows = [(250, 'CH₂', 16, None, 'C₁₇H₃₅ — стеариновая, предельная'),
            (470, 'CH', 16, 10, 'C₁₇H₃₃ — олеиновая, 1 C=C — излом'),
            (690, 'CH₂', 14, None, 'C₁₅H₃₁ — пальмитиновая, предельная')]
    for y, g, n, kink, lab in rows:
        s += box(140, y, 110, 70, g, '#F7EFC8', cls='t')
        s += text(205, y + 11, '–O–CO–', 't')
        s += zigzag(400, y, n, kink_at=kink)
        s += text(410, y - 40, lab, 's', 'start', RED if kink else INK)
    s += bond(140, 285, 140, 435, 5) + bond(140, 505, 140, 655, 5)
    s += text(140, 790, 'глицерин', 's', 'middle', GREY) + text(700, 790, 'остатки высших кислот', 's', 'middle', GREY)
    s += text(575, 850, 'триглицерид: кислоты могут быть одинаковыми и разными', 'cap', 'middle')
    s += box(1455, 290, 560, 260, 'Твёрдые жиры|в основном предельные кислоты|обычно животные|исключение: рыбий жир — жидкий', '#FFF6E8')
    s += box(1455, 640, 560, 260, 'Масла (жидкие)|в основном непредельные кислоты|обычно растительные|исключение: кокосовое и|пальмовое масло — твёрдые', '#E3F1E6')
    return s


# 7. Гидролиз и гидрирование ------------------------------------------------------------------------
def fat_reactions():
    s = text(900, 52, 'Что можно сделать с жиром', 'h', 'middle')
    items = [('Кислотный гидролиз', 'жир', 'H₂O, H⁺, t', 'глицерин +|3 карбоновые кислоты', '#FFF6E8', BLUE),
             ('Омыление', 'жир', 'NaOH или KOH, t', 'глицерин +|3 соли = мыло', '#E3EEF7', RED),
             ('Гидрирование', 'жидкое масло', 'H₂, кат., t', 'твёрдый жир|(саломас) → маргарин', '#E3F1E6', GREEN)]
    for k, (t, a, cond, res, fill, col) in enumerate(items):
        x = 30 + k * 590
        cx = x + 280
        s += card(x, 90, 560, 700)
        s += text(cx, 160, t, 't', 'middle', col)
        s += box(cx, 270, 320, 90, a, '#F7EFC8', cls='t')
        s += arrow(cx, 320, cx, 470, col, 6) + text(cx + 20, 410, cond, 's', 'start', col)
        s += box(cx, 560, 420, 120, res, fill, cls='t')
    s += lines_at(900, 860, ['(C₁₇H₃₅COO)₃C₃H₅ + 3NaOH → C₃H₅(OH)₃ + 3C₁₇H₃₅COONa',
                             'триолеин + 3H₂ → тристеарин · гидролиз — расщепление, гидрирование — присоединение H₂'], 's', step=44)
    return s


# 8. Мыло ------------------------------------------------------------------------------------------------
def soap():
    s = text(900, 52, 'Как моет мыло и почему не моет в жёсткой воде', 'h', 'middle')
    s += card(30, 90, 1060, 800, '#DCEBF5') + card(1110, 90, 660, 800)
    cx, cy = 560, 460
    s += f'<path d="M{cx - 130} {cy - 40} q 40 -110 150 -80 q 120 30 100 130 q -20 110 -140 90 q -130 -20 -110 -140 Z" fill="{BROWN}"/>'
    s += text(cx, cy + 10, 'грязь, жир', 's', 'middle', '#fff')
    for k in range(10):
        a = math.radians(k * 36 + 10)
        x1, y1 = cx + 105 * math.cos(a), cy + 105 * math.sin(a)
        x2, y2 = cx + 250 * math.cos(a), cy + 250 * math.sin(a)
        s += bond(x1, y1, x2, y2, 5, INK)
        s += f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="20" fill="{RED}" stroke="{INK}" stroke-width="2"/>'
    s += text(150, 170, 'вода', 't', 'start', BLUE)
    s += text(560, 800, 'хвост C₁₇H₃₅ — в грязи; головка –COO⁻ (красная) — в воде', 's', 'middle')
    s += text(560, 845, 'мыло — ПАВ: уменьшает поверхностное натяжение', 'cap', 'middle')
    s += text(1440, 160, 'Жёсткая вода: Ca²⁺, Mg²⁺', 't', 'middle')
    s += tube(1440, 210, '#EEF3F6', 320)
    s += ''.join(f'<ellipse cx="{1420 + (j * 17) % 40}" cy="{270 + j * 34}" rx="12" ry="6" fill="#fff" stroke="{INK}" stroke-width="2"/>' for j in range(7))
    s += text(1440, 590, 'белые хлопья, пены нет', 's', 'middle', RED)
    s += lines_at(1440, 670, ['2C₁₇H₃₅COONa + Ca²⁺ →', '(C₁₇H₃₅COO)₂Ca↓ + 2Na⁺'], 's', step=40)
    s += text(1440, 800, 'расход мыла растёт', 's', 'middle', GREY)
    return s


# 9. Мыло и СМС --------------------------------------------------------------------------------------
def soap_sms():
    s = text(900, 52, 'Мыло и синтетические моющие средства', 'h', 'middle')
    data = [('Мыло', 'C₁₇H₃₅COONa — из жиров', ['неразветвлённые цепи разлагаются бактериями', 'натриевое твёрдое, калиевое жидкое'],
             ['в жёсткой воде — осадок с Ca²⁺ и Mg²⁺', 'тратятся пищевые жиры', 'моет только в щелочной среде'], GREEN),
            ('СМС', 'R–O–SO₃Na — алкилсульфаты', ['соли Ca и Mg растворимы — моют в жёсткой воде', 'сырьё — нефть и газ',
                                              'работают в кислой, нейтральной, щелочной среде'],
             ['разветвлённые цепи трудно разлагаются', 'загрязняют водоёмы, «горы пены»', 'сушат кожу рук'], BLUE)]
    for k, (t, f, plus, minus, col) in enumerate(data):
        x = 30 + k * 880
        cx = x + 425
        s += card(x, 90, 850, 620)
        s += text(cx, 160, t, 'h', 'middle', col) + text(cx, 215, f, 't', 'middle')
        s += text(x + 50, 300, '+ плюсы', 't', 'start', GREEN)
        s += lines_at(x + 80, 350, plus, 's', 'start', step=44)
        s += text(x + 50, 520, '− минусы', 't', 'start', RED)
        s += lines_at(x + 80, 570, minus, 's', 'start', step=44)
    return s


# 10. Распознавание и цепочка --------------------------------------------------------------------------
def recognition():
    s = text(900, 52, 'Распознавание и цепочка превращений', 'h', 'middle')
    s += card(30, 90, 1120, 900) + card(1180, 90, 590, 900)
    rows = [('лакмус', 'красный', 'кислоты'), ('Na₂CO₃, NaHCO₃', 'пузырьки CO₂', 'кислоты'),
            ('Ag₂O (NH₃), t', 'серебряное зеркало', 'альдегиды, HCOOH'), ('конц. H₂SO₄, t', 'выделяется CO', 'HCOOH'),
            ('бромная вода', 'обесцвечивается', 'масла, непредельные'), ('спирт + H₂SO₄, t', 'запах эфира', 'кислота'),
            ('жёсткая вода', 'осадок, нет пены', 'мыло (СМС — нет)')]
    s += text(200, 150, 'реактив', 's', 'middle', GREY) + text(560, 150, 'признак', 's', 'middle', GREY) + text(920, 150, 'кто даёт', 's', 'middle', GREY)
    for k, (r, f, c) in enumerate(rows):
        y = 220 + k * 104
        s += f'<rect x="60" y="{y - 40}" width="1060" height="84" rx="12" fill="{"#fff" if k % 2 else "#F7F5EF"}"/>'
        s += text(200, y + 10, r, 's', 'middle') + text(560, y + 10, f, 's', 'middle') + text(920, y + 10, c, 's', 'middle', BLUE)
    s += text(590, 950, 'спирты и фенол с карбонатами CO₂ не дают', 's', 'middle', RED)
    chain = ['этилен', 'этанол', 'этаналь', 'уксусная кислота', 'этилацетат']
    conds = ['H₂O, H₃PO₄, t, p', 'CuO, t', 'Ag₂O (NH₃), t', 'C₂H₅OH, H₂SO₄, t']
    for k, n in enumerate(chain):
        y = 170 + k * 190
        s += box(1475, y, 400, 76, n, '#F7EFC8' if k in (0, 4) else '#fff', cls='t')
        if k < 4:
            s += arrow(1475, y + 40, 1475, y + 150, RED, 5) + text(1495, y + 105, conds[k], 's', 'start', BLUE)
    return s


if __name__ == '__main__':
    jobs = {
        'acid-names.png': (acid_names(), 1800, 980),
        'carboxyl.png': (carboxyl(), 1800, 880),
        'acetic-tests.png': (acetic_tests(), 1800, 920),
        'formic-acid.png': (formic_acid(), 1800, 880),
        'esterification.png': (esterification(), 1800, 980),
        'fat-structure.png': (fat_structure(), 1800, 920),
        'fat-reactions.png': (fat_reactions(), 1800, 940),
        'soap.png': (soap(), 1800, 920),
        'soap-sms.png': (soap_sms(), 1800, 740),
        'recognition.png': (recognition(), 1800, 1020),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
