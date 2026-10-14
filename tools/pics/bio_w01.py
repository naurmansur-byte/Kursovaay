"""Рисунки недели 1 биологии (course/biology/week-01/pics/*.png) — по реестру в README недели.

Запуск: .venv/Scripts/python tools/pics/bio_w01.py
"""
from __future__ import annotations

from common import (GREEN, GREY, INK, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, ROOT, arrow, chloro, dna_loop, elongated_cell, ends,
                    label, mito, nucleus, render, ribosomes, ruler, text)

OUT = ROOT / 'course' / 'biology' / 'week-01' / 'pics'


def lab(px: float, py: float, tx: float, ty: float, s: str) -> str:
    """Подпись над или под объектом, текст по центру; линия от точки на объекте к краю подписи."""
    ey = ty + 8 if ty < py else ty - 26
    return (f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{tx:.0f}" y2="{ey:.0f}" stroke="{INK}" stroke-width="2.5"/>'
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{INK}"/>' + text(tx, ty, s, 's', 'middle'))


def cell_comparison() -> str:
    s = ''
    # 1. Бактерия (центр x=300)
    s += text(300, 55, 'Бактерия', 'h', 'middle')
    s += '<rect x="150" y="300" width="300" height="180" rx="90" fill="#EFE7D2" stroke="#8A6D2C" stroke-width="12"/>'
    s += '<rect x="164" y="314" width="272" height="152" rx="76" fill="#FFF7E0" stroke="#3B3833" stroke-width="3"/>'
    s += dna_loop(300, 390, 50) + ribosomes([(210, 360), (225, 425), (380, 345), (405, 410), (340, 440), (250, 345)])
    s += lab(160, 330, 235, 150, 'клеточная стенка') + lab(380, 370, 400, 195, 'цитоплазма')
    s += lab(175, 430, 200, 600, 'мембрана') + lab(300, 390, 320, 645, 'ДНК — без ядра') + lab(405, 410, 440, 600, 'рибосомы')
    # 2. Клетка мякоти листа (центр x=900)
    s += text(900, 55, 'Клетка мякоти листа', 'h', 'middle')
    s += '<rect x="740" y="210" width="320" height="350" rx="14" fill="#E7F0D9" stroke="#5B7A2A" stroke-width="14"/>'
    s += '<rect x="754" y="224" width="292" height="322" rx="8" fill="#F4F9EE" stroke="#3B3833" stroke-width="3"/>'
    s += '<rect x="810" y="290" width="180" height="200" rx="34" fill="#DDEBF7" stroke="#5E8BB5" stroke-width="3"/>'
    s += nucleus(1005, 258, 30)
    s += ''.join(chloro(x, y, 20, 11, r) for x, y, r in [(780, 300, 80), (780, 420, 95), (1025, 345, 85), (1025, 450, 100),
                                                       (870, 525, 0), (950, 525, 5)])
    s += mito(1025, 520, 20, 10, 60)
    s += lab(754, 250, 700, 130, 'мембрана') + lab(1005, 230, 1010, 130, 'ядро (ДНК)') + lab(860, 210, 880, 175, 'клеточная стенка')
    s += lab(780, 420, 770, 620, 'хлоропласты') + lab(900, 390, 900, 665, 'центральная вакуоль') + lab(1025, 520, 1050, 620, 'митохондрия')
    # 3. Клетка кожи человека (центр x=1500)
    s += text(1500, 55, 'Клетка кожи человека', 'h', 'middle')
    s += ('<path d="M1350 390 C1340 290 1430 245 1500 250 C1590 255 1650 310 1648 390 C1645 470 1580 530 1500 530 '
          'C1415 530 1358 480 1350 390 Z" fill="#FBE7E1" stroke="#3B3833" stroke-width="4"/>')
    s += nucleus(1500, 390, 46) + mito(1420, 470, 24, 12, 30) + mito(1590, 320, 24, 12, -40) + mito(1595, 455, 24, 12, 20)
    s += ribosomes([(1420, 320), (1440, 350), (1580, 400), (1530, 300), (1460, 480)])
    s += lab(1352, 360, 1390, 150, 'мембрана') + lab(1590, 320, 1620, 195, 'митохондрия')
    s += lab(1500, 390, 1500, 620, 'ядро (ДНК)') + lab(1580, 400, 1660, 665, 'рибосомы') + lab(1430, 430, 1360, 665, 'цитоплазма')
    s += text(900, 760, 'Общее у всех трёх: мембрана, цитоплазма, рибосомы, ДНК. У эукариот ДНК — в ядре.', 't', 'middle')
    s += text(900, 805, 'Рисунки не в одном масштабе.', 'cap', 'middle')
    return s


def cell_common_structures() -> str:
    s = text(800, 60, 'Эукариотическая клетка', 'h', 'middle')
    s += ('<path d="M400 450 C380 250 560 140 800 140 C1060 140 1230 250 1210 460 C1190 650 1020 760 800 760 '
          'C560 760 420 640 400 450 Z" fill="#FDF3EA" stroke="#3B3833" stroke-width="6"/>')
    s += nucleus(800, 430, 95)
    # шероховатая ЭПС — изогнутые мембраны с рибосомами
    for k in range(4):
        y = 300 + k * 26
        s += f'<path d="M560 {y} q 40 -20 80 0 t 80 0" fill="none" stroke="#7A4FA3" stroke-width="5"/>'
        s += ribosomes([(570 + j * 26, y - 6 + (j % 2) * 10) for j in range(6)])
    # аппарат Гольджи — стопка дуг
    for k in range(4):
        s += f'<path d="M{960 + k * 6} {560 + k * 22} q 70 -30 140 0" fill="none" stroke="#C7891B" stroke-width="7"/>'
    s += mito(620, 580, 38, 18, 20) + mito(1000, 330, 38, 18, -25) + mito(760, 650, 38, 18, 5)
    s += ribosomes([(900, 600), (930, 660), (680, 450), (1050, 470), (520, 450), (1120, 380)])
    s += ribosomes([(560, 660)])
    s += label(404, 470, 300, 470, 'мембрана', 's') + label(1150, 520, 1290, 620, 'цитоплазма', 's')
    s += label(800, 430, 880, 820, 'ядро с ДНК', 's') + label(640, 305, 420, 200, 'шероховатая ЭПС', 's')
    s += label(1040, 575, 1290, 700, 'аппарат Гольджи', 's') + label(1000, 330, 1200, 220, 'митохондрия', 's')
    s += label(560, 660, 400, 760, 'рибосомы', 's')
    return s


def scale_task(cell_len: float, ruler_len: float, cap: str, segments: int | None = None, title: str = '') -> str:
    x0 = (1600 - cell_len) / 2
    s = text(800, 70, title, 'h', 'middle') if title else ''
    s += elongated_cell(x0, 330, cell_len) + ends(x0, x0 + cell_len, 330)
    if segments:
        step = cell_len / segments
        for k in range(segments):
            s += (f'<line x1="{x0 + k * step + 4:.0f}" y1="200" x2="{x0 + (k + 1) * step - 4:.0f}" y2="200" stroke="{GREEN}" stroke-width="8"/>')
            s += f'<line x1="{x0 + k * step:.0f}" y1="185" x2="{x0 + k * step:.0f}" y2="215" stroke="{GREEN}" stroke-width="4"/>'
        s += f'<line x1="{x0 + cell_len:.0f}" y1="185" x2="{x0 + cell_len:.0f}" y2="215" stroke="{GREEN}" stroke-width="4"/>'
    s += ruler(x0, 560, ruler_len, cap)
    return s


def water_properties() -> str:
    s = text(800, 70, 'Вода: свойство → роль в живом', 'h', 'middle')
    rows = [('Растворяет многие вещества', 'среда для переноса веществ и реакций', LIGHT_BLUE),
            ('Высокая теплоёмкость', 'сглаживает колебания температуры', LIGHT_YELLOW),
            ('Испарение', 'отводит тепло, охлаждает', LIGHT_GREEN)]
    for k, (a, b, bg) in enumerate(rows):
        y = 140 + k * 170
        s += f'<rect x="40" y="{y}" width="470" height="120" rx="14" fill="{bg}" stroke="{INK}" stroke-width="4"/>'
        s += text(275, y + 70, a, 's', 'middle') + arrow(525, y + 60, 610, y + 60)
        s += f'<rect x="625" y="{y}" width="590" height="120" rx="14" fill="#fff" stroke="{GREEN}" stroke-width="4"/>'
        s += text(920, y + 70, b, 's', 'middle')

    # модель двух молекул воды: (угол связи O–H, угол подписи δ+)
    def h2o(ox, oy, hs):
        import math
        out = ''
        for a, la in hs:
            hx, hy = ox + 70 * math.cos(math.radians(a)), oy + 70 * math.sin(math.radians(a))
            out += f'<line x1="{ox}" y1="{oy}" x2="{hx:.0f}" y2="{hy:.0f}" stroke="{INK}" stroke-width="6"/>'
            out += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="22" fill="#fff" stroke="{INK}" stroke-width="4"/>' + text(hx, hy + 9, 'H', 's', 'middle')
            out += text(hx + 36 * math.cos(math.radians(la)), hy + 36 * math.sin(math.radians(la)) + 8, 'δ+', 'cap', 'middle')
        out += f'<circle cx="{ox}" cy="{oy}" r="34" fill="#F8D0D2" stroke="{INK}" stroke-width="4"/>' + text(ox, oy + 10, 'O', 't', 'middle')
        return out
    s += h2o(1320, 220, [(55, -35), (125, 215)]) + text(1320, 168, 'δ−', 'cap', 'middle')
    s += h2o(1450, 470, [(0, -60), (105, 165)]) + text(1392, 478, 'δ−', 'cap', 'middle')
    s += f'<line x1="1371" y1="301" x2="1435" y2="437" stroke="{GREEN}" stroke-width="5" stroke-dasharray="10 8"/>'
    s += text(1420, 615, 'водородная связь —', 's', 'middle') + text(1420, 650, 'пунктир между H и O', 's', 'middle')
    return s


def leaf_root_cells() -> str:
    s = text(380, 70, 'Р — клетка мякоти листа', 'h', 'middle') + text(1220, 70, 'К — клетка корня', 'h', 'middle')
    for x0 in (150, 990):
        s += f'<rect x="{x0}" y="130" width="460" height="470" rx="16" fill="#EEF2E2" stroke="#5B7A2A" stroke-width="14"/>'
        s += f'<rect x="{x0 + 14}" y="144" width="432" height="442" rx="10" fill="#FAFBF5" stroke="#3B3833" stroke-width="3"/>'
        s += f'<rect x="{x0 + 110}" y="230" width="240" height="280" rx="40" fill="#DDEBF7" stroke="#5E8BB5" stroke-width="3"/>'
    s += nucleus(540, 210, 34) + nucleus(1060, 210, 34)
    s += ''.join(chloro(x, y, 22, 12, r) for x, y, r in [(565, 330, 85), (565, 470, 100), (330, 555, 0), (440, 555, 5),
                                                       (200, 300, 80), (200, 430, 95), (300, 170, 10)])
    s += mito(555, 555, 22, 11, 60) + mito(1045, 555, 22, 11, -60) + mito(1380, 180, 22, 11, 20) + mito(220, 540, 22, 11, -20)
    # подписи — в общей колонке между клетками; линия к структуре каждой клетки
    rows = [('ядро', (540, 210), (1060, 210)), ('клеточная стенка', (610, 270), (990, 270)), ('хлоропласты', (565, 330), None),
            ('мембрана', (596, 395), (1004, 395)), ('центральная вакуоль', (480, 420), (1120, 420)),
            ('цитоплазма', (585, 510), (1015, 510)), ('митохондрия', (555, 555), (1045, 555))]
    for k, (name, a, b) in enumerate(rows):
        y = 190 + k * 62
        half = len(name) * 7.2 + 14
        s += text(800, y + 8, name, 's', 'middle')
        for pt, xend in ((a, 800 - half), (b, 800 + half)):
            if pt:
                s += (f'<line x1="{pt[0]}" y1="{pt[1]}" x2="{xend:.0f}" y2="{y}" stroke="{INK}" stroke-width="2.5"/>'
                      f'<circle cx="{pt[0]}" cy="{pt[1]}" r="5" fill="{INK}"/>')
    s += text(800, 680, 'У К те же структуры, что у Р, кроме хлоропластов.', 't', 'middle')
    return s


def scale_two_views() -> str:
    s = text(400, 70, 'Изображение', 'h', 'middle') + text(1180, 70, 'То же, увеличенное вдвое', 'h', 'middle')
    u = 110  # линейка на левом рисунке
    s += elongated_cell(400 - 2.5 * u / 2, 260, 2.5 * u, 90) + ruler(400 - 2.5 * u / 2, 430, u, '8 мкм')
    s += ends(400 - 2.5 * u / 2, 400 + 2.5 * u / 2, 260)
    s += elongated_cell(1180 - 2.5 * u, 300, 5 * u, 180) + ruler(1180 - 2.5 * u, 560, 2 * u, '8 мкм')
    s += ends(1180 - 2.5 * u, 1180 + 2.5 * u, 300)
    s += f'<line x1="800" y1="120" x2="800" y2="760" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 10"/>'
    return s


def levels() -> str:
    names = ['Клетка эпителия кишечника', 'Эпителиальная ткань', 'Орган: тонкая кишка', 'Система: пищеварительная', 'Организм: человек']
    s = text(800, 60, 'Уровни организации', 'h', 'middle')
    cx = [160, 470, 800, 1130, 1440]
    y = 330
    # 1 клетка
    s += f'<rect x="{cx[0] - 55}" y="{y - 110}" width="110" height="220" rx="24" fill="#FBE7E1" stroke="{INK}" stroke-width="5"/>' + nucleus(cx[0], y + 30, 30)
    s += ''.join(f'<line x1="{cx[0] - 45 + k * 15}" y1="{y - 110}" x2="{cx[0] - 45 + k * 15}" y2="{y - 135}" stroke="{INK}" stroke-width="4"/>' for k in range(7))
    # 2 ткань
    for k in range(5):
        x = cx[1] - 125 + k * 50
        s += f'<rect x="{x}" y="{y - 100}" width="48" height="200" rx="12" fill="#FBE7E1" stroke="{INK}" stroke-width="4"/>'
        s += f'<circle cx="{x + 24}" cy="{y + 30}" r="14" fill="#E3E4F4" stroke="#3A57A7" stroke-width="3"/>'
    # 3 орган — петли кишки
    s += (f'<path d="M{cx[2] - 130} {y - 80} q 60 -60 120 0 t 120 0 q 30 60 -20 90 q -60 30 -120 0 q -60 -30 -100 20 q -40 60 20 100 '
          f'q 60 30 120 0 q 60 -30 110 10" fill="none" stroke="#C86B5E" stroke-width="34" stroke-linecap="round"/>')
    # 4 система — пищевод, желудок, кишечник
    s += f'<path d="M{cx[3]} {y - 190} L{cx[3]} {y - 90}" stroke="#C86B5E" stroke-width="18" stroke-linecap="round"/>'
    s += f'<path d="M{cx[3]} {y - 90} q 90 -10 80 60 q -10 50 -90 40" fill="#E9A99E" stroke="#C86B5E" stroke-width="8"/>'
    s += (f'<path d="M{cx[3] - 10} {y + 10} q -90 10 -80 60 q 10 40 70 30 q 70 -10 90 30 q 20 50 -60 70 q -80 10 -100 -30" '
          f'fill="none" stroke="#C86B5E" stroke-width="16" stroke-linecap="round"/>')
    s += f'<path d="M{cx[3] - 70} {y - 70} q -40 30 -20 70 q 50 10 70 -30 z" fill="#B85C3B" stroke="#7A3B24" stroke-width="5"/>'
    # 5 человек
    s += f'<circle cx="{cx[4]}" cy="{y - 150}" r="38" fill="#fff" stroke="{INK}" stroke-width="6"/>'
    s += f'<path d="M{cx[4]} {y - 110} L{cx[4]} {y + 60} M{cx[4] - 80} {y - 60} L{cx[4] + 80} {y - 60} M{cx[4]} {y + 60} L{cx[4] - 55} {y + 180} M{cx[4]} {y + 60} L{cx[4] + 55} {y + 180}" stroke="{INK}" stroke-width="12" stroke-linecap="round" fill="none"/>'
    for k in range(4):
        s += arrow(cx[k] + 95, y, cx[k + 1] - 95, y, GREEN, 6)
    for k, n in enumerate(names):
        first, _, rest = n.partition(': ')
        if rest:
            s += text(cx[k], 620, first + ':', 's', 'middle') + text(cx[k], 655, rest, 's', 'middle')
        else:
            words = n.split(' ', 1)
            s += text(cx[k], 620, words[0], 's', 'middle') + (text(cx[k], 655, words[1], 's', 'middle') if len(words) > 1 else '')
    return s


def scale_compare() -> str:
    cm = 70
    s = ''
    for k, (name, cl, rl, cap) in enumerate([('X', 8, 2, '10 мкм'), ('Y', 6, 3, '25 мкм')]):
        y = 170 + k * 360
        x0 = 220
        s += text(80, y + 12, name, 'h')
        s += elongated_cell(x0, y, cl * cm, 100) + ends(x0, x0 + cl * cm, y)
        s += text(x0 + cl * cm + 40, y + 10, f'клетка: {cl} см на рисунке', 's')
        s += ruler(x0, y + 130, rl * cm, cap)
        s += text(x0 + rl * cm + 40, y + 140, f'линейка: {rl} см на рисунке', 's')
    s += f'<line x1="60" y1="430" x2="1540" y2="430" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 10"/>'
    return s


if __name__ == '__main__':
    jobs = {
        'cell-comparison.png': (cell_comparison(), 1800, 830),
        'cell-common-structures.png': (cell_common_structures(), 1600, 860),
        'cell-scale-example.png': (scale_task(3 * 300, 300, '12 мкм', segments=3, title='Клетка и масштабная линейка'), 1600, 700),
        'water-properties.png': (water_properties(), 1600, 720),
        'scale-homework.png': (scale_task(3 * 260, 260, '12 мкм', title='Клетка — 6 см, линейка — 2 см (на рисунке)'), 1600, 700),
        'scale-compare.png': (scale_compare(), 1600, 760),
        'leaf-root-cells.png': (leaf_root_cells(), 1600, 720),
        'scale-two-views.png': (scale_two_views(), 1600, 800),
        'quiz-scale.png': (scale_task(1.5 * 480, 480, '36 мкм'), 1600, 700),
        'levels-organization.png': (levels(), 1600, 720),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
