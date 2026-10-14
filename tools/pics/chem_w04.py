"""Рисунки недели 4 химии (course/week-04/pics/*.png): карта переходов через моль, расчёт по уравнению, равные объёмы газов.

Факты — по выжимке course/textbooks/chem-04-mole.md (Х8 § 15–19, Х10-1 § 20–22).
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w04.py
"""
from __future__ import annotations

from common import GREY, INK, PAPER, RED, ROOT, arrow, chem, render, text

OUT = ROOT / 'course' / 'week-04' / 'pics'
TINT = '#FBE3E4'


def box(cx: float, cy: float, w: float, h: float, fill: str = '#fff', stroke: str = INK) -> str:
    return f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'


def mole_map() -> str:
    s = text(800, 60, 'Всё считаем через моль', 'h', 'middle') + '<g transform="translate(0,-100)">'
    n = (800, 390)
    s += f'<circle cx="{n[0]}" cy="{n[1]}" r="110" fill="{TINT}" stroke="{RED}" stroke-width="6"/>'
    s += text(800, 395, 'n', 'f', 'middle') + text(800, 440, 'моль', 's', 'middle')
    sats = [((230, 390), 'm', 'масса, г', chem('M — молярная масса, г/моль')),
            ((1370, 390), 'N', 'число частиц', chem('Nₐ = 6,02 · 10²³ моль⁻¹'))]
    for (x, y), sym, cap, const in sats:
        s += box(x, y, 280, 130) + text(x, y + 6, sym, 'f', 'middle') + text(x, y + 44, cap, 'cap', 'middle')
        s += text(x, y + 110, const, 's', 'middle')
    # m <-> n
    s += arrow(375, 372, 688, 372, RED, 5) + arrow(688, 410, 375, 410, INK, 5)
    s += text(530, 350, chem('n = m / M'), 't', 'middle') + text(530, 455, chem('m = n · M'), 't', 'middle')
    # n <-> N
    s += arrow(912, 372, 1225, 372, INK, 5) + arrow(1225, 410, 912, 410, RED, 5)
    s += text(1068, 350, chem('N = n · Nₐ'), 't', 'middle') + text(1068, 455, chem('n = N / Nₐ'), 't', 'middle')
    # n <-> V
    s += box(800, 730, 300, 130) + text(800, 736, 'V', 'f', 'middle') + text(800, 774, 'объём газа, л', 'cap', 'middle')
    s += arrow(780, 503, 780, 660, INK, 5) + arrow(820, 660, 820, 503, RED, 5)
    s += text(755, 590, chem('V = n · Vₘ'), 't', 'end') + text(845, 590, chem('n = V / Vₘ'), 't')
    s += text(800, 840, chem('Vₘ = 22,4 л/моль — только для газов и только при н. у.'), 's', 'middle')
    s += text(800, 885, 'Красные стрелки — переход к молям; чёрные — от молей к ответу.', 'cap', 'middle')
    return s + '</g>'


def reaction_route() -> str:
    s = text(800, 60, 'Расчёт по уравнению реакции', 'h', 'middle')
    steps = [(['Данные'], ['m, г или V, л', 'данного вещества']),
             (['n данного'], [chem('n = m / M'), chem('или n = V / Vₘ')]),
             (['Отношение', 'коэффициентов'], ['по уравнению', 'реакции']),
             (['n искомого'], ['моль']),
             (['Ответ'], [chem('m = n · M, г'), chem('или V = n · Vₘ, л')])]
    w, gap, x0, y0 = 270, 50, 25, 140
    for k, (title, sub) in enumerate(steps):
        x = x0 + k * (w + gap)
        hot = k in (1, 3)
        s += f'<rect x="{x}" y="{y0}" width="{w}" height="230" rx="16" fill="{TINT if hot else "#fff"}" stroke="{RED if hot else INK}" stroke-width="4"/>'
        s += f'<circle cx="{x + w / 2}" cy="{y0}" r="24" fill="{RED}"/>' + text(x + w / 2, y0 + 10, str(k + 1), 't', 'middle', '#fff')
        s += ''.join(text(x + w / 2, y0 + 75 + j * 36, t, 't', 'middle') for j, t in enumerate(title))
        s += ''.join(text(x + w / 2, y0 + 165 + j * 32, t, 's', 'middle') for j, t in enumerate(sub))
        if k < 4:
            s += arrow(x + w + 6, y0 + 115, x + w + gap - 6, y0 + 115, INK, 5)
    s += text(800, 440, 'Сравниваем и переводим только моли; масса и объём — на входе и в ответе, с единицами.', 's', 'middle')
    return s


def equal_gas_volumes() -> str:
    s = text(800, 60, 'Равные объёмы газов при н. у.', 'h', 'middle')
    spots = [(-90, -80), (-10, -110), (80, -70), (-60, -10), (30, 0), (100, 30), (-100, 60), (-20, 80), (70, 100), (10, -50)]
    for cx, gas, r, fill in ((420, 'H₂', 9, '#DCEBF5'), (1180, 'O₂', 15, '#FBE3E4')):
        s += box(cx, 290, 320, 330, PAPER) + text(cx, 170, chem(gas), 'f', 'middle')
        for dx, dy in spots:
            x, y = cx + dx, 335 + dy
            s += ''.join(f'<circle cx="{x + o * r * 0.9:.0f}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="3"/>' for o in (-1, 1))
    rows = [('объём', 'V = 22,4 л', 'V = 22,4 л', '='), ('количество вещества', 'n = 1 моль', 'n = 1 моль', '='),
            ('число молекул', 'N = 6,02 · 10²³', 'N = 6,02 · 10²³', '='), ('масса', 'm = 2 г', 'm = 32 г', '≠')]
    for k, (name, a, b, sign) in enumerate(rows):
        y = 520 + k * 50
        hot = sign == '≠'
        s += text(420, y, chem(a), 't', 'middle', RED if hot else None) + text(1180, y, chem(b), 't', 'middle', RED if hot else None)
        s += text(800, y, f'{sign}  {name}  {sign}', 's', 'middle', RED if hot else GREY)
    s += f'<rect x="200" y="735" width="1200" height="70" rx="14" fill="{PAPER}"/>'
    s += text(800, 780, '22,4 л/моль — только для газов при н. у. Жидкая вода и твёрдые вещества сюда не относятся.', 's', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'mole-map.png': (mole_map(), 1600, 810),
        'reaction-route.png': (reaction_route(), 1600, 480),
        'equal-gas-volumes.png': (equal_gas_volumes(), 1600, 830),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
