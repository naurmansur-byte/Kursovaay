"""Рисунки недели 11 химии (course/week-11/pics/*.png): экзо- и эндотермический процесс, закон Гесса, концентрация во времени,
факторы скорости, правило Вант-Гоффа, энергия активации и катализатор, гомогенный и гетерогенный катализ.

Факты — по выжимке course/textbooks/chem-11-thermo-kinetics.md (Х8 § 22–23; Х9-1 § 14–16; Х10-1 § 28–38). Схемы условные, без чисел из учебника.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w11.py
"""
from __future__ import annotations

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-11' / 'pics'
BLUE, WATER, ORANGE = '#3A57A7', '#E4EEF8', '#D98A2B'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def axes(x0, y0, w, h, ylab='энергия', xlab='путь реакции'):
    s = arrow(x0, y0 + h, x0, y0, INK, 4) + arrow(x0, y0 + h, x0 + w, y0 + h, INK, 4)
    s += text(x0 + 12, y0 + 6, ylab, 'cap') + text(x0 + w, y0 + h + 36, xlab, 'cap', 'end')
    return s


def hump(x0, yr, xa, xm, peak, xb, yp, x1, color, w=6, dash=''):
    d = (f'M{x0} {yr} H {xa} C {xa + 70} {yr} {xm - 70} {peak} {xm} {peak} '
         f'C {xm + 70} {peak} {xb - 70} {yp} {xb} {yp} H {x1}')
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da}/>'


def dim(x, y1, y2, color, label, side='end'):
    """Вертикальная стрелка-размер от y1 к y2 с подписью."""
    s = arrow(x, y1, x, y2, color, 4)
    tx = x - 14 if side == 'end' else x + 14
    return s + text(tx, (y1 + y2) / 2 + 9, chem(label), 't', side, color)


# 1. Экзо- и эндотермический процесс -------------------------------------------------------------
def exo_endo() -> str:
    s = text(820, 50, 'Тепловой эффект: экзо- и эндотермический процесс', 'h', 'middle')
    for k, (title, yr, yp, col, sign, note) in enumerate((
            ('экзотермический', 300, 470, RED, 'ΔH &lt; 0', 'теплота выделяется в окружающую среду'),
            ('эндотермический', 470, 300, BLUE, 'ΔH &gt; 0', 'теплота поглощается из окружающей среды'))):
        x0 = 110 + k * 780
        s += text(x0 + 330, 110, title, 't', 'middle', col)
        s += axes(x0, 140, 700, 440)
        s += hump(x0 + 20, yr, x0 + 170, x0 + 320, 200, x0 + 470, yp, x0 + 620, col)
        s += text(x0 + 95, yr - 16, 'реагенты', 's', 'middle') + text(x0 + 545, yp - 16, 'продукты', 's', 'middle')
        s += f'<path d="M{x0 + 470} {yr} H {x0 + 670}" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 6"/>'
        s += dim(x0 + 665, yr, yp, col, sign)
        s += text(x0 + 330, 660, note, 'cap', 'middle')
    s += text(820, 710, 'По вертикали — энергия веществ, не температура. Знак ΔH противоположен знаку Q в записи «+Q».', 's', 'middle')
    return s


# 2. Закон Гесса --------------------------------------------------------------------------------
def box(x, y, w, h, label, fill):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
            + text(x + w / 2, y + h / 2 + 10, chem(label), 't', 'middle'))


def hess_cycle() -> str:
    s = text(700, 50, 'Закон Гесса: результат не зависит от пути', 'h', 'middle')
    s += box(80, 110, 360, 80, 'C(графит) + O₂', PAPER) + box(960, 110, 360, 80, 'CO₂', PAPER)
    s += box(520, 350, 360, 80, 'CO + ½O₂', '#FFF6DE')
    s += arrow(450, 150, 950, 150, RED, 6) + text(700, 132, chem('ΔH — прямой путь: C + O₂ → CO₂'), 's', 'middle', RED)
    s += arrow(300, 200, 560, 340, BLUE, 6) + text(300, 300, chem('ΔH₁: C + ½O₂ → CO'), 's', 'middle', BLUE)
    s += arrow(840, 340, 1100, 200, BLUE, 6) + text(1110, 300, chem('ΔH₂: CO + ½O₂ → CO₂'), 's', 'middle', BLUE)
    s += f'<rect x="420" y="470" width="560" height="70" rx="14" fill="#fff" stroke="{RED}" stroke-width="3"/>'
    s += text(700, 515, chem('ΔH = ΔH₁ + ΔH₂'), 't', 'middle', RED)
    s += text(700, 580, 'Одинаковы начальное и конечное состояния — одинаков и тепловой эффект.', 'cap', 'middle')
    return s


# 3. Концентрация реагента во времени --------------------------------------------------------------
def concentration_time() -> str:
    s = text(650, 50, 'Скорость реакции по изменению концентрации', 'h', 'middle')
    x0, y0, w, h = 140, 110, 760, 440
    s += axes(x0, y0, w, h, 'c реагента, моль/л', 'время t, с')
    pts = [(x0 + 10, y0 + 40), (x0 + 200, y0 + 170), (x0 + 400, y0 + 270), (x0 + 600, y0 + 330), (x0 + 740, y0 + 360)]
    d = f'M{pts[0][0]} {pts[0][1]} C {x0 + 90} {y0 + 110} {x0 + 140} {y0 + 140} {pts[1][0]} {pts[1][1]} ' \
        f'S {x0 + 330} {y0 + 250} {pts[2][0]} {pts[2][1]} S {x0 + 540} {y0 + 320} {pts[3][0]} {pts[3][1]} S {x0 + 700} {y0 + 356} {pts[4][0]} {pts[4][1]}'
    s += f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="6"/>'
    (ax, ay), (bx, by) = pts[1], pts[3]
    m = (by - ay) / (bx - ax)
    s += f'<path d="M{ax - 80} {ay - 80 * m:.0f} L {bx + 80} {by + 80 * m:.0f}" stroke="{RED}" stroke-width="3" stroke-dasharray="10 8"/>'
    for (px, py), n in (((ax, ay), '1'), ((bx, by), '2')):
        s += f'<path d="M{px} {py} V {y0 + h} M{px} {py} H {x0}" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 6"/>'
        s += f'<circle cx="{px}" cy="{py}" r="10" fill="{RED}"/>'
        s += text(px, y0 + h + 34, chem('t₁' if n == '1' else 't₂'), 's', 'middle')
        s += text(x0 - 14, py + 9, chem('c₁' if n == '1' else 'c₂'), 's', 'end')
    s += arrow(ax, y0 + h + 60, bx, y0 + h + 60, INK, 3) + text((ax + bx) / 2, y0 + h + 92, chem('Δt = t₂ − t₁'), 'cap', 'middle')
    s += dim(bx + 40, ay, by, RED, 'Δc = c₂ − c₁ &lt; 0', 'start')
    s += f'<rect x="1000" y="110" width="380" height="190" rx="16" fill="{PAPER}"/>'
    s += lines_at(1190, 160, ['для убывающего реагента', 'v = −Δc / Δt', 'v &gt; 0, моль/(л·с)'], 't', step=48)
    return s


# 4. Факторы скорости ----------------------------------------------------------------------------
def tube(x, y, liquid, solid=None, bubbles=0, hot=False):
    s = ''
    if hot:
        s += ''.join(f'<path d="M{x + 10 + 22 * k} {y + 300} q -10 -18 0 -36 q 10 -18 0 -36" fill="none" stroke="{ORANGE}" stroke-width="4"/>' for k in range(3))
    s += f'<path d="M{x} {y} V {y + 200} Q {x + 35} {y + 240} {x + 70} {y + 200} V {y}" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    s += f'<path d="M{x + 3} {y + 80} V {y + 200} Q {x + 35} {y + 236} {x + 67} {y + 200} V {y + 80} Z" fill="{liquid}"/>'
    if solid == 'piece':
        s += f'<rect x="{x + 20}" y="{y + 175}" width="30" height="24" rx="4" fill="#E9E5DC" stroke="{GREY}" stroke-width="2"/>'
    elif solid == 'powder':
        s += ''.join(f'<circle cx="{x + 14 + (k % 6) * 8}" cy="{y + 205 - (k // 6) * 7}" r="3.5" fill="#CFC9BD"/>' for k in range(18))
    elif solid == 'metal':
        s += f'<rect x="{x + 22}" y="{y + 150}" width="26" height="50" rx="3" fill="#A7AEB6" stroke="{GREY}" stroke-width="2"/>'
    for k in range(bubbles):
        bx = x + 14 + (k * 17) % 44
        by = y + 190 - (k * 23) % 105
        s += f'<circle cx="{bx}" cy="{by}" r="5" fill="#fff" stroke="{BLUE}" stroke-width="2"/>'
    return s


def rate_factors() -> str:
    s = text(800, 50, 'Что ускоряет реакцию: меняем один фактор', 'h', 'middle')
    acid, acid2 = '#DCEBF5', '#A9CBE8'
    panels = [
        ('природа вещества', [('Zn', acid, 'metal', 3, False), ('Mg', acid, 'metal', 10, False)], 'металл, HCl одинаковая'),
        ('концентрация', [('разбавл.', acid, 'metal', 3, False), ('концентр.', acid2, 'metal', 10, False)], 'кислота разной концентрации'),
        ('поверхность', [('кусок', acid, 'piece', 3, False), ('порошок', acid, 'powder', 10, False)], 'мел равной массы + HCl'),
        ('температура', [('холодная', acid, 'metal', 3, False), ('нагретая', acid, 'metal', 10, True)], 'та же смесь'),
    ]
    for k, (title, pair, note) in enumerate(panels):
        x = 40 + k * 390
        s += f'<rect x="{x}" y="90" width="370" height="520" rx="18" fill="{PAPER}"/>'
        s += text(x + 185, 135, title, 't', 'middle')
        for j, (lab, liq, solid, bub, hot) in enumerate(pair):
            tx = x + 70 + j * 160
            s += tube(tx, 190, liq, solid, bub, hot)
            s += text(tx + 35, 545, chem(lab), 's', 'middle', RED if j else INK)
        s += text(x + 255, 180, 'быстрее', 'cap', 'middle', RED)
        s += text(x + 185, 590, note, 'cap', 'middle')
    s += text(800, 660, 'Остальные условия в каждой паре одинаковы; быстрее там, где больше пузырьков газа за то же время.', 's', 'middle')
    return s


# 5. Правило Вант-Гоффа --------------------------------------------------------------------------
def vanthoff() -> str:
    s = text(700, 50, 'Правило Вант-Гоффа: каждые 10 °C — в γ раз', 'h', 'middle')
    x0, base = 160, 560
    vals = [1, 2, 4, 8]
    for k, v in enumerate(vals):
        x = x0 + k * 220
        hgt = v * 50
        s += f'<rect x="{x}" y="{base - hgt}" width="130" height="{hgt}" rx="8" fill="{RED if k == 3 else "#F6B9B4"}"/>'
        s += text(x + 65, base - hgt - 14, f'v × {v}' if v > 1 else 'v', 't', 'middle')
        s += text(x + 65, base + 36, 't' if k == 0 else f't + {10 * k} °C', 's', 'middle')
        if k:
            s += f'<rect x="{x - 78}" y="{base - 44}" width="66" height="34" rx="17" fill="#E6EEF8"/>' + text(x - 45, base - 19, '× 2', 's', 'middle', BLUE)
    s += f'<path d="M{x0 - 20} {base} H {x0 + 3 * 220 + 160}" stroke="{INK}" stroke-width="4"/>'
    s += f'<rect x="1040" y="140" width="330" height="230" rx="16" fill="{PAPER}"/>'
    s += lines_at(1205, 190, ['γ = 2 (дано)', 'v₂/v₁ = γ<tspan baseline-shift="0.6em" font-size="68%">Δt/10</tspan>', '+30 °C: 2³ = 8,', 'а не 2 · 3 = 6'], 's', step=44)
    s += text(700, 640, 'Охлаждение — в обратную сторону: на каждые 10 °C скорость уменьшается в γ раз.', 's', 'middle')
    return s


# 6. Энергия активации и катализатор -------------------------------------------------------------
def activation_catalyst() -> str:
    s = text(700, 50, 'Катализатор снижает энергию активации', 'h', 'middle')
    x0, y0 = 140, 100
    s += axes(x0, y0, 880, 480)
    yr, yp = 400, 500
    s += hump(x0 + 20, yr, x0 + 180, x0 + 400, 150, x0 + 620, yp, x0 + 800, RED)
    s += hump(x0 + 20, yr, x0 + 180, x0 + 400, 290, x0 + 620, yp, x0 + 800, GREEN, 6, '14 8')
    s += text(x0 + 100, yr - 16, 'реагенты', 's', 'middle') + text(x0 + 710, yp - 16, 'продукты', 's', 'middle')
    s += f'<path d="M{x0 + 180} {yr} H {x0 + 440}" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 6"/>'
    s += dim(x0 + 412, yr, 158, RED, 'Eₐ', 'start')
    s += dim(x0 + 372, yr, 298, GREEN, 'Eₐ', 'end')
    s += f'<path d="M{x0 + 620} {yr} H {x0 + 860}" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 6"/>'
    s += dim(x0 + 850, yr, yp, INK, 'ΔH')
    s += f'<rect x="1060" y="130" width="360" height="330" rx="16" fill="{PAPER}"/>'
    s += f'<path d="M1085 175 H 1135" stroke="{RED}" stroke-width="6"/>' + text(1150, 184, 'без катализатора', 's')
    s += f'<path d="M1085 225 H 1135" stroke="{GREEN}" stroke-width="6" stroke-dasharray="14 8"/>' + text(1150, 234, 'с катализатором', 's')
    s += lines_at(1240, 300, ['ΔH не меняется:', 'уровни те же', 'катализатор', 'не расходуется'], 's', step=40)
    s += text(700, 670, 'Меньше барьер — больше частиц преодолевают его — реакция быстрее.', 's', 'middle')
    return s


# 7. Гомогенный и гетерогенный катализ -----------------------------------------------------------
def molecule(x, y, label, col):
    return f'<circle cx="{x}" cy="{y}" r="30" fill="#fff" stroke="{col}" stroke-width="3"/>' + text(x, y + 8, chem(label), 'cap', 'middle', col)


def catalysis_types() -> str:
    s = text(800, 50, 'Гомогенный и гетерогенный катализ', 'h', 'middle')
    # гомогенный
    s += text(400, 110, 'гомогенный — одна фаза', 't', 'middle', BLUE)
    s += f'<rect x="120" y="140" width="560" height="360" rx="30" fill="#F2F6FB" stroke="{BLUE}" stroke-width="4"/>'
    for x, y, lab, col in ((210, 220, 'SO₂', INK), (340, 300, 'O₂', INK), (480, 220, 'NO₂', RED), (590, 330, 'SO₂', INK),
                           (230, 400, 'O₂', INK), (420, 420, 'NO₂', RED)):
        s += molecule(x, y, lab, col)
    s += text(400, 545, chem('все вещества — газы, катализатор NO₂ тоже газ'), 'cap', 'middle')
    # гетерогенный
    s += text(1200, 110, 'гетерогенный — разные фазы', 't', 'middle', GREEN)
    bx = 960
    s += f'<path d="M{bx} 150 V 480 Q {bx} 500 {bx + 20} 500 H {bx + 460} Q {bx + 480} 500 {bx + 480} 480 V 150" fill="none" stroke="{INK}" stroke-width="5"/>'
    s += f'<rect x="{bx + 4}" y="250" width="472" height="246" fill="{WATER}"/>'
    s += text(bx + 240, 285, chem('раствор H₂O₂'), 's', 'middle', BLUE)
    s += ''.join(f'<circle cx="{bx + 120 + (k % 14) * 17}" cy="{490 - (k // 14) * 9}" r="6" fill="#4A4038"/>' for k in range(28))
    s += text(bx + 240, 450, chem('MnO₂ — твёрдый'), 's', 'middle')
    for k in range(9):
        cx = bx + 130 + (k * 53) % 230
        cy = 330 + (k * 29) % 85
        s += f'<circle cx="{cx}" cy="{cy}" r="8" fill="#fff" stroke="{BLUE}" stroke-width="2"/>'
    s += text(bx + 240, 200, chem('O₂ ↑'), 't', 'middle', BLUE)
    s += text(1200, 545, chem('ещё пример: NH₃ + O₂ на твёрдой платине'), 'cap', 'middle')
    s += text(800, 620, 'Признак — фаза катализатора по сравнению с фазой реагентов.', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'exo-endo.png': (exo_endo(), 1650, 740),
        'hess-cycle.png': (hess_cycle(), 1400, 610),
        'concentration-time.png': (concentration_time(), 1420, 700),
        'rate-factors.png': (rate_factors(), 1600, 690),
        'vanthoff.png': (vanthoff(), 1420, 680),
        'activation-catalyst.png': (activation_catalyst(), 1460, 710),
        'catalysis-types.png': (catalysis_types(), 1600, 660),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
