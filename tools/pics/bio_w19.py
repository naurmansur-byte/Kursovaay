"""Рисунки недели 19 биологии (course/biology/week-19/pics/*.png): Ламарк и Дарвин, формы борьбы, формы отбора,
приспособления, критерии вида, дрейф и изоляция, видообразование, пути эволюции, гомология и аналогия, кладограмма,
антропогенез.

Факты — по выжимке course/textbooks/bio-19-evolution.md (Б9 § 53–61; Б10-2 § 81–99). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w19.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    return _text(x, y, chem(s), cls, anchor, fill)

OUT = ROOT / 'course' / 'biology' / 'week-19' / 'pics'
BLUE, ORANGE, PURPLE, BROWN, LEAF = '#3A57A7', '#D98A2B', '#8E44AD', '#8A5A2B', '#5DAA6F'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32, color=color))


def heron(x, y, leg, col='#B9C4CC'):
    s = f'<ellipse cx="{x}" cy="{y}" rx="46" ry="26" fill="{col}" stroke="{INK}" stroke-width="2"/>'
    s += f'<path d="M{x + 36} {y - 10} q 20 -50 10 -80" fill="none" stroke="{INK}" stroke-width="5"/><circle cx="{x + 46}" cy="{y - 92}" r="12" fill="{col}" stroke="{INK}" stroke-width="2"/>'
    s += f'<path d="M{x + 56} {y - 92} l 30 4 l -30 6 Z" fill="{ORANGE}"/>'
    s += f'<line x1="{x - 8}" y1="{y + 22}" x2="{x - 8}" y2="{y + 22 + leg}" stroke="{INK}" stroke-width="4"/><line x1="{x + 12}" y1="{y + 22}" x2="{x + 12}" y2="{y + 22 + leg}" stroke="{INK}" stroke-width="4"/>'
    return s


def curve(x0, y0, w, h, mu, sd, color, dash=None, bimodal=False):
    pts = []
    for k in range(101):
        t = k / 100
        if bimodal:
            v = math.exp(-((t - 0.25) / 0.08) ** 2) + math.exp(-((t - 0.75) / 0.08) ** 2)
        else:
            v = math.exp(-((t - mu) / sd) ** 2)
        pts.append(f'{x0 + t * w:.0f},{y0 - v * h:.0f}')
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="5"{d}/>'


# 1. Ламарк и Дарвин --------------------------------------------------------------------------------
def lamarck_darwin():
    s = text(900, 52, 'Почему у цапли длинные ноги', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 145, 'Ламарк (1809)', 't', 'middle', RED)
    s += heron(250, 330, 90) + arrow(340, 360, 480, 360, RED, 5) + heron(620, 330, 150)
    s += text(250, 520, 'тянулась к воде', 's', 'middle') + text(620, 560, 'птенцы «с длинными ногами»', 's', 'middle')
    s += lines_at(460, 680, ['стремление к совершенству,', 'упражнение органов —', 'приобретённое передаётся потомкам'], 's', step=38)
    s += text(460, 840, 'ошибка: упражнение не меняет наследственность', 's', 'middle', RED)
    s += text(1340, 145, 'Дарвин (1859)', 't', 'middle', GREEN)
    for k, leg in enumerate((70, 100, 140)):
        s += heron(1030 + k * 210, 300, leg)
    s += f'<line x1="975" y1="190" x2="1110" y2="410" stroke="{RED}" stroke-width="6"/><line x1="1110" y1="190" x2="975" y2="410" stroke="{RED}" stroke-width="6"/>'
    s += text(1040, 460, 'гибнут чаще', 'cap', 'middle', RED) + text(1460, 500, 'оставляют потомство', 'cap', 'middle', GREEN)
    s += lines_at(1340, 620, ['ноги разной длины уже были;', 'длинноногие лучше добывают корм,', 'выживают и оставляют больше потомства;', 'доля длинноногих растёт'], 's', step=38)
    s += text(1340, 840, 'изменчивость + борьба + естественный отбор', 's', 'middle', GREEN)
    return s


# 2. Формы борьбы -------------------------------------------------------------------------------------
def struggle_forms():
    s = text(900, 52, 'Борьба за существование: три формы', 'h', 'middle')
    items = [('Внутривидовая', 'самая острая: одинаковые|потребности; олени, сосны'),
             ('Межвидовая', 'хищник и жертва,|паразит и хозяин'),
             ('С условиями среды', 'заморозки, засуха,|наводнения')]
    for k, (t, d) in enumerate(items):
        x = 30 + k * 590
        s += card(x, 90, 560, 640)
        cx = x + 280
        if k == 0:
            for sg in (-1, 1):
                bx = cx + sg * 140
                s += ''.join(f'<line x1="{bx + j}" y1="420" x2="{bx + j}" y2="480" stroke="{BROWN}" stroke-width="7"/>' for j in (-45, -20, 20, 45))
                s += f'<ellipse cx="{bx}" cy="410" rx="75" ry="34" fill="{BROWN}"/>'
                s += f'<line x1="{bx - sg * 60}" y1="400" x2="{cx + sg * 45}" y2="370" stroke="{BROWN}" stroke-width="16"/>'
                s += f'<circle cx="{cx + sg * 40}" cy="368" r="20" fill="{BROWN}"/>'
                s += f'<path d="M{cx + sg * 40} 352 l {-sg * 20} -50 M{cx + sg * 34} 330 l {sg * 22} -24 M{cx + sg * 28} 314 l {-sg * 26} -12" fill="none" stroke="{INK}" stroke-width="5"/>'
        elif k == 1:
            s += f'<ellipse cx="{cx - 110}" cy="380" rx="70" ry="38" fill="{ORANGE}"/><ellipse cx="{cx + 110}" cy="380" rx="70" ry="38" fill="#8A8A8A"/>'
            s += f'<ellipse cx="{cx}" cy="470" rx="40" ry="24" fill="#D9D3C7" stroke="{INK}" stroke-width="2"/>'
            s += arrow(cx - 60, 410, cx - 30, 450, RED, 4) + arrow(cx + 60, 410, cx + 30, 450, RED, 4)
            s += text(cx - 110, 330, 'лиса', 'cap', 'middle') + text(cx + 110, 330, 'волк', 'cap', 'middle') + text(cx, 520, 'заяц', 'cap', 'middle')
        else:
            s += ''.join(f'<line x1="{cx - 120 + j * 60}" y1="470" x2="{cx - 120 + j * 60}" y2="370" stroke="{LEAF}" stroke-width="6"/>' for j in range(5))
            s += ''.join(f'<text x="{cx - 140 + j * 70}" y="{290 + (j % 2) * 30}" style="font: 800 44px Manrope; fill:{BLUE}">*</text>' for j in range(5))
            s += text(cx, 520, 'посевы под заморозком', 'cap', 'middle')
        s += text(cx, 200, t, 't', 'middle')
        s += lines_at(cx, 580, d.split('|'), 's', step=38)
    s += text(900, 780, 'Мак: 3000 семян → 9 000 000 → 27 000 000 000 — ресурсов на всех не хватит', 's', 'middle')
    return s


# 3. Формы отбора -------------------------------------------------------------------------------------
def selection_forms():
    s = text(900, 52, 'Формы естественного отбора', 'h', 'middle')
    items = [('Движущий', 'условия меняются:|норма сдвигается', 0.4, 0.15, 0.62, 0.13, False),
             ('Стабилизирующий', 'условия постоянны:|сохраняется среднее', 0.5, 0.18, 0.5, 0.08, False),
             ('Разделительный', 'сохраняются обе крайние|формы, средние гибнут', 0.5, 0.18, 0, 0, True)]
    for k, (t, d, m0, s0, m1, s1, bi) in enumerate(items):
        x = 30 + k * 590
        s += card(x, 90, 560, 680)
        s += text(x + 280, 150, t, 't', 'middle')
        s += f'<line x1="{x + 50}" y1="520" x2="{x + 510}" y2="520" stroke="{INK}" stroke-width="3"/>'
        s += curve(x + 60, 520, 440, 250, m0, s0, GREY, '10 8')
        s += curve(x + 60, 520, 440, 300, m1, s1, GREEN, None, bi)
        s += text(x + 280, 560, 'значение признака', 'cap', 'middle')
        s += lines_at(x + 280, 640, d.split('|'), 's', step=36)
    s += text(820, 820, '- - - до отбора', 's', 'end', GREY) + text(980, 820, '—— после отбора', 's', 'start', GREEN)
    return s


# 4. Приспособления ----------------------------------------------------------------------------------
def moth(cx, cy, col):
    return (f'<path d="M{cx} {cy} q -60 -50 -70 10 q 20 30 70 0 Z" fill="{col}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{cx} {cy} q 60 -50 70 10 q -20 30 -70 0 Z" fill="{col}" stroke="{INK}" stroke-width="2"/>')


def adaptations():
    s = text(900, 52, 'Приспособленность и её относительность', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 145, 'Березовая пяденица', 't', 'middle')
    for k, (bark, title) in enumerate((('#ECE8DD', 'чистый ствол'), ('#4A4640', 'закопчённый ствол'))):
        x = 140 + k * 360
        s += f'<rect x="{x}" y="190" width="180" height="420" fill="{bark}" stroke="{INK}" stroke-width="2"/>'
        s += moth(x + 90, 300, '#F4F1E6') + moth(x + 90, 480, '#2E2B27')
        s += text(x + 90, 650, title, 's', 'middle')
    s += lines_at(460, 730, ['на светлом стволе заметны тёмные бабочки,', 'на закопчённом — светлые; доля меняется'], 's', step=38)
    s += text(460, 860, 'приспособление полезно только в своих условиях', 's', 'middle', RED)
    s += text(1340, 145, 'Покровительственная окраска', 't', 'middle')
    rows = [('Маскировка', 'слиться с фоном: полосы тигра,|тёмная спина и светлое брюхо рыб', GREEN),
            ('Мимикрия', 'сходство с защищённым или предметом:|муха-журчалка — оса; палочник — веточка', BLUE),
            ('Демонстрация', 'напугать врага: яркая божья коровка,|раздувающаяся кобра', RED)]
    for k, (n, d, col) in enumerate(rows):
        y = 280 + k * 200
        s += f'<rect x="960" y="{y - 70}" width="760" height="160" rx="14" fill="#fff" stroke="{col}" stroke-width="4"/>'
        s += text(990, y - 20, n, 't', 'start', col) + lines_at(990, y + 20, d.split('|'), 's', 'start', step=34)
    return s


# 5. Критерии вида ----------------------------------------------------------------------------------
def species_criteria():
    s = text(900, 52, 'Критерии вида', 'h', 'middle')
    items = [('Морфологический', 'строение; самый древний;|виды-двойники не различает', GREY),
             ('Физиологический', 'биохимия и физиология', BLUE),
             ('Генетический', 'хромосомы, плодовитость|потомства; сегодня основной', RED),
             ('Экологический', 'ареал и условия жизни', GREEN)]
    for k, (n, d, col) in enumerate(items):
        x = 30 + (k % 2) * 590
        y = 100 + (k // 2) * 330
        s += f'<rect x="{x}" y="{y}" width="560" height="300" rx="18" fill="#fff" stroke="{col}" stroke-width="5"/>'
        s += text(x + 280, y + 70, n, 't', 'middle', col) + lines_at(x + 280, y + 150, d.split('|'), 's', step=40)
    s += card(1210, 100, 560, 630)
    s += text(1490, 160, 'Мул', 't', 'middle')
    s += box(1350, 280, 220, 80, 'осёл|2n = 62', '#E9E4D8') + box(1630, 280, 220, 80, 'лошадь|2n = 64', '#E9E4D8')
    s += arrow(1350, 320, 1460, 420, INK, 4) + arrow(1630, 320, 1520, 420, INK, 4)
    s += box(1490, 470, 340, 80, 'мул — бесплоден', '#FBE3E4', cls='t')
    s += lines_at(1490, 580, ['хромосомы родителей не гомологичны —', 'мейоз нарушен, гамет нет'], 's', step=36)
    s += text(615, 780, 'Ни один критерий отдельно не достаточен — вид определяют по комплексу', 's', 'middle')
    return s


# 6. Дрейф и изоляция -----------------------------------------------------------------------------------
def drift_isolation():
    s = text(900, 52, 'Дрейф генов и изоляция', 'h', 'middle')
    s += card(30, 90, 900, 820) + card(950, 90, 820, 820)
    s += text(480, 145, 'Частота аллеля по поколениям', 't', 'middle')
    x0, y0, w, h = 110, 700, 760, 480
    s += f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{INK}" stroke-width="3"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h}" stroke="{INK}" stroke-width="3"/>'
    s += text(x0 - 10, y0 - h + 10, '1', 's', 'end') + text(x0 - 10, y0 - h / 2 + 10, '0,5', 's', 'end') + text(x0 - 10, y0 + 10, '0', 's', 'end')
    big = [0.5, 0.51, 0.49, 0.5, 0.52, 0.5, 0.49, 0.51, 0.5]
    small = [0.5, 0.62, 0.45, 0.6, 0.74, 0.85, 0.93, 1.0, 1.0]
    for data, col in ((big, BLUE), (small, RED)):
        pts = ' '.join(f'{x0 + i * w / 8:.0f},{y0 - v * h:.0f}' for i, v in enumerate(data))
        s += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="5"/>'
    s += text(480, 770, 'большая популяция — почти ровно', 's', 'middle', BLUE)
    s += text(480, 810, 'малая — случайно до 0 или 1', 's', 'middle', RED)
    s += text(480, 860, 'данные условные', 'cap', 'middle')
    s += text(1360, 145, 'Изоляция', 't', 'middle')
    rows = [('Географическая', 'барьеры: горы, реки, пустыни'), ('Экологическая', 'разные места и сроки размножения'),
            ('Биологическая', 'строение, брачное поведение,|бесплодие гибридов')]
    for k, (n, d) in enumerate(rows):
        y = 280 + k * 200
        s += box(1360, y, 720, 150, f'{n}|{d}', '#fff')
    return s


# 7. Видообразование ------------------------------------------------------------------------------
def speciation():
    s = text(900, 52, 'Как возникают новые виды', 'h', 'middle')
    for k in range(3):
        s += card(30 + k * 590, 90, 560, 760)
    # географическое
    cx = 310
    s += text(cx, 145, 'Географическое', 't', 'middle') + text(cx, 180, '(аллопатрическое)', 'cap', 'middle')
    s += f'<ellipse cx="{cx}" cy="420" rx="220" ry="150" fill="#E2F1E6" stroke="{INK}" stroke-width="3"/>'
    s += f'<polygon points="{cx - 30},270 {cx + 10},420 {cx - 20},570 {cx + 40},570 {cx + 60},420 {cx + 20},270" fill="#9A8F7A"/>'
    s += ''.join(f'<circle cx="{cx - 150 + (j % 3) * 40}" cy="{360 + (j // 3) * 50}" r="12" fill="{BLUE}"/>' for j in range(6))
    s += ''.join(f'<circle cx="{cx + 90 + (j % 3) * 40}" cy="{360 + (j // 3) * 50}" r="12" fill="{RED}"/>' for j in range(6))
    s += lines_at(cx, 650, ['барьер разделил ареал;', 'вьюрки, попугайчики'], 's', step=38)
    # экологическое
    cx = 900
    s += text(cx, 145, 'Экологическое', 't', 'middle') + text(cx, 180, '(симпатрическое)', 'cap', 'middle')
    s += f'<rect x="{cx - 220}" y="260" width="440" height="320" rx="20" fill="#DCEBF5" stroke="{INK}" stroke-width="3"/>'
    s += ''.join(f'<ellipse cx="{cx - 140 + j * 70}" cy="350" rx="22" ry="10" fill="{BLUE}"/>' for j in range(5))
    s += ''.join(f'<ellipse cx="{cx - 140 + j * 70}" cy="530" rx="22" ry="10" fill="{RED}"/>' for j in range(5))
    s += text(cx - 200, 300, 'у поверхности', 'cap', 'start', BLUE) + text(cx - 200, 480, 'у дна', 'cap', 'start', RED)
    s += lines_at(cx, 650, ['одна территория, разные условия;', 'озеро Ланао, Байкал'], 's', step=38)
    # полиплоидия
    cx = 1490
    s += text(cx, 145, 'Полиплоидия', 't', 'middle') + text(cx, 180, 'новый вид сразу', 'cap', 'middle')
    for k, n in enumerate((14, 28, 42)):
        y = 290 + k * 120
        s += box(cx, y, 300, 80, f'пшеница: {n}', '#F7EFC8', cls='t')
        if k < 2:
            s += arrow(cx, y + 42, cx, y + 78, INK, 4)
    s += lines_at(cx, 700, ['основное число 7: 2n, 4n, 6n;', 'полиплоид не скрещивается', 'с исходной формой'], 's', step=38)
    return s


# 8. Пути эволюции -----------------------------------------------------------------------------------
def evolution_paths():
    s = text(900, 52, 'Пути эволюции', 'h', 'middle')
    items = [('Ароморфоз', 'усложнение, рост уровня|организации', ['мезодерма у плоских червей', 'кровеносная система у кольчатых', 'четырёхкамерное сердце'], GREEN, 'up'),
             ('Идиоадаптация', 'частные приспособления|без изменения уровня', ['покровительственная окраска', 'плоское тело камбалы, ската', 'колючки растений'], BLUE, 'side'),
             ('Дегенерация', 'упрощение строения', ['паразитические черви', 'без пищеварительной системы', 'повилика, заразиха'], RED, 'down')]
    for k, (n, d, ex, col, kind) in enumerate(items):
        x = 30 + k * 590
        s += card(x, 90, 560, 780)
        cx = x + 280
        if kind == 'up':
            s += arrow(cx - 120, 420, cx + 120, 220, col, 10)
        elif kind == 'side':
            s += ''.join(arrow(cx - 120, 320, cx + 120, 320 + dy, col, 7) for dy in (-80, 0, 80))
        else:
            s += arrow(cx - 120, 220, cx + 120, 420, col, 10)
        s += text(cx, 160, n, 't', 'middle', col)
        s += lines_at(cx, 500, d.split('|'), 's', step=36)
        s += lines_at(cx, 640, ex, 's', step=38, color=GREY)
    s += text(900, 920, 'Ароморфоз, идиоадаптация, дегенерация — пути биологического прогресса (Северцов, Шмальгаузен)', 's', 'middle')
    return s


# 9. Гомология и аналогия --------------------------------------------------------------------------
def limb(x, y, scale=1.0, tilt=0, col='#E8C547'):
    s = f'<g transform="rotate({tilt} {x} {y})">'
    s += f'<rect x="{x - 12}" y="{y}" width="24" height="{110 * scale:.0f}" rx="10" fill="{col}" stroke="{INK}" stroke-width="2"/>'
    s += f'<rect x="{x - 26}" y="{y + 115 * scale:.0f}" width="20" height="{80 * scale:.0f}" rx="8" fill="#9DB8E0" stroke="{INK}" stroke-width="2"/>'
    s += f'<rect x="{x + 6}" y="{y + 115 * scale:.0f}" width="20" height="{80 * scale:.0f}" rx="8" fill="#9DB8E0" stroke="{INK}" stroke-width="2"/>'
    for j in range(5):
        s += f'<rect x="{x - 32 + j * 14}" y="{y + 200 * scale:.0f}" width="10" height="{50 * scale:.0f}" rx="4" fill="#F2A7C3" stroke="{INK}" stroke-width="1.5"/>'
    return s + '</g>'


def homology_analogy():
    s = text(900, 52, 'Гомологичные, аналогичные, рудименты', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 410) + card(910, 520, 860, 390)
    s += text(460, 145, 'Гомологичные: одно происхождение', 't', 'middle', GREEN)
    for k, (name, sc, tilt) in enumerate((('рука', 1.0, 0), ('ласт кита', 0.7, 0), ('крыло птицы', 1.0, 20))):
        x = 190 + k * 270
        s += limb(x, 210, sc, tilt) + text(x, 560, name, 's', 'middle')
    s += lines_at(460, 650, ['одинаковые отделы костей:', 'плечо (жёлтая), предплечье (синие),', 'кисть (розовые)'], 's', step=38)
    s += text(460, 830, 'функции разные, план строения один', 's', 'middle', GREY)
    s += text(1340, 145, 'Аналогичные: одна функция', 't', 'middle', BLUE)
    s += f'<path d="M1100 300 q -80 -80 -90 20 q 30 40 90 -20 Z" fill="#E6D3EE" stroke="{INK}" stroke-width="2"/>' + text(1060, 400, 'бабочка: вырост покрова', 's', 'middle')
    s += f'<path d="M1480 300 q 100 -60 220 20 q -120 -10 -220 -20 Z" fill="#B9C4CC" stroke="{INK}" stroke-width="2"/>' + text(1560, 400, 'птица: передняя конечность', 's', 'middle')
    s += text(1340, 460, 'колючки кактуса (лист) и боярышника (стебель)', 'cap', 'middle')
    s += text(1340, 575, 'Рудименты и атавизмы', 't', 'middle', RED)
    s += lines_at(1340, 650, ['рудименты — у всех особей:', 'аппендикс, третье веко, тазовые кости кита', '',
                              'атавизмы — у отдельных особей:', 'хвост, многососковость у человека'], 's', step=40)
    return s


# 10. Кладограмма -----------------------------------------------------------------------------------
def cladogram():
    s = text(900, 52, 'Кладограмма: как читать', 'h', 'middle')
    s += card(30, 90, 1740, 820)
    root = (300, 760)
    n3, n2, n1 = (560, 520), (820, 330), (1000, 230)
    leaves = {'A': (1180, 170), 'B': (1180, 290), 'C': (1180, 420), 'D': (1180, 600)}
    seg = lambda a, b, c=INK: f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{c}" stroke-width="6"/>'
    s += seg(root, n3) + seg(n3, n2) + seg(n2, n1) + seg(n1, leaves['A'], RED) + seg(n1, leaves['B'], RED)
    s += seg(n2, leaves['C']) + seg(n3, leaves['D'])
    for k, (lbl, (x, y)) in enumerate(leaves.items()):
        s += f'<circle cx="{x}" cy="{y}" r="28" fill="#fff" stroke="{INK}" stroke-width="4"/>' + text(x, y + 10, lbl, 't', 'middle')
    for p in (n1, n2, n3):
        s += f'<circle cx="{p[0]}" cy="{p[1]}" r="12" fill="{BLUE}"/>'
    s += f'<circle cx="{root[0]}" cy="{root[1]}" r="16" fill="{GREEN}"/>'
    s += text(root[0], root[1] + 50, 'корень — общий предок', 's', 'middle', GREEN)
    s += text(n1[0] - 20, n1[1] - 30, 'узел A и B', 's', 'end', BLUE)
    s += text(1230, 180, 'лист — вид', 'cap')
    s += lines_at(1500, 380, ['ближайший родственник A — B:', 'их общий узел ближе всего', 'к листьям', '',
                              'C ближе к A, чем D', 'D отделился первым'], 's', step=40)
    s += text(900, 870, 'Длины ветвей нет; кладограмма не показывает, кто от кого произошёл', 's', 'middle', RED)
    return s


# 11. Антропогенез -----------------------------------------------------------------------------------
def anthropogenesis():
    s = text(900, 52, 'Этапы антропогенеза', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    stages = [('Протоантропы', 'австралопитек,|человек умелый', '≈ 530 см³', 530),
              ('Архантропы', 'питекантроп, человек|прямоходящий; огонь', '800–1200 см³', 1000),
              ('Палеоантропы', 'неандертальцы', '1200–1400 см³', 1300),
              ('Неоантропы', 'кроманьонцы —|ранние Homo sapiens', 'современный тип', 1400)]
    for k, (n, who, vol, v) in enumerate(stages):
        x = 250 + k * 430
        h = v / 1400 * 260
        s += f'<rect x="{x - 60}" y="{560 - h:.0f}" width="120" height="{h:.0f}" fill="#C9A27A" opacity=".85"/>'
        s += text(x, 540 - h, vol, 's', 'middle')
        s += text(x, 160, n, 't', 'middle') + lines_at(x, 620, who.split('|'), 's', step=34)
        if k < 3:
            s += arrow(x + 80, 580, x + 350, 580, GREY, 4)
    s += text(900, 780, 'Все люди — один биологический вид; прямохождение освободило руки, труд и речь развили мозг', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'lamarck-darwin.png': (lamarck_darwin(), 1800, 940),
        'struggle-forms.png': (struggle_forms(), 1800, 820),
        'selection-forms.png': (selection_forms(), 1800, 860),
        'adaptations.png': (adaptations(), 1800, 940),
        'species-criteria.png': (species_criteria(), 1800, 820),
        'drift-isolation.png': (drift_isolation(), 1800, 940),
        'speciation.png': (speciation(), 1800, 880),
        'evolution-paths.png': (evolution_paths(), 1800, 960),
        'homology-analogy.png': (homology_analogy(), 1800, 940),
        'cladogram.png': (cladogram(), 1800, 940),
        'anthropogenesis.png': (anthropogenesis(), 1800, 880),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
