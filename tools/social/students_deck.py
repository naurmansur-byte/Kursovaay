"""Презентация курса для учеников, которые уже записались, 1920×1080 в стиле 2: как устроен курс, материалы, формат ЕНТ, книги «Конспект ЕНТ».

Запуск: .venv/Scripts/python tools/social/students_deck.py
Результат — «00 Материалы ХимБио просто/Для учеников/Презентация курса/»: PNG слайдов, PDF и PPTX.
Карточки преподавателей берутся готовыми из «00 Материалы…/Преподаватели/Карточки/» (вне Git, см. teachers.py --cards).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
from social import ATOM, doc, dna, shot  # noqa: E402

ROOT = HERE.parents[1]
CARDS = ROOT / '00 Материалы ХимБио просто' / 'Преподаватели' / 'Карточки'
OUT = ROOT / '00 Материалы ХимБио просто' / 'Для учеников' / 'Презентация курса'
RED, GREEN, LGREEN, INK, PAPER, MUTED, CARD = '#F13A43', '#1F7A4A', '#3FA65F', '#151515', '#F3F0E8', '#B9B3A8', '#1D1D1D'
W, H = 1920, 1080
N = 14

CSS = f"""
body {{ background-size: 80px 80px; }}
.eye {{ position: absolute; left: 90px; top: 64px; font: 800 26px 'Manrope'; letter-spacing: .16em; display: flex; align-items: center; gap: 14px; color: {MUTED}; }}
.eye i {{ width: 14px; height: 14px; border-radius: 50%; background: {RED}; }}
h2 {{ position: absolute; left: 90px; top: 118px; right: 90px; margin: 0; font: 800 70px/1.05 'Unbounded'; text-transform: uppercase; letter-spacing: -.01em; }}
.lead {{ position: absolute; left: 90px; top: 222px; right: 160px; margin: 0; font: 700 34px/1.3 'Manrope'; color: {MUTED}; }}
.pg {{ position: absolute; right: 90px; bottom: 50px; font: 800 24px 'Unbounded'; color: {MUTED}; }}
.box {{ background: {CARD}; border: 4px solid {PAPER}; }}
.red {{ color: {RED}; }} .green {{ color: {LGREEN}; }} .muted {{ color: {MUTED}; }}
ul.dot {{ margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 16px; }}
ul.dot li {{ font: 700 29px/1.3 'Manrope'; display: flex; gap: 16px; }} ul.dot li i {{ flex: none; width: 14px; height: 14px; margin-top: 13px; background: {RED}; }}
code {{ font: 800 30px 'Unbounded'; background: {PAPER}; color: {INK}; padding: 6px 16px 8px; }}
"""


def slide(k: int, title: str, body: str, css: str = '', lead: str = '') -> str:
    head = f'<div class="eye"><i></i>ХИМБИО ПРОСТО · ДЛЯ УЧЕНИКОВ</div><h2>{title}</h2>' if title else ''
    lead = f'<p class="lead">{lead}</p>' if lead else ''
    return doc(W, H, CSS + css, f'{head}{lead}{body}<div class="pg">{k:02d} / {N}</div>')


def cover() -> str:
    return doc(W, H, CSS + """
.slash { position: absolute; top: -200px; bottom: -200px; transform: skewX(-14deg); }
h1 { position: absolute; left: 300px; top: 250px; margin: 0; font: 800 104px/1.04 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }
.plaque { position: absolute; left: 300px; top: 560px; padding: 14px 34px 20px; font-size: 50px; }
.sub { position: absolute; left: 300px; top: 700px; width: 1150px; margin: 0; font: 700 40px/1.35 'Manrope'; color: #B9B3A8; }
.atom { position: absolute; right: 70px; top: 40px; width: 220px; height: 220px; transform: rotate(-12deg); }
.dna { position: absolute; right: 210px; bottom: 90px; width: 180px; height: 380px; transform: rotate(14deg); }
""", f"""<div class="slash" style="left:-40px;width:150px;background:{RED}"></div><div class="slash" style="left:150px;width:44px;background:{GREEN}"></div>
{ATOM}{dna().replace('#F13A43', LGREEN)}
<h1>Добро пожаловать<br>в ХимБио просто</h1><div class="plaque">старт курса</div>
<p class="sub">Как устроен курс, что ты будешь получать каждую неделю и как мы готовимся к ЕНТ по химии и биологии</p>""")


def numbers() -> str:
    items = [('2', 'предмета: химия и биология', RED), ('4', 'урока в неделю — по 2 на каждый предмет', LGREEN),
             ('90', 'минут урок, онлайн в Google Meet', RED), ('23', 'недели новых тем по каждому предмету', LGREEN),
             ('2', 'полных пробника ЕНТ в мае', RED), ('7', 'месяцев: со 2 ноября по 30 мая', LGREEN)]
    its = ''.join(f'<div class="i box"><b style="color:{c}">{n}</b><span>{t}</span></div>' for n, t, c in items)
    return slide(2, 'Курс в цифрах', f'<div class="its">{its}</div>', """
.its { position: absolute; left: 90px; right: 90px; top: 310px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; }
.i { padding: 26px 32px 30px; min-height: 290px; }
.i b { display: block; font: 800 120px/1 'Unbounded'; } .i span { display: block; margin-top: 18px; font: 800 32px/1.25 'Manrope'; }
""", 'ДЗ и вопросы — в Telegram. Уроки записываются: пропустил — посмотришь запись')


def schedule() -> str:
    days = [('Пн', 'Химия', 'новая тема', RED), ('Вт', 'Биология', 'новая тема', LGREEN), ('Ср', 'Дома', 'конспект и домашняя работа', MUTED),
            ('Чт', 'Химия', 'разбор ДЗ, практика, контроль', RED), ('Пт', 'Биология', 'разбор ДЗ, практика, контроль', LGREEN)]
    ds = ''.join(f'<div class="d" style="border-color:{c}"><span>{d}</span><b style="color:{c}">{s}</b><p>{t}</p></div>' for d, s, t, c in days)
    return slide(3, 'Неделя курса', f"""<div class="ds">{ds}</div>
<div class="times"><b>18:00–19:30</b><span>или</span><b>19:30–21:00</b><p>по времени твоей группы</p></div>
<div class="pause"><b>Каникулы:</b> 28 декабря — 10 января и неделя Наурыза, 22–28 марта.</div>""", """
.ds { position: absolute; left: 90px; right: 90px; top: 300px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 20px; }
.d { background: #1D1D1D; border-top: 10px solid; padding: 24px 26px 28px; min-height: 290px; }
.d span { font: 800 30px 'Unbounded'; color: #B9B3A8; } .d b { display: block; margin: 16px 0 10px; font: 800 38px 'Unbounded'; text-transform: uppercase; }
.d p { margin: 0; font: 700 27px/1.3 'Manrope'; }
.times { position: absolute; left: 90px; top: 660px; display: flex; align-items: baseline; gap: 26px; }
.times b { font: 800 64px 'Unbounded'; } .times span { font: 800 30px 'Manrope'; color: #B9B3A8; }
.times p { margin: 0 0 0 10px; font: 800 30px 'Manrope'; color: #F13A43; text-transform: uppercase; letter-spacing: .06em; }
.pause { position: absolute; left: 90px; right: 90px; top: 810px; font: 700 30px/1.35 'Manrope'; color: #B9B3A8; } .pause b { color: #F3F0E8; }
""", 'Первые уроки — 2 и 3 ноября')


def teachers() -> str:
    cards = sorted(CARDS.glob('Преподаватель *.png'), key=lambda p: 'биологии' in p.name)  # химия, затем биология
    imgs = ''.join(f'<img src="{p.as_uri()}">' for p in cards)
    return slide(4, 'Преподаватели', f'<div class="cards">{imgs}</div>', """
.cards { position: absolute; left: 0; right: 0; top: 250px; display: flex; justify-content: center; gap: 70px; }
.cards img { height: 760px; border: 4px solid #F3F0E8; }
""")


def week() -> str:
    steps = [('1', 'Урок 1', 'новая тема с нуля по презентации, практика, короткая проверка', RED),
             ('2', 'После урока', 'конспект, закрепление и общая часть домашней работы', LGREEN),
             ('3', 'Урок 2', 'твои вопросы, разбор ДЗ, задания в формате ЕНТ, контроль 10 минут', RED),
             ('4', 'После урока', 'вариант ДЗ по уровню, исправление ошибок, трек недели', LGREEN)]
    ss = ''.join(f'<div class="s box"><b style="background:{c}">{n}</b><h3>{t}</h3><p>{d}</p></div>' for n, t, d, c in steps)
    return slide(5, 'Как проходит неделя', f"""<div class="ss">{ss}</div>
<div class="note">Дома — около <b>2,5 часа в неделю</b> на каждый предмет. Сначала урок, потом задания: заранее ничего читать не нужно.</div>""", """
.ss { position: absolute; left: 90px; right: 90px; top: 300px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.s { padding: 28px 30px 32px; min-height: 390px; }
.s b { display: flex; width: 80px; height: 80px; align-items: center; justify-content: center; font: 800 42px 'Unbounded'; color: #fff; }
.s h3 { margin: 26px 0 14px; font: 800 36px/1.15 'Unbounded'; text-transform: uppercase; } .s p { margin: 0; font: 700 29px/1.3 'Manrope'; color: #B9B3A8; }
.note { position: absolute; left: 90px; right: 90px; top: 790px; font: 700 34px/1.35 'Manrope'; } .note b { color: #F13A43; }
""")


def materials() -> str:
    items = [('Конспект', 'вся теория урока: «Запомни», «Ловушка», «Разберём», «Проверь себя»', RED),
             ('Факты ЕНТ недели', 'учёные, даты, числа и формулировки, которые спрашивают на тесте', LGREEN),
             ('Памятки', 'карточки на телефон: главное правило и ловушки на одном экране', RED),
             ('Закрепление', 'короткие задания сразу после первого урока', LGREEN),
             ('Домашняя работа', 'общая часть и вариант по уровню: A — углубление, B — закрепление, C — поддержка', RED),
             ('Решения', 'полный разбор каждого задания — открываешь после своей попытки', LGREEN)]
    its = ''.join(f'<div class="i box" style="border-top:10px solid {c}"><h3>{t}</h3><p>{d}</p></div>' for t, d, c in items)
    return slide(6, 'Материалы каждую неделю', f'<div class="its">{its}</div>', """
.its { position: absolute; left: 90px; right: 90px; top: 290px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.i { padding: 24px 30px 28px; min-height: 300px; }
.i h3 { margin: 0 0 16px; font: 800 36px/1.15 'Unbounded'; text-transform: uppercase; } .i p { margin: 0; font: 700 29px/1.3 'Manrope'; color: #B9B3A8; }
""", 'Всё в PDF и картинках под экран телефона — ничего не нужно распечатывать')


def homework() -> str:
    rows = [('Тест', 'ответы одной строкой в Telegram', '<code>1В 2Б 3АВД 4: А2 Б4</code>'),
            ('Задачи', 'фото решения из тетради', 'видно ход: формула, подстановка, ответ'),
            ('Найди ошибку', 'одна-две фразы или голосовое', 'объясни, где ошибся «ученик»')]
    rs = ''.join(f'<div class="r box"><h3>{a}</h3><p>{b}</p><div class="ex">{c}</div></div>' for a, b, c in rows)
    return slide(7, 'Как сдавать домашнюю работу', f"""<div class="rs">{rs}</div>
<div class="note">Строка в примере — образец оформления, а не ответы. Преподаватель проверяет и разбирает ошибки на следующем уроке.</div>""", """
.rs { position: absolute; left: 90px; right: 90px; top: 300px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; }
.r { padding: 28px 32px 34px; min-height: 380px; display: flex; flex-direction: column; gap: 18px; }
.r h3 { margin: 0; font: 800 44px 'Unbounded'; text-transform: uppercase; color: #F13A43; } .r:nth-child(2) h3 { color: #3FA65F; }
.r p { margin: 0; font: 800 32px/1.25 'Manrope'; } .ex { margin-top: auto; font: 700 28px/1.3 'Manrope'; color: #B9B3A8; }
.note { position: absolute; left: 90px; right: 90px; top: 790px; font: 700 31px/1.35 'Manrope'; color: #B9B3A8; }
""", 'Домашка рассчитана на телефон: без таблиц и распечаток')


def ent() -> str:
    rows = [('Один ответ', '4 варианта, А–Г', '1'), ('Несколько ответов', '6 вариантов, верных от 1 до 3', '2 · 1 · 0'),
            ('Соответствие', '2 пункта и 4 варианта', '2 · 1 · 0'), ('Контекст', 'текст, таблица или опыт и 5 вопросов', '5 × 1')]
    rs = ''.join(f'<div class="r"><b>{a}</b><span>{b}</span><em>{c}</em></div>' for a, b, c in rows)
    return slide(8, 'Формат ЕНТ — с первой недели', f"""<div class="rs box">{rs}</div>
<div class="big"><b>40 %</b><span>баллов предмета — двухбалльные задания. Поэтому тренируем их каждую неделю: в ДЗ, контроле и пробниках.</span></div>""", """
.rs { position: absolute; left: 90px; top: 300px; width: 1060px; padding: 10px 36px; }
.r { display: grid; grid-template-columns: 380px 1fr 200px; gap: 20px; align-items: baseline; padding: 26px 0; border-bottom: 2px solid #3A3A3A; }
.r:last-child { border-bottom: none; }
.r b { font: 800 34px 'Unbounded'; text-transform: uppercase; } .r span { font: 700 29px/1.3 'Manrope'; color: #B9B3A8; }
.r em { font: 800 34px 'Unbounded'; font-style: normal; color: #F13A43; text-align: right; white-space: nowrap; }
.big { position: absolute; left: 1230px; right: 90px; top: 320px; }
.big b { display: block; font: 800 150px/1 'Unbounded'; color: #3FA65F; } .big span { display: block; margin-top: 20px; font: 800 32px/1.3 'Manrope'; }
""", 'Профильный предмет на ЕНТ: 40 заданий, 50 баллов')


def tracks() -> str:
    return slide(9, 'Треки недели', f"""<div class="t t1 box" style="border-top:10px solid {RED}"><div class="tg red">химия · с 6-й недели</div>
<h3>Расчётный трек</h3><p>Две задачи на расчёты ЕНТ: смеси, растворы, цепочки превращений, олеум, электролиз. Новые модели — раньше, а не в конце курса, и каждая потом повторяется.</p></div>
<div class="t t2 box" style="border-top:10px solid {LGREEN}"><div class="tg green">биология · с 3-й недели</div>
<h3>Контекст-трек</h3><p>Опыт, таблица или график и четыре вопроса — как задания 26–30 на ЕНТ. Учимся видеть контроль, читать данные и делать вывод только по фактам.</p></div>
<div class="note">15 минут в неделю, решения — после попытки.</div>""", """
.t { position: absolute; top: 300px; width: 840px; padding: 30px 38px 36px; min-height: 420px; }
.t1 { left: 90px; } .t2 { left: 990px; }
.tg { font: 800 26px 'Manrope'; letter-spacing: .1em; text-transform: uppercase; }
.t h3 { margin: 24px 0 18px; font: 800 52px 'Unbounded'; text-transform: uppercase; } .t p { margin: 0; font: 700 31px/1.35 'Manrope'; color: #B9B3A8; }
.note { position: absolute; left: 90px; right: 90px; top: 800px; font: 800 32px 'Manrope'; }
""")


def books() -> str:
    def book(subj, color, pages, err):
        return (f'<div class="book" style="--c:{color}"><div class="spine"></div><div class="cv"><span>Конспект ЕНТ</span><b>{subj}</b>'
                f'<i>23 главы · {pages} страниц</i></div><div class="err">{err} ошибок учебников<br>и как правильно</div></div>')
    items = ['Одна глава — одна неделя курса', 'Конспект, памятка и факты ЕНТ недели', '«Что легко перепутать» — со страницами учебников',
             'В конце — ошибки школьных учебников и верные формулировки']
    return slide(10, 'Конспект ЕНТ — две книги курса', f"""<div class="books">{book('химия', RED, 257, 83)}{book('биология', LGREEN, 272, 110)}</div>
<ul class="dot">{"".join(f"<li><i></i>{x}</li>" for x in items)}</ul>
<div class="note">Весь курс в одной книге по каждому предмету — для повторения перед контролем, пробником и самим ЕНТ.</div>""", """
.books { position: absolute; left: 110px; top: 300px; display: flex; gap: 60px; }
.book { position: relative; width: 380px; height: 520px; transform: rotate(-3deg); }
.book:nth-child(2) { transform: rotate(3deg); margin-top: 30px; }
.spine { position: absolute; left: 0; top: 0; bottom: 0; width: 34px; background: var(--c); }
.cv { position: absolute; left: 34px; right: 0; top: 0; bottom: 0; background: #1D1D1D; border: 4px solid #F3F0E8; border-left: none;
  padding: 40px 30px; display: flex; flex-direction: column; gap: 18px; box-shadow: 18px 18px 0 rgba(0,0,0,.45); }
.cv span { font: 800 26px 'Manrope'; letter-spacing: .14em; text-transform: uppercase; color: #B9B3A8; }
.cv b { font: 800 38px/1 'Unbounded'; text-transform: uppercase; color: var(--c); }
.cv i { margin-top: auto; margin-bottom: 40px; font: 700 24px 'Manrope'; font-style: normal; color: #B9B3A8; }
.err { position: absolute; left: 60px; right: -20px; bottom: -50px; background: var(--c); color: #fff; padding: 12px 20px 16px; font: 800 24px/1.25 'Manrope'; transform: rotate(2deg); }
ul.dot { position: absolute; left: 1060px; right: 90px; top: 320px; gap: 24px; } ul.dot li { font-size: 32px; }
.note { position: absolute; left: 1060px; right: 90px; top: 760px; font: 800 30px/1.35 'Manrope'; color: #F3F0E8; }
""", 'Все конспекты курса собраны в книги: химия и биология')


def textbooks() -> str:
    return slide(11, 'Учимся по учебникам НЦТ', f"""<div class="c c1 box"><b class="red">19 + 12</b><h3>тем ЕНТ</h3><p>химии и биологии — каждая с учебником, параграфами и страницами: документ «Темы ЕНТ по учебникам»</p></div>
<div class="c c2 box"><b class="green">7–11</b><h3>классы</h3><p>материал курса — по учебникам из перечня НЦТ: по ним составляют задания ЕНТ</p></div>
<div class="c c3 box"><b class="red">193</b><h3>ошибки учебников</h3><p>нашли и разобрали: на уроках и в конспектах — сразу верная формулировка</p></div>""", """
.c { position: absolute; top: 300px; width: 550px; padding: 30px 36px 36px; min-height: 470px; }
.c1 { left: 90px; } .c2 { left: 685px; } .c3 { left: 1280px; }
.c b { display: block; font: 800 104px/1 'Unbounded'; } .c h3 { margin: 14px 0 18px; font: 800 38px 'Unbounded'; text-transform: uppercase; }
.c p { margin: 0; font: 700 30px/1.35 'Manrope'; color: #B9B3A8; }
""", 'Ничего «от себя»: определения, факты и числа — как в учебниках')


def checks() -> str:
    rows = [('Каждую неделю', 'контроль 10 минут в формате ЕНТ на втором уроке', RED),
            ('После разделов', 'рубежи — проверка большой темы целиком', LGREEN),
            ('Уровень A · B · C', 'маршрут ДЗ под тебя — меняется по результатам, это не оценка', RED),
            ('Май', 'два полных пробника: 40 заданий, 50 баллов, 80 минут', LGREEN),
            ('После пробника', 'карта ошибок по темам и твой план повторения до ЕНТ', RED)]
    rs = ''.join(f'<div class="r"><b style="color:{c}">{a}</b><span>{b}</span></div>' for a, b, c in rows)
    return slide(12, 'Как проверяем прогресс', f'<div class="rs">{rs}</div>', """
.rs { position: absolute; left: 90px; right: 90px; top: 290px; display: flex; flex-direction: column; gap: 18px; }
.r { display: grid; grid-template-columns: 520px 1fr; gap: 30px; align-items: baseline; background: #1D1D1D; border-left: 10px solid #F3F0E8; padding: 22px 34px; }
.r b { font: 800 38px 'Unbounded'; text-transform: uppercase; } .r span { font: 700 32px/1.3 'Manrope'; }
""", 'Ошибка — не провал, а тема для повторения')


def rules() -> str:
    items = ['Камера и микрофон на уроке, тетрадь и ручка рядом', 'После первого урока — конспект и закрепление',
             'ДЗ — в срок, тест строкой, задачи фото', 'Ключи открываешь только после своей попытки',
             'Не понял — пиши вопрос в Telegram группы', 'Пропустил урок — смотри запись и сдавай ДЗ как обычно']
    lis = ''.join(f'<li class="box"><b>{k}</b>{x}</li>' for k, x in enumerate(items, 1))
    return slide(13, 'Что нужно от тебя', f'<ul class="g">{lis}</ul>', """
ul.g { position: absolute; left: 90px; right: 90px; top: 300px; margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
ul.g li { padding: 26px 32px; font: 800 32px/1.25 'Manrope'; display: flex; gap: 24px; align-items: center; min-height: 150px; }
ul.g li b { flex: none; width: 66px; height: 66px; display: flex; align-items: center; justify-content: center; background: #F13A43; color: #fff; font: 800 34px 'Unbounded'; }
ul.g li:nth-child(4n+2) b, ul.g li:nth-child(4n+3) b { background: #3FA65F; }
""")


def final() -> str:
    return doc(W, H, CSS + """
.slash { position: absolute; top: -200px; bottom: -200px; transform: skewX(-14deg); }
h1 { position: absolute; left: 300px; top: 230px; margin: 0; font: 800 100px/1.05 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }
.cta { position: absolute; left: 300px; top: 500px; padding: 26px 40px 32px; background: #F13A43; color: #fff; transform: rotate(-2deg); font: 800 46px/1.25 'Manrope'; }
.honest { position: absolute; left: 300px; right: 160px; top: 720px; margin: 0; font: 700 34px/1.4 'Manrope'; color: #B9B3A8; }
""", f"""<div class="slash" style="left:-40px;width:150px;background:{RED}"></div><div class="slash" style="left:150px;width:44px;background:{GREEN}"></div>
<h1>Увидимся<br>на первом уроке</h1><div class="cta">Вопросы — пиши в Telegram группы</div>
<p class="honest">Балл на ЕНТ зависит от твоей работы. Мы даём систему: уроки по учебникам НЦТ, практику в формате ЕНТ каждую неделю и честную проверку прогресса.</p>
<div class="pg">{N:02d} / {N}</div>""")


def main() -> None:
    pages = [cover(), numbers(), schedule(), teachers(), week(), materials(), homework(), ent(), tracks(), books(), textbooks(), checks(), rules(), final()]
    assert len(pages) == N
    OUT.mkdir(parents=True, exist_ok=True)
    pngs = []
    for i, html in enumerate(pages, 1):
        p = OUT / f'{i:02d}.png'
        shot(html, W, H, p)
        pngs.append(p)
    from PIL import Image
    ims = [Image.open(p).convert('RGB') for p in pngs]
    ims[0].save(OUT / 'ХимБио просто — для учеников.pdf', save_all=True, append_images=ims[1:], resolution=144)
    from pptx import Presentation
    from pptx.util import Emu
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    for p in pngs:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.shapes.add_picture(str(p), 0, 0, prs.slide_width, prs.slide_height)
    prs.save(OUT / 'ХимБио просто — для учеников.pptx')
    print(f'{len(pages)} slides -> {OUT}')


if __name__ == '__main__':
    main()
