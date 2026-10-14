"""«Как проходит неделя» и «Как проверяем знания» — две картинки 1080×1920 в стиле 2 (к программе курса).

Запуск: .venv/Scripts/python tools/social/week.py
Результат: deliverables/sales/week-1.png, week-2.png, week.pdf.
Источник порядка недели: docs/STYLE.md (урок 1 / урок 2, ДЗ), комплекты недель, docs/ENT-PREP-METHOD.md § 5 (пробники).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools' / 'social'), str(ROOT / 'tools' / 'youtube')]
from art import shot  # noqa: E402
from program import CSS, GREEN, INK, PAPER, RED  # noqa: E402

GREY = '#5A554D'

CSS2 = CSS + f"""
h1 {{ font-size: 86px; }}
.row {{ display: flex; gap: 22px; margin-top: 18px; align-items: stretch; }}
.day {{ width: 150px; flex: none; display: flex; align-items: center; justify-content: center; text-align: center;
        font: 800 34px/1.05 'Unbounded'; text-transform: uppercase; color: {PAPER}; transform: rotate(-2deg); padding: 8px; }}
.box {{ flex: 1; border: 4px solid {PAPER}; background: #1D1D1D; padding: 16px 22px 18px; }}
.box h3 {{ margin: 0 0 6px; font: 800 30px/1.15 'Unbounded'; text-transform: uppercase; }}
.box p {{ margin: 0; font: 700 28px/1.3 'Manrope'; color: #D8D3C9; }}
.box.home {{ border-style: dashed; background: transparent; }}
.sum {{ margin-top: 34px; font: 700 29px/1.35 'Manrope'; color: #B9B3A8; }} .sum b {{ color: {PAPER}; }}
.card {{ display: flex; gap: 26px; margin-top: 26px; align-items: stretch; }}
.when {{ width: 230px; flex: none; padding: 18px 14px; text-align: center; display: flex; align-items: center; justify-content: center;
         font: 800 30px/1.15 'Unbounded'; text-transform: uppercase; color: {PAPER}; transform: rotate(-2deg); }}
.what {{ flex: 1; border: 4px solid {PAPER}; background: #1D1D1D; padding: 18px 24px 20px; }}
.what h3 {{ margin: 0 0 8px; font: 800 32px/1.15 'Unbounded'; text-transform: uppercase; }}
.what p {{ margin: 0; font: 700 28px/1.32 'Manrope'; color: #D8D3C9; }}
.what p + p {{ margin-top: 8px; }}
.big3 {{ display: flex; gap: 14px; margin-top: 12px; flex-wrap: wrap; }}
.big3 span {{ background: {PAPER}; color: {INK}; padding: 6px 14px 8px; font: 800 26px 'Manrope'; text-transform: uppercase; }}
"""


def row(day: str, bg: str, title: str, text: str, home: bool = False) -> str:
    return (f'<div class="row"><div class="day" style="background:{bg}">{day}</div>'
            f'<div class="box{" home" if home else ""}"><h3>{title}</h3><p>{text}</p></div></div>')


def card(when: str, bg: str, title: str, *texts: str, extra: str = '') -> str:
    ps = ''.join(f'<p>{t}</p>' for t in texts)
    return (f'<div class="card"><div class="when" style="background:{bg}">{when}</div>'
            f'<div class="what"><h3>{title}</h3>{ps}{extra}</div></div>')


def slide(n: int) -> str:
    if n == 0:
        body = f"""
<div class="tag"><i></i>ХИМБИО ПРОСТО · ПОДГОТОВКА К ЕНТ</div>
<h1>Как проходит<br>неделя</h1><div class="plaque">4 урока по 90 минут</div>
{row('Пн', RED, 'Химия · урок 1', 'Новая тема с нуля: объяснение, разбор примеров, задания в формате ЕНТ на уроке.')}
{row('Вт', GREEN, 'Биология · урок 1', 'Новая тема с нуля: объяснение, схемы, задания в формате ЕНТ на уроке.')}
{row('Дома', GREY, 'После урока 1', 'Конспект и закрепление, домашнее задание: тест в формате ЕНТ (ответ строкой в Telegram) и задачи с решением (фото преподавателю).', home=True)}
{row('Чт', RED, 'Химия · урок 2', 'Вопросы и повторение → разбор ДЗ → практика в формате ЕНТ → <b>контроль недели</b>.')}
{row('Пт', GREEN, 'Биология · урок 2', 'Вопросы и повторение → разбор ДЗ → практика в формате ЕНТ → <b>контроль недели</b>.')}
{row('Дома', GREY, 'После урока 2', 'Задание своего уровня (углубление, закрепление или поддержка), работа над ошибками, повторение, памятка недели.', home=True)}
<p class="sum"><b>Около 150 минут самостоятельной работы в неделю на предмет.</b><br>Вопросы между уроками — в Telegram-группе. Все уроки записываются.</p>
<div class="num">1 / 2</div>"""
    else:
        body = f"""
<div class="tag"><i></i>ХИМБИО ПРОСТО · ПОДГОТОВКА К ЕНТ</div>
<h1>Как проверяем<br>знания</h1><div class="plaque">контроль и пробные ЕНТ</div>
{card('Старт', PAPER.replace(PAPER, '#8F897F'), 'Входной тест', 'Бесплатно, до начала курса. Показывает уровень ученика и с какого варианта ДЗ начинать.')}
{card('Каждый урок', GREY, 'Задания ЕНТ на уроке', 'Решаем задания в формате ЕНТ и сразу разбираем ошибки.')}
{card('Каждую неделю', RED, 'ДЗ и контроль недели', 'ДЗ проверяет преподаватель: тест — строкой в Telegram, решения — фото.', '<b>Контроль недели</b> — 10 минут в конце урока 2 по каждому предмету. Задания как на ЕНТ:', extra='<div class="big3"><span>один ответ</span><span>несколько ответов</span><span>соответствие</span></div>')}
{card('Каждый месяц', GREEN, 'Пробный ЕНТ', '40 заданий по предмету, 80 минут — как на настоящем экзамене. Дома в выходные, с автопроверкой.', 'Ошибки разбираем на ближайшем уроке 2. <b>В мае — 2 полных пробных ЕНТ.</b>')}
<p class="sum">Дополнительно советуем пройти официальный пробный тест НЦТ.</p>
<div class="foot"><div class="start">Старт — 2 ноября</div><div class="acc">@himbio.prosto</div></div>
<div class="num">2 / 2</div>"""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS2} body {{ width: 1080px; height: 1920px; }}</style></head><body>{body}</body></html>'


if __name__ == '__main__':
    from PIL import Image
    out = ROOT / 'deliverables' / 'sales'
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for n in range(2):
        f = out / f'week-{n + 1}.png'
        shot(slide(n), 1080, 1920, f)
        files.append(f)
    imgs = [Image.open(f).convert('RGB') for f in files]
    imgs[0].save(out / 'week.pdf', save_all=True, append_images=imgs[1:], resolution=150)
    for f in files + [out / 'week.pdf']:
        print(f)
