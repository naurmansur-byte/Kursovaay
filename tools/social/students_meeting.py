"""Встреча с учениками «Как идём дальше», 1920×1080 в стиле 2: знакомство, что показал стартовый тест, план до Нового года.

Запуск: .venv/Scripts/python tools/social/students_meeting.py
Результат — «00 Материалы ХимБио просто/Для учеников/Встреча — как идём дальше/»: PDF и PPTX.
На слайдах нет имён и баллов. План недель считается по закрытому results.json (см. tools/forms/placement_report.py).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'forms')]
from placement_report import OUT as RESULTS, decide, score  # noqa: E402
import placement as pl  # noqa: E402
from social import doc, shot  # noqa: E402
from students_deck import CSS as DECK, CARD, GREEN, H, INK, LGREEN, MUTED, PAPER, RED, W  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / '00 Материалы ХимБио просто' / 'Для учеников' / 'Встреча — как идём дальше'
N = 9
DATES = ['02–08.11', '09–15.11', '16–22.11', '23–29.11', '30.11–06.12', '07–13.12', '14–20.12', '21–27.12']
TAG = {'fast': 'быстрее', 'norm': 'обычно', 'full': 'подробно', 'now': 'уже идёт'}


def slide(k: int, title: str, body: str, css: str = '', lead: str = '') -> str:
    lead = f'<p class="lead">{lead}</p>' if lead else ''
    return doc(W, H, DECK + css, f'<div class="eye"><i></i>ХИМБИО ПРОСТО · ВСТРЕЧА</div><h2>{title}</h2>{lead}{body}<div class="pg">{k:02d} / {N}</div>')


BOXES = """
.bx {{ position: absolute; left: 90px; right: 90px; top: {top}px; display: grid; grid-template-columns: repeat({n}, 1fr); gap: 26px; }}
.bx > div {{ padding: 30px 32px 34px; min-height: {h}px; }}
.bx h3 {{ margin: 0 0 16px; font: 800 36px/1.15 'Unbounded'; text-transform: uppercase; }}
.bx p {{ margin: 0; font: 700 35px/1.32 'Manrope'; color: {muted}; }} .bx p b {{ color: {paper}; }}
.note {{ position: absolute; left: 90px; right: 90px; top: {note}px; font: 700 34px/1.35 'Manrope'; }}
"""


def boxes(items, n, top=300, h=390, note=790) -> tuple[str, str]:
    html = ''.join(f'<div class="box"><h3{f" style=color:{c}" if c else ""}>{t}</h3><p>{d}</p></div>' for t, d, c in items)
    return f'<div class="bx">{html}</div>', BOXES.format(top=top, n=n, h=h, note=note, muted=MUTED, paper=PAPER)


def cover() -> str:
    return doc(W, H, DECK + """
.c { position: absolute; left: 110px; top: 250px; }
.c .plaque { display: block; width: max-content; font-size: 104px; padding: 18px 40px 26px; }
.c p { margin: 56px 0 0; font: 700 40px/1.3 'Manrope'; color: #B9B3A8; }""",
               f'<div class="eye"><i></i>ХИМБИО ПРОСТО · ВСТРЕЧА</div><div class="c"><span class="plaque" style="transform:rotate(-2deg)">Знакомимся</span>'
               f'<span class="plaque" style="background:{GREEN};transform:rotate(-1deg);margin-top:20px">и идём дальше</span>'
               '<p>Что мы увидели на старте и как пойдём до Нового года</p></div>')


def hello() -> str:
    b, c = boxes([('Кто ты', 'Как тебя зовут и куда хочешь поступать?', RED),
                  ('Что легко', 'Какая тема в химии или биологии тебе нравится больше всего?', LGREEN),
                  ('Что страшно', 'Что на ЕНТ кажется самым сложным?', RED)], 3)
    return slide(2, 'Давайте знакомиться', b + '<div class="note">Правильных ответов здесь нет. Мы хотим узнать вас, а не проверить.</div>', c,
                 'Три вопроса каждому')


def test() -> str:
    b, c = boxes([('Не оценка', 'Тест не влияет ни на что, кроме плана курса.', RED),
                  ('Не рейтинг', 'Мы не сравниваем вас друг с другом и не показываем ответы другим ученикам.', LGREEN),
                  ('Карта', 'Тест показывает, откуда стартует каждый и где не надо терять время.', RED)], 3)
    return slide(3, 'Зачем был стартовый тест', b + '<div class="note">Спасибо за честное <b class="red">«Не знаю»</b>: такой ответ помогает больше, чем угаданный.</div>', c)


def strong() -> str:
    b, c = boxes([('Химия', 'Строение атома · химическая связь · классы веществ · язык химии', RED),
                  ('Биология', 'Клетка · выделение · кровь и транспорт · нервная система · ДНК · эволюция', LGREEN)], 2, h=340, note=740)
    return slide(4, 'Что у вас уже сильное', b + '<div class="note">Здесь задерживаться не будем: короткое повторение и сразу задания в формате ЕНТ.</div>', c)


TRAPS = [('Биология', 'Что делает диафрагма при вдохе?', 'Сокращается и <b>опускается</b>: объём грудной клетки растёт, воздух входит.', LGREEN),
         ('Биология', 'Какое запасное вещество у грибов?', '<b>Гликоген</b>. Хитин — это стенка клетки, а не запас.', LGREEN),
         ('Химия', 'Что вытесняет бром из раствора KBr?', '<b>Хлор</b>. Активность падает так: Cl₂ &gt; Br₂ &gt; I₂.', RED),
         ('Химия', 'Какая соль получится из CO₂ и NaOH в соотношении 1 : 1?', '<b>NaHCO₃</b>. Если щёлочи вдвое больше — Na₂CO₃.', RED)]


def traps(answers: bool) -> str:
    items = [(t, f'{q}<br><br>{a}' if answers else q, col) for t, q, a, col in TRAPS]
    b, c = boxes(items, 2, top=240 if answers else 300, h=300 if answers else 230, note=850)
    c += '.bx h3 { font-size: 26px; margin-bottom: 10px; } .bx p { color: #F3F0E8; font-size: 30px; }' + ('.bx > div { padding: 22px 30px 24px; }' if answers else '')
    if answers:
        return slide(6, 'Разгадка', b, c)
    return slide(5, 'Четыре ловушки', b + '<div class="note" style="top:880px">Отвечаем вслух. Здесь можно ошибаться: для этого мы и собрались.</div>', c,
                 'Хитрые вопросы из теста. Разберём вместе.')


def plan() -> str:
    blocks = json.loads((RESULTS / 'results.json').read_text(encoding='utf-8'))
    cols = []
    for code, data in (('chem', pl.CHEM), ('bio', pl.BIO)):
        res = [score(data, a) for a in blocks[code]['answers'].values()]
        cols.append({w: decide([r['weeks'][w] for r in res]) for w in range(1, 9)})
        cols[-1][1] = 'now'  # неделя 1 уже идёт
    cell = lambda names, v, w: f'<div class="t">{names[w]}<span class="g {v[w]}">{TAG[v[w]]}</span></div>'
    rows = ''.join(f'<div class="d">{w} · {DATES[w - 1]}</div>{cell(pl.CHEM_WEEKS, cols[0], w)}{cell(pl.BIO_WEEKS, cols[1], w)}' for w in range(1, 9))
    return slide(7, 'План до Нового года', f'<div class="tb"><div class="h">Неделя</div><div class="h">Химия</div><div class="h">Биология</div>{rows}</div>'
                 '<div class="lg"><b>быстрее</b> — тема уже знакома, сразу к заданиям ЕНТ · <b>подробно</b> — здесь дадим больше времени</div>', f"""
.tb {{ position: absolute; left: 90px; right: 90px; top: 212px; display: grid; grid-template-columns: 330px 1fr 1fr; column-gap: 26px; align-items: center; }}
.tb > div {{ height: 80px; display: flex; align-items: center; border-top: 2px solid #3A3A38; }}
.tb .h {{ height: 46px; border: 0; font: 800 26px 'Manrope'; color: {MUTED}; }}
.d {{ font: 800 28px 'Manrope'; color: {MUTED}; }}
.t {{ justify-content: space-between; font: 800 31px/1.1 'Manrope'; gap: 16px; }}
.g {{ flex: none; width: 170px; padding: 8px 0 10px; text-align: center; font: 800 26px 'Manrope'; border-radius: 4px; }}
.fast {{ background: {PAPER}; color: {INK}; }} .norm, .now {{ color: {MUTED}; }} .full {{ background: {GREEN}; color: #fff; }}
.lg {{ position: absolute; left: 90px; right: 200px; top: 960px; font: 700 27px/1.3 'Manrope'; color: {MUTED}; }} .lg b {{ color: {PAPER}; }}""")


def route() -> str:
    b, c = boxes([('A · углубление', 'Тема уже получается, берём задачи сложнее.', LGREEN),
                  ('B · закрепление', 'Основное понятно, нужна практика.', PAPER),
                  ('C · поддержка', 'Нужен образец и больше шагов.', RED)], 3, h=300, note=700)
    return slide(8, 'У каждого свой маршрут', b + '<div class="note">Уроки общие, вариант ДЗ свой. Буква — <b class="red">не оценка</b>: она меняется от недели к неделе.<br><br>'
                 'Личную карту со старта пришлём каждому лично. Там нет баллов: только что уже получается и с чего начинаем.</div>', c)


def ask() -> str:
    items = ['Делай закрепление сразу после первого урока недели', 'Приноси вопросы на второй урок', 'Не знаешь — так и скажи: это не минус',
             'Ошибки разбираем, а не стыдимся их']
    li = ''.join(f'<li><i></i>{t}</li>' for t in items)
    return slide(9, 'Что просим от тебя', f'<ul class="dot" style="position:absolute;left:90px;top:300px;right:90px;gap:30px">{li}</ul>'
                 '<div class="q">Ваши вопросы?</div>', f"""
ul.dot li {{ font-size: 42px; }} ul.dot li i {{ margin-top: 20px; }}
.q {{ position: absolute; left: 90px; top: 760px; font: 800 84px 'Unbounded'; text-transform: uppercase; color: {LGREEN}; }}""")


def main() -> None:
    pages = [cover(), hello(), test(), strong(), traps(False), traps(True), plan(), route(), ask()]
    assert len(pages) == N
    OUT.mkdir(parents=True, exist_ok=True)
    pngs = []
    for i, html in enumerate(pages, 1):
        p = OUT / f'{i:02d}.png'
        shot(html, W, H, p)
        pngs.append(p)
    from PIL import Image
    ims = [Image.open(p).convert('RGB') for p in pngs]
    ims[0].save(OUT / 'Как идём дальше — встреча с учениками.pdf', save_all=True, append_images=ims[1:], resolution=144)
    from pptx import Presentation
    from pptx.util import Emu
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    for p in pngs:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.shapes.add_picture(str(p), 0, 0, prs.slide_width, prs.slide_height)
    prs.save(OUT / 'Как идём дальше — встреча с учениками.pptx')
    print(f'{len(pages)} slides -> {OUT}')


if __name__ == '__main__':
    main()
