"""Рисунки с номерами для книги «Конспект ЕНТ: биология»: вопросы «что показано под цифрой N», как в блоке 36–40 ЕНТ.

Подробные схемы в стиле рисунков недель (органоиды и цвета из common.py и bio_w01.py, синий и красный — из bio_w06.py).
Вопросы и ответы — course/biology/week-NN/pic-quiz.json, книга собирает их в конец главы и в раздел ответов.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_numbered.py
"""
from __future__ import annotations

from bio_w01 import chloro, mito, ribosomes
from bio_w06 import BLUE, LBLUE, LRED, RED
from common import INK, ROOT, render, text

BIO = ROOT / 'course' / 'biology'
MUSCLE = '#E9B3AE'


def num(px: float, py: float, tx: float, ty: float, n: int) -> str:
    """Выноска от точки на объекте к кружку с номером."""
    return (f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{INK}" stroke-width="2.5"/>'
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{INK}"/>'
            f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="26" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            + text(tx, ty + 11, str(n), 'h', 'middle'))


def nucleus2(cx: float, cy: float, r: float) -> str:
    """Ядро: двойная оболочка с порами, хроматин, ядрышко."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#E3E4F4" stroke="#3A57A7" stroke-width="5"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r - 9}" fill="none" stroke="#3A57A7" stroke-width="2.5"/>'
    for a in range(0, 360, 40):
        s += f'<rect x="{cx - 5}" y="{cy - r - 4}" width="10" height="16" fill="#E3E4F4" transform="rotate({a} {cx} {cy})"/>'
    s += ''.join(f'<path d="M{cx - r * 0.55 + k * r * 0.22:.0f} {cy - r * 0.45:.0f} q {r * 0.18:.0f} {r * 0.35:.0f} 0 {r * 0.8:.0f}" '
                 f'fill="none" stroke="#3A57A7" stroke-width="3"/>' for k in range(6))
    s += f'<circle cx="{cx + r * 0.25:.0f}" cy="{cy - r * 0.1:.0f}" r="{r * 0.28:.0f}" fill="#4B5BA8"/>'
    return s


def lysosome(cx: float, cy: float, r: float = 17) -> str:
    dots = ''.join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="3" fill="#7A3E12"/>' for dx, dy in ((-6, -4), (5, -6), (0, 5), (7, 4)))
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#F3C969" stroke="#A86F12" stroke-width="3"/>' + dots


def centrioles(cx: float, cy: float) -> str:
    """Клеточный центр: две центриоли под прямым углом."""
    bars = ''.join(f'<line x1="{cx - 26 + k * 13}" y1="{cy - 14}" x2="{cx - 26 + k * 13}" y2="{cy + 14}" stroke="#2E6B4F" stroke-width="3"/>' for k in range(5))
    bars2 = ''.join(f'<line x1="{cx + 20}" y1="{cy + 22 + k * 11}" x2="{cx + 48}" y2="{cy + 22 + k * 11}" stroke="#2E6B4F" stroke-width="3"/>' for k in range(5))
    return (f'<rect x="{cx - 32}" y="{cy - 18}" width="64" height="36" rx="8" fill="#CFE8DA" stroke="#2E6B4F" stroke-width="3"/>{bars}'
            f'<rect x="{cx + 16}" y="{cy + 14}" width="36" height="58" rx="8" fill="#CFE8DA" stroke="#2E6B4F" stroke-width="3"/>{bars2}')


def golgi(x: float, y: float) -> str:
    s = ''.join(f'<path d="M{x + k * 6} {y + k * 20} q 80 -34 160 0" fill="none" stroke="#C7891B" stroke-width="8" stroke-linecap="round"/>' for k in range(5))
    s += ''.join(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#F7E1B2" stroke="#C7891B" stroke-width="3"/>'
                 for cx, cy in ((x + 180, y + 10), (x + 190, y + 48), (x - 18, y + 60), (x + 178, y + 92)))
    return s


def animal_cell() -> str:
    """1 гладкая ЭПС, 2 ядрышко, 3 клеточный центр, 4 митохондрия, 5 мембрана, 6 аппарат Гольджи, 7 лизосома,
    8 шероховатая ЭПС, 9 ядро, 10 рибосомы, 11 цитоплазма."""
    s = ('<path d="M380 470 C360 250 560 130 810 130 C1080 130 1260 250 1240 480 C1220 690 1040 800 810 800 '
         'C560 800 400 670 380 470 Z" fill="#FDF3EA" stroke="#3B3833" stroke-width="9"/>')
    s += ('<path d="M392 470 C372 258 566 142 810 142 C1074 142 1248 258 1228 480 C1208 680 1034 788 810 788 '
          'C566 788 412 662 392 470 Z" fill="none" stroke="#3B3833" stroke-width="2"/>')
    s += nucleus2(800, 450, 120)
    for k in range(5):  # шероховатая ЭПС
        y = 260 + k * 24
        s += f'<path d="M500 {y} q 30 -18 60 0 t 60 0 t 60 0" fill="none" stroke="#7A4FA3" stroke-width="5"/>'
        s += ribosomes([(505 + j * 22, y - 7 + (j % 2) * 12) for j in range(9)])
    for k in range(4):  # гладкая ЭПС
        y = 590 + k * 26
        s += f'<path d="M470 {y} q 35 -22 70 0 t 70 0 t 70 0" fill="none" stroke="#9C6BC4" stroke-width="7" stroke-linecap="round"/>'
    s += golgi(990, 560)
    s += mito(1060, 330, 50, 22, -25) + mito(640, 720, 46, 20, 10) + mito(1120, 470, 42, 18, 80)
    s += lysosome(950, 700) + lysosome(1000, 740) + lysosome(560, 520)
    s += centrioles(960, 240)
    s += ribosomes([(700, 640), (880, 640), (1150, 600), (620, 420), (720, 230), (1180, 380), (860, 260)])
    s += num(540, 616, 300, 690, 1) + num(830, 440, 640, 120, 2) + num(960, 240, 1180, 150, 3) + num(1060, 330, 1330, 280, 4)
    s += num(1236, 520, 1360, 560, 5) + num(1060, 600, 1340, 700, 6) + num(1000, 740, 1110, 850, 7) + num(560, 268, 330, 220, 8)
    s += num(720, 520, 690, 870, 9) + num(700, 640, 520, 860, 10) + num(450, 420, 285, 440, 11)
    return s


def plant_cell() -> str:
    """1 хлоропласт, 2 ядро, 3 клеточная стенка, 4 центральная вакуоль, 5 мембрана, 6 митохондрия, 7 ядрышко,
    8 аппарат Гольджи, 9 цитоплазма."""
    s = '<rect x="400" y="130" width="600" height="640" rx="22" fill="#E7F0D9" stroke="#5B7A2A" stroke-width="22"/>'
    for x, y, w, h in ((600, 120, 26, 22), (820, 120, 26, 22), (390, 400, 22, 26), (990, 520, 22, 26), (700, 760, 26, 22)):
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#F4F9EE"/>'  # поры в стенке
    s += '<rect x="422" y="152" width="556" height="596" rx="14" fill="#F4F9EE" stroke="#3B3833" stroke-width="3"/>'
    s += '<path d="M520 300 C520 250 560 230 640 232 L800 236 C880 240 900 280 896 340 L890 600 C886 660 850 680 790 680 L620 676 C550 672 516 640 518 580 Z" fill="#DDEBF7" stroke="#3A6E9B" stroke-width="5"/>'
    s += nucleus2(905, 225, 55)
    s += ''.join(chloro(x, y, 34, 18, r) for x, y, r in [(465, 260, 80), (465, 430, 95), (470, 600, 85), (940, 380, 95), (940, 560, 80),
                                                       (600, 715, 0), (780, 715, 8), (650, 190, 0)])
    s += mito(930, 690, 30, 14, 60) + mito(780, 190, 30, 14, 10)
    s += ''.join(f'<path d="M{575 + k * 5} {705 - 60 - k * 14} q 50 -22 100 0" fill="none" stroke="#C7891B" stroke-width="6" stroke-linecap="round"/>' for k in range(0))
    s += ''.join(f'<path d="M{850 + k * 5} {470 + k * 16} q 40 -18 80 0" fill="none" stroke="#C7891B" stroke-width="6" stroke-linecap="round"/>' for k in range(4))
    s += ribosomes([(560, 690), (700, 200), (880, 300), (470, 520), (960, 470)])
    s += num(465, 430, 280, 400, 1) + num(876, 252, 1110, 160, 2) + num(408, 700, 260, 760, 3) + num(700, 450, 700, 870, 4)
    s += num(424, 300, 260, 260, 5) + num(930, 690, 1120, 760, 6) + num(919, 221, 1120, 300, 7) + num(890, 490, 1120, 520, 8)
    s += num(520, 690, 430, 860, 9)
    return s


def heart_numbered() -> str:
    """Сердце в разрезе, вид спереди: 1 верхняя полая вена, 2 аорта, 3 лёгочный ствол, 4 лёгочные вены, 5 левое предсердие,
    6 правое предсердие, 7 двустворчатый клапан, 8 трёхстворчатый клапан, 9 полулунный клапан, 10 левый желудочек,
    11 межжелудочковая перегородка, 12 правый желудочек, 13 нижняя полая вена."""
    s = ''
    # аорта: выходит из левого желудочка, дуга над сердцем, ветви вверх
    s += f'<path d="M780 560 V 210 C780 120 840 80 920 80 C1010 80 1060 130 1060 210 V 330" fill="none" stroke="{RED}" stroke-width="56"/>'
    s += ''.join(f'<path d="M{x} {y} V 20" stroke="{RED}" stroke-width="18"/>' for x, y in ((870, 70), (930, 62), (990, 72)))
    # лёгочный ствол: из правого желудочка, делится на две лёгочные артерии
    s += f'<path d="M650 560 V 250 L 520 180 M650 250 L 700 200 L 1120 200" fill="none" stroke="{BLUE}" stroke-width="44" stroke-linejoin="round"/>'
    s += f'<path d="M780 560 V 230" fill="none" stroke="{RED}" stroke-width="56"/>'  # аорта поверх ветви лёгочной артерии
    # полые вены
    s += f'<path d="M470 110 V 330" stroke="{BLUE}" stroke-width="54"/>'
    s += f'<path d="M330 1010 V 600 C330 540 360 520 400 520" fill="none" stroke="{BLUE}" stroke-width="54"/>'
    # лёгочные вены
    s += f'<path d="M1010 360 H 1170 M1010 450 H 1170" stroke="{RED}" stroke-width="30"/>'
    # предсердия
    s += f'<path d="M380 340 C380 300 410 290 450 290 L620 290 C650 290 660 310 660 340 L660 500 L380 500 Z" fill="{LBLUE}" stroke="{BLUE}" stroke-width="7"/>'
    s += f'<path d="M740 340 C740 300 760 290 800 290 L990 290 C1020 290 1030 310 1030 340 L1030 500 L740 500 Z" fill="{LRED}" stroke="{RED}" stroke-width="7"/>'
    # желудочки и перегородка; стенка левого желудочка толще
    s += f'<path d="M380 520 L 680 520 L 690 900 C 600 860 420 760 380 600 Z" fill="{LBLUE}" stroke="{BLUE}" stroke-width="10"/>'
    s += f'<path d="M730 520 L 1030 520 C 1050 760 900 900 760 950 L 730 905 Z" fill="{MUSCLE}" stroke="{RED}" stroke-width="10"/>'
    s += f'<path d="M760 545 L 1000 545 C 1015 740 890 860 770 905 Z" fill="{LRED}"/>'
    s += f'<path d="M680 520 L 730 520 L 730 905 L 690 900 Z" fill="{MUSCLE}" stroke="#B5524A" stroke-width="3"/>'
    # клапаны
    for x in (450, 510, 570):
        s += f'<path d="M{x - 18} 500 L {x} 548 L {x + 18} 500 Z" fill="#fff" stroke="{BLUE}" stroke-width="3"/>'
    for x in (860, 930):
        s += f'<path d="M{x - 20} 500 L {x} 552 L {x + 20} 500 Z" fill="#fff" stroke="{RED}" stroke-width="3"/>'
    for x, c in ((650, BLUE), (780, RED)):
        s += f'<path d="M{x - 20} 575 q 10 -22 20 0 q 10 -22 20 0" fill="#fff" stroke="{c}" stroke-width="3"/>'
    s += num(470, 160, 300, 120, 1) + num(900, 82, 1240, 110, 2) + num(650, 268, 560, 50, 3) + num(1170, 450, 1260, 520, 4)
    s += num(900, 380, 1240, 330, 5) + num(470, 380, 250, 380, 6) + num(930, 520, 1230, 640, 7) + num(510, 520, 250, 560, 8)
    s += num(780, 575, 600, 660, 9) + num(880, 720, 1180, 820, 10) + num(708, 800, 820, 1010, 11) + num(520, 700, 230, 760, 12)
    s += num(330, 950, 200, 990, 13)
    s += text(560, 1040, '← правая сторона тела', 'cap', 'end') + text(860, 1040, 'левая сторона тела →', 'cap')
    return s


if __name__ == '__main__':
    jobs = {BIO / 'week-01' / 'pics' / 'cell-animal-numbered.png': (animal_cell(), 1600, 900),
            BIO / 'week-01' / 'pics' / 'cell-plant-numbered.png': (plant_cell(), 1400, 900),
            BIO / 'week-06' / 'pics' / 'heart-numbered.png': (heart_numbered(), 1400, 1060)}
    for out, (svg, w, h) in jobs.items():
        render(svg, w, h, out)
        print(out)
