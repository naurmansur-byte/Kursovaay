"""Рисунки недели 10 биологии (course/biology/week-10/pics/*.png): типы нервной системы, нейрон, синапс, спинной мозг,
рефлекторная дуга, головной мозг и доли коры, вегетативная регуляция, глаз и оптика, ухо.

Факты — по выжимке course/textbooks/bio-10-nervous.md (Б7а § 35–43, Б8 § 38–40, 43, Б9 § 22–24, Б10-2 § 100–110). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w10.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, label, render, smooth, text

OUT = ROOT / 'course' / 'biology' / 'week-10' / 'pics'
BLUE, NERVE, MYELIN, GRAYM, WHITEM = '#3A57A7', '#E0A33A', '#F6E7B5', '#B9A9C9', '#F4F0F7'
SKIN, MUSCLE, MUSCLE_LINE = '#F3D3C8', '#E58C82', '#A2463C'


def lbl(px, py, tx, ty, s, color=INK):
    return label(px, py, tx, ty, s, 's', color)


def lines_at(x, y, rows, cls='s', anchor='middle', step=32, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def node(x, y, r=9, fill=NERVE):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="#8A6A2A" stroke-width="2"/>'


# 1. Типы нервной системы ----------------------------------------------------------------------
def nervous_system_types() -> str:
    s = text(800, 50, 'Типы нервной системы животных', 'h', 'middle')
    titles = [('Диффузная', ['гидра', '(кишечнополостные)']), ('Лестничная', ['(стволовая): планария', '(плоские черви)']),
              ('Узловая', ['дождевой червь:', 'брюшная цепочка']), ('Трубчатая', ['хордовые:', 'трубка на спине'])]
    for k, (t1, t2) in enumerate(titles):
        x = 20 + k * 395
        cx, cy = x + 185, 290
        s += f'<rect x="{x}" y="90" width="375" height="440" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += text(cx, 135, t1, 't', 'middle')
        if k == 0:
            s += f'<path d="M{cx - 45} 380 V 220 Q {cx} 190 {cx + 45} 220 V 380 Z" fill="#E6F1F7" stroke="{BLUE}" stroke-width="3"/>'
            for t in (-30, -10, 10, 30):
                s += f'<path d="M{cx + t} 210 q {t / 3} -40 {t * 1.4} -50" fill="none" stroke="{BLUE}" stroke-width="3"/>'
            pts = [(cx - 30 + (i % 4) * 20, 235 + (i // 4) * 30 + (i % 2) * 8) for i in range(20)]
            for i, (px, py) in enumerate(pts):
                for qx, qy in pts[i + 1:i + 3]:
                    s += f'<line x1="{px}" y1="{py}" x2="{qx}" y2="{qy}" stroke="{NERVE}" stroke-width="2"/>'
            s += ''.join(node(px, py, 5) for px, py in pts)
        elif k == 1:
            s += f'<path d="{smooth([(cx, 175), (cx + 60, 230), (cx + 50, 380), (cx, 410), (cx - 50, 380), (cx - 60, 230)], True)}" fill="#F3EDE4" stroke="#8A7350" stroke-width="3"/>'
            s += node(cx - 18, 215, 12) + node(cx + 18, 215, 12)
            s += f'<path d="M{cx - 18} 225 V 390 M{cx + 18} 225 V 390" stroke="{NERVE}" stroke-width="6"/>'
            for y in range(250, 390, 28):
                s += f'<path d="M{cx - 18} {y} H {cx + 18}" stroke="{NERVE}" stroke-width="4"/>'
        elif k == 2:
            s += f'<rect x="{cx - 40}" y="170" width="80" height="250" rx="40" fill="#F6D7D2" stroke="#A2463C" stroke-width="3"/>'
            for y in range(195, 410, 22):
                s += f'<path d="M{cx - 38} {y} H {cx + 38}" stroke="#D9A7A0" stroke-width="2"/>'
            s += f'<ellipse cx="{cx}" cy="200" rx="18" ry="12" fill="none" stroke="{NERVE}" stroke-width="5"/>'
            s += f'<path d="M{cx} 212 V 405" stroke="{NERVE}" stroke-width="5"/>' + ''.join(node(cx, y, 7) for y in range(230, 410, 22))
        else:
            s += f'<path d="{smooth([(cx - 150, 300), (cx - 90, 250), (cx + 40, 245), (cx + 130, 270), (cx + 150, 300), (cx + 130, 330), (cx + 40, 350), (cx - 90, 345)], True)}" fill="#E6F1F7" stroke="{BLUE}" stroke-width="3"/>'
            s += f'<path d="M{cx + 110} 268 Q {cx + 40} 262 {cx - 120} 280" fill="none" stroke="{NERVE}" stroke-width="8" stroke-linecap="round"/>'
            s += f'<ellipse cx="{cx + 105}" cy="272" rx="24" ry="14" fill="{NERVE}" stroke="#8A6A2A" stroke-width="2"/>'
            s += text(cx + 50, 225, 'головной мозг', 'cap', 'middle') + text(cx - 30, 318, 'спинной мозг', 'cap', 'middle')
        s += lines_at(cx, 470, t2, 'cap')
    return s


# 2. Нейрон ---------------------------------------------------------------------------------------
def neuron() -> str:
    s = text(825, 50, 'Строение нейрона', 'h', 'middle') + '<g transform="translate(150 0)">'
    cx, cy = 260, 300
    for a in (150, 190, 220, 250, 120, 280):
        r = math.radians(a)
        x1, y1 = cx + 60 * math.cos(r), cy - 60 * math.sin(r)
        x2, y2 = cx + 150 * math.cos(r), cy - 150 * math.sin(r)
        s += f'<path d="M{x1:.0f} {y1:.0f} L {x2:.0f} {y2:.0f}" stroke="#C9A54A" stroke-width="8" stroke-linecap="round"/>'
        for d in (-25, 25):
            r2 = math.radians(a + d)
            s += f'<path d="M{x2:.0f} {y2:.0f} l {40 * math.cos(r2):.0f} {-40 * math.sin(r2):.0f}" stroke="#C9A54A" stroke-width="5" stroke-linecap="round"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="70" fill="#F7E2A8" stroke="#8A6A2A" stroke-width="4"/><circle cx="{cx - 8}" cy="{cy}" r="26" fill="#C9B3E0" stroke="#5B4A8A" stroke-width="3"/>'
    s += f'<path d="M{cx + 68} {cy} H 1290" stroke="#C9A54A" stroke-width="10"/>'
    for k in range(5):
        x = 380 + k * 175
        s += f'<rect x="{x}" y="{cy - 24}" width="150" height="48" rx="22" fill="{MYELIN}" stroke="#B8902A" stroke-width="3"/>'
    for b in (-50, 0, 50):
        s += f'<path d="M1290 {cy} L 1380 {cy + b}" stroke="#C9A54A" stroke-width="6"/>' + f'<circle cx="1390" cy="{cy + b}" r="14" fill="#F7E2A8" stroke="#8A6A2A" stroke-width="3"/>'
    s += arrow(100, 170, 170, 225, BLUE, 4) + text(60, 150, 'к телу', 's', 'start', BLUE)
    s += arrow(900, 380, 1100, 380, RED, 5) + text(1000, 420, 'импульс от тела по аксону', 's', 'middle', RED)
    s += lbl(150, 170, 120, 100, 'дендриты') + lbl(cx - 8, cy, 120, 470, 'ядро') + lbl(cx + 40, cy + 50, 300, 470, 'тело нейрона')
    s += lbl(455, cy - 24, 560, 150, 'миелиновая оболочка (шванновская клетка)', '#8A6A2A')
    s += lbl(542, cy, 640, 470, 'перехват Ранвье') + lbl(1390, cy + 50, 1250, 470, 'окончания → синапсы')
    s += lbl(1200, cy, 1250, 200, 'аксон')
    return s + '</g>'


# 3. Синапс ---------------------------------------------------------------------------------------
def synapse() -> str:
    s = text(900, 50, 'Химический синапс', 'h', 'middle') + '<g transform="translate(250 0)">'
    s += f'<path d="M520 90 V 200 Q 400 230 400 330 Q 400 420 650 420 Q 900 420 900 330 Q 900 230 780 200 V 90" fill="#F7E2A8" stroke="#8A6A2A" stroke-width="4"/>'
    for k in range(7):
        x, y = 470 + (k % 4) * 110 + (k // 4) * 50, 300 + (k // 4) * 60
        s += f'<circle cx="{x}" cy="{y}" r="24" fill="#fff" stroke="{BLUE}" stroke-width="3"/>' + ''.join(f'<circle cx="{x + dx}" cy="{y + dy}" r="4" fill="{RED}"/>' for dx, dy in ((-7, -5), (6, -6), (0, 7)))
    s += f'<path d="M380 420 H 920" stroke="#8A6A2A" stroke-width="6"/>'
    s += f'<path d="M300 480 H 1000 V 640 H 300 Z" fill="#F3C4BE" stroke="{MUSCLE_LINE}" stroke-width="4"/>'
    for x in range(450, 870, 60):
        s += f'<path d="M{x - 12} 480 v -14 h 24 v 14" fill="#9CCB86" stroke="{GREEN}" stroke-width="2"/>'
    for x, y in ((520, 440), (600, 452), (690, 438), (770, 450), (640, 462)):
        s += f'<circle cx="{x}" cy="{y}" r="5" fill="{RED}"/>'
    s += arrow(650, 140, 650, 230, RED, 6) + text(670, 175, 'импульс', 's', 'start', RED)
    s += lbl(470, 300, 230, 260, 'пузырьки с медиатором', BLUE)
    s += lbl(395, 420, 230, 400, 'пресинаптическая мембрана', '#8A6A2A')
    s += lbl(905, 452, 1080, 452, 'синаптическая щель')
    s += lbl(870, 470, 1080, 520, 'рецепторы', GREEN)
    s += lbl(990, 560, 1080, 590, 'постсинаптическая мембрана', MUSCLE_LINE)
    s += text(650, 690, 'Медиатор из окончания проходит щель и действует на рецепторы следующей клетки.', 's', 'middle')
    return s + '</g>'


# 4. Спинной мозг -------------------------------------------------------------------------------
def butterfly(cx, cy, k=1.0):
    pts = [(0, -30), (25, -95), (60, -105), (55, -60), (30, -20), (80, 40), (85, 85), (40, 70), (0, 30),
           (-40, 70), (-85, 85), (-80, 40), (-30, -20), (-55, -60), (-60, -105), (-25, -95)]
    return smooth([(cx + x * k, cy + y * k) for x, y in pts], True)


def spinal_cord() -> str:
    s = text(850, 50, 'Спинной мозг в поперечном разрезе', 'h', 'middle') + '<g transform="translate(260 0)">'
    cx, cy = 560, 400
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="230" ry="190" fill="{WHITEM}" stroke="{INK}" stroke-width="4"/>'
    s += f'<path d="{butterfly(cx, cy, 1.5)}" fill="{GRAYM}" stroke="#5B4A8A" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="12" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    # корешки справа
    s += f'<path d="M{cx + 85} {cy - 150} Q {cx + 200} {cy - 230} {cx + 330} {cy - 190}" fill="none" stroke="{BLUE}" stroke-width="12"/>'
    s += f'<ellipse cx="{cx + 340}" cy="{cy - 185}" rx="42" ry="30" fill="#C9D7EF" stroke="{BLUE}" stroke-width="3"/>'
    s += f'<path d="M{cx + 110} {cy + 110} Q {cx + 230} {cy + 170} {cx + 380} {cy + 80}" fill="none" stroke="{RED}" stroke-width="12"/>'
    s += f'<path d="M{cx + 375} {cy - 165} Q {cx + 420} {cy - 90} {cx + 440} {cy - 40}" fill="none" stroke="{BLUE}" stroke-width="12"/>'
    s += f'<path d="M{cx + 380} {cy + 80} Q {cx + 425} {cy + 10} {cx + 440} {cy - 40}" fill="none" stroke="{RED}" stroke-width="12"/>'
    s += f'<path d="M{cx + 440} {cy - 40} H {cx + 600}" stroke="#7A5BA0" stroke-width="16"/>'
    s += lbl(cx - 70, cy - 120, 180, 130, 'задний рог (чувствительный)')
    s += lbl(cx - 90, cy + 100, 180, 650, 'передний рог (двигательный)')
    s += lbl(cx - 30, cy - 5, 180, 400, 'серое вещество (внутри)', '#5B4A8A')
    s += lbl(cx - 200, cy - 90, 180, 280, 'белое вещество (снаружи)')
    s += lbl(cx, cy + 12, 180, 520, 'спинномозговой канал')
    s += lbl(cx + 230, cy - 210, 760, 120, 'задний корешок — вход', BLUE)
    s += lbl(cx + 360, cy - 210, 1000, 165, 'спинномозговой узел', BLUE)
    s += lbl(cx + 250, cy + 150, 860, 690, 'передний корешок — выход', RED)
    s += lbl(cx + 560, cy - 40, 1160, 300, 'смешанный нерв', '#7A5BA0')
    return s + '</g>'


# 5. Рефлекторная дуга --------------------------------------------------------------------------
def reflex_arc() -> str:
    s = text(750, 50, 'Рефлекторная дуга: пять звеньев', 'h', 'middle')
    cx, cy = 900, 360
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="150" ry="125" fill="{WHITEM}" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="{butterfly(cx, cy, 1.0)}" fill="{GRAYM}" stroke="#5B4A8A" stroke-width="2"/>'
    # рецептор в коже пальца
    s += f'<path d="M80 520 Q 160 470 260 500 L 260 560 Q 160 590 80 560 Z" fill="{SKIN}" stroke="#B85C4E" stroke-width="3"/>'
    s += f'<circle cx="120" cy="530" r="10" fill="{BLUE}"/>'
    # чувствительный нейрон: к узлу и в задний рог
    s += f'<path d="M120 530 C 300 420 520 240 760 220" fill="none" stroke="{BLUE}" stroke-width="6"/>'
    s += f'<circle cx="760" cy="220" r="18" fill="#C9D7EF" stroke="{BLUE}" stroke-width="3"/>'
    s += f'<path d="M778 222 Q 840 240 880 290" fill="none" stroke="{BLUE}" stroke-width="6"/>'
    # вставочный
    s += f'<path d="M880 290 Q 900 330 870 400" fill="none" stroke="#5B4A8A" stroke-width="6"/>' + f'<circle cx="890" cy="330" r="10" fill="#5B4A8A"/>'
    # двигательный
    s += f'<circle cx="860" cy="410" r="14" fill="#F3C4BE" stroke="{RED}" stroke-width="3"/>'
    s += f'<path d="M850 420 C 700 520 520 600 380 640" fill="none" stroke="{RED}" stroke-width="6"/>'
    s += f'<path d="M260 610 Q 330 590 400 640 Q 330 700 260 670 Z" fill="{MUSCLE}" stroke="{MUSCLE_LINE}" stroke-width="3"/>'
    for x, y in ((380, 400), (600, 300)):
        s += arrow(x, y, x + 50, y - 25, BLUE, 4)
    s += arrow(650, 530, 590, 560, RED, 4)
    marks = [(120, 530, '1', 'рецептор'), (500, 360, '2', 'чувствительный нейрон'), (890, 330, '3', 'центр в ЦНС (вставочный)'),
             (620, 545, '4', 'двигательный нейрон'), (330, 640, '5', 'рабочий орган — мышца')]
    for k, (x, y, n, cap) in enumerate(marks):
        s += f'<circle cx="{x + 28}" cy="{y - 30}" r="20" fill="{RED}"/>' + text(x + 28, y - 21, n, 's', 'middle', '#fff')
    for k, (x, y, n, cap) in enumerate(marks):
        s += text(1120, 180 + k * 52, f'{n} — {cap}', 's', 'start')
    s += f'<rect x="1100" y="460" width="380" height="200" rx="16" fill="{PAPER}"/>'
    s += lines_at(1290, 505, ['Коленный рефлекс:', 'чувствительный нейрон', 'сразу на двигательный —', 'вставочного нет'], 's', step=34)
    s += text(760, 185, 'узел', 'cap', 'middle', BLUE) + text(cx, cy + 160, 'спинной мозг', 'cap', 'middle')
    return s


# 6. Головной мозг ----------------------------------------------------------------------------------
def brain_cortex() -> str:
    s = text(1070, 50, 'Головной мозг: отделы и доли коры', 'h', 'middle') + '<g transform="translate(520 0)">'
    # слева — отделы (продольный разрез, схема)
    s += f'<path d="{smooth([(110, 300), (160, 170), (330, 120), (520, 150), (600, 260), (560, 380), (420, 410), (250, 400), (150, 380)], True)}" fill="#F6D7D2" stroke="#A2463C" stroke-width="3"/>'
    s += f'<ellipse cx="380" cy="360" rx="60" ry="34" fill="#F2C14E" stroke="#8A6A2A" stroke-width="2"/>'
    s += f'<ellipse cx="420" cy="410" rx="40" ry="26" fill="#9CCB86" stroke="{GREEN}" stroke-width="2"/>'
    s += f'<path d="{smooth([(470, 420), (560, 400), (600, 460), (520, 500), (460, 480)], True)}" fill="#C7A6E0" stroke="#5B4A8A" stroke-width="2"/>'
    s += f'<ellipse cx="440" cy="455" rx="34" ry="22" fill="#7FB3D5" stroke="{BLUE}" stroke-width="2"/>'
    s += f'<path d="M430 470 Q 420 520 425 590" stroke="#7FB3D5" stroke-width="30" fill="none"/>'
    s += lbl(300, 220, 90, 110, 'большие полушария (кора)', '#A2463C')
    s += lbl(350, 360, 90, 460, 'промежуточный: голод, жажда, температура', '#8A6A2A')
    s += lbl(410, 410, 90, 510, 'средний: ориентировочные рефлексы', GREEN)
    s += lbl(450, 455, 90, 560, 'мост: связь отделов', BLUE)
    s += lbl(428, 560, 90, 610, 'продолговатый: дыхание, сердце', BLUE)
    s += lbl(540, 450, 650, 520, 'мозжечок: координация', '#5B4A8A')
    s += '</g><g transform="translate(600 0)">'
    # справа — доли
    x0 = 850
    lobes = [('лобная', '#F2C14E', [(860, 300), (900, 170), (1030, 130), (1080, 220), (1060, 350), (940, 380)]),
             ('теменная', '#9CCB86', [(1030, 130), (1180, 120), (1260, 200), (1170, 280), (1080, 220)]),
             ('затылочная', '#7FB3D5', [(1260, 200), (1320, 290), (1270, 380), (1190, 350), (1170, 280)]),
             ('височная', '#E58C82', [(940, 380), (1060, 350), (1080, 220), (1170, 280), (1190, 350), (1120, 440), (980, 440)])]
    for name, col, pts in lobes:
        s += f'<path d="M{" L".join(f"{x} {y}" for x, y in pts)} Z" fill="{col}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    s += text(965, 260, 'лобная', 's', 'middle') + text(1165, 190, 'теменная', 's', 'middle') + text(1248, 300, 'затылоч.', 'cap', 'middle')
    s += text(1080, 400, 'височная', 's', 'middle')
    s += lines_at(890, 565, ['лобная — мышление, речь, движения', 'теменная — кожно-мышечная чувствительность',
                             'височная — слух', 'затылочная — зрение'], 'cap', 'start', step=34)
    return s + '</g>'


# 7. Вегетативная регуляция ---------------------------------------------------------------------------
def autonomic_effects() -> str:
    s = text(725, 50, 'Вегетативная нервная система', 'h', 'middle')
    s += f'<rect x="600" y="90" width="380" height="70" rx="14" fill="#FDECEC"/>' + text(790, 136, 'симпатическая', 't', 'middle', RED)
    s += f'<rect x="1000" y="90" width="380" height="70" rx="14" fill="#E6F1F7"/>' + text(1190, 136, 'парасимпатическая', 't', 'middle', BLUE)
    rows = [('сердце', 'учащает', 'замедляет'), ('зрачок', 'расширяет', 'сужает'), ('бронхи и бронхиолы', 'расширяет', '—'),
            ('пищеварение (слюна, соки, перистальтика)', 'угнетает', 'усиливает'), ('давление', 'повышает', 'понижает')]
    for k, (organ, sym, par) in enumerate(rows):
        y = 190 + k * 80
        s += f'<rect x="60" y="{y}" width="1330" height="68" rx="12" fill="{"#fff" if k % 2 else PAPER}"/>'
        s += text(80, y + 44, organ, 's')
        s += text(790, y + 44, sym, 't', 'middle', RED) + text(1190, y + 44, par, 't', 'middle', BLUE)
    s += lines_at(725, 640, ['Симпатическая переводит организм в активное состояние; парасимпатическая — наоборот.',
                             'Центры парасимпатической — в стволе мозга и крестцовом отделе; крупнейший нерв — блуждающий.'], 'cap', step=32)
    return s


# 8. Глаз ---------------------------------------------------------------------------------------
def eye(cx, cy, r, focus_dx=0, small=False):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FBFBFB" stroke="#8A7350" stroke-width="{3 if small else 6}"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r - (5 if small else 12)}" fill="none" stroke="#B85C4E" stroke-width="{2 if small else 5}"/>'
    s += f'<path d="M{cx - r * 0.75} {cy - r * 0.62} A {r * 0.65} {r * 0.65} 0 0 0 {cx - r * 0.75} {cy + r * 0.62}" fill="#E6F1F7" stroke="{BLUE}" stroke-width="{2 if small else 4}"/>'
    s += f'<ellipse cx="{cx - r * 0.55}" cy="{cy}" rx="{r * 0.14}" ry="{r * 0.33}" fill="#F7E2A8" stroke="#8A6A2A" stroke-width="{2 if small else 3}"/>'
    return s


def eye_optics() -> str:
    s = text(950, 50, 'Глаз: строение и ход лучей', 'h', 'middle') + '<g transform="translate(90 0)">'
    cx, cy, r = 600, 360, 230
    s += eye(cx, cy, r)
    s += f'<path d="M{cx - r * 0.66} {cy - r * 0.42} l -10 -25 M{cx - r * 0.66} {cy + r * 0.42} l -10 25" stroke="{INK}" stroke-width="10"/>'
    s += f'<path d="M{cx + r - 6} {cy + 30} L {cx + r + 120} {cy + 60}" stroke="{NERVE}" stroke-width="22"/>'
    for y0 in (-80, 0, 80):
        s += f'<path d="M160 {cy + y0} L {cx - r * 0.55} {cy + y0 * 0.6} L {cx + r - 14} {cy}" fill="none" stroke="{RED}" stroke-width="3"/>'
    s += f'<circle cx="{cx + r - 14}" cy="{cy}" r="10" fill="#F2C14E" stroke="#8A6A2A" stroke-width="2"/>'
    s += lbl(cx - r * 0.85, cy - 120, 330, 170, 'роговица')
    s += lbl(cx - r * 0.66, cy - r * 0.45, 330, 110, 'радужка, зрачок')
    s += lbl(cx - r * 0.55, cy + 60, 330, 640, 'хрусталик (аккомодация)')
    s += lbl(cx, cy + 120, 560, 670, 'стекловидное тело')
    s += lbl(cx + 150, cy - 160, 890, 110, 'склера (наружная)', '#8A7350')
    s += lbl(cx + 200, cy - 80, 890, 170, 'сетчатка: палочки и колбочки', '#B85C4E')
    s += lbl(cx + r - 14, cy, 960, 290, 'жёлтое пятно', '#8A6A2A')
    s += lbl(cx + r + 40, cy + 40, 960, 440, 'слепое пятно, зрительный нерв')
    # врезки
    for k, (title, fx, lens, fix) in enumerate((('близорукость', -60, 'двояковогнутая', 'рассеивающая'), ('дальнозоркость', 50, 'двояковыпуклая', 'собирающая'))):
        bx, by = 1560, 230 + k * 260
        s += f'<rect x="{bx - 160}" y="{by - 120}" width="330" height="230" rx="16" fill="{PAPER}"/>'
        s += text(bx, by - 85, title, 't', 'middle', RED)
        s += eye(bx + 20, by, 70, small=True)
        fpx = bx + 20 + 70 + fx * 0.6 - 4
        for y0 in (-30, 30):
            s += f'<path d="M{bx - 150} {by + y0} L {bx - 18} {by + y0 * 0.6} L {fpx} {by}" fill="none" stroke="{RED}" stroke-width="2"/>'
        s += f'<circle cx="{fpx}" cy="{by}" r="5" fill="{RED}"/>'
        s += text(bx, by + 95, f'очки: {lens} ({fix})', 'cap', 'middle')
    return s + '</g>'


# 9. Ухо ----------------------------------------------------------------------------------------
def ear_pathway() -> str:
    s = text(870, 50, 'Ухо: путь звука и равновесие', 'h', 'middle') + '<g transform="translate(140 0)">'
    s += f'<path d="{smooth([(150, 200), (230, 150), (280, 230), (250, 330), (200, 420), (150, 400), (170, 300)], True)}" fill="{SKIN}" stroke="#B85C4E" stroke-width="4"/>'
    s += f'<rect x="250" y="290" width="270" height="50" fill="#F8E6DE" stroke="#B85C4E" stroke-width="3"/>'
    s += f'<path d="M525 270 Q 545 315 525 360" fill="none" stroke="{INK}" stroke-width="8"/>'
    s += f'<rect x="530" y="220" width="250" height="200" rx="20" fill="#EEF3F8" stroke="{GREY}" stroke-width="3"/>'
    s += f'<path d="M540 300 L 600 270 L 640 300 L 690 290 L 740 300" fill="none" stroke="#8A7350" stroke-width="10" stroke-linejoin="round"/>'
    for x, y in ((600, 270), (640, 300), (690, 290)):
        s += f'<circle cx="{x}" cy="{y}" r="12" fill="#F4EBDD" stroke="#8A7350" stroke-width="3"/>'
    s += f'<ellipse cx="760" cy="300" rx="10" ry="24" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M660 420 Q 700 520 820 560" fill="none" stroke="{GREY}" stroke-width="16"/>'
    # улитка и каналы
    pts = [(900 + (60 - k * 2.3) * math.cos(k * 0.35), 330 + (60 - k * 2.3) * math.sin(k * 0.35)) for k in range(26)]
    s += f'<path d="M770 300 Q 820 330 {pts[0][0]:.0f} {pts[0][1]:.0f} ' + ' '.join(f'L {x:.0f} {y:.0f}' for x, y in pts) + '" fill="none" stroke="#C9A54A" stroke-width="16" stroke-linecap="round"/>'
    for k, (dx, dy, rr) in enumerate(((880, 190, 45), (930, 210, 40), (840, 230, 38))):
        s += f'<circle cx="{dx}" cy="{dy}" r="{rr}" fill="none" stroke="{BLUE}" stroke-width="8"/>'
    s += lbl(170, 230, 120, 120, 'ушная раковина')
    s += lbl(380, 315, 330, 450, 'слуховой проход')
    s += lbl(528, 300, 460, 140, 'барабанная перепонка')
    s += lbl(600, 270, 640, 105, 'молоточек → наковальня → стремечко', '#8A7350')
    s += lbl(760, 285, 760, 470, 'овальное окно')
    s += lbl(760, 540, 560, 620, 'слуховая труба → носоглотка', GREY)
    s += lbl(905, 330, 1120, 390, 'улитка: волосковые клетки', '#8A6A2A')
    s += lbl(930, 175, 1080, 185, 'полукружные каналы — равновесие', BLUE)
    s += '</g>' + text(870, 690, 'Звук → проход → перепонка → косточки → овальное окно → жидкость улитки → волосковые клетки → нерв → височная доля', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'nervous-system-types.png': (nervous_system_types(), 1600, 560),
        'neuron.png': (neuron(), 1650, 510),
        'synapse.png': (synapse(), 1800, 720),
        'spinal-cord.png': (spinal_cord(), 1700, 720),
        'reflex-arc.png': (reflex_arc(), 1520, 720),
        'brain-cortex.png': (brain_cortex(), 2140, 680),
        'autonomic-effects.png': (autonomic_effects(), 1450, 720),
        'eye-optics.png': (eye_optics(), 1900, 720),
        'ear-pathway.png': (ear_pathway(), 1740, 720),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
