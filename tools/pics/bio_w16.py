"""Рисунки недели 16 биологии (course/biology/week-16/pics/*.png): кариотип и определение пола, X и Y, наследование
гемофилии, опыты Моргана с окраской глаз, группы крови, кроссинговер и гаметы, опыт с окраской тела и крыльями,
три типа взаимодействия неаллельных генов.

Факты — по выжимке course/textbooks/bio-16-sex-linkage-interaction.md (Б9 § 38–39; Б10-2 § 71–76). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w16.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


MOD = {'ᴬ': 'A', 'ᴮ': 'B', 'ᴴ': 'H', 'ʰ': 'h', 'ᴰ': 'D', 'ᵈ': 'd', 'ᵂ': 'W', 'ʷ': 'w'}


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = chem(s)
    for m, a in MOD.items():  # аллели при X и I — настоящим верхним индексом, крупнее символов-модификаторов
        s = s.replace(m, f'<tspan baseline-shift="0.55em" font-size="72%">{a}</tspan>')
    return _text(x, y, s, cls, anchor, fill)

OUT = ROOT / 'course' / 'biology' / 'week-16' / 'pics'
XC, YC, AUT = '#D8344A', '#3A57A7', '#BDB8AE'          # X, Y, аутосомы
EYE_R, EYE_W, BODY_G, BODY_B = '#C8263A', '#FFFFFF', '#A39C8F', '#2B2B2B'
DOM, REC = '#2F3E73', '#F08A3C'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def rod(x, y, h, color, w=16):
    return f'<rect x="{x - w / 2:.0f}" y="{y:.0f}" width="{w}" height="{h:.0f}" rx="{w / 2:.0f}" fill="{color}" stroke="{INK}" stroke-width="2"/>'


def person(cx, cy, sex, fill='none', half=False, r=38):
    """Родословная: женщина — круг, мужчина — квадрат; заливка — болен, половина — носительница."""
    clip = f'cl{cx}{cy}'
    if sex == 'f':
        shape = f'<circle cx="{cx}" cy="{cy}" r="{r}"'
        s = f'<clipPath id="{clip}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    else:
        shape = f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}"'
        s = f'<clipPath id="{clip}"><rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}"/></clipPath>'
    s += shape + f' fill="{"#fff" if half or fill == "none" else fill}" stroke="{INK}" stroke-width="4"/>'
    if half:
        s += f'<rect x="{cx}" y="{cy - r}" width="{r}" height="{2 * r}" fill="{RED}" clip-path="url(#{clip})"/>' + shape + f' fill="none" stroke="{INK}" stroke-width="4"/>'
    return s


def fly(cx, cy, eye=EYE_R, body=BODY_G, wings='normal', s=1.0):
    """Схематичная дрозофила сверху: крылья, брюшко, грудь, голова с глазом."""
    if wings == 'normal':
        w = (f'<ellipse cx="{cx - 30 * s:.0f}" cy="{cy + 12 * s:.0f}" rx="{20 * s:.0f}" ry="{52 * s:.0f}" transform="rotate(18 {cx - 30 * s:.0f} {cy + 12 * s:.0f})" '
             f'fill="#E7F0F7" stroke="{INK}" stroke-width="2" opacity=".9"/>'
             f'<ellipse cx="{cx + 30 * s:.0f}" cy="{cy + 12 * s:.0f}" rx="{20 * s:.0f}" ry="{52 * s:.0f}" transform="rotate(-18 {cx + 30 * s:.0f} {cy + 12 * s:.0f})" '
             f'fill="#E7F0F7" stroke="{INK}" stroke-width="2" opacity=".9"/>')
    else:
        w = (f'<ellipse cx="{cx - 22 * s:.0f}" cy="{cy - 6 * s:.0f}" rx="{9 * s:.0f}" ry="{16 * s:.0f}" fill="#E7F0F7" stroke="{INK}" stroke-width="2"/>'
             f'<ellipse cx="{cx + 22 * s:.0f}" cy="{cy - 6 * s:.0f}" rx="{9 * s:.0f}" ry="{16 * s:.0f}" fill="#E7F0F7" stroke="{INK}" stroke-width="2"/>')
    b = (f'<ellipse cx="{cx}" cy="{cy + 22 * s:.0f}" rx="{20 * s:.0f}" ry="{36 * s:.0f}" fill="{body}" stroke="{INK}" stroke-width="2"/>'
         f'<ellipse cx="{cx}" cy="{cy - 14 * s:.0f}" rx="{18 * s:.0f}" ry="{16 * s:.0f}" fill="{body}" stroke="{INK}" stroke-width="2"/>'
         f'<circle cx="{cx}" cy="{cy - 40 * s:.0f}" r="{14 * s:.0f}" fill="{body}" stroke="{INK}" stroke-width="2"/>'
         f'<circle cx="{cx - 10 * s:.0f}" cy="{cy - 43 * s:.0f}" r="{7 * s:.0f}" fill="{eye}" stroke="{INK}" stroke-width="2"/>'
         f'<circle cx="{cx + 10 * s:.0f}" cy="{cy - 43 * s:.0f}" r="{7 * s:.0f}" fill="{eye}" stroke="{INK}" stroke-width="2"/>')
    return w + b


# 1. Кариотип и определение пола ---------------------------------------------------------------------
def karyotype_sex():
    s = text(900, 52, 'Как определяется пол у человека', 'h', 'middle')
    for k, (x, title, sx) in enumerate(((30, 'Женщина: 44 + XX', ('X', 'X')), (620, 'Мужчина: 44 + XY', ('X', 'Y')))):
        s += card(x, 90, 560, 470) + text(x + 280, 140, title, 't', 'middle')
        for i in range(22):
            col, row = i % 11, i // 11
            h = 70 - i * 2.2
            px = x + 50 + col * 44
            py = 190 + row * 120 + (70 - h)
            s += rod(px - 7, py, h, AUT, 11) + rod(px + 7, py, h, AUT, 11)
        s += text(x + 280, 450, '22 пары аутосом', 's', 'middle')
        hx = 75 if sx[1] == 'X' else 40
        s += rod(x + 240, 470, 75, XC, 16) + rod(x + 290, 470 + (75 - hx), hx, XC if sx[1] == 'X' else YC, 16)
        s += text(x + 340, 530, ' '.join(sx), 't', 'start', XC if sx[1] == 'X' else INK)
    # оплодотворение
    s += card(1210, 90, 560, 780)
    s += text(1490, 140, 'Оплодотворение', 't', 'middle')
    rows = [(260, '22 + X', XC, '44 + XX', 'девочка'), (560, '22 + Y', YC, '44 + XY', 'мальчик')]
    for y, sp, col, z, who in rows:
        s += f'<circle cx="1300" cy="{y}" r="50" fill="#F6E3D3" stroke="{INK}" stroke-width="3"/>' + text(1300, y + 8, '22 + X', 's', 'middle')
        s += f'<ellipse cx="1430" cy="{y}" rx="26" ry="16" fill="#fff" stroke="{col}" stroke-width="4"/>'
        s += f'<path d="M1456 {y} q 20 -14 40 0 t 40 0" fill="none" stroke="{col}" stroke-width="3"/>'
        s += text(1440, y - 34, sp, 's', 'middle', col)
        s += arrow(1550, y, 1600, y, INK, 4)
        s += text(1690, y - 6, z, 't', 'middle') + text(1690, y + 32, who, 's', 'middle')
    s += text(1490, 410, 'яйцеклетка + сперматозоид', 'cap', 'middle')
    s += lines_at(1490, 700, ['сперматозоидов 22 + X и 22 + Y поровну —', 'по 50 %; пол ребёнка определяет отец'], 's', step=36)
    s += card(30, 590, 1150, 280)
    s += lines_at(605, 660, ['Женский пол — гомогаметный: все яйцеклетки 22 + X.',
                             'Мужской пол — гетерогаметный: сперматозоиды 22 + X и 22 + Y.',
                             'У птиц и бабочек наоборот: гетерогаметны самки (XY).',
                             'У кузнечиков и клопов самцы X0; у молей самки X0.'], 's', step=48)
    return s


# 2. X и Y: негомологичные участки -------------------------------------------------------------------
def x_y_chromosomes():
    s = text(800, 52, 'X и Y: гены, которых нет в паре', 'h', 'middle')
    s += card(30, 90, 1540, 760)
    # X
    s += f'<rect x="420" y="140" width="80" height="560" rx="40" fill="{XC}" opacity=".85" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="420" y="140" width="80" height="110" rx="40" fill="url(#hatch)" stroke="{INK}" stroke-width="3"/>'
    s += text(460, 760, 'X', 'f', 'middle', XC)
    # Y
    s += f'<rect x="1000" y="140" width="80" height="260" rx="40" fill="{YC}" opacity=".85" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="1000" y="140" width="80" height="110" rx="40" fill="url(#hatch)" stroke="{INK}" stroke-width="3"/>'
    s += text(1040, 460, 'Y', 'f', 'middle', YC)
    s = ('<defs><pattern id="hatch" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<rect width="16" height="16" fill="#F3E9C8"/><line x1="0" y1="0" x2="0" y2="16" stroke="{GREY}" stroke-width="6"/></pattern></defs>') + s
    s += f'<line x1="500" y1="195" x2="1000" y2="195" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
    s += text(750, 180, 'общий участок', 's', 'middle', GREY)
    for y, lbl in ((380, 'ген гемофилии: Xᴴ / Xʰ'), (520, 'ген дальтонизма: Xᴰ / Xᵈ')):
        s += f'<rect x="420" y="{y - 12}" width="80" height="24" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += f'<line x1="420" y1="{y}" x2="360" y2="{y}" stroke="{INK}" stroke-width="2.5"/>' + text(350, y + 9, lbl, 's', 'end')
    for y, lbl in ((300, 'гипертрихоз ушной раковины'), (350, 'перепонки между пальцами ног')):
        s += f'<line x1="1080" y1="{y}" x2="1140" y2="{y}" stroke="{INK}" stroke-width="2.5"/>' + text(1150, y + 9, lbl, 's')
    s += text(1150, 410, '— только от отца сыну', 'cap')
    s += lines_at(1240, 560, ['Для генов этого участка X', 'в Y аллеля нет: у мужчины', 'ген в одном экземпляре —', 'рецессивный аллель проявляется'], 's', step=40)
    s += text(800, 820, 'Сын получает X от матери, Y — от отца; дочь — X от обоих родителей', 't', 'middle')
    return s


# 3. Наследование гемофилии ---------------------------------------------------------------------------
def hemophilia_inheritance():
    s = text(900, 52, 'Мать — носительница гемофилии, отец здоров', 'h', 'middle')
    s += card(30, 90, 1740, 840)
    s += person(700, 190, 'f', half=True) + text(700, 270, 'Xᴴ Xʰ', 't', 'middle') + text(700, 305, 'носительница', 'cap', 'middle')
    s += person(1100, 190, 'm') + text(1100, 270, 'Xᴴ Y', 't', 'middle') + text(1100, 305, 'здоров', 'cap', 'middle')
    s += text(900, 200, '×', 'f', 'middle')
    s += text(150, 200, 'P', 't')
    s += text(150, 400, 'G', 't')
    for x, g, col in ((600, 'Xᴴ', INK), (800, 'Xʰ', RED), (1000, 'Xᴴ', INK), (1200, 'Y', YC)):
        s += f'<circle cx="{x}" cy="390" r="40" fill="#fff" stroke="{col}" stroke-width="3"/>' + text(x, 400, g, 't', 'middle', col)
    s += text(150, 600, 'F₁', 't')
    kids = [(330, 'f', 'none', False, 'Xᴴ Xᴴ', 'здорова'), (690, 'f', 'none', True, 'Xᴴ Xʰ', 'носительница'),
            (1050, 'm', 'none', False, 'Xᴴ Y', 'здоров'), (1410, 'm', RED, False, 'Xʰ Y', 'болен')]
    for x, sex, fill, half, g, st in kids:
        s += person(x, 590, sex, fill, half) + text(x, 670, g, 't', 'middle') + text(x, 705, st, 's', 'middle', RED if fill == RED else INK)
    s += f'<line x1="330" y1="520" x2="1410" y2="520" stroke="{INK}" stroke-width="3"/>'
    s += ''.join(f'<line x1="{x}" y1="520" x2="{x}" y2="552" stroke="{INK}" stroke-width="3"/>' for x in (330, 690, 1050, 1410))
    s += f'<line x1="900" y1="460" x2="900" y2="520" stroke="{INK}" stroke-width="3"/>'
    s += lines_at(900, 790, ['Дочери здоровы, половина — носительницы; половина сыновей больны.',
                             'Больной ребёнок: среди всех детей 1/4, среди сыновей 1/2.'], 't', step=46)
    s += person(250, 880, 'f', half=True, r=16) + text(275, 888, 'носительница', 'cap')
    s += person(520, 880, 'm', RED, r=16) + text(545, 888, 'болен', 'cap')
    return s


# 4. Опыты Моргана с окраской глаз ------------------------------------------------------------------
def morgan_eye_color():
    s = text(900, 52, 'Опыты Т. Моргана: окраска глаз дрозофилы, ген в X', 'h', 'middle')
    crosses = [
        ('Скрещивание 1', (EYE_R, '♀ Xᵂ Xᵂ'), (EYE_W, '♂ Xʷ Y'),
         [(EYE_R, '♀ Xᵂ Xʷ'), (EYE_R, '♂ Xᵂ Y')], 'все красноглазые',
         ['самки: все красноглазые', 'самцы: 1/2 красных, 1/2 белых']),
        ('Скрещивание 2', (EYE_W, '♀ Xʷ Xʷ'), (EYE_R, '♂ Xᵂ Y'),
         [(EYE_R, '♀ Xᵂ Xʷ'), (EYE_W, '♂ Xʷ Y')], 'самки красные, самцы белые',
         ['самки: 1/2 красных, 1/2 белых', 'самцы: 1/2 красных, 1/2 белых'])]
    for k, (title, mom, dad, f1, f1t, f2) in enumerate(crosses):
        x = 30 + k * 880
        s += card(x, 90, 860, 790) + text(x + 430, 140, title, 't', 'middle')
        s += text(x + 40, 260, 'P', 't')
        s += fly(x + 280, 250, mom[0]) + text(x + 280, 360, mom[1], 's', 'middle')
        s += text(x + 430, 260, '×', 'f', 'middle')
        s += fly(x + 580, 250, dad[0]) + text(x + 580, 360, dad[1], 's', 'middle')
        s += text(x + 40, 500, 'F₁', 't')
        s += fly(x + 280, 490, f1[0][0]) + text(x + 280, 600, f1[0][1], 's', 'middle')
        s += fly(x + 580, 490, f1[1][0]) + text(x + 580, 600, f1[1][1], 's', 'middle')
        s += text(x + 430, 650, f1t, 's', 'middle', RED)
        s += text(x + 40, 740, 'F₂', 't')
        s += lines_at(x + 430, 740, f2, 's', step=40)
    s += f'<circle cx="640" cy="985" r="12" fill="{EYE_R}" stroke="{INK}" stroke-width="2"/>' + text(660, 993, 'W — красные (доминантный)', 'cap')
    s += f'<circle cx="1040" cy="985" r="12" fill="{EYE_W}" stroke="{INK}" stroke-width="2"/>' + text(1060, 993, 'w — белые', 'cap')
    s += text(900, 935, 'Самцы получают X только от матери', 't', 'middle')
    return s


# 5. Группы крови AB0 ----------------------------------------------------------------------------------
def blood_groups():
    s = text(900, 52, 'Группы крови AB0: три аллеля, шесть генотипов, четыре группы', 'h', 'middle')
    s += card(30, 90, 620, 820)
    s += text(340, 140, 'Аллели', 't', 'middle')
    for k, (al, col) in enumerate((('Iᴬ', RED), ('Iᴮ', YC), ('i', GREY))):
        s += f'<rect x="{90 + k * 180}" y="170" width="140" height="70" rx="14" fill="#fff" stroke="{col}" stroke-width="4"/>' + text(160 + k * 180, 217, al, 't', 'middle', col)
    s += lines_at(340, 290, ['Iᴬ и Iᴮ доминируют над i,', 'между собой кодоминантны'], 's', step=34)
    rows = [('ii', 'I (0)'), ('IᴬIᴬ, Iᴬi', 'II (A)'), ('IᴮIᴮ, Iᴮi', 'III (B)'), ('IᴬIᴮ', 'IV (AB)')]
    for k, (g, grp) in enumerate(rows):
        y = 420 + k * 110
        s += f'<rect x="80" y="{y - 45}" width="520" height="85" rx="12" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
        s += text(110, y + 8, g, 't') + text(570, y + 8, grp, 't', 'end', GREEN)
    s += text(340, 880, '3 гомозиготы + 3 гетерозиготы = 6', 's', 'middle')
    # эритроциты
    s += card(680, 90, 1090, 820)
    s += text(1225, 140, 'Агглютиногены на эритроцитах и агглютинины в плазме', 't', 'middle')
    groups = [('I (0)', '', 'α и β'), ('II (A)', 'A', 'β'), ('III (B)', 'B', 'α'), ('IV (AB)', 'AB', 'нет')]
    for k, (grp, ag, agl) in enumerate(groups):
        cx = 820 + k * 270
        s += f'<circle cx="{cx}" cy="360" r="95" fill="#E8A3A3" stroke="{INK}" stroke-width="3"/>'
        s += f'<circle cx="{cx}" cy="360" r="45" fill="#F0BEBE"/>'
        for j in range(8):
            a = 2 * math.pi * j / 8
            px, py = cx + 95 * math.cos(a), 360 + 95 * math.sin(a)
            kind = ag[j % len(ag)] if ag else ''
            if kind == 'A':
                s += f'<polygon points="{px:.0f},{py - 16:.0f} {px - 14:.0f},{py + 10:.0f} {px + 14:.0f},{py + 10:.0f}" fill="{RED}" stroke="{INK}" stroke-width="2"/>'
            elif kind == 'B':
                s += f'<rect x="{px - 11:.0f}" y="{py - 11:.0f}" width="22" height="22" fill="{YC}" stroke="{INK}" stroke-width="2"/>'
        s += text(cx, 510, grp, 't', 'middle')
        s += text(cx, 560, 'антигены: ' + (ag.replace('AB', 'A и B') if ag else 'нет'), 's', 'middle')
        s += text(cx, 610, 'плазма: ' + agl, 's', 'middle')
    s += f'<polygon points="900,700 886,726 914,726" fill="{RED}" stroke="{INK}" stroke-width="2"/>' + text(930, 722, 'агглютиноген A', 'cap')
    s += f'<rect x="1210" y="702" width="22" height="22" fill="{YC}" stroke="{INK}" stroke-width="2"/>' + text(1245, 722, 'агглютиноген B', 'cap')
    s += lines_at(1225, 800, ['Несовместимая кровь при переливании — эритроциты склеиваются'], 's', step=34)
    return s


# 6. Сцепленные гены и кроссинговер -------------------------------------------------------------------
def chromatid(x, y, h, color, genes, w=22):
    s = rod(x, y, h, color, w)
    for k, g in enumerate(genes):
        gy = y + h * (0.28 + 0.44 * k)
        s += f'<rect x="{x - w / 2 - 2:.0f}" y="{gy - 5:.0f}" width="{w + 4}" height="10" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
    return s


def linkage_crossing_over():
    s = text(900, 52, 'Кроссинговер в профазе I: новые сочетания сцепленных генов', 'h', 'middle')
    s += card(30, 90, 1740, 820)
    # 1. конъюгация
    s += text(250, 150, '1. Конъюгация гомологов', 't', 'middle')
    for k, (col, gs) in enumerate(((DOM, ('A', 'B')), (DOM, ('A', 'B')), (REC, ('a', 'b')), (REC, ('a', 'b')))):
        s += chromatid(160 + k * 60 + (40 if k > 1 else 0), 200, 380, col, gs)
    for gy, (g1, g2) in ((306, ('A', 'a')), (473, ('B', 'b'))):
        s += text(125, gy + 9, g1, 't', 'end') + text(410, gy + 9, g2, 't')
    # 2. хиазма
    s += text(780, 150, '2. Хиазма и обмен', 't', 'middle')
    s += rod(680, 200, 380, DOM, 22)
    s += f'<path d="M740 200 L740 390 L860 470 L860 580" fill="none" stroke="{DOM}" stroke-width="22" stroke-linecap="round"/>'
    s += f'<path d="M860 200 L860 390 L740 470 L740 580" fill="none" stroke="{REC}" stroke-width="22" stroke-linecap="round"/>'
    s += rod(920, 200, 380, REC, 22)
    s += text(800, 640, 'Х-образная фигура — хиазма', 's', 'middle')
    s += arrow(470, 390, 580, 390, INK, 5) + arrow(1000, 390, 1110, 390, INK, 5)
    # 3. гаметы
    s += text(1440, 150, '3. Четыре типа гамет', 't', 'middle')
    gam = [(DOM, DOM, 'AB', 'некроссоверная'), (DOM, REC, 'Ab', 'кроссоверная'), (REC, DOM, 'aB', 'кроссоверная'), (REC, REC, 'ab', 'некроссоверная')]
    for k, (c1, c2, lbl, kind) in enumerate(gam):
        x = 1230 + k * 140
        s += rod(x, 220, 190, c1, 22) + rod(x, 410, 170, c2, 22)
        s += f'<line x1="{x - 14}" y1="410" x2="{x + 14}" y2="410" stroke="#fff" stroke-width="3"/>'
        s += text(x, 640, lbl, 't', 'middle', RED if kind == 'кроссоверная' else INK)
    s += text(1440, 690, 'AB, ab — некроссоверные; Ab, aB — кроссоверные', 'cap', 'middle')
    s += lines_at(900, 770, ['Чем дальше гены друг от друга, тем чаще между ними кроссинговер.',
                             'Частота кроссинговера = кроссоверные особи × 100 % / все потомки; 1 % = 1 морганида'], 's', step=44)
    return s


# 7. Опыт с окраской тела и формой крыльев -------------------------------------------------------------
def body_wing_cross():
    s = text(900, 52, 'Сцепленное наследование: окраска тела и форма крыльев', 'h', 'middle')
    s += card(30, 90, 1740, 920)
    s += text(90, 230, 'P', 't')
    s += fly(420, 210, EYE_R, BODY_G, 'normal', 1.1) + text(420, 330, 'BBVV — серое тело, нормальные крылья', 's', 'middle')
    s += text(900, 220, '×', 'f', 'middle')
    s += fly(1380, 210, EYE_R, BODY_B, 'short', 1.1) + text(1380, 330, 'bbvv — чёрное тело, зачаточные крылья', 's', 'middle')
    s += text(90, 450, 'F₁', 't')
    s += fly(900, 430, EYE_R, BODY_G, 'normal', 1.0) + text(900, 540, 'BbVv — все серые с нормальными крыльями', 's', 'middle')
    s += text(900, 590, 'Анализирующее: самка F₁ BbVv × самец bbvv', 't', 'middle')
    classes = [(BODY_G, 'normal', 'серые, нормальные', 41.5, DOM), (BODY_B, 'short', 'чёрные, зачаточные', 41.5, DOM),
               (BODY_G, 'short', 'серые, зачаточные', 8.5, RED), (BODY_B, 'normal', 'чёрные, нормальные', 8.5, RED)]
    base = 930
    for k, (body, wing, lbl, pct, col) in enumerate(classes):
        x = 280 + k * 410
        h = pct * 3
        s += f'<rect x="{x - 60}" y="{base - h:.0f}" width="120" height="{h:.0f}" fill="{col}" opacity=".85"/>'
        s += text(x, base - h - 14, f'{pct:g} %'.replace('.', ','), 't', 'middle')
        s += fly(x, 700, EYE_R, body, wing, 0.6)
        s += text(x, base + 34, lbl, 's', 'middle')
    s += f'<line x1="180" y1="{base - 75}" x2="1620" y2="{base - 75}" stroke="{GREY}" stroke-width="3" stroke-dasharray="12 8"/>'
    s += text(1740, base - 83, '25 %', 's', 'end', GREY)
    s += text(1740, base - 51, 'если бы', 'cap', 'end') + text(1740, base - 23, 'независимо', 'cap', 'end')
    s += text(485, 650, 'как у родителей: 83 %', 's', 'middle', DOM)
    s += text(1305, 650, 'новые сочетания: 17 % → 17 морганид', 's', 'middle', RED)
    return s


# 8. Взаимодействие неаллельных генов ---------------------------------------------------------------
def ratio_bar(x, y, w, parts, h=60):
    total = sum(n for n, _, _ in parts)
    s, cx = '', x
    for n, color, lbl in parts:
        pw = w * n / total
        s += f'<rect x="{cx:.0f}" y="{y}" width="{pw:.0f}" height="{h}" fill="{color}" stroke="{INK}" stroke-width="2"/>'
        if pw > 34:
            s += text(cx + pw / 2, y + h / 2 + 10, str(n), 's', 'middle', '#fff' if color in (GREEN, YC, '#6B4226', '#9C6B3A') else INK)
        s += text(cx + pw / 2, y + h + 32, lbl, 'cap', 'middle') if lbl else ''
        cx += pw
    return s


def bird(cx, cy, color, r=40):
    return (f'<ellipse cx="{cx}" cy="{cy + 10}" rx="{r}" ry="{r * 0.75:.0f}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{cx + r * 0.7:.0f}" cy="{cy - r * 0.45:.0f}" r="{r * 0.45:.0f}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
            f'<polygon points="{cx + r * 1.1:.0f},{cy - r * 0.5:.0f} {cx + r * 1.4:.0f},{cy - r * 0.35:.0f} {cx + r * 1.1:.0f},{cy - r * 0.25:.0f}" fill="#E8A33A" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{cx + r * 0.85:.0f}" cy="{cy - r * 0.55:.0f}" r="4" fill="{INK}"/>')


def gene_interaction():
    s = text(900, 52, 'Взаимодействие неаллельных генов', 'h', 'middle')
    titles = [('Комплементарность', 'два доминантных гена дают новый признак'),
              ('Эпистаз', 'ген-супрессор подавляет неаллельный ген'),
              ('Полимерия', 'несколько генов усиливают один признак')]
    for k, (t, sub) in enumerate(titles):
        x = 30 + k * 590
        s += card(x, 90, 560, 900) + text(x + 280, 140, t, 't', 'middle') + text(x + 280, 178, sub, 'cap', 'middle')
    # попугаи
    BLUE, YEL, GRN, WHT = '#4A78C2', '#E8C547', '#3E9B54', '#F7F7F5'
    s += bird(110, 280, BLUE) + text(130, 360, 'синий A_bb', 's', 'middle')
    s += text(310, 290, '×', 't', 'middle')
    s += bird(430, 280, YEL) + text(450, 360, 'жёлтый aaB_', 's', 'middle')
    s += arrow(310, 390, 310, 440, INK, 4)
    s += bird(290, 500, GRN) + text(310, 580, 'F₁ зелёные AaBb', 's', 'middle')
    s += text(310, 650, 'F₂', 't', 'middle')
    s += ratio_bar(70, 680, 480, [(9, GRN, 'зелён.'), (3, BLUE, 'син.'), (3, YEL, 'жёлт.'), (1, WHT, '')])
    s += text(310, 820, 'душистый горошек: 9 красных : 7 белых', 's', 'middle')
    s += ratio_bar(70, 850, 480, [(9, '#C8263A', ''), (7, WHT, '')], 50)
    # эпистаз
    s += lines_at(900, 260, ['C — окраска, c — без пигмента', 'I — подавляет окраску (супрессор)'], 's', step=40)
    s += bird(760, 420, WHT) + text(780, 500, 'I_C_ белые', 's', 'middle')
    s += bird(1010, 420, '#9C6B3A') + text(1030, 500, 'iiC_ окрашенные', 's', 'middle')
    s += text(900, 600, 'IiCc × IiCc → F₂', 't', 'middle')
    s += ratio_bar(660, 640, 480, [(13, WHT, 'белые'), (3, '#9C6B3A', 'окраш.')])
    s += lines_at(900, 790, ['белые: все I_ (12/16)', 'и iicc (1/16) = 13/16'], 's', step=36)
    # полимерия
    shades = ['#6B1F1F', '#A6402F', '#D98A6A', '#EDC3AE', '#FAF3EC']
    for k, col in enumerate(shades):
        x = 1310 + k * 90
        s += f'<ellipse cx="{x}" cy="320" rx="30" ry="44" fill="{col}" stroke="{INK}" stroke-width="3"/>'
        s += text(x, 400, str(4 - k), 's', 'middle')
    s += text(1490, 445, 'число доминантных аллелей', 'cap', 'middle')
    s += text(1490, 520, 'пшеница A₁a₁A₂a₂ × A₁a₁A₂a₂', 's', 'middle')
    s += ratio_bar(1250, 560, 480, [(1, shades[0], ''), (4, shades[1], ''), (6, shades[2], ''), (4, shades[3], ''), (1, shades[4], '')])
    s += text(1490, 670, '1 : 4 : 6 : 4 : 1 — пять фенотипов', 's', 'middle')
    s += text(1490, 760, 'оперённость ног кур: 15 : 1', 's', 'middle')
    s += ratio_bar(1250, 790, 480, [(15, '#9C6B3A', ''), (1, WHT, '')], 50)
    s += text(1490, 900, 'Нильсон-Эле, 1909', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'karyotype-sex.png': (karyotype_sex(), 1800, 900),
        'x-y-chromosomes.png': (x_y_chromosomes(), 1600, 880),
        'hemophilia-inheritance.png': (hemophilia_inheritance(), 1800, 960),
        'morgan-eye-color.png': (morgan_eye_color(), 1800, 1030),
        'blood-groups.png': (blood_groups(), 1800, 940),
        'linkage-crossing-over.png': (linkage_crossing_over(), 1800, 940),
        'body-wing-cross.png': (body_wing_cross(), 1800, 1040),
        'gene-interaction.png': (gene_interaction(), 1800, 1020),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
