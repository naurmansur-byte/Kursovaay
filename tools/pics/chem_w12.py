"""Рисунки недели 12 химии (course/week-12/pics/*.png): скорости прямой и обратной реакции до равновесия,
динамическое равновесие на частицах, выражения константы, факторы Ле Шателье, давление и число молей газов,
условия синтеза аммиака, опыт с тиоцианатом железа(III).

Факты — по выжимке course/textbooks/chem-12-equilibrium.md (Х9-1 § 17–18; Х10-1 § 39–42). Схемы условные, без чисел из учебника.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w12.py
"""
from __future__ import annotations

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-12' / 'pics'
BLUE, PURPLE, ORANGE = '#3A57A7', '#7B4FA0', '#D98A2B'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER, stroke=None):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"{st}/>'


# 1. Скорости до равновесия ---------------------------------------------------------------------
def rate_equilibrium() -> str:
    s = text(700, 50, 'Как устанавливается химическое равновесие', 'h', 'middle')
    x0, y0, w, h = 140, 110, 1080, 460
    s += arrow(x0, y0 + h, x0, y0, INK, 4) + arrow(x0, y0 + h, x0 + w, y0 + h, INK, 4)
    s += text(x0 + 14, y0 + 8, 'скорость v', 'cap') + text(x0 + w, y0 + h + 38, 'время', 'cap', 'end')
    teq, veq = x0 + 520, y0 + 250
    s += (f'<path d="M{x0} {y0 + 40} C {x0 + 180} {y0 + 120} {x0 + 360} {veq - 6} {teq} {veq} H {x0 + w - 40}" '
          f'fill="none" stroke="{RED}" stroke-width="7"/>')
    s += (f'<path d="M{x0} {y0 + h} C {x0 + 180} {y0 + h - 100} {x0 + 360} {veq + 6} {teq} {veq}" '
          f'fill="none" stroke="{BLUE}" stroke-width="7" stroke-dasharray="18 10"/>')
    s += f'<path d="M{teq} {y0 + 10} V {y0 + h}" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 8"/>'
    s += text(x0 + 110, y0 + 90, 'v прямой', 't', 'start', RED)
    s += text(x0 + 220, y0 + h - 40, 'v обратной', 't', 'start', BLUE)
    s += text(teq + 20, y0 + 40, 'равновесие', 't', 'start', INK)
    s += text(teq + 20, y0 + 76, 'установилось', 's', 'start')
    s += text(x0 + w - 60, veq - 24, 'v пр = v обр ≠ 0', 't', 'end', GREEN)
    s += text(x0 + 30, y0 + h + 38, 'сначала только реагенты', 'cap')
    s += text(700, 650, 'Реакции не останавливаются: обе идут с равными скоростями, состав смеси больше не меняется.', 's', 'middle')
    return s


# 2. Динамическое равновесие на частицах -------------------------------------------------------
def h2(cx, cy):
    return (f'<circle cx="{cx - 13}" cy="{cy}" r="14" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{cx + 13}" cy="{cy}" r="14" fill="#fff" stroke="{INK}" stroke-width="2"/>')


def i2(cx, cy):
    return (f'<circle cx="{cx - 20}" cy="{cy}" r="21" fill="{PURPLE}"/>'
            f'<circle cx="{cx + 20}" cy="{cy}" r="21" fill="{PURPLE}"/>')


def hi(cx, cy):
    return (f'<circle cx="{cx - 17}" cy="{cy}" r="14" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{cx + 12}" cy="{cy}" r="21" fill="{PURPLE}"/>')


def vessel(x, y, title, mols, note):
    s = card(x, y, 600, 360, '#fff', INK)
    s += text(x + 300, y - 18, title, 't', 'middle')
    for kind, cx, cy in mols:
        s += {'h2': h2, 'i2': i2, 'hi': hi}[kind](x + cx, y + cy)
    s += text(x + 300, y + 410, chem(note), 's', 'middle')
    return s


def dynamic_particles() -> str:
    s = text(760, 50, chem('Равновесие динамическое: H₂ + I₂ ⇄ 2HI'), 'h', 'middle')
    a = [('h2', 90, 70), ('h2', 420, 120), ('h2', 250, 290), ('i2', 230, 80), ('i2', 500, 260), ('i2', 110, 210),
         ('hi', 350, 200), ('hi', 520, 60), ('hi', 90, 310), ('hi', 420, 320)]
    b = [('h2', 300, 60), ('h2', 110, 150), ('h2', 480, 300), ('i2', 470, 160), ('i2', 120, 300), ('i2', 300, 300),
         ('hi', 230, 190), ('hi', 520, 70), ('hi', 120, 60), ('hi', 380, 230)]
    s += vessel(90, 120, 'момент 1', a, '3 H₂ · 3 I₂ · 4 HI')
    s += vessel(830, 120, 'момент 2 (позже)', b, '3 H₂ · 3 I₂ · 4 HI')
    s += arrow(712, 300, 812, 300, GREY, 5)
    s += text(762, 270, 'время', 'cap', 'middle')
    s += text(760, 640, 'За это время часть HI распалась и столько же HI образовалось — общий состав не изменился.', 's', 'middle')
    s += text(760, 680, 'Числа частиц разных веществ при равновесии не обязаны быть равными.', 'cap', 'middle')
    return s


# 3. Выражения константы равновесия ------------------------------------------------------------
def fraction(cx, y, num, den, color=INK):
    return (text(cx, y, chem(num), 't', 'middle', color)
            + f'<line x1="{cx - 150}" y1="{y + 18}" x2="{cx + 150}" y2="{y + 18}" stroke="{color}" stroke-width="3"/>'
            + text(cx, y + 58, chem(den), 't', 'middle', color))


def equilibrium_constant() -> str:
    s = text(760, 50, 'Константа равновесия K: коэффициенты — в степени', 'h', 'middle')
    s += card(40, 100, 700, 430) + card(780, 100, 700, 430)
    s += text(390, 150, 'гомогенная (все — газы)', 't', 'middle', BLUE)
    s += text(390, 220, chem('H₂(г) + I₂(г) ⇄ 2HI(г)'), 't', 'middle')
    s += text(170, 330, 'K =', 't', 'middle') + fraction(400, 310, '[HI]²', '[H₂] · [I₂]')
    s += text(390, 460, 'коэффициент 2 → квадрат', 's', 'middle', RED)
    s += text(1130, 150, 'гетерогенная (есть твёрдое)', 't', 'middle', BLUE)
    s += (text(1130, 220, chem('<tspan style="fill:#8F897F">C(тв)</tspan> + CO₂(г) ⇄ 2CO(г)'), 't', 'middle'))
    s += text(910, 330, 'K =', 't', 'middle') + fraction(1140, 310, '[CO]²', '[CO₂]')
    s += lines_at(1130, 450, ['твёрдый углерод в выражение K', 'не входит'], 's', step=32, color=RED)
    s += text(760, 585, 'K зависит от температуры; катализатор и концентрации её не меняют.', 's', 'middle')
    return s


# 4. Факторы Ле Шателье -----------------------------------------------------------------------
def le_chatelier_factors() -> str:
    s = text(800, 50, 'Принцип Ле Шателье: система ослабляет воздействие', 'h', 'middle')
    cols = (60, 420, 900)
    s += card(40, 90, 1520, 70, INK)
    for x, t in zip(cols, ('фактор', 'воздействие', 'куда смещается равновесие')):
        s += text(x, 135, t, 'w')
    rows = [
        ('концентрация', 'добавили вещество', 'в сторону его расхода', RED),
        ('', 'удалили вещество', 'в сторону его образования', RED),
        ('давление', 'сжатие (p ↑), T = const', 'к меньшему числу молей газов', BLUE),
        ('(газы)', 'расширение (p ↓)', 'к большему числу молей газов', BLUE),
        ('температура', 'нагревание', 'в сторону эндотермической (ΔH &gt; 0)', ORANGE),
        ('', 'охлаждение', 'в сторону экзотермической (ΔH &lt; 0)', ORANGE),
        ('катализатор', 'добавили', 'не смещается — равновесие наступает быстрее', GREEN),
    ]
    for j, (f, a, r, col) in enumerate(rows):
        y = 170 + j * 74
        if j % 2 == 0:
            s += f'<rect x="40" y="{y}" width="1520" height="74" fill="{PAPER}"/>'
        s += text(cols[0], y + 48, f, 't', 'start', col) + text(cols[1], y + 48, a, 's') + text(cols[2], y + 48, r, 's')
    s += text(800, 720, 'Давление учитывает только газы; если моли газов слева и справа равны — сдвига нет.', 'cap', 'middle')
    return s


# 5. Давление и число молей газов ---------------------------------------------------------------
def piston(x, y, n_left, n_right, eq, verdict, col):
    s = card(x, y, 680, 460)
    s += text(x + 340, y + 50, chem(eq), 't', 'middle')
    s += text(x + 340, y + 100, f'газов: {n_left} моль → {n_right} моль', 's', 'middle')
    cx, cy = x + 170, y + 150
    s += f'<rect x="{cx}" y="{cy}" width="340" height="200" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    s += f'<rect x="{cx + 4}" y="{cy + 40}" width="332" height="16" fill="{GREY}"/>'
    s += f'<line x1="{cx + 170}" y1="{cy + 40}" x2="{cx + 170}" y2="{cy - 40}" stroke="{GREY}" stroke-width="10"/>'
    s += arrow(cx + 250, cy - 50, cx + 250, cy + 30, RED, 5)
    s += text(cx + 270, cy - 20, 'сжатие', 's', 'start', RED)
    for k in range(10):
        s += f'<circle cx="{cx + 40 + (k % 5) * 64}" cy="{cy + 95 + (k // 5) * 60}" r="13" fill="{BLUE if k % 3 else PURPLE}"/>'
    s += text(x + 340, y + 420, chem(verdict), 't', 'middle', col)
    return s


def pressure_gases() -> str:
    s = text(760, 50, 'Сжатие газов (T = const): считаем моли газов', 'h', 'middle')
    s += piston(40, 100, '1 + 3 = 4', '2', 'N₂ + 3H₂ ⇄ 2NH₃', 'смещение вправо (к NH₃)', GREEN)
    s += piston(800, 100, '1 + 1 = 2', '2', 'N₂ + O₂ ⇄ 2NO', 'равновесие не смещается', GREY)
    s += text(760, 610, 'Твёрдые вещества и жидкости в подсчёт молей газа не входят.', 's', 'middle')
    return s


# 6. Условия синтеза аммиака -------------------------------------------------------------------
def ammonia_conditions() -> str:
    s = text(800, 50, 'Синтез аммиака: условия и зачем они', 'h', 'middle')
    s += card(500, 300, 600, 150, '#fff', INK)
    s += text(800, 365, chem('N₂(г) + 3H₂(г) ⇄ 2NH₃(г)'), 't', 'middle')
    s += text(800, 410, chem('ΔH = −92 кДж (экзотермическая)'), 's', 'middle', RED)
    boxes = [
        (40, 100, 'давление 15–100 МПа', ['газов 4 моль → 2 моль:', 'сжатие смещает к NH₃'], BLUE),
        (1110, 100, '450–500 °C', ['ниже — выход больше,', 'но реакция идёт медленно'], ORANGE),
        (40, 520, 'катализатор Fe', ['с оксидами K и Al;', 'ускоряет, не смещает'], GREEN),
        (1110, 520, 'N₂ : H₂ = 1 : 3', ['газы очищают от примесей,', 'отравляющих катализатор'], INK),
    ]
    for x, y, t, rows, col in boxes:
        s += card(x, y, 450, 170, PAPER, col)
        s += text(x + 225, y + 50, chem(t), 't', 'middle', col) + lines_at(x + 225, y + 100, rows, 's', step=32)
    s += arrow(490, 230, 560, 300, GREY, 4) + arrow(1110, 230, 1040, 300, GREY, 4)
    s += arrow(490, 560, 560, 450, GREY, 4) + arrow(1110, 560, 1040, 450, GREY, 4)
    s += text(800, 750, 'Температура — компромисс между скоростью и равновесным выходом.', 's', 'middle')
    return s


# 7. Опыт с тиоцианатом железа(III) ------------------------------------------------------------
def beaker(x, y, fill, title, note):
    s = (f'<path d="M{x} {y} V {y + 220} Q {x} {y + 250} {x + 30} {y + 250} H {x + 190} Q {x + 220} {y + 250} {x + 220} {y + 220} V {y}" '
         f'fill="none" stroke="{INK}" stroke-width="4"/>')
    s += (f'<path d="M{x + 4} {y + 70} V {y + 220} Q {x + 4} {y + 246} {x + 30} {y + 246} H {x + 190} Q {x + 216} {y + 246} {x + 216} {y + 220} V {y + 70} Z" '
          f'fill="{fill}"/>')
    s += text(x + 110, y - 24, chem(title), 't', 'middle')
    s += text(x + 110, y + 296, chem(note), 's', 'middle')
    return s


def thiocyanate_experiment() -> str:
    s = text(800, 50, 'Опыт: смещение равновесия видно по окраске', 'h', 'middle')
    s += text(800, 105, chem('FeCl₃ + 3KSCN ⇄ Fe(SCN)₃ + 3KCl  (упрощённая запись)'), 't', 'middle')
    data = [('контроль', '#C8262E', 'исходная смесь'), ('+ FeCl₃', '#8E1018', 'краснее'),
            ('+ KSCN', '#8E1018', 'краснее'), ('+ KCl', '#EE9A9E', 'светлее')]
    for k, (t, f, n) in enumerate(data):
        s += beaker(130 + k * 360, 190, f, t, n)
    s += text(800, 590, chem('Красный цвет создают комплексы железа(III) с тиоцианат-ионами SCN⁻.'), 's', 'middle')
    s += text(800, 630, 'Ослабление от KCl — результат в условиях этого учебного опыта.', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'rate-equilibrium.png': (rate_equilibrium(), 1400, 690),
        'dynamic-particles.png': (dynamic_particles(), 1520, 710),
        'equilibrium-constant.png': (equilibrium_constant(), 1520, 620),
        'le-chatelier-factors.png': (le_chatelier_factors(), 1600, 750),
        'pressure-gases.png': (pressure_gases(), 1520, 650),
        'ammonia-conditions.png': (ammonia_conditions(), 1600, 780),
        'thiocyanate-experiment.png': (thiocyanate_experiment(), 1600, 660),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
