"""Рисунки недели 3 биологии (course/biology/week-03/pics/*.png): мембрана, транспорт, осмос, насос, ферменты.

Факты — по выжимке course/textbooks/bio-03-membrane-enzymes.md (Б9, Б10-1, Б11-1).
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w03.py
"""
from __future__ import annotations

from common import GREEN, GREY, INK, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, PAPER, RED, ROOT, arrow, chem, lab, label, render, smooth, text

OUT = ROOT / 'course' / 'biology' / 'week-03' / 'pics'
BLUE, ORANGE, PURPLE, LILAC = '#3A57A7', '#D9822B', '#7A4FA3', '#E6DDF2'
HEAD, HEAD_LINE, TAIL = '#F6C667', '#B4842C', '#B9A27A'


def lipids(x1: float, x2: float, y: float, down: bool, step: float = 34, skip: tuple = (), r: float = 13, tail: float = 56) -> str:
    """Ряд фосфолипидов: головки на уровне y, хвосты вниз (наружный слой) или вверх (внутренний)."""
    s, sign, x = '', 1 if down else -1, x1
    while x <= x2:
        if not any(a <= x <= b for a, b in skip):
            for dx in (-5, 5):
                y0, y1 = y + sign * r, y + sign * (r + tail)
                s += f'<path d="M{x + dx:.0f} {y0:.0f} q {dx * 0.8:.0f} {sign * tail / 3:.0f} 0 {sign * tail * 0.5:.0f} t 0 {sign * tail * 0.5:.0f}" fill="none" stroke="{TAIL}" stroke-width="4"/>'
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{HEAD}" stroke="{HEAD_LINE}" stroke-width="2.5"/>'
        x += step
    return s


def bilayer(x1: float, x2: float, y_out: float, y_in: float, **kw) -> str:
    return lipids(x1, x2, y_out, True, **kw) + lipids(x1, x2, y_in, False, **kw)


def ion(cx: float, cy: float, s: str, color: str, r: float = 22) -> str:
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{color}"/>'
            f'<text x="{cx:.0f}" y="{cy + 6:.0f}" text-anchor="middle" style="font-size:17px;font-weight:800;fill:#fff">{chem(s)}</text>')


def sugar_chain(segs: list[tuple[tuple[float, float], tuple[float, float]]]) -> str:
    s = ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{ORANGE}" stroke-width="3"/>' for a, b in segs)
    pts = {p for seg in segs for p in seg}
    return s + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="{LIGHT_YELLOW}" stroke="{ORANGE}" stroke-width="3"/>' for x, y in pts)


def fluid_mosaic() -> str:
    s = text(800, 55, 'Жидкостно-мозаичная модель мембраны', 'h', 'middle')
    s += text(60, 120, 'снаружи клетки', 's', fill=GREY) + text(60, 700, 'цитоплазма', 's', fill=GREY)
    s += bilayer(80, 1520, 300, 450, skip=((425, 575), (975, 1125)))
    s += f'<rect x="440" y="255" width="120" height="240" rx="50" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="4"/>'
    s += f'<rect x="990" y="255" width="120" height="240" rx="50" fill="{LILAC}" stroke="{PURPLE}" stroke-width="4"/>'
    s += f'<ellipse cx="720" cy="500" rx="58" ry="30" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4"/>'
    s += f'<ellipse cx="1320" cy="252" rx="58" ry="30" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4"/>'
    s += sugar_chain([((500, 255), (500, 228)), ((500, 228), (482, 205)), ((482, 205), (470, 180)), ((500, 228), (520, 204)), ((520, 204), (538, 182))])
    s += sugar_chain([((828, 287), (828, 260)), ((828, 260), (812, 238)), ((812, 238), (826, 214)), ((828, 260), (848, 240))])
    s += lab(216, 287, 216, 190, 'гидрофильная головка')
    s += lab(470, 180, 640, 120, 'углеводные цепочки — гликокаликс')
    s += f'<line x1="826" y1="214" x2="700" y2="128" stroke="{INK}" stroke-width="2.5"/><circle cx="826" cy="214" r="5" fill="{INK}"/>'
    s += lab(1320, 222, 1320, 160, 'периферический белок')
    s += lab(250, 375, 230, 620, 'гидрофобные хвосты')
    s += lab(500, 495, 500, 665, 'интегральный белок') + lab(720, 530, 760, 615, 'периферический белок')
    s += lab(1050, 495, 1050, 665, 'интегральный белок')
    s += f'<line x1="1330" y1="492" x2="1490" y2="492" stroke="{RED}" stroke-width="4"/>' + arrow(1400, 492, 1330, 492, RED, 4) + arrow(1420, 492, 1490, 492, RED, 4)
    s += text(1410, 600, 'липиды и белки', 's', 'middle') + text(1410, 632, 'перемещаются в слое', 's', 'middle')
    s += text(800, 745, 'Головки — к воде, хвосты — внутрь бислоя.', 't', 'middle')
    return s


def passive_transport() -> str:
    s = text(800, 55, 'Пассивный транспорт', 'h', 'middle')
    titles = [('Простая диффузия', ['через липидный бислой;', chem('малые неполярные, например O₂')]),
              ('Через канал', ['белок-канал с водной порой;', 'ионы по своему градиенту']),
              ('С переносчиком', ['облегчённая диффузия: белок', 'меняет форму; есть насыщение'])]
    top_dots = [(-150, -200), (-90, -230), (-30, -180), (40, -210), (110, -185), (150, -225), (-120, -135), (80, -125), (-40, -240)]
    low_dots = [(-110, 120), (60, 140), (150, 110)]
    for k, (title, cap) in enumerate(titles):
        x0, cx = 30 + k * 530, 30 + k * 530 + 240
        s += f'<rect x="{x0}" y="90" width="480" height="580" rx="16" fill="{PAPER}"/>' + text(cx, 140, title, 't', 'middle')
        skip = () if k == 0 else ((cx - 70, cx + 70),)
        s += bilayer(x0 + 25, x0 + 465, 360, 480, step=30, skip=skip, r=11, tail=40)
        dot = (lambda x, y: f'<circle cx="{x}" cy="{y}" r="9" fill="{BLUE}"/>') if k == 0 else (lambda x, y: ion(x, y, '+', PURPLE, 14))
        if k == 2:
            dot = lambda x, y: f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" rx="4" fill="{ORANGE}"/>'  # noqa: E731
        s += ''.join(dot(cx + dx, 420 + dy) for dx, dy in top_dots + low_dots)
        s += ''.join(text(cx, 610 + j * 32, ln, 's', 'middle') for j, ln in enumerate(cap))
    # 1: стрелка сквозь бислой
    cx = 270
    s += arrow(cx, 250, cx, 560, GREEN, 7) + f'<circle cx="{cx + 22}" cy="420" r="9" fill="{BLUE}"/>'
    # 2: канал — два белка с порой между ними
    cx = 800
    s += f'<rect x="{cx - 68}" y="335" width="50" height="170" rx="20" fill="{LILAC}" stroke="{PURPLE}" stroke-width="4"/>'
    s += f'<rect x="{cx + 18}" y="335" width="50" height="170" rx="20" fill="{LILAC}" stroke="{PURPLE}" stroke-width="4"/>'
    s += f'<rect x="{cx - 18}" y="335" width="36" height="170" fill="{LIGHT_BLUE}"/>' + ion(cx, 420, '+', PURPLE, 14)
    s += arrow(cx, 250, cx, 395, GREEN, 6) + arrow(cx, 446, cx, 560, GREEN, 6)
    # 3: переносчик открыт наружу -> открыт внутрь
    cx = 1330
    for dx, open_up in ((-60, True), (60, False)):
        x = cx + dx
        if open_up:
            d = f'M{x - 45} 335 H{x - 12} L{x} 380 L{x + 12} 335 H{x + 45} V505 H{x - 45} Z'
            mol_y = 368
        else:
            d = f'M{x - 45} 335 H{x + 45} V505 H{x + 12} L{x} 460 L{x - 12} 505 H{x - 45} Z'
            mol_y = 492
        s += f'<path d="{d}" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="4" stroke-linejoin="round"/>'
        s += f'<rect x="{x - 10}" y="{mol_y - 10}" width="20" height="20" rx="4" fill="{ORANGE}"/>'
    s += arrow(cx - 18, 420, cx + 18, 420, INK, 4)
    s += text(800, 720, 'Все три пути — по градиенту концентрации, без затрат АТФ.', 't', 'middle', GREEN)
    return s


def plant_osmosis() -> str:
    s = text(800, 55, 'Растительная клетка в воде и в растворе соли', 'h', 'middle')
    panels = [(40, 'В воде', LIGHT_BLUE), (820, 'В более концентрированном растворе соли', '#F1EEDF')]
    for x0, title, bg in panels:
        s += f'<rect x="{x0}" y="95" width="740" height="500" rx="16" fill="{bg}"/>' + text(x0 + 370, 140, title, 's', 'middle')
    s += ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="{GREY}"/>' for x, y in
                 [(870, 200), (930, 560), (1010, 180), (1480, 210), (1500, 520), (1400, 570), (880, 420), (1520, 380), (950, 300), (1460, 300)])
    for cx, shrunk in ((410, False), (1190, True)):
        s += f'<rect x="{cx - 160}" y="190" width="320" height="320" rx="20" fill="{"#fff" if not shrunk else "#F1EEDF"}" stroke="#5B7A2A" stroke-width="16"/>'
        if not shrunk:
            s += f'<rect x="{cx - 144}" y="206" width="288" height="288" rx="12" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="3"/>'
            s += f'<rect x="{cx - 100}" y="250" width="200" height="200" rx="36" fill="#DDEBF7" stroke="#5E8BB5" stroke-width="3"/>'
        else:
            blob = [(cx - 85, 280), (cx - 20, 255), (cx + 70, 265), (cx + 95, 340), (cx + 80, 420), (cx + 10, 445), (cx - 75, 430), (cx - 100, 350)]
            s += f'<path d="{smooth(blob, closed=True)}" fill="{LIGHT_GREEN}" stroke="{GREEN}" stroke-width="3"/>'
            s += f'<ellipse cx="{cx}" cy="350" rx="48" ry="45" fill="#DDEBF7" stroke="#5E8BB5" stroke-width="3"/>'
        for y in (300, 400):  # вода: в воде — внутрь, в растворе соли — наружу
            for side in (-1, 1):
                outer, inner = cx + side * 290, cx + side * (180 if not shrunk else 112)
                s += arrow(outer, y, inner, y, BLUE, 6) if not shrunk else arrow(inner, y, outer, y, BLUE, 6)
    s += text(410, 640, 'тургор: вода входит,', 't', 'middle') + text(410, 676, 'содержимое прижато к стенке', 's', 'middle')
    s += text(1190, 640, 'плазмолиз: вода выходит,', 't', 'middle') + text(1190, 676, 'протопласт отходит от стенки', 's', 'middle')
    s += text(800, 730, 'Клеточная стенка в обоих случаях одна и та же.', 'cap', 'middle')
    return s


def sodium_potassium_pump() -> str:
    s = text(800, 55, 'Натрий-калиевый насос', 'h', 'middle')
    NA, K = ORANGE, PURPLE
    s += text(60, 115, 'снаружи клетки: Na⁺ много, K⁺ мало'.replace('Na⁺', chem('Na⁺')).replace('K⁺', chem('K⁺')), 's', fill=GREY)
    s += text(60, 705, 'цитоплазма: K⁺ много, Na⁺ мало'.replace('Na⁺', chem('Na⁺')).replace('K⁺', chem('K⁺')), 's', fill=GREY)
    s += bilayer(60, 1540, 330, 470, skip=((665, 935),))
    s += f'<rect x="680" y="280" width="240" height="240" rx="40" fill="{LILAC}" stroke="{PURPLE}" stroke-width="5"/>'
    s += text(800, 392, chem('Na⁺/K⁺-'), 's', 'middle') + text(800, 424, 'АТФаза', 's', 'middle')
    s += ''.join(ion(x, y, 'Na⁺', NA) for x, y in [(150, 200), (260, 170), (380, 230), (480, 180), (1150, 200), (1260, 170), (1380, 230), (1480, 190)])
    s += ion(300, 265, 'K⁺', K) + ion(1080, 265, 'K⁺', K)
    s += ''.join(ion(x, y, 'K⁺', K) for x, y in [(150, 600), (270, 640), (390, 590), (1250, 600), (1370, 640), (1480, 590), (1130, 650)])
    s += ion(520, 650, 'Na⁺', NA)
    # перенос: 3 Na⁺ наружу (слева), 2 K⁺ внутрь (справа)
    s += ''.join(ion(x, y, 'Na⁺', NA) for x, y in [(640, 590), (700, 625), (760, 595)])
    s += arrow(740, 555, 740, 240, RED, 6)
    s += ''.join(ion(x, y, 'Na⁺', NA) for x, y in [(640, 230), (690, 175), (760, 155)])
    s += ''.join(ion(x, y, 'K⁺', K) for x, y in [(900, 175), (965, 220)])
    s += arrow(860, 245, 860, 560, RED, 6) + ''.join(ion(x, y, 'K⁺', K) for x, y in [(850, 610), (910, 650)])
    s += f'<rect x="975" y="525" width="240" height="50" rx="25" fill="{LIGHT_YELLOW}" stroke="{ORANGE}" stroke-width="3"/>'
    s += text(1095, 558, 'АТФ → АДФ + Ф', 's', 'middle') + arrow(975, 540, 925, 505, ORANGE, 4)
    s += text(800, 760, 'За цикл: 3 Na⁺ — из клетки, 2 K⁺ — в клетку; против градиентов, энергия АТФ.'
              .replace('Na⁺', chem('Na⁺')).replace('K⁺', chem('K⁺')), 't', 'middle')
    return s


def enzyme_models() -> str:
    s = ''

    def body(cx: float, cy: float, notch: str) -> str:
        pockets = {
            'v': [(cx - 40, cy - 60), (cx, cy - 10), (cx + 40, cy - 60)],
            'flat': [(cx - 56, cy - 60), (cx - 36, cy - 28), (cx + 36, cy - 28), (cx + 56, cy - 60)],
            'grip': [(cx - 64, cy - 60), (cx - 64, cy - 104), (cx - 46, cy - 104), (cx - 40, cy - 60), (cx, cy - 10), (cx + 40, cy - 60),
                     (cx + 46, cy - 104), (cx + 64, cy - 104), (cx + 64, cy - 60)],
        }[notch]
        pts = [(cx - 130, cy - 60)] + pockets + [(cx + 130, cy - 60), (cx + 130, cy + 80), (cx - 130, cy + 80)]
        return (f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="5" stroke-linejoin="round"/>'
                + text(cx, cy + 45, 'фермент', 's', 'middle'))

    def substrate(cx: float, cy: float, part: str = 'whole') -> str:
        left = [(cx - 40, cy - 100), (cx, cy - 100), (cx, cy - 10), (cx - 40, cy - 60)]
        right = [(cx, cy - 100), (cx + 40, cy - 100), (cx + 40, cy - 60), (cx, cy - 10)]
        shapes = {'whole': [left[:1] + [(cx + 40, cy - 100), (cx + 40, cy - 60), (cx, cy - 10), (cx - 40, cy - 60)]],
                  'split': [[(x - 70, y - 90) for x, y in left], [(x + 70, y - 90) for x, y in right]]}[part]
        return ''.join(f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in sh)}" fill="{LIGHT_YELLOW}" stroke="{ORANGE}" '
                       f'stroke-width="4" stroke-linejoin="round"/>' for sh in shapes)

    rows = [(300, '«Ключ — замок» (Э. Фишер): активный центр жёсткий', ('v', 'v', 'v')),
            (690, 'Индуцированное соответствие (Кошланд): центр подстраивается', ('flat', 'grip', 'flat'))]
    caps = ['фермент + субстрат', 'фермент-субстратный комплекс', 'фермент + продукты']
    for cy, title, shapes in rows:
        s += text(60, cy - 215, title, 't')
        for k, cx in enumerate((280, 800, 1320)):
            s += body(cx, cy, shapes[k])
            if k == 0:
                s += substrate(cx, cy - 70) + text(cx + 70, cy - 150, 'субстрат', 'cap')
            elif k == 1:
                s += substrate(cx, cy)
            else:
                s += substrate(cx, cy, 'split') + text(cx, cy - 120, 'продукты', 'cap', 'middle')
            s += text(cx, cy + 125, caps[k], 's', 'middle')
            if k < 2:
                s += arrow(cx + 160, cy, cx + 360, cy, INK, 5)
    s += label(280, 265, 470, 225, 'активный центр', 'cap')
    s += text(800, 890, 'После реакции фермент освобождается и может работать снова.', 't', 'middle')
    return s


def activity_curve(points: list[tuple[float, float]], peak_x: float, xname: str, regions: tuple[str, str, str], title: str,
                   notes: list[tuple[float, float, str]], caption: str) -> str:
    s = text(800, 55, title, 'h', 'middle')
    ox, oy = 180, 560
    s += arrow(ox, oy, 1470, oy, INK, 4) + arrow(ox, oy, ox, 110, INK, 4)
    s += f'<text x="120" y="340" transform="rotate(-90 120 340)" text-anchor="middle" class="t">активность фермента</text>'
    s += text(1470, 535, xname, 't', 'end')
    s += f'<line x1="{peak_x}" y1="175" x2="{peak_x}" y2="{oy}" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
    s += f'<path d="{smooth(points)}" fill="none" stroke="{GREEN}" stroke-width="8" stroke-linecap="round"/>'
    peak_y = min(y for _, y in points)
    s += f'<circle cx="{peak_x}" cy="{peak_y}" r="10" fill="{RED}"/>' + text(peak_x, peak_y - 25, 'максимум', 's', 'middle')
    for x, name in zip(((ox + peak_x) / 2, peak_x, (peak_x + 1450) / 2), regions):
        s += text(x, 605, name, 's', 'middle', RED if name == 'оптимум' else None)
    s += ''.join(text(x, y, n, 'cap', 'middle') for x, y, n in notes)
    s += text(800, 680, caption, 't', 'middle')
    return s


def enzyme_temperature() -> str:
    pts = [(200, 545), (400, 505), (600, 410), (780, 260), (900, 185), (990, 245), (1080, 400), (1170, 540)]
    return activity_curve(pts, 900, 'температура', ('ниже оптимума', 'оптимум', 'выше оптимума'), 'Активность фермента и температура',
                          [(520, 330, 'активность растёт'), (1260, 330, 'белок денатурирует —'), (1260, 360, 'активность падает')],
                          'У каждого фермента свой оптимум; у ферментов человека — около температуры тела.')


def enzyme_ph() -> str:
    pts = [(220, 545), (450, 490), (650, 310), (800, 185), (950, 310), (1150, 490), (1380, 545)]
    return activity_curve(pts, 800, 'pH', ('кислее оптимума', 'оптимум', 'щелочнее оптимума'), 'Активность фермента и pH',
                          [(420, 380, 'ниже'), (1180, 380, 'ниже')],
                          'У каждого фермента свой оптимум pH; сдвиг в кислую или щелочную сторону снижает активность.')


if __name__ == '__main__':
    jobs = {
        'fluid-mosaic.png': (fluid_mosaic(), 1600, 780),
        'passive-transport.png': (passive_transport(), 1600, 750),
        'plant-osmosis.png': (plant_osmosis(), 1600, 760),
        'sodium-potassium-pump.png': (sodium_potassium_pump(), 1600, 790),
        'enzyme-models.png': (enzyme_models(), 1600, 920),
        'enzyme-temperature.png': (enzyme_temperature(), 1600, 710),
        'enzyme-ph.png': (enzyme_ph(), 1600, 710),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
