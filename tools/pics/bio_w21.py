"""Рисунки недели 21 биологии (course/biology/week-21/pics/*.png): бактериальная клетка и спора, формы бактерий,
бактериофаг, средства против микробов, пищевая биотехнология, стерилизация, посев по Дригальскому, окраска по Граму,
рекомбинантная ДНК, клонирование Долли, микроклональное размножение.

Факты — по выжимке course/textbooks/bio-21-microbes-biotech.md (Б7а § 60–63; Б7м § 63–66; Б11-2 § 39–48). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w21.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    return _text(x, y, chem(s), cls, anchor, fill)

OUT = ROOT / 'course' / 'biology' / 'week-21' / 'pics'
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


def rod(cx, cy, w=90, h=34, fill='#C9E3C9', rot=0):
    return f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="{h / 2:.0f}" fill="{fill}" stroke="{INK}" stroke-width="2.5" transform="rotate({rot} {cx} {cy})"/>'


def coc(cx, cy, r=18, fill='#C9E3C9'):
    return f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'


def dish(cx, cy, r=150, fill='#F7EFC8'):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 12}" fill="none" stroke="{GREY}" stroke-width="2"/>')


def tube(cx, top, fill, h=240):
    return f'<path d="M{cx - 30} {top} V {top + h - 30} A 30 30 0 0 0 {cx + 30} {top + h - 30} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'


# 1. Бактериальная клетка ----------------------------------------------------------------------------
def bacterium():
    s = text(900, 52, 'Бактериальная клетка и спора', 'h', 'middle')
    s += card(30, 90, 1140, 760) + card(1190, 90, 580, 760)
    cx, cy = 560, 430
    s += f'<rect x="{cx - 330}" y="{cy - 170}" width="660" height="340" rx="170" fill="#E9F1E2" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
    s += f'<rect x="{cx - 300}" y="{cy - 140}" width="600" height="280" rx="140" fill="#C9E3C9" stroke="{INK}" stroke-width="8"/>'
    s += f'<rect x="{cx - 285}" y="{cy - 125}" width="570" height="250" rx="125" fill="#DCEFD7" stroke="{BLUE}" stroke-width="3"/>'
    s += f'<path d="M{cx - 120} {cy} c 40 -90 120 -60 140 -10 s 100 70 60 100 s -140 30 -170 -20 s -50 -40 -30 -70" fill="none" stroke="{RED}" stroke-width="5"/>'
    s += ''.join(f'<circle cx="{cx - 220 + (j * 67) % 440}" cy="{cy - 80 + (j * 41) % 160}" r="7" fill="{BROWN}"/>' for j in range(14))
    s += f'<path d="M{cx + 300} {cy} c 60 -40 90 40 150 0 s 90 40 140 0" fill="none" stroke="{INK}" stroke-width="5"/>'
    s += lead(cx - 300, cy - 150, 90, 160, 'капсула') + lead(cx - 200, cy - 132, 330, 160, 'клеточная стенка (муреин)')
    s += lead(cx - 270, cy + 60, 90, 720, 'мембрана') + lead(cx - 90, cy + 20, 330, 720, 'кольцевая ДНК — ядра нет')
    s += lead(cx + 180, cy + 60, 720, 720, 'рибосомы') + lead(cx + 400, cy - 10, 980, 230, 'жгутик', 'end')
    s += text(1480, 150, 'Спора', 't', 'middle')
    for k, (y, lab) in enumerate(((250, 'неблагоприятные|условия'), (470, 'содержимое сжимается,|плотная оболочка'), (690, 'хорошие условия —|спора прорастает'))):
        s += f'<rect x="1300" y="{y - 50}" width="160" height="80" rx="40" fill="#DCEFD7" stroke="{INK}" stroke-width="3"/>'
        if k == 1:
            s += f'<ellipse cx="1380" cy="{y - 10}" rx="40" ry="26" fill="{BROWN}" stroke="{INK}" stroke-width="6"/>'
        s += lines_at(1610, y - 20, lab.split('|'), 's', step=32)
        if k < 2:
            s += arrow(1380, y + 36, 1380, y + 160, INK, 4)
    s += text(1480, 815, 'спора — переживание, не размножение', 's', 'middle', RED)
    return s


# 2. Формы бактерий ---------------------------------------------------------------------------------
def bacteria_forms():
    s = text(900, 52, 'Формы бактерий', 'h', 'middle')
    data = [('Диплококки', 'по две', 'diplo'), ('Стрептококки', 'цепочка · молочнокислые', 'strepto'),
            ('Стафилококки', 'гроздь', 'staph'), ('Бациллы', 'палочки · сенная палочка,|палочка Коха', 'rod'),
            ('Спириллы', 'извитые', 'spir'), ('Вибрионы', 'запятая · холерный вибрион', 'vib')]
    for k, (n, d, kind) in enumerate(data):
        x = 30 + (k % 3) * 590
        y = 90 + (k // 3) * 420
        s += card(x, y, 560, 390)
        cx, cy = x + 280, y + 170
        if kind == 'diplo':
            s += ''.join(coc(cx - 120 + j * 120 + dx, cy + (j % 2) * 30, 22) for j in range(3) for dx in (-21, 21))
        elif kind == 'strepto':
            s += ''.join(coc(cx - 180 + j * 40, cy + 30 * math.sin(j / 1.5), 20) for j in range(10))
        elif kind == 'staph':
            pts = [(0, 0), (40, 0), (-40, 0), (20, -34), (-20, -34), (20, 34), (-20, 34), (60, -34), (-60, 34), (0, -68), (60, 34)]
            s += ''.join(coc(cx + a, cy + b, 20) for a, b in pts)
        elif kind == 'rod':
            s += ''.join(rod(cx - 140 + j * 140, cy + (j % 2) * 40 - 20, 110, 34, '#C9E3C9', (j * 25) % 50 - 20) for j in range(3))
        elif kind == 'spir':
            for j in range(2):
                pts = ' '.join(f'{cx - 150 + t * 3:.0f},{cy - 40 + j * 80 + 20 * math.sin(t / 6):.0f}' for t in range(100))
                s += f'<polyline points="{pts}" fill="none" stroke="{GREEN}" stroke-width="10" stroke-linecap="round"/>'
        else:
            for j in range(3):
                bx = cx - 150 + j * 140
                s += f'<path d="M{bx} {cy + 20} q 30 -60 80 -40" fill="none" stroke="{GREEN}" stroke-width="18" stroke-linecap="round"/>'
                s += f'<path d="M{bx + 80} {cy - 20} q 30 -10 50 10" fill="none" stroke="{INK}" stroke-width="3"/>'
        s += text(cx, y + 300, n, 't', 'middle') + lines_at(cx, y + 340, d.split('|'), 's', step=30, color=GREY)
    return s


# 3. Бактериофаг ---------------------------------------------------------------------------------------
def phage_icon(cx, cy, sc=1.0):
    r = 40 * sc
    pts = ' '.join(f'{cx + r * math.cos(math.radians(60 * k)):.0f},{cy + r * math.sin(math.radians(60 * k)):.0f}' for k in range(6))
    s = f'<polygon points="{pts}" fill="#F7EFC8" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M{cx - 12 * sc} {cy - 10 * sc} q {12 * sc} {-14 * sc} {24 * sc} 0 q {-12 * sc} {14 * sc} {-24 * sc} {20 * sc}" fill="none" stroke="{RED}" stroke-width="{3 * sc:.1f}"/>'
    s += f'<rect x="{cx - 8 * sc:.0f}" y="{cy + r - 2:.0f}" width="{16 * sc:.0f}" height="{60 * sc:.0f}" fill="#B9C4CC" stroke="{INK}" stroke-width="2.5"/>'
    for d in (-1, 1):
        s += f'<path d="M{cx} {cy + r + 58 * sc:.0f} l {d * 40 * sc:.0f} {30 * sc:.0f} l {d * 10 * sc:.0f} {20 * sc:.0f}" fill="none" stroke="{INK}" stroke-width="3"/>'
    return s


def phage():
    s = text(900, 52, 'Бактериофаг: заражение бактерии', 'h', 'middle')
    s += card(30, 90, 420, 760) + card(470, 90, 1300, 760)
    s += phage_icon(240, 300, 1.8)
    s += lead(240, 300, 300, 160, 'ДНК в капсиде') + lead(240, 430, 300, 520, 'отросток')
    s += lines_at(240, 680, ['вирус — не клетка:', 'ДНК или РНК', 'в белковой оболочке'], 's', step=36)
    steps = ['прикрепление', 'ввод ДНК — оболочка|снаружи', 'синтез ДНК|и белков фага', 'сборка фагов', 'клетка разрушается,|фаги выходят']
    for k, lab in enumerate(steps):
        cx = 600 + k * 250
        s += f'<rect x="{cx - 100}" y="420" width="200" height="190" rx="60" fill="#DCEFD7" stroke="{INK}" stroke-width="3"' + (' stroke-dasharray="14 10"' if k == 4 else '') + '/>'
        if k < 2:
            s += phage_icon(cx, 300, 0.9)
        if k == 1:
            s += f'<path d="M{cx} 400 q 10 60 -20 90 q -30 30 10 60" fill="none" stroke="{RED}" stroke-width="4"/>'
        if k == 2:
            s += ''.join(f'<path d="M{cx - 60 + j * 30} 480 q 10 -14 20 0" fill="none" stroke="{RED}" stroke-width="3"/>' for j in range(5))
            s += ''.join(f'<rect x="{cx - 60 + j * 30}" y="540" width="14" height="24" fill="#B9C4CC" stroke="{INK}" stroke-width="1.5"/>' for j in range(5))
        if k == 3:
            s += ''.join(phage_icon(cx - 50 + (j % 3) * 50, 470 + (j // 3) * 70, 0.35) for j in range(6))
        if k == 4:
            s += ''.join(phage_icon(cx - 80 + j * 55, 330 + (j % 2) * 30, 0.4) for j in range(4))
        s += text(cx, 680, f'{k + 1}', 't', 'middle', RED) + lines_at(cx, 725, lab.split('|'), 's', step=32)
        if k < 4:
            s += arrow(cx + 104, 515, cx + 146, 515, INK, 3)
    return s


# 4. Средства против микробов --------------------------------------------------------------------
def fight_microbes():
    s = text(900, 52, 'Против микробов: где и чем', 'h', 'middle')
    items = [('Дезинфекция', 'неживые предметы', 'хлор, спирты, кислоты', BLUE),
             ('Антисептик', 'рана, кожа', 'йод, зелёнка, перекись 3 %', GREEN),
             ('Антибиотик', 'внутри организма', 'пенициллин; на вирусы — нет', RED)]
    for k, (n, where, ex, col) in enumerate(items):
        x = 30 + k * 590
        cx = x + 280
        s += card(x, 90, 560, 430)
        s += text(cx, 160, n, 't', 'middle', col)
        if k == 0:
            s += f'<rect x="{cx - 140}" y="250" width="280" height="30" fill="{BROWN}"/><line x1="{cx - 120}" y1="280" x2="{cx - 120}" y2="360" stroke="{BROWN}" stroke-width="10"/><line x1="{cx + 120}" y1="280" x2="{cx + 120}" y2="360" stroke="{BROWN}" stroke-width="10"/>'
            s += ''.join(f'<circle cx="{cx - 60 + j * 30}" cy="{220 - (j % 2) * 15}" r="6" fill="{BLUE}"/>' for j in range(5))
        elif k == 1:
            s += f'<rect x="{cx - 150}" y="250" width="300" height="90" rx="40" fill="#F3D3B8" stroke="{INK}" stroke-width="3"/><line x1="{cx - 40}" y1="295" x2="{cx + 40}" y2="295" stroke="{RED}" stroke-width="6"/>'
            s += f'<rect x="{cx + 60}" y="200" width="50" height="70" rx="8" fill="#5A3A1A" stroke="{INK}" stroke-width="2"/>'
        else:
            s += f'<rect x="{cx - 90}" y="260" width="180" height="70" rx="35" fill="#fff" stroke="{INK}" stroke-width="3"/><rect x="{cx}" y="260" width="90" height="70" rx="35" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
        s += text(cx, 420, where, 't', 'middle') + text(cx, 465, ex, 's', 'middle', GREY)
    s += card(30, 540, 1740, 380)
    rows = [('воздушно-капельный', 'ангина', 'повязка, проветривание, изоляция больного'),
            ('вода, пища, руки, мухи', 'холера, брюшной тиф', 'кипячёная вода, мытьё рук и овощей'),
            ('больные животные', 'бруцеллёз, сибирская язва', 'пастеризованное молоко, проваренное мясо'),
            ('почва, раны, консервы', 'столбняк, ботулизм', 'рана с землёй — к врачу; не есть сомнительные консервы')]
    s += text(300, 600, 'путь заражения', 's', 'middle', GREY) + text(780, 600, 'болезнь', 's', 'middle', GREY) + text(1350, 600, 'профилактика', 's', 'middle', GREY)
    for k, (a, b, c) in enumerate(rows):
        y = 660 + k * 66
        s += text(300, y, a, 's', 'middle') + text(780, y, b, 's', 'middle', RED) + text(1350, y, c, 's', 'middle')
    return s


# 5. Пищевая биотехнология ---------------------------------------------------------------------------
def yeast(cx, cy):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="26" fill="#F7EFC8" stroke="{INK}" stroke-width="2.5"/>'
            f'<ellipse cx="{cx + 36}" cy="{cy - 18}" rx="16" ry="12" fill="#F7EFC8" stroke="{INK}" stroke-width="2.5"/>')


def food_biotech():
    s = text(900, 52, 'Продукт — микроорганизм — процесс', 'h', 'middle')
    data = [('Йогурт', 'болгарская палочка|+ термофильный стрептококк', 'молочнокислое брожение', 'yog'),
            ('Сыр', 'кисломолочный — бактерии;|сычужный — сычужный фермент', 'свёртывание молока,|созревание', 'cheese'),
            ('Кумыс', 'молочнокислые бактерии|+ дрожжи', 'молочнокислое|и спиртовое брожение', 'kumys')]
    for k, (n, who, proc, kind) in enumerate(data):
        x = 30 + k * 590
        cx = x + 280
        s += card(x, 90, 560, 760)
        s += text(cx, 160, n, 'h', 'middle')
        if kind == 'yog':
            s += rod(cx - 80, 280, 110, 30) + rod(cx - 60, 330, 110, 30, '#C9E3C9', 20)
            s += ''.join(coc(cx + 40 + j * 34, 300, 15) for j in range(4))
        elif kind == 'cheese':
            s += f'<polygon points="{cx - 120},350 {cx + 120},350 {cx + 120},280 {cx - 120},240" fill="#F2C230" stroke="{INK}" stroke-width="3"/>'
            s += ''.join(f'<circle cx="{cx - 70 + j * 50}" cy="{310 - (j % 2) * 20}" r="10" fill="#E0A800"/>' for j in range(4))
        else:
            s += ''.join(rod(cx - 120 + j * 70, 260 + (j % 2) * 30, 70, 24) for j in range(3)) + yeast(cx + 80, 320)
        s += lines_at(cx, 450, who.split('|'), 's', step=36)
        s += f'<line x1="{x + 60}" y1="530" x2="{x + 500}" y2="530" stroke="{GREY}" stroke-width="2"/>'
        s += lines_at(cx, 590, proc.split('|'), 't', step=40, color=GREEN)
    s += text(900, 900, 'Кумыс — кобылье молоко, шубат — верблюжье; уксус из вина — уксуснокислые бактерии', 's', 'middle')
    return s


# 6. Стерилизация --------------------------------------------------------------------------------------
def sterilization():
    s = text(900, 52, 'Стерилизация: способ под объект', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 150, 'Автоклав — пар под давлением', 't', 'middle', BLUE)
    s += f'<rect x="270" y="320" width="380" height="420" rx="40" fill="#DCEBF5" stroke="{INK}" stroke-width="5"/>'
    s += f'<rect x="250" y="275" width="420" height="50" rx="14" fill="#B9C4CC" stroke="{INK}" stroke-width="4"/>'
    s += f'<circle cx="460" cy="225" r="38" fill="#fff" stroke="{INK}" stroke-width="4"/><line x1="460" y1="225" x2="485" y2="203" stroke="{RED}" stroke-width="5"/>'
    s += text(515, 215, '1 атм', 't', 'start', RED)
    s += ''.join(f'<path d="M{330 + j * 70} 650 q 15 -30 0 -60 q -15 -30 0 -60" fill="none" stroke="#7FB3E0" stroke-width="5"/>' for j in range(4))
    s += text(460, 790, '121 °C — гибнут и споры', 't', 'middle', RED)
    s += text(460, 840, 'среды, растворы, бельё', 's', 'middle')
    rows = [('прокаливание в пламени', 'петли, металл'), ('сухой жар 160–170 °C', 'стеклянная посуда'),
            ('кипячение 30 мин', 'споры выживают'), ('текучий пар дробно', 'среды с сахарами'),
            ('пастеризация', 'молоко; споры живы'), ('фильтрование', 'не выносит нагрева'), ('окись этилена', 'пластмасса')]
    for k, (a, b) in enumerate(rows):
        y = 190 + k * 95
        s += f'<rect x="950" y="{y - 40}" width="780" height="80" rx="12" fill="{"#fff" if k % 2 else "#F7F5EF"}"/>'
        s += text(980, y + 10, a, 's') + text(1700, y + 10, b, 's', 'end', RED if 'спор' in b else GREY)
    s += lines_at(1340, 850, ['стерилизация — все микробы и споры;', 'дезинфекция — только болезнетворные'], 's', step=32)
    return s


# 7. Дригальский --------------------------------------------------------------------------------------
def drigalski():
    s = text(900, 52, 'Чистая культура: посев по Дригальскому и контроль', 'h', 'middle')
    s += card(30, 90, 1180, 800) + card(1230, 90, 540, 800)
    for k, (lab, n) in enumerate((('сплошной рост', 0), ('густой рост', 60), ('отдельные колонии', 9))):
        cx = 230 + k * 390
        s += dish(cx, 380)
        if k == 0:
            s += f'<circle cx="{cx}" cy="380" r="120" fill="#E8C68A" opacity=".9"/>'
        else:
            for j in range(n):
                a = j * 2.4
                r = 20 + (j * 37) % 100
                s += f'<circle cx="{cx + r * math.cos(a):.0f}" cy="{380 + r * math.sin(a):.0f}" r="{7 if k == 1 else 13}" fill="#C9A35A" stroke="{INK}" stroke-width="1.5"/>'
        s += text(cx, 580, f'чашка {k + 1}', 't', 'middle') + text(cx, 620, lab, 's', 'middle', RED if k == 2 else INK)
        if k < 2:
            s += arrow(cx + 160, 380, cx + 225, 380, INK, 4)
    s += text(620, 720, 'один шпатель по трём чашкам — клеток всё меньше', 's', 'middle')
    s += text(620, 770, 'колония из чашки 3 выросла из одной клетки → чистая культура', 's', 'middle', RED)
    s += text(1500, 150, 'Термостат', 't', 'middle')
    s += f'<rect x="1300" y="200" width="400" height="420" rx="20" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    s += text(1500, 250, '35 °C, 16–24 ч', 's', 'middle', RED)
    s += tube(1410, 300, '#E8C68A', 240) + tube(1590, 300, '#F7EFC8', 240)
    s += text(1410, 580, 'опыт', 's', 'middle') + text(1590, 580, 'контроль', 's', 'middle', BLUE)
    s += lines_at(1500, 700, ['контроль — та же среда без посева:', 'проверяет стерильность;', 'вывод — только сравнением'], 's', step=36)
    return s


# 8. Окраска по Граму ------------------------------------------------------------------------------
def gram():
    s = text(900, 52, 'Окраска по Граму', 'h', 'middle')
    s += card(30, 90, 1740, 300)
    steps = [('1. кристаллический|фиолетовый', '#7B3FA0'), ('2. раствор йода', '#8A5A2B'), ('3. этанол —|обесцвечивание', '#DCEBF5'), ('4. сафранин|или фуксин', '#E04B4B')]
    for k, (lab, col) in enumerate(steps):
        cx = 250 + k * 430
        s += f'<circle cx="{cx}" cy="200" r="40" fill="{col}" stroke="{INK}" stroke-width="3"/>'
        s += lines_at(cx, 290, lab.split('|'), 's', step=32)
        if k < 3:
            s += arrow(cx + 60, 200, cx + 370, 200, GREY, 4)
    for k, (t, col, thick, outer, lab) in enumerate((('Грамположительные — фиолетовые', VIOLET, 80, False, ['толстый слой муреина', 'чувствительны к пенициллину', 'стрептококки, стафилококки, бациллы']),
                                                   ('Грамотрицательные — красные', RED, 30, True, ['тонкий муреин + наружная мембрана', 'устойчивы к пенициллину', 'сальмонеллы, спирохеты']))):
        x = 30 + k * 880
        s += card(x, 410, 860, 520)
        cx = x + 430
        s += text(cx, 470, t, 't', 'middle', col)
        y = 540
        if outer:
            s += f'<rect x="{x + 80}" y="{y}" width="700" height="34" fill="#F2C230" stroke="{INK}" stroke-width="2"/>' + text(x + 100, y + 26, 'наружная мембрана', 's')
            y += 40
        s += f'<rect x="{x + 80}" y="{y}" width="700" height="{thick}" fill="#C9A35A" stroke="{INK}" stroke-width="2"/>'
        s += text(x + 100, y + thick / 2 + 9, 'муреин', 's') if thick > 30 else text(x + 100, y + thick / 2 + 9, 'тонкий муреин', 's', 'start', INK)
        y += thick + 8
        s += f'<rect x="{x + 80}" y="{y}" width="700" height="34" fill="#7FB3E0" stroke="{INK}" stroke-width="2"/>' + text(x + 100, y + 26, 'мембрана', 's')
        s += ''.join(rod(x + 160 + j * 110, 760, 80, 30, col) for j in range(6))
        s += lines_at(cx, 830, lab, 's', step=32)
    return s


# 9. Рекомбинантная ДНК ------------------------------------------------------------------------------
def plasmid(cx, cy, r=70, gap=False, insert=False):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE}" stroke-width="10"' + (f' stroke-dasharray="{2 * math.pi * r - 40:.0f} 40"' if gap else '') + '/>'
    if insert:
        s += f'<path d="M{cx + r} {cy - 20} A {r} {r} 0 0 1 {cx + r * math.cos(0.5):.0f} {cy + r * math.sin(0.5):.0f}" fill="none" stroke="{RED}" stroke-width="12"/>'
    s += f'<rect x="{cx - 30}" y="{cy - r - 10}" width="60" height="20" fill="#5DAA6F"/>'
    return s


def recombinant():
    s = text(900, 52, 'Генная инженерия: рекомбинантная ДНК', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    s += f'<line x1="80" y1="220" x2="520" y2="220" stroke="{INK}" stroke-width="10"/><line x1="230" y1="220" x2="370" y2="220" stroke="{RED}" stroke-width="12"/>'
    s += text(300, 190, 'ген (например, инсулина)', 's', 'middle', RED) + text(300, 280, 'ДНК донора', 's', 'middle')
    s += text(300, 330, '✂ рестриктаза', 's', 'middle', ORANGE)
    s += plasmid(300, 520, 80, gap=True) + text(300, 650, 'плазмида, разрезанная', 's', 'middle') + text(300, 685, 'той же рестриктазой', 's', 'middle', ORANGE)
    s += text(300, 470, 'ген устойчивости', 'cap', 'middle').replace('y="470"', 'y="415"')
    s += arrow(540, 400, 700, 400, INK, 5) + text(620, 380, 'лигаза', 's', 'middle', GREEN)
    s += plasmid(830, 400, 90, insert=True) + text(830, 540, 'рекомбинантная', 's', 'middle') + text(830, 575, 'плазмида', 's', 'middle')
    s += arrow(940, 400, 1080, 400, INK, 5) + text(1010, 380, 'ввод', 's', 'middle')
    s += rod(1240, 400, 260, 120, '#DCEFD7') + plasmid(1240, 400, 30, insert=True)
    s += text(1240, 500, 'кишечная палочка', 's', 'middle')
    s += arrow(1240, 520, 1240, 610, INK, 5) + text(1260, 575, 'отбор', 's', 'start')
    s += dish(1240, 760, 120, '#F7EFC8') + ''.join(f'<circle cx="{1240 + 60 * math.cos(j * 1.9):.0f}" cy="{760 + 60 * math.sin(j * 1.9):.0f}" r="14" fill="#C9A35A" stroke="{INK}" stroke-width="2"/>' for j in range(5))
    s += lines_at(1550, 720, ['среда с антибиотиком:', 'растут только клетки', 'с плазмидой'], 's', step=34)
    s += lines_at(560, 800, ['рестриктаза режет и оставляет «липкие» концы', 'лигаза сшивает; продукты — инсулин, гормон роста, интерферон'], 's', step=40)
    return s


# 10. Долли -----------------------------------------------------------------------------------------
def sheep(cx, cy, col, lab):
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="110" ry="65" fill="{col}" stroke="{INK}" stroke-width="3"/>'
    s += f'<ellipse cx="{cx + 120}" cy="{cy - 40}" rx="40" ry="30" fill="#3B3833"/>'
    s += ''.join(f'<line x1="{cx + d}" y1="{cy + 55}" x2="{cx + d}" y2="{cy + 120}" stroke="#3B3833" stroke-width="10"/>' for d in (-60, -20, 30, 70))
    return s + text(cx, cy + 170, lab, 's', 'middle')


def dolly():
    s = text(900, 52, 'Клонирование овцы Долли (1996)', 'h', 'middle')
    s += card(30, 90, 1740, 860)
    s += sheep(230, 250, '#F4F1E6', 'овца А — клетка вымени')
    s += sheep(230, 600, '#B9C4CC', 'овца Б — яйцеклетка')
    s += f'<circle cx="620" cy="250" r="50" fill="#DCEFD7" stroke="{INK}" stroke-width="3"/><circle cx="620" cy="250" r="20" fill="{RED}"/>'
    s += f'<circle cx="620" cy="600" r="60" fill="#FDE3E4" stroke="{INK}" stroke-width="3"/><line x1="580" y1="560" x2="660" y2="640" stroke="{INK}" stroke-width="4"/>'
    s += arrow(380, 250, 560, 250, INK, 4) + arrow(380, 600, 550, 600, INK, 4)
    s += text(620, 340, 'ядро', 's', 'middle', RED) + text(620, 700, 'ядро удалено', 's', 'middle')
    s += f'<circle cx="900" cy="430" r="65" fill="#FDE3E4" stroke="{INK}" stroke-width="3"/><circle cx="900" cy="430" r="20" fill="{RED}"/>'
    s += arrow(670, 260, 840, 400, RED, 4) + arrow(680, 590, 840, 460, INK, 4)
    s += text(900, 540, 'эмбрион', 's', 'middle')
    s += arrow(975, 430, 1080, 430, INK, 4)
    s += sheep(1250, 430, '#3B3833', 'овца В — вынашивает')
    s += arrow(1250, 640, 1250, 700, INK, 4)
    s += sheep(1550, 760, '#F4F1E6', 'Долли — копия овцы А')
    return s


# 11. Микроклональное размножение ----------------------------------------------------------------------
def microclonal():
    s = text(900, 52, 'Микроклональное размножение растений', 'h', 'middle')
    s += card(30, 90, 1740, 780)
    labels = ['1. эксплант —|верхушка побега', '2. стерильная среда —|микропобеги', '3. укоренение —|ауксины', '4. теплица']
    for k, lab in enumerate(labels):
        cx = 250 + k * 430
        if k == 0:
            s += f'<path d="M{cx} 520 V 280" stroke="{GREEN}" stroke-width="10"/>' + ''.join(
                f'<ellipse cx="{cx + d * 40}" cy="{360 + j * 60}" rx="40" ry="16" fill="#5DAA6F" transform="rotate({d * -25} {cx + d * 40} {360 + j * 60})"/>' for j in range(3) for d in (-1, 1))
            s += f'<circle cx="{cx}" cy="275" r="22" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="6 5"/>'
        elif k in (1, 2):
            s += tube(cx, 240, '#FFF8E1', 300)
            s += f'<rect x="{cx - 30}" y="440" width="60" height="70" fill="#F7EFC8"/>'
            n = 5 if k == 1 else 3
            for j in range(n):
                x = cx - 20 + j * (40 / max(n - 1, 1))
                s += f'<line x1="{x:.0f}" y1="440" x2="{x:.0f}" y2="{360 - (j % 2) * 20}" stroke="{GREEN}" stroke-width="5"/>'
                if k == 2:
                    s += f'<path d="M{x:.0f} 440 q -10 30 0 60" fill="none" stroke="{BROWN}" stroke-width="3"/>'
        else:
            for j in range(3):
                px = cx - 110 + j * 110
                s += f'<polygon points="{px - 40},520 {px + 40},520 {px + 30},460 {px - 30},460" fill="{BROWN}"/>'
                s += f'<line x1="{px}" y1="460" x2="{px}" y2="360" stroke="{GREEN}" stroke-width="6"/><ellipse cx="{px - 22}" cy="390" rx="22" ry="10" fill="#5DAA6F"/><ellipse cx="{px + 22}" cy="410" rx="22" ry="10" fill="#5DAA6F"/>'
        s += lines_at(cx, 600, lab.split('|'), 's', step=34)
        if k < 3:
            s += arrow(cx + 110, 400, cx + 300, 400, INK, 4)
    s += lines_at(900, 760, ['основа — тотипотентность: клетка растения даёт любые клетки',
                             'культура меристем — безвирусные, генетически одинаковые растения'], 's', step=42)
    return s


if __name__ == '__main__':
    jobs = {
        'bacterium.png': (bacterium(), 1800, 880),
        'bacteria-forms.png': (bacteria_forms(), 1800, 940),
        'phage.png': (phage(), 1800, 880),
        'fight-microbes.png': (fight_microbes(), 1800, 950),
        'food-biotech.png': (food_biotech(), 1800, 940),
        'sterilization.png': (sterilization(), 1800, 940),
        'drigalski.png': (drigalski(), 1800, 920),
        'gram.png': (gram(), 1800, 960),
        'recombinant.png': (recombinant(), 1800, 980),
        'dolly.png': (dolly(), 1800, 980),
        'microclonal.png': (microclonal(), 1800, 900),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
