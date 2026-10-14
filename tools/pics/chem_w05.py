"""Рисунки недели 5 химии (course/week-05/pics/*.png): раствор, изменения раствора, технический образец, недостаток, выход.

Числа — из разобранных примеров конспекта недели (по выжимке course/textbooks/chem-05-solutions-yield.md).
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w05.py
"""
from __future__ import annotations

from common import GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-05' / 'pics'
TINT = '#FBE3E4'
WATER = '#DCEBF5'


def liquid(omega: float) -> str:
    """Цвет раствора: чем больше ω, тем насыщеннее красный."""
    a = min(1.0, 0.12 + omega * 2.2)
    r, g, b = (int(255 - (255 - c) * a) for c in (241, 58, 67))
    return f'#{r:02X}{g:02X}{b:02X}'


def beaker(cx: float, base: float, w: float, h: float, level: float, fill: str) -> str:
    """Стакан с жидкостью: base — низ, level — доля высоты, занятая жидкостью."""
    x0, top = cx - w / 2, base - h
    lh = h * level
    return (f'<rect x="{x0 + 5:.0f}" y="{base - lh:.0f}" width="{w - 10:.0f}" height="{lh - 5:.0f}" rx="10" fill="{fill}"/>'
            f'<path d="M{x0 - 10:.0f} {top:.0f} H{x0:.0f} V{base - 14:.0f} a14 14 0 0 0 14 14 H{x0 + w - 14:.0f} a14 14 0 0 0 14 -14 '
            f'V{top:.0f} H{x0 + w + 10:.0f}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')


def crystals(cx: float, base: float) -> str:
    pts = [(-40, 0), (-14, 0), (12, 0), (38, 0), (-27, -26), (-1, -26), (25, -26), (-14, -52), (12, -52)]
    return ''.join(f'<rect x="{cx + dx - 12:.0f}" y="{base + dy - 24:.0f}" width="24" height="24" rx="3" fill="#fff" stroke="{INK}" stroke-width="3" '
                   f'transform="rotate({(k * 17) % 30 - 15} {cx + dx:.0f} {base + dy - 12:.0f})"/>' for k, (dx, dy) in enumerate(pts))


def solution_parts() -> str:
    s = text(800, 60, 'Раствор = вещество + растворитель', 'h', 'middle')
    s += crystals(260, 330) + text(260, 400, 'растворённое вещество', 't', 'middle') + text(260, 440, 'NaCl, 5 г', 's', 'middle', GREY)
    s += text(470, 300, '+', 'f', 'middle')
    s += beaker(700, 340, 190, 220, 0.62, WATER) + text(700, 400, 'растворитель', 't', 'middle') + text(700, 440, 'вода, 45 г', 's', 'middle', GREY)
    s += text(920, 300, '=', 'f', 'middle')
    s += beaker(1180, 340, 210, 230, 0.66, liquid(0.10)) + text(1180, 400, 'раствор — однородная система', 't', 'middle')
    s += text(1180, 440, '50 г', 's', 'middle', GREY)
    s += f'<rect x="200" y="490" width="1200" height="110" rx="16" fill="{PAPER}"/>'
    s += text(800, 535, 'm(раствора) = m(вещества) + m(растворителя) = 5 + 45 = 50 г', 't', 'middle')
    s += text(800, 580, 'ω = m(вещества) / m(раствора) = 5 / 50 = 0,1 = 10 %', 't', 'middle', RED)
    return s


def solution_changes() -> str:
    s = text(800, 55, 'Что происходит с раствором', 'h', 'middle')
    panels = [('Долили воду', '+ 40 г воды', (200, 30, 0.15), (240, 30, 0.125), 'вещество — то же, раствор больше'),
              ('Упарили воду', '− 200 г воды', (400, 60, 0.15), (200, 60, 0.30), 'вещество — то же, раствор меньше'),
              ('Добавили вещество', '+ 20 г NaCl', (180, 14.4, 0.08), (200, 34.4, 0.172), 'меняются обе массы'),
              ('Смешали два раствора', '+ 200 г 4 %', (120, 12, 0.10), (320, 20, 0.0625), 'вещества и растворы складывают отдельно')]

    def fmt(x: float) -> str:
        return f'{x:g}'.replace('.', ',')
    for k, (title, action, a, b, note) in enumerate(panels):
        x0, y0 = 30 + (k % 2) * 785, 95 + (k // 2) * 380
        s += f'<rect x="{x0}" y="{y0}" width="755" height="360" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/>'
        s += text(x0 + 26, y0 + 46, title, 't')
        for (m, mv, w), cx in ((a, x0 + 170), (b, x0 + 560)):
            lvl = 0.25 + 0.6 * m / 400
            s += beaker(cx, y0 + 268, 150, 170, lvl, liquid(w))
            s += text(cx, y0 + 305, f'раствор {fmt(m)} г', 's', 'middle') + text(cx, y0 + 337, f'вещество {fmt(mv)} г · ω {fmt(round(w * 100, 2))} %', 'cap', 'middle')
        s += arrow(x0 + 270, y0 + 185, x0 + 460, y0 + 185, RED, 6) + text(x0 + 365, y0 + 165, action, 's', 'middle')
        s += text(x0 + 26, y0 + 80, note, 'cap')
    return s


def technical_sample() -> str:
    s = text(800, 60, 'Технический образец = чистое вещество + примеси', 'h', 'middle')
    x0, y0, w = 150, 150, 1300
    s += f'<rect x="{x0}" y="{y0}" width="{w * 0.8:.0f}" height="110" rx="14" fill="{TINT}" stroke="{RED}" stroke-width="4"/>'
    s += f'<rect x="{x0 + w * 0.8:.0f}" y="{y0}" width="{w * 0.2:.0f}" height="110" rx="14" fill="#E4E2DC" stroke="{GREY}" stroke-width="4"/>'
    s += text(x0 + w * 0.4, y0 + 52, chem('чистый CaCO₃ — 40 г (80 %)'), 't', 'middle') + text(x0 + w * 0.4, y0 + 88, 'идёт в реакцию', 's', 'middle', RED)
    s += text(x0 + w * 0.9, y0 + 52, 'примеси 10 г', 's', 'middle') + text(x0 + w * 0.9, y0 + 88, 'не реагируют', 'cap', 'middle')
    s += f'<path d="M{x0} {y0 - 18} v-14 H{x0 + w} v14" fill="none" stroke="{INK}" stroke-width="3"/>' + text(800, y0 - 42, 'образец 50 г', 's', 'middle')
    s += arrow(x0 + w * 0.4, y0 + 125, x0 + w * 0.4, y0 + 205, RED, 6)
    s += f'<rect x="300" y="365" width="1000" height="150" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    s += text(800, 410, chem('CaCO₃ → CaO + CO₂'), 't', 'middle')
    s += text(800, 455, chem('n(CaCO₃) = 40 / 100 = 0,4 моль → n(CO₂) = 0,4 моль'), 's', 'middle')
    s += text(800, 492, chem('V(CO₂) = 0,4 × 22,4 = 8,96 л (н. у.)'), 's', 'middle')
    s += text(800, 565, 'm(чистого) = m(образца) × (1 − ω(примесей))', 't', 'middle') + text(800, 605, 'ω(чистого) + ω(примесей) = 1', 's', 'middle')
    return s


def limiting_reagent() -> str:
    s = text(800, 55, 'Кто в недостатке: сравниваем n / коэффициент', 'h', 'middle')
    s += text(800, 120, chem('2NaOH + CuSO₄ → Cu(OH)₂ + Na₂SO₄'), 't', 'middle')
    cols = [(420, 'NaOH', '16 г', '16 / 40 = 0,4 моль', '0,4 / 2 = 0,2', 0.2, True),
            (1180, chem('CuSO₄'), '48 г', '48 / 160 = 0,3 моль', '0,3 / 1 = 0,3', 0.3, False)]
    for cx, name, m, n, frac, val, low in cols:
        s += text(cx, 190, name, 'f', 'middle')
        rows = [('масса', m), ('количество', n), ('n / коэффициент', frac)]
        for j, (lab, v) in enumerate(rows):
            y = 240 + j * 70
            s += f'<rect x="{cx - 230}" y="{y}" width="460" height="56" rx="12" fill="{PAPER if j < 2 else (TINT if low else "#fff")}" stroke="{RED if j == 2 and low else INK}" stroke-width="3"/>'
            s += text(cx - 210, y + 37, lab, 'cap') + text(cx + 210, y + 37, v, 's', 'end')
            if j < 2:
                s += arrow(cx, y + 56, cx, y + 70, GREY, 3)
        h = val * 500
        s += f'<rect x="{cx - 50}" y="{620 - h:.0f}" width="100" height="{h:.0f}" rx="8" fill="{RED if low else "#C9C5BD"}"/>'
    s += text(800, 470, '0,2 < 0,3', 'f', 'middle', RED)
    s += text(800, 520, 'NaOH — в недостатке:', 't', 'middle') + text(800, 556, 'по нему считаем продукт', 's', 'middle')
    s += f'<line x1="300" y1="620" x2="1300" y2="620" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="200" y="645" width="1200" height="100" rx="16" fill="{PAPER}"/>'
    s += text(800, 685, chem('n(Cu(OH)₂) = 0,2 моль → m = 0,2 × 98 = 19,6 г'), 't', 'middle')
    s += text(800, 725, chem('CuSO₄ — в избытке: израсходовано 0,2 моль, осталось 0,3 − 0,2 = 0,1 моль'), 's', 'middle')
    return s


def product_yield() -> str:
    s = text(800, 55, 'Выход продукта η', 'h', 'middle')
    s += text(800, 115, chem('N₂ + 3H₂ → 2NH₃: из 0,3 моль N₂ по уравнению — 0,6 моль NH₃'), 's', 'middle', GREY)
    base, x1, x2, bw = 560, 430, 1020, 220
    s += f'<rect x="{x1 - bw / 2:.0f}" y="{base - 360}" width="{bw}" height="360" rx="10" fill="{TINT}" stroke="{RED}" stroke-width="4"/>'
    s += f'<rect x="{x2 - bw / 2:.0f}" y="{base - 180}" width="{bw}" height="180" rx="10" fill="{RED}"/>'
    s += f'<rect x="{x2 - bw / 2:.0f}" y="{base - 360}" width="{bw}" height="360" rx="10" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
    s += text(x1, base - 300, '100 %', 'f', 'middle') + text(x2, base - 80, '50 %', 'f', 'middle', '#fff')
    s += text(x1, base + 45, 'теоретический', 't', 'middle') + text(x1, base + 80, chem('по уравнению: 13,44 л NH₃'), 's', 'middle')
    s += text(x2, base + 45, 'практический', 't', 'middle') + text(x2, base + 80, chem('получено: 6,72 л NH₃'), 's', 'middle')
    s += text(x2, base - 260, 'потери', 'cap', 'middle')
    s += arrow(x1 + 130, base - 330, x2 - 130, base - 330, INK, 5) + text((x1 + x2) / 2, base - 345, '× η', 't', 'middle')
    s += arrow(x2 - 130, base - 140, x1 + 130, base - 140, INK, 5) + text((x1 + x2) / 2, base - 155, ': η', 't', 'middle')
    s += f'<rect x="1220" y="230" width="340" height="230" rx="16" fill="{PAPER}"/>'
    s += text(1390, 290, 'η = практ. / теор.', 't', 'middle', RED) + text(1390, 340, '= 6,72 / 13,44', 's', 'middle')
    s += text(1390, 380, '= 0,5 = 50 %', 's', 'middle') + text(1390, 430, 'теор. = практ. / η', 's', 'middle')
    s += text(800, 700, 'Сначала теоретический результат по уравнению, потом выход.', 't', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'solution-parts.png': (solution_parts(), 1600, 640),
        'solution-changes.png': (solution_changes(), 1600, 870),
        'technical-sample.png': (technical_sample(), 1600, 640),
        'limiting-reagent.png': (limiting_reagent(), 1600, 770),
        'product-yield.png': (product_yield(), 1600, 740),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
