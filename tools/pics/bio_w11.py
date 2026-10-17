"""Рисунки недели 11 биологии (course/biology/week-11/pics/*.png): типы желёз, эндокринные железы, нервная и гуморальная регуляция,
обратная связь по глюкозе и CO₂, терморегуляция, фитогормоны, опыты с ауксином, фототропизм, движения растений.

Факты — по выжимке course/textbooks/bio-11-hormones.md (Б8 § 41–42, 44; Б9 § 25, 27–28; Б11-1 § 21–26; Б7а § 32; Б7м § 36). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w11.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, label, render, smooth, text

OUT = ROOT / 'course' / 'biology' / 'week-11' / 'pics'
BLUE, BLOOD, GLAND, SKIN, PLANT, LEAF = '#3A57A7', '#C0392B', '#F2C14E', '#F3D3C6', '#5E9E4A', '#9CCB86'


def lbl(px, py, tx, ty, s, color=INK):
    return label(px, py, tx, ty, s, 's', color)


def lines_at(x, y, rows, cls='s', anchor='middle', step=32, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def box(x, y, w, h, rows, fill=PAPER, stroke=INK, cls='s', color=None, step=30):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    y0 = y + h / 2 - (len(rows) - 1) * step / 2 + 9
    return s + lines_at(x + w / 2, y0, rows, cls, 'middle', step, color)


def cell(x, y, r=22, fill=GLAND):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="#8A6A2A" stroke-width="2"/><circle cx="{x}" cy="{y}" r="6" fill="#8A6A2A"/>'


def capillary(x1, y1, x2, y2, w=34):
    return f'<path d="M{x1} {y1} L {x2} {y2}" stroke="{BLOOD}" stroke-width="{w}" stroke-linecap="round" opacity=".85"/>'


def dots(points, col=RED, r=6):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>' for x, y in points)


# 1. Типы желёз ---------------------------------------------------------------------------------
def gland_types() -> str:
    s = text(800, 50, 'Железы внешней, внутренней и смешанной секреции', 'h', 'middle')
    titles = [('внешней секреции', '(экзокринная)', 'есть проток: секрет — в полость', 'или на поверхность тела'),
              ('внутренней секреции', '(эндокринная)', 'протока нет: гормон —', 'прямо в кровь'),
              ('смешанной секреции', '(поджелудочная, половые)', 'поджелудочная: сок — по протоку,', 'гормоны — в кровь')]
    for k, (t, t2, a, b) in enumerate(titles):
        x = 40 + k * 520
        s += f'<rect x="{x}" y="90" width="500" height="560" rx="18" fill="{PAPER}"/>' + text(x + 250, 130, t, 't', 'middle') + text(x + 250, 160, t2, 'cap', 'middle')
        cx = x + 250 - (60 if k == 2 else 0)
        if k in (0, 2):
            s += f'<path d="M{cx - 20} 420 V 220 M{cx + 20} 420 V 220" stroke="#8A6A2A" stroke-width="4"/>'
            s += f'<path d="M{cx - 120} 210 H {cx - 20} M{cx + 20} 210 H {cx + 120}" stroke="{INK}" stroke-width="5"/>'
            s += text(cx - 70, 196, 'поверхность' if k == 0 else 'кишка', 'cap', 'middle')
            s += ''.join(cell(cx + 60 * math.cos(a_ / 57.3), 450 + 50 * math.sin(a_ / 57.3)) for a_ in range(0, 360, 45))
            s += arrow(cx, 400, cx, 230, GREEN, 5) + text(cx - 30, 330, 'секрет', 'cap', 'end', GREEN)
        if k in (1, 2):
            gx = cx if k == 1 else cx + 180
            gy = 430 if k == 1 else 470
            s += capillary(gx - 140 if k == 1 else gx - 60, 590, gx + 140 if k == 1 else gx + 80, 590)
            s += ''.join(cell(gx + dx, gy + dy, 18 if k == 2 else 22, '#F6B9B4' if k == 2 else GLAND) for dx, dy in ((-40, 0), (0, -35), (40, 0), (0, 35)))
            s += arrow(gx, gy + 60, gx, 570, BLOOD, 4) + dots([(gx - 50, 590), (gx - 10, 586), (gx + 30, 592)], '#fff', 5)
            s += text(gx + 16, 545, 'гормон', 'cap', 'start', BLOOD) if k == 1 else text(gx - 14, 545, 'гормон', 'cap', 'end', BLOOD)
            if k == 2:
                s += text(gx, gy - 62, 'островок', 'cap', 'middle')
        s += text(cx, 615 if k != 2 else 545, '', 'cap')
        s += text(x + 250, 674, a, 's', 'middle') + text(x + 250, 704, b, 's', 'middle')
    return s


# 2. Эндокринные железы ------------------------------------------------------------------------
def endocrine_glands() -> str:
    s = text(750, 50, 'Железы внутренней секреции человека', 'h', 'middle')
    cx = 750
    body = smooth([(cx, 90), (cx + 70, 110), (cx + 80, 190), (cx + 40, 250), (cx + 45, 280), (cx + 170, 320), (cx + 190, 520),
                   (cx + 160, 760), (cx + 120, 900), (cx + 90, 1180), (cx - 90, 1180), (cx - 120, 900), (cx - 160, 760),
                   (cx - 190, 520), (cx - 170, 320), (cx - 45, 280), (cx - 40, 250), (cx - 80, 190), (cx - 70, 110)], True)
    s += f'<path d="{body}" fill="#FBF3EE" stroke="#B85C4E" stroke-width="3"/>'
    s += f'<ellipse cx="{cx}" cy="165" rx="58" ry="46" fill="#F1D9E8" stroke="#8A4A7A" stroke-width="2"/>'
    glands = [  # (x, y, rx, ry, fill, text_side, label)
        (cx, 200, 14, 11, GLAND, 'L', 'гипофиз — у основания мозга'),
        (cx, 300, 46, 20, '#E58C82', 'R', 'щитовидная — йод, тироксин'),
        (cx, 380, 34, 40, '#C7A6E0', 'L', 'тимус — за грудиной'),
        (cx - 60, 640, 22, 14, GLAND, 'L', 'надпочечники — над почками'),
        (cx + 10, 700, 78, 20, '#F6B9B4', 'R', 'поджелудочная — инсулин, глюкагон'),
        (cx, 960, 50, 24, '#9CCB86', 'L', 'половые железы'),
    ]
    s += f'<ellipse cx="{cx - 60}" cy="680" rx="26" ry="40" fill="#D9A7A0" stroke="#A2463C" stroke-width="2"/>'
    s += f'<ellipse cx="{cx + 60}" cy="680" rx="26" ry="40" fill="#D9A7A0" stroke="#A2463C" stroke-width="2"/>'
    s += f'<ellipse cx="{cx + 60}" cy="640" rx="22" ry="14" fill="{GLAND}" stroke="#8A6A2A" stroke-width="2"/>'
    for x, y, rx, ry, fill, side, lab in glands:
        s += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        tx = 470 if side == 'L' else 1000
        s += lbl(x + (-rx if side == 'L' else rx), y, tx, y + 8, lab)
    for k in range(4):
        s += f'<circle cx="{cx - 30 + (k % 2) * 60}" cy="{292 + (k // 2) * 16}" r="6" fill="#8A4A7A"/>'
    s += lbl(cx + 30, 308, 1000, 360, 'паращитовидные (4) — Ca и P', '#8A4A7A')
    # надпочечник крупно
    s += f'<rect x="1040" y="760" width="400" height="260" rx="16" fill="{PAPER}"/>' + text(1240, 795, 'надпочечник в разрезе', 's', 'middle')
    s += f'<ellipse cx="1240" cy="895" rx="120" ry="80" fill="{GLAND}" stroke="#8A6A2A" stroke-width="3"/>'
    s += f'<ellipse cx="1240" cy="895" rx="62" ry="38" fill="#E58C82" stroke="#A2463C" stroke-width="2"/>'
    s += text(1240, 903, 'мозговой', 'cap', 'middle', '#fff') + text(1240, 1005, 'кора — снаружи', 'cap', 'middle')
    s += f'<rect x="1040" y="1050" width="400" height="140" rx="16" fill="{PAPER}"/>'
    s += lines_at(1240, 1100, ['протоков нет: гормоны', 'выделяются прямо в кровь'], 's', step=36)
    return s


# 3. Нервная и гуморальная регуляция ---------------------------------------------------------------
def neural_humoral() -> str:
    s = text(800, 50, 'Нервная и гуморальная регуляция', 'h', 'middle')
    s += f'<rect x="40" y="90" width="740" height="520" rx="18" fill="{PAPER}"/>' + text(410, 130, 'нервная', 't', 'middle', BLUE)
    s += f'<circle cx="140" cy="300" r="40" fill="#F7E2A8" stroke="#8A6A2A" stroke-width="3"/>'
    s += f'<path d="M180 300 C 300 300 380 260 560 260" fill="none" stroke="#C9A54A" stroke-width="8"/>'
    s += f'<path d="M560 230 Q 700 210 720 280 Q 700 350 560 330 Z" fill="#F3C4BE" stroke="#A2463C" stroke-width="3"/>'
    s += text(640, 380, 'мышца или железа', 'cap', 'middle')
    s += arrow(260, 270, 460, 240, BLUE, 5) + text(360, 230, 'импульс', 'cap', 'middle', BLUE)
    s += lines_at(410, 470, ['по нервному волокну к конкретному', 'органу: быстро, адресно, кратко'], 's', step=36)
    s += f'<rect x="820" y="90" width="740" height="520" rx="18" fill="{PAPER}"/>' + text(1190, 130, 'гуморальная', 't', 'middle', BLOOD)
    s += f'<ellipse cx="920" cy="260" rx="60" ry="40" fill="{GLAND}" stroke="#8A6A2A" stroke-width="3"/>' + text(920, 330, 'железа', 'cap', 'middle')
    s += capillary(990, 260, 1500, 260, 40)
    s += dots([(1020 + 60 * k, 255 + (k % 2) * 10) for k in range(8)], '#fff', 7)
    for k, (x, ok) in enumerate(((1100, True), (1260, False), (1420, True))):
        s += f'<rect x="{x - 45}" y="330" width="90" height="70" rx="14" fill="{"#D9EEDF" if ok else "#fff"}" stroke="{GREEN if ok else GREY}" stroke-width="3"/>'
        if ok:
            s += f'<path d="M{x - 12} 330 v -14 h 24 v 14" fill="#9CCB86" stroke="{GREEN}" stroke-width="2"/>'
        s += text(x, 425, 'ответ' if ok else 'нет рецептора', 'cap', 'middle', GREEN if ok else GREY)
    s += lines_at(1190, 490, ['гормон с кровью ко многим клеткам;', 'отвечают только клетки с рецептором;', 'медленнее, но дольше'], 's', step=36)
    s += text(800, 660, 'Обе системы работают вместе — нейрогуморальная регуляция.', 's', 'middle')
    return s


# 4. Обратная связь по глюкозе ------------------------------------------------------------------
def loop_arrow(points, col):
    s = ''
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        s += arrow(x1, y1, x2, y2, col, 4)
    return s


def glucose_feedback() -> str:
    s = text(845, 50, 'Глюкоза крови: отрицательная обратная связь', 'h', 'middle')
    s += box(660, 330, 360, 90, ['норма глюкозы', 'в крови'], '#fff', INK, 't')
    up = [(40, ['глюкоза ↑'], '#FDECEC'), (372, ['β-клетки', 'островков'], PAPER), (700, ['инсулин'], '#FDECEC'),
          (1030, ['клетки берут глюкозу;', 'печень — гликоген'], '#fff'), (1360, ['глюкоза ↓'], '#FDECEC')]
    for x, rows, f in up:
        s += box(x, 100, 306, 90, rows, f, RED)
    s += ''.join(arrow(x + 308, 145, x + 368, 145, RED, 4) for x, *_ in up[:-1])
    s += arrow(1500, 192, 1000, 330, RED, 4) + arrow(680, 330, 185, 192, GREY, 3)
    down = [(40, ['глюкоза ↓'], '#E6F1F7'), (370, ['α-клетки', 'островков'], PAPER), (700, ['глюкагон'], '#E6F1F7'),
            (1030, ['печень: гликоген →', '→ глюкоза в кровь'], '#fff'), (1360, ['глюкоза ↑'], '#E6F1F7')]
    for x, rows, f in down:
        s += box(x, 560, 306, 90, rows, f, BLUE)
    s += ''.join(arrow(x + 308, 605, x + 368, 605, BLUE, 4) for x, *_ in down[:-1])
    s += arrow(1500, 558, 1000, 422, BLUE, 4) + arrow(680, 422, 185, 558, GREY, 3)
    s += text(845, 700, 'Ответ уменьшает исходное отклонение — показатель возвращается к норме.', 's', 'middle')
    return s


# 5. Обратная связь по CO₂ -----------------------------------------------------------------------
def co2_feedback() -> str:
    s = text(870, 50, chem('Регуляция дыхания по CO₂'), 'h', 'middle')
    steps = [['CO₂ в крови ↑', '(pH ↓)'], ['хеморецепторы', 'сосудов и', 'продолговатого мозга'],
             ['дыхательные центры:', 'продолговатый мозг', 'и мост'], ['диафрагма', 'и межрёберные', 'мышцы'], ['вентиляция ↑,', 'выведение CO₂ ↑']]
    for k, rows in enumerate(steps):
        x = 40 + k * 340
        s += box(x, 120, 310, 170, rows, '#FDECEC' if k in (0, 4) else PAPER, RED if k in (0, 4) else INK, 's', None, 34)
        if k < 4:
            s += arrow(x + 312, 205, x + 338, 205, INK, 4)
    s += f'<path d="M1555 292 C 1555 420 215 420 195 300" fill="none" stroke="{GREEN}" stroke-width="5"/>'
    s += f'<polygon points="195,292 181,318 211,316" fill="{GREEN}"/>'
    s += text(870, 445, 'CO₂ снижается к исходному уровню — отклонение уменьшается: отрицательная обратная связь', 's', 'middle', GREEN)
    return s


# 6. Терморегуляция -------------------------------------------------------------------------------
def thermoregulation() -> str:
    s = text(800, 50, 'Терморегуляция: гипоталамус и кожа', 'h', 'middle')
    s += box(560, 100, 480, 110, ['терморецепторы кожи и внутренних', 'органов → гипоталамус'], '#fff', INK)
    s += f'<rect x="40" y="260" width="740" height="420" rx="18" fill="#FDECEC"/>' + text(410, 296, 'жарко', 't', 'middle', RED)
    s += f'<rect x="820" y="260" width="740" height="420" rx="18" fill="#E6F1F7"/>' + text(1190, 300, 'холодно', 't', 'middle', BLUE)
    s += arrow(700, 212, 410, 258, RED, 4) + arrow(900, 212, 1190, 258, BLUE, 4)
    # кожа с сосудом
    for x0, wide, col in ((120, True, RED), (900, False, BLUE)):
        s += f'<rect x="{x0}" y="380" width="580" height="130" fill="{SKIN}" stroke="#B85C4E" stroke-width="2"/>'
        s += f'<path d="M{x0} 465 H {x0 + 580}" stroke="{BLOOD}" stroke-width="{26 if wide else 8}" stroke-linecap="round"/>'
        s += text(x0 + 290, 545, 'сосуды кожи расширяются' if wide else 'сосуды кожи сужаются', 's', 'middle', col)
    for k in range(5):
        x = 200 + k * 110
        s += f'<path d="M{x} 380 q -8 -20 0 -30 q 8 -12 0 -22" fill="none" stroke="{BLUE}" stroke-width="4"/>'
    s += text(410, 330 - 40, '', 'cap')
    s += lines_at(410, 600, ['потоотделение и испарение пота', 'теплоотдача ↑'], 's', step=40, color=RED)
    s += lines_at(1190, 600, ['теплоотдача ↓;', 'дрожь мышц — теплопродукция ↑'], 's', step=40, color=BLUE)
    return s


# 7. Фитогормоны ---------------------------------------------------------------------------------
def phytohormones() -> str:
    s = text(800, 50, 'Фитогормоны и их основные эффекты', 'h', 'middle')
    items = [('ауксин', ['растяжение клеток,', 'образование корней'], LEAF), ('гиббереллин', ['рост междоузлий', 'и стебля'], '#C9E5A8'),
             ('цитокинин', ['деление клеток'], '#F7EFC8'), ('этилен', ['созревание плодов'], '#F8D5B0'),
             ('абсцизовая к-та', ['покой, ответ', 'на стресс'], '#DCEBF5')]
    for k, (name, rows, col) in enumerate(items):
        x = 40 + k * 310
        s += f'<rect x="{x}" y="100" width="290" height="440" rx="18" fill="{col}"/>'
        s += text(x + 145, 150, name, 't', 'middle')
        cx, cy = x + 145, 300
        if k == 0:
            s += ''.join(f'<rect x="{cx - 60 + j * 42}" y="{cy - 70}" width="36" height="{90 + j * 30}" rx="10" fill="#fff" stroke="{PLANT}" stroke-width="3"/>' for j in range(3))
            s += ''.join(f'<path d="M{cx - 30 + j * 30} {cy + 70} q {j * 10 - 10} 40 {j * 20 - 20} 70" fill="none" stroke="#8A6A2A" stroke-width="4"/>' for j in range(3))
        elif k == 1:
            s += f'<path d="M{cx} {cy + 120} V {cy - 80}" stroke="{PLANT}" stroke-width="8"/>'
            s += ''.join(f'<path d="M{cx} {cy + 100 - j * 70} q 40 -10 60 -40 M{cx} {cy + 100 - j * 70} q -40 -10 -60 -40" fill="none" stroke="{PLANT}" stroke-width="5"/>' for j in range(3))
        elif k == 2:
            s += ''.join(f'<rect x="{cx - 70 + (j % 4) * 36}" y="{cy - 50 + (j // 4) * 40}" width="32" height="34" rx="6" fill="#fff" stroke="{PLANT}" stroke-width="2"/>' for j in range(12))
        elif k == 3:
            s += f'<circle cx="{cx - 40}" cy="{cy}" r="40" fill="#9CCB86" stroke="{PLANT}" stroke-width="3"/>' + arrow(cx, cy, cx + 30, cy, INK, 4)
            s += f'<circle cx="{cx + 75}" cy="{cy}" r="40" fill="#E8414A" stroke="#A2463C" stroke-width="3"/>'
        else:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="60" ry="40" fill="#E9DCC0" stroke="#8A7350" stroke-width="3"/>'
            s += text(cx, cy + 10, 'Zz', 't', 'middle', BLUE)
        s += lines_at(x + 145, 470, rows, 's', step=34)
    s += text(800, 590, 'Фитогормоны действуют в малых количествах и регулируют рост и развитие растения.', 's', 'middle')
    return s


# 8. Опыты с ауксином ----------------------------------------------------------------------------
def coleoptile(x, base, h=180, bend=0, col=PLANT, tip=True):
    top = (x + bend, base - h)
    d = f'M{x - 14} {base} C {x - 14} {base - h * 0.5} {top[0] - 14} {top[1] + 40} {top[0] - 14} {top[1] + 16} ' \
        f'Q {top[0]} {top[1] - 14} {top[0] + 14} {top[1] + 16} C {top[0] + 14} {top[1] + 40} {x + 14} {base - h * 0.5} {x + 14} {base} Z'
    return f'<path d="{d}" fill="#D9EEDF" stroke="{col}" stroke-width="3"/>' + f'<path d="M{x - 60} {base} H {x + 60}" stroke="#8A7350" stroke-width="6"/>'


def light(x, y):
    return ''.join(arrow(x, y + k * 30, x + 70, y + k * 30, '#E0A100', 4) for k in range(3))


def auxin_experiments() -> str:
    s = text(800, 50, 'Опыты, открывшие ауксин', 'h', 'middle')
    panels = ['Ч. и Ф. Дарвин', 'П. Бойсен-Йенсен', 'Ф. Вент']
    for k, t in enumerate(panels):
        s += f'<rect x="{40 + k * 520}" y="90" width="500" height="560" rx="18" fill="{PAPER}"/>' + text(290 + k * 520, 130, t, 't', 'middle')
    # Дарвин
    s += light(60, 220) + coleoptile(220, 460, bend=50) + coleoptile(400, 460)
    s += f'<rect x="384" y="268" width="32" height="40" rx="6" fill="{INK}"/>' + text(400, 500, 'колпачок', 'cap', 'middle')
    s += text(220, 500, 'верхушка открыта', 'cap', 'middle')
    s += lines_at(290, 570, ['свет воспринимает верхушка;', 'под колпачком изгиба нет'], 's', step=32)
    # Бойсен-Йенсен
    s += light(580, 220) + coleoptile(740, 460, bend=45) + coleoptile(920, 460)
    s += f'<rect x="716" y="330" width="48" height="12" fill="#F7E2A8" stroke="#8A6A2A" stroke-width="2"/>' + text(740, 500, 'желатин', 'cap', 'middle')
    s += f'<rect x="896" y="330" width="48" height="12" fill="#B8C4CE" stroke="{GREY}" stroke-width="2"/>' + text(920, 500, 'слюда', 'cap', 'middle')
    s += lines_at(810, 570, ['сигнал проходит через желатин,', 'но не через слюду — это вещество'], 's', step=32)
    # Вент
    s += f'<rect x="1150" y="300" width="70" height="30" fill="#F2E3B5" stroke="#8A6A2A" stroke-width="2"/>' + coleoptile(1185, 300, 90, tip=True)
    s += text(1185, 360, 'агар', 'cap', 'middle')
    s += coleoptile(1420, 460, 150, bend=-40)
    s += f'<rect x="1372" y="296" width="40" height="24" fill="#F2E3B5" stroke="#8A6A2A" stroke-width="2" transform="rotate(-10 1392 308)"/>'
    s += text(1420, 500, 'агар сбоку,', 'cap', 'middle') + text(1420, 526, 'в темноте', 'cap', 'middle')
    s += lines_at(1330, 570, ['вещество переходит в агар', 'и вызывает изгиб без света'], 's', step=32)
    return s


# 9. Фототропизм ----------------------------------------------------------------------------------
def phototropism() -> str:
    s = text(650, 50, 'Фототропизм: побег растёт к свету', 'h', 'middle')
    s += f'<circle cx="120" cy="250" r="50" fill="#F7D04A"/>' + ''.join(arrow(190, 210 + k * 40, 330, 210 + k * 40, '#E0A100', 4) for k in range(3))
    s += f'<path d="M560 620 C 560 480 540 360 470 240" fill="none" stroke="{PLANT}" stroke-width="60" stroke-linecap="round"/>'
    for k in range(10):
        t = 0.08 + k * 0.085
        bx = (1 - t) ** 3 * 560 + 3 * (1 - t) ** 2 * t * 560 + 3 * (1 - t) * t ** 2 * 540 + t ** 3 * 470
        by = (1 - t) ** 3 * 620 + 3 * (1 - t) ** 2 * t * 480 + 3 * (1 - t) * t ** 2 * 360 + t ** 3 * 240
        dx = 3 * (1 - t) ** 2 * 0 + 6 * (1 - t) * t * (540 - 560) + 3 * t ** 2 * (470 - 540)
        dy = 3 * (1 - t) ** 2 * (480 - 620) + 6 * (1 - t) * t * (360 - 480) + 3 * t ** 2 * (240 - 360)
        n = (dx * dx + dy * dy) ** 0.5
        s += f'<circle cx="{bx - dy / n * 16:.0f}" cy="{by + dx / n * 16:.0f}" r="6" fill="{RED}"/>'
    s += f'<path d="M500 640 H 660" stroke="#8A7350" stroke-width="10"/>'
    s += text(470, 180, 'верхушка воспринимает свет', 'cap', 'middle')
    s += f'<rect x="760" y="150" width="460" height="400" rx="18" fill="{PAPER}"/>'
    s += f'<rect x="800" y="210" width="60" height="120" rx="10" fill="#fff" stroke="{PLANT}" stroke-width="3"/>'
    s += f'<rect x="900" y="190" width="60" height="180" rx="10" fill="#fff" stroke="{PLANT}" stroke-width="3"/>'
    s += dots([(930, 230), (918, 270), (942, 310), (930, 350)], RED, 6)
    s += text(830, 360, 'светлая', 'cap', 'middle') + text(930, 400, 'теневая', 'cap', 'middle')
    s += lines_at(990, 460, ['ауксина больше на теневой', 'стороне — её клетки растягиваются', 'сильнее, побег изгибается к свету'], 'cap', step=30)
    return s


# 10. Движения растений ---------------------------------------------------------------------------
def plant_movements() -> str:
    s = text(800, 50, 'Тропизм, настия, таксис', 'h', 'middle')
    for k, (t, t2) in enumerate((('тропизм', 'рост к стимулу или от него'), ('настия', 'не зависит от стороны стимула'), ('таксис', 'движение всего организма'))):
        s += f'<rect x="{40 + k * 520}" y="90" width="500" height="520" rx="18" fill="{PAPER}"/>' + text(290 + k * 520, 130, t, 't', 'middle') + text(290 + k * 520, 160, t2, 'cap', 'middle')
    # тропизм: побег к свету, корень вниз
    s += light(70, 220)
    s += f'<path d="M300 380 C 300 300 280 250 240 210" fill="none" stroke="{PLANT}" stroke-width="16" stroke-linecap="round"/>'
    s += f'<path d="M230 380 H 370" stroke="#8A7350" stroke-width="6"/>'
    s += f'<path d="M300 380 C 300 450 300 500 300 560" fill="none" stroke="#8A6A2A" stroke-width="10"/>' + arrow(380, 440, 380, 540, GREY, 4)
    s += text(395, 500, 'сила', 'cap', 'start') + text(395, 524, 'тяжести', 'cap', 'start')
    s += text(290, 600, 'побег — к свету, корень — вниз', 'cap', 'middle')
    # настия: мимоза
    for j, (x0, closed) in enumerate(((660, False), (880, True))):
        s += f'<path d="M{x0} 520 V 260" stroke="{PLANT}" stroke-width="6"/>'
        for i in range(5):
            y = 290 + i * 45
            if closed:
                s += f'<path d="M{x0} {y} l 14 -30 M{x0} {y} l -14 -30" stroke="{PLANT}" stroke-width="10" stroke-linecap="round"/>'
            else:
                s += f'<path d="M{x0} {y} l 60 -10 M{x0} {y} l -60 -10" stroke="{PLANT}" stroke-width="10" stroke-linecap="round"/>'
        s += text(x0, 560, 'до касания' if not closed else 'после касания', 'cap', 'middle')
    s += arrow(730, 390, 820, 390, INK, 4)
    # таксис: хламидомонада
    s += f'<circle cx="1490" cy="220" r="40" fill="#F7D04A"/>'
    for j, x in enumerate((1150, 1250, 1350)):
        y = 460 - j * 70
        s += f'<ellipse cx="{x}" cy="{y}" rx="34" ry="24" fill="{LEAF}" stroke="{PLANT}" stroke-width="3" transform="rotate(-30 {x} {y})" opacity="{0.45 + j * 0.27:.2f}"/>'
    s += f'<path d="M1376 340 q 20 -26 44 -26 M1376 340 q 26 -8 44 6" fill="none" stroke="{PLANT}" stroke-width="3"/>'
    s += arrow(1150, 520, 1420, 300, GREY, 3)
    s += text(1330, 600, 'хламидомонада плывёт к свету', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'gland-types.png': (gland_types(), 1600, 730),
        'endocrine-glands.png': (endocrine_glands(), 1500, 1220),
        'neural-humoral.png': (neural_humoral(), 1600, 700),
        'glucose-feedback.png': (glucose_feedback(), 1690, 730),
        'co2-feedback.png': (co2_feedback(), 1740, 480),
        'thermoregulation.png': (thermoregulation(), 1600, 710),
        'phytohormones.png': (phytohormones(), 1600, 620),
        'auxin-experiments.png': (auxin_experiments(), 1600, 680),
        'phototropism.png': (phototropism(), 1260, 680),
        'plant-movements.png': (plant_movements(), 1600, 640),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
