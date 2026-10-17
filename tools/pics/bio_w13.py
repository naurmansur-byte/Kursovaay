"""Рисунки недели 13 биологии (course/biology/week-13/pics/*.png): бесполое размножение, вегетативное размножение,
строение цветка, двойное оплодотворение, циклы мха и папоротника, эмбриогенез, превращение насекомых.

Факты — по выжимке course/textbooks/bio-13-reproduction.md (Б7а § 52–58; Б8 § 46–49; Б10-2 § 62–63). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w13.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, LIGHT_GREEN, LIGHT_YELLOW, PAPER, RED, ROOT, arrow, chem, label, render, text

OUT = ROOT / 'course' / 'biology' / 'week-13' / 'pics'
HAP, DIP, TRI = '#3A57A7', '#D98A2B', '#8E44AD'          # n, 2n, 3n
ECTO, MESO, ENDO = '#4A6FC7', '#E0656B', '#E8B33A'        # зародышевые листки
SOIL, BROWN, PINK, LEAF = '#EFE3D0', '#8A5A2B', '#F2A7B5', '#5DAA6F'
CELL = '#FBF6EE'


def panel(x, y, w, h, title, sub=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{PAPER}"/>' + text(x + w / 2, y + 44, title, 't', 'middle')
    if sub:
        s += text(x + w / 2, y + 78, sub, 'cap', 'middle')
    return s


def lines_at(x, y, rows, cls='s', anchor='middle', step=30, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def chip(x, y, s, color):
    w = 22 + 16 * len(s)
    return (f'<rect x="{x - w / 2:.0f}" y="{y - 24:.0f}" width="{w:.0f}" height="34" rx="17" fill="{color}"/>'
            + text(x, y, s, 's', 'middle', '#fff'))


def tag(x, y, s, color=RED):
    w = 26 + 14.5 * len(s)
    return (f'<rect x="{x - w / 2:.0f}" y="{y - 26:.0f}" width="{w:.0f}" height="38" rx="8" fill="{color}"/>'
            + text(x, y, s, 's', 'middle', '#fff'))


def leaf(x, y, L, ang, color=LEAF, w=0.32):
    """Лист-эллипс от точки (x, y) под углом ang (градусы, 0 — вправо)."""
    cx, cy = x + L / 2 * math.cos(math.radians(ang)), y - L / 2 * math.sin(math.radians(ang))
    return (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{L / 2:.0f}" ry="{L * w / 2:.0f}" fill="{color}" stroke="#1F5E36" '
            f'stroke-width="2.5" transform="rotate({-ang} {cx:.0f} {cy:.0f})"/>')


def soil(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{SOIL}"/>'
            f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="{BROWN}" stroke-width="4"/>')


def roots(x, y, n=4, L=46, spread=60):
    return ''.join(f'<path d="M{x} {y} q {(-spread / 2 + k * spread / max(n - 1, 1)) * 0.3:.0f} {L * 0.5:.0f} '
                   f'{-spread / 2 + k * spread / max(n - 1, 1):.0f} {L:.0f}" fill="none" stroke="{BROWN}" stroke-width="3"/>'
                   for k in range(n))


# 1. Бесполое размножение ----------------------------------------------------------------------
def hydra(cx, base, h, w):
    top = base - h
    s = f'<rect x="{cx - w / 2:.0f}" y="{top:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{w / 2:.0f}" fill="#CFE6D6" stroke="{GREEN}" stroke-width="4"/>'
    for k, dx in enumerate((-1.6, -0.8, 0.8, 1.6)):
        s += (f'<path d="M{cx + dx * w * 0.2:.0f} {top + 6:.0f} q {dx * w * 0.5:.0f} {-h * 0.25:.0f} {dx * w * 0.9:.0f} {-h * 0.18 * (1 + k % 2 * 0.4):.0f}" '
              f'fill="none" stroke="{GREEN}" stroke-width="{max(3, w / 12):.0f}" stroke-linecap="round"/>')
    return s


def star(cx, cy, R, r, rays=5, rot=-90, fill='#F4B183', stroke=BROWN, skip=()):
    pts = []
    for k in range(rays * 2):
        if k // 2 in skip and k % 2 == 0:
            rr = r
        else:
            rr = R if k % 2 == 0 else r
        a = math.radians(rot + k * 180 / rays)
        pts.append(f'{cx + rr * math.cos(a):.0f},{cy + rr * math.sin(a):.0f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="4" stroke-linejoin="round"/>'


def asexual() -> str:
    s = text(870, 52, 'Бесполое размножение: одна родительская особь, без гамет', 'h', 'middle')
    # деление
    x, y = 30, 90
    s += panel(x, y, 540, 500, 'Деление (митоз)', 'амёба, эвглена, хламидомонада')
    s += f'<ellipse cx="{x + 140}" cy="{y + 290}" rx="85" ry="68" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4"/>'
    s += f'<circle cx="{x + 140}" cy="{y + 290}" r="24" fill="#B9DCC4" stroke="{GREEN}" stroke-width="3"/>'
    s += arrow(x + 245, y + 290, x + 320, y + 290, GREY, 4)
    for yy in (y + 210, y + 370):
        s += f'<ellipse cx="{x + 420}" cy="{yy}" rx="62" ry="50" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4"/>'
        s += f'<circle cx="{x + 420}" cy="{yy}" r="18" fill="#B9DCC4" stroke="{GREEN}" stroke-width="3"/>'
    s += text(x + 270, y + 470, '1 клетка → 2 одинаковые клетки', 's', 'middle')
    # почкование
    x = 600
    s += panel(x, y, 540, 500, 'Почкование', 'гидра, губки')
    s += hydra(x + 160, y + 430, 230, 64)
    s += f'<g transform="rotate(58 {x + 192} {y + 320})">' + hydra(x + 192, y + 320, 100, 34) + '</g>'
    s += label(x + 262, y + 270, x + 330, y + 170, 'почка', 's')
    s += arrow(x + 300, y + 330, x + 380, y + 330, GREY, 4)
    s += hydra(x + 440, y + 430, 130, 40)
    s += text(x + 440, y + 470, 'отделилась', 's', 'middle')
    # фрагментация
    x = 1170
    s += panel(x, y, 540, 500, 'Фрагментация', 'морская звезда, плоские черви')
    s += star(x + 150, y + 290, 105, 40)
    s += arrow(x + 270, y + 290, x + 330, y + 290, GREY, 4)
    # отделившийся луч, на котором отрастают новые
    s += f'<g transform="rotate(20 {x + 430} {y + 290})">'
    s += f'<polygon points="{x + 430},{y + 170} {x + 452},{y + 300} {x + 408},{y + 300}" fill="#F4B183" stroke="{BROWN}" stroke-width="4" stroke-linejoin="round"/>'
    for dx, dy, a in ((-30, 300, 200), (30, 300, -20), (-14, 330, 240), (14, 330, -60)):
        s += (f'<line x1="{x + 430}" y1="{y + 305}" x2="{x + 430 + 36 * math.cos(math.radians(a)):.0f}" '
              f'y2="{y + 305 - 36 * math.sin(math.radians(a)):.0f}" stroke="#F4B183" stroke-width="12" stroke-linecap="round"/>')
    s += '</g>'
    s += text(x + 270, y + 440, 'из части тела', 's', 'middle') + text(x + 270, y + 470, 'восстанавливается целая особь', 's', 'middle')
    s += text(870, 640, 'Потомки — копии родителя (клоны); изменчивость понижена.', 's', 'middle', GREEN)
    return s


# 2. Вегетативное размножение ------------------------------------------------------------------
def rosette(x, y, size):
    return ''.join(leaf(x, y, size, a) for a in (30, 70, 110, 150))


def shoot(x, y, h):
    s = f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - h}" stroke="#1F5E36" stroke-width="4"/>'
    for k in range(3):
        yy = y - h * (0.35 + 0.25 * k)
        s += leaf(x, yy, 46 - k * 8, 35) + leaf(x, yy, 46 - k * 8, 145)
    return s


def vegetative() -> str:
    s = text(900, 52, 'Вегетативное размножение растений: потомки — клоны', 'h', 'middle')
    W, H, G = 420, 430, 22
    cells = [(30 + i * (W + G), 90 + j * (H + 20)) for j in range(2) for i in range(4)]
    # корневище
    x, y = cells[0]
    s += panel(x, y, W, H, 'Корневище', 'пырей') + soil(x + 20, y + 250, W - 40, 150)
    s += f'<path d="M{x + 40} {y + 300} C {x + 140} {y + 280}, {x + 260} {y + 330}, {x + 380} {y + 300}" fill="none" stroke="{BROWN}" stroke-width="16" stroke-linecap="round"/>'
    for xx in (x + 110, x + 220, x + 330):
        s += shoot(xx, y + 300, 170) + roots(xx, y + 308, 3, 40, 40)
    s += text(x + W / 2, y + 410, 'подземный побег с почками', 's', 'middle')
    # клубень
    x, y = cells[1]
    s += panel(x, y, W, H, 'Клубень', 'картофель') + soil(x + 20, y + 230, W - 40, 170)
    s += f'<ellipse cx="{x + 210}" cy="{y + 320}" rx="100" ry="62" fill="#D9B57E" stroke="{BROWN}" stroke-width="4"/>'
    for ex, ey in ((x + 150, y + 300), (x + 230, y + 290), (x + 270, y + 340), (x + 180, y + 350)):
        s += f'<path d="M{ex - 9} {ey} q 9 -9 18 0" fill="none" stroke="{BROWN}" stroke-width="4"/>'
    s += shoot(x + 230, y + 288, 150)
    s += label(x + 270, y + 340, x + 300, y + 405, 'глазок', 's')
    # луковица
    x, y = cells[2]
    s += panel(x, y, W, H, 'Луковица', 'лук') + soil(x + 20, y + 250, W - 40, 150)
    cx, by = x + 190, y + 385
    s += f'<path d="M{cx - 80} {by} C {cx - 110} {by - 70}, {cx - 40} {by - 120}, {cx} {by - 170} C {cx + 40} {by - 120}, {cx + 110} {by - 70}, {cx + 80} {by} Z" fill="#F1D9C0" stroke="{BROWN}" stroke-width="4"/>'
    for k in (1, 2):
        f = 1 - 0.3 * k
        s += f'<path d="M{cx - 80 * f:.0f} {by} C {cx - 110 * f:.0f} {by - 70 * f:.0f}, {cx - 40 * f:.0f} {by - 120 * f:.0f}, {cx} {by - 170 * f:.0f}" fill="none" stroke="{BROWN}" stroke-width="2.5"/>'
    s += f'<rect x="{cx - 70}" y="{by - 6}" width="140" height="14" rx="5" fill="{BROWN}"/>' + roots(cx, by + 8, 5, 30, 110)
    for a in (80, 95, 110):
        s += f'<line x1="{cx}" y1="{by - 170}" x2="{cx + 100 * math.cos(math.radians(a)):.0f}" y2="{by - 170 - 100 * math.sin(math.radians(a)):.0f}" stroke="{LEAF}" stroke-width="10" stroke-linecap="round"/>'
    s += label(cx + 60, by - 60, x + 290, y + 250, 'сочные', 's') + text(x + 298, y + 280, 'чешуи', 's') + label(cx + 70, by, x + 290, by + 34, 'донце', 's')
    # ус
    x, y = cells[3]
    s += panel(x, y, W, H, 'Ус (столон)', 'земляника') + soil(x + 20, y + 290, W - 40, 110)
    s += rosette(x + 100, y + 290, 110) + roots(x + 100, y + 296, 4, 40, 50)
    s += f'<path d="M{x + 120} {y + 280} C {x + 200} {y + 170}, {x + 280} {y + 190}, {x + 320} {y + 286}" fill="none" stroke="#1F5E36" stroke-width="5"/>'
    s += rosette(x + 320, y + 290, 70) + roots(x + 320, y + 296, 3, 32, 36)
    s += text(x + W / 2, y + 400, 'дочерняя розетка укореняется', 's', 'middle')
    # черенок
    x, y = cells[4]
    s += panel(x, y, W, H, 'Стеблевой черенок', 'смородина, тополь, ива') + soil(x + 20, y + 280, W - 40, 120)
    s += f'<line x1="{x + 170}" y1="{y + 340}" x2="{x + 250}" y2="{y + 130}" stroke="{BROWN}" stroke-width="16" stroke-linecap="round"/>'
    for t in (0.35, 0.6, 0.85):
        bx, byy = x + 170 + 80 * t, y + 340 - 210 * t
        s += f'<polygon points="{bx + 6:.0f},{byy:.0f} {bx + 30:.0f},{byy - 12:.0f} {bx + 8:.0f},{byy - 22:.0f}" fill="{LEAF}" stroke="#1F5E36" stroke-width="2"/>'
    s += roots(x + 172, y + 338, 5, 44, 90)
    s += label(x + 230, y + 185, x + 310, y + 160, 'почки', 's') + text(x + W / 2, y + 410, 'укореняется в почве', 's', 'middle')
    # отводок
    x, y = cells[5]
    s += panel(x, y, W, H, 'Отводок', 'смородина') + soil(x + 20, y + 280, W - 40, 120)
    s += f'<path d="M{x + 220} {y + 270} q 70 30 140 10" fill="{SOIL}" stroke="{BROWN}" stroke-width="3"/>'
    for dx in (-30, 0, 30):
        s += f'<line x1="{x + 100}" y1="{y + 282}" x2="{x + 100 + dx * 1.6:.0f}" y2="{y + 120}" stroke="{BROWN}" stroke-width="9" stroke-linecap="round"/>'
    s += f'<path d="M{x + 104} {y + 200} C {x + 170} {y + 160}, {x + 230} {y + 280}, {x + 290} {y + 300} C {x + 320} {y + 290}, {x + 330} {y + 220}, {x + 340} {y + 170}" fill="none" stroke="{BROWN}" stroke-width="9" stroke-linecap="round"/>'
    s += leaf(x + 340, y + 175, 46, 60) + leaf(x + 340, y + 175, 46, 120) + roots(x + 290, y + 306, 4, 40, 60)
    s += text(x + W / 2, y + 380, 'ветвь пригнута и присыпана;', 's', 'middle') + text(x + W / 2, y + 410, 'отделяют после укоренения', 's', 'middle')
    # прививка
    x, y = cells[6]
    s += panel(x, y, W, H, 'Прививка', 'черенком или глазком') + soil(x + 20, y + 330, W - 40, 70)
    cx = x + 110
    s += f'<rect x="{cx - 18}" y="{y + 210}" width="36" height="122" fill="#B07A45" stroke="{BROWN}" stroke-width="3"/>' + roots(cx, y + 336, 5, 40, 90)
    s += f'<rect x="{cx - 14}" y="{y + 110}" width="28" height="104" fill="#9C8F4B" stroke="{BROWN}" stroke-width="3"/>'
    s += f'<rect x="{cx - 24}" y="{y + 198}" width="48" height="26" rx="4" fill="{DIP}" opacity=".85"/>'
    s += leaf(cx, y + 130, 50, 40) + leaf(cx, y + 150, 50, 140)
    s += label(cx + 16, y + 150, x + 190, y + 140, 'привой —', 's') + text(x + 198, y + 168, 'что прививают', 's')
    s += label(cx + 20, y + 280, x + 190, y + 270, 'подвой —', 's') + text(x + 198, y + 298, 'на что прививают', 's')
    s += label(cx + 26, y + 211, x + 190, y + 216, 'срастание', 's', DIP)
    # итог
    x, y = cells[7]
    s += f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="18" fill="{LIGHT_GREEN}"/>'
    s += text(x + W / 2, y + 60, 'Итог', 't', 'middle')
    s += lines_at(x + W / 2, y + 120, ['Потомки — клоны:', 'генотип как у', 'материнской особи.'], 's')
    s += lines_at(x + W / 2, y + 260, ['При прививке клетки', 'привоя и подвоя', 'остаются своими —', 'геномы не сливаются.'], 's', color=GREEN)
    return s


# 3. Строение цветка ---------------------------------------------------------------------------
def flower() -> str:
    s = text(840, 52, 'Строение цветка', 'h', 'middle')
    cx = 750
    s += f'<line x1="{cx}" y1="{660}" x2="{cx}" y2="{860}" stroke="#1F5E36" stroke-width="16"/>'
    for sgn in (-1, 1):  # чашелистики
        s += (f'<path d="M{cx + sgn * 40} 650 C {cx + sgn * 120} 640, {cx + sgn * 200} 660, {cx + sgn * 230} 600 '
              f'C {cx + sgn * 180} 690, {cx + sgn * 90} 700, {cx + sgn * 30} 680 Z" fill="{LEAF}" stroke="#1F5E36" stroke-width="3"/>')
    for sgn in (-1, 1):  # лепестки
        s += (f'<path d="M{cx + sgn * 50} 640 C {cx + sgn * 160} 600, {cx + sgn * 320} 420, {cx + sgn * 250} 300 '
              f'C {cx + sgn * 200} 360, {cx + sgn * 120} 480, {cx + sgn * 40} 610 Z" fill="{PINK}" stroke="#B5546A" stroke-width="3"/>')
    s += f'<ellipse cx="{cx}" cy="655" rx="95" ry="30" fill="#7FB98C" stroke="#1F5E36" stroke-width="3"/>'  # цветоложе
    for sgn in (-1, 1):  # тычинки
        s += f'<path d="M{cx + sgn * 70} 630 C {cx + sgn * 100} 520, {cx + sgn * 140} 440, {cx + sgn * 150} 370" fill="none" stroke="#C9A227" stroke-width="6"/>'
        s += f'<ellipse cx="{cx + sgn * 152}" cy="345" rx="22" ry="36" fill="#F2C94C" stroke="#A07D14" stroke-width="3"/>'
    s += f'<ellipse cx="{cx}" cy="560" rx="70" ry="82" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4"/>'  # завязь
    for oy in (520, 565, 610):
        s += f'<ellipse cx="{cx}" cy="{oy}" rx="16" ry="12" fill="#F7EFC8" stroke="{DIP}" stroke-width="3"/>'
    s += f'<rect x="{cx - 10}" y="330" width="20" height="152" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4"/>'  # столбик
    s += f'<ellipse cx="{cx}" cy="322" rx="44" ry="17" fill="#A9D18E" stroke="{GREEN}" stroke-width="4"/>'  # рыльце
    # подписи слева
    s += label(cx - 165, 345, 330, 250, 'пыльник', 't') + label(cx - 108, 500, 330, 420, 'тычиночная нить', 't')
    s += label(cx - 230, 420, 330, 340, 'лепесток', 't') + label(cx - 190, 645, 330, 610, 'чашелистик', 't')
    s += label(cx - 80, 660, 330, 700, 'цветоложе', 't') + label(cx, 760, 330, 800, 'цветоножка', 't')
    s += text(60, 150, 'тычинка = пыльник + нить', 't', 'start', '#A07D14')
    # подписи справа
    s += label(cx + 40, 318, 1150, 240, 'рыльце', 't') + label(cx + 10, 410, 1150, 330, 'столбик', 't')
    s += label(cx + 66, 560, 1150, 470, 'завязь', 't') + label(cx + 14, 610, 1150, 560, 'семязачаток', 't')
    s += text(1630, 150, 'пестик = рыльце + столбик + завязь', 't', 'end', GREEN)
    s += text(840, 900, 'После оплодотворения: семязачаток → семя (кожура — из его оболочек), стенка завязи → околоплодник', 's', 'middle')
    return s


# 4. Двойное оплодотворение --------------------------------------------------------------------
def dot(x, y, r, color, lbl=None):
    s = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{color}" opacity=".9"/>'
    if lbl:
        s += text(x, y + 9, lbl, 's', 'middle', '#fff')
    return s


def double_fertilization() -> str:
    s = text(1000, 52, 'Двойное оплодотворение у цветковых', 'h', 'middle')
    # пыльцевое зерно
    s += panel(30, 90, 520, 790, 'Пыльцевое зерно', 'мужской гаметофит')
    s += f'<circle cx="290" cy="340" r="160" fill="#F7EFC8" stroke="#A07D14" stroke-width="6"/>'
    s += f'<circle cx="225" cy="290" r="44" fill="#FCE9B0" stroke="{HAP}" stroke-width="4" stroke-dasharray="8 6"/>' + text(225, 299, 'n', 't', 'middle', HAP)
    s += text(225, 368, 'вегетативная', 'cap', 'middle')
    s += f'<ellipse cx="355" cy="395" rx="44" ry="28" fill="#DCE6F7" stroke="{HAP}" stroke-width="4"/>' + text(355, 404, 'n', 't', 'middle', HAP)
    s += text(320, 456, 'генеративная', 'cap', 'middle')
    s += lines_at(290, 530, ['вегетативная клетка (n)', '→ пыльцевая трубка'], 's')
    s += lines_at(290, 600, ['генеративная клетка (n)', '→ делится → 2 спермия (n)'], 's')
    s += dot(230, 720, 22, HAP, 'n') + dot(350, 720, 22, HAP, 'n')
    s += text(290, 790, 'обе клетки гаплоидны', 's', 'middle', HAP)
    # пестик и семязачаток
    cx = 1150
    s += panel(560, 90, 840, 790, 'Пестик и семязачаток')
    s += f'<ellipse cx="{cx}" cy="195" rx="70" ry="22" fill="#A9D18E" stroke="{GREEN}" stroke-width="4"/>'
    s += f'<circle cx="{cx - 30}" cy="172" r="22" fill="#F7EFC8" stroke="#A07D14" stroke-width="4"/>'
    s += f'<path d="M{cx - 18} 210 L{cx - 18} 330 Q{cx - 230} 380 {cx - 230} 590 Q{cx - 230} 840 {cx} 840 Q{cx + 230} 840 {cx + 230} 590 Q{cx + 230} 380 {cx + 18} 330 L{cx + 18} 210" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4"/>'
    oy = 610
    s += f'<ellipse cx="{cx}" cy="{oy}" rx="150" ry="190" fill="#F3E3C8" stroke="{DIP}" stroke-width="5"/>'
    s += f'<ellipse cx="{cx}" cy="{oy}" rx="122" ry="162" fill="none" stroke="{DIP}" stroke-width="3" stroke-dasharray="10 6"/>'
    s += f'<ellipse cx="{cx}" cy="{oy + 10}" rx="82" ry="128" fill="{CELL}" stroke="{GREY}" stroke-width="3"/>'  # зародышевый мешок
    s += f'<rect x="{cx - 16}" y="{oy - 196}" width="32" height="40" fill="{LIGHT_GREEN}"/>'  # микропиле
    s += f'<path d="M{cx - 30} 185 C {cx - 20} 260, {cx} 300, {cx} {oy - 120}" fill="none" stroke="{DIP}" stroke-width="7" stroke-linecap="round"/>'
    s += dot(cx - 14, oy - 140, 11, HAP) + dot(cx + 12, oy - 132, 11, HAP)
    s += dot(cx, oy - 70, 26, HAP, 'n')                       # яйцеклетка у микропиле
    s += dot(cx, oy + 40, 32, DIP, '2n')                      # центральная клетка
    s += label(cx - 14, 300, 900, 250, 'пыльцевая трубка', 's')
    s += label(cx - 226, 520, 900, 370, 'стенка завязи', 's')
    s += label(cx - 22, oy - 72, 900, 480, 'яйцеклетка (n)', 's')
    s += label(cx - 148, oy + 40, 900, 600, 'оболочки семязачатка', 's')
    s += label(cx - 30, oy + 40, 900, 720, 'центральная клетка 2n', 's')
    # итог
    s += panel(1430, 90, 540, 790, 'Два слияния', 'открыл С. Г. Навашин, 1898')
    y1, X = 230, 190
    s += dot(1320 + X, y1, 26, HAP, 'n') + text(1360 + X, y1 + 9, '+', 't', 'middle') + dot(1400 + X, y1, 26, HAP, 'n')
    s += arrow(1440 + X, y1, 1510 + X, y1, GREY, 4) + dot(1560 + X, y1, 32, DIP, '2n')
    s += lines_at(1510 + X, y1 + 70, ['спермий + яйцеклетка', '→ зигота → зародыш'], 's')
    y2 = 440
    s += dot(1320 + X, y2, 26, HAP, 'n') + text(1360 + X, y2 + 9, '+', 't', 'middle') + dot(1410 + X, y2, 32, DIP, '2n')
    s += arrow(1455 + X, y2, 1515 + X, y2, GREY, 4) + dot(1570 + X, y2, 38, TRI, '3n')
    s += lines_at(1510 + X, y2 + 76, ['спермий + центральная клетка', '→ эндосперм — запас питания'], 's')
    s += f'<rect x="{1280 + X}" y="620" width="460" height="230" rx="14" fill="#fff"/>'
    s += lines_at(1510 + X, 662, ['Пример: 2n = 20', '10 + 10 = 20 — зигота', '10 + 20 = 30 — эндосперм', 'кожура и околоплодник — 20'], 's', step=44)
    return s


# 5–6. Жизненные циклы -------------------------------------------------------------------------
def moss_shoot(x, y, h=150):
    s = f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - h}" stroke="#1F5E36" stroke-width="5"/>'
    for k in range(7):
        yy = y - 12 - k * (h - 20) / 7
        s += leaf(x, yy, 30 - k * 2, 40, w=0.4) + leaf(x, yy, 30 - k * 2, 140, w=0.4)
    return s + roots(x, y, 3, 22, 30)


def capsule(x, y, h=120):
    return (f'<path d="M{x} {y} C {x + 6} {y - h * 0.5}, {x - 6} {y - h * 0.8}, {x + 4} {y - h}" fill="none" stroke="{BROWN}" stroke-width="4"/>'
            f'<ellipse cx="{x + 10}" cy="{y - h - 16}" rx="15" ry="26" fill="{DIP}" stroke="{BROWN}" stroke-width="3" transform="rotate(20 {x + 10} {y - h - 16})"/>')


def spores(x, y, color=HAP):
    return ''.join(f'<circle cx="{x + dx}" cy="{y + dy}" r="9" fill="{color}"/>' for dx, dy in ((-30, 0), (0, -18), (28, 4), (-8, 22), (22, 30)))


def gametes(x, y):
    s = f'<circle cx="{x - 30}" cy="{y}" r="30" fill="#DCE6F7" stroke="{HAP}" stroke-width="4"/>'
    for k in range(3):
        sx, sy = x + 30 + k * 18, y - 30 + k * 26
        s += f'<ellipse cx="{sx}" cy="{sy}" rx="8" ry="6" fill="{HAP}"/><path d="M{sx + 6} {sy} q 12 -8 22 2" fill="none" stroke="{HAP}" stroke-width="2.5"/>'
    return s


def zygote(x, y):
    return f'<circle cx="{x}" cy="{y}" r="34" fill="#F8E2C4" stroke="{DIP}" stroke-width="5"/><circle cx="{x}" cy="{y}" r="11" fill="{DIP}"/>'


def protonema(x, y):
    s = f'<path d="M{x - 70} {y} q 35 -18 70 0 t 70 0" fill="none" stroke="{LEAF}" stroke-width="8" stroke-linecap="round"/>'
    for dx in (-40, 10, 50):
        s += f'<path d="M{x + dx} {y - 4} q 6 -24 22 -34" fill="none" stroke="{LEAF}" stroke-width="6" stroke-linecap="round"/>'
    return s + moss_shoot(x + 50, y - 34, 50)


def frond(x, y, h=220):
    s = f'<path d="M{x} {y} C {x + 10} {y - h * 0.5}, {x + 40} {y - h * 0.85}, {x + 70} {y - h}" fill="none" stroke="#1F5E36" stroke-width="5"/>'
    for k in range(8):
        t = 0.15 + k * 0.1
        px, py = x + 70 * t ** 1.6, y - h * t
        L = 70 * (1 - t * 0.7)
        s += leaf(px, py, L, 160, w=0.28) + leaf(px, py, L, 20, w=0.28)
    return s + roots(x, y + 4, 4, 30, 50)


def sorus_leaf(x, y):
    s = f'<path d="M{x - 90} {y} C {x - 40} {y - 60}, {x + 40} {y - 60}, {x + 90} {y} C {x + 40} {y + 50}, {x - 40} {y + 50}, {x - 90} {y} Z" fill="{LEAF}" stroke="#1F5E36" stroke-width="3"/>'
    s += f'<line x1="{x - 90}" y1="{y}" x2="{x + 90}" y2="{y}" stroke="#1F5E36" stroke-width="3"/>'
    return s + ''.join(f'<circle cx="{x + dx}" cy="{y + dy}" r="9" fill="{BROWN}"/>' for dx in (-50, -15, 20, 55) for dy in (-18, 18))


def prothallus(x, y):
    s = (f'<path d="M{x} {y + 40} C {x - 70} {y}, {x - 70} {y - 50}, {x - 30} {y - 50} C {x - 10} {y - 50}, {x} {y - 30}, {x} {y - 20} '
         f'C {x} {y - 30}, {x + 10} {y - 50}, {x + 30} {y - 50} C {x + 70} {y - 50}, {x + 70} {y}, {x} {y + 40} Z" fill="{LEAF}" stroke="#1F5E36" stroke-width="3"/>')
    return s + roots(x, y + 36, 4, 26, 40)


def cycle(title, center, nodes, edges, W, H) -> str:
    s = text(W / 2, 52, title, 'h', 'middle')
    s += f'<ellipse cx="{W / 2}" cy="{H / 2 + 30}" rx="{W * 0.36:.0f}" ry="{H * 0.3:.0f}" fill="none" stroke="#E6E1D6" stroke-width="40"/>'
    s += lines_at(W / 2, H / 2 + 10, center, 't', step=40)
    for (x, y), icon, rows, ploidy in nodes:
        s += icon(x, y) + lines_at(x, y + 80, rows, 's') + chip(x, y + 80 + 30 * len(rows) + 6, ploidy, HAP if ploidy == 'n' else DIP)
    for (x1, y1, x2, y2), word, hot in edges:
        s += arrow(x1, y1, x2, y2, RED if hot else GREY, 6 if hot else 4)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if abs(x2 - x1) < abs(y2 - y1):
            side = 1 if mx < W / 2 else -1
            s += text(mx + side * 18, my + 8, word, 'cap', 'start' if side > 0 else 'end')
        elif hot:
            s += tag(mx, my - 14 if my < H / 2 else my - 50, word)
        else:
            s += text(mx, my - 18, word, 'cap', 'middle')
    return s


def moss_cycle() -> str:
    W, H = 1700, 1000
    nodes = [
        ((300, 330), lambda x, y: moss_shoot(x, y + 40, 150), ['зелёный мох —', 'гаметофит'], 'n'),
        ((850, 220), gametes, ['гаметы (митозом):', 'сперматозоид и яйцеклетка'], 'n'),
        ((1400, 330), zygote, ['зигота', 'на женском растении'], '2n'),
        ((1400, 720), lambda x, y: moss_shoot(x - 20, y + 40, 90) + capsule(x - 20, y - 50, 70), ['коробочка на ножке —', 'спорофит на гаметофите'], '2n'),
        ((850, 800), spores, ['споры'], 'n'),
        ((300, 720), protonema, ['предросток', '(нитчатый)'], 'n'),
    ]
    edges = [((440, 300, 700, 230), 'митоз', False), ((1010, 230, 1320, 300), 'оплодотворение (вода)', True),
             ((1400, 498, 1400, 556), 'развитие', False), ((1225, 800, 945, 800), 'мейоз', True),
             ((760, 800, 430, 760), 'прорастание', False), ((300, 610, 300, 520), 'развитие', False)]
    return cycle('Жизненный цикл мха (кукушкин лён)', ['Преобладает', 'гаметофит (n)'], nodes, edges, W, H)


def fern_cycle() -> str:
    W, H = 1700, 1000
    nodes = [
        ((300, 330), lambda x, y: frond(x - 30, y + 30, 190), ['взрослый папоротник —', 'спорофит'], '2n'),
        ((850, 220), sorus_leaf, ['сорусы (спорангии)', 'на нижней стороне листа'], '2n'),
        ((1400, 330), spores, ['спора'], 'n'),
        ((1400, 720), prothallus, ['заросток ~1 мм —', 'гаметофит'], 'n'),
        ((850, 800), gametes, ['гаметы (митозом):', 'сперматозоид и яйцеклетка'], 'n'),
        ((300, 720), zygote, ['зигота →', 'молодой спорофит'], '2n'),
    ]
    edges = [((470, 300, 720, 230), 'на листьях', False), ((1000, 230, 1320, 300), 'мейоз', True),
             ((1400, 470, 1400, 620), 'прорастание', False), ((1235, 790, 1010, 800), 'митоз', False),
             ((770, 800, 352, 736), 'оплодотворение (вода)', True), ((300, 640, 300, 540), 'развитие', False)]
    return cycle('Жизненный цикл папоротника', ['Преобладает', 'спорофит (2n)'], nodes, edges, W, H)


# 7. Эмбриогенез -------------------------------------------------------------------------------
def arc(cx, cy, r, a1, a2, color, w):
    """Дуга окружности от угла a1 до a2 (градусы, по часовой от оси x, y вниз), большая дуга через верх."""
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
    return f'<path d="M{x1:.1f} {y1:.1f} A {r} {r} 0 1 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'


def embryogenesis() -> str:
    s = text(900, 52, 'Эмбриогенез животных: от зиготы до нейрулы', 'h', 'middle')
    xs = [150, 450, 750, 1050, 1350, 1650]
    y = 290
    for k in range(5):
        s += arrow(xs[k] + 95, y, xs[k + 1] - 95, y, GREY, 4)
    s += f'<circle cx="{xs[0]}" cy="{y}" r="72" fill="#F8E2C4" stroke="{DIP}" stroke-width="4"/><circle cx="{xs[0]}" cy="{y}" r="20" fill="{DIP}"/>'
    for dx, dy in ((-30, -30), (30, -30), (-30, 30), (30, 30), (0, -52), (0, 52), (-52, 0), (52, 0)):
        s += f'<circle cx="{xs[1] + dx}" cy="{y + dy}" r="26" fill="#F8E2C4" stroke="{DIP}" stroke-width="3"/>'
    s += f'<circle cx="{xs[2]}" cy="{y}" r="58" fill="#FFF8EC"/>'
    for k in range(22):
        a = 2 * math.pi * k / 22
        s += f'<circle cx="{xs[2] + 66 * math.cos(a):.0f}" cy="{y + 66 * math.sin(a):.0f}" r="11" fill="#F8E2C4" stroke="{DIP}" stroke-width="2.5"/>'
    s += label(xs[2], y, xs[2] + 20, y + 120, 'полость', 's')
    # ранняя гаструла: 2 листка
    s += arc(xs[3], y, 70, 115, 65, ECTO, 20) + arc(xs[3], y - 6, 40, 120, 60, ENDO, 18)
    s += label(xs[3], y + 60, xs[3] + 20, y + 140, 'первичный рот', 's')
    # поздняя гаструла: 3 листка
    s += arc(xs[4], y, 72, 115, 65, ECTO, 18) + arc(xs[4], y - 4, 54, 118, 62, MESO, 10) + arc(xs[4], y - 6, 36, 122, 58, ENDO, 16)
    # нейрула (поперечный срез)
    nx = xs[5]
    s += f'<circle cx="{nx}" cy="{y}" r="78" fill="#FFF8EC" stroke="{ECTO}" stroke-width="12"/>'
    s += f'<circle cx="{nx}" cy="{y - 42}" r="18" fill="#fff" stroke="{ECTO}" stroke-width="10"/>'
    s += f'<ellipse cx="{nx - 42}" cy="{y + 2}" rx="18" ry="30" fill="{MESO}" opacity=".85"/><ellipse cx="{nx + 42}" cy="{y + 2}" rx="18" ry="30" fill="{MESO}" opacity=".85"/>'
    s += f'<circle cx="{nx}" cy="{y + 30}" r="20" fill="#fff" stroke="{ENDO}" stroke-width="10"/>'
    s += label(nx - 12, y - 52, nx - 60, y - 128, 'нервная трубка', 's')
    names = [('Зигота', ['2n']), ('Дробление', ['митозы, клетки', 'не растут']), ('Бластула', ['один слой', 'клеток']),
             ('Ранняя гаструла', ['2 листка']), ('Поздняя гаструла', ['3 листка']), ('Нейрула', ['только', 'у хордовых'])]
    for x, (n, sub) in zip(xs, names):
        s += text(x, y + 190, n, 't', 'middle') + lines_at(x, y + 226, sub, 'cap', step=28)
    # листки
    ly = 640
    for k, (c, n, what) in enumerate(((ECTO, 'эктодерма', 'кожа, волосы, ногти, нервная система, органы чувств'),
                                      (MESO, 'мезодерма', 'мышцы, кости, хрящи, сердце, сосуды, кровь'),
                                      (ENDO, 'энтодерма', 'пищеварительная система, печень, лёгкие'))):
        yy = ly + k * 46
        s += f'<rect x="230" y="{yy - 26}" width="34" height="34" rx="6" fill="{c}"/>' + text(282, yy, n, 't') + text(520, yy, '→ ' + what, 's')
    return s


# 8. Превращение насекомых ---------------------------------------------------------------------
def eggs(x, y):
    return ''.join(f'<ellipse cx="{x + dx}" cy="{y + dy}" rx="14" ry="20" fill="#FFF3C4" stroke="#A07D14" stroke-width="3"/>'
                   for dx, dy in ((-34, 6), (-10, -8), (14, 6), (38, -6), (2, 26)))


def caterpillar(x, y):
    s = ''.join(f'<circle cx="{x - 66 + k * 22}" cy="{y + 6 * math.sin(k)}" r="18" fill="#9CCB6B" stroke="#4E7A2B" stroke-width="3"/>' for k in range(7))
    return s + f'<circle cx="{x + 92}" cy="{y - 6}" r="20" fill="#7FB04F" stroke="#4E7A2B" stroke-width="3"/>'


def pupa(x, y):
    return (f'<path d="M{x} {y - 70} C {x + 40} {y - 50}, {x + 40} {y + 40}, {x} {y + 74} C {x - 40} {y + 40}, {x - 40} {y - 50}, {x} {y - 70} Z" '
            f'fill="#C9A66B" stroke="{BROWN}" stroke-width="4"/>'
            + ''.join(f'<path d="M{x - 24} {y + k * 18} q 24 8 48 0" fill="none" stroke="{BROWN}" stroke-width="2"/>' for k in range(-1, 4)))


def butterfly(x, y):
    s = ''
    for sgn in (-1, 1):
        s += f'<ellipse cx="{x + sgn * 52}" cy="{y - 26}" rx="54" ry="40" fill="#F2A65A" stroke="{BROWN}" stroke-width="3" transform="rotate({sgn * 25} {x + sgn * 52} {y - 26})"/>'
        s += f'<ellipse cx="{x + sgn * 40}" cy="{y + 30}" rx="34" ry="28" fill="#F2C94C" stroke="{BROWN}" stroke-width="3"/>'
        s += f'<path d="M{x} {y - 52} q {sgn * 10} -30 {sgn * 26} -38" fill="none" stroke="{INK}" stroke-width="3"/>'
    return s + f'<ellipse cx="{x}" cy="{y}" rx="10" ry="52" fill="{INK}"/>'


def grasshopper(x, y, s_=1.0, wings=True):
    b = f'<g transform="translate({x} {y}) scale({s_})">'
    b += '<ellipse cx="0" cy="0" rx="90" ry="24" fill="#8DBF5A" stroke="#4E7A2B" stroke-width="3"/>'
    b += '<circle cx="96" cy="-8" r="24" fill="#8DBF5A" stroke="#4E7A2B" stroke-width="3"/>'
    b += '<path d="M110 -26 q 30 -40 70 -50" fill="none" stroke="#4E7A2B" stroke-width="3"/>'
    if wings:
        b += '<path d="M-60 -18 C -20 -46, 40 -40, 70 -20 C 30 -24, -20 -20, -60 -18 Z" fill="#B9DA8F" stroke="#4E7A2B" stroke-width="3"/>'
    b += '<path d="M-30 14 L -70 -40 L -110 40" fill="none" stroke="#4E7A2B" stroke-width="6" stroke-linejoin="round"/>'
    b += '<path d="M30 18 l -10 30 M 60 16 l 10 30" stroke="#4E7A2B" stroke-width="4"/>'
    return b + '</g>'


def metamorphosis() -> str:
    s = text(920, 52, 'Развитие насекомых с превращением', 'h', 'middle')
    xs = [640, 960, 1280, 1600]
    for row, (y, title, sub) in enumerate(((250, 'Полное превращение', 'жуки, бабочки, мухи, комары, пчёлы'),
                                           (610, 'Неполное превращение', 'саранча, кузнечики, тараканы, богомолы'))):
        s += f'<rect x="20" y="{y - 150}" width="1800" height="300" rx="18" fill="{PAPER}"/>'
        s += text(40, y - 20, title, 't') + text(40, y + 16, sub, 'cap')
        for k in range(3):
            s += arrow(xs[k] + 115, y, xs[k + 1] - 115, y, GREY, 4)
    y = 250
    s += eggs(xs[0], y) + caterpillar(xs[1], y) + pupa(xs[2], y) + butterfly(xs[3], y)
    for x, n in zip(xs, ('яйцо', 'личинка', 'куколка', 'имаго')):
        s += text(x, y + 120, n, 't', 'middle', RED if n == 'куколка' else INK)
    s += text(xs[2], y - 110, 'не питается, не двигается', 'cap', 'middle')
    y = 610
    s += eggs(xs[0], y) + grasshopper(xs[1] - 10, y, 0.6, False) + grasshopper(xs[3] - 20, y, 0.85, True)
    s += f'<rect x="{xs[2] - 95}" y="{y - 70}" width="190" height="140" rx="14" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
    s += text(xs[2], y + 8, 'куколки нет', 's', 'middle', GREY)
    for x, n in zip((xs[0], xs[1], xs[3]), ('яйцо', 'личинка', 'имаго')):
        s += text(x, y + 120, n, 't', 'middle')
    s += text(xs[1], y - 100, 'похожа на взрослого, крылья недоразвиты', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'asexual-reproduction.png': (asexual(), 1740, 680),
        'vegetative-propagation.png': (vegetative(), 1800, 1000),
        'flower-structure.png': (flower(), 1680, 930),
        'double-fertilization.png': (double_fertilization(), 2000, 910),
        'moss-life-cycle.png': (moss_cycle(), 1700, 1000),
        'fern-life-cycle.png': (fern_cycle(), 1700, 1000),
        'embryogenesis.png': (embryogenesis(), 1800, 800),
        'insect-metamorphosis.png': (metamorphosis(), 1840, 780),
    }
    only = set(__import__('sys').argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
