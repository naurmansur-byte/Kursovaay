"""Рисунки с номерами для книги «Конспект ЕНТ: биология»: вопросы «что показано под цифрой N», как в блоке 36–40 ЕНТ.

Геометрия та же, что в рисунках недель (bio_w01.py, bio_w06.py), только вместо подписей — номера.
Вопросы и ответы — course/biology/week-NN/pic-quiz.json, книга собирает их в конец главы и в раздел ответов.
Запуск: cd tools/pics && ../../.venv/Scripts/python.exe bio_numbered.py
"""
from __future__ import annotations

from bio_w01 import chloro, mito, nucleus, ribosomes
from bio_w06 import BLUE, RED, heart
from common import INK, ROOT, render, text

BIO = ROOT / 'course' / 'biology'


def num(px: float, py: float, tx: float, ty: float, n: int) -> str:
    """Выноска от точки на объекте к кружку с номером."""
    return (f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{INK}" stroke-width="2.5"/>'
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="{INK}"/>'
            f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="26" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            + text(tx, ty + 11, str(n), 'h', 'middle'))


def animal_cell() -> str:
    """Клетка животного: 1 ЭПС, 2 митохондрия, 3 цитоплазма, 4 аппарат Гольджи, 5 ядро, 6 рибосома, 7 мембрана."""
    s = ('<path d="M400 450 C380 250 560 140 800 140 C1060 140 1230 250 1210 460 C1190 650 1020 760 800 760 '
         'C560 760 420 640 400 450 Z" fill="#FDF3EA" stroke="#3B3833" stroke-width="6"/>')
    s += nucleus(800, 430, 95)
    for k in range(4):
        y = 300 + k * 26
        s += f'<path d="M560 {y} q 40 -20 80 0 t 80 0" fill="none" stroke="#7A4FA3" stroke-width="5"/>'
        s += ribosomes([(570 + j * 26, y - 6 + (j % 2) * 10) for j in range(6)])
    for k in range(4):
        s += f'<path d="M{960 + k * 6} {560 + k * 22} q 70 -30 140 0" fill="none" stroke="#C7891B" stroke-width="7"/>'
    s += mito(620, 580, 38, 18, 20) + mito(1000, 330, 38, 18, -25) + mito(760, 650, 38, 18, 5)
    s += ribosomes([(900, 600), (930, 660), (680, 450), (1050, 470), (520, 450), (1120, 380), (560, 660)])
    s += num(640, 305, 450, 190, 1) + num(1000, 330, 1190, 210, 2) + num(1150, 520, 1300, 520, 3)
    s += num(1040, 575, 1270, 720, 4) + num(800, 430, 800, 830, 5) + num(560, 660, 420, 770, 6) + num(404, 470, 290, 470, 7)
    return s


def plant_cell() -> str:
    """Клетка листа: 1 клеточная стенка, 2 хлоропласт, 3 ядро, 4 центральная вакуоль, 5 мембрана, 6 митохондрия."""
    s = '<rect x="440" y="160" width="520" height="560" rx="20" fill="#E7F0D9" stroke="#5B7A2A" stroke-width="18"/>'
    s += '<rect x="458" y="178" width="484" height="524" rx="12" fill="#F4F9EE" stroke="#3B3833" stroke-width="3"/>'
    s += '<rect x="540" y="280" width="300" height="330" rx="50" fill="#DDEBF7" stroke="#5E8BB5" stroke-width="3"/>'
    s += nucleus(880, 240, 40)
    s += ''.join(chloro(x, y, 28, 15, r) for x, y, r in [(495, 290, 80), (495, 470, 95), (900, 380, 85), (900, 540, 100),
                                                       (600, 665, 0), (730, 665, 5)])
    s += mito(890, 655, 28, 14, 60)
    s += num(450, 600, 300, 640, 1) + num(495, 470, 300, 430, 2) + num(880, 240, 1080, 170, 3)
    s += num(690, 445, 690, 830, 4) + num(462, 240, 300, 220, 5) + num(890, 655, 1080, 720, 6)
    return s


def heart_numbered() -> str:
    """Сердце: 1 лёгочные вены, 2 правое предсердие, 3 аорта, 4 левый желудочек, 5 трёхстворчатый клапан,
    6 полые вены, 7 правый желудочек, 8 лёгочный ствол, 9 двустворчатый клапан, 10 левое предсердие."""
    cx, cy = 700, 520
    s = f'<path d="M{cx - 200} {cy - 210} V {cy - 330}" stroke="{BLUE}" stroke-width="30"/>'
    s += f'<path d="M{cx - 240} {cy - 120} H {cx - 330}" stroke="{BLUE}" stroke-width="30"/>'
    s += f'<path d="M{cx + 240} {cy - 150} H {cx + 330} M{cx + 240} {cy - 90} H {cx + 330}" stroke="{RED}" stroke-width="22"/>'
    s += heart(cx, cy, names=False)
    s += num(cx + 330, cy - 90, cx + 440, cy - 30, 1) + num(cx - 145, cy - 140, cx - 420, cy - 210, 2)
    s += num(cx + 28, cy - 290, cx + 150, cy - 390, 3) + num(cx + 123, cy + 110, cx + 420, cy + 200, 4)
    s += num(cx - 145, cy - 20, cx - 420, cy + 20, 5) + num(cx - 200, cy - 300, cx - 330, cy - 390, 6)
    s += num(cx - 123, cy + 110, cx - 420, cy + 200, 7) + num(cx - 28, cy - 290, cx - 150, cy - 390, 8)
    s += num(cx + 145, cy - 20, cx + 440, cy + 60, 9) + num(cx + 145, cy - 140, cx + 440, cy - 230, 10)
    s += text(cx - 400, cy + 320, '← правая сторона тела', 'cap') + text(cx + 400, cy + 320, 'левая сторона тела →', 'cap', 'end')
    return s


if __name__ == '__main__':
    jobs = {BIO / 'week-01' / 'pics' / 'cell-animal-numbered.png': (animal_cell(), 1600, 880),
            BIO / 'week-01' / 'pics' / 'cell-plant-numbered.png': (plant_cell(), 1400, 880),
            BIO / 'week-06' / 'pics' / 'heart-numbered.png': (heart_numbered(), 1400, 900)}
    for out, (svg, w, h) in jobs.items():
        render(svg, w, h, out)
        print(out)
