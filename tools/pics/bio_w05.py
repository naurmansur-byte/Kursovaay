"""Рисунки недели 5 биологии (course/biology/week-05/pics/*.png): желудок жвачного, пищеварительная система, путь пищи, ворсинка, зуб.

Факты — по выжимке course/textbooks/bio-05-nutrition.md (Б8 § 10–13, Б9 § 10, 12). Схемы условные, не анатомический атлас.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_w05.py
"""
from __future__ import annotations

import math

from common import GREEN, GREY, INK, LIGHT_GREEN, LIGHT_YELLOW, PAPER, RED, ROOT, arrow, lab, label, render, smooth, text

OUT = ROOT / 'course' / 'biology' / 'week-05' / 'pics'
PINK, PINK_LINE, BLUE, YELLOW_LINE = '#F6C9C2', '#B85C4E', '#3A57A7', '#C79A1B'
LIVER, LIVER_LINE = '#B9785E', '#7A4630'


def blob(points, fill, stroke, w=5):
    return f'<path d="{smooth(points, closed=True)}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'


def ruminant_stomach() -> str:
    s = text(800, 60, 'Желудок жвачного: четыре отдела', 'h', 'middle')
    # пищевод сверху
    s += f'<path d="M640 110 C640 170 660 200 700 230" fill="none" stroke="{PINK_LINE}" stroke-width="34" stroke-linecap="round"/>'
    s += text(560, 140, 'пищевод', 's', 'end')
    # рубец — самый большой
    s += blob([(300, 300), (520, 230), (700, 260), (760, 380), (720, 540), (520, 610), (320, 590), (220, 460)], PINK, PINK_LINE)
    s += text(490, 400, 'РУБЕЦ', 't', 'middle')
    s += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="5" fill="{GREEN}" transform="rotate({(x * 7) % 60 - 30} {x} {y})"/>'
                 for x, y in ((360, 470), (400, 500), (450, 470), (500, 520), (560, 480), (610, 510), (420, 540), (540, 550), (330, 420), (640, 450)))
    s += text(490, 590, 'микроорганизмы', 's', 'middle', GREEN)
    # сетка — ячейки
    s += blob([(780, 250), (880, 230), (950, 290), (930, 370), (840, 380), (780, 330)], '#F2DDA9', YELLOW_LINE)
    s += ''.join(f'<path d="M{x} {y} l12 -8 l12 8 l0 14 l-12 8 l-12 -8 Z" fill="none" stroke="{YELLOW_LINE}" stroke-width="2"/>'
                 for x in range(805, 915, 26) for y in range(275, 350, 30))
    s += text(865, 222, 'СЕТКА', 't', 'middle')
    # книжка — складки
    s += blob([(990, 330), (1090, 300), (1170, 350), (1160, 450), (1070, 480), (990, 430)], '#E7D9C8', '#8A6D4E')
    s += ''.join(f'<path d="M{1010 + k * 26} 345 q 10 50 0 110" fill="none" stroke="#8A6D4E" stroke-width="3"/>' for k in range(6))
    s += text(1080, 280, 'КНИЖКА', 't', 'middle')
    # сычуг — вытянутый, переходит в кишечник
    s += blob([(1150, 480), (1260, 450), (1360, 490), (1420, 560), (1380, 620), (1260, 610), (1170, 560)], '#F3B7AE', RED)
    s += text(1290, 660, 'СЫЧУГ', 't', 'middle')
    s += f'<path d="M1415 575 C1480 580 1520 620 1530 690" fill="none" stroke="{PINK_LINE}" stroke-width="26" stroke-linecap="round"/>'
    s += text(1540, 735, 'кишечник', 's', 'end')
    # стрелки пути
    s += arrow(700, 250, 790, 285, INK, 5) + arrow(940, 350, 995, 380, INK, 5) + arrow(1150, 450, 1185, 495, INK, 5)
    s += (f'<path d="M820 240 C 780 160 720 140 680 150" fill="none" stroke="{GREEN}" stroke-width="5" stroke-dasharray="12 8"/>'
          + arrow(700, 147, 676, 151, GREEN, 5))
    s += text(760, 130, 'жвачка: отрыгивает и пережёвывает снова', 's', 'start', GREEN)
    # подписи ролей
    s += text(110, 680, 'Рубец — самый большой: бактерии и одноклеточные помогают переваривать клетчатку', 's')
    s += text(110, 718, 'Книжка — складки, всасывается часть жидкости · Сычуг — настоящий желудок с желудочным соком', 's')
    return s


def digestive_system() -> str:
    s = text(700, 60, 'Пищеварительная система человека', 'h', 'middle')
    # рот и слюнные железы
    s += f'<rect x="600" y="110" width="200" height="90" rx="40" fill="{PINK}" stroke="{PINK_LINE}" stroke-width="5"/>' + text(700, 165, 'рот', 's', 'middle')
    glands = [(560, 120), (575, 190), (840, 120), (825, 190), (640, 225), (760, 225)]
    s += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="26" ry="18" fill="{LIGHT_YELLOW}" stroke="{YELLOW_LINE}" stroke-width="4"/>' for x, y in glands)
    s += label(534, 120, 470, 120, 'слюнные железы — 3 пары', 's')
    # глотка, пищевод
    s += f'<path d="M700 200 L700 430" stroke="{PINK_LINE}" stroke-width="28" stroke-linecap="round"/>'
    s += label(700, 330, 520, 330, 'пищевод', 's')
    # желудок
    s += blob([(700, 430), (820, 420), (930, 470), (950, 560), (880, 620), (790, 600), (760, 530), (700, 480)], PINK, PINK_LINE)
    s += text(860, 530, 'желудок', 's', 'middle')
    # печень и желчный пузырь
    s += blob([(380, 420), (620, 400), (690, 450), (640, 540), (470, 570), (370, 520)], LIVER, LIVER_LINE)
    s += text(520, 490, 'печень', 's', 'middle', '#fff')
    s += f'<ellipse cx="610" cy="580" rx="30" ry="20" fill="#8DBF6B" stroke="#4F7A2D" stroke-width="4"/>'
    s += label(590, 590, 420, 640, 'желчный пузырь', 's')
    # поджелудочная
    s += blob([(720, 660), (900, 640), (1000, 660), (990, 700), (860, 705), (730, 700)], '#F2DDA9', YELLOW_LINE)
    s += label(960, 680, 1030, 620, 'поджелудочная железа', 's')
    # двенадцатиперстная кишка (C-петля) и протоки
    s += f'<path d="M790 600 C 700 620 650 700 690 760 C 720 800 800 790 830 760" fill="none" stroke="{PINK_LINE}" stroke-width="24" stroke-linecap="round"/>'
    s += f'<path d="M610 600 C 640 650 660 700 690 720" fill="none" stroke="#4F7A2D" stroke-width="5"/>'
    s += f'<path d="M730 690 C 715 700 700 712 692 722" fill="none" stroke="{YELLOW_LINE}" stroke-width="5"/>'
    s += f'<circle cx="690" cy="722" r="8" fill="{RED}"/>'
    s += label(690, 722, 500, 745, 'протоки — в 12-перстную кишку', 's')
    # тонкий кишечник — петли
    loops = [(600, 840), (700, 820), (800, 850), (880, 830), (860, 900), (760, 920), (660, 900), (600, 960), (700, 990), (800, 980), (880, 1000)]
    s += f'<path d="{smooth(loops)}" fill="none" stroke="{PINK_LINE}" stroke-width="22" stroke-linecap="round"/>'
    s += label(820, 975, 1030, 900, 'тонкий кишечник', 's')
    # толстый кишечник рамкой, слепая кишка, аппендикс
    s += (f'<path d="M520 1050 L520 820 C520 790 540 780 570 780 L940 780 C970 780 990 790 990 820 L990 1080 C990 1110 970 1120 940 1120 L760 1120 L760 1200" '
          f'fill="none" stroke="#C98A5A" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>')
    s += f'<path d="M520 1050 C520 1090 500 1110 470 1120" fill="none" stroke="#C98A5A" stroke-width="22" stroke-linecap="round"/>'
    s += f'<path d="M475 1125 q -10 40 10 70" fill="none" stroke="#C98A5A" stroke-width="10" stroke-linecap="round"/>'
    s += label(508, 1040, 400, 980, 'слепая кишка', 's')
    s += label(485, 1190, 400, 1240, 'аппендикс', 's')
    s += label(1003, 1040, 1030, 1070, 'толстый кишечник', 's')
    s += label(770, 1190, 900, 1240, 'прямая кишка', 's')
    return s


def food_path() -> str:
    s = text(800, 60, 'Путь пищи: что, где и чем расщепляется', 'h', 'middle')
    boxes = [('Рот', ['амилаза: крахмал →', 'мальтоза'], PINK),
             ('Желудок', ['пепсин начинает', 'расщепление белков', '+ соляная кислота'], PINK),
             ('12-перстная кишка', ['желчь эмульгирует', 'жиры', 'трипсин — белки', 'липаза — жиры', 'амилаза — углеводы'], LIGHT_YELLOW),
             ('Тонкий кишечник', ['окончательное', 'переваривание,', 'всасывание', 'через ворсинки'], LIGHT_GREEN),
             ('Толстый кишечник', ['вода, соли,', 'витамины;', 'микрофлора —', 'клетчатка'], PAPER)]
    w, gap, x0, y0 = 272, 36, 40, 120
    for k, (title, lines, fill) in enumerate(boxes):
        x = x0 + k * (w + gap)
        s += f'<rect x="{x}" y="{y0}" width="{w}" height="300" rx="16" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
        s += text(x + w / 2, y0 + 48, title, 't' if len(title) < 14 else 's', 'middle')
        s += ''.join(text(x + w / 2, y0 + 105 + j * 36, ln, 's', 'middle') for j, ln in enumerate(lines))
        if k < 4:
            s += arrow(x + w + 4, y0 + 150, x + w + gap - 4, y0 + 150, INK, 5)
    # всасывание
    cx = x0 + 3 * (w + gap) + w / 2
    s += arrow(cx - 60, y0 + 305, cx - 200, 600, RED, 6) + arrow(cx + 60, y0 + 305, cx + 200, 600, YELLOW_LINE, 6)
    s += f'<rect x="{cx - 420}" y="610" width="360" height="120" rx="16" fill="#FBE3E4" stroke="{RED}" stroke-width="4"/>'
    s += text(cx - 240, 660, 'в КРОВЬ', 't', 'middle', RED) + text(cx - 240, 700, 'глюкоза, аминокислоты', 's', 'middle')
    s += f'<rect x="{cx + 30}" y="610" width="420" height="120" rx="16" fill="#FFF4D6" stroke="{YELLOW_LINE}" stroke-width="4"/>'
    s += text(cx + 240, 655, 'в ЛИМФУ — основной путь', 't', 'middle', YELLOW_LINE) + text(cx + 240, 700, 'продукты расщепления жиров', 's', 'middle')
    s += text(40, 690, 'Желчь — не фермент:', 't') + text(40, 728, 'она дробит жир для липазы', 's')
    return s


def villus() -> str:
    s = text(600, 60, 'Ворсинка тонкого кишечника', 'h', 'middle')
    # ворсинка — палец
    out = [(420, 820), (420, 300), (440, 200), (520, 150), (600, 200), (620, 300), (620, 820)]
    s += f'<path d="M420 820 L420 300 C420 180 620 180 620 300 L620 820" fill="#F6D6CF" stroke="{PINK_LINE}" stroke-width="6"/>'
    # эпителий — клетки по краю
    for k in range(14):
        y = 300 + k * 37
        s += f'<rect x="424" y="{y}" width="22" height="34" fill="#FBE7E1" stroke="{PINK_LINE}" stroke-width="2"/>'
        s += f'<rect x="594" y="{y}" width="22" height="34" fill="#FBE7E1" stroke="{PINK_LINE}" stroke-width="2"/>'
    # капилляры: артериальный и венозный, сеть
    s += f'<path d="M470 820 L470 300 C470 240 570 240 570 300 L570 820" fill="none" stroke="{RED}" stroke-width="10"/>'
    s += ''.join(f'<path d="M470 {y} C 500 {y - 20} 540 {y + 20} 570 {y}" fill="none" stroke="{RED}" stroke-width="4"/>' for y in range(340, 780, 60))
    # лимфатический капилляр в центре
    s += f'<path d="M520 820 L520 290" stroke="{YELLOW_LINE}" stroke-width="18" stroke-linecap="round"/>'
    s += label(440, 420, 390, 360, 'эпителий', 's')
    s += label(470, 560, 390, 560, 'кровеносные капилляры', 's')
    s += label(520, 700, 390, 760, 'лимфатический капилляр', 's')
    s += f'<path d="M380 820 L660 820" stroke="{INK}" stroke-width="4"/>'
    # стрелки всасывания
    s += arrow(700, 300, 600, 300, INK, 5) + text(720, 290, 'питательные вещества', 's') + text(720, 322, 'из пищевой кашицы', 'cap')
    s += f'<rect x="700" y="470" width="420" height="110" rx="16" fill="#FBE3E4" stroke="{RED}" stroke-width="4"/>'
    s += text(910, 515, 'в кровь:', 't', 'middle', RED) + text(910, 555, 'глюкоза, аминокислоты', 's', 'middle')
    s += f'<rect x="680" y="620" width="460" height="110" rx="16" fill="#FFF4D6" stroke="{YELLOW_LINE}" stroke-width="4"/>'
    s += text(910, 665, 'в лимфу — основной путь:', 't', 'middle', YELLOW_LINE) + text(910, 705, 'продукты расщепления жиров', 's', 'middle')
    s += text(600, 880, 'Ворсинки многократно увеличивают поверхность всасывания.', 't', 'middle')
    return s


def tooth() -> str:
    s = text(600, 60, 'Строение зуба', 'h', 'middle')
    # кость и десна
    s += f'<rect x="250" y="470" width="500" height="430" fill="#EFE7D2" stroke="#B8A47A" stroke-width="4"/>'
    s += f'<path d="M250 440 C 330 420 360 470 400 470 L 600 470 C 640 470 670 420 750 440 L750 500 L250 500 Z" fill="#E9A0A0" stroke="#B85C5C" stroke-width="4"/>'
    # зуб: эмаль (коронка), дентин, цемент (корни), пульпа
    crown = 'M330 190 C 330 130 420 120 450 160 C 480 120 520 120 550 160 C 580 120 670 130 670 190 L 660 470 L 340 470 Z'
    s += f'<path d="{crown}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    dentin = 'M360 230 C 360 190 640 190 640 230 L 630 500 C 620 600 600 700 590 820 L 520 830 L 500 600 L 480 830 L 410 820 C 400 700 380 600 370 500 Z'
    s += f'<path d="{dentin}" fill="#F3E3B0" stroke="#B89A3A" stroke-width="4"/>'
    s += (f'<path d="M370 470 C 380 600 400 700 410 830 L 480 840 L 500 640 L 520 840 L 590 830 C 600 700 620 600 630 470" '
          f'fill="none" stroke="#A9834F" stroke-width="16"/>')
    pulp = 'M420 270 C 420 240 580 240 580 270 L 570 480 C 565 560 555 650 548 790 L 530 790 L 505 560 L 495 560 L 470 790 L 452 790 C 445 650 435 560 430 480 Z'
    s += f'<path d="{pulp}" fill="#F2A3A3" stroke="#B85C5C" stroke-width="3"/>'
    s += f'<path d="M462 780 C 470 600 480 420 500 300" fill="none" stroke="{RED}" stroke-width="3"/><path d="M540 780 C 530 600 520 420 505 300" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    # уровни
    for y, name in ((140, 'коронка'), (470, 'шейка'), (700, 'корень')):
        s += text(180, y + 10, name, 't', 'end')
    s += f'<path d="M200 130 L200 455 M195 485 L205 485 M200 515 L200 840" stroke="{GREY}" stroke-width="3"/>'
    s += label(662, 200, 825, 180, 'эмаль — только на коронке', 's')
    s += label(615, 360, 825, 310, 'дентин — основная часть', 's')
    s += label(560, 400, 825, 430, 'пульпа: сосуды и нервы', 's')
    s += label(700, 452, 825, 530, 'десна', 's')
    s += label(614, 700, 825, 680, 'цемент — корень и шейка', 's')
    s += text(600, 960, 'Эмаль — самая твёрдая ткань организма.', 't', 'middle')
    return s


if __name__ == '__main__':
    jobs = {
        'ruminant-stomach.png': (ruminant_stomach(), 1600, 760),
        'digestive-system.png': (digestive_system(), 1400, 1300),
        'food-path.png': (food_path(), 1600, 780),
        'villus.png': (villus(), 1200, 920),
        'tooth.png': (tooth(), 1200, 1000),
    }
    for name, (svg, w, h) in jobs.items():
        render(svg, w, h, OUT / name)
        print(OUT / name)
