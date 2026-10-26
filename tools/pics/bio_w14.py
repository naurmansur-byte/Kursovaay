"""Рисунки недели 14 биологии (course/biology/week-14/pics/*.png): двойная спираль ДНК, репликация, три модели репликации
и опыт Мезельсона — Сталя, тРНК, путь информации от гена к белку, трансляция.

Факты — по выжимке course/textbooks/bio-14-molecular-genetics.md (Б10-1 § 12–17; Б11-1 § 4–5). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w14.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, render, text

OUT = ROOT / 'course' / 'biology' / 'week-14' / 'pics'
BASE = {'А': '#E0656B', 'Т': '#E8B33A', 'У': '#E8B33A', 'Г': '#3A57A7', 'Ц': '#1F7A4A'}
PAIR = {'А': 'Т', 'Т': 'А', 'Г': 'Ц', 'Ц': 'Г'}
OLD, NEW = '#2F3E73', '#F08A3C'                       # старая (родительская) и новая (дочерняя) цепь
HEAVY, LIGHT, HYB = '#2F3E73', '#F3B27A', '#9A6E8E'   # ¹⁵N, ¹⁴N, гибрид
RNA, EXON, INTRON = '#8E44AD', '#2E8B57', '#C9C3B6'


def panel(x, y, w, h, title=None, sub=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{PAPER}"/>'
    if title:
        s += text(x + w / 2, y + 44, title, 't', 'middle')
    if sub:
        s += text(x + w / 2, y + 78, sub, 'cap', 'middle')
    return s


def brace_h(x1, x2, y, s, up=True):
    d = -1 if up else 1
    return (f'<path d="M{x1} {y} v {12 * d} H {x2} v {-12 * d}" fill="none" stroke="{INK}" stroke-width="3"/>'
            + text((x1 + x2) / 2, y + (22 if not up else -0) * d + (-12 if up else 36), s, 's', 'middle'))


def base_box(x, y, b, w=64, h=56):
    return (f'<rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="10" fill="{BASE[b]}"/>'
            + text(x, y + 11, b, 'w', 'middle'))


def hbonds(x1, x2, y, n, gap=14):
    ys = [y + (k - (n - 1) / 2) * gap for k in range(n)]
    return ''.join(f'<line x1="{x1}" y1="{yy:.0f}" x2="{x2}" y2="{yy:.0f}" stroke="{INK}" stroke-width="3" stroke-dasharray="7 6"/>'
                   for yy in ys)


# 1. Двойная спираль -----------------------------------------------------------------------------
def dna_helix():
    s = text(900, 54, 'Двойная спираль ДНК', 'h', 'middle')
    s += panel(30, 90, 1080, 640)
    cy, A, x0, per = 420, 130, 120, 600            # один виток — 600 px = 10 пар
    seq = 'АТГЦЦАТГАЦГТАЦ'
    n = len(seq)
    xs = [x0 + 30 + k * per / 10 for k in range(n)]
    for k, x in enumerate(xs):
        ph = 2 * math.pi * (x - x0) / per
        y1, y2 = cy - A * math.sin(ph), cy + A * math.sin(ph)
        top, bot = min(y1, y2), max(y1, y2)
        b1 = seq[k]
        b2 = PAIR[b1]
        bt, bb = (b1, b2) if y1 <= y2 else (b2, b1)
        mid = (top + bot) / 2
        s += (f'<line x1="{x:.0f}" y1="{top:.0f}" x2="{x:.0f}" y2="{mid - 3:.0f}" stroke="{BASE[bt]}" stroke-width="12"/>'
              f'<line x1="{x:.0f}" y1="{mid + 3:.0f}" x2="{x:.0f}" y2="{bot:.0f}" stroke="{BASE[bb]}" stroke-width="12"/>')
    for sign, color in ((1, OLD), (-1, '#6D7BB0')):
        pts = [(x, cy - sign * A * math.sin(2 * math.pi * (x - x0) / per)) for x in range(x0, x0 + 841, 6)]
        s += f'<polyline points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round"/>'
    # концы цепей
    s += text(x0 - 10, cy - 8, '5′', 't', 'end', OLD) + text(x0 - 10, cy + 40, '3′', 't', 'end', '#6D7BB0')
    s += text(x0 + 860, cy - 8, '3′', 't', 'start', OLD) + text(x0 + 860, cy + 40, '5′', 't', 'start', '#6D7BB0')
    # виток
    xa, xb = x0, x0 + per
    s += (f'<path d="M{xa} 255 v -14 H {xb} v 14" fill="none" stroke="{INK}" stroke-width="3"/>'
          + text((xa + xb) / 2, 228, '1 виток = 10 пар = 3,4 нм', 's', 'middle'))
    # 0,34 нм
    xa, xb = xs[11], xs[12]
    s += (f'<path d="M{xa:.0f} 590 v 14 H {xb:.0f} v -14" fill="none" stroke="{INK}" stroke-width="3"/>'
          + text((xa + xb) / 2, 640, '0,34 нм между парами', 's', 'middle'))
    # ширина
    s += (f'<path d="M1020 {cy - A} h 14 V {cy + A} h -14" fill="none" stroke="{INK}" stroke-width="3"/>'
          + text(1034, cy + A + 44, '≈ 2 нм', 's', 'middle'))
    s += text(570, 700, 'цепи антипараллельны: против 5′-конца одной — 3′-конец другой', 'cap', 'middle')
    # пары оснований
    s += panel(1140, 90, 640, 640, 'Комплементарные пары')
    s += base_box(1300, 230, 'А') + base_box(1520, 230, 'Т') + hbonds(1334, 1486, 230, 2)
    s += text(1410, 300, '2 водородные связи', 's', 'middle')
    s += base_box(1300, 410, 'Г') + base_box(1520, 410, 'Ц') + hbonds(1334, 1486, 410, 3)
    s += text(1410, 480, '3 водородные связи', 's', 'middle')
    s += text(1460, 560, 'пурины А, Г — пиримидины Т, Ц', 'cap', 'middle')
    s += text(1460, 620, 'нуклеотид: основание +', 'cap', 'middle')
    s += text(1460, 652, 'дезоксирибоза + остаток', 'cap', 'middle')
    s += text(1460, 684, 'фосфорной кислоты', 'cap', 'middle')
    return s


# 2. Репликация ----------------------------------------------------------------------------------
def rungs(x1, x2, y1, y2, step=40):
    return ''.join(f'<line x1="{x:.0f}" y1="{y1}" x2="{x:.0f}" y2="{y2}" stroke="{GREY}" stroke-width="5"/>'
                   for x in range(int(x1), int(x2), step))


def strand(x1, x2, y, color, label_l=None, label_r=None):
    s = f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'
    if label_l:
        s += text(x1 - 16, y + 10, label_l, 't', 'end', color)
    if label_r:
        s += text(x2 + 16, y + 10, label_r, 't', 'start', color)
    return s


def dna_replication():
    s = text(900, 54, 'Репликация ДНК — полуконсервативная', 'h', 'middle')
    s += panel(20, 90, 1310, 690)
    fx, cy = 640, 430
    # родительская двойная спираль слева
    s += rungs(110, fx - 30, cy - 40, cy + 40)
    s += strand(100, fx - 20, cy - 40, OLD, '5′') + strand(100, fx - 20, cy + 40, OLD, '3′')
    s += text(360, cy - 90, 'родительская ДНК', 's', 'middle')
    # расходящиеся старые цепи
    s += f'<path d="M{fx - 20} {cy - 40} C {fx + 40} {cy - 40}, {fx + 60} 240, {fx + 140} 240 H 1200" fill="none" stroke="{OLD}" stroke-width="12" stroke-linecap="round"/>'
    s += f'<path d="M{fx - 20} {cy + 40} C {fx + 40} {cy + 40}, {fx + 60} 620, {fx + 140} 620 H 1200" fill="none" stroke="{OLD}" stroke-width="12" stroke-linecap="round"/>'
    s += text(1216, 250, '3′', 't', 'start', OLD) + text(1216, 630, '5′', 't', 'start', OLD)
    # новые цепи
    s += rungs(fx + 190, 1200, 252, 310) + rungs(fx + 190, 1200, 550, 608)
    s += strand(fx + 180, 1200, 320, NEW) + strand(fx + 180, 1200, 540, NEW)
    s += text(1216, 330, '5′', 't', 'start', NEW) + text(1216, 550, '3′', 't', 'start', NEW)
    # хеликаза
    s += (f'<ellipse cx="{fx + 10}" cy="{cy}" rx="44" ry="70" fill="#F6D27A" stroke="#B88A1E" stroke-width="4"/>'
          + text(fx + 10, cy + 10, 'Х', 'w', 'middle'))
    s += text(fx - 10, 190, 'хеликаза (Х) разрывает', 's', 'middle') + text(fx - 10, 222, 'водородные связи', 's', 'middle')
    s += f'<line x1="{fx}" y1="232" x2="{fx + 8}" y2="{cy - 72}" stroke="{INK}" stroke-width="2.5"/>'
    # ДНК-полимераза
    for y in (320, 540):
        s += (f'<ellipse cx="{fx + 200}" cy="{y}" rx="46" ry="34" fill="#9FD3B2" stroke="{GREEN}" stroke-width="4"/>'
              + text(fx + 200, y + 10, 'П', 'w', 'middle'))
    s += text(fx + 380, 412, 'ДНК-полимераза (П)', 's', 'middle')
    s += text(fx + 380, 444, 'достраивает новую цепь', 's', 'middle')
    s += text(fx + 380, 476, 'по комплементарности', 's', 'middle')
    s += text(360, cy + 120, 'старая цепь = матрица', 'cap', 'middle')
    s += text(360, cy + 152, 'для новой', 'cap', 'middle')
    # итог
    s += panel(1360, 90, 420, 690, 'Две дочерние молекулы')
    for k, y in enumerate((260, 520)):
        s += rungs(1420, 1720, y - 30, y + 30)
        s += strand(1410, 1720, y - 34, OLD) + strand(1410, 1720, y + 34, NEW)
    s += text(1570, 360, 'старая + новая', 's', 'middle') + text(1570, 620, 'старая + новая', 's', 'middle')
    s += (f'<rect x="1400" y="670" width="40" height="14" fill="{OLD}"/>' + text(1452, 684, 'старая цепь', 'cap')
          + f'<rect x="1400" y="712" width="40" height="14" fill="{NEW}"/>' + text(1452, 726, 'новая цепь', 'cap'))
    return s


# 3. Три модели и опыт Мезельсона — Сталя --------------------------------------------------------
def mol(x, y, top, bot, w=150, gap=26):
    """Молекула из двух цепей; top/bot — цвет или список цветов отрезков."""
    s = ''
    for yy, c in ((y - gap / 2, top), (y + gap / 2, bot)):
        cols = c if isinstance(c, list) else [c]
        seg = w / len(cols)
        for k, cc in enumerate(cols):
            s += f'<line x1="{x + k * seg:.0f}" y1="{yy:.0f}" x2="{x + (k + 1) * seg:.0f}" y2="{yy:.0f}" stroke="{cc}" stroke-width="11"/>'
    return s


def tube(x, y, bands, h=300, w=90):
    s = (f'<path d="M{x - w / 2} {y} V {y + h - w / 2} a {w / 2} {w / 2} 0 0 0 {w} 0 V {y}" fill="#F4F6FA" stroke="{GREY}" stroke-width="4"/>')
    for pos, color in bands:
        yy = y + 40 + pos * (h - 110)
        s += f'<rect x="{x - w / 2 + 10}" y="{yy - 9:.0f}" width="{w - 20}" height="18" rx="6" fill="{color}"/>'
    return s


def replication_models():
    s = text(900, 54, 'Три модели репликации и опыт Мезельсона — Сталя (1958)', 'h', 'middle')
    models = (('Полуконсервативная', [(OLD, LIGHT), (LIGHT, OLD)], 'подтверждена'),
              ('Консервативная', [(OLD, OLD), (LIGHT, LIGHT)], 'отвергнута после 1-го поколения'),
              ('Дисперсная', [([OLD, LIGHT, OLD, LIGHT], [LIGHT, OLD, LIGHT, OLD]), ([LIGHT, OLD, LIGHT, OLD], [OLD, LIGHT, OLD, LIGHT])],
               'отвергнута после 2-го поколения'))
    for k, (name, kids, verdict) in enumerate(models):
        x = 30 + k * 590
        s += panel(x, 90, 560, 330, name)
        s += mol(x + 40, 250, OLD, OLD)
        s += arrow(x + 205, 250, x + 280, 210, GREY, 4) + arrow(x + 205, 250, x + 280, 300, GREY, 4)
        s += mol(x + 300, 200, *kids[0]) + mol(x + 300, 305, *kids[1])
        s += text(x + 280, 395, verdict, 's', 'middle', GREEN if k == 0 else RED)
    s += text(115 + 0, 300, 'исходная', 'cap', 'middle')
    # опыт
    s += panel(30, 450, 1740, 470)
    s += text(240, 510, 'Кишечная палочка: ¹⁵N → среда с ¹⁴N', 't', 'start')
    s += text(240, 548, 'ДНК разделяют по плотности (центрифугирование); тяжёлая ДНК — ниже', 'cap', 'start')
    cols = ((300, 'исходно (¹⁵N)', [(1.0, HEAVY)], 'одна тяжёлая полоса'),
            (700, 'после 1-го поколения', [(0.5, HYB)], 'одна промежуточная'),
            (1100, 'после 2-го поколения', [(0.0, LIGHT), (0.5, HYB)], 'промежуточная + лёгкая, поровну'))
    for x, cap, bands, res in cols:
        s += tube(x, 580, bands)
        s += text(x, 905, cap, 's', 'middle')
    s += text(300 + 70, 585 + 40 + 1.0 * 190, 'тяжёлая', 'cap')
    s += text(700 + 70, 585 + 40 + 0.5 * 190, 'промежуточная', 'cap')
    s += text(1100 + 70, 585 + 40, 'лёгкая', 'cap') + text(1100 + 70, 585 + 40 + 0.5 * 190, 'промежуточная', 'cap')
    s += text(1500, 640, '¹⁵N — тяжёлый', 's', 'middle') + text(1500, 672, 'изотоп, не радиоактивный', 's', 'middle')
    s += (f'<rect x="1380" y="730" width="44" height="16" fill="{HEAVY}"/>' + text(1436, 746, '¹⁵N-цепь (старая)', 'cap')
          + f'<rect x="1380" y="770" width="44" height="16" fill="{LIGHT}"/>' + text(1436, 786, '¹⁴N-цепь (новая)', 'cap')
          + f'<rect x="1380" y="810" width="44" height="16" fill="{HYB}"/>' + text(1436, 826, 'гибрид ¹⁵N/¹⁴N', 'cap'))
    return s


# 4. тРНК ----------------------------------------------------------------------------------------
def loop(cx, cy, r, n, color=RNA, hi=()):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="7"/>'
    for k in range(n):
        a = 2 * math.pi * k / n
        fill = RED if k in hi else '#fff'
        s += f'<circle cx="{cx + r * math.cos(a):.0f}" cy="{cy + r * math.sin(a):.0f}" r="11" fill="{fill}" stroke="{color}" stroke-width="3"/>'
    return s


def stem(x1, y1, x2, y2, n, off=26, color=RNA):
    """Двуцепочечный стебель: две линии и перемычки (пары оснований)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * off, dx / L * off
    s = ''.join(f'<line x1="{x1 + nx * sgn:.0f}" y1="{y1 + ny * sgn:.0f}" x2="{x2 + nx * sgn:.0f}" y2="{y2 + ny * sgn:.0f}" '
                f'stroke="{color}" stroke-width="7"/>' for sgn in (1, -1))
    for k in range(1, n + 1):
        t = k / (n + 1)
        px, py = x1 + dx * t, y1 + dy * t
        s += (f'<line x1="{px + nx:.0f}" y1="{py + ny:.0f}" x2="{px - nx:.0f}" y2="{py - ny:.0f}" stroke="{GREY}" '
              f'stroke-width="3" stroke-dasharray="6 5"/>')
    return s


def t_rna():
    s = text(700, 54, 'Транспортная РНК — «лист клевера»', 'h', 'middle')
    s += panel(30, 90, 1340, 1090)
    cx, cy = 560, 600
    s += stem(cx, 210, cx, cy - 60, 6)                # акцепторный стебель
    s += stem(cx - 60, cy, cx - 230, cy, 4)           # левая ветвь
    s += loop(cx - 300, cy, 70, 8)
    s += stem(cx + 60, cy, cx + 230, cy, 4)           # правая ветвь
    s += loop(cx + 300, cy, 70, 8)
    s += stem(cx, cy + 60, cx, cy + 230, 4)           # антикодоновая ветвь
    s += loop(cx, cy + 305, 75, 8, hi=(1, 2, 3))
    s += f'<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="{RNA}" stroke-width="7"/>'
    # концы
    s += f'<line x1="{cx + 26}" y1="210" x2="{cx + 26}" y2="150" stroke="{RNA}" stroke-width="7"/>'
    s += text(cx - 40, 205, '5′', 't', 'end', RNA) + text(cx + 46, 205, '3′', 't', 'start', RNA)
    s += (f'<circle cx="{cx + 26}" cy="128" r="30" fill="#F6D27A" stroke="#B88A1E" stroke-width="4"/>'
          + text(cx + 26, 138, 'Гли', 's', 'middle'))
    s += text(cx + 80, 120, 'аминокислота присоединяется', 's', 'start')
    s += text(cx + 80, 152, 'к 3′-концу (акцепторный конец)', 's', 'start')
    s += f'<line x1="{cx + 245}" y1="{cy + 40}" x2="{cx + 245}" y2="{cy + 40}" />'
    s += text(cx + 400, cy - 120, 'пары оснований внутри', 's', 'middle')
    s += text(cx + 400, cy - 88, 'молекулы (водородные связи)', 's', 'middle')
    s += f'<line x1="{cx + 330}" y1="{cy - 80}" x2="{cx + 150}" y2="{cy - 12}" stroke="{INK}" stroke-width="2.5"/>'
    # антикодон
    s += f'<line x1="{cx + 70}" y1="{cy + 340}" x2="{cx + 230}" y2="{cy + 290}" stroke="{INK}" stroke-width="2.5"/>'
    s += text(cx + 240, cy + 290, 'антикодон — 3 нуклеотида:', 's', 'start')
    s += text(cx + 240, cy + 326, '3′-ЦЦА-5′', 't', 'start', RED)
    s += text(cx + 240, cy + 362, 'узнаёт кодон иРНК 5′-ГГУ-3′', 's', 'start')
    s += text(cx + 240, cy + 394, '→ эта тРНК несёт только глицин', 's', 'start')
    s += text(100, 1140, 'Самая маленькая РНК: обычно около 76 нуклеотидов; одна цепь, свёрнутая в «лист клевера»', 'cap', 'start')
    return s


# 5. Путь информации -----------------------------------------------------------------------------
def segs(x, y, parts, h=40):
    """Отрезки [(ширина, цвет, подпись)] подряд."""
    s = ''
    for w, color, lab in parts:
        s += f'<rect x="{x}" y="{y - h / 2}" width="{w}" height="{h}" fill="{color}" stroke="#fff" stroke-width="2"/>'
        if lab:
            s += text(x + w / 2, y + 9, lab, 's', 'middle', '#fff' if color not in (INTRON, '#E7E2D8') else INK)
        x += w
    return s, x


def information_flow():
    s = text(950, 54, 'От гена к белку у эукариот', 'h', 'middle')
    s += (f'<rect x="20" y="90" width="1240" height="860" rx="40" fill="#E3E4F4" stroke="#3A57A7" stroke-width="5"/>'
          + text(60, 140, 'Ядро', 't', 'start', '#3A57A7'))
    # ген
    s += text(80, 210, 'Ген в ДНК', 't')
    g, _ = segs(80, 260, [(150, GREY, 'промотор'), (160, EXON, 'экзон'), (120, INTRON, 'интрон'), (160, EXON, 'экзон'),
                          (120, INTRON, 'интрон'), (160, EXON, 'экзон'), (160, GREY, 'терминатор')])
    s += g
    s += arrow(600, 300, 600, 380, INK, 5) + text(620, 350, 'транскрипция (РНК-полимераза)', 's')
    # пре-мРНК
    s += text(80, 420, 'Пре-мРНК (первичный транскрипт)', 't')
    g, _ = segs(230, 470, [(160, EXON, 'экзон'), (120, INTRON, 'интрон'), (160, EXON, 'экзон'), (120, INTRON, 'интрон'),
                           (160, EXON, 'экзон')])
    s += g + text(215, 480, '5′', 't', 'end', RNA) + text(965, 480, '3′', 't', 'start', RNA)
    s += arrow(600, 510, 600, 600, INK, 5)
    s += text(620, 536, 'процессинг: кэп на 5′-конец, поли-А на 3′-конец;', 's') + text(620, 568, 'сплайсинг — интроны вырезаются,', 's') + text(620, 600, 'экзоны сшиваются', 's')
    # зрелая мРНК
    s += text(80, 650, 'Зрелая мРНК', 't')
    s += f'<circle cx="250" cy="700" r="26" fill="#F6D27A" stroke="#B88A1E" stroke-width="4"/>' + text(250, 760, 'кэп', 's', 'middle')
    g, xe = segs(278, 700, [(160, EXON, 'экзон'), (160, EXON, 'экзон'), (160, EXON, 'экзон'), (150, '#E7E2D8', 'АААА…')])
    s += g + text(278 + 555, 760, 'поли-А', 's', 'middle') + text(215, 710, '5′', 't', 'end', RNA) + text(xe + 14, 710, '3′', 't', 'start', RNA)
    # выход из ядра
    s += f'<rect x="1235" y="660" width="50" height="80" fill="#fff"/>' + text(1260, 640, 'пора', 'cap', 'middle')
    s += arrow(xe + 60, 700, 1320, 700, INK, 5)
    # цитоплазма: рибосома и белок
    s += text(1580, 140, 'Цитоплазма', 't', 'middle', GREY)
    s += f'<line x1="1330" y1="700" x2="1860" y2="700" stroke="{RNA}" stroke-width="9"/>' + text(1340, 750, 'мРНК', 's', 'start', RNA)
    s += (f'<ellipse cx="1640" cy="650" rx="120" ry="70" fill="#C9DDF0" stroke="#3A57A7" stroke-width="4"/>'
          f'<ellipse cx="1640" cy="720" rx="95" ry="38" fill="#9DBFE0" stroke="#3A57A7" stroke-width="4"/>'
          + text(1640, 660, 'рибосома', 's', 'middle'))
    s += text(1640, 810, 'трансляция', 't', 'middle')
    beads = [(1600, 560), (1570, 510), (1600, 460), (1640, 420), (1690, 400), (1740, 420)]
    for k in range(len(beads) - 1):
        (a, b), (c, d) = beads[k], beads[k + 1]
        s += f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{INK}" stroke-width="4"/>'
    for k, (a, b) in enumerate(beads):
        s += f'<circle cx="{a}" cy="{b}" r="20" fill="{["#F6D27A", "#9FD3B2", "#F2A7B5", "#C9DDF0"][k % 4]}" stroke="{INK}" stroke-width="3"/>'
    s += text(1740, 370, 'белок', 't', 'middle')
    s += text(1100, 1000, 'ДНК → (транскрипция) → иРНК → (трансляция) → белок', 't', 'middle')
    return s


# 6. Трансляция ----------------------------------------------------------------------------------
def trna_shape(x, y, anti, aa, color=RNA, aa_fill='#F6D27A'):
    """Упрощённая тРНК над кодоном: антикодон внизу (y — линия мРНК), аминокислота сверху."""
    w = 150
    s = (f'<path d="M{x - 55} {y - 60} V {y - 200} M{x + 55} {y - 60} V {y - 200}" stroke="{color}" stroke-width="10" fill="none"/>'
         f'<rect x="{x - w / 2}" y="{y - 64}" width="{w}" height="44" rx="10" fill="#fff" stroke="{color}" stroke-width="4"/>')
    for k, b in enumerate(anti):
        s += text(x - 45 + k * 45, y - 32, b, 't', 'middle', BASE[b])
    s += f'<line x1="{x}" y1="{y - 200}" x2="{x}" y2="{y - 236}" stroke="{color}" stroke-width="7"/>'
    s += f'<circle cx="{x}" cy="{y - 266}" r="32" fill="{aa_fill}" stroke="{INK}" stroke-width="3"/>' + text(x, y - 256, aa, 's', 'middle')
    return s


def translation():
    s = text(950, 54, 'Трансляция: синтез белка на рибосоме', 'h', 'middle')
    s += panel(20, 90, 1860, 810)
    y = 640
    codons = ['АУГ', 'ГГУ', 'УУУ', 'УАА']
    x0, cw = 330, 270
    # рибосома (две субъединицы)
    rc = x0 + cw / 2
    s += (f'<ellipse cx="{rc}" cy="{y - 150}" rx="300" ry="230" fill="#DCEBF5" stroke="#3A57A7" stroke-width="5"/>'
          f'<ellipse cx="{rc}" cy="{y + 60}" rx="280" ry="70" fill="#B9D3EA" stroke="#3A57A7" stroke-width="5"/>')
    s += text(rc + 250, y - 330, 'большая субъединица', 's', 'start') + text(rc, y + 165, 'малая субъединица', 's', 'middle')
    # мРНК
    s += f'<line x1="120" y1="{y}" x2="1640" y2="{y}" stroke="{RNA}" stroke-width="10"/>'
    s += text(100, y + 10, '5′', 't', 'end', RNA) + text(1660, y + 10, '3′', 't', 'start', RNA)
    for k, c in enumerate(codons):
        cx = x0 + k * cw
        s += f'<rect x="{cx - 75}" y="{y + 10}" width="150" height="46" rx="10" fill="#fff" stroke="{RNA}" stroke-width="3"/>'
        for j, b in enumerate(c):
            s += text(cx - 45 + j * 45, y + 44, b, 't', 'middle', BASE[b])
    # тРНК
    s += trna_shape(x0, y, 'УАЦ', 'Мет')
    s += trna_shape(x0 + cw, y, 'ЦЦА', 'Гли', aa_fill='#9FD3B2')
    s += f'<line x1="{x0 + 32}" y1="{y - 266}" x2="{x0 + cw - 32}" y2="{y - 266}" stroke="{RED}" stroke-width="7"/>'
    s += text(x0 + cw / 2, y - 300, 'пептидная связь', 's', 'middle', RED)
    s += text(x0 - 120, y - 120, 'антикодон', 'cap', 'end') + text(x0 - 120, y - 92, '3′ → 5′', 'cap', 'end')
    s += f'<line x1="{x0 - 112}" y1="{y - 110}" x2="{x0 - 78}" y2="{y - 44}" stroke="{INK}" stroke-width="2.5"/>'
    # движение и стоп
    s += arrow(x0 + 2 * cw - 60, y + 110, x0 + 2 * cw + 160, y + 110, GREEN, 6)
    s += text(x0 + 2 * cw + 50, y + 150, 'рибосома идёт 5′ → 3′', 's', 'middle', GREEN)
    s += text(x0 + 2 * cw, y - 30, 'УУУ → Фен', 's', 'middle')
    s += text(x0 + 3 * cw, y - 90, 'стоп-кодон:', 's', 'middle', RED)
    s += text(x0 + 3 * cw, y - 58, 'тРНК нет —', 's', 'middle', RED)
    s += text(x0 + 3 * cw, y - 26, 'белок отделяется', 's', 'middle', RED)
    s += text(950, 870, 'иРНК 5′-АУГ ГГУ УУУ УАА-3′ → Мет — Гли — Фен: 3 аминокислоты, 2 пептидные связи; старт АУГ — метионин', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'dna-helix.png': (dna_helix(), 1810, 760),
        'dna-replication.png': (dna_replication(), 1800, 810),
        'replication-models.png': (replication_models(), 1800, 950),
        't-rna.png': (t_rna(), 1400, 1200),
        'information-flow.png': (information_flow(), 1900, 1040),
        'translation.png': (translation(), 1900, 930),
    }
    only = set(__import__('sys').argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
