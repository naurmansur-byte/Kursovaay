"""Рисунки недели 22 биологии (course/biology/week-22/pics/*.png): микроскоп и разрешение, расчёт размера, ПЦР,
электрофорез, выравнивание, эпигенетика, ЭКО, гибридома, гемодиализ, шкала шума.

Факты — по выжимке course/textbooks/bio-22-biomedicine-methods.md (Б10-1 § 55–57; Б10-2 § 122–124; Б11-2 § 35–56).
Схемы и данные условные. Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w22.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = chem(s.replace('ⁿ', '\x02')).replace('\x02', '<tspan baseline-shift="0.6em" font-size="68%">n</tspan>')
    return _text(x, y, s, cls, anchor, fill)

OUT = ROOT / 'course' / 'biology' / 'week-22' / 'pics'
BLUE, ORANGE, BROWN, VIOLET, PINK = '#3A57A7', '#D98A2B', '#8A5A2B', '#7B3FA0', '#E57373'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32, color=color))


def lead(px, py, tx, ty, s, anchor='start'):
    return (f'<line x1="{px}" y1="{py}" x2="{tx}" y2="{ty - 8}" stroke="{INK}" stroke-width="2"/><circle cx="{px}" cy="{py}" r="5" fill="{INK}"/>'
            + text(tx + (8 if anchor == 'start' else -8), ty, s, 's', anchor))


# 1. Микроскоп и разрешение ---------------------------------------------------------------------------
def microscope():
    s = text(900, 52, 'Микроскоп: увеличение и разрешение', 'h', 'middle')
    s += card(30, 90, 900, 820) + card(950, 90, 820, 820)
    s += f'<rect x="330" y="140" width="70" height="90" rx="10" fill="#B9C4CC" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="345" y="230" width="40" height="230" fill="#DDE3E8" stroke="{INK}" stroke-width="3" transform="rotate(-12 365 345)"/>'
    s += f'<rect x="330" y="455" width="140" height="40" rx="10" fill="#8A8A8A" stroke="{INK}" stroke-width="3"/>'
    s += ''.join(f'<rect x="{350 + j * 40}" y="495" width="22" height="{50 + j * 12}" fill="#B9C4CC" stroke="{INK}" stroke-width="2"/>' for j in range(3))
    s += f'<rect x="250" y="600" width="320" height="24" fill="#3B3833"/>'
    s += f'<path d="M560 200 Q 660 400 560 720" fill="none" stroke="{INK}" stroke-width="22"/>'
    s += f'<rect x="230" y="740" width="420" height="50" rx="10" fill="#3B3833"/><circle cx="410" cy="690" r="26" fill="#F2C230" stroke="{INK}" stroke-width="3"/>'
    s += lead(345, 180, 300, 180, 'окуляр', 'end') + lead(360, 530, 300, 530, 'объективы', 'end')
    s += lead(260, 612, 230, 660, 'столик', 'end') + lead(390, 700, 300, 720, 'свет', 'end')
    s += box(480, 850, 820, 70, 'окуляр ×10, объектив ×40: увеличение 10 × 40 = ×400', '#F7EFC8')
    s += text(1360, 150, 'Разрешение', 't', 'middle')
    for k, (dx, blur, lab, col) in enumerate(((60, 0, 'видны раздельно', GREEN), (18, 14, 'сливаются', RED))):
        cy = 300 + k * 270
        for d in (-1, 1):
            s += f'<circle cx="{1360 + d * dx}" cy="{cy}" r="{24 + blur}" fill="{BLUE}" opacity="{1 if not blur else 0.55}"/>'
        s += text(1360, cy + 90, lab, 's', 'middle', col)
    s += lines_at(1360, 720, ['разрешение — наименьшее расстояние', 'между двумя точками, видимыми раздельно', 'глаз 0,2 мм · световой ~0,2 мкм'], 's', step=36)
    return s


# 2. Расчёт размера ---------------------------------------------------------------------------------
def size_calc():
    s = text(900, 52, 'Реальный размер по микрофотографии', 'h', 'middle')
    s += card(30, 90, 820, 760) + card(870, 90, 900, 760)
    s += f'<rect x="90" y="150" width="700" height="500" fill="#EEF3F6" stroke="{INK}" stroke-width="3"/>'
    s += f'<ellipse cx="440" cy="400" rx="250" ry="170" fill="#DCEFD7" stroke="{INK}" stroke-width="4"/><circle cx="470" cy="390" r="60" fill="#B39DDB" stroke="{INK}" stroke-width="3"/>'
    s += f'<line x1="190" y1="600" x2="690" y2="600" stroke="{RED}" stroke-width="5"/><line x1="190" y1="585" x2="190" y2="615" stroke="{RED}" stroke-width="5"/><line x1="690" y1="585" x2="690" y2="615" stroke="{RED}" stroke-width="5"/>'
    s += text(440, 640, 'на снимке 25 мм', 's', 'middle', RED)
    s += text(440, 720, 'клетка, ×500 (данные условные)', 's', 'middle', GREY)
    s += box(1320, 220, 760, 90, 'реальный размер = изображение : увеличение', '#F7EFC8', cls='t')
    s += lines_at(1320, 360, ['25 мм = 25 000 мкм', '25 000 : 500 = 50 мкм'], 't', step=50)
    s += box(1320, 560, 760, 90, 'увеличение = изображение : реальный размер', '#fff', cls='t')
    s += text(1320, 680, '25 000 мкм : 50 мкм = ×500', 't', 'middle')
    s += text(1320, 780, '1 мм = 1000 мкм · 1 мкм = 1000 нм', 's', 'middle', RED)
    return s


# 3. ПЦР -----------------------------------------------------------------------------------------------
def dsdna(x, y, w=220, sep=0, prim=False, ext=False):
    s = f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="{BLUE}" stroke-width="7"/>'
    s += f'<line x1="{x}" y1="{y + 24 + sep}" x2="{x + w}" y2="{y + 24 + sep}" stroke="{RED}" stroke-width="7"/>'
    if not sep:
        s += ''.join(f'<line x1="{x + 10 + j * 20}" y1="{y + 4}" x2="{x + 10 + j * 20}" y2="{y + 20}" stroke="{GREY}" stroke-width="2"/>' for j in range(11))
    if prim:
        s += f'<line x1="{x + w - 50}" y1="{y + 14}" x2="{x + w}" y2="{y + 14}" stroke="{GREEN}" stroke-width="8"/>'
        s += f'<line x1="{x}" y1="{y + 10 + sep}" x2="{x + 50}" y2="{y + 10 + sep}" stroke="{GREEN}" stroke-width="8"/>'
    if ext:
        s += f'<line x1="{x}" y1="{y + 14}" x2="{x + w}" y2="{y + 14}" stroke="{GREEN}" stroke-width="6" stroke-dasharray="10 6"/>'
        s += f'<line x1="{x}" y1="{y + 10 + sep}" x2="{x + w}" y2="{y + 10 + sep}" stroke="{GREEN}" stroke-width="6" stroke-dasharray="10 6"/>'
    return s


def pcr():
    s = text(900, 52, 'ПЦР: один цикл — удвоение', 'h', 'middle')
    s += card(30, 90, 1740, 520) + card(30, 630, 1740, 300)
    steps = [('Денатурация', '90–97 °C', 'цепи расходятся', 70, False, False, RED),
             ('Отжиг', '50–60 °C', 'праймеры садятся', 70, True, False, BLUE),
             ('Элонгация', '~72 °C', 'полимераза достраивает', 70, False, True, GREEN)]
    s += dsdna(110, 300) + text(220, 260, 'ДНК', 't', 'middle')
    for k, (n, t, d, sep, pr, ex, col) in enumerate(steps):
        x = 460 + k * 440
        s += arrow(x - 110, 320, x - 30, 320, INK, 4)
        s += dsdna(x, 280, 220, sep, pr, ex)
        s += text(x + 110, 200, n, 't', 'middle', col) + text(x + 110, 240, t, 't', 'middle')
        s += text(x + 110, 450, d, 's', 'middle')
    s += lines_at(900, 540, ['смесь: ДНК, два праймера (зелёные), Taq-полимераза, нуклеотиды, Mg²⁺'], 's')
    for k, n in enumerate((1, 2, 4, 8, 16)):
        x = 180 + k * 330
        for j in range(min(n, 8)):
            s += f'<line x1="{x - 60}" y1="{700 + j * 22}" x2="{x + 60}" y2="{700 + j * 22}" stroke="{BLUE if j % 2 == 0 else RED}" stroke-width="5"/>'
        s += text(x, 890, f'{n}' + (' …' if n > 8 else ''), 't', 'middle')
        if k < 4:
            s += arrow(x + 80, 760, x + 250, 760, GREY, 4)
    s += text(1600, 680, 'после n циклов — 2ⁿ копий', 't', 'end', RED)
    return s


# 4. Электрофорез ----------------------------------------------------------------------------------------
def electrophoresis():
    s = text(900, 52, 'Генетический отпечаток: установление отцовства', 'h', 'middle')
    s += card(30, 90, 1000, 820) + card(1050, 90, 720, 820)
    s += f'<rect x="100" y="180" width="860" height="620" rx="12" fill="#DCEBF5" stroke="{INK}" stroke-width="3"/>'
    lanes = [('мать', [2, 5]), ('ребёнок', [2, 4, 7]), ('мужчина 1', [4, 6, 7]), ('мужчина 2', [1, 4, 8])]
    for k, (n, bands) in enumerate(lanes):
        x = 210 + k * 215
        s += text(x, 160, n, 's', 'middle')
        s += f'<rect x="{x - 50}" y="195" width="100" height="18" fill="#3B3833"/>'
        for b in bands:
            y = 230 + b * 62
            s += f'<rect x="{x - 60}" y="{y}" width="120" height="16" rx="6" fill="{VIOLET}"/>'
    for b in range(1, 9):
        s += text(130, 244 + b * 62, str(b), 'cap', 'middle')
    s += text(530, 860, 'полосы условные; фрагменты движутся сверху вниз', 'cap', 'middle')
    s += text(1410, 160, 'Как читать', 't', 'middle')
    s += lines_at(1410, 240, ['каждая полоса ребёнка —', 'от матери или от отца', '', 'полоса 2 — от матери;', 'полосы 4 и 7 ищем у отца', '',
                              'мужчина 1: 4 и 7 есть —', 'не исключён', '', 'мужчина 2: нет полосы 7 —', 'исключён'], 's', step=42)
    s += text(1410, 820, 'совпадение — не доказательство', 's', 'middle', RED)
    return s


# 5. Выравнивание ------------------------------------------------------------------------------------------
def alignment():
    s = text(900, 52, 'Биоинформатика: сравнение последовательностей', 'h', 'middle')
    s += card(30, 90, 1740, 680)
    a, b = 'ATGCTAGCTAGGA', 'ATGCTTGCTACGA'
    for k, (ca, cb) in enumerate(zip(a, b)):
        x = 200 + k * 110
        same = ca == cb
        fill = '#E2F1E6' if same else '#FDE3E4'
        s += f'<rect x="{x - 40}" y="220" width="80" height="80" rx="10" fill="{fill}" stroke="{INK}" stroke-width="2"/>' + text(x, 275, ca, 'f', 'middle')
        s += f'<rect x="{x - 40}" y="400" width="80" height="80" rx="10" fill="{fill}" stroke="{INK}" stroke-width="2"/>' + text(x, 455, cb, 'f', 'middle')
        s += text(x, 360, '|' if same else '×', 't', 'middle', GREEN if same else RED)
    s += text(110, 270, 'вид 1', 's', 'end') + text(110, 450, 'вид 2', 's', 'end')
    s += text(900, 570, '11 из 13 совпадают — последовательности сходны (данные условные)', 't', 'middle')
    s += lines_at(900, 650, ['сходство последовательностей — основание для гипотезы о родстве и функции;', 'гипотезу проверяют опытом'], 's', step=40)
    return s


# 6. Эпигенетика ------------------------------------------------------------------------------------------
def nucleosome(cx, cy, tight=True, ac=False):
    s = f'<circle cx="{cx}" cy="{cy}" r="38" fill="#F7EFC8" stroke="{INK}" stroke-width="3"/>'
    if ac:
        s += ''.join(f'<text x="{cx + 30 * math.cos(a)}" y="{cy + 30 * math.sin(a) + 8}" text-anchor="middle" style="font: 800 20px Manrope; fill:{GREEN}">Ac</text>' for a in (0.5, 2.6, 4.4))
    return s


def epigenetics():
    s = text(900, 52, 'Эпигенетика: ген выключен или включён без изменения ДНК', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 150, 'Метилирование ДНК', 't', 'middle', RED)
    s += f'<line x1="90" y1="380" x2="830" y2="380" stroke="{BLUE}" stroke-width="10"/>'
    s += f'<rect x="150" y="360" width="250" height="40" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 6"/>' + text(275, 440, 'промотор', 's', 'middle', GREY)
    s += f'<rect x="460" y="360" width="320" height="40" fill="#DCEBF5" stroke="{INK}" stroke-width="2"/>' + text(620, 440, 'ген', 's', 'middle')
    for j in range(4):
        x = 180 + j * 60
        s += f'<line x1="{x}" y1="360" x2="{x}" y2="300" stroke="{RED}" stroke-width="4"/><circle cx="{x}" cy="290" r="18" fill="{RED}"/>' + text(x, 297, 'CH₃', 'cap', 'middle').replace('class="cap"', 'class="cap" style="fill:#fff;font-size:15px"')
    s += arrow(470, 560, 760, 560, GREY, 5) + f'<line x1="560" y1="520" x2="660" y2="600" stroke="{RED}" stroke-width="8"/><line x1="660" y1="520" x2="560" y2="600" stroke="{RED}" stroke-width="8"/>'
    s += text(615, 650, 'транскрипции нет', 's', 'middle', RED)
    s += lines_at(460, 740, ['CH₃ на цитозинах промотора —', 'ген выключен; последовательность та же'], 's', step=36)
    s += text(1340, 150, 'Ацетилирование гистонов', 't', 'middle', GREEN)
    s += text(1130, 230, 'плотно — ген закрыт', 's', 'middle') + text(1560, 230, 'Ac — хроматин раскрыт', 's', 'middle', GREEN)
    for j in range(3):
        s += nucleosome(1060 + j * 70, 360)
    s += f'<path d="M1010 330 {" ".join(f"Q {1030 + j * 70} {300 if j % 2 else 420} {1060 + j * 70 + 35} 360" for j in range(3))}" fill="none" stroke="{BLUE}" stroke-width="5"/>'
    for j in range(3):
        s += nucleosome(1450 + j * 120, 360, False, True)
    s += f'<line x1="1400" y1="360" x2="1740" y2="360" stroke="{BLUE}" stroke-width="5"/>'
    for j in range(3):
        s += nucleosome(1450 + j * 120, 360, False, True)
    s += arrow(1500, 560, 1720, 560, GREEN, 5) + text(1610, 610, 'транскрипция идёт', 's', 'middle', GREEN)
    s += lines_at(1340, 740, ['ацетилирование ослабляет связь ДНК', 'с гистонами — ген доступен'], 's', step=36)
    return s


# 7. ЭКО ---------------------------------------------------------------------------------------------------
def ivf():
    s = text(900, 52, 'ЭКО: оплодотворение вне организма', 'h', 'middle')
    steps = ['1. гормональная|стимуляция', '2. извлечение|яйцеклеток', '3. оплодотворение|в питательной среде', '4. перенос эмбриона|в матку']
    for k, lab in enumerate(steps):
        x = 30 + k * 440
        cx = x + 205
        s += card(x, 90, 410, 640)
        if k == 0:
            s += f'<ellipse cx="{cx}" cy="300" rx="110" ry="80" fill="#FDE3E4" stroke="{INK}" stroke-width="3"/>' + ''.join(f'<circle cx="{cx - 60 + j * 40}" cy="{290 + (j % 2) * 30}" r="16" fill="#F7EFC8" stroke="{INK}" stroke-width="2"/>' for j in range(4))
        elif k == 1:
            s += f'<line x1="{cx - 120}" y1="200" x2="{cx + 20}" y2="330" stroke="{GREY}" stroke-width="6"/><circle cx="{cx + 40}" cy="350" r="26" fill="#F7EFC8" stroke="{INK}" stroke-width="3"/>'
        elif k == 2:
            s += f'<ellipse cx="{cx}" cy="330" rx="140" ry="50" fill="#DCEBF5" stroke="{INK}" stroke-width="3"/><circle cx="{cx}" cy="320" r="34" fill="#F7EFC8" stroke="{INK}" stroke-width="3"/>'
            s += ''.join(f'<path d="M{cx - 110 + j * 30} {300 + j * 8} q 10 -6 20 0" fill="none" stroke="{INK}" stroke-width="3"/><circle cx="{cx - 112 + j * 30}" cy="{300 + j * 8}" r="5" fill="{INK}"/>' for j in range(3))
        else:
            s += f'<path d="M{cx - 90} 230 Q {cx} 450 {cx + 90} 230" fill="#FDE3E4" stroke="{INK}" stroke-width="3"/>'
            s += f'<line x1="{cx}" y1="460" x2="{cx}" y2="330" stroke="{GREY}" stroke-width="6"/>' + ''.join(f'<circle cx="{cx - 9 + (j % 2) * 18}" cy="{310 + (j // 2) * 16}" r="9" fill="#F7EFC8" stroke="{INK}" stroke-width="2"/>' for j in range(4))
        s += lines_at(cx, 560, lab.split('|'), 's', step=34)
        if k < 3:
            s += arrow(x + 400, 330, x + 450, 330, INK, 4)
    s += lines_at(900, 790, ['1978 — Луиза Браун (Эдвардс и Стептоу); ИКСИ — один сперматозоид в яйцеклетку',
                             'этика: лишние эмбрионы, выбор пола, донорство, многоплодие'], 's', step=40)
    return s


# 8. Гибридома ------------------------------------------------------------------------------------------
def antibody(cx, cy, sc=1.0, col=BLUE):
    s = ''
    for d in (-1, 1):
        s += f'<line x1="{cx}" y1="{cy}" x2="{cx + d * 50 * sc}" y2="{cy - 70 * sc}" stroke="{col}" stroke-width="{10 * sc:.0f}"/>'
        s += f'<line x1="{cx + d * 20 * sc}" y1="{cy - 20 * sc}" x2="{cx + d * 70 * sc}" y2="{cy - 80 * sc}" stroke="{ORANGE}" stroke-width="{7 * sc:.0f}"/>'
    s += f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy + 70 * sc}" stroke="{col}" stroke-width="{10 * sc:.0f}"/>'
    return s


def hybridoma():
    s = text(900, 52, 'Моноклональные антитела: гибридома', 'h', 'middle')
    s += card(30, 90, 1260, 820) + card(1310, 90, 460, 820)
    s += f'<ellipse cx="160" cy="260" rx="90" ry="50" fill="#D9D3C7" stroke="{INK}" stroke-width="3"/>' + text(160, 345, 'мышь + антиген X', 's', 'middle')
    s += arrow(260, 260, 330, 260, INK, 4)
    s += f'<circle cx="400" cy="260" r="50" fill="#DCEBF5" stroke="{INK}" stroke-width="3"/>' + text(400, 270, 'B', 't', 'middle', BLUE)
    s += text(400, 345, 'B-лимфоцит:', 's', 'middle') + text(400, 380, 'нужное антитело', 's', 'middle', BLUE)
    s += f'<circle cx="400" cy="560" r="50" fill="#FDE3E4" stroke="{INK}" stroke-width="3"/>' + text(400, 572, '∞', 't', 'middle', RED)
    s += text(400, 645, 'плазмоцитома:', 's', 'middle') + text(400, 680, 'бессмертие', 's', 'middle', RED)
    s += arrow(460, 280, 590, 390, INK, 4) + arrow(460, 540, 590, 430, INK, 4)
    s += f'<ellipse cx="660" cy="410" rx="70" ry="56" fill="#E6D3EE" stroke="{INK}" stroke-width="3"/>' + text(660, 420, 'B∞', 't', 'middle', VIOLET)
    s += text(660, 510, 'гибридома', 's', 'middle', VIOLET)
    s += arrow(740, 410, 830, 410, INK, 4) + text(785, 390, 'ГАТ', 's', 'middle')
    s += f'<rect x="840" y="330" width="170" height="160" rx="12" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    s += ''.join(f'<circle cx="{875 + (j % 3) * 50}" cy="{370 + (j // 3) * 50}" r="16" fill="#E6D3EE" stroke="{INK}" stroke-width="2"/>' for j in range(6))
    s += lines_at(925, 530, ['выживают', 'только гибридомы'], 's', step=32)
    s += arrow(1020, 410, 1100, 410, INK, 4)
    s += ''.join(antibody(1140 + (j % 2) * 70, 360 + (j // 2) * 120, 0.55) for j in range(4))
    s += lines_at(1180, 640, ['клон — одинаковые', 'антитела к X'], 's', step=32)
    s += text(660, 820, 'Кёлер и Мильштейн, 1975; ИФА, тесты, лечение опухолей', 's', 'middle')
    s += text(1540, 150, 'Антитело', 't', 'middle')
    s += antibody(1540, 450, 2.0)
    s += text(1420, 270, 'лёгкие', 's', 'middle', ORANGE) + text(1660, 270, 'цепи', 's', 'middle', ORANGE)
    s += text(1540, 660, 'две тяжёлые (синие)', 's', 'middle', BLUE) + text(1540, 700, 'и две лёгкие цепи', 's', 'middle', ORANGE)
    s += lines_at(1540, 780, ['концы «рогаток» —', 'связывают антиген'], 's', step=32)
    return s


# 9. Гемодиализ -----------------------------------------------------------------------------------------
def dialysis():
    s = text(900, 52, 'Гемодиализ — «искусственная почка»', 'h', 'middle')
    s += card(30, 90, 1740, 780)
    s += f'<rect x="120" y="200" width="1560" height="180" fill="#FDE3E4" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="120" y="440" width="1560" height="180" fill="#DCEBF5" stroke="{INK}" stroke-width="3"/>'
    s += f'<line x1="120" y1="410" x2="1680" y2="410" stroke="{INK}" stroke-width="6" stroke-dasharray="20 12"/>'
    s += text(900, 170, 'кровь →', 't', 'middle', RED) + text(900, 660, '← диализирующий раствор (без мочевины)', 't', 'middle', BLUE)
    s += text(1700, 418, 'мембрана', 's', 'end').replace('x="1700"', 'x="1670"').replace('y="418"', 'y="400"')
    for j in range(6):
        x = 250 + j * 230
        s += f'<circle cx="{x}" cy="260" r="34" fill="{PINK}" stroke="{INK}" stroke-width="2"/>' if j % 2 == 0 else f'<ellipse cx="{x}" cy="260" rx="44" ry="22" fill="#F2C230" stroke="{INK}" stroke-width="2"/>'
        s += f'<circle cx="{x + 90}" cy="320" r="9" fill="{BROWN}"/>'
        s += arrow(x + 90, 335, x + 90, 520, BROWN, 3)
        s += f'<circle cx="{x + 90}" cy="540" r="9" fill="{BROWN}"/>'
    s += text(250, 330, 'клетки', 'cap', 'middle') + text(480, 310, 'белки', 'cap', 'middle')
    s += lines_at(900, 730, ['мочевина и соли (коричневые точки) уходят диффузией — из большей концентрации в меньшую;',
                             'белки и клетки крови через мембрану не проходят и остаются в крови'], 's', step=42)
    return s


# 10. Шум --------------------------------------------------------------------------------------------------
def noise():
    s = text(900, 52, 'Шум: шкала в децибелах', 'h', 'middle')
    s += card(30, 90, 1740, 680)
    x0, x1, y = 120, 1680, 420
    for k in range(101):
        pass
    grad = [(0, '#5DAA6F'), (30, '#5DAA6F'), (80, '#F2C230'), (110, ORANGE), (130, RED), (150, '#8E1A1A')]
    for (a, ca), (b, _) in zip(grad, grad[1:]):
        xa, xb = x0 + a / 150 * (x1 - x0), x0 + b / 150 * (x1 - x0)
        s += f'<rect x="{xa:.0f}" y="{y - 30}" width="{xb - xa:.0f}" height="60" fill="{ca}"/>'
    for v in range(0, 151, 10):
        x = x0 + v / 150 * (x1 - x0)
        s += f'<line x1="{x:.0f}" y1="{y + 30}" x2="{x:.0f}" y2="{y + 45}" stroke="{INK}" stroke-width="2"/>' + text(x, y + 75, str(v), 'cap', 'middle')
    marks = [(25, '20–30 дБ', 'безвредный фон', -1), (80, '≈ 80 дБ', 'допустимо', 1), (100, '90–110 дБ', 'производственный шум', -1),
             (130, '130 дБ', 'болевой порог', 1), (150, '150 дБ', 'непереносимо', -1)]
    for v, n, d, side in marks:
        x = x0 + v / 150 * (x1 - x0)
        ty = y - 120 if side < 0 else y + 170
        s += f'<line x1="{x:.0f}" y1="{y - 30 if side < 0 else y + 30}" x2="{x:.0f}" y2="{ty + (30 if side < 0 else -50)}" stroke="{INK}" stroke-width="2"/>'
        anc = 'end' if v == 150 else 'middle'
        s += text(x, ty - 10, n, 't', anc) + text(x, ty + 25, d, 's', anc)
    s += lines_at(900, 700, ['звук — 16–20 000 Гц; выше — ультразвук, ниже — инфразвук',
                             'шум накапливается: снижает слух и утомляет нервную систему'], 's', step=40)
    return s


if __name__ == '__main__':
    jobs = {
        'microscope.png': (microscope(), 1800, 940),
        'size-calc.png': (size_calc(), 1800, 880),
        'pcr.png': (pcr(), 1800, 960),
        'electrophoresis.png': (electrophoresis(), 1800, 940),
        'alignment.png': (alignment(), 1800, 800),
        'epigenetics.png': (epigenetics(), 1800, 940),
        'ivf.png': (ivf(), 1800, 880),
        'hybridoma.png': (hybridoma(), 1800, 940),
        'dialysis.png': (dialysis(), 1800, 900),
        'noise.png': (noise(), 1800, 800),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
