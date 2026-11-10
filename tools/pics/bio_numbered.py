"""Рисунки с номерами для книги «Конспект ЕНТ: биология»: вопросы «что показано под цифрой N», как в блоке 36–40 ЕНТ.

Подробные схемы в стиле рисунков недель (органоиды и цвета из common.py и bio_w01.py, синий и красный — из bio_w06.py).
Вопросы и ответы — course/biology/week-NN/pic-quiz.json, книга собирает их в конец главы и в раздел ответов.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_numbered.py
"""
from __future__ import annotations

import math
import sys

import bio_w08
import bio_w09
import bio_w10
import bio_w13
from bio_w01 import chloro, mito, ribosomes
from bio_w06 import BLUE, LBLUE, LRED, RED
from common import INK, ROOT, render, smooth, text

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


def numbered(module, fn, nums: dict, extra: str = '', dx: float = 0, dy: float = 0, drop: tuple = ()) -> str:
    """Рисунок недели с номерами вместо подписей: тот же рисунок из bio_wNN.py, выноски из nums получают номер,
    все прочие подписи и заголовок убираются, чтобы ответ не был виден. nums: подпись → номер или (номер, x, y);
    drop — ещё функции рисунка, которые нужно убрать (например, стрелки-подсказки)."""
    names = [k for k in ('lbl', 'label', 'text', 'lines_at', *drop) if hasattr(module, k)]
    saved = {k: getattr(module, k) for k in names}
    used = set()

    def callout(px, py, tx, ty, s, *a, **k):
        v = nums.get(s)
        if v is None:
            return ''
        used.add(s)
        n, tx, ty = (v, tx, ty) if isinstance(v, int) else v
        return num(px, py, tx, ty, n)

    for k in names:
        setattr(module, k, callout if k in ('lbl', 'label') else (lambda *a, **kw: ''))
    try:
        svg = fn()
    finally:
        for k, v in saved.items():
            setattr(module, k, v)
    assert used == set(nums), set(nums) - used
    return f'<g transform="translate({dx} {dy})">{svg}{extra}</g>'


def urinary_numbered() -> str:
    """1 почка, 2 надпочечник, 3 мочеточник, 4 почечная артерия, 5 мочевой пузырь, 6 почечная вена, 7 мочеиспускательный канал."""
    return numbered(bio_w08, bio_w08.urinary_system, {'почка': 1, 'надпочечник': 2, 'мочеточник': 3, 'почечная артерия': 4,
                                                      'мочевой пузырь': 5, 'почечная вена': 6, 'мочеиспускательный канал': 7}, dy=-60)


def kidney_numbered() -> str:
    """1 пирамидка мозгового слоя, 2 корковый слой, 3 чашечка, 4 почечная вена, 5 лоханка, 6 мочеточник, 7 почечная артерия."""
    extra = num(1180, 400, 1300, 330, 7) + num(1180, 440, 1300, 530, 4)
    return numbered(bio_w08, bio_w08.kidney_section, {'мозговой слой: пирамидки': 1, 'корковый слой': 2, 'чашечка': 3, 'лоханка': 5,
                                                      'мочеточник': 6}, extra, dy=-40)


def nephron_numbered() -> str:
    """1 клубочек, 2 капсула, 3 приносящая артериола, 4 выносящая артериола, 5 проксимальный извитой каналец, 6 петля Генле,
    7 дистальный извитой каналец, 8 собирательная трубка, 9 капилляры вокруг канальцев."""
    return numbered(bio_w08, bio_w08.nephron, {'клубочек': 1, 'капсула': 2, 'выносящая': (4, 560, 104), 'проксимальный извитой каналец': 5,
                                               'петля Генле': 6, 'дистальный извитой каналец': 7, 'собирательная трубка': 8,
                                               'капилляры вокруг канальцев': 9}, num(200, 197, 92, 112, 3), dy=-50)


def skeleton_numbered() -> str:
    """1 мозговой отдел черепа, 2 лицевой отдел, 3 ключица, 4 грудина, 5 рёбра, 6 лопатка, 7 позвоночник, 8 плечевая кость,
    9 локтевая, 10 лучевая, 11 кисть, 12 тазовая кость, 13 бедренная, 14 надколенник, 15 большая берцовая, 16 малая берцовая, 17 стопа."""
    # локтевая — внутренняя кость предплечья, лучевая — наружная; большая берцовая — внутренняя и толстая, малая — наружная и тонкая
    extra = ('<g transform="translate(100 0)">' + num(431, 740, 330, 770, 9) + num(418, 700, 330, 650, 10)
             + num(578, 1200, 650, 1215, 15) + num(551, 1215, 330, 1200, 16) + '</g>')
    return numbered(bio_w09, bio_w09.skeleton, {'череп: мозговой отдел': 1, 'лицевой отдел': 2, 'ключица (плечевой пояс)': 3, 'грудина': 4,
                                                'рёбра — 12 пар': 5, 'лопатка (плечевой пояс)': 6, 'позвоночник': 7, 'плечевая кость': 8,
                                                'кисть': 11, 'тазовая кость (3 сросшиеся)': 12, 'бедренная кость': 13, 'надколенник': 14,
                                                'стопа': 17}, extra, dy=-40)


def neuron_numbered() -> str:
    """1 дендриты, 2 ядро, 3 перехват Ранвье, 4 тело нейрона, 5 аксон, 6 миелиновая оболочка, 7 окончания аксона."""
    # стрелки направления импульса убраны: о направлении есть вопрос; выноска тела — сверху, чтобы не попасть на дендрит
    return numbered(bio_w10, bio_w10.neuron, {'дендриты': 1, 'ядро': 2, 'перехват Ранвье': 3, 'аксон': 5,
                                              'миелиновая оболочка (шванновская клетка)': 6, 'окончания → синапсы': 7},
                    '<g transform="translate(150 0)">' + num(295, 262, 410, 80, 4) + '</g>', drop=('arrow',))


def brain_numbered() -> str:
    """Продольный разрез головного мозга, крупно (формы — из bio_w10.brain_cortex): 1 большие полушария, 2 мозжечок,
    3 промежуточный мозг, 4 продолговатый мозг, 5 средний мозг, 6 мост."""
    k, ox, oy = 1.6, 84, -136
    p = lambda x, y: (ox + k * x, oy + k * y)
    s = f'<g transform="translate({ox} {oy}) scale({k})">'
    s += f'<path d="{smooth([(110, 300), (160, 170), (330, 120), (520, 150), (600, 260), (560, 380), (420, 410), (250, 400), (150, 380)], True)}" fill="#F6D7D2" stroke="#A2463C" stroke-width="3"/>'
    s += ''.join(f'<path d="M{x1} {y1} q 30 {20 + j * 4} 70 {6 - j * 3}" fill="none" stroke="#C98478" stroke-width="2"/>'
                 for j, (x1, y1) in enumerate(((180, 210), (260, 170), (360, 160), (450, 190), (200, 300), (300, 260), (420, 270), (500, 300))))
    s += '<ellipse cx="380" cy="360" rx="60" ry="34" fill="#F2C14E" stroke="#8A6A2A" stroke-width="2"/>'
    s += '<ellipse cx="420" cy="410" rx="40" ry="26" fill="#9CCB86" stroke="#2E7D4F" stroke-width="2"/>'
    s += f'<path d="{smooth([(470, 420), (560, 400), (600, 460), (520, 500), (460, 480)], True)}" fill="#C7A6E0" stroke="#5B4A8A" stroke-width="2"/>'
    s += ''.join(f'<path d="M{480 + j * 4} {430 + j * 14} q 50 -10 100 {8 + j * 6}" fill="none" stroke="#5B4A8A" stroke-width="1.5"/>' for j in range(4))
    s += '<ellipse cx="440" cy="455" rx="34" ry="22" fill="#7FB3D5" stroke="#3A57A7" stroke-width="2"/>'
    s += '<path d="M430 470 Q 420 520 425 590" stroke="#7FB3D5" stroke-width="30" fill="none"/></g>'
    s += num(*p(300, 220), 200, 150, 1) + num(*p(545, 450), 1150, 560, 2) + num(*p(370, 360), 200, 470, 3)
    s += num(*p(427, 560), 1150, 800, 4) + num(*p(420, 410), 200, 600, 5) + num(*p(452, 457), 200, 730, 6)
    return s


def eye_numbered() -> str:
    """1 роговица, 2 радужка со зрачком, 3 хрусталик, 4 стекловидное тело, 5 сетчатка, 6 сосудистая оболочка, 7 склера,
    8 жёлтое пятно, 9 зрительный нерв (место выхода — слепое пятно). Врезки с очками обрезаны шириной холста."""
    cx, cy = 600, 360
    # три оболочки задней части глаза толще, чем на рисунке недели, чтобы их было видно по отдельности;
    # сосудистая оболочка — между склерой и сетчаткой, спереди переходит в радужку
    a1, a2 = math.radians(-148), math.radians(148)
    pt = lambda r, deg: (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))
    rings = ''.join(f'<path d="M{cx + r * math.cos(a1):.0f} {cy + r * math.sin(a1):.0f} A {r} {r} 0 1 1 {cx + r * math.cos(a2):.0f} '
                    f'{cy + r * math.sin(a2):.0f}" fill="none" stroke="{c}" stroke-width="{w}"/>'
                    for r, c, w in ((235, '#B59A6E', 10), (225, '#7A3B2E', 9), (215, '#D9705F', 8)))
    extra = (f'<g transform="translate(90 0)">{rings}<circle cx="{cx + 216}" cy="{cy}" r="10" fill="#F2C14E" stroke="#8A6A2A" stroke-width="2"/>'
             + num(*pt(235, -45), 890, 105, 7) + num(*pt(215, -20), 905, 195, 5) + num(*pt(225, 40), 960, 590, 6)
             + num(cx + 216, cy, 960, 290, 8) + num(343, 285, 300, 165, 1) + '</g>')  # роговица — точка на самой дуге
    return numbered(bio_w10, bio_w10.eye_optics, {'радужка, зрачок': 2, 'хрусталик (аккомодация)': 3, 'стекловидное тело': 4,
                                                  'слепое пятно, зрительный нерв': 9}, extra, dy=-40)


def flower_numbered() -> str:
    """1 цветоножка, 2 цветоложе, 3 чашелистик, 4 лепесток, 5 пыльник, 6 тычиночная нить, 7 рыльце, 8 столбик, 9 завязь, 10 семязачаток."""
    return numbered(bio_w13, bio_w13.flower, {'цветоножка': 1, 'цветоложе': 2, 'чашелистик': 3, 'лепесток': 4, 'пыльник': 5,
                                              'тычиночная нить': 6, 'рыльце': 7, 'столбик': 8, 'завязь': 9, 'семязачаток': 10}, dx=-150, dy=-170)


if __name__ == '__main__':
    jobs = {BIO / 'week-01' / 'pics' / 'cell-animal-numbered.png': (animal_cell(), 1600, 900),
            BIO / 'week-01' / 'pics' / 'cell-plant-numbered.png': (plant_cell(), 1400, 900),
            BIO / 'week-06' / 'pics' / 'heart-numbered.png': (heart_numbered(), 1400, 1060),
            BIO / 'week-08' / 'pics' / 'urinary-numbered.png': (urinary_numbered(), 1120, 900),
            BIO / 'week-08' / 'pics' / 'kidney-numbered.png': (kidney_numbered(), 1400, 860),
            BIO / 'week-08' / 'pics' / 'nephron-numbered.png': (nephron_numbered(), 1180, 810),
            BIO / 'week-09' / 'pics' / 'skeleton-numbered.png': (skeleton_numbered(), 1200, 1360),
            BIO / 'week-10' / 'pics' / 'neuron-numbered.png': (neuron_numbered(), 1650, 510),
            BIO / 'week-10' / 'pics' / 'brain-numbered.png': (brain_numbered(), 1300, 860),
            BIO / 'week-10' / 'pics' / 'eye-numbered.png': (eye_numbered(), 1300, 680),
            BIO / 'week-13' / 'pics' / 'flower-numbered.png': (flower_numbered(), 1250, 740)}
    only = set(sys.argv[1:])
    jobs = {k: v for k, v in jobs.items() if not only or any(o in k.name for o in only)}
    for out, (svg, w, h) in jobs.items():
        render(svg, w, h, out)
        print(out)
