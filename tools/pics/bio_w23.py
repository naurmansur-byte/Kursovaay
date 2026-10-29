"""Рисунки недели 23 биологии (course/biology/week-23/pics/*.png): карта 12 тем, сквозные связи «энергия» и «информация»,
схема отчёта об опыте, опыты с амилазой, транспирацией и свёклой, опыт Мезельсона и Сталя, порядок чтения графика,
карта пробелов ученика.

Факты — по выжимке course/textbooks/bio-23-synthesis-experiment.md (Б9 с. 53–54, 66–67; Б10-1 с. 66–68, 124; Б7а с. 235–236).
Окраски, уровни воды и графики условные. Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w23.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, PAPER, RED, ROOT, arrow, chem, chloro, mito, render, smooth
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = chem(s.replace('ⁿ', '\x02')).replace('\x02', '<tspan baseline-shift="0.6em" font-size="68%">n</tspan>')
    return _text(x, y, s, cls, anchor, fill)


OUT = ROOT / 'course' / 'biology' / 'week-23' / 'pics'
BLUE, ORANGE, BROWN, VIOLET, PINK = '#3A57A7', '#D98A2B', '#8A5A2B', '#7B3FA0', '#E57373'
LIGHT_VIOLET = '#EADFF2'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None, step=32):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * step / 2 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=step, color=color))


def badge(cx, cy, s, fill, r=26, cls='s'):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>' + text(cx, cy + 9, s, cls, 'middle', '#fff')


# 1. Карта 12 тем ------------------------------------------------------------------------------------
TOPICS = [
    ('01', 'Экосистема, популяция', 'нед. 1, 18, 20', 'цепи, 10 %, J- и S-кривые, Харди — Вайнберг'),
    ('02', 'Питание', 'нед. 2, 4, 5', 'фотосинтез, пищеварение, ферменты'),
    ('03', 'Транспорт веществ', 'нед. 3, 6', 'диффузия, осмос, ксилема, флоэма, кровь'),
    ('04', 'Дыхание', 'нед. 4, 7', 'гликолиз, Кребс, АТФ, газообмен, гемоглобин'),
    ('05', 'Выделение', 'нед. 8, 11', 'нефрон, АДГ, водный баланс'),
    ('06', 'Движение. Биофизика', 'нед. 9, 10', 'мышца, потенциал действия'),
    ('07', 'Координация и регуляция', 'нед. 10, 11', 'дуга, синапс, гормоны, обратная связь'),
    ('08', 'Размножение и развитие', 'нед. 12, 13', 'гаметогенез, двойное оплодотворение, циклы'),
    ('09', 'Клеточный цикл, клетка', 'нед. 1, 3, 12, 14', 'органоиды, мембрана, митоз, мейоз, n и c'),
    ('10', 'Наследственность, эволюция', 'нед. 14–17, 19', 'Мендель, сцепление, мутации, отбор'),
    ('11', 'Молекулярная биология', 'нед. 1–4, 14', 'ферменты, ДНК → РНК → белок'),
    ('12', 'Микробиология, биомедицина', 'нед. 1, 21, 22', 'бактерии, вирусы, генная инженерия, ПЦР'),
]


def topic_row(x, y, t, col):
    n, name, weeks, models = t
    return (badge(x + 34, y, n, col, 28) + text(x + 80, y + 2, name, 't') + text(x + 80, y + 40, weeks + ' · ' + models, 's'))


def topics_map():
    s = text(900, 52, 'Карта 12 тем ЕНТ по биологии', 'h', 'middle')
    s += card(30, 90, 880, 820, LIGHT_GREEN) + card(930, 90, 840, 420, LIGHT_BLUE) + card(930, 530, 840, 380, LIGHT_VIOLET)
    s += text(60, 140, 'Раздел 01 · строение и функции, организм и среда', 's', fill=GREEN)
    for k, t in enumerate(TOPICS[:7]):
        s += topic_row(50, 200 + k * 102, t, GREEN)
    s += text(960, 140, 'Раздел 02 · размножение, наследственность, эволюция', 's', fill=BLUE)
    for k, t in enumerate(TOPICS[7:10]):
        s += topic_row(950, 200 + k * 102, t, BLUE)
    s += text(960, 580, 'Раздел 03 · прикладные интегрированные науки', 's', fill=VIOLET)
    for k, t in enumerate(TOPICS[10:]):
        s += topic_row(950, 640 + k * 102, t, VIOLET)
    s += box(900, 960, 1100, 64, 'тема → модель → данные → вывод → проверка', LIGHT_YELLOW, cls='t')
    return s


# 2. Сквозная связь «энергия» ---------------------------------------------------------------------------
def energy_link():
    s = text(900, 52, 'Сквозная связь «энергия»: клетка → организм → среда', 'h', 'middle')
    s += f'<circle cx="150" cy="250" r="62" fill="#F2C230" stroke="{ORANGE}" stroke-width="4"/>'
    for k in range(12):
        a = 2 * math.pi * k / 12
        s += (f'<line x1="{150 + 74 * math.cos(a):.0f}" y1="{250 + 74 * math.sin(a):.0f}" x2="{150 + 98 * math.cos(a):.0f}" '
              f'y2="{250 + 98 * math.sin(a):.0f}" stroke="{ORANGE}" stroke-width="5"/>')
    s += text(150, 260, 'свет', 't', 'middle')
    s += arrow(255, 250, 300, 250, ORANGE)
    s += f'<rect x="310" y="130" width="530" height="240" rx="18" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4"/>'
    s += chloro(378, 190, 48, 24)
    s += text(440, 200, 'Хлоропласт · фотосинтез', 't')
    s += lines_at(575, 265, ['CO₂ + H₂O → глюкоза + O₂', 'энергия света → энергия глюкозы', 'нед. 4'], 's', step=36)
    s += arrow(848, 250, 997, 250)
    s += text(922, 230, 'глюкоза, O₂', 'cap', 'middle')
    s += f'<rect x="1005" y="130" width="560" height="240" rx="18" fill="#FBE3D2" stroke="{ORANGE}" stroke-width="4"/>'
    s += mito(1090, 190, 56, 26)
    s += text(1165, 200, 'Митохондрия · дыхание', 't')
    s += lines_at(1285, 265, ['глюкоза + O₂ → CO₂ + H₂O', 'энергия глюкозы → АТФ', 'нед. 4, 7'], 's', step=36)
    s += f'<path d="M1285 375 Q 950 520 600 380" fill="none" stroke="{BLUE}" stroke-width="5" stroke-dasharray="14 9"/>'
    s += f'<polygon points="600,376 628,380 612,402" fill="{BLUE}"/>'
    s += text(930, 470, 'CO₂ и H₂O снова в лист — круговорот углерода, нед. 20', 's', 'middle', BLUE)
    s += card(30, 530, 1740, 360)
    s += text(60, 580, 'Цепь питания: на следующий уровень — около 10 % энергии, 90 % теряется', 't')
    levels = [('трава', '10 000 кДж', 760, GREEN), ('кузнечик', '1000 кДж', 520, ORANGE),
              ('лягушка', '100 кДж', 320, BROWN), ('уж', '10 кДж', 170, RED)]
    for k, (who, e, w, col) in enumerate(reversed(levels)):
        y = 620 + k * 62
        s += f'<rect x="{560 - w / 2:.0f}" y="{y}" width="{w}" height="50" rx="8" fill="{col}" opacity="0.85"/>'
        s += text(560, y + 34, f'{who} · {e}', 's', 'middle', '#fff')
    s += lines_at(1330, 660, ['продуценты → консументы I, II, III порядка', 'пирамида энергии всегда правильная',
                              'правило 10 % — Линдеман, нед. 20'], 's', step=48)
    return s


# 3. Сквозная связь «информация» ------------------------------------------------------------------------
def helix(x, y, w=150):
    a = ''.join(f'{x + k * w / 40:.0f},{y + 26 * math.sin(k / 40 * 4 * math.pi):.0f} ' for k in range(41))
    b = ''.join(f'{x + k * w / 40:.0f},{y - 26 * math.sin(k / 40 * 4 * math.pi):.0f} ' for k in range(41))
    rungs = ''.join(f'<line x1="{x + k * w / 16:.0f}" y1="{y + 26 * math.sin(k / 16 * 4 * math.pi):.0f}" x2="{x + k * w / 16:.0f}" '
                    f'y2="{y - 26 * math.sin(k / 16 * 4 * math.pi):.0f}" stroke="{GREY}" stroke-width="2"/>' for k in range(1, 16))
    return (rungs + f'<polyline points="{a}" fill="none" stroke="{BLUE}" stroke-width="5"/>'
            f'<polyline points="{b}" fill="none" stroke="{RED}" stroke-width="5"/>')


def info_link():
    s = text(900, 52, 'Сквозная связь «информация»: от гена до вида', 'h', 'middle')
    s += card(30, 90, 1740, 300, LIGHT_BLUE) + card(30, 420, 1740, 330, LIGHT_GREEN)
    s += text(60, 135, 'В клетке и организме', 's', fill=BLUE)
    xs = [230, 640, 1050, 1460]
    labs = [('ДНК', 'ген, нед. 14'), ('иРНК', 'транскрипция'), ('Белок', 'трансляция'), ('Признак', 'работа белка, нед. 3, 15')]
    for x, (a, b) in zip(xs, labs):
        s += f'<rect x="{x - 170}" y="160" width="340" height="190" rx="16" fill="#fff" stroke="{INK}" stroke-width="3"/>'
        s += text(x, 205, a, 't', 'middle') + text(x, 335, b, 's', 'middle', GREY)
    s += helix(155, 265)
    s += f'<polyline points="{"".join(f"{490 + k * 7.5:.0f},{265 + 14 * math.sin(k * 1.2):.0f} " for k in range(41))}" fill="none" stroke="{GREEN}" stroke-width="5"/>'
    for k in range(6):
        s += f'<circle cx="{960 + k * 36}" cy="265" r="15" fill="{[ORANGE, VIOLET, GREEN, BLUE, PINK, BROWN][k]}"/>'
    s += f'<ellipse cx="1460" cy="265" rx="70" ry="44" fill="#F2C230" stroke="{INK}" stroke-width="3"/>'
    for x in (435, 845, 1255):
        s += arrow(x - 30, 255, x + 30, 255)
    s += text(1740, 465, 'В популяции и эволюции', 's', 'end', GREEN)
    xs2 = [200, 550, 900, 1250, 1600]
    labs2 = [('мутация в ДНК', 'нед. 17'), ('новый признак', 'фенотип'), ('отбор в среде', 'нед. 19'),
             ('частоты p и q', 'Харди — Вайнберг'), ('новый вид', 'изоляция, нед. 19')]
    for x, (a, b) in zip(xs2, labs2):
        w = 290
        s += f'<rect x="{x - w / 2:.0f}" y="510" width="{w}" height="150" rx="16" fill="#fff" stroke="{INK}" stroke-width="3"/>'
        s += text(x, 570, a, 't', 'middle') + text(x, 620, b, 's', 'middle', GREY)
    for a, b in zip(xs2[:-1], xs2[1:]):
        s += arrow(a + 149, 585, b - 149, 585)
    s += f'<path d="M230 360 C 230 440 200 440 200 505" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="12 8"/>'
    s += text(250, 445, 'замена нуклеотида', 's', fill=RED)
    s += text(900, 720, 'Модификация меняет только фенотип и не меняет частоты аллелей', 's', 'middle', GREY)
    return s


# 4. Схема отчёта ------------------------------------------------------------------------------------
def report_scheme():
    s = text(900, 52, 'Схема отчёта об опыте: девять шагов', 'h', 'middle')
    steps = ['Цель', 'Гипотеза', 'Материалы|и оборудование', 'Ход работы', 'Результаты|(таблица)',
             'Анализ|результатов', 'Вывод', 'Оценка|гипотезы', 'Оценка|метода']
    pos = [(200, 200), (550, 200), (900, 200), (1250, 200), (1600, 200), (1600, 420), (1250, 420), (900, 420), (550, 420)]
    fills = {1: LIGHT_YELLOW, 4: LIGHT_BLUE, 6: LIGHT_GREEN, 8: '#FBE3D2'}
    for k, ((x, y), lab) in enumerate(zip(pos, steps)):
        s += box(x, y, 300, 120, lab, fills.get(k, '#fff'), cls='t', step=36)
        s += badge(x - 150, y - 60, str(k + 1), INK, 24)
    for k in range(4):
        s += arrow(pos[k][0] + 152, 200, pos[k + 1][0] - 152, 200)
    s += arrow(1600, 262, 1600, 358)
    for k in range(5, 8):
        s += arrow(pos[k][0] - 152, 420, pos[k + 1][0] + 152, 420)
    s += text(200, 430, 'Б10-1, с. 124', 'cap', 'middle')
    s += card(30, 540, 1740, 270)
    s += lines_at(60, 600, ['Гипотеза — предположение, которое опыт может подтвердить или опровергнуть.',
                            'Изменяемое условие — что меняют; результат — что наблюдают; остальные условия одинаковые.',
                            'Контроль — обычные условия, всё остальное как в опыте.',
                            'Результат: «вода покраснела». Вывод: «мембраны разрушены».',
                            'Оценка метода — что сделать точнее: например, измерить температуру воды.'], 's', 'start', step=44)
    return s


# 5. Опыт с амилазой ------------------------------------------------------------------------------------
def tube(cx, top, liquid, label, outline=INK, h=250, sub=''):
    w = 56
    d = f'M{cx - w / 2} {top} L{cx - w / 2} {top + h - w / 2} A{w / 2} {w / 2} 0 0 0 {cx + w / 2} {top + h - w / 2} L{cx + w / 2} {top}'
    lq = top + 80
    s = (f'<path d="M{cx - w / 2 + 4} {lq} L{cx - w / 2 + 4} {top + h - w / 2} A{w / 2 - 4} {w / 2 - 4} 0 0 0 {cx + w / 2 - 4} '
         f'{top + h - w / 2} L{cx + w / 2 - 4} {lq} Z" fill="{liquid}"/>')
    s += f'<path d="{d}" fill="none" stroke="{outline}" stroke-width="{5 if outline != INK else 3}"/>'
    s += text(cx, top + h + 45, label, 's', 'middle')
    if sub:
        s += text(cx, top + h + 80, sub, 'cap', 'middle')
    return s


def rack(x, y, w):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="6" fill="#C9A77A" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x + 20}" y="{y + 22}" width="16" height="70" fill="#C9A77A"/><rect x="{x + w - 36}" y="{y + 22}" width="16" height="70" fill="#C9A77A"/>')


def amylase():
    s = text(900, 52, 'Опыт с амилазой слюны: одно условие в каждом штативе', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 145, 'Штатив № 1 — меняется только pH', 't', 'middle')
    s += text(460, 185, 'все пробирки при 37 °C', 's', 'middle', GREY)
    s += rack(140, 300, 640)
    for x, lab, sub, out in ((260, 'кислота', '', INK), (460, 'сода', '', INK), (660, 'без добавок', 'контроль', GREEN)):
        s += tube(x, 230, '#F3E6C8', lab, out, sub=sub)
    s += lines_at(460, 650, ['в каждой пробирке — крахмал и слюна', 'в равных количествах и в одно время',
                             'результат сравнивают с контролем по йоду'], 's', step=40)
    s += text(1340, 145, 'Штатив № 2 — меняется только температура', 't', 'middle')
    s += text(1340, 185, 'через одно время — раствор йода', 's', 'middle', GREY)
    s += rack(1020, 300, 640)
    for x, lab, col, res in ((1140, 'лёд', '#2B3F9E', 'синий'), (1340, '37 °C', '#E8C77A', 'не синий'), (1540, '58 °C', '#2B3F9E', 'синий')):
        s += tube(x, 230, col, lab, sub=res)
    s += box(1340, 690, 780, 110, 'синий — крахмал остался: фермент не работал|при 37 °C крахмал расщеплён', LIGHT_YELLOW, step=40)
    s += text(1340, 820, 'холод и нагрев снижают активность амилазы', 's', 'middle')
    return s


# 6. Транспирация -------------------------------------------------------------------------------------
def branch(cx, top):
    s = f'<line x1="{cx}" y1="740" x2="{cx}" y2="{top}" stroke="{BROWN}" stroke-width="6"/>'
    for k, (dx, dy, rot) in enumerate(((-40, 40, -35), (40, 70, 35), (-40, 110, -35), (40, 140, 35))):
        s += f'<ellipse cx="{cx + dx}" cy="{top + dy}" rx="36" ry="15" fill="#5DAA6F" stroke="{GREEN}" stroke-width="3" transform="rotate({rot} {cx + dx} {top + dy})"/>'
    return s


def cylinder(cx, level, top=400, bottom=760):
    w = 110
    s = f'<rect x="{cx - w / 2}" y="{level}" width="{w}" height="{bottom - level}" fill="{LIGHT_BLUE}"/>'
    s += f'<rect x="{cx - w / 2}" y="{level - 12}" width="{w}" height="12" fill="#E6C34A"/>'
    s += f'<line x1="{cx - w / 2 - 10}" y1="430" x2="{cx + w / 2 + 10}" y2="430" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 6"/>'
    s += f'<path d="M{cx - w / 2} {top} L{cx - w / 2} {bottom} L{cx + w / 2} {bottom} L{cx + w / 2} {top}" fill="none" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="{cx - w / 2 - 20}" y="{bottom}" width="{w + 40}" height="14" rx="5" fill="{INK}"/>'
    return s


def transpiration():
    s = text(900, 52, 'Транспирация: ветки одного вида, на воде слой масла', 'h', 'middle')
    s += card(30, 90, 1740, 870)
    data = [(220, 'тепло', 'нагреватель', 600, RED), (560, 'ветер', 'вентилятор', 620, RED), (900, 'влажность', 'влажный аквариум', 460, BLUE),
            (1240, 'холод', 'холодная камера', 490, BLUE), (1580, 'контроль', 'обычная комната', 530, GREEN)]
    for cx, what, where, level, col in data:
        s += cylinder(cx, level) + branch(cx, 200)
        s += text(cx, 815, what, 't', 'middle', col) + text(cx, 855, where, 's', 'middle', GREY)
    s += f'<rect x="80" y="150" width="70" height="40" rx="8" fill="{RED}"/>' + ''.join(
        f'<path d="M{95 + k * 20} 200 q 8 15 0 30 q -8 15 0 30" fill="none" stroke="{RED}" stroke-width="3"/>' for k in range(3))
    s += f'<circle cx="445" cy="200" r="12" fill="{INK}"/>' + ''.join(
        f'<ellipse cx="{445 + 30 * math.cos(a):.0f}" cy="{200 + 30 * math.sin(a):.0f}" rx="28" ry="11" fill="{GREY}" transform="rotate({math.degrees(a):.0f} {445 + 30 * math.cos(a):.0f} {200 + 30 * math.sin(a):.0f})"/>'
        for a in (0, 2.09, 4.19))
    s += f'<rect x="795" y="140" width="210" height="645" rx="10" fill="#9CC9E8" opacity="0.25" stroke="{BLUE}" stroke-width="3"/>'
    s += ''.join(f'<path d="M{x} {y} q 6 10 0 14 q -6 -4 0 -14" fill="{BLUE}"/>' for x, y in ((830, 170), (970, 210), (840, 300), (965, 330)))
    s += ''.join(f'<line x1="{1130 + 26 * math.cos(a):.0f}" y1="{180 + 26 * math.sin(a):.0f}" x2="{1130 - 26 * math.cos(a):.0f}" y2="{180 - 26 * math.sin(a):.0f}" stroke="{BLUE}" stroke-width="5"/>'
                 for a in (0, 1.05, 2.09))
    s += text(1700, 445, 'было', 'cap', 'end')
    s += lines_at(900, 910, ['тепло и ветер усиливают, влажность и холод ослабляют · масло — вода не испаряется с поверхности'], 's')
    return s


# 7. Свёкла -----------------------------------------------------------------------------------------
def flask(cx, base, col, label):
    s = (f'<path d="M{cx - 30} 300 L{cx - 30} 400 L{cx - 120} {base} L{cx + 120} {base} L{cx + 30} 400 L{cx + 30} 300" '
         f'fill="none" stroke="{INK}" stroke-width="4"/>')
    s += f'<path d="M{cx - 30 - 0.75 * 70} {470} L{cx - 116} {base - 4} L{cx + 116} {base - 4} L{cx + 30 + 0.75 * 70} {470} Z" fill="{col}"/>'
    s += f'<rect x="{cx - 28}" y="{base - 70}" width="56" height="50" rx="8" fill="#8E1E46" stroke="{INK}" stroke-width="2"/>'
    s += text(cx, base + 50, label, 't', 'middle')
    return s


def beet():
    s = text(900, 52, 'Свёкла в воде разной температуры', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    for cx, col, lab in ((260, '#F4F0EE', 'лёд'), (660, '#F6E4E8', '20 °C'), (1060, '#E9A3B7', '60 °C'), (1460, '#B0234A', 'кипяток')):
        s += flask(cx, 590, col, lab)
    s += f'<rect x="1590" y="200" width="22" height="300" rx="11" fill="#fff" stroke="{INK}" stroke-width="3"/><circle cx="1601" cy="520" r="24" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="1595" y="330" width="12" height="190" fill="{RED}"/>'
    s += text(1601, 175, 'термометр', 's', 'middle')
    s += text(900, 170, 'окраска воды условная: чем горячее, тем сильнее выходит антоциан', 's', 'middle', GREY)
    s += lines_at(900, 720, ['результат: в кипятке вода окрасилась сильнее всего', 'вывод: кипяток разрушает мембраны клеток',
                             'оценка метода: измерить температуру в каждой колбе'], 's', step=42)
    return s


# 8. Мезельсон и Сталь ---------------------------------------------------------------------------------
def duplex(x, y, a, b):
    return (f'<line x1="{x}" y1="{y}" x2="{x + 90}" y2="{y}" stroke="{a}" stroke-width="9"/>'
            f'<line x1="{x}" y1="{y + 18}" x2="{x + 90}" y2="{y + 18}" stroke="{b}" stroke-width="9"/>')


def meselson():
    H, L = '#1B2A6B', '#9DB4E8'
    s = text(900, 52, 'Опыт Мезельсона и Сталя: ¹⁵N → ¹⁴N', 'h', 'middle')
    s += card(30, 90, 1200, 800) + card(1250, 90, 520, 800)
    ys = {'heavy': 600, 'mid': 530, 'light': 460}
    cols = [(200, '0 делений', 'всё на ¹⁵N', ['heavy'], [(H, H)]),
            (520, '1 деление', 'на ¹⁴N', ['mid'], [(H, L), (L, H)]),
            (840, '2 деления', 'на ¹⁴N', ['mid', 'light'], [(H, L), (L, L), (L, L), (L, H)])]
    for cx, a, b, bands, dup in cols:
        s += text(cx, 145, a, 't', 'middle') + text(cx, 185, b, 's', 'middle', GREY)
        s += f'<path d="M{cx - 45} 400 L{cx - 45} 680 A45 45 0 0 0 {cx + 45} 680 L{cx + 45} 400" fill="#F6F3EC" stroke="{INK}" stroke-width="3"/>'
        for band in bands:
            s += f'<rect x="{cx - 40}" y="{ys[band]}" width="80" height="14" rx="5" fill="{INK}"/>'
        for k, (p, q) in enumerate(dup):
            dx = cx - 45 if len(dup) == 1 else cx - 110 + (k % 2) * 130
            s += duplex(dx, 250 if len(dup) == 1 else 230 + (k // 2) * 60, p, q)
    for band, lab in (('heavy', 'тяжёлая'), ('mid', 'промежуточная'), ('light', 'лёгкая')):
        s += text(910, ys[band] + 12, lab, 's')
    s += text(600, 800, 'центрифугирование в CsCl: тяжёлая ДНК опускается ниже', 's', 'middle')
    s += text(1510, 160, 'Цепи ДНК', 't', 'middle')
    s += duplex(1300, 210, H, H) + text(1410, 230, 'старая, ¹⁵N', 's', fill=H)
    s += duplex(1300, 290, L, L) + text(1410, 310, 'новая, ¹⁴N', 's', fill=GREY)
    s += lines_at(1510, 440, ['после 1-го деления —', 'одна промежуточная полоса:', 'в каждой молекуле', 'одна старая и одна новая цепь'], 's', step=40)
    s += box(1510, 720, 440, 150, 'репликация|полуконсервативная|1958, E. coli', LIGHT_YELLOW, cls='t', step=40)
    return s


# 9. Порядок чтения графика ---------------------------------------------------------------------------
def axes(x0, y0, w, h, xl, yl):
    s = arrow(x0, y0, x0 + w, y0, INK, 4) + arrow(x0, y0, x0, y0 - h, INK, 4)
    s += text(x0 + w, y0 + 45, xl, 's', 'end') + text(x0 - 10, y0 - h - 18, yl, 's')
    return s


def graph_reading():
    s = text(900, 52, 'Порядок чтения графика', 'h', 'middle')
    s += card(30, 90, 860, 680) + card(910, 90, 860, 680)
    x0, y0 = 120, 640
    s += axes(x0, y0, 720, 430, 'температура, °C', 'активность фермента, %')
    pts = [(0, 5), (10, 20), (20, 45), (30, 80), (37, 100), (45, 70), (55, 20), (65, 0)]
    P = [(x0 + 20 + t * 9.5, y0 - a * 3.6) for t, a in pts]
    s += f'<path d="{smooth(P)}" fill="none" stroke="{GREEN}" stroke-width="6"/>'
    ox, oy = P[4]
    s += f'<line x1="{ox:.0f}" y1="{oy:.0f}" x2="{ox:.0f}" y2="{y0}" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 6"/>'
    s += text(ox, y0 + 40, '37', 's', 'middle')
    s += badge(int(ox), int(oy) - 50, '2', GREEN, 22) + text(ox + 30, oy - 40, 'оптимум', 's')
    s += badge(int(P[6][0]) + 40, int(P[6][1]) - 40, '2', GREEN, 22) + lines_at(P[6][0] + 70, P[6][1] - 30, ['спад —', 'денатурация'], 's', 'start', step=32)
    s += badge(x0 + 40, y0 + 80, '1', INK, 22) + text(x0 + 75, y0 + 90, 'оси и единицы', 's')
    x1, y1 = 1000, 640
    s += axes(x1, y1, 720, 430, 'освещённость', 'скорость фотосинтеза')
    pts2 = [(0, 0), (2, 45), (4, 75), (6, 90), (8, 95), (10, 95)]
    Q = [(x1 + 10 + v * 55, y1 - r * 3.6) for v, r in pts2]
    s += f'<path d="{smooth(Q)}" fill="none" stroke="{BLUE}" stroke-width="6"/>'
    lx, ly = Q[-1]
    s += f'<line x1="{lx:.0f}" y1="{ly:.0f}" x2="{lx + 130:.0f}" y2="{ly - 60:.0f}" stroke="{RED}" stroke-width="4" stroke-dasharray="10 8"/>'
    s += text(lx + 140, ly - 70, '?', 't', 'middle', RED)
    s += badge(int(Q[4][0]) - 20, int(Q[4][1]) + 60, '2', BLUE, 22) + text(Q[4][0] + 10, Q[4][1] + 70, 'плато', 's')
    s += lines_at(1380, 520, ['плато — ограничивает', 'другой фактор, например CO₂'], 's', step=36)
    s += badge(lx + 60, ly, '4', RED, 22) + text(lx, ly - 50, 'дальше данных нет', 's', 'end', RED)
    s += card(30, 790, 1740, 140)
    s += text(60, 840, '1) Оси и единицы. 2) Рост, максимум, плато, спад. 3) Что сравниваем: две кривые, опыт и контроль.', 's')
    s += text(60, 890, '4) Вывод только в пределах данных: не продолжать за последнюю точку, не называть причиной то, что не проверяли.', 's')
    return s


# 10. Карта пробелов ----------------------------------------------------------------------------------
def gaps_map():
    s = text(900, 52, 'Карта пробелов после итоговой проверки', 'h', 'middle')
    cols = [(40, 'Тема', 430), (470, 'Задания', 200), (670, 'Мой балл', 180), (850, 'Тип ошибки', 420), (1270, 'Что повторить', 490)]
    s += f'<rect x="30" y="90" width="1740" height="60" rx="10" fill="{INK}"/>'
    for x, h, _ in cols:
        s += text(x + 16, 130, h, 't', fill='#fff')
    rows = [('01 Экосистема', 'Q1', '1 / 1', '', ''), ('02 Питание', 'Q12–Q16', '3 / 5', 'вывод шире данных', 'нед. 23 · раздел 5'),
            ('03 Транспорт', 'Q2', '1 / 1', '', ''), ('04 Дыхание', 'Q3', '0 / 1', 'не та модель', 'нед. 6 · кривые диссоциации'),
            ('05 Выделение', 'Q4', '1 / 1', '', ''), ('06 Биофизика', 'Q5', '1 / 1', '', ''), ('07 Регуляция', 'Q6', '1 / 1', '', ''),
            ('08 Размножение', 'Q8', '2 / 2', '', ''), ('09 Клеточный цикл', 'Q9', '1 / 2', 'не знал факт', 'нед. 12 · счёт n и c'),
            ('10 Наследственность', 'Q10', '2 / 2', '', ''), ('11 Молекулярная', 'Q7', '1 / 1', '', ''), ('12 Микробиология', 'Q11', '2 / 2', '', '')]
    for k, r in enumerate(rows):
        y = 160 + k * 62
        bad = bool(r[3])
        fill = '#FBE0DC' if r[2].startswith('0') else (LIGHT_YELLOW if bad else ('#fff' if k % 2 else PAPER))
        s += f'<rect x="30" y="{y}" width="1740" height="56" rx="8" fill="{fill}"/>'
        for (x, _, _), v in zip(cols, r):
            s += text(x + 16, y + 38, v, 's', fill=RED if (bad and v in (r[3], r[4])) else None)
    s += text(900, 940, 'пример заполнения · красным — 0 баллов, жёлтым — частичные ошибки', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'topics-map.png': (topics_map(), 1800, 1010),
        'energy-link.png': (energy_link(), 1800, 920),
        'info-link.png': (info_link(), 1800, 770),
        'report-scheme.png': (report_scheme(), 1800, 840),
        'amylase.png': (amylase(), 1800, 940),
        'transpiration.png': (transpiration(), 1800, 980),
        'beet.png': (beet(), 1800, 880),
        'meselson.png': (meselson(), 1800, 910),
        'graph-reading.png': (graph_reading(), 1800, 950),
        'gaps-map.png': (gaps_map(), 1800, 970),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
