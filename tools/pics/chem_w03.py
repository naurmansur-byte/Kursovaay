"""Рисунки недели 3 химии (course/week-03/pics/*.png): классы веществ, индикаторы, ряд Бекетова, цепочка кальция.

Факты — по выжимке course/textbooks/chem-03-classes.md (Х8 § 42–50).
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w03.py
"""
from __future__ import annotations

from common import GREEN, GREY, INK, LIGHT_BLUE, LIGHT_GREEN, PAPER, RED, ROOT, arrow, chem, render, span, text

OUT = ROOT / 'course' / 'week-03' / 'pics'
BLUE, ORANGE = '#3A57A7', '#D9822B'


def classes_map() -> str:
    s = text(800, 60, 'Четыре класса неорганических веществ', 'h', 'middle')
    legend = [(RED, 'водород кислоты'), (BLUE, 'кислотный остаток'), (GREEN, 'группа OH'), (ORANGE, 'кислород оксида')]
    for k, (c, name) in enumerate(legend):
        x = 170 + k * 340
        s += f'<rect x="{x}" y="92" width="26" height="26" rx="5" fill="{c}"/>' + text(x + 38, 114, name, 's')
    H, OH, O = (lambda t: span(t, RED)), (lambda t: span(t, GREEN)), (lambda t: span(t, ORANGE))
    R = lambda t: span(t, BLUE)  # noqa: E731
    cards = [
        ('Оксиды', ['соединения из двух элементов,', 'один из которых — кислород'],
         [(f'Ca{O("O")}', 'оксид кальция'), (f'C{O("O₂")}', 'оксид углерода (IV)')]),
        ('Кислоты', ['сложные вещества из атомов водорода', 'и кислотных остатков'],
         [(f'{H("H₂")}{R("SO₄")}', 'серная кислота'), (f'{H("H")}{R("Cl")}', 'соляная кислота')]),
        ('Основания (гидроксиды)', ['атомы металла, соединённые с одной', 'или несколькими группами OH'],
         [(f'Na{OH("OH")}', 'гидроксид натрия'), (f'Cu({OH("OH")})₂', 'гидроксид меди (II)')]),
        ('Соли', ['сложные вещества из атомов металла', 'и кислотных остатков'],
         [(f'K{R("Cl")}', 'хлорид калия'), (f'Na₂{R("SO₄")}', 'сульфат натрия')]),
    ]
    for k, (name, lines, examples) in enumerate(cards):
        x0, y0 = 30 + (k % 2) * 785, 150 + (k // 2) * 320
        s += f'<rect x="{x0}" y="{y0}" width="755" height="295" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/>'
        s += f'<path d="M{x0} {y0 + 60} V{y0 + 16} a16 16 0 0 1 16 -16 H{x0 + 739} a16 16 0 0 1 16 16 V{y0 + 60} Z" fill="{INK}"/>'
        s += text(x0 + 26, y0 + 42, name, 'w')
        s += ''.join(text(x0 + 26, y0 + 100 + j * 33, ln, 's') for j, ln in enumerate(lines))
        for j, (f, cap) in enumerate(examples):
            cx = x0 + 190 + j * 375
            s += text(cx, y0 + 222, chem(f), 'f', 'middle') + text(cx, y0 + 268, cap, 'cap', 'middle')
    s += f'<rect x="30" y="800" width="1540" height="80" rx="14" fill="{PAPER}"/>'
    s += text(800, 851, 'Кислые соли содержат водород: ' + chem(f'Na{H("H")}{R("SO₄")}') + '   ·   основные соли — группу OH: '
              + chem(f'Cu({OH("OH")}){R("Cl")}'), 't', 'middle')
    return s


def indicators() -> str:
    s = text(800, 60, 'Индикаторы: цвет в разной среде', 'h', 'middle')
    cols = [(650, 'кислая'), (1000, 'щелочная'), (1350, 'нейтральная')]
    s += ''.join(text(x, 140, name, 't', 'middle') for x, name in cols)
    rows = [('лакмус', [('красный', '#E0303A'), ('синий', '#2F5DD3'), ('фиолетовый', '#7B4FB5')]),
            ('фенолфталеин', [('бесцветный', None), ('малиновый', '#C2185B'), ('бесцветный', None)]),
            ('метилоранж', [('розовый', '#F48FB1'), ('жёлтый', '#F7CB2D'), ('оранжевый', '#F28C28')])]
    for k, (name, cells) in enumerate(rows):
        y0 = 170 + k * 225
        if k:
            s += f'<line x1="60" y1="{y0 - 8}" x2="1540" y2="{y0 - 8}" stroke="#DEDAD1" stroke-width="3"/>'
        s += text(80, y0 + 105, name, 't')
        for (cx, _), (word, color) in zip(cols, cells):
            liquid = color or '#F4F7F9'
            s += (f'<path d="M{cx - 28} {y0 + 75} V{y0 + 135} a28 28 0 0 0 56 0 V{y0 + 75} Z" fill="{liquid}"/>'
                  f'<path d="M{cx - 28} {y0 + 12} V{y0 + 135} a28 28 0 0 0 56 0 V{y0 + 12}" fill="none" stroke="{INK}" stroke-width="4"/>'
                  f'<line x1="{cx - 38}" y1="{y0 + 12}" x2="{cx + 38}" y2="{y0 + 12}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
            s += text(cx, y0 + 205, word, 's', 'middle')
    return s


def activity_series() -> str:
    s = text(800, 60, 'Ряд активности металлов Н. Н. Бекетова (1863)', 'h', 'middle')
    els = ['Li', 'K', 'Na', 'Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', '(H)', 'Cu', 'Hg', 'Ag', 'Pt', 'Au']
    w, gap, x0, y = 86, 6, 67, 130
    for i, e in enumerate(els):
        x = x0 + i * (w + gap)
        fill = RED if e == '(H)' else LIGHT_GREEN if e in ('Mg', 'Zn', 'Fe') else LIGHT_BLUE if e == 'Cu' else PAPER
        s += f'<rect x="{x}" y="{y}" width="{w}" height="96" rx="12" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
        s += text(x + w / 2, y + 62, e, 't', 'middle', '#fff' if e == '(H)' else None)
    left_end, right_start, right_end = x0 + 10 * (w + gap) - gap, x0 + 11 * (w + gap), x0 + 16 * (w + gap) - gap
    for a, b in ((x0, left_end), (right_start, right_end)):
        s += f'<path d="M{a} 250 v18 H{b} v-18" fill="none" stroke="{INK}" stroke-width="4"/>'
    s += text((x0 + left_end) / 2, 312, 'левее H — вытесняют водород из кислот*', 't', 'middle')
    s += text((x0 + left_end) / 2, 350, 'с кислотой: Mg — быстро, Zn — медленнее, Fe — ещё медленнее', 'cap', 'middle')
    s += text((right_start + right_end) / 2, 312, 'правее H — не вытесняют', 't', 'middle')
    s += text((right_start + right_end) / 2, 350, 'Cu с кислотой не реагирует', 'cap', 'middle')
    s += arrow(x0, 420, right_end, 420, GREY, 5) + text(800, 465, 'активность металлов уменьшается', 's', 'middle')
    s += text(800, 530, '* кроме азотной кислоты: с ней выделяются NO, NO₂, NH₃ и др., а не водород'.replace('NO₂', chem('NO₂')).replace('NH₃', chem('NH₃')),
              'cap', 'middle')
    return s


def lime_chain() -> str:
    s = text(800, 60, 'Цепочка превращений кальция', 'h', 'middle')
    xs, y = [190, 600, 1010, 1420], 160
    subs = ['Ca', 'CaO', 'Ca(OH)₂', 'CaCO₃']
    for x, f in zip(xs, subs):
        s += f'<rect x="{x - 130}" y="{y}" width="260" height="110" rx="16" fill="#fff" stroke="{INK}" stroke-width="4"/>'
        s += text(x, y + 74, chem(f), 'f', 'middle')
    for k, r in enumerate(['+ O₂', '+ H₂O', '+ CO₂']):
        a, b = xs[k] + 145, xs[k + 1] - 145
        s += arrow(a, y + 55, b, y + 55, RED, 6) + text((a + b) / 2, y + 32, chem(r), 't', 'middle')
    classes = ['металл', 'основной оксид', 'основание', 'соль']
    names = [[], ['негашёная (жжёная)', 'известь'], ['гашёная известь;', 'раствор — известковая вода'], ['мел, известняк']]
    for x, c, nm in zip(xs, classes, names):
        s += text(x, y + 160, c, 't', 'middle')
        s += ''.join(text(x, y + 200 + j * 32, ln, 'cap', 'middle') for j, ln in enumerate(nm))
    # известковая вода мутнеет: стакан с осадком
    bx, by = 560, 470
    s += (f'<path d="M{bx + 2} {by + 34} V{by + 100} a12 12 0 0 0 12 12 H{bx + 86} a12 12 0 0 0 12 -12 V{by + 34} Z" fill="#E4E4DC"/>'
          f'<path d="M{bx} {by} V{by + 100} a14 14 0 0 0 14 14 H{bx + 86} a14 14 0 0 0 14 -14 V{by}" fill="none" stroke="{INK}" stroke-width="4"/>')
    s += ''.join(f'<circle cx="{bx + 16 + j * 13}" cy="{by + 102 - (j % 2) * 7}" r="6" fill="#fff" stroke="{GREY}" stroke-width="1.5"/>'
                 for j in range(6))
    s += text(bx + 140, by + 50, 'Известковая вода + ' + chem('CO₂') + ' → мутнеет:', 't')
    s += text(bx + 140, by + 92, 'выпадает осадок ' + chem('CaCO₃') + '↓', 't')
    return s


if __name__ == '__main__':
    jobs = {
        'classes-map.png': (classes_map(), 1600, 910),
        'indicators.png': (indicators(), 1600, 840),
        'activity-series.png': (activity_series(), 1600, 570),
        'lime-chain.png': (lime_chain(), 1600, 620),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
