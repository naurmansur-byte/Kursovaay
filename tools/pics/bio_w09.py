"""Рисунки недели 9 биологии (course/biology/week-09/pics/*.png): скелет, позвоночник, трубчатая кость, соединения костей,
сустав, уровни строения мышцы, саркомер, мышцы-антагонисты, особенности скелета человека.

Факты — по выжимке course/textbooks/bio-09-movement.md (Б8 § 31–37, Б10-2 § 111–114). Схемы условные.
Ошибки учебников (ERRATA) не переносим: затылочное отверстие у человека — снизу, ближе к центру; локтевой сустав не шаровидный.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w09.py
"""
from __future__ import annotations

import math

from common import GREY, INK, PAPER, RED, ROOT, arrow, chem, label, render, smooth, text

OUT = ROOT / 'course' / 'biology' / 'week-09' / 'pics'
BLUE = '#3A57A7'
BONE, BONE_LINE, CART, MUSCLE, MUSCLE_LINE = '#F4EBDD', '#8A7350', '#CFE3F2', '#E58C82', '#A2463C'
SEGMENTS = [('шейный', 7, '#F2C14E'), ('грудной', 12, '#E58C82'), ('поясничный', 5, '#7FB3D5'), ('крестцовый', 5, '#9CCB86'), ('копчиковый', 4, '#C7A6E0')]


def lbl(px, py, tx, ty, s, color=INK):
    return label(px, py, tx, ty, s, 's', color)


def lines_at(x, y, rows, cls='s', anchor='middle', step=32, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def bone(x1, y1, x2, y2, w=20, fill=BONE):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BONE_LINE}" stroke-width="{w + 6}" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{fill}" stroke-width="{w}" stroke-linecap="round"/>')


def catmull(points, n=24):
    """Плотная ломаная по Catmull-Rom (для раскладки позвонков вдоль кривой)."""
    pts = [points[0]] + points + [points[-1]]
    out = []
    for k in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[k - 1], pts[k], pts[k + 1], pts[k + 2]
        for i in range(n):
            t = i / n
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    out.append(points[-1])
    return out


def along(poly, frac):
    """Точка и угол касательной на доле длины ломаной."""
    lens = [math.dist(poly[i], poly[i + 1]) for i in range(len(poly) - 1)]
    target = frac * sum(lens)
    for i, L in enumerate(lens):
        if target <= L or i == len(lens) - 1:
            t = target / L if L else 0
            x = poly[i][0] + (poly[i + 1][0] - poly[i][0]) * t
            y = poly[i][1] + (poly[i + 1][1] - poly[i][1]) * t
            return x, y, math.degrees(math.atan2(poly[i + 1][1] - poly[i][1], poly[i + 1][0] - poly[i][0]))
        target -= L
    return poly[-1][0], poly[-1][1], 90


def vertebrae(poly, scale=1.0, labels=False):
    """Позвонки вдоль кривой: 7 + 12 + 5, крестец единым блоком, копчик."""
    s, total, k = '', 33, 0
    bounds = {}
    for name, n, col in SEGMENTS:
        start = k
        if name == 'крестцовый':
            x, y, a = along(poly, (k + 2.5) / total)
            s += (f'<rect x="{x - 26 * scale:.0f}" y="{y - 70 * scale:.0f}" width="{52 * scale:.0f}" height="{140 * scale:.0f}" rx="{14 * scale:.0f}" '
                  f'fill="{col}" stroke="{INK}" stroke-width="2" transform="rotate({a - 90:.0f} {x:.0f} {y:.0f})"/>')
            k += n
        else:
            for i in range(n):
                x, y, a = along(poly, (k + 0.5) / total)
                w, h = (40 if name != 'копчиковый' else 26) * scale, (15 if name != 'поясничный' else 19) * scale
                s += (f'<rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="4" fill="{col}" stroke="{INK}" '
                      f'stroke-width="1.5" transform="rotate({a - 90:.0f} {x:.0f} {y:.0f})"/>')
                k += 1
        bounds[name] = (start, k)
    return s, bounds


# 1. Скелет -------------------------------------------------------------------------------------
def skeleton() -> str:
    s = text(750, 56, 'Скелет человека', 'h', 'middle') + '<g transform="translate(100 0)">'
    cx = 650
    # череп
    s += f'<ellipse cx="{cx}" cy="170" rx="72" ry="80" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<path d="M{cx - 48} 220 Q {cx - 50} 290 {cx} 300 Q {cx + 50} 290 {cx + 48} 220" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<circle cx="{cx - 26}" cy="190" r="15" fill="#fff" stroke="{BONE_LINE}" stroke-width="3"/><circle cx="{cx + 26}" cy="190" r="15" fill="#fff" stroke="{BONE_LINE}" stroke-width="3"/>'
    # позвоночник (вид спереди)
    for k in range(24):
        y = 310 + k * 17
        s += f'<rect x="{cx - 14}" y="{y}" width="28" height="13" rx="3" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="2"/>'
    # рёбра и грудина
    for k in range(10):
        y = 380 + k * 18
        wdt = 70 + 10 * min(k, 6) - 6 * max(0, k - 7)
        for d in (-1, 1):
            s += f'<path d="M{cx + d * 14} {y} Q {cx + d * (wdt + 30)} {y - 10} {cx + d * (wdt + 10)} {y + 40} Q {cx + d * 40} {y + 50} {cx + d * 12} {y + 34}" fill="none" stroke="{BONE_LINE}" stroke-width="5"/>'
    s += f'<rect x="{cx - 12}" y="380" width="24" height="150" rx="8" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="3"/>'
    # ключицы и лопатки
    s += f'<path d="M{cx - 150} 360 L {cx - 120} 400 L {cx - 145} 470 Z" fill="#E9DCC5" stroke="{BONE_LINE}" stroke-width="3"/>'
    s += f'<path d="M{cx + 150} 360 L {cx + 120} 400 L {cx + 145} 470 Z" fill="#E9DCC5" stroke="{BONE_LINE}" stroke-width="3"/>'
    s += bone(cx - 14, 350, cx - 160, 345, 12) + bone(cx + 14, 350, cx + 160, 345, 12)
    # руки
    for d in (-1, 1):
        sx = cx + d * 170
        s += bone(sx, 365, sx + d * 30, 580, 22)
        s += bone(sx + d * 30, 590, sx + d * 55, 790, 11) + bone(sx + d * 46, 592, sx + d * 75, 785, 11)
        for f in range(5):
            s += bone(sx + d * (50 + f * 7), 810, sx + d * (40 + f * 14), 880, 6)
    # таз
    s += (f'<path d="M{cx - 150} 720 Q {cx - 170} 640 {cx - 60} 700 L {cx} 730 L {cx + 60} 700 Q {cx + 170} 640 {cx + 150} 720 '
          f'Q {cx + 140} 800 {cx + 60} 830 L {cx - 60} 830 Q {cx - 140} 800 {cx - 150} 720 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>')
    s += f'<circle cx="{cx}" cy="790" r="34" fill="#fff" stroke="{BONE_LINE}" stroke-width="3"/>'
    # ноги
    for d in (-1, 1):
        hx = cx + d * 110
        s += bone(hx, 800, cx + d * 80, 1060, 26)
        s += f'<circle cx="{cx + d * 80}" cy="1080" r="18" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="3"/>'
        s += bone(cx + d * 76, 1100, cx + d * 72, 1300, 20) + bone(cx + d * 102, 1105, cx + d * 98, 1295, 9)
        s += f'<path d="M{cx + d * 60} 1320 L {cx + d * 120} 1320 L {cx + d * 125} 1360 L {cx + d * 40} 1360 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="3"/>'
    # подписи: слева — голова, туловище, рука; справа — пояса и нога
    s += lbl(cx - 60, 140, 330, 130, 'череп: мозговой отдел')
    s += lbl(cx - 30, 285, 330, 260, 'лицевой отдел')
    s += lbl(cx, 330, 330, 330, 'позвоночник')
    s += lbl(cx - 100, 470, 330, 420, 'рёбра — 12 пар')
    s += lbl(cx - 175, 470, 330, 520, 'плечевая кость')
    s += lbl(cx - 215, 700, 330, 640, 'лучевая и локтевая')
    s += lbl(cx - 230, 850, 330, 860, 'кисть')
    s += lbl(cx + 80, 350, 960, 300, 'ключица (плечевой пояс)')
    s += lbl(cx + 140, 420, 960, 400, 'лопатка (плечевой пояс)')
    s += lbl(cx, 460, 960, 480, 'грудина')
    s += lbl(cx + 140, 740, 960, 700, 'тазовая кость (3 сросшиеся)')
    s += lbl(cx + 97, 930, 960, 900, 'бедренная кость')
    s += lbl(cx + 96, 1080, 960, 1040, 'надколенник')
    s += lbl(cx + 99, 1200, 960, 1180, 'большая и малая берцовые')
    s += lbl(cx + 110, 1340, 960, 1330, 'стопа')
    return s + '</g>'


# 2. Позвоночник -------------------------------------------------------------------------------
def spine() -> str:
    s = text(600, 56, 'Позвоночник: 5 отделов, 4 изгиба', 'h', 'middle')
    curve = catmull([(560, 130), (600, 230), (580, 330), (500, 500), (540, 680), (600, 780), (575, 880), (520, 960), (535, 1030), (575, 1060)])
    s += f'<path d="M{" L".join(f"{x:.0f} {y:.0f}" for x, y in curve)}" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="6 6"/>'
    v, bounds = vertebrae(curve)
    s += v
    for name, n, col in SEGMENTS:
        a, b = bounds[name]
        x, y, _ = along(curve, (a + b) / 2 / 33)
        cnt = '4–5' if name == 'копчиковый' else str(n)
        s += lbl(x - 30, y, 360, y + 8, f'{name} — {cnt}', INK)
    s += lbl(615, 230, 760, 230, 'изгиб вперёд') + lbl(495, 500, 760, 470, 'изгиб назад', BLUE)
    s += lbl(610, 780, 760, 760, 'изгиб вперёд') + lbl(520, 950, 760, 960, 'изгиб назад', BLUE)
    s += arrow(780, 1100, 900, 1100, INK, 4) + text(760, 1108, 'спина', 'cap', 'end') + text(920, 1108, 'грудь и живот', 'cap', 'start')
    s += text(600, 1170, 'Всего 33–34 позвонка; изгибы смягчают толчки при ходьбе и беге.', 's', 'middle')
    return s


# 3. Трубчатая кость ------------------------------------------------------------------------------
def long_bone() -> str:
    s = text(650, 56, 'Строение трубчатой кости', 'h', 'middle')
    cx = 340
    head = lambda cy: f'<ellipse cx="{cx}" cy="{cy}" rx="120" ry="95" fill="#F7E2C6" stroke="{BONE_LINE}" stroke-width="5"/>'
    s += f'<rect x="{cx - 70}" y="230" width="140" height="500" fill="#E9D6B5" stroke="{BONE_LINE}" stroke-width="5"/>'
    s += head(200) + head(760)
    # губчатое вещество в головках
    for cy, sign in ((200, 1), (760, -1)):
        for k in range(-4, 5):
            s += f'<path d="M{cx + k * 22} {cy + sign * 70} Q {cx + k * 30} {cy} {cx + k * 14} {cy - sign * 70}" fill="none" stroke="#C98A6A" stroke-width="3"/>'
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="120" ry="95" fill="none" stroke="#B8A07A" stroke-width="14"/>'
    # суставной хрящ сверху
    s += f'<path d="M{cx - 105} 160 A 120 95 0 0 1 {cx + 105} 160" fill="none" stroke="#7FB3D5" stroke-width="16"/>'
    # ростковые пластинки
    for y in (290, 670):
        s += f'<path d="M{cx - 85} {y} H {cx + 85}" stroke="#4E8FC2" stroke-width="10"/>'
    # компактное вещество и полость
    s += f'<rect x="{cx - 40}" y="300" width="80" height="360" rx="10" fill="#F6E38A" stroke="#C9A43A" stroke-width="3"/>'
    s += f'<path d="M{cx - 66} 300 V 660 M{cx + 66} 300 V 660" stroke="#B8A07A" stroke-width="20"/>'
    # надкостница — тонкая красная линия по телу, не на суставной поверхности
    s += f'<path d="M{cx - 78} 290 V 680 M{cx + 78} 290 V 680" stroke="{RED}" stroke-width="5"/>'
    s += lbl(cx + 60, 140, 560, 120, 'суставной хрящ (на поверхности)', '#2F6E9E')
    s += lbl(cx + 40, 200, 560, 200, 'губчатое вещество: красный костный мозг')
    s += lbl(cx + 85, 290, 560, 290, 'хрящевая пластинка — рост в длину', '#2F6E9E')
    s += lbl(cx + 78, 380, 560, 380, 'надкостница — рост в толщину и срастание', RED)
    s += lbl(cx + 62, 470, 560, 470, 'компактное вещество')
    s += lbl(cx + 10, 560, 560, 560, 'полость: жёлтый костный мозг')
    s += text(568, 594, '(у детей — красный)', 'cap')
    s += text(650, 880, 'Соли кальция — твёрдость; органическое вещество (оссеин) — упругость.', 's', 'middle')
    return s


# 4. Соединения костей ------------------------------------------------------------------------------
def bone_connections() -> str:
    s = text(800, 56, 'Три типа соединения костей', 'h', 'middle')
    panels = [('неподвижное', 'шов', ['кости мозгового', 'отдела черепа, таза']),
              ('полуподвижное', 'хрящевая прокладка', ['позвонки,', 'рёбра с грудиной']),
              ('подвижное', 'сустав', ['кости конечностей,', 'нижняя челюсть'])]
    for k, (kind, how, ex) in enumerate(panels):
        x = 30 + k * 520
        cx = x + 240
        s += f'<rect x="{x}" y="100" width="480" height="560" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += text(cx, 155, kind, 't', 'middle', RED) + text(cx, 192, how, 's', 'middle')
        if k == 0:
            s += f'<path d="M{cx - 170} 260 H {cx + 170} V 420 H {cx - 170} Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
            zig = ' '.join(f'L {cx + (12 if i % 2 else -12)} {260 + i * 16}' for i in range(11))
            s += f'<path d="M{cx} 260 {zig}" fill="none" stroke="{BONE_LINE}" stroke-width="4"/>'
        elif k == 1:
            s += f'<rect x="{cx - 110}" y="230" width="220" height="80" rx="16" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
            s += f'<rect x="{cx - 100}" y="314" width="200" height="40" rx="14" fill="{CART}" stroke="#4E8FC2" stroke-width="3"/>'
            s += f'<rect x="{cx - 110}" y="358" width="220" height="80" rx="16" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
            s += text(cx + 120, 342, 'хрящ', 'cap', 'start', '#2F6E9E')
        else:
            s += f'<path d="M{cx - 60} 230 V 300 A 60 60 0 1 0 {cx + 60} 300 V 230" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
            s += f'<path d="M{cx - 110} 450 V 380 Q {cx - 100} 330 {cx - 80} 330 A 82 82 0 0 0 {cx + 80} 330 Q {cx + 100} 330 {cx + 110} 380 V 450 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
            s += f'<path d="M{cx - 140} 310 Q {cx - 140} 400 {cx - 90} 410 M{cx + 140} 310 Q {cx + 140} 400 {cx + 90} 410" fill="none" stroke="{MUSCLE_LINE}" stroke-width="4"/>'
        s += lines_at(cx, 520, ex, 's')
    s += text(800, 700, 'Роднички черепа новорождённого окостеневают к 2 годам.', 'cap', 'middle')
    return s


# 5. Сустав ----------------------------------------------------------------------------------------
def joint() -> str:
    s = text(660, 56, 'Строение сустава', 'h', 'middle')
    cx = 600
    # полость и капсула
    cap = [(cx - 82, 250), (cx - 160, 360), (cx - 168, 470), (cx - 152, 560), (cx + 152, 560), (cx + 168, 470), (cx + 160, 360), (cx + 82, 250)]
    s += f'<path d="{smooth(cap, True)}" fill="#EAF4FB" stroke="{MUSCLE_LINE}" stroke-width="7"/>'
    # верхняя кость с головкой
    s += f'<path d="M{cx - 80} 90 V 330 A 110 100 0 0 0 {cx + 80} 330 V 90 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="5"/>'
    s += f'<path d="M{cx - 98} 360 A 110 100 0 0 0 {cx + 98} 360" fill="none" stroke="#7FB3D5" stroke-width="16"/>'
    # нижняя кость со впадиной
    s += f'<path d="M{cx - 150} 760 V 520 Q {cx - 150} 470 {cx - 120} 470 A 125 90 0 0 0 {cx + 120} 470 Q {cx + 150} 470 {cx + 150} 520 V 760 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="5"/>'
    s += f'<path d="M{cx - 118} 478 A 125 90 0 0 0 {cx + 118} 478" fill="none" stroke="#7FB3D5" stroke-width="16"/>'
    # связки снаружи капсулы
    for d in (-1, 1):
        s += f'<path d="M{cx + d * 84} 200 Q {cx + d * 250} 430 {cx + d * 152} 660" fill="none" stroke="#C9A43A" stroke-width="12" stroke-linecap="round"/>'
    s += lbl(cx - 40, 250, 330, 160, 'головка')
    s += lbl(cx + 70, 393, 880, 300, 'суставной хрящ', '#2F6E9E')
    s += lbl(cx + 10, 450, 880, 420, 'полость с суставной жидкостью', '#2F6E9E')
    s += lbl(cx - 166, 460, 330, 460, 'суставная сумка', MUSCLE_LINE)
    s += lbl(cx + 187, 522, 880, 560, 'связки — прочность, ограничение')
    s += text(888, 594, 'движений, защита от вывиха', 's')
    s += lbl(cx - 80, 620, 330, 680, 'впадина')
    s += text(660, 830, 'Дополнительно в коленном суставе — мениски и надколенник.', 'cap', 'middle')
    return s


# 6. Уровни мышцы -----------------------------------------------------------------------------------
def muscle_levels() -> str:
    s = text(800, 56, 'Из чего состоит скелетная мышца', 'h', 'middle')
    xs = [150, 470, 790, 1110, 1430]
    caps = [('мышца', ['фасция снаружи,', 'сухожилия на концах']), ('пучок волокон', ['между пучками —', 'сосуды и нервы']),
            ('мышечное волокно', ['клетка до 10 см,', 'многоядерная']), ('миофибрилла', ['тёмные A и светлые I', '— исчерченность']),
            ('саркомер', ['от Z до Z —', 'единица сокращения'])]
    y = 280
    # мышца
    s += f'<path d="M{xs[0]} 120 Q {xs[0] + 90} 200 {xs[0] + 70} {y} Q {xs[0] + 90} 360 {xs[0]} 440 Q {xs[0] - 90} 360 {xs[0] - 70} {y} Q {xs[0] - 90} 200 {xs[0]} 120 Z" fill="{MUSCLE}" stroke="{MUSCLE_LINE}" stroke-width="4"/>'
    s += f'<path d="M{xs[0]} 120 V 90 M{xs[0]} 440 V 470" stroke="#D9CBB0" stroke-width="16" stroke-linecap="round"/>'
    # пучок: круг из волокон
    s += f'<circle cx="{xs[1]}" cy="{y}" r="95" fill="#F3C4BE" stroke="{MUSCLE_LINE}" stroke-width="4"/>'
    for k in range(19):
        a, r = k * 2.4, 14 + 70 * math.sqrt(k / 19)
        s += f'<circle cx="{xs[1] + r * math.cos(a):.0f}" cy="{y + r * math.sin(a):.0f}" r="13" fill="{MUSCLE}" stroke="{MUSCLE_LINE}" stroke-width="2"/>'
    s += f'<circle cx="{xs[1] + 60}" cy="{y - 60}" r="7" fill="{RED}"/><circle cx="{xs[1] - 70}" cy="{y + 40}" r="7" fill="{BLUE}"/>'
    # волокно
    s += f'<rect x="{xs[2] - 130}" y="{y - 45}" width="260" height="90" rx="40" fill="{MUSCLE}" stroke="{MUSCLE_LINE}" stroke-width="3"/>'
    for dx in (-80, -20, 40, 95):
        s += f'<ellipse cx="{xs[2] + dx}" cy="{y - 28}" rx="12" ry="7" fill="#7A2E28"/>'
    for k in range(4):
        s += f'<path d="M{xs[2] - 120} {y - 10 + k * 14} H {xs[2] + 120}" stroke="#C2554B" stroke-width="3"/>'
    # миофибрилла
    for k in range(10):
        s += f'<rect x="{xs[3] - 130 + k * 26}" y="{y - 22}" width="26" height="44" fill="{"#7A2E28" if k % 2 else "#F3C4BE"}"/>'
    s += f'<rect x="{xs[3] - 130}" y="{y - 22}" width="260" height="44" fill="none" stroke="{INK}" stroke-width="2"/>'
    # саркомер
    s += f'<path d="M{xs[4] - 120} {y - 70} V {y + 70} M{xs[4] + 120} {y - 70} V {y + 70}" stroke="{INK}" stroke-width="5"/>'
    for dy in (-40, 0, 40):
        s += f'<path d="M{xs[4] - 120} {y + dy - 12} H {xs[4] - 20} M{xs[4] + 120} {y + dy - 12} H {xs[4] + 20}" stroke="{BLUE}" stroke-width="3"/>'
        s += f'<path d="M{xs[4] - 70} {y + dy} H {xs[4] + 70}" stroke="{RED}" stroke-width="9"/>'
    s += text(xs[4] - 120, y + 100, 'Z', 't', 'middle') + text(xs[4] + 120, y + 100, 'Z', 't', 'middle')
    for k, (title, rows) in enumerate(caps):
        s += text(xs[k], 520, title, 't', 'middle', RED if k == 4 else INK) + lines_at(xs[k], 560, rows, 'cap')
        if k < 4:
            s += arrow(xs[k] + 140 if k else xs[k] + 100, y, xs[k + 1] - 140 if k + 1 < 4 else xs[k + 1] - 140, y, GREY, 4)
    return s


# 7. Саркомер -------------------------------------------------------------------------------------
def sarcomere_row(y, z1, z2, title):
    s = text(80, y - 100, title, 't')
    s += f'<path d="M{z1} {y - 80} V {y + 80} M{z2} {y - 80} V {y + 80}" stroke="{INK}" stroke-width="6"/>'
    for dy in (-50, 0, 50):
        s += f'<path d="M{z1} {y + dy - 16} h 350 M{z2} {y + dy - 16} h -350" stroke="{BLUE}" stroke-width="4"/>'
        s += f'<path d="M{z1} {y + dy + 16} h 350 M{z2} {y + dy + 16} h -350" stroke="{BLUE}" stroke-width="4"/>'
        s += f'<path d="M400 {y + dy} H 900" stroke="{RED}" stroke-width="12"/>'
        for x in range(420, 900, 40):
            if not 620 < x < 680:
                s += f'<path d="M{x} {y + dy - 6} l 8 -8 M{x} {y + dy + 6} l 8 8" stroke="{RED}" stroke-width="3"/>'
    def brace(x1, x2, yy, cap, col, up=False):
        tick = 10 if up else -10
        ty = yy - 14 if up else yy + 30
        return (f'<path d="M{x1} {yy + tick} V {yy} H {x2} V {yy + tick}" fill="none" stroke="{col}" stroke-width="3"/>'
                + text((x1 + x2) / 2, ty, cap, 'cap', 'middle', col))
    h1, h2 = z1 + 350, z2 - 350
    s += brace(400, 900, y + 110, 'диск A (длина не меняется)', INK)
    s += brace(z1, 400, y + 160, 'I', BLUE) + brace(900, z2, y + 160, 'I', BLUE)
    s += brace(h1, h2, y - 90, 'H', GREY, True)
    s += text(z1, y - 95, 'Z', 't', 'middle') + text(z2, y - 95, 'Z', 't', 'middle')
    return s


def sarcomere() -> str:
    s = text(750, 56, 'Саркомер: нити скользят, их длина не меняется', 'h', 'middle')
    s += sarcomere_row(260, 200, 1100, 'покой')
    s += sarcomere_row(620, 290, 1010, 'сокращение')
    s += f'<rect x="1150" y="200" width="320" height="200" rx="16" fill="{PAPER}"/>'
    s += f'<path d="M1180 250 H 1260" stroke="{RED}" stroke-width="12"/>' + text(1280, 258, 'миозин —', 's') + text(1280, 290, 'толстые нити', 's')
    s += f'<path d="M1180 340 H 1260" stroke="{BLUE}" stroke-width="4"/>' + text(1280, 348, 'актин —', 's') + text(1280, 380, 'тонкие нити', 's')
    s += lines_at(1310, 560, ['Z сближаются,', 'I и H короче,', 'A прежний'], 's', step=36)
    s += text(750, 830, chem('Запуск — ионы Ca²⁺; энергия для мостиков — АТФ.'), 'cap', 'middle')
    return s


# 8. Антагонисты --------------------------------------------------------------------------------
def arm(sx, sy, ang_fore, flex):
    """Плечевая кость вертикально, предплечье под углом; бицепс спереди, трицепс сзади."""
    ex, ey = sx, sy + 300
    fx, fy = ex + 280 * math.cos(math.radians(ang_fore)), ey - 280 * math.sin(math.radians(ang_fore))
    s = bone(sx, sy, ex, ey, 26) + bone(ex, ey, fx, fy, 18)
    bx, by = ex + 60 * math.cos(math.radians(ang_fore)), ey - 60 * math.sin(math.radians(ang_fore))
    bic_w = 46 if flex else 24
    tri_w = 24 if flex else 46
    s += (f'<path d="M{sx + 14} {sy + 30} Q {sx + 30 + bic_w * 1.6} {(sy + ey) / 2} {bx:.0f} {by:.0f} Q {sx + 30} {(sy + ey) / 2} {sx + 14} {sy + 30} Z" '
          f'fill="{MUSCLE if flex else "#F3C4BE"}" stroke="{MUSCLE_LINE}" stroke-width="3"/>')
    s += (f'<path d="M{sx - 14} {sy + 30} Q {sx - 30 - tri_w * 1.6} {(sy + ey) / 2} {ex - 22} {ey + 18} Q {sx - 30} {(sy + ey) / 2} {sx - 14} {sy + 30} Z" '
          f'fill="{"#C9D7EF" if flex else "#7FA0D8"}" stroke="{BLUE}" stroke-width="3"/>')
    s += f'<circle cx="{ex}" cy="{ey}" r="12" fill="{INK}"/>'
    return s, (bx, by), (ex, ey), (fx, fy)


def antagonists() -> str:
    s = text(750, 56, 'Мышцы-антагонисты: сгибатель и разгибатель', 'h', 'middle')
    a, b, e, f = arm(420, 160, 70, True)
    s += a + text(420, 120, 'Сгибание', 't', 'middle')
    s += lbl(490, 300, 640, 250, 'бицепс сокращён', MUSCLE_LINE)
    s += lbl(390, 330, 250, 330, 'трицепс', BLUE) + text(242, 364, 'расслаблен', 'cap', 'end')
    s += lbl(e[0], e[1], 640, 520, 'локоть — точка опоры')
    a, b, e, f = arm(1080, 160, -80, False)
    s += a + text(1080, 120, 'Разгибание', 't', 'middle')
    s += lbl(1130, 300, 1280, 250, 'бицепс', MUSCLE_LINE) + text(1288, 284, 'расслаблен', 'cap')
    s += lbl(1040, 330, 900, 330, 'трицепс сокращён', BLUE)
    s += text(750, 820, 'Мышца только тянет — поэтому сгибатель и разгибатель работают по очереди.', 's', 'middle')
    return s


# 9. Особенности скелета человека ----------------------------------------------------------------
def bipedal_skeleton() -> str:
    s = text(800, 56, 'Скелет человека и прямохождение', 'h', 'middle')
    # позвоночник: 4 изгиба, лицо вправо
    curve = catmull([(355, 290), (372, 345), (350, 405), (318, 500), (335, 600), (366, 680), (350, 760), (322, 815), (334, 860)])
    # рёбра
    for k in range(8):
        sx, sy, _ = along(curve, (8 + k * 1.4) / 33)
        s += f'<path d="M{sx:.0f} {sy:.0f} Q {sx + 80:.0f} {sy - 20:.0f} {470 - k * 2} {sy + 30:.0f}" fill="none" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<path d="M468 430 L 462 560" stroke="{BONE_LINE}" stroke-width="10" stroke-linecap="round"/>'
    v, _ = vertebrae(curve, 0.75)
    s += v
    # череп: мозговой отдел больше лицевого, подбородок, отверстие снизу
    s += f'<ellipse cx="350" cy="190" rx="100" ry="88" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<path d="M420 240 Q 450 270 445 300 Q 452 320 430 325 L 380 320 Q 395 290 380 270 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<ellipse cx="352" cy="276" rx="16" ry="7" fill="#fff" stroke="{RED}" stroke-width="3"/>'
    # таз, нога, стопа со сводом
    s += f'<path d="M300 735 Q 330 700 420 712 Q 440 770 420 815 Q 380 860 330 845 Q 295 800 300 735 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += bone(378, 825, 392, 1060, 24)
    s += f'<circle cx="414" cy="1066" r="13" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="3"/>'
    s += bone(390, 1078, 382, 1280, 20) + bone(370, 1086, 364, 1276, 8)
    s += f'<path d="M345 1312 Q 350 1282 385 1284 Q 450 1290 510 1312 Q 430 1296 345 1312 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    # рука короче ноги
    s += bone(425, 415, 432, 635, 16) + bone(432, 645, 462, 815, 11)
    s += f'<path d="M456 826 L 474 822 L 484 872 L 462 876 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="3"/>'
    s += lbl(400, 150, 600, 150, 'мозговой отдел больше лицевого')
    s += lbl(352, 283, 600, 240, 'затылочное отверстие — снизу', RED)
    s += lbl(443, 312, 600, 320, 'подбородочный выступ')
    s += lbl(320, 500, 600, 430, 'позвоночник: 4 изгиба')
    s += lbl(462, 520, 600, 520, 'грудная клетка уплощена')
    s += lbl(415, 760, 600, 740, 'таз чашеобразный')
    s += lbl(390, 960, 600, 960, 'ноги длиннее и сильнее рук')
    s += lbl(450, 1298, 600, 1240, 'стопа со сводом')
    # врезка: затылочное отверстие
    s += f'<rect x="1060" y="110" width="510" height="660" rx="18" fill="{PAPER}"/>'
    s += text(1315, 160, 'Затылочное отверстие', 't', 'middle')
    s += text(1315, 215, 'человек — снизу, ближе к центру', 's', 'middle')
    s += f'<ellipse cx="1290" cy="320" rx="105" ry="72" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<path d="M1370 350 Q 1400 380 1388 410 L 1345 402 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<path d="M1295 398 V 470" stroke="{BONE_LINE}" stroke-width="16"/>'
    s += f'<ellipse cx="1295" cy="390" rx="15" ry="6" fill="#fff" stroke="{RED}" stroke-width="3"/>'
    s += text(1315, 530, 'обезьяна — ближе к затылку', 's', 'middle')
    s += f'<ellipse cx="1270" cy="620" rx="88" ry="60" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<path d="M1340 600 Q 1430 615 1440 650 Q 1420 680 1330 668 Z" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    s += f'<path d="M1200 668 Q 1180 700 1150 745" stroke="{BONE_LINE}" stroke-width="16" fill="none"/>'
    s += f'<ellipse cx="1203" cy="665" rx="15" ry="6" fill="#fff" stroke="{RED}" stroke-width="3"/>'
    # врезка: кисть
    s += f'<rect x="1060" y="800" width="510" height="400" rx="18" fill="{PAPER}"/>'
    s += text(1315, 850, 'Кисть человека', 't', 'middle')
    hx, hy = 1290, 1070
    s += f'<rect x="{hx - 70}" y="{hy - 120}" width="140" height="150" rx="30" fill="{BONE}" stroke="{BONE_LINE}" stroke-width="4"/>'
    for k in range(4):
        s += bone(hx - 50 + k * 33, hy - 120, hx - 52 + k * 34, hy - 190 + abs(k - 1.5) * 10, 18)
    s += bone(hx + 70, hy - 20, hx + 135, hy - 85, 20)
    s += text(1315, 1135, 'большой палец', 's', 'middle') + text(1315, 1167, 'противопоставлен остальным', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'skeleton.png': (skeleton(), 1500, 1400),
        'spine.png': (spine(), 1200, 1210),
        'bone.png': (long_bone(), 1300, 920),
        'bone-connections.png': (bone_connections(), 1600, 730),
        'joint.png': (joint(), 1320, 860),
        'muscle-levels.png': (muscle_levels(), 1600, 640),
        'sarcomere.png': (sarcomere(), 1500, 860),
        'antagonists.png': (antagonists(), 1500, 860),
        'bipedal-skeleton.png': (bipedal_skeleton(), 1600, 1340),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
