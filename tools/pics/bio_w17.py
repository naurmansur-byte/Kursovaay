"""Рисунки недели 17 биологии (course/biology/week-17/pics/*.png): виды изменчивости, стрелолист и норма реакции,
вариационная кривая, мутагены, генные и хромосомные мутации, плоидность, синдромы и нерасхождение, гетерозис,
рафанобрассика, центры Вавилова.

Факты — по выжимке course/textbooks/bio-17-variation-selection.md (Б10-2 § 67–68, 77–80, 83, 97–98; Б9 § 41). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w17.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    return _text(x, y, chem(s), cls, anchor, fill)

OUT = ROOT / 'course' / 'biology' / 'week-17' / 'pics'
BLUE, ORANGE, PURPLE, WATER, LEAF = '#3A57A7', '#D98A2B', '#8E44AD', '#DCEBF5', '#5DAA6F'
SEG = ['#E8A3A3', '#F3D27A', '#9CC9A8', '#9DB8E0', '#C9A7DE', '#F0B98A', '#BFE3E0', '#D9D3C7']


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s'):
    rows = label.split('\n')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32))


def chrom_bar(x, y, letters, w=60, h=56, colors=None):
    """Хромосома как ряд блоков с буквами-участками."""
    s = ''
    for k, ch in enumerate(letters):
        c = (colors or {}).get(ch, SEG['ABCDEFGHQR'.index(ch) % 8] if ch in 'ABCDEFGHQR' else '#ddd')
        s += f'<rect x="{x + k * w}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="2.5"/>'
        s += text(x + k * w + w / 2, y + h / 2 + 10, ch, 't', 'middle')
    return s


# 1. Виды изменчивости ----------------------------------------------------------------------------
def variation_types():
    s = text(900, 52, 'Виды изменчивости', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    s += box(900, 160, 360, 70, 'Изменчивость', '#F7EFC8', cls='t')
    s += box(450, 300, 560, 80, 'Ненаследственная\n(фенотипическая)', '#E3EEF7', cls='t')
    s += box(1310, 300, 620, 80, 'Наследственная (генотипическая)', '#E2F1E6', cls='t')
    s += f'<line x1="900" y1="195" x2="450" y2="260" stroke="{INK}" stroke-width="3"/><line x1="900" y1="195" x2="1310" y2="260" stroke="{INK}" stroke-width="3"/>'
    s += box(450, 470, 560, 150, 'Модификационная\nгенотип тот же, меняется фенотип;\nпределы — норма реакции', '#fff')
    s += box(1060, 470, 420, 150, 'Комбинативная\nновые сочетания генов;\nсами гены не меняются', '#fff')
    s += box(1560, 470, 360, 150, 'Мутационная\nменяются гены\nили хромосомы', '#fff')
    s += f'<line x1="450" y1="340" x2="450" y2="395" stroke="{INK}" stroke-width="3"/>'
    s += f'<line x1="1310" y1="340" x2="1060" y2="395" stroke="{INK}" stroke-width="3"/><line x1="1310" y1="340" x2="1560" y2="395" stroke="{INK}" stroke-width="3"/>'
    for k, m in enumerate(('генные', 'хромосомные', 'геномные', 'цитоплазматические')):
        s += box(1560, 600 + k * 60, 330, 48, m, '#FBE3E4')
    s += lines_at(450, 640, ['не наследуется; среда: свет, температура,', 'влажность, питание'], 's', step=36, color=GREY)
    s += lines_at(1060, 640, ['кроссинговер; независимое', 'расхождение; случайное', 'оплодотворение'], 's', step=36, color=GREY)
    return s


# 2. Стрелолист и норма реакции -------------------------------------------------------------------
def arrowhead_reaction_norm():
    s = text(900, 52, 'Один генотип — разные фенотипы', 'h', 'middle')
    s += card(30, 90, 900, 820) + card(960, 90, 810, 820)
    s += text(480, 140, 'Стрелолист', 't', 'middle')
    s += f'<rect x="60" y="460" width="840" height="420" fill="{WATER}"/>'
    s += f'<line x1="60" y1="460" x2="900" y2="460" stroke="{BLUE}" stroke-width="4"/>'
    s += f'<path d="M480 880 C 470 700 480 400 470 300" fill="none" stroke="{GREEN}" stroke-width="8"/>'
    # стреловидный над водой
    s += f'<polygon points="470,170 420,280 470,255 520,280" fill="{LEAF}" stroke="{GREEN}" stroke-width="4"/>'
    s += f'<line x1="470" y1="300" x2="470" y2="255" stroke="{GREEN}" stroke-width="6"/>'
    s += text(560, 230, 'над водой — стреловидные', 's')
    # сердцевидный на поверхности
    s += f'<path d="M478 460 C 560 470 640 470 700 455" fill="none" stroke="{GREEN}" stroke-width="5"/>'
    s += f'<path d="M700 455 C 760 420 820 440 800 470 C 830 490 770 510 700 460 Z" fill="{LEAF}" stroke="{GREEN}" stroke-width="4"/>'
    s += text(700, 420, 'на поверхности — сердцевидные', 's', 'middle')
    # лентовидные под водой
    for k, dx in enumerate((-160, -90, 100, 170)):
        s += f'<path d="M475 {800 - k * 30} C {475 + dx * 0.4} {700 - k * 30} {475 + dx} {640 - k * 20} {475 + dx * 1.2} {560 - k * 10}" fill="none" stroke="{LEAF}" stroke-width="14" stroke-linecap="round"/>'
    s += text(880, 860, 'под водой — лентовидные', 's', 'end')
    # норма реакции: удой и жирность
    s += text(1365, 140, 'Корова при разном кормлении', 't', 'middle')
    bars = [('удой, л', 3000, 4500, 4500, BLUE), ('жирность, %', 3.8, 3.8, 5.0, ORANGE)]
    for k, (lbl, a, b, mx, col) in enumerate(bars):
        x0 = 1060 + k * 360
        for j, (v, cap) in enumerate(((a, 'обычное'), (b, 'хорошее'))):
            h = 520 * v / mx
            x = x0 + j * 130
            s += f'<rect x="{x}" y="{780 - h:.0f}" width="100" height="{h:.0f}" fill="{col}" opacity="{0.55 + 0.4 * j}"/>'
            s += text(x + 50, 770 - h, f'{v:g}'.replace('.', ','), 's', 'middle')
            s += text(x + 50, 815, cap, 'cap', 'middle')
        s += text(x0 + 115, 860, lbl, 't', 'middle')
    s += text(1170, 200, 'широкая норма', 's', 'middle', BLUE) + text(1530, 200, 'узкая норма', 's', 'middle', ORANGE)
    return s


# 3. Вариационная кривая ----------------------------------------------------------------------------
def variation_curve():
    s = text(900, 52, 'Вариационная кривая: колоски в колосе пшеницы', 'h', 'middle')
    s += card(30, 90, 1740, 840)
    V = [14, 15, 16, 17, 18, 19, 20]
    p = [2, 7, 22, 32, 24, 8, 5]
    x0, y0, dx, sy = 250, 760, 190, 17
    s += arrow(x0 - 40, y0, x0 + dx * 6 + 120, y0, INK, 4) + arrow(x0 - 40, y0, x0 - 40, y0 - 34 * sy, INK, 4)
    pts = [(x0 + k * dx, y0 - v * sy) for k, v in enumerate(p)]
    s += f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="none" stroke="{GREEN}" stroke-width="6"/>'
    for (x, y), v, f in zip(pts, V, p):
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="{GREEN}"/>' + text(x, y - 22, str(f), 's', 'middle')
        s += text(x, y0 + 40, str(v), 't', 'middle')
    s += text(x0 + dx * 3, y0 + 85, 'варианта V — число колосков', 's', 'middle')
    s += text(x0 - 60, y0 - 34 * sy - 20, 'частота p', 's', 'start')
    s += f'<rect x="1300" y="150" width="440" height="200" rx="14" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    s += lines_at(1520, 200, ['n = 100 колосьев', 'Σ(V · p) = 1713', 'M = 1713 / 100 = 17,13'], 't', step=46)
    s += text(900, 905, 'Средние значения встречаются чаще всего, крайние — редко', 's', 'middle')
    return s


# 4. Мутагены ---------------------------------------------------------------------------------
def mutagens():
    s = text(900, 52, 'Мутагены — факторы, вызывающие мутации', 'h', 'middle')
    cols = [('Физические', ORANGE, ['радиоактивное излучение', 'ультрафиолет', 'лазерные лучи']),
            ('Химические', BLUE, ['колхицин', 'этиленимин', 'некоторые пестициды', 'и гербициды в высоких дозах']),
            ('Биологические', GREEN, ['вирусы краснухи,', 'кори, гриппа', 'продукты окисления липидов'])]
    for k, (t, c, rows) in enumerate(cols):
        x = 30 + k * 590
        s += card(x, 90, 560, 620)
        s += f'<circle cx="{x + 280}" cy="230" r="80" fill="{c}" opacity=".85"/>'
        if k == 0:
            s += ''.join(f'<line x1="{x + 280}" y1="230" x2="{x + 280 + 70 * math.cos(a):.0f}" y2="{230 + 70 * math.sin(a):.0f}" stroke="#fff" stroke-width="6"/>'
                         for a in [j * math.pi / 4 for j in range(8)])
        elif k == 1:
            s += f'<path d="M{x + 255} 180 h50 v40 l25 50 h-100 l25 -50 Z" fill="#fff"/>'
        else:
            s += f'<circle cx="{x + 280}" cy="230" r="34" fill="#fff"/>' + ''.join(
                f'<line x1="{x + 280 + 34 * math.cos(a):.0f}" y1="{230 + 34 * math.sin(a):.0f}" x2="{x + 280 + 52 * math.cos(a):.0f}" y2="{230 + 52 * math.sin(a):.0f}" stroke="#fff" stroke-width="6"/>'
                for a in [j * math.pi / 3 for j in range(6)])
        s += text(x + 280, 360, t, 't', 'middle', c)
        s += lines_at(x + 280, 430, rows, 's', step=40)
    s += text(900, 760, 'Мутации бывают спонтанные (без воздействия) и индуцированные (от мутагенов)', 's', 'middle')
    return s


# 5. Генные мутации ----------------------------------------------------------------------------------
def triplets(x, y, trip, colors, w=92):
    s = ''
    for k, t in enumerate(trip):
        s += f'<rect x="{x + k * (w + 26)}" y="{y}" width="{w}" height="64" rx="10" fill="{colors[k]}" stroke="{INK}" stroke-width="2.5"/>'
        s += text(x + k * (w + 26) + w / 2, y + 43, t, 't', 'middle')
    return s


def gene_mutations():
    s = text(900, 52, 'Генные мутации: замена и сдвиг рамки', 'h', 'middle')
    s += card(30, 90, 1740, 700)
    ok, bad = '#E2F1E6', '#FBE3E4'
    s += text(90, 200, 'Исходный ген', 't') + triplets(560, 155, ['ТАЦ', 'ГГА', 'ЦТТ'], [ok] * 3)
    s += text(90, 360, 'Замена Г → Ц', 't') + triplets(560, 315, ['ТАЦ', 'ГЦА', 'ЦТТ'], [ok, bad, ok])
    s += text(1000, 360, 'меняется один триплет', 's', 'start', RED)
    s += text(90, 520, 'Вставка Г', 't') + triplets(560, 475, ['ТАЦ', 'ГГГ', 'АЦТ', 'Т…'], [ok, bad, bad, bad])
    s += text(1060, 600, 'сдвиг рамки: меняются все следующие триплеты', 's', 'middle', RED)
    s += lines_at(900, 690, ['генная мутация — изменение последовательности нуклеотидов; в микроскоп не видна',
                             'выпадение нуклеотида тоже сдвигает рамку'], 's', step=40)
    return s


# 6. Хромосомные мутации ---------------------------------------------------------------------------
def chromosome_mutations():
    s = text(900, 52, 'Хромосомные мутации: изменение структуры', 'h', 'middle')
    s += card(30, 90, 1740, 900)
    rows = [('Исходная', 'ABCDEFGH', ''), ('Делеция', 'ABCDGH', 'утрачен участок EF'),
            ('Дупликация', 'ABCDEFEFGH', 'участок EF удвоен'), ('Инверсия', 'ABFEDCGH', 'участок CDEF повёрнут на 180°')]
    for k, (name, seq, note) in enumerate(rows):
        y = 150 + k * 150
        s += text(80, y + 38, name, 't')
        s += chrom_bar(420, y, seq)
        s += text(420, y + 95, note, 's', 'start', GREY)
    y = 760
    s += text(80, y + 38, 'Транслокация', 't')
    s += chrom_bar(420, y, 'ABCDEF') + chrom_bar(420 + 6 * 60, y, 'QR', colors={'Q': '#7A7A7A', 'R': '#9A9A9A'})
    s += chrom_bar(1200, y, 'QR', colors={'Q': '#7A7A7A', 'R': '#9A9A9A'})
    s += arrow(1190, y + 28, 1000, y + 28, RED, 4)
    s += text(1200, y + 95, 'участок негомологичной хромосомы', 's', 'start', GREY)
    return s


# 7. Плоидность -------------------------------------------------------------------------------------
def ploidy():
    s = text(900, 52, 'Геномные мутации: изменение числа хромосом', 'h', 'middle')
    s += card(30, 90, 1050, 640, '#E2F1E6') + card(1110, 90, 660, 640, '#FBE3E4')
    s += text(555, 140, 'Полиплоидия — кратно', 't', 'middle', GREEN) + text(1440, 140, 'Анеуплоидия — некратно', 't', 'middle', RED)
    sets = [(190, '2n', 2, 0), (530, '3n', 3, 0), (880, '4n', 4, 0), (1290, '2n + 1', 2, 1), (1600, '2n − 1', 2, -1)]
    cols = ['#3A57A7', '#F08A3C', '#8E44AD']
    for cx, lbl, mult, extra in sets:
        for c, col in enumerate(cols):  # строка — один тип хромосом, число палочек — сколько копий
            count = mult + (extra if c == 0 else 0)
            h = 110 - c * 22
            y = 200 + c * 125 + (110 - h)
            for j in range(count):
                s += f'<rect x="{cx - count * 15 + j * 30}" y="{y}" width="22" height="{h}" rx="11" fill="{col}" stroke="{INK}" stroke-width="2"/>'
        s += text(cx, 610, lbl, 'f', 'middle')
    s += text(555, 690, 'у растений полиплоиды крупнее и продуктивнее', 's', 'middle')
    s += text(1440, 690, 'трисомия и моносомия', 's', 'middle')
    s += text(900, 790, 'Причина — нерасхождение хромосом в мейозе', 't', 'middle')
    return s


# 8. Синдромы и нерасхождение ----------------------------------------------------------------------
def chromosome_diseases():
    s = text(900, 52, 'Хромосомные болезни: лишняя или недостающая хромосома', 'h', 'middle')
    s += card(30, 90, 900, 820) + card(960, 90, 810, 820)
    s += text(480, 140, 'Кариограмма: 47, трисомия 21', 't', 'middle')
    for i in range(23):
        col, row = i % 8, i // 8
        x = 90 + col * 102
        y = 190 + row * 210
        h = 130 - i * 4 if i < 22 else 90
        n = 3 if i == 20 else 2
        for j in range(n):
            s += f'<rect x="{x + j * 22}" y="{y + 130 - h}" width="18" height="{h}" rx="9" fill="{RED if i == 20 else "#BDB8AE"}" stroke="{INK}" stroke-width="1.5"/>'
        s += text(x + 20, y + 165, 'XY' if i == 22 else str(i + 1), 'cap', 'middle', RED if i == 20 else GREY)
    s += lines_at(480, 830, ['синдром Дауна — три хромосомы 21', 'цитогенетический метод'], 's', step=36)
    s += text(1365, 140, 'Нерасхождение половых хромосом', 't', 'middle')
    rows = [(330, 'XX', 'Y', '47, XXY', 'Клайнфельтер:|мужчины'), (620, '0', 'X', '45, X0', 'Шерешевский — Тёрнер:|женщины')]
    for y, egg, sp, kar, name in rows:
        s += f'<circle cx="1080" cy="{y}" r="60" fill="#F6E3D3" stroke="{INK}" stroke-width="3"/>' + text(1080, y + 10, egg if egg != '0' else 'без X', 's', 'middle')
        s += text(1180, y + 10, '+', 'f', 'middle')
        s += f'<ellipse cx="1280" cy="{y}" rx="34" ry="22" fill="#fff" stroke="{BLUE}" stroke-width="4"/>' + text(1280, y + 9, sp, 's', 'middle', BLUE)
        s += arrow(1330, y, 1420, y, INK, 4)
        s += text(1590, y - 15, kar, 't', 'middle') + lines_at(1590, y + 25, name.split('|'), 'cap', step=28)
    s += lines_at(1365, 800, ['Даун — 21, Патау — 13, Эдвардс — 18', 'по законам Менделя не наследуются'], 's', step=36)
    return s


# 9. Гетерозис ---------------------------------------------------------------------------------------
def heterosis():
    s = text(900, 52, 'Гетерозис кукурузы по поколениям', 'h', 'middle')
    s += card(30, 90, 1740, 720)
    data = [('F₁', 100, GREEN), ('F₂', 65, ORANGE), ('F₃', 50, RED)]
    for k, (g, v, c) in enumerate(data):
        x = 330 + k * 420
        h = v * 5
        s += f'<rect x="{x}" y="{700 - h}" width="200" height="{h}" fill="{c}" opacity=".85"/>'
        s += text(x + 100, 680 - h, f'{v} %' + ('' if v == 100 else f' (−{100 - v} %)'), 't', 'middle', c) + text(x + 100, 750, g, 'f', 'middle')
    s += lines_at(900, 160, ['урожай гибрида F₁ принят за 100 % (В. Шелл, 1914)'], 's')
    return s


# 10. Рафанобрассика --------------------------------------------------------------------------------
def raphanobrassica():
    s = text(900, 52, 'Карпеченко, 1924: плодовитый гибрид капусты и редьки', 'h', 'middle')
    s += card(30, 90, 1740, 820)
    s += box(300, 220, 380, 110, 'Капуста\n2n = 18, гаметы 9', '#E2F1E6', cls='t')
    s += box(1500, 220, 380, 110, 'Редька\n2n = 18, гаметы 9', '#F3E3C9', cls='t')
    s += box(900, 420, 520, 130, 'Гибрид: 9 + 9 = 18\nхромосомы без пар —\nмейоз нарушен, бесплоден', '#FBE3E4')
    s += arrow(490, 260, 640, 380, INK, 5) + arrow(1310, 260, 1160, 380, INK, 5)
    s += arrow(900, 490, 900, 600, INK, 5) + text(930, 560, 'удвоение набора (колхицин)', 's')
    s += box(900, 690, 560, 130, 'Рафанобрассика: 36 хромосом\nу каждой хромосомы есть пара —\nплодовита', '#E3EEF7')
    s += text(900, 860, 'Колхицин разрушает веретено деления — набор хромосом удваивается', 's', 'middle')
    return s


# 11. Центры Вавилова --------------------------------------------------------------------------------
def vavilov_centers():
    s = text(900, 52, 'Семь центров происхождения культурных растений (Н. И. Вавилов)', 'h', 'middle')
    s += card(30, 90, 1740, 860, '#EAF2F8')
    centers = [(300, 330, 'Центрально-\nамериканский', 'кукуруза, фасоль,\nтыква, какао'),
               (380, 700, 'Южно-\nамериканский', 'картофель, табак,\nарахис, ананас'),
               (760, 300, 'Средиземно-\nморский', 'маслина, свёкла,\nкапуста'),
               (860, 700, 'Абиссинский', 'твёрдая пшеница,\nячмень, кофе'),
               (1160, 470, 'Юго-Западно-\nазиатский', 'мягкая пшеница,\nгорох, чечевица'),
               (1560, 290, 'Восточно-\nазиатский', 'просо, гречиха,\nяблоня, слива'),
               (1500, 700, 'Южно-\nазиатский', 'рис, сахарный\nтростник, банан')]
    for k, (x, y, name, plants) in enumerate(centers):
        s += f'<ellipse cx="{x}" cy="{y}" rx="190" ry="120" fill="{SEG[k]}" opacity=".9" stroke="{INK}" stroke-width="2"/>'
        s += lines_at(x, y - 40, name.split('\n'), 's', step=30)
        s += lines_at(x, y + 30, plants.split('\n'), 'cap', step=28)
    s += text(900, 910, 'Наибольшее разнообразие форм — там, где сохранились дикие предки', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'variation-types.png': (variation_types(), 1800, 880),
        'arrowhead-reaction-norm.png': (arrowhead_reaction_norm(), 1800, 940),
        'variation-curve.png': (variation_curve(), 1800, 960),
        'mutagens.png': (mutagens(), 1800, 800),
        'gene-mutations.png': (gene_mutations(), 1800, 820),
        'chromosome-mutations.png': (chromosome_mutations(), 1800, 1020),
        'ploidy.png': (ploidy(), 1800, 830),
        'chromosome-diseases.png': (chromosome_diseases(), 1800, 940),
        'heterosis.png': (heterosis(), 1800, 840),
        'raphanobrassica.png': (raphanobrassica(), 1800, 940),
        'vavilov-centers.png': (vavilov_centers(), 1800, 980),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
