"""Рисунки недели 23 химии (course/week-23/pics/*.png): общий алгоритм, выбор модели, система для смеси,
стехиометрические схемы, масса раствора после реакции, кислая соль, олеум, таблица моделей.

Факты — по выжимке course/textbooks/chem-23-calculation-models.md (Х11-1 § 39; Х11-2 § 49–50; модели недель 4–22).
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w23.py
"""
from __future__ import annotations

import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    return _text(x, y, chem(s), cls, anchor, fill)

OUT = ROOT / 'course' / 'week-23' / 'pics'
BLUE, ORANGE, BROWN = '#3A57A7', '#D98A2B', '#8A5A2B'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32, color=color))


# 1. Алгоритм ----------------------------------------------------------------------------------------
def algorithm():
    s = text(900, 52, 'Расчётная задача: шесть шагов', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    steps = [('1', 'Уравнение|или схема', '#F7EFC8'), ('2', 'Всё в моль|n = m/M, V/22,4', '#fff'), ('3', 'Недостаток|(если два реагента)', '#fff'),
             ('4', 'Коэффициенты|к искомому', '#fff'), ('5', 'Величина|и выход η', '#fff'), ('6', 'Проверка|смысла', '#E2F1E6')]
    cols = [330, 900, 1470]
    for k, (n, lab, f) in enumerate(steps):
        c = cols[k] if k < 3 else cols[5 - k]
        y = 290 if k < 3 else 560
        s += f'<circle cx="{c - 230}" cy="{y}" r="36" fill="{RED}"/>' + text(c - 230, y + 12, n, 't', 'middle', '#fff')
        s += box(c + 20, y, 380, 120, lab, f, cls='t')
    s += arrow(540, 290, 628, 290, INK, 5) + arrow(1110, 290, 1198, 290, INK, 5)
    s += arrow(1490, 352, 1490, 498, INK, 5)
    s += arrow(1240 - 40, 560, 1110 + 4, 560, INK, 5) + arrow(670 - 40, 560, 540 + 4, 560, INK, 5)
    s += lines_at(900, 720, ['проверка: доля 0–100 %, выход ≤ 100 %, масса компонента меньше массы смеси, моль > 0',
                             'для раствора — сначала m(вещества) = ω · m(раствора); для руды — m(чистого) = ω · m(образца)'], 's', step=44, color=GREY)
    return s


# 2. Выбор модели -------------------------------------------------------------------------------------
def model_tree():
    s = text(900, 52, 'Какую модель выбрать', 'h', 'middle')
    s += card(30, 90, 1740, 800)
    s += box(900, 170, 480, 80, 'что дано в условии?', '#F7EFC8', cls='t')
    leaves = [('один реагент', 'прямой расчёт|по уравнению'), ('два реагента', 'избыток:|по недостатку'),
              ('смесь, общий|продукт', 'система:|масса + продукт'), ('цепочка|стадий', 'схема по элементу|× выходы'),
              ('раствор, газ|или осадок', 'масса раствора|− газ − осадок')]
    for k, (cond, model) in enumerate(leaves):
        x = 200 + k * 350
        s += arrow(900, 212, x, 320, GREY, 3)
        s += box(x, 380, 300, 100, cond, '#fff')
        s += arrow(x, 432, x, 520, INK, 4)
        s += box(x, 600, 320, 130, model, '#E2F1E6' if k in (2, 3) else '#DCEBF5', cls='t')
    s += text(900, 790, 'Кислая или средняя соль — по отношению количеств; олеум — SO₃ + H₂O → H₂SO₄', 's', 'middle', GREY)
    return s


# 3. Система для смеси -----------------------------------------------------------------------------
def mixture_system():
    s = text(900, 52, 'Смесь двух металлов: система', 'h', 'middle')
    s += card(30, 90, 860, 780) + card(910, 90, 860, 780)
    s += text(460, 150, 'Mg и Al + избыток HCl', 't', 'middle')
    s += box(250, 290, 280, 110, 'Mg|x моль', '#E3EEF7', cls='t') + box(670, 290, 280, 110, 'Al|y моль', '#F7EFC8', cls='t')
    s += arrow(250, 348, 250, 470, BLUE, 5) + arrow(670, 348, 670, 470, ORANGE, 5)
    s += text(270, 420, 'Mg → H₂', 's', 'start', BLUE) + text(690, 420, '2Al → 3H₂', 's', 'start', ORANGE)
    s += box(250, 530, 260, 90, 'x моль H₂', '#fff', cls='t') + box(670, 530, 260, 90, '1,5y моль H₂', '#fff', cls='t')
    s += text(460, 680, 'вместе — весь водород', 's', 'middle', GREY)
    s += text(1340, 150, 'Два уравнения', 't', 'middle')
    s += box(1340, 270, 760, 90, 'по массе:  24x + 27y = m(смеси)', '#FFF6E8', cls='t')
    s += box(1340, 400, 760, 90, 'по водороду:  x + 1,5y = n(H₂)', '#E2F1E6', cls='t')
    s += lines_at(1340, 520, ['пример: 10,2 г смеси, 0,5 моль H₂', 'x = 0,2 (Mg 4,8 г); y = 0,2 (Al 5,4 г)'], 't', step=46)
    s += lines_at(1340, 690, ['Al → 1,5 H₂; Mg, Fe, Zn → 1 H₂', 'Cu с HCl не реагирует — система не нужна', 'проверка: x > 0, y > 0, массы в сумме = m'], 's', step=40, color=RED)
    return s


# 4. Схемы и выход ------------------------------------------------------------------------------------
def stoich_schemes():
    s = text(900, 52, 'Стехиометрические схемы и выход по стадиям', 'h', 'middle')
    s += card(30, 90, 1740, 440) + card(30, 550, 1740, 360)
    rows = [('N₂', '2HNO₃', 'по азоту'), ('FeS₂', '2H₂SO₄', 'по сере'), ('Ca₃(PO₄)₂', '2P', 'по фосфору'), ('NH₃', 'HNO₃', 'по азоту')]
    for k, (a, b, c) in enumerate(rows):
        y = 170 + k * 95
        s += text(500, y, a, 'f', 'end') + arrow(530, y - 16, 760, y - 16, INK, 5) + text(800, y, b, 'f', 'start', RED)
        s += text(1300, y, c, 't', 'start', GREY)
    s += text(900, 505, 'элемент уравнивают: промежуточные вещества не считают', 's', 'middle')
    s += text(900, 610, 'Выход по стадиям', 't', 'middle')
    for k, (lab, eta) in enumerate((('сырьё', None), ('стадия 1', '90 %'), ('стадия 2', '80 %'), ('продукт', None))):
        x = 250 + k * 430
        s += box(x, 720, 260, 90, lab, '#F7EFC8' if k in (0, 3) else '#fff', cls='t')
        if eta:
            s += text(x, 800, f'η = {eta}', 's', 'middle', BLUE)
        if k < 3:
            s += arrow(x + 132, 720, x + 298, 720, INK, 4)
    s += text(900, 870, 'общий выход = 0,9 · 0,8 = 0,72 = 72 % — перемножаем, а не складываем', 't', 'middle', RED)
    return s


# 5. Масса раствора ----------------------------------------------------------------------------------
def beaker(cx, top, fill, h=240, w=200):
    return (f'<path d="M{cx - w / 2} {top} V {top + h} H {cx + w / 2} V {top}" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{cx - w / 2 + 4}" y="{top + 60}" width="{w - 8}" height="{h - 64}" fill="{fill}"/>')


def solution_mass():
    s = text(900, 52, 'Масса раствора после реакции', 'h', 'middle')
    s += card(30, 90, 1740, 780)
    s += beaker(220, 200, '#DCEBF5') + text(220, 490, 'раствор 1', 's', 'middle') + text(220, 530, 'm₁', 't', 'middle')
    s += text(410, 340, '+', 'f', 'middle')
    s += beaker(600, 200, '#FDE3E4') + text(600, 490, 'раствор 2', 's', 'middle') + text(600, 530, 'm₂', 't', 'middle')
    s += arrow(740, 330, 900, 330, INK, 6)
    s += beaker(1100, 200, '#E6D3EE')
    s += ''.join(f'<circle cx="{1060 + j * 25}" cy="{180 - j * 25}" r="10" fill="#fff" stroke="{INK}" stroke-width="2"/>' for j in range(3))
    s += text(1180, 140, 'газ ↑', 't', 'start', RED)
    s += f'<rect x="1010" y="410" width="180" height="26" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>' + text(1210, 430, 'осадок ↓', 't', 'start', RED)
    s += box(900, 650, 1300, 100, 'm(раствора) = m₁ + m₂ − m(газа) − m(осадка)', '#F7EFC8', cls='t')
    s += lines_at(900, 760, ['доля продукта — от конечной массы раствора; избыток реагента тоже остаётся в растворе',
                             'пример: 100 г + 100 г, ушло 4,4 г CO₂ → 195,6 г раствора'], 's', step=40)
    return s


# 6. Кислая соль -------------------------------------------------------------------------------------
def acid_salt():
    s = text(900, 52, 'Кислая или средняя соль: CO₂ и NaOH', 'h', 'middle')
    s += card(30, 90, 1740, 640)
    x0, x1, y = 200, 1600, 380
    s += f'<rect x="{x0}" y="{y - 30}" width="{(x1 - x0) / 2:.0f}" height="60" fill="#DCEBF5"/><rect x="{(x0 + x1) / 2:.0f}" y="{y - 30}" width="{(x1 - x0) / 2:.0f}" height="60" fill="#FFF6E8"/>'
    s += f'<line x1="{x0}" y1="{y + 30}" x2="{x1}" y2="{y + 30}" stroke="{INK}" stroke-width="3"/>'
    for v, lab in ((1, '1 : 1'), (1.5, '1,5 : 1'), (2, '2 : 1')):
        x = x0 + (v - 1) * (x1 - x0)
        s += f'<line x1="{x:.0f}" y1="{y - 50}" x2="{x:.0f}" y2="{y + 50}" stroke="{RED if v != 1.5 else GREY}" stroke-width="5"/>'
        s += text(x, y + 90, lab, 't', 'middle')
    s += text(x0, y - 70, 'NaHCO₃ — кислая', 't', 'middle', BLUE) + text(x1, y - 70, 'Na₂CO₃ — средняя', 't', 'middle', RED)
    s += text((x0 + x1) / 2, y - 70, 'смесь двух солей', 's', 'middle', GREY)
    s += text(900, 210, 'n(NaOH) : n(CO₂)', 't', 'middle')
    s += lines_at(900, 560, ['NaOH + CO₂ → NaHCO₃;  2NaOH + CO₂ → Na₂CO₃ + H₂O',
                             'соль выбирают по количествам веществ, а не по массам'], 's', step=44)
    return s


# 7. Олеум --------------------------------------------------------------------------------------------
def oleum():
    s = text(900, 52, 'Олеум и вода', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    s += box(330, 300, 440, 170, 'олеум|H₂SO₄ · SO₃|SO₃ в 100 %-й H₂SO₄', '#F7EFC8', cls='t')
    s += text(620, 315, '+', 'f', 'middle')
    s += box(860, 300, 300, 120, 'вода', '#DCEBF5', cls='t')
    s += arrow(1030, 300, 1200, 300, INK, 6)
    s += box(1440, 300, 420, 140, 'серная кислота|H₂SO₄', '#FDE3E4', cls='t')
    s += box(900, 540, 900, 90, 'SO₃ + H₂O → H₂SO₄:  80 г → 98 г', '#fff', cls='t')
    s += lines_at(900, 680, ['итог H₂SO₄ = кислота олеума + 98/80 · m(SO₃) + кислота исходного раствора',
                             'газа и осадка нет — масса раствора равна сумме масс'], 's', step=42)
    s += text(900, 800, 'пример: 0,1 моль H₂SO₄ · SO₃ даёт 0,2 моль H₂SO₄', 's', 'middle', RED)
    return s


# 8. Таблица моделей -------------------------------------------------------------------------------
def models_table():
    s = text(900, 52, 'Модели расчётов курса и типичные ошибки', 'h', 'middle')
    s += card(30, 90, 1120, 900) + card(1170, 90, 600, 900)
    rows = [('Газы при н. у.', 'V = 22,4 · n; D = M₁ : M₂', '4'), ('Газы не при н. у.', 'pV = nRT, T в К', '11'),
            ('Растворы', 'ω = m(в-ва) : m(р-ра)', '5'), ('Примеси, выход', 'ω · m(обр.); η = практ. : теор.', '5'),
            ('Избыток', 'по недостатку', '5'), ('Электролиз', 'по уравнению: Cu и O₂', '10'),
            ('Тепловой эффект', 'Q пропорционален n', '11'), ('Скорость', 'Вант-Гофф: γ^(Δt/10)', '11'),
            ('Равновесие', 'стало = было − прореагировало', '12'), ('Формула', 'ω, горение, плотность', '17, 22')]
    s += text(270, 150, 'модель', 's', 'middle', GREY) + text(700, 150, 'правило', 's', 'middle', GREY) + text(1060, 150, 'нед.', 's', 'middle', GREY)
    for k, (a, b, c) in enumerate(rows):
        y = 215 + k * 76
        s += f'<rect x="60" y="{y - 32}" width="1060" height="66" rx="10" fill="{"#fff" if k % 2 else "#F7F5EF"}"/>'
        s += text(270, y + 10, a, 's', 'middle') + text(700, y + 10, b, 's', 'middle', BLUE) + text(1060, y + 10, c, 's', 'middle', GREY)
    s += text(1470, 160, 'Типичные ошибки', 't', 'middle', RED)
    traps = ['считать по избытку', 'забыть коэффициент|(2Al → 3H₂, FeS₂ → 2H₂SO₄)', 'масса воды вместо раствора',
             'не вычесть газ или осадок', 'сложить выходы', 'градусы вместо кельвинов', 'не проверить смысл']
    for k, t in enumerate(traps):
        y = 250 + k * 105
        s += f'<circle cx="1220" cy="{y - 8}" r="12" fill="{RED}"/>' + lines_at(1245, y, t.split('|'), 's', 'start', step=30)
    return s


if __name__ == '__main__':
    jobs = {
        'algorithm.png': (algorithm(), 1800, 880),
        'model-tree.png': (model_tree(), 1800, 920),
        'mixture-system.png': (mixture_system(), 1800, 900),
        'stoich-schemes.png': (stoich_schemes(), 1800, 940),
        'solution-mass.png': (solution_mass(), 1800, 900),
        'acid-salt.png': (acid_salt(), 1800, 760),
        'oleum.png': (oleum(), 1800, 880),
        'models-table.png': (models_table(), 1800, 1020),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
