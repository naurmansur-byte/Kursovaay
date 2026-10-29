"""Рисунки недели 19 химии (course/week-19/pics/*.png): галогеналкан и щёлочь, классы спиртов, водородные связи,
дегидратация, производство этанола, реакции фенола, кумольный способ, карбонильная группа, качественные реакции
альдегидов, таблица распознавания.

Факты — по выжимке course/textbooks/chem-19-alcohols-phenol-carbonyls.md (Х9-2 § 63; Х10-2 § 83–90; Х11-1 § 6–8).
Схемы условные. Запуск: cd tools/pics && ../../.venv/Scripts/python.exe chem_w19.py
"""
from __future__ import annotations

import math
import sys

from common import GREEN, GREY, INK, PAPER, RED, ROOT, arrow, chem, render
from common import text as _text


def text(x, y, s, cls='t', anchor='start', fill=None):
    s = chem(s).replace('ₙ', '<tspan baseline-shift="-0.28em" font-size="68%">n</tspan>')
    return _text(x, y, s, cls, anchor, fill)

OUT = ROOT / 'course' / 'week-19' / 'pics'
BLUE, ORANGE, PURPLE = '#3A57A7', '#D98A2B', '#8E44AD'
CC, HC, OC = '#3B3833', '#F4F1E6', '#E04B4B'


def lines_at(x, y, rows, cls='s', anchor='middle', step=34, color=None):
    return ''.join(text(x, y + j * step, r, cls, anchor, color) for j, r in enumerate(rows))


def card(x, y, w, h, fill=PAPER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def box(cx, cy, w, h, label, fill='#fff', stroke=INK, cls='s', color=None):
    rows = label.split('|')
    y0 = cy - (len(rows) - 1) * 16 + 9
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + lines_at(cx, y0, rows, cls, step=32, color=color))


def tube(cx, top, fill, h=240, sediment=None):
    s = f'<path d="M{cx - 32} {top} V {top + h - 32} A 32 32 0 0 0 {cx + 32} {top + h - 32} V {top}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if sediment:
        s += (f'<path d="M{cx - 32} {top + h - 70} V {top + h - 32} A 32 32 0 0 0 {cx + 32} {top + h - 32} V {top + h - 70} Z" '
              f'fill="{sediment}" stroke="{INK}" stroke-width="2"/>')
    return s


def atom(x, y, label, r=26, fill=CC, color='#fff'):
    fs = r if len(label) < 3 else r * 0.62
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{x:.0f}" y="{y + fs * 0.36:.0f}" text-anchor="middle" style="font: 800 {fs:.0f}px Manrope; fill:{color}">{chem(label)}</text>')


def bond(x1, y1, x2, y2, w=5, color=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w}"{d}/>'


def hexring(cx, cy, r=70):
    pts = [(cx + r * math.cos(math.radians(90 + 60 * k)), cy - r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    return (f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="#fff" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.58:.0f}" fill="none" stroke="{INK}" stroke-width="4"/>'), pts


# 1. Галогеналкан и щёлочь ----------------------------------------------------------------------
def haloalkane_alkali():
    s = text(900, 52, 'Бромэтан и щёлочь: замещение или отщепление', 'h', 'middle')
    s += card(30, 90, 1740, 700)
    s += box(900, 190, 380, 90, 'C₂H₅Br|бромэтан', '#F7EFC8', cls='t')
    s += arrow(780, 230, 460, 360, BLUE, 6) + arrow(1020, 230, 1340, 360, RED, 6)
    s += text(560, 270, 'NaOH, водный раствор', 's', 'end', BLUE) + text(1240, 270, 'NaOH, спиртовой раствор', 's', 'start', RED)
    s += tube(400, 370, '#DCEBF5') + tube(1400, 370, '#F7EFC8')
    s += box(400, 700, 520, 90, 'C₂H₅OH — спирт|замещение', '#E3EEF7')
    s += box(1400, 700, 520, 90, 'CH₂=CH₂ — алкен|отщепление (Зайцев)', '#FBE3E4')
    s += lines_at(900, 470, ['Зайцев: H уходит от соседнего', 'менее гидрогенизированного атома C'], 's', step=36, color=GREY)
    return s


# 2. Классы спиртов ---------------------------------------------------------------------------------
def alcohol_classes():
    s = text(900, 52, 'Классы спиртов', 'h', 'middle')
    s += card(30, 90, 860, 820) + card(910, 90, 860, 820)
    s += text(460, 145, 'По числу групп –OH', 't', 'middle')
    rows = [('одноатомные', 'CH₃–OH  метанол|CH₃–CH₂–OH  этанол'), ('двухатомные', 'HO–CH₂–CH₂–OH|этиленгликоль, этандиол-1,2'),
            ('трёхатомные', 'HO–CH₂–CH(OH)–CH₂–OH|глицерин, пропантриол-1,2,3')]
    for k, (n, f) in enumerate(rows):
        y = 260 + k * 220
        s += text(110, y, n, 't', 'start', BLUE) + box(500, y + 70, 680, 100, f)
    s += text(1340, 145, 'По атому C с группой –OH', 't', 'middle')
    rows = [('первичный', 'CH₃–CH₂–CH₂–OH|пропанол-1', 'C с –OH связан с одним C'),
            ('вторичный', 'CH₃–CH(OH)–CH₃|пропанол-2', 'с двумя C'),
            ('третичный', '(CH₃)₃C–OH|2-метилпропанол-2', 'с тремя C')]
    for k, (n, f, note) in enumerate(rows):
        y = 260 + k * 220
        s += text(990, y, n, 't', 'start', RED) + text(1700, y, note, 's', 'end', GREY) + box(1340, y + 70, 700, 100, f)
    return s


# 3. Водородные связи -------------------------------------------------------------------------------
def ethanol_mol(x, y, flip=False):
    sg = -1 if flip else 1
    s = bond(x - 80 * sg, y, x, y) + bond(x, y, x + 60 * sg, y - 50)
    s += atom(x - 80 * sg, y, 'C₂H₅', 34, '#9A958C') + atom(x, y, 'O', 26, OC) + atom(x + 60 * sg, y - 50, 'H', 20, HC, INK)
    return s


def hydrogen_bonds():
    s = text(900, 52, 'Водородные связи в спиртах', 'h', 'middle')
    s += card(30, 90, 1740, 760)
    y = 430
    for k, ox in enumerate((220, 450, 680)):   # цепочка O–H···O–H···O–H, радикал C₂H₅ над или под атомом O
        ry = y - 90 if k % 2 else y + 90
        s += bond(ox, y, ox, ry) + bond(ox, y, ox + 70, y)
        s += atom(ox, ry, 'C₂H₅', 34, '#9A958C') + atom(ox, y, 'O', 28, OC) + atom(ox + 70, y, 'H', 20, HC, INK)
        if k < 2:
            s += bond(ox + 92, y, ox + 200, y, 4, BLUE, '8 7')
    wx = 1150
    s += bond(wx, y, wx - 50, y - 60) + bond(wx, y, wx + 70, y)
    s += atom(wx, y, 'O', 28, OC) + atom(wx - 50, y - 60, 'H', 20, HC, INK) + atom(wx + 70, y, 'H', 20, HC, INK)
    s += bond(wx + 92, y, wx + 200, y, 4, BLUE, '8 7')
    ex = wx + 230
    s += bond(ex, y, ex, y - 90) + bond(ex, y, ex + 70, y)
    s += atom(ex, y - 90, 'C₂H₅', 34, '#9A958C') + atom(ex, y, 'O', 28, OC) + atom(ex + 70, y, 'H', 20, HC, INK)
    s += text(600, 160, 'спирт — спирт', 't', 'middle') + text(1400, 160, 'спирт — вода', 't', 'middle')
    s += lines_at(900, 640, ['H группы –OH притягивается к атому O соседней молекулы (пунктир)',
                             'поэтому спирты кипят выше алканов и смешиваются с водой'], 's', step=44)
    s += text(900, 780, 'метанол 64,5 °C · этанол 78,3 °C', 't', 'middle')
    return s


# 4. Дегидратация ---------------------------------------------------------------------------------
def dehydration():
    s = text(900, 52, 'Дегидратация этанола: два продукта', 'h', 'middle')
    s += card(30, 90, 1740, 700)
    s += box(900, 190, 420, 90, 'C₂H₅OH + конц. H₂SO₄', '#F7EFC8', cls='t')
    s += arrow(760, 235, 460, 380, BLUE, 6) + arrow(1040, 235, 1340, 380, RED, 6)
    s += text(560, 300, 'сильный нагрев', 's', 'end', BLUE) + text(1240, 300, 'избыток спирта, ниже t', 's', 'start', RED)
    s += box(400, 470, 560, 130, 'C₂H₅OH → CH₂=CH₂ + H₂O|внутримолекулярная|этилен', '#E3EEF7')
    s += box(1400, 470, 600, 130, '2C₂H₅OH → C₂H₅–O–C₂H₅ + H₂O|межмолекулярная|диэтиловый эфир', '#FBE3E4')
    s += text(900, 700, 'Продукт решает условие — подписывай его над стрелкой', 't', 'middle')
    return s


# 5. Производство этанола ---------------------------------------------------------------------------
def ethanol_production():
    s = text(900, 52, 'Как получают этанол', 'h', 'middle')
    s += card(30, 90, 860, 760) + card(910, 90, 860, 760)
    s += text(460, 145, 'Спиртовое брожение', 't', 'middle')
    s += f'<path d="M300 300 H620 V640 Q620 680 580 680 H340 Q300 680 300 640 Z" fill="#F7EFC8" stroke="{INK}" stroke-width="4"/>'
    s += ''.join(f'<ellipse cx="{340 + (j * 53) % 240}" cy="{560 + (j * 37) % 90}" rx="12" ry="9" fill="#E8C547" stroke="{INK}" stroke-width="1.5"/>' for j in range(10))
    s += ''.join(f'<circle cx="{360 + j * 40}" cy="{480 - (j % 3) * 50}" r="9" fill="#fff" stroke="{INK}" stroke-width="2"/>' for j in range(6))
    s += text(640, 600, 'дрожжи', 's') + arrow(460, 290, 460, 210, GREY, 4) + text(490, 230, 'CO₂', 's')
    s += lines_at(460, 760, ['C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂↑', 'из глюкозы, крахмала, целлюлозы'], 's', step=40)
    s += text(1340, 145, 'Гидратация этилена', 't', 'middle')
    s += box(1340, 350, 360, 220, 'контактный|аппарат|H₃PO₄', '#E3EEF7', cls='t')
    s += arrow(1000, 350, 1155, 350, INK, 5) + text(1040, 320, 'C₂H₄ + H₂O', 's')
    s += arrow(1525, 350, 1680, 350, INK, 5) + text(1600, 320, 'C₂H₅OH', 's', 'middle')
    s += lines_at(1340, 560, ['C₂H₄ + H₂O ⇄ C₂H₅OH + Q', '280–300 °C, 7–8 МПа',
                              'давление смещает равновесие к спирту:', 'число молекул газа уменьшается'], 's', step=40)
    return s


# 6. Фенол -----------------------------------------------------------------------------------------
def phenol_tests():
    s = text(900, 52, 'Фенол: –OH прямо на кольце', 'h', 'middle')
    s += card(30, 90, 640, 820) + card(700, 90, 1070, 820)
    ring, pts = hexring(200, 330, 70)
    s += ring + bond(*pts[0], pts[0][0], pts[0][1] - 60) + atom(pts[0][0], pts[0][1] - 80, 'OH', 30, OC)
    s += text(200, 470, 'фенол', 't', 'middle')
    ring, pts = hexring(480, 330, 70)
    s += ring + bond(*pts[0], pts[0][0], pts[0][1] - 50) + atom(pts[0][0], pts[0][1] - 70, 'CH₂', 30, '#9A958C')
    s += bond(pts[0][0], pts[0][1] - 100, pts[0][0], pts[0][1] - 130) + atom(pts[0][0], pts[0][1] - 150, 'OH', 26, OC)
    s += text(480, 470, 'бензиловый спирт', 't', 'middle')
    s += lines_at(350, 560, ['фенол кислее спиртов:', 'реагирует с NaOH', '', 'бензиловый спирт —', 'как обычный спирт'], 's', step=40)
    tests = [('NaOH', '#F1F5F8', None, 'фенолят натрия', INK), ('бромная вода', '#F1F5F8', '#FFFFFF', 'белый осадок', INK),
             ('FeCl₃', '#B35BB8', None, 'фиолетовый', PURPLE)]
    for k, (r, fill, sed, res, col) in enumerate(tests):
        cx = 880 + k * 330
        s += text(cx, 160, r, 't', 'middle') + tube(cx, 190, fill, 300, sed)
        s += text(cx, 560, res, 't', 'middle', col)
    s += lines_at(1235, 660, ['C₆H₅OH + NaOH → C₆H₅ONa + H₂O', 'C₆H₅OH + 3Br₂ → C₆H₂Br₃OH↓ + 3HBr',
                              'бром замещает H в положениях 2, 4, 6 без катализатора'], 's', step=44)
    return s


# 7. Кумольный способ --------------------------------------------------------------------------------
def cumene():
    s = text(900, 52, 'Кумольный способ: фенол и ацетон', 'h', 'middle')
    s += card(30, 90, 1740, 560)
    s += box(220, 330, 300, 110, 'бензол|C₆H₆', '#F7EFC8', cls='t') + text(220, 460, '+ пропилен (AlCl₃)', 's', 'middle')
    s += arrow(380, 330, 560, 330, INK, 6)
    s += box(720, 330, 300, 110, 'кумол|изопропилбензол', '#E3EEF7', cls='t')
    s += arrow(880, 330, 1060, 330, INK, 6) + text(970, 300, 'окисление', 's', 'middle')
    s += box(1260, 260, 360, 90, 'фенол C₆H₅OH', '#FBE3E4', cls='t') + box(1260, 410, 360, 90, 'ацетон CH₃COCH₃', '#E2F1E6', cls='t')
    s += text(1260, 352, '+', 't', 'middle')
    s += text(900, 570, 'Почти весь фенол сейчас получают этим способом; второй продукт — ацетон', 's', 'middle')
    return s


# 8. Карбонильная группа --------------------------------------------------------------------------
def carbonyl():
    s = text(900, 52, 'Карбонильная группа C=O', 'h', 'middle')
    s += card(30, 90, 860, 760) + card(910, 90, 860, 760)
    cx, cy = 460, 420
    s += f'<line x1="{cx - 10}" y1="{cy - 14}" x2="{cx + 150}" y2="{cy - 14}" stroke="{INK}" stroke-width="6"/><line x1="{cx - 10}" y1="{cy + 14}" x2="{cx + 150}" y2="{cy + 14}" stroke="{INK}" stroke-width="6"/>'
    s += bond(cx, cy, cx - 110, cy - 90) + bond(cx, cy, cx - 110, cy + 90)
    s += atom(cx, cy, 'C', 40) + atom(cx + 170, cy, 'O', 40, OC)
    s += text(cx, cy - 70, 'δ+', 't', 'middle', BLUE) + text(cx + 170, cy - 70, 'δ−', 't', 'middle', RED)
    s += text(cx - 140, cy - 100, 'R', 't', 'middle') + text(cx - 140, cy + 120, 'H или R′', 's', 'middle')
    s += lines_at(460, 650, ['σ + π; атом C — sp²', 'связь полярна: δ+ на C, δ− на O'], 's', step=40)
    s += text(1340, 160, 'Альдегиды и кетоны', 't', 'middle')
    rows = [('R–CHO — альдегид, -аль', BLUE), ('HCHO — метаналь, формальдегид', INK), ('CH₃CHO — этаналь, ацетальдегид', INK),
            ('R–CO–R′ — кетон, -он', RED), ('CH₃COCH₃ — пропанон, ацетон', INK)]
    for k, (r, c) in enumerate(rows):
        s += text(1340, 260 + k * 80, r, 't', 'middle', c)
    s += text(1340, 700, 'C₃H₆O — пропаналь и ацетон: межклассовые изомеры', 's', 'middle', GREY)
    return s


# 9. Качественные реакции альдегидов ---------------------------------------------------------------
def aldehyde_tests():
    s = text(900, 52, 'Альдегид или многоатомный спирт: следи за условием', 'h', 'middle')
    s += card(30, 90, 1740, 800)
    items = [('альдегид + Ag₂O (NH₃), t', '#E9EBEE', 'серебряное зеркало', True, None),
             ('альдегид + Cu(OH)₂, t', '#7FB3E0', 'красный осадок Cu₂O', False, '#C0392B'),
             ('глицерин + Cu(OH)₂, без t', '#1F5FD1', 'ярко-синий раствор', False, None),
             ('кетон + Ag₂O (NH₃), t', '#F1F5F8', 'реакции нет', False, None)]
    for k, (title, fill, res, mirror, sed) in enumerate(items):
        cx = 250 + k * 430
        s += lines_at(cx, 160, title.split(', ', 1) if len(title) > 22 else [title], 's', step=32)
        s += tube(cx, 240, fill, 300, sed)
        if mirror:
            s += f'<path d="M{cx - 32} 260 V 500" stroke="#B8BDC4" stroke-width="10"/><path d="M{cx + 32} 260 V 500" stroke="#E8ECF0" stroke-width="10"/>'
        s += text(cx, 600, res, 't', 'middle', RED if 'нет' in res else INK)
    s += lines_at(900, 720, ['CH₃CHO + Ag₂O → CH₃COOH + 2Ag↓;  CH₃CHO + 2Cu(OH)₂ → CH₃COOH + Cu₂O↓ + 2H₂O',
                             'альдегид окисляется до кислоты; кетон не окисляется'], 's', step=44)
    return s


# 10. Таблица распознавания ----------------------------------------------------------------------------
def recognition():
    s = text(900, 52, 'Распознавание: реактив → признак → класс', 'h', 'middle')
    s += card(30, 90, 1120, 1000) + card(1180, 90, 590, 1000)
    rows = [('Na', 'выделяется H₂', 'спирты, фенол'), ('NaOH', 'образуется соль', 'только фенол'),
            ('бромная вода', 'белый осадок', 'фенол'), ('FeCl₃', 'фиолетовое окрашивание', 'фенол'),
            ('Cu(OH)₂, без t', 'ярко-синий раствор', 'многоатомные спирты'), ('Cu(OH)₂, t', 'красный Cu₂O', 'альдегиды'),
            ('Ag₂O (NH₃), t', 'серебряное зеркало', 'альдегиды'), ('медная спираль', 'блестит, запах', 'этанол'),
            ('индикатор', 'не меняется', 'растворы спиртов')]
    s += text(170, 150, 'реактив', 's', 'middle', GREY) + text(500, 150, 'признак', 's', 'middle', GREY) + text(890, 150, 'класс', 's', 'middle', GREY)
    for k, (r, f, c) in enumerate(rows):
        y = 210 + k * 96
        s += f'<rect x="60" y="{y - 38}" width="1060" height="80" rx="12" fill="{"#fff" if k % 2 else "#F7F5EF"}"/>'
        s += text(170, y + 10, r, 's', 'middle') + text(500, y + 10, f, 's', 'middle') + text(890, y + 10, c, 's', 'middle', BLUE)
    s += text(1475, 160, 'Окисление и восстановление', 't', 'middle')
    s += box(1475, 300, 380, 80, 'первичный спирт', '#E3EEF7') + box(1475, 480, 380, 80, 'альдегид', '#F7EFC8')
    s += box(1475, 660, 380, 80, 'карбоновая кислота', '#FBE3E4')
    s += arrow(1440, 345, 1440, 435, RED, 5) + arrow(1510, 435, 1510, 345, BLUE, 5)
    s += arrow(1475, 525, 1475, 615, RED, 5)
    s += text(1420, 400, '[O]', 's', 'end', RED) + text(1530, 400, '+H₂', 's', 'start', BLUE) + text(1500, 580, '[O]', 's', 'start', RED)
    s += box(1475, 840, 380, 80, 'вторичный спирт ⇄ кетон', '#E2F1E6')
    s += text(1475, 940, 'кетон дальше не окисляется', 's', 'middle', GREY)
    return s


if __name__ == '__main__':
    jobs = {
        'haloalkane-alkali.png': (haloalkane_alkali(), 1800, 820),
        'alcohol-classes.png': (alcohol_classes(), 1800, 940),
        'hydrogen-bonds.png': (hydrogen_bonds(), 1800, 880),
        'dehydration.png': (dehydration(), 1800, 820),
        'ethanol-production.png': (ethanol_production(), 1800, 880),
        'phenol-tests.png': (phenol_tests(), 1800, 940),
        'cumene.png': (cumene(), 1800, 680),
        'carbonyl.png': (carbonyl(), 1800, 880),
        'aldehyde-tests.png': (aldehyde_tests(), 1800, 920),
        'recognition.png': (recognition(), 1800, 1120),
    }
    only = set(sys.argv[1:])
    for name, (svg, w, h) in jobs.items():
        if only and name not in only:
            continue
        render(svg, w, h, OUT / name)
        print(OUT / name)
