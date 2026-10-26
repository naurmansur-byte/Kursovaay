"""Программа курса для родителей и учеников — одна длинная картинка в стиле 2 (для WhatsApp/директа).

Запуск: .venv/Scripts/python tools/social/program.py
Результат: deliverables/sales/program-kursa-1…4.png (1080×1920, формат сторис — WhatsApp не сжимает в нечитаемое) и program-kursa.pdf.
Темы — по course/PROGRAM.md и course/biology/PROGRAM.md, сгруппированы по месяцам.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools' / 'youtube')]
from art import BASE, shot  # noqa: E402

RED, GREEN, INK, PAPER = '#F13A43', '#1F7A4A', '#151515', '#F3F0E8'

FORMAT = ['4 урока в неделю', '2 — химия, 2 — биология', '90 минут', 'онлайн в Google Meet', 'ДЗ с проверкой',
          'пробный ЕНТ раз в месяц', 'записи уроков']

# (месяц, даты, химия, биология)
MONTHS = [
    ('Ноябрь', '2–29.11',
     ['Атом, молекула, формулы, валентность', 'Уравнения и типы реакций', 'Оксиды, кислоты, основания, соли', 'Моль и расчёты по уравнению'],
     ['Клетка и органоиды', 'Белки, углеводы, липиды, ДНК и РНК', 'Мембрана, транспорт, ферменты', 'Обмен веществ, АТФ, дыхание, фотосинтез']),
    ('Декабрь', '30.11–27.12',
     ['Растворы, примеси, избыток, выход', 'Строение атома, периодический закон', 'Химическая связь, кристаллические решётки', 'Электролиты, ионные уравнения, гидролиз'],
     ['Питание и пищеварение', 'Транспорт веществ, кровь, кровообращение', 'Газообмен и дыхание', 'Выделение, почки, водно-солевой баланс']),
    ('pause', 'Зимние каникулы — 28.12–10.01', [], []),
    ('Январь', '11.01–07.02',
     ['Окислительно-восстановительные реакции', 'Электролиз', 'Термохимия, скорость реакций', 'Химическое равновесие'],
     ['Опора и движение', 'Нервная система, органы чувств', 'Гормоны и гомеостаз', 'Клеточный цикл, митоз, мейоз']),
    ('Февраль', '08.02–07.03',
     ['Металлы: общие свойства, группы 1–2, жёсткость воды', 'Алюминий, железо, медь, цинк, хром, марганец', 'Углерод, кремний, азот, фосфор', 'Повторение и работа над ошибками'],
     ['Размножение и развитие', 'ДНК, РНК, синтез белка', 'Генетика: законы Менделя', 'Повторение и работа над ошибками']),
    ('Март', '08–21.03',
     ['Кислород, сера, галогены', 'Органика: строение, изомерия, алканы'],
     ['Генетика пола, сцепленное наследование', 'Изменчивость, мутации, селекция']),
    ('pause', 'Весенние каникулы — 22–28.03', [], []),
    ('Апрель', '29.03–02.05',
     ['Алкены, алкины, арены, нефть', 'Спирты, фенол, альдегиды', 'Кислоты, сложные эфиры, жиры', 'Углеводы, амины, аминокислоты, белки'],
     ['Систематика организмов', 'Эволюция', 'Экология и биосфера', 'Микробиология, биотехнология']),
    ('Май', '03–30.05',
     ['Полимеры; вывод формул веществ', 'Сложные задачи: смеси, выход', 'Пробный ЕНТ — 2 полных варианта'],
     ['Биомедицина и биоинформатика', 'Сводное повторение по всем темам', 'Пробный ЕНТ — 2 полных варианта']),
]

CSS = BASE + f"""
body {{ background-size: 72px 72px; font-family: 'Manrope'; padding: 70px 64px 0; }}
.tag {{ font: 800 28px 'Manrope'; letter-spacing: .14em; display: flex; align-items: center; gap: 12px; }}
.tag i {{ width: 16px; height: 16px; border-radius: 50%; background: {RED}; }}
h1 {{ margin: 34px 0 0; font: 800 104px/1 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }}
.plaque {{ margin-top: 22px; padding: 12px 28px 16px; font-size: 40px; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 14px; margin-top: 52px; }}
.chip {{ border: 4px solid {PAPER}; padding: 10px 20px; font: 800 28px 'Manrope'; text-transform: uppercase; white-space: nowrap; }}
.sched {{ margin-top: 26px; font: 700 32px/1.35 'Manrope'; color: #B9B3A8; }}
.sched b {{ color: {PAPER}; }}
.legend {{ display: flex; gap: 40px; margin: 54px 0 22px; font: 800 30px 'Manrope'; text-transform: uppercase; letter-spacing: .06em; }}
.legend span {{ display: flex; align-items: center; gap: 14px; }} .legend i {{ width: 30px; height: 30px; }}
.month {{ border: 4px solid {PAPER}; background: #1D1D1D; margin-top: 26px; }}
.mh {{ display: flex; align-items: baseline; gap: 22px; padding: 18px 26px 14px; border-bottom: 4px solid {PAPER}; }}
.mh b {{ font: 800 46px/1 'Unbounded'; text-transform: uppercase; }}
.mh span {{ font: 800 28px 'Manrope'; color: #B9B3A8; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; }}
.col {{ padding: 18px 22px 22px 26px; }} .col + .col {{ border-left: 4px solid {PAPER}; }}
.col h3 {{ margin: 0 0 12px; display: inline-block; padding: 4px 14px 8px; font: 800 26px 'Unbounded'; text-transform: uppercase; color: {PAPER}; transform: rotate(-2deg); }}
.col ul {{ margin: 0; padding: 0; list-style: none; }}
.col li {{ font: 700 29px/1.28 'Manrope'; padding-left: 26px; position: relative; margin-top: 10px; }}
.col li::before {{ content: ''; position: absolute; left: 0; top: 13px; width: 12px; height: 12px; background: currentColor; opacity: .55; }}
.pause {{ margin-top: 26px; padding: 16px 26px; border: 4px dashed rgba(243,240,232,.45); font: 800 30px 'Manrope'; color: #B9B3A8; text-align: center; }}
.foot {{ margin-top: 46px; display: flex; align-items: center; justify-content: space-between; }}
.foot .start {{ background: {PAPER}; color: {INK}; padding: 14px 26px 18px; font: 800 44px/1 'Unbounded'; text-transform: uppercase; transform: rotate(-2deg); }}
.foot .acc {{ font: 800 32px 'Manrope'; letter-spacing: .06em; }}
.num {{ position: absolute; right: 64px; bottom: 44px; font: 800 26px 'Manrope'; color: #8F897F; letter-spacing: .08em; }}
.note {{ margin-top: 30px; font: 700 26px/1.35 'Manrope'; color: #8F897F; }}
"""


def month(name: str, dates: str, chem: list[str], bio: list[str]) -> str:
    if name == 'pause':
        return f'<div class="pause">{dates}</div>'
    col = lambda title, bg, items: (f'<div class="col"><h3 style="background:{bg}">{title}</h3><ul>'  # noqa: E731
                                    + ''.join(f'<li>{t}</li>' for t in items) + '</ul></div>')
    return (f'<div class="month"><div class="mh"><b>{name}</b><span>{dates}</span></div>'
            f'<div class="cols">{col("Химия", RED, chem)}{col("Биология", GREEN, bio)}</div></div>')


SLIDES = [[0], [1, 2, 3], [4, 5, 6], [7, 8]]  # индексы MONTHS на каждой картинке


def page(n: int) -> str:
    chips = ''.join(f'<div class="chip">{c}</div>' for c in FORMAT)
    total = len(SLIDES)
    if n == 0:
        top = f"""
<div class="tag"><i></i>ХИМБИО ПРОСТО · ПОДГОТОВКА К ЕНТ</div>
<h1>Программа<br>курса</h1><div class="plaque">химия + биология</div>
<div class="chips">{chips}</div>
<p class="sched"><b>Ноябрь — май, 7 месяцев.</b> Онлайн, Google Meet.<br><b>Пн и Чт — химия, Вт и Пт — биология.</b><br>Время на выбор: 18:00–19:30 или 19:30–21:00.<br>Все темы ЕНТ по обоим предметам — по учебникам из перечня НЦТ.</p>
<div class="legend"><span><i style="background:{RED}"></i>Химия</span><span><i style="background:{GREEN}"></i>Биология</span></div>"""
    else:
        top = '<div class="tag"><i></i>ХИМБИО ПРОСТО · ПРОГРАММА КУРСА</div>'
    blocks = ''.join(month(*MONTHS[i]) for i in SLIDES[n])
    foot = ''
    if n == 0:
        foot = '<div class="foot"><div class="start">Старт — 2 ноября</div><div class="acc">@himbio.prosto</div></div>'
    if n == total - 1:
        foot = ('<p class="note">Каждую неделю: урок новой темы и урок разбора ДЗ и практики в формате ЕНТ.<br>'
                'Порядок тем внутри месяца может немного уточняться.</p>'
                '<div class="foot"><div class="start">Старт — 2 ноября</div><div class="acc">@himbio.prosto</div></div>')
    num = f'<div class="num">{n + 1} / {total}</div>'
    body = top + blocks + foot + num
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body {{ width: 1080px; height: 1920px; }}</style></head><body>{body}</body></html>'


if __name__ == '__main__':
    from PIL import Image
    out = ROOT / 'deliverables' / 'sales'
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for n in range(len(SLIDES)):
        f = out / f'program-kursa-{n + 1}.png'
        shot(page(n), 1080, 1920, f)
        files.append(f)
    imgs = [Image.open(f).convert('RGB') for f in files]
    imgs[0].save(out / 'program-kursa.pdf', save_all=True, append_images=imgs[1:], resolution=150)
    for f in files + [out / 'program-kursa.pdf']:
        print(f)
