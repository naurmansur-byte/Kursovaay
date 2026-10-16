"""Рисунки недели 9 химии (course/week-09/pics/*.png): шкала степеней окисления, перенос электронов, электронный баланс,
роли серы, типы ОВР, перманганат в разных средах.

Факты — по выжимке course/textbooks/chem-09-redox.md (Х9-1 § 19–20, Х10-1 § 43–46). Схемы условные.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w09.py
"""
from __future__ import annotations

from common import GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-09' / 'pics'
BLUE, VIOLET, GREEN = '#3A57A7', '#9B2D8E', '#1F7A4A'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, chem(r), cls, anchor, color) for j, r in enumerate(rows))


def arc(x1, x2, y, up, color, h=70):
    """Дуга-стрелка над (up) или под осью от x1 к x2."""
    cy = y - h if up else y + h
    mid = (x1 + x2) / 2
    d = 1 if x2 > x1 else -1
    head = f'{x2},{y - 6 if up else y + 6} {x2 - d * 22},{y - 24 if up else y + 24} {x2 + d * 4},{y - 30 if up else y + 30}'
    return (f'<path d="M{x1} {y - 6 if up else y + 6} Q {mid} {cy - (h if up else -h) * 0.6} {x2} {y - 8 if up else y + 8}" fill="none" stroke="{color}" stroke-width="5"/>'
            f'<polygon points="{head}" fill="{color}"/>')


# 1. Шкала степеней окисления -------------------------------------------------------------------
def oxidation_scale() -> str:
    s = text(800, 56, 'Степень окисления: рост и снижение', 'h', 'middle')
    x0, step, y = 160, 140, 300
    s += f'<path d="M{x0 - 40} {y} H {x0 + 9 * step + 40}" stroke="{INK}" stroke-width="4"/>'
    for k, v in enumerate(range(-3, 7)):
        x = x0 + k * step
        s += f'<line x1="{x}" y1="{y - 12}" x2="{x}" y2="{y + 12}" stroke="{INK}" stroke-width="3"/>'
        s += text(x, y + 50, ('+' if v > 0 else '−' if v < 0 else '') + str(abs(v)), 't', 'middle')
    xa = lambda v: x0 + (v + 3) * step
    s += arc(xa(0), xa(3), y, True, RED) + text((xa(0) + xa(3)) / 2, y - 130, chem('Al⁰ − 3e⁻ → Al⁺³'), 't', 'middle', RED)
    s += arc(xa(0), xa(-2), y, False, BLUE) + text((xa(0) + xa(-2)) / 2, y + 150, chem('S⁰ + 2e⁻ → S⁻²'), 't', 'middle', BLUE)
    s += arrow(420, 130, 1180, 130, RED, 6) + text(800, 110, 'окисление: отдаёт e⁻, степень растёт', 's', 'middle', RED)
    s += arrow(1180, 480, 420, 480, BLUE, 6) + text(800, 520, 'восстановление: принимает e⁻, степень снижается', 's', 'middle', BLUE)
    return s


# 2. Перенос электронов --------------------------------------------------------------------------
def electron_transfer() -> str:
    s = text(800, 56, 'Кто отдаёт, кто принимает электроны', 'h', 'middle')
    for cx, col, title, rows in ((360, RED, 'восстановитель', ['отдаёт e⁻,', 'сам окисляется,', 'степень растёт']),
                                 (1240, BLUE, 'окислитель', ['принимает e⁻,', 'сам восстанавливается,', 'степень снижается'])):
        s += f'<circle cx="{cx}" cy="250" r="140" fill="#fff" stroke="{col}" stroke-width="6"/>'
        s += text(cx, 240, title, 's', 'middle', col) + text(cx, 280, 'Mg' if col == RED else chem('O₂'), 'h', 'middle')
        s += lines_at(cx, 420, rows, 's')
    for k, y in enumerate((200, 250, 300)):
        s += arrow(520, y, 1080, y, INK, 3)
        s += f'<circle cx="{700 + k * 60}" cy="{y}" r="16" fill="#FFE07A" stroke="{INK}" stroke-width="2"/>' + text(700 + k * 60, y + 7, 'e', 'cap', 'middle', INK)
    s += f'<rect x="420" y="540" width="760" height="140" rx="16" fill="{PAPER}"/>'
    s += text(800, 585, chem('2Mg + O₂ = 2MgO'), 't', 'middle')
    s += text(800, 630, chem('Mg⁰ − 2e⁻ → Mg⁺² (×2);  O₂⁰ + 4e⁻ → 2O⁻² (×1)'), 's', 'middle')
    s += text(800, 668, 'электронов отдано столько же, сколько принято', 'cap', 'middle')
    return s


# 3. Пять шагов баланса ---------------------------------------------------------------------------
def balance_steps() -> str:
    s = text(800, 56, 'Электронный баланс: пять шагов', 'h', 'middle')
    steps = [('1. Степени', ['Ca⁰ + P⁰ → Ca₃⁺²P₂⁻³'], 'кто меняет степень?'),
             ('2. Переходы', ['Ca⁰ − 2e⁻ → Ca⁺²', 'P⁰ + 3e⁻ → P⁻³'], 'сколько e⁻ на атом'),
             ('3. НОК', ['НОК(2; 3) = 6', 'Ca ×3,  P ×2'], 'множители'),
             ('4. Коэффициенты', ['3Ca + 2P → Ca₃P₂'], 'остальное — подбором'),
             ('5. Проверка', ['Ca: 3 = 3;  P: 2 = 2', 'e⁻: 6 = 6'], 'H и O — последними')]
    for k, (title, rows, cap) in enumerate(steps):
        x = 30 + k * 312
        cx = x + 145
        s += f'<rect x="{x}" y="110" width="290" height="330" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += f'<rect x="{x}" y="110" width="290" height="62" rx="18" fill="{RED if k == 2 else INK}"/>' + text(cx, 152, title, 't', 'middle', '#fff')
        s += lines_at(cx, 250 - (len(rows) - 1) * 18, rows, 's', step=40)
        s += text(cx, 400, cap, 'cap', 'middle')
        if k < 4:
            s += arrow(x + 292, 275, x + 310, 275, GREY, 4)
    s += f'<rect x="200" y="480" width="1200" height="110" rx="16" fill="{PAPER}"/>'
    s += text(800, 522, chem('Пример сложнее: 6P + 5KClO₃ = 3P₂O₅ + 5KCl'), 't', 'middle')
    s += text(800, 565, chem('P⁰ − 5e⁻ → P⁺⁵ (×6);  Cl⁺⁵ + 6e⁻ → Cl⁻¹ (×5);  НОК = 30'), 's', 'middle')
    return s


# 4. Роли серы ------------------------------------------------------------------------------------
def sulfur_roles() -> str:
    s = text(800, 56, 'Сера: степень окисления определяет роль', 'h', 'middle')
    y, xs = 290, {-2: 240, 0: 600, 4: 1000, 6: 1360}
    s += f'<path d="M150 {y} H 1450" stroke="{GREY}" stroke-width="4"/>'
    items = [(-2, 'H₂S', 'низшая', 'только восстановитель', BLUE),
             (0, 'S', 'промежуточная', 'и окислитель, и восстановитель', VIOLET),
             (4, 'SO₂', 'промежуточная', 'и окислитель, и восстановитель', VIOLET),
             (6, 'H₂SO₄', 'высшая', 'только окислитель', RED)]
    for v, f, kind, role, col in items:
        x = xs[v]
        s += f'<circle cx="{x}" cy="{y}" r="58" fill="#fff" stroke="{col}" stroke-width="5"/>'
        s += text(x, y - 4, ('+' if v > 0 else '−' if v < 0 else '') + str(abs(v)), 'h', 'middle', col)
        s += text(x, y + 30, chem(f), 's', 'middle')
        s += text(x, y + 110, kind, 's', 'middle', GREY)
        role_rows = role.split(', ') if ',' in role else [role]
        s += lines_at(x, y + 150, [r + (',' if j < len(role_rows) - 1 else '') for j, r in enumerate(role_rows)], 's', color=col)
        if v != 6:
            s += arrow(x + 30, y - 75, x + 110, y - 115, RED, 5)
        if v != -2:
            s += arrow(x - 30, y - 75, x - 110, y - 115, BLUE, 5)
    s += text(1450, 140, '→ рост степени: отдаёт e⁻', 'cap', 'end', RED) + text(150, 140, '← снижение: принимает e⁻', 'cap', 'start', BLUE)
    s += text(800, 560, chem('Не реагируют между собой два «только окислителя» (HNO₃ и H₂SO₄) или два «только восстановителя» (H₂S и HI).'), 'cap', 'middle')
    return s


# 5. Типы ОВР ----------------------------------------------------------------------------------
def tbox(x, y, w, h, title, rows, col=INK, fill='#fff'):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{col}" stroke-width="3"/>'
    s += text(x + w / 2, y + 42, title, 't', 'middle', col)
    return s + lines_at(x + w / 2, y + 86, rows, 's')


def redox_types() -> str:
    s = text(800, 56, 'Три типа окислительно-восстановительных реакций', 'h', 'middle')
    s += tbox(40, 110, 480, 200, 'межмолекулярные', ['меняются элементы', 'разных веществ', 'Fe₂O₃ + 3CO = 2Fe + 3CO₂'])
    s += tbox(560, 110, 480, 200, 'внутримолекулярные', ['меняются разные элементы', 'одного вещества', '4FeSO₄ = 2Fe₂O₃ + 4SO₂ + O₂'])
    s += tbox(1080, 110, 480, 200, 'самоокисления-', ['самовосстановления:', 'окислитель и восстановитель —', 'атомы одного элемента'], RED, '#FDECEC')
    s += arrow(1240, 315, 820, 385, RED, 4) + arrow(1400, 315, 1340, 385, RED, 4)
    s += tbox(560, 390, 500, 230, 'диспропорционирование', ['одна степень → две', 'Cl₂ + H₂O = HClO + HCl', 'Cl⁰ → Cl⁺¹ и Cl⁻¹'])
    s += tbox(1080, 390, 500, 230, 'конпропорционирование', ['две степени → одна', 'SO₂ + 2H₂S = 3S + 2H₂O', 'S⁺⁴ и S⁻² → S⁰'])
    s += lines_at(280, 430, ['Внутримолекулярная ≠', 'диспропорционирование:', 'там меняются разные', 'элементы (Fe, S, O)'], 'cap', step=32)
    return s


# 6. Перманганат и среда -------------------------------------------------------------------------
def permanganate_medium() -> str:
    s = text(800, 56, 'Перманганат: продукт зависит от среды', 'h', 'middle')
    s += f'<circle cx="800" cy="230" r="95" fill="#C2185B"/>' + text(800, 225, chem('MnO₄⁻'), 'h', 'middle', '#fff')
    s += text(800, 268, chem('Mn⁺⁷'), 't', 'middle', '#fff')
    s += arrow(700, 260, 420, 360, INK, 6) + arrow(900, 260, 1180, 360, INK, 6)
    s += text(470, 280, chem('кислая (H⁺)'), 't', 'middle') + text(1130, 280, 'нейтральная', 't', 'middle')
    for cx, prod, st, rows, eq in ((360, 'Mn²⁺', 'Mn⁺²: +5e⁻', ['MnO₄⁻ + 8H⁺ + 5e⁻ →', 'Mn²⁺ + 4H₂O'],
                                    ['2KMnO₄ + 10FeSO₄ + 8H₂SO₄ =', '2MnSO₄ + 5Fe₂(SO₄)₃ + K₂SO₄ + 8H₂O']),
                                   (1240, 'MnO₂↓', 'Mn⁺⁴: +3e⁻', ['MnO₄⁻ + 2H₂O + 3e⁻ →', 'MnO₂ + 4OH⁻'],
                                    ['3Na₂SO₃ + 2KMnO₄ + H₂O =', '2MnO₂ + 3Na₂SO₄ + 2KOH'])):
        s += f'<rect x="{cx - 330}" y="380" width="660" height="380" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += text(cx, 440, chem(prod), 'h', 'middle', RED) + text(cx, 480, chem(st), 's', 'middle', GREY)
        s += lines_at(cx, 540, rows, 't', step=40)
        s += lines_at(cx, 660, eq, 's', step=34)
    s += text(800, 800, 'По разобранным реакциям учебника. Кислота и вода тоже участвуют в балансе H и O.', 'cap', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'oxidation-scale.png': (oxidation_scale(), 1600, 560),
        'electron-transfer.png': (electron_transfer(), 1600, 710),
        'balance-steps.png': (balance_steps(), 1600, 620),
        'sulfur-roles.png': (sulfur_roles(), 1600, 600),
        'redox-types.png': (redox_types(), 1600, 660),
        'permanganate-medium.png': (permanganate_medium(), 1600, 830),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
