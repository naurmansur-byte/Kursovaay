"""Рисунки недели 8 биологии (course/biology/week-08/pics/*.png): мочевыделительная система, разрез почки, нефрон, этапы
образования мочи, регуляция АДГ, кожа, продукты азотистого обмена, диализ.

Факты — по выжимке course/textbooks/bio-08-excretion.md (Б8 § 28–30, Б9 § 18–21, Б10-1 § 50–58). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w08.py
"""
from __future__ import annotations

import math

from common import GREY, INK, PAPER, RED, ROOT, arrow, chem, label, render, smooth, text

OUT = ROOT / 'course' / 'biology' / 'week-08' / 'pics'
BLUE, URINE, URINE_LINE = '#3A57A7', '#F3E2A0', '#B8902A'
CORTEX, MEDULLA, PELVIS = '#B5524A', '#E2A68A', '#F6E7B5'


def lbl(px, py, tx, ty, s, color=INK):
    return label(px, py, tx, ty, s, 's', color)


def lines_at(x, y, rows, cls='s', anchor='middle', step=32, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def bean(cx, cy, w, h, flip=False):
    """Почка: бобовидный контур, ворота (вогнутая сторона) справа; flip — ворота слева."""
    base = [(0, -1), (0.55, -0.88), (0.8, -0.5), (0.5, -0.15), (0.5, 0.15), (0.8, 0.5), (0.55, 0.88), (0, 1),
            (-0.6, 0.78), (-0.9, 0.2), (-0.9, -0.2), (-0.6, -0.78)]
    k = -1 if flip else 1
    return smooth([(cx + k * x * w, cy + y * h) for x, y in base], True)


# 1. Мочевыделительная система -------------------------------------------------------------------
def urinary_system() -> str:
    s = text(660, 56, 'Органы мочевыделительной системы', 'h', 'middle') + '<g transform="translate(60 0)">'
    for x0, col in ((560, BLUE), (640, RED)):
        s += f'<path d="M{x0} 140 V 700" stroke="{col}" stroke-width="22" stroke-linecap="round"/>'
    for cx, flip in ((360, False), (840, True)):
        hx = cx + (-1 if flip else 1) * 0.5 * 90
        s += f'<path d="M{hx:.0f} 300 H 640" stroke="{RED}" stroke-width="10"/>' if not flip else f'<path d="M560 300 H {hx:.0f}" stroke="{RED}" stroke-width="10"/>'
        s += f'<path d="M{hx:.0f} 330 H 560" stroke="{BLUE}" stroke-width="10"/>' if not flip else f'<path d="M560 330 H {hx:.0f}" stroke="{BLUE}" stroke-width="10"/>'
    # главные сосуды поверх ветвей
    s += f'<path d="M640 140 V 700" stroke="{RED}" stroke-width="22" stroke-linecap="round"/>'
    for cx, flip in ((360, False), (840, True)):
        s += f'<path d="{bean(cx, 320, 90, 150, flip)}" fill="{CORTEX}" stroke="#7A2E28" stroke-width="4"/>'
        s += f'<path d="M{cx - 50} 180 Q {cx} 130 {cx + 50} 180 Z" fill="#E9C46A" stroke="#9C7A2A" stroke-width="3"/>'
        hx = cx + (-1 if flip else 1) * 40
        s += f'<path d="M{hx} 360 C {hx + (-1 if flip else 1) * 40} 480 {600 + (1 if flip else -1) * 140} 600 {600 + (1 if flip else -1) * 60} 750" fill="none" stroke="{URINE_LINE}" stroke-width="10"/>'
    s += f'<path d="M520 770 Q 520 700 600 700 Q 680 700 680 770 Q 680 840 600 840 Q 520 840 520 770 Z" fill="{URINE}" stroke="{URINE_LINE}" stroke-width="5"/>'
    s += f'<path d="M600 840 V 920" stroke="{URINE_LINE}" stroke-width="12"/>'
    s += lbl(300, 320, 150, 320, 'почка')
    s += lbl(320, 165, 150, 150, 'надпочечник')
    s += lbl(760, 300, 1000, 260, 'почечная артерия', RED)
    s += lbl(760, 330, 1000, 380, 'почечная вена', BLUE)
    s += lbl(450, 560, 220, 580, 'мочеточник')
    s += lbl(540, 780, 300, 800, 'мочевой пузырь')
    s += lbl(600, 890, 840, 900, 'мочеиспускательный канал')
    return s + '</g>'


# 2. Разрез почки ---------------------------------------------------------------------------------
def kidney_section() -> str:
    s = text(700, 56, 'Почка в разрезе', 'h', 'middle')
    cx, cy, w, h = 700, 470, 300, 360
    s += f'<path d="{bean(cx, cy, w, h)}" fill="{CORTEX}" stroke="#7A2E28" stroke-width="5"/>'
    px, py = cx + 140, cy
    for k in range(6):
        phi = math.radians(-70 + k * 28)
        dx, dy = -math.cos(phi), math.sin(phi)
        nx, ny = -dy, dx
        ax, ay = px + dx * 150, py + dy * 150
        bx, by = px + dx * 330, py + dy * 330
        s += (f'<path d="M{ax:.0f} {ay:.0f} L {bx + nx * 62:.0f} {by + ny * 62:.0f} Q {bx + dx * 20:.0f} {by + dy * 20:.0f} '
              f'{bx - nx * 62:.0f} {by - ny * 62:.0f} Z" fill="{MEDULLA}" stroke="#8A4A36" stroke-width="2"/>')
        for t in (-30, 0, 30):
            s += f'<path d="M{ax + dx * 25:.0f} {ay + dy * 25:.0f} L {bx + nx * t:.0f} {by + ny * t:.0f}" stroke="#B9715A" stroke-width="2"/>'
        s += f'<path d="M{px + dx * 60:.0f} {py + dy * 60:.0f} L {ax:.0f} {ay:.0f}" stroke="{PELVIS}" stroke-width="34" stroke-linecap="round"/>'
        s += f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="26" fill="{PELVIS}" stroke="{URINE_LINE}" stroke-width="2"/>'
    s += f'<ellipse cx="{px}" cy="{py}" rx="80" ry="110" fill="{PELVIS}" stroke="{URINE_LINE}" stroke-width="3"/>'
    s += f'<path d="M{px + 40} {py + 80} C {px + 90} {py + 160} {px + 120} {py + 260} {px + 140} {py + 380}" fill="none" stroke="{URINE_LINE}" stroke-width="22"/>'
    s += f'<path d="M{px + 70} {py - 70} H 1230" stroke="{RED}" stroke-width="16"/><path d="M{px + 70} {py - 30} H 1230" stroke="{BLUE}" stroke-width="16"/>'
    s += lbl(cx - 140, cy - 330, 380, 150, 'корковый слой', CORTEX)
    a = math.radians(-14)
    s += lbl(px - math.cos(a) * 260, py + math.sin(a) * 260, 380, 330, 'мозговой слой: пирамидки')
    s += lbl(px - 150 * math.cos(math.radians(42)), py + 150 * math.sin(math.radians(42)), 380, 760, 'чашечка')
    s += lbl(px + 10, py + 40, 1090, 520, 'лоханка')
    s += lbl(px + 115, py + 260, 1090, 760, 'мочеточник')
    s += text(1240, py - 62, 'артерия', 's', 'start', RED) + text(1240, py - 22, 'вена', 's', 'start', BLUE)
    return s


# 3. Нефрон ---------------------------------------------------------------------------------------
def nephron() -> str:
    s = text(750, 50, 'Нефрон — единица почки', 'h', 'middle')
    s += f'<rect x="40" y="90" width="1420" height="330" fill="#FBEAE6"/><rect x="40" y="420" width="1420" height="420" fill="#F6EEDC"/>'
    s += text(60, 408, 'корковый слой', 'cap') + text(60, 455, 'мозговой слой', 'cap')
    # сосуды: приносящая (шире) и выносящая
    s += f'<path d="M110 170 L 300 228" stroke="{RED}" stroke-width="26" stroke-linecap="round"/>'
    s += f'<path d="M320 222 C 420 160 470 150 520 160" fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>'
    s += arrow(150, 182, 230, 206, '#fff', 4) + arrow(400, 178, 470, 160, '#fff', 3)
    # капилляры вокруг канальцев: от выносящей, красные → синие
    cap = [(520, 160), (600, 190), (680, 175), (760, 205), (840, 185), (900, 230), (930, 330), (900, 420), (930, 560), (880, 700), (800, 790)]
    s += f'<defs><linearGradient id="pc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient></defs>'
    s += f'<path d="{smooth(cap)}" fill="none" stroke="url(#pc)" stroke-width="6" stroke-dasharray="14 6"/>'
    # капсула и клубочек
    s += f'<path d="M 380 300 A 80 80 0 1 1 330 210" fill="#FFF7D6" stroke="{URINE_LINE}" stroke-width="6"/>'
    for k in range(7):
        a = k * 2 * math.pi / 7
        s += f'<circle cx="{325 + 28 * math.cos(a):.0f}" cy="{285 + 28 * math.sin(a):.0f}" r="18" fill="none" stroke="{RED}" stroke-width="5"/>'
    # каналец: проксимальный → петля → дистальный → собирательная трубка
    tub = [(390, 310), (450, 330), (480, 270), (540, 300), (560, 360), (620, 330), (650, 380), (640, 460), (640, 640), (660, 770), (700, 790),
           (730, 760), (740, 620), (740, 420), (760, 330), (820, 350), (850, 290), (910, 300), (950, 260), (1020, 250)]
    s += f'<path d="{smooth(tub)}" fill="none" stroke="{URINE_LINE}" stroke-width="22" stroke-linecap="round"/>'
    s += f'<path d="{smooth(tub)}" fill="none" stroke="{URINE}" stroke-width="12" stroke-linecap="round"/>'
    s += f'<path d="M1040 110 V 830" stroke="{URINE_LINE}" stroke-width="30"/><path d="M1040 110 V 830" stroke="{URINE}" stroke-width="18"/>'
    s += f'<path d="M1020 250 H 1040" stroke="{URINE}" stroke-width="12"/>'
    for x1, y1, x2, y2 in ((640, 520, 640, 600), (740, 600, 740, 520), (1040, 600, 1040, 700)):
        s += arrow(x1, y1, x2, y2, URINE_LINE, 4)
    s += lbl(250, 320, 120, 350, 'капсула')
    s += lbl(325, 285, 180, 290, 'клубочек', RED)
    s += text(60, 140, 'приносящая артериола (шире)', 'cap', 'start', RED)
    s += lbl(470, 155, 470, 120, 'выносящая', RED)
    s += lbl(560, 360, 470, 560, 'проксимальный извитой каналец')
    s += lbl(700, 790, 480, 800, 'петля Генле')
    s += lbl(910, 300, 1100, 380, 'дистальный извитой каналец')
    s += lbl(1040, 700, 1100, 720, 'собирательная трубка')
    s += lbl(905, 450, 1100, 520, 'капилляры вокруг канальцев')
    s += text(1100, 560, 'сюда возвращаются вещества', 'cap')
    return s


# 4. Три процесса -------------------------------------------------------------------------------
def urine_processes() -> str:
    s = text(750, 56, 'Как образуется моча', 'h', 'middle')
    s += f'<rect x="120" y="140" width="1260" height="60" rx="30" fill="#F9D6D6" stroke="{RED}" stroke-width="4"/>'
    s += text(140, 128, 'кровь', 't', 'start', RED)
    s += f'<rect x="120" y="340" width="1160" height="60" rx="30" fill="{URINE}" stroke="{URINE_LINE}" stroke-width="4"/>'
    s += text(140, 440, 'нефрон: капсула → канальцы', 't', 'start', URINE_LINE)
    s += arrow(1280, 370, 1440, 370, URINE_LINE, 8)
    blocks = [(260, 'down', RED, '1. Фильтрация', ['в капсуле: вода, глюкоза,', 'аминокислоты, соли, мочевина;', 'без клеток крови и белков'], 'первичная моча ≈ 180 л/сут'),
              (700, 'up', GREEN_UP, '2. Реабсорбция', ['из канальцев в кровь: вся', 'глюкоза, аминокислоты, витамины,', 'большая часть воды и солей; АТФ'], 'возвращается ≈ 178,5 л'),
              (1110, 'down', BLUE, '3. Секреция', ['из крови в каналец:', 'ионы H⁺, K⁺, аммиак'], '')]
    for x, d, col, title, rows, vol in blocks:
        for dx in (-50, 0, 50):
            s += arrow(x + dx, 215, x + dx, 330, col, 7) if d == 'down' else arrow(x + dx, 330, x + dx, 215, col, 7)
        s += text(x, 500, title, 't', 'middle', col) + lines_at(x, 540, rows, 'cap')
        if vol:
            s += text(x, 660, vol, 't', 'middle')
    s += lines_at(1390, 300, ['конечная', 'моча'], 's') + text(1390, 440, '≈ 1,5 л', 't', 'middle')
    s += text(750, 720, 'Объём первичной мочи: 125 мл/мин × 1440 мин ≈ 180 л (Б10-1); в Б8 — около 150 л, в Б9 — 150–170 л.', 'cap', 'middle')
    return s


GREEN_UP = '#1F7A4A'


# 5. Петля АДГ ----------------------------------------------------------------------------------
def box(x, y, w, h, rows, fill='#fff', stroke=INK, cls='s'):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
    y0 = y + h / 2 - (len(rows) - 1) * 16 + 9
    return s + lines_at(x + w / 2, y0, rows, cls)


def adh_loop() -> str:
    s = text(750, 56, 'Регуляция воды: антидиуретический гормон (АДГ)', 'h', 'middle')
    w, h = 400, 150
    s += box(60, 110, w, h, ['мало воды, много соли,', 'сильное потоотделение'], PAPER)
    s += box(550, 110, w, h, ['осмотическое давление', 'крови растёт — его чувствуют', 'осморецепторы гипоталамуса'])
    s += box(1040, 110, w, h, ['АДГ: синтез в гипоталамусе,', 'выделение из задней доли', 'гипофиза в кровь'], '#FDECEC', RED)
    s += box(1040, 400, w, h, ['дистальные канальцы и', 'собирательные трубки:', 'проницаемость для воды ↑'])
    s += box(550, 400, w, h, ['вода возвращается в кровь;', 'мочи меньше, она', 'концентрированнее'])
    s += box(60, 400, w, h, ['осмотическое давление', 'снижается — выделение', 'АДГ уменьшается'], PAPER)
    s += arrow(465, 185, 540, 185, INK, 5) + arrow(955, 185, 1030, 185, INK, 5) + arrow(1240, 265, 1240, 390, INK, 5)
    s += arrow(1035, 475, 960, 475, INK, 5) + arrow(545, 475, 470, 475, INK, 5)
    s += f'<path d="M260 395 V 330 H 700 V 272" fill="none" stroke="{GREY}" stroke-width="4" stroke-dasharray="10 8"/>'
    s += f'<polygon points="700,262 690,282 710,282" fill="{GREY}"/>'
    s += text(480, 322, 'обратная связь: стимул слабеет', 'cap', 'middle')
    s += f'<rect x="60" y="600" width="1380" height="120" rx="16" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    s += lines_at(750, 645, ['Много воды → АДГ не выделяется → стенки канальцев не пропускают воду → много разбавленной мочи.',
                             'Недостаток АДГ — несахарный диабет: 4–8 л мочи в сутки и сильная жажда.'], 's')
    return s


# 6. Кожа ---------------------------------------------------------------------------------------
def skin() -> str:
    s = text(700, 56, 'Строение кожи', 'h', 'middle')
    x0, x1 = 380, 980
    s += f'<rect x="{x0}" y="140" width="{x1 - x0}" height="22" fill="#E3B48F"/>'
    s += f'<rect x="{x0}" y="162" width="{x1 - x0}" height="70" fill="#F5D9C4"/>'
    s += f'<rect x="{x0}" y="232" width="{x1 - x0}" height="360" fill="#F9ECE4"/>'
    s += f'<rect x="{x0}" y="592" width="{x1 - x0}" height="220" fill="#FFF6D8"/>'
    for i in range(9):
        for j in range(3):
            s += f'<circle cx="{x0 + 40 + i * 66 + (j % 2) * 30}" cy="{640 + j * 62}" r="28" fill="#F9E7A6" stroke="#C9A43A" stroke-width="2"/>'
    s += f'<path d="M{x0} 140 H {x1} V 812 H {x0} Z" fill="none" stroke="{INK}" stroke-width="3"/>'
    # сосуды только в дерме: артериола, венула и петли капилляров
    s += f'<path d="M{x0} 500 H {x1}" stroke="{RED}" stroke-width="7"/><path d="M{x0} 535 H {x1}" stroke="{BLUE}" stroke-width="7"/>'
    for bx in (590, 740, 900):
        s += f'<path d="M{bx} 500 V 285 A 16 16 0 0 1 {bx + 32} 285" fill="none" stroke="{RED}" stroke-width="5"/>'
        s += f'<path d="M{bx + 32} 285 V 535" fill="none" stroke="{BLUE}" stroke-width="5"/>'
    # волос с луковицей, сальная железа, мышца
    s += f'<path d="M500 250 L 488 555 M540 250 L 552 555" stroke="#7A5A3A" stroke-width="4"/>'
    s += f'<ellipse cx="520" cy="560" rx="38" ry="30" fill="#D9B48A" stroke="#7A5A3A" stroke-width="4"/>'
    s += f'<path d="M520 548 L 512 80" stroke="#4A3A2A" stroke-width="10" stroke-linecap="round"/>'
    s += f'<path d="M498 320 q -55 -15 -55 25 q 0 45 55 35 Z" fill="#FCE9B8" stroke="#B8902A" stroke-width="3"/>'
    s += f'<path d="M548 440 L 650 236" stroke="#B4532A" stroke-width="9" stroke-linecap="round"/>'
    # рецептор
    s += f'<ellipse cx="680" cy="420" rx="22" ry="34" fill="#E4E6F7" stroke="#5B5FA8" stroke-width="3"/><ellipse cx="680" cy="420" rx="10" ry="18" fill="none" stroke="#5B5FA8" stroke-width="2"/>'
    s += f'<path d="M680 454 Q 690 520 670 580" stroke="#5B5FA8" stroke-width="3" fill="none"/>'
    # потовая железа: клубок и проток с порой
    s += ''.join(f'<ellipse cx="{850 + dx}" cy="{565 + dy}" rx="26" ry="14" fill="none" stroke="{BLUE}" stroke-width="5"/>'
                 for dx, dy in ((-10, -12), (8, 0), (-6, 12), (10, 22)))
    s += f'<path d="M848 548 C 830 480 868 420 846 360 C 826 300 866 240 850 140" fill="none" stroke="{BLUE}" stroke-width="5"/>'
    # подписи
    s += text(1010, 158, 'роговой слой', 's') + text(1010, 205, 'эпидермис: нет сосудов, меланин', 's')
    s += lbl(932, 280, 1010, 290, 'капилляры', RED)
    s += lbl(846, 360, 1010, 360, 'проток потовой железы', BLUE)
    s += text(1010, 440, 'дерма', 't')
    s += lbl(870, 580, 1010, 580, 'потовая железа', BLUE)
    s += text(1010, 712, 'подкожная жировая', 't') + text(1010, 746, 'клетчатка', 't')
    s += lbl(514, 120, 340, 110, 'волос')
    s += lbl(470, 350, 340, 350, 'сальная железа')
    s += lbl(600, 340, 340, 260, 'мышца волоса')
    s += lbl(660, 420, 340, 440, 'рецептор', '#5B5FA8')
    s += lbl(500, 570, 340, 560, 'волосяная луковица')
    return s


# 7. Азотистые продукты ----------------------------------------------------------------------------
def drop(x, y, k=1.0, fill='#7DB7E8'):
    return f'<path d="M{x} {y - 34 * k} C {x + 22 * k} {y - 6 * k} {x + 22 * k} {y + 18 * k} {x} {y + 18 * k} C {x - 22 * k} {y + 18 * k} {x - 22 * k} {y - 6 * k} {x} {y - 34 * k} Z" fill="{fill}" stroke="{BLUE}" stroke-width="2"/>'


def nitrogen_products() -> str:
    s = text(750, 56, 'Чем выводят азот разные животные', 'h', 'middle')
    cols = [('аммиак NH₃', 3, ['очень ядовит,', 'хорошо растворим'], 'нужно много воды',
             ['пресноводные беспозвоночные,', 'костистые пресноводные рыбы,', 'личинки в пресной воде,', 'водные насекомые и земноводные']),
            ('мочевина', 2, ['значительно менее', 'ядовита'], 'воду экономят умеренно',
             ['большинство млекопитающих', 'и человек; морские рыбы;', 'взрослые жабы']),
            ('мочевая кислота', 1, ['белые кристаллы,', 'плохо растворима'], 'воду сильно экономят',
             ['наземные насекомые,', 'пресмыкающиеся, птицы', '(у птиц нет мочевого пузыря)'])]
    for k, (name, nd, prop, water, animals) in enumerate(cols):
        x = 25 + k * 490
        cx = x + 230
        s += f'<rect x="{x}" y="100" width="460" height="540" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += text(cx, 160, chem(name), 't', 'middle', RED)
        s += lines_at(cx, 210, prop, 's')
        for i in range(nd):
            s += drop(cx + (i - (nd - 1) / 2) * 60, 330)
        s += text(cx, 400, water, 's', 'middle', BLUE)
        s += f'<line x1="{x + 30}" y1="440" x2="{x + 430}" y2="440" stroke="{GREY}" stroke-width="2"/>'
        s += lines_at(cx, 490, animals, 's')
    s += text(750, 690, 'Все три — продукты распада белков. Паукообразные выделяют гуанин.', 'cap', 'middle')
    return s


# 8. Диализ ---------------------------------------------------------------------------------------
def dialysis() -> str:
    s = text(750, 56, 'Диализ: очистка крови через полупроницаемую мембрану', 'h', 'middle')
    # гемодиализ
    s += text(380, 130, 'Гемодиализ — вне тела', 't', 'middle')
    s += f'<rect x="90" y="190" width="580" height="260" rx="20" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="110" y="210" width="540" height="100" rx="12" fill="#F9D6D6"/>'
    s += f'<rect x="110" y="330" width="540" height="100" rx="12" fill="#DCEBF5"/>'
    s += f'<path d="M110 320 H 650" stroke="{INK}" stroke-width="4" stroke-dasharray="14 8"/>'
    s += arrow(140, 260, 330, 260, RED, 6) + text(470, 268, 'кровь', 's', 'middle', RED)
    s += arrow(640, 380, 490, 380, BLUE, 6) + text(290, 388, 'диализирующий раствор', 'cap', 'middle', BLUE)
    for dx in (220, 340, 460, 580):
        s += f'<circle cx="{dx}" cy="296" r="8" fill="{URINE_LINE}"/>' + arrow(dx, 300, dx, 345, URINE_LINE, 3)
    s += f'<path d="M90 260 H 40 V 560 H 120" fill="none" stroke="{RED}" stroke-width="8"/><path d="M670 260 H 720 V 560 H 640" fill="none" stroke="{RED}" stroke-width="8"/>'
    s += f'<rect x="120" y="520" width="520" height="80" rx="40" fill="#F3D3C8" stroke="#B85C4E" stroke-width="3"/>' + text(380, 570, 'кровь пациента', 's', 'middle')
    s += lines_at(380, 660, ['аппарат «искусственная почка»;', 'обычно не реже 3 раз в неделю по 4 ч'], 'cap')
    # перитонеальный
    s += text(1120, 130, 'Перитонеальный — внутри тела', 't', 'middle')
    s += f'<path d="{smooth([(940, 190), (1300, 190), (1340, 400), (1300, 600), (940, 600), (900, 400)], True)}" fill="#FBEAE6" stroke="#B85C4E" stroke-width="4"/>'
    s += f'<ellipse cx="1120" cy="420" rx="170" ry="120" fill="#DCEBF5" stroke="{INK}" stroke-width="4" stroke-dasharray="14 8"/>'
    s += f'<path d="M1200 320 Q 1260 250 1340 250 H 1440" fill="none" stroke="{GREY}" stroke-width="10"/>'
    s += f'<path d="M985 520 q 30 -40 0 -80 q -30 -40 0 -80" fill="none" stroke="{RED}" stroke-width="6"/>'
    for dy in (340, 400, 460):
        s += arrow(1000, dy, 1060, dy, URINE_LINE, 3)
    s += text(1120, 430, 'раствор', 's', 'middle', BLUE)
    s += f'<line x1="1120" y1="541" x2="1120" y2="560" stroke="{INK}" stroke-width="2.5"/>' + text(1120, 585, 'мембрана — брюшина', 's', 'middle')
    s += text(1440, 300, 'катетер', 'cap', 'end')
    s += lines_at(1100, 660, ['раствор вводят в брюшную полость', 'через катетер'], 'cap')
    s += text(750, 760, 'В основе — диффузия и осмос. Гемодиализ эффективнее перитонеального.', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'urinary-system.png': (urinary_system(), 1320, 960),
        'kidney-section.png': (kidney_section(), 1400, 900),
        'nephron.png': (nephron(), 1500, 860),
        'urine-processes.png': (urine_processes(), 1500, 760),
        'adh-loop.png': (adh_loop(), 1500, 760),
        'skin.png': (skin(), 1460, 850),
        'nitrogen-products.png': (nitrogen_products(), 1500, 730),
        'dialysis.png': (dialysis(), 1500, 800),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
