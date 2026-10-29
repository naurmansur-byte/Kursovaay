"""Презентация для родителей 1920×1080 в стиле 2: гранты и ЕНТ по химии и биологии, затем курс «ХимБио просто».

Запуск: .venv/Scripts/python tools/social/parents_deck.py
Результат — «00 Материалы ХимБио просто/Продажи/Презентация для родителей/»: PNG слайдов, PDF и PPTX.
Данные и фото преподавателя — вне Git: «00 Материалы ХимБио просто/Преподаватели/teachers.json» (первая запись).
Цифры о грантах, порогах и формате ЕНТ — из источников на последнем слайде (проверено 29.10.2026); перед новым
учебным годом сверять с НЦТ и МНВО.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
from social import ATOM, doc, dna, shot  # noqa: E402

ROOT = HERE.parents[1]
PRIVATE = ROOT / '00 Материалы ХимБио просто' / 'Преподаватели'
OUT = ROOT / '00 Материалы ХимБио просто' / 'Продажи' / 'Презентация для родителей'
RED, GREEN, LGREEN, INK, PAPER, MUTED, CARD = '#F13A43', '#1F7A4A', '#3FA65F', '#151515', '#F3F0E8', '#B9B3A8', '#1D1D1D'
W, H = 1920, 1080

CSS = f"""
body {{ background-size: 80px 80px; }}
.eye {{ position: absolute; left: 90px; top: 64px; font: 800 26px 'Manrope'; letter-spacing: .16em; display: flex; align-items: center; gap: 14px; color: {MUTED}; }}
.eye i {{ width: 14px; height: 14px; border-radius: 50%; background: {RED}; }}
h2 {{ position: absolute; left: 90px; top: 118px; right: 90px; margin: 0; font: 800 70px/1.05 'Unbounded'; text-transform: uppercase; letter-spacing: -.01em; }}
.lead {{ position: absolute; left: 90px; top: 222px; right: 160px; margin: 0; font: 700 34px/1.3 'Manrope'; color: {MUTED}; }}
.pg {{ position: absolute; right: 90px; bottom: 50px; font: 800 24px 'Unbounded'; color: {MUTED}; }}
.src {{ position: absolute; left: 90px; bottom: 50px; right: 300px; font: 600 21px/1.3 'Manrope'; color: rgba(243,240,232,.5); }}
.box {{ background: {CARD}; border: 4px solid {PAPER}; padding: 30px 36px; }}
.red {{ color: {RED}; }} .green {{ color: {LGREEN}; }} .muted {{ color: {MUTED}; }}
b.num {{ font: 800 1em 'Unbounded'; }}
"""
N = 18


def slide(k: int, title: str, body: str, css: str = '', lead: str = '', src: str = '') -> str:
    head = f'<div class="eye"><i></i>ХИМБИО ПРОСТО · ДЛЯ РОДИТЕЛЕЙ</div><h2>{title}</h2>' if title else ''
    lead = f'<p class="lead">{lead}</p>' if lead else ''
    src = f'<div class="src">{src}</div>' if src else ''
    return doc(W, H, CSS + css, f'{head}{lead}{body}{src}<div class="pg">{k:02d} / {N}</div>')


def cover() -> str:
    return doc(W, H, CSS + """
.slash { position: absolute; top: -200px; bottom: -200px; transform: skewX(-14deg); }
h1 { position: absolute; left: 300px; top: 270px; margin: 0; font: 800 100px/1.04 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }
.plaque { position: absolute; left: 300px; top: 560px; padding: 14px 34px 20px; font-size: 50px; }
.sub { position: absolute; left: 300px; top: 700px; width: 1100px; margin: 0; font: 700 40px/1.35 'Manrope'; color: #B9B3A8; }
.atom { position: absolute; right: 70px; top: 40px; width: 220px; height: 220px; transform: rotate(-12deg); }
.dna { position: absolute; right: 210px; bottom: 90px; width: 180px; height: 380px; transform: rotate(14deg); }
""", f"""<div class="slash" style="left:-40px;width:150px;background:{RED}"></div><div class="slash" style="left:150px;width:44px;background:{GREEN}"></div>
{ATOM}{dna().replace('#F13A43', LGREEN)}
<h1>Химия + биология:<br>путь к гранту</h1><div class="plaque">для родителей</div>
<p class="sub">Что нужно знать о грантах и ЕНТ по профилю «химия — биология» и как мы готовим к экзамену</p>""")


def programs() -> str:
    groups = [('Медицина', RED, ['Общая медицина', 'Педиатрия', 'Стоматология', 'Общественное здоровье', 'Сестринское дело']),
              ('Фармация', RED, ['Фармация', 'Технология фармацевтического производства']),
              ('Наука', LGREEN, ['Биологические и смежные науки', 'Химия']),
              ('Педагогика', LGREEN, ['Подготовка учителей химии', 'Подготовка учителей биологии']),
              ('Ветеринария и агро', PAPER, ['Ветеринария', 'Растениеводство', 'Животноводство', 'Рыбное хозяйство', 'Производство продуктов питания'])]
    cols = ''.join(f'<div class="g" style="border-color:{c}"><h3 style="color:{c}">{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul></div>'
                   for t, c, xs in groups)
    return slide(2, 'Куда ведут химия и биология', f'<div class="grid">{cols}</div><div class="note">В конкурсе на грант можно указать <b>до 4 групп</b> образовательных программ с этими предметами</div>', """
.grid { position: absolute; left: 90px; right: 90px; top: 320px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 22px; }
.g { background: #1D1D1D; border-top: 10px solid; padding: 26px 24px 30px; min-height: 470px; }
.g h3 { margin: 0 0 20px; font: 800 30px/1.1 'Unbounded'; text-transform: uppercase; }
.g ul { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 14px; }
.g li { font: 700 27px/1.25 'Manrope'; }
.note { position: absolute; left: 90px; right: 90px; top: 830px; font: 800 32px/1.3 'Manrope'; }
.note b { color: #F13A43; }
""", '16 групп образовательных программ, в которые поступают по ЕНТ с химией и биологией',
        'Источник: univision.kz — группы образовательных программ для комбинации «химия — биология»')


def grants() -> str:
    rows = [('Педагогические науки', 13738), ('Естественные науки, математика и статистика', 9363),
            ('Сельское хозяйство и биоресурсы', 3145), ('Здравоохранение', 2700), ('Ветеринария', 1275)]
    bars = ''.join(f'<div class="r"><span class="l">{n}</span><span class="bar"><i style="width:{v / 13738 * 100:.1f}%"></i></span>'
                   f'<b>{v:,}</b></div>'.replace(',', ' ') for n, v in rows)
    return slide(3, 'Гранты 2026–2027', f"""<div class="big"><b>89 457</b><span>государственных образовательных грантов на 2026–2027 учебный год — всего по стране</span></div>
<div class="bars"><p>Направления, в которых есть программы для химии и биологии (бакалавриат)</p>{bars}</div>""", """
.big { position: absolute; left: 90px; top: 290px; width: 580px; }
.big b { display: block; font: 800 118px/1 'Unbounded'; color: #F13A43; white-space: nowrap; }
.big span { display: block; margin-top: 20px; font: 700 34px/1.3 'Manrope'; color: #B9B3A8; }
.bars { position: absolute; left: 720px; right: 90px; top: 290px; display: flex; flex-direction: column; gap: 26px; }
.bars p { margin: 0 0 6px; font: 800 26px 'Manrope'; letter-spacing: .08em; text-transform: uppercase; color: #B9B3A8; }
.r { display: grid; grid-template-columns: 1fr; gap: 8px; position: relative; }
.r .l { font: 700 30px/1.2 'Manrope'; }
.r .bar { display: block; height: 34px; background: #2A2A2A; margin-right: 200px; }
.r .bar i { display: block; height: 100%; background: #3FA65F; }
.r b { position: absolute; right: 0; bottom: -4px; font: 800 40px 'Unbounded'; }
""", src='Источник: Министерство науки и высшего образования РК (министр С. Нурбек), BES.media, 26.05.2026. Сколько грантов получит профиль «химия — биология», зависит от выбранных групп программ.')


def thresholds() -> str:
    cards = [('50', 'обычные вузы', PAPER), ('65', 'национальные вузы', PAPER), ('70', 'здравоохранение (медицина)', RED), ('75', 'педагогика', LGREEN)]
    cs = ''.join(f'<div class="c" style="border-color:{c}"><b style="color:{c}">{n}</b><small>из 140</small><span>{t}</span></div>' for n, t, c in cards)
    return slide(4, 'Минимальный балл для гранта', f"""<div class="cards">{cs}</div>
<div class="rules"><p><b>По каждому предмету тоже есть минимум:</b> история Казахстана и каждый профильный предмет — не меньше 5 баллов, грамотность чтения и математическая грамотность — не меньше 3.</p>
<p><b>С 1 сентября 2026 года</b> вуз может назначить дополнительный экзамен или свой проходной балл.</p>
<p class="key">Порог — это только вход в конкурс. Гранты получают те, у кого балл выше.</p></div>""", """
.cards { position: absolute; left: 90px; right: 90px; top: 300px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 26px; }
.c { background: #1D1D1D; border: 5px solid; padding: 26px 30px 30px; }
.c b { font: 800 120px/1 'Unbounded'; } .c small { margin-left: 12px; font: 800 28px 'Manrope'; color: #B9B3A8; }
.c span { display: block; margin-top: 14px; font: 800 30px/1.2 'Manrope'; text-transform: uppercase; }
.rules { position: absolute; left: 90px; right: 90px; top: 620px; display: flex; flex-direction: column; gap: 16px; }
.rules p { margin: 0; font: 700 30px/1.35 'Manrope'; }
.rules .key { margin-top: 6px; padding: 16px 26px 20px; background: #F13A43; color: #fff; font-weight: 800; display: inline-block; align-self: flex-start; transform: rotate(-1deg); }
""", src='Источник: приказ министра науки и высшего образования РК от 1 июля 2026 года (Zakon.kz, 08.07.2026). Пороги для поступления в 2026 году; на 2027 год их могут изменить.')


def ent() -> str:
    rows = [('История Казахстана', '20', '20', ''), ('Математическая грамотность', '10', '10', ''), ('Грамотность чтения', '10', '10', ''),
            ('Химия', '40', '50', 'red'), ('Биология', '40', '50', 'green')]
    tr = ''.join(f'<tr class="{c}"><td>{n}</td><td>{q}</td><td>{p}</td></tr>' for n, q, p, c in rows)
    return slide(5, 'Что такое ЕНТ', f"""<table><tr><th>Предмет</th><th>Заданий</th><th>Баллов</th></tr>{tr}
<tr class="sum"><td>Всего · 240 минут</td><td>120</td><td>140</td></tr></table>
<div class="side"><b>100</b><span>из 140 баллов дают химия и биология</span><p>Профильные предметы решают исход конкурса на грант</p></div>""", """
table { position: absolute; left: 90px; top: 300px; width: 1050px; border-collapse: collapse; font: 700 34px 'Manrope'; }
th { text-align: left; font: 800 24px 'Manrope'; letter-spacing: .08em; text-transform: uppercase; color: #B9B3A8; padding: 0 0 14px; }
td { padding: 18px 0; border-top: 2px solid rgba(243,240,232,.15); } td + td, th + th { text-align: right; width: 200px; }
tr.red td { color: #F13A43; font-weight: 800; } tr.green td { color: #3FA65F; font-weight: 800; }
tr.sum td { border-top: 4px solid #F3F0E8; font-weight: 800; }
.side { position: absolute; left: 1240px; right: 90px; top: 320px; background: #1D1D1D; border: 4px solid #F3F0E8; box-shadow: 16px 16px 0 #F13A43; padding: 34px 40px; }
.side b { display: block; font: 800 150px/1 'Unbounded'; color: #F13A43; }
.side span { display: block; margin-top: 10px; font: 800 34px/1.25 'Manrope'; }
.side p { margin: 18px 0 0; font: 700 28px/1.3 'Manrope'; color: #B9B3A8; }
""", src='Источник: Национальный центр тестирования (testcenter.kz), формат ЕНТ и спецификации предметов 2026 года.')


def profile() -> str:
    parts = [('25', 'один ответ из 4', '25 баллов · по 1', PAPER), ('5', 'на основе текста (контекст)', '5 баллов · по 1', PAPER),
             ('5', 'соответствие', '10 баллов · по 2', RED), ('5', 'один или несколько ответов из 6', '10 баллов · по 2', RED)]
    ps = ''.join(f'<div class="p" style="border-color:{c}"><b>{n}</b><span>{t}</span><em style="color:{c if c != PAPER else MUTED}">{s}</em></div>'
                 for n, t, s, c in parts)
    return slide(6, 'Химия и биология на ЕНТ', f"""<div class="ps">{ps}</div>
<div class="out"><b>20 из 50</b> баллов — задания по 2 балла. За одну ошибку ставят 1 балл, а лишняя галочка в «нескольких ответах» отнимает балл. Это мы тренируем с первой недели.</div>""", """
.ps { position: absolute; left: 90px; right: 90px; top: 300px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 26px; }
.p { background: #1D1D1D; border-top: 10px solid; padding: 28px 30px 32px; min-height: 330px; display: flex; flex-direction: column; gap: 14px; }
.p b { font: 800 110px/1 'Unbounded'; } .p span { font: 800 32px/1.2 'Manrope'; } .p em { font: 800 28px 'Manrope'; font-style: normal; margin-top: auto; }
.out { position: absolute; left: 90px; right: 90px; top: 720px; font: 700 34px/1.35 'Manrope'; }
.out b { font: 800 1em 'Unbounded'; color: #F13A43; }
""", '40 заданий и 50 баллов по каждому предмету', 'Источник: формат тестирования НЦТ; правила проведения ЕНТ (приказ № 204, п. 18, adilet.zan.kz).')


def dates() -> str:
    return slide(7, 'Когда сдают ЕНТ', f"""<div class="tl">
<div class="s"><span>Январь</span><b>Январское ЕНТ</b><p>Зимнее тестирование; в 2026 году регистрация открылась 22 декабря 2025</p></div>
<div class="s hot"><span>Май — июль</span><b>Основное ЕНТ</b><p>В 2026 году — с 10 мая по 10 июля; можно было сдать дважды и взять лучший результат</p></div>
<div class="s"><span>Лето</span><b>Конкурс грантов</b><p>Заявка по результату ЕНТ: до 4 групп образовательных программ</p></div></div>
<div class="note">Даты и правила ЕНТ-2027 Национальный центр тестирования объявит позже — мы следим и сразу сообщаем родителям. Курс заканчивается в конце мая, к основному ЕНТ.</div>""", """
.tl { position: absolute; left: 90px; right: 90px; top: 310px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; }
.s { background: #1D1D1D; border: 4px solid #F3F0E8; padding: 30px 34px 34px; min-height: 330px; }
.s.hot { border-color: #F13A43; box-shadow: 16px 16px 0 #F13A43; }
.s span { font: 800 26px 'Manrope'; letter-spacing: .1em; text-transform: uppercase; color: #B9B3A8; }
.s b { display: block; margin: 14px 0; font: 800 42px/1.1 'Unbounded'; text-transform: uppercase; }
.s p { margin: 0; font: 700 30px/1.3 'Manrope'; }
.note { position: absolute; left: 90px; right: 90px; top: 740px; font: 700 32px/1.35 'Manrope'; color: #B9B3A8; }
""", src='Источники: BES.media (основное ЕНТ-2026), Bizmedia (январское ЕНТ-2026), univision.kz (выбор групп). Даты 2027 года на 29.10.2026 не объявлены.')


def topics(k: int, subj: str) -> str:
    if subj == 'chem':
        title, acc = 'Что спрашивают: химия', RED
        blocks = [('Общая химия', ['Строение атома, химическая связь', 'Периодический закон', 'ОВР и электролиз', 'Скорость реакции и равновесие', 'Растворы, электролиты, гидролиз']),
                  ('Неорганическая', ['Металлы и неметаллы, производство металлов', 'Элементы I–VII групп и их соединения', 'Переходные элементы, комплексы', 'Производство серной кислоты']),
                  ('Органическая', ['Углеводороды', 'Спирты, альдегиды, кислоты, жиры', 'Углеводы', 'Амины, аминокислоты, белки', 'Полимеры, нефть, новые материалы']),
                  ('Расчёты', ['Выход продукта, смеси', 'Формула по продуктам горения', 'Параллельные реакции, олеум', 'Задачи на кинетику и электролиз'])]
        lead = '19 тем спецификации НЦТ — все они есть в программе курса'
    else:
        title, acc = 'Что спрашивают: биология', LGREEN
        blocks = [('Организмы и среда', ['Разнообразие организмов; экосистема, популяция; влияние человека', 'Питание', 'Транспорт веществ', 'Дыхание', 'Выделение']),
                  ('Регуляция и движение', ['Движение, биофизика', 'Координация и регуляция']),
                  ('Наследственность и эволюция', ['Размножение, рост и развитие', 'Клеточный цикл, клеточная биология', 'Генетика, селекция, эволюция']),
                  ('Прикладные науки', ['Молекулярная биология и биохимия', 'Микробиология и биотехнология', 'Биомедицина и биоинформатика'])]
        lead = '12 тем в 3 разделах спецификации НЦТ — все они есть в программе курса'
    bs = ''.join(f'<div class="b"><h3>{t}</h3><ul>{"".join(f"<li><i></i>{x}</li>" for x in xs)}</ul></div>' for t, xs in blocks)
    return slide(k, title, f'<div class="bs">{bs}</div>', f"""
.bs {{ position: absolute; left: 90px; right: 90px; top: 310px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }}
.b {{ background: #1D1D1D; border-top: 10px solid {acc}; padding: 26px 26px 30px; min-height: 560px; }}
.b h3 {{ margin: 0 0 20px; font: 800 30px/1.15 'Unbounded'; text-transform: uppercase; color: {acc}; }}
.b ul {{ margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 16px; }}
.b li {{ font: 700 27px/1.25 'Manrope'; display: flex; gap: 14px; }} .b li i {{ flex: none; width: 12px; height: 12px; margin-top: 12px; background: {acc}; }}
""", lead, 'Источник: спецификации тестов НЦТ «для использования с 2026 года» (testcenter.kz).')


def books() -> str:
    chem = ['7 класс — 2017', '8 класс — 2018', '9 класс, части 1–2 — 2019', '10 класс ЕМН, части 1–2 — 2019', '11 класс ЕМН, части 1–2 — 2020']
    bio = ['7 класс — Очкур, Курмангалиева (Мектеп); Соловьева и др. (Атамұра)', '8 класс — Соловьева, Ибраимова (Атамұра)',
           '9 класс — Асанов, Соловьева, Ибраимова (Атамұра)', '10 класс ЕМН — Очкур, Курмангалиева, Нуртаева (Мектеп)',
           '11 класс ЕМН — Абылайханова, Қалыбаева, Пәрімбекова (Мектеп)']
    li = lambda xs, c: ''.join(f'<li><i style="background:{c}"></i>{x}</li>' for x in xs)  # noqa: E731
    return slide(10, 'По каким учебникам вопросы', f"""<div class="two">
<div class="col"><h3 class="red">Химия</h3><p>Оспанова, Аухадиева, Белоусова · «Мектеп»</p><ul>{li(chem, RED)}</ul></div>
<div class="col"><h3 class="green">Биология</h3><p>линии из перечня НЦТ</p><ul>{li(bio, LGREEN)}</ul></div></div>
<div class="note">Каждый урок курса построен по параграфам этих учебников. Неточности в учебниках мы проверяем и исправляем — уже нашли и разобрали 192.</div>""", """
.two { position: absolute; left: 90px; right: 90px; top: 300px; display: grid; grid-template-columns: 1fr 1.35fr; gap: 30px; }
.col { background: #1D1D1D; border: 4px solid #F3F0E8; padding: 28px 34px 32px; }
.col h3 { margin: 0; font: 800 40px 'Unbounded'; text-transform: uppercase; } .col p { margin: 8px 0 22px; font: 700 26px 'Manrope'; color: #B9B3A8; }
.col ul { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 14px; }
.col li { font: 700 27px/1.25 'Manrope'; display: flex; gap: 14px; } .col li i { flex: none; width: 12px; height: 12px; margin-top: 12px; }
.note { position: absolute; left: 90px; right: 90px; top: 830px; font: 800 30px/1.35 'Manrope'; }
""", 'НЦТ рекомендует эти учебники — задания ЕНТ опираются на их содержание',
        'Источник: перечни рекомендуемых учебников НЦТ по химии и биологии (testcenter.kz).')


def course() -> str:
    items = [('4', 'урока в неделю: 2 по химии и 2 по биологии'), ('90', 'минут каждый урок, онлайн в Google Meet'),
             ('7', 'месяцев: со 2 ноября 2026 по конец мая 2027'), ('39', 'недель уроков из 50 уже подготовлены')]
    its = ''.join(f'<div class="i"><b>{n}</b><span>{t}</span></div>' for n, t in items)
    week = ['Конспект урока и памятка', 'Задания сразу после урока', 'Домашняя работа в трёх уровнях: A — углубление, B — закрепление, C — поддержка',
            'Проверка ДЗ и разбор ошибок', 'Контроль недели — 10 минут в формате ЕНТ']
    return slide(11, 'Наш курс', f"""<div class="its">{its}</div><div class="wk"><h3>Каждую неделю у ученика</h3><ul>{"".join(f"<li><i></i>{x}</li>" for x in week)}</ul></div>""", """
.its { position: absolute; left: 90px; top: 300px; width: 820px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.i { background: #1D1D1D; border: 4px solid #F3F0E8; padding: 24px 28px 28px; min-height: 250px; }
.i b { display: block; font: 800 96px/1 'Unbounded'; color: #F13A43; } .i:nth-child(even) b { color: #3FA65F; }
.i span { display: block; margin-top: 12px; font: 800 28px/1.25 'Manrope'; }
.wk { position: absolute; left: 980px; right: 90px; top: 300px; }
.wk h3 { margin: 0 0 24px; font: 800 34px 'Unbounded'; text-transform: uppercase; }
.wk ul { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 20px; }
.wk li { font: 700 30px/1.3 'Manrope'; display: flex; gap: 16px; } .wk li i { flex: none; width: 16px; height: 16px; margin-top: 12px; background: #F13A43; }
""", 'Живой преподаватель, химия и биология в одном пакете')


def schedule() -> str:
    days = [('Пн', 'Химия', 'новая тема', RED), ('Вт', 'Биология', 'новая тема', LGREEN), ('Ср', 'Дома', 'домашняя работа', MUTED),
            ('Чт', 'Химия', 'разбор ДЗ, практика, контроль', RED), ('Пт', 'Биология', 'разбор ДЗ, практика, контроль', LGREEN)]
    ds = ''.join(f'<div class="d" style="border-color:{c}"><span>{d}</span><b style="color:{c}">{s}</b><p>{t}</p></div>' for d, s, t, c in days)
    return slide(12, 'Расписание', f"""<div class="ds">{ds}</div>
<div class="times"><div><b>18:00–19:30</b><span>или</span><b>19:30–21:00</b></div><p>время группы — на выбор</p></div>
<div class="pause"><b>Каникулы:</b> 28 декабря — 10 января и неделя Наурыза (22–28 марта). Праздничные дни переносим, уроки не теряются.</div>""", """
.ds { position: absolute; left: 90px; right: 90px; top: 300px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 20px; }
.d { background: #1D1D1D; border-top: 10px solid; padding: 24px 26px 28px; min-height: 290px; }
.d span { font: 800 30px 'Unbounded'; color: #B9B3A8; } .d b { display: block; margin: 16px 0 10px; font: 800 38px 'Unbounded'; text-transform: uppercase; }
.d p { margin: 0; font: 700 27px/1.3 'Manrope'; }
.times { position: absolute; left: 90px; top: 650px; display: flex; align-items: baseline; gap: 30px; }
.times div { display: flex; align-items: baseline; gap: 24px; } .times b { font: 800 64px 'Unbounded'; } .times span { font: 800 30px 'Manrope'; color: #B9B3A8; }
.times p { margin: 0; font: 800 30px 'Manrope'; color: #F13A43; text-transform: uppercase; letter-spacing: .06em; }
.pause { position: absolute; left: 90px; right: 90px; top: 800px; font: 700 30px/1.35 'Manrope'; color: #B9B3A8; } .pause b { color: #F3F0E8; }
""", 'Первые уроки — 2 и 3 ноября 2026; 4 урока в неделю по 90 минут')


def teacher(t: dict) -> str:
    photo = PRIVATE / t['photo'] if t.get('photo') else None
    if photo and photo.exists():
        pic = (f'<div class="sl" style="left:150px;width:160px;background:{RED}"></div><div class="sl" style="left:340px;width:44px;background:{GREEN}"></div>'
               f'<img src="{photo.as_uri()}">')
    else:
        pic = '<div class="ph">фото</div>'
    stats = ''.join(f'<div class="st"><b>{n.split("/")[0]}<small>/{n.split("/")[1]}</small></b><span>{lbl}</span></div>' for n, lbl in t['stats'][:2])
    facts = ''.join(f'<li><i></i>{f}</li>' for f in t.get('facts', [])[:3])
    return slide(13, '', f"""<div class="photo">{pic}</div><div class="eye2"><i></i>ПРЕПОДАВАТЕЛЬ КУРСА</div>
<h1>{t['name']}</h1><div class="sts">{stats}</div><ul>{facts}</ul>""", f"""
.photo {{ position: absolute; left: 110px; top: 110px; width: 640px; height: 820px; border: 6px solid {PAPER}; box-shadow: -22px 22px 0 {RED};
  transform: rotate(-2deg); background: #E9E4D8; overflow: hidden; }}
.photo .sl {{ position: absolute; top: -100px; bottom: -100px; transform: skewX(-14deg); }}
.photo img {{ position: relative; width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%; display: block; }}
.ph {{ height: 100%; display: flex; align-items: center; justify-content: center; font: 800 40px 'Manrope'; color: #8F897F; }}
.eye2 {{ position: absolute; left: 870px; top: 140px; font: 800 26px 'Manrope'; letter-spacing: .16em; display: flex; align-items: center; gap: 14px; color: {MUTED}; }}
.eye2 i {{ width: 14px; height: 14px; border-radius: 50%; background: {RED}; }}
h1 {{ position: absolute; left: 870px; top: 190px; margin: 0; font: 800 110px/1 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }}
.sts {{ position: absolute; left: 870px; top: 370px; display: flex; gap: 70px; }}
.st b {{ font: 800 140px/1 'Unbounded'; }} .st b small {{ font-size: 48px; color: {MUTED}; }}
.st:first-child b {{ color: {RED}; }} .st:nth-child(2) b {{ color: {LGREEN}; }}
.st span {{ display: block; margin-top: 10px; font: 800 28px/1.2 'Manrope'; text-transform: uppercase; letter-spacing: .04em; color: {MUTED}; }}
ul {{ position: absolute; left: 870px; right: 90px; top: 640px; margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 18px; }}
li {{ font: 700 34px/1.3 'Manrope'; display: flex; gap: 18px; }} li i {{ flex: none; width: 16px; height: 16px; margin-top: 14px; background: {RED}; }}
""")


def parents() -> str:
    steps = [('1', 'Практический тест', 'раз в месяц — в формате ЕНТ, по пройденным темам', RED),
             ('2', 'Разбор с учеником', 'каждая ошибка — по теме и причине', LGREEN),
             ('3', 'Отчёт родителю', 'баллы, сильные и слабые темы, как идёт подготовка', RED),
             ('4', 'План на месяц', 'что подтягиваем и какие задания добавляем', LGREEN)]
    ss = ''.join(f'<div class="s"><b style="background:{c}">{n}</b><h3>{t}</h3><p>{d}</p></div>' for n, t, d, c in steps)
    return slide(14, 'Родители всегда в курсе', f"""<div class="ss">{ss}</div>
<div class="note">Каждую неделю — проверка домашней работы и короткий контроль. На связи с родителями в WhatsApp или Telegram: можно спросить о ребёнке в любой момент.</div>""", """
.ss { position: absolute; left: 90px; right: 90px; top: 310px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.s { background: #1D1D1D; border: 4px solid #F3F0E8; padding: 28px 30px 32px; min-height: 380px; position: relative; }
.s b { display: flex; width: 80px; height: 80px; align-items: center; justify-content: center; font: 800 42px 'Unbounded'; color: #fff; }
.s h3 { margin: 26px 0 14px; font: 800 34px/1.15 'Unbounded'; text-transform: uppercase; } .s p { margin: 0; font: 700 28px/1.3 'Manrope'; color: #B9B3A8; }
.note { position: absolute; left: 90px; right: 90px; top: 780px; font: 700 32px/1.35 'Manrope'; }
""", 'Ежемесячный цикл: тест → разбор → отчёт → план')


def trial() -> str:
    items = ['Входная диагностика: 28 заданий по химии и 28 по биологии', 'Настоящие уроки по обоим предметам',
             'Личный разбор результатов с учеником', 'Уровень A, B или C и рекомендации — родителю']
    return slide(15, 'Пробная неделя — бесплатно', f"""<div class="pl">сначала попробуйте</div><ul>{"".join(f"<li><b>{k}</b>{x}</li>" for k, x in enumerate(items, 1))}</ul>
<div class="note">Решение о курсе — после пробной недели, когда понятно, подходит ли формат ребёнку.</div>""", """
.pl { position: absolute; left: 90px; top: 250px; padding: 10px 26px 16px; background: #3FA65F; color: #fff; font: 800 36px 'Unbounded'; text-transform: uppercase; transform: rotate(-2deg); }
ul { position: absolute; left: 90px; right: 90px; top: 360px; margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
li { background: #1D1D1D; border: 4px solid #F3F0E8; padding: 28px 32px; font: 800 34px/1.25 'Manrope'; display: flex; gap: 24px; align-items: center; min-height: 170px; }
li b { flex: none; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; background: #F13A43; color: #fff; font: 800 36px 'Unbounded'; }
.note { position: absolute; left: 90px; right: 90px; top: 800px; font: 700 32px/1.35 'Manrope'; color: #B9B3A8; }
""")


def price() -> str:
    return slide(16, 'Стоимость', f"""<div class="old"><s>19 500 ₸</s><span>в месяц за химию и биологию</span></div>
<div class="new"><div class="off">−30 %</div><b>13 650 ₸</b><span>в месяц — первым 20 ученикам,<br>на весь курс, все 7 месяцев</span></div>
<ul><li><i></i>Оплата помесячно через Kaspi</li><li><i></i>Химия и биология — одним пакетом</li><li><i></i>Пробная неделя — бесплатно</li></ul>""", """
.old { position: absolute; left: 90px; top: 320px; } .old s { font: 800 80px 'Unbounded'; color: #B9B3A8; text-decoration-color: #F13A43; text-decoration-thickness: 8px; }
.old span { display: block; margin-top: 10px; font: 700 30px 'Manrope'; color: #B9B3A8; }
.new { position: absolute; left: 90px; top: 600px; width: 1000px; background: #1D1D1D; border: 5px solid #F13A43; box-shadow: 18px 18px 0 #F13A43; padding: 34px 44px 40px; }
.new .off { position: absolute; right: -30px; top: -50px; padding: 10px 26px 16px; background: #F13A43; color: #fff; font: 800 54px 'Unbounded'; transform: rotate(6deg); }
.new b { display: block; font: 800 140px/1 'Unbounded'; } .new span { display: block; margin-top: 16px; font: 800 34px/1.3 'Manrope'; }
ul { position: absolute; left: 1200px; right: 90px; top: 620px; margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 26px; }
li { font: 800 34px/1.3 'Manrope'; display: flex; gap: 18px; } li i { flex: none; width: 18px; height: 18px; margin-top: 12px; background: #3FA65F; }
""")


def final() -> str:
    return doc(W, H, CSS + """
.slash { position: absolute; top: -200px; bottom: -200px; transform: skewX(-14deg); }
h1 { position: absolute; left: 300px; top: 210px; margin: 0; font: 800 96px/1.05 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }
.cta { position: absolute; left: 300px; top: 470px; padding: 26px 40px 32px; background: #F13A43; color: #fff; transform: rotate(-2deg); font: 800 46px/1.25 'Manrope'; }
.cta span { font-family: 'Unbounded'; }
.where { position: absolute; left: 300px; top: 720px; font: 800 40px 'Manrope'; } .where b { font-family: 'Unbounded'; }
.honest { position: absolute; left: 300px; right: 140px; top: 840px; margin: 0; font: 700 32px/1.35 'Manrope'; color: #B9B3A8; }
.pg { position: absolute; right: 90px; bottom: 50px; font: 800 24px 'Unbounded'; color: #B9B3A8; }
""", f"""<div class="slash" style="left:-40px;width:150px;background:{RED}"></div><div class="slash" style="left:150px;width:44px;background:{GREEN}"></div>
<h1>Запишитесь<br>на пробную неделю</h1><div class="cta">Напишите <span>«ПРОГРАММА»</span> — пришлём программу и время групп</div>
<div class="where">WhatsApp или Instagram <b>@himbio.prosto</b></div>
<p class="honest">Мы не обещаем баллы и грант — это зависит от работы ученика. Мы даём систему подготовки по учебникам НЦТ, практику в формате ЕНТ и честный контроль каждый месяц.</p>
<div class="pg">17 / {N}</div>""")


def sources() -> str:
    rows = ['Национальный центр тестирования: формат ЕНТ, спецификации «Химия» и «Биология» для использования с 2026 года, перечни учебников — testcenter.kz',
            'Правила проведения ЕНТ, приказ № 204, п. 18 (баллы за задания) — adilet.zan.kz',
            'Приказ министра науки и высшего образования РК от 1 июля 2026 года: минимальные пороговые баллы — Zakon.kz, 08.07.2026',
            'Распределение 89 457 грантов на 2026–2027 учебный год, МНВО РК — BES.media, 26.05.2026',
            'Основное ЕНТ-2026: 10 мая — 10 июля, две попытки — BES.media; январское ЕНТ-2026 — Bizmedia, 19.12.2025',
            'Группы образовательных программ для «химия — биология», выбор до 4 групп — univision.kz']
    return slide(18, 'Источники', '<ol>' + ''.join(f'<li>{r}</li>' for r in rows) + '</ol>', """
ol { position: absolute; left: 90px; right: 90px; top: 280px; margin: 0; padding-left: 40px; display: flex; flex-direction: column; gap: 22px; }
li { font: 700 28px/1.35 'Manrope'; color: #B9B3A8; } li::marker { color: #F13A43; font-weight: 800; }
""", '', 'Данные проверены 29.10.2026. Правила на 2027 год могут измениться — сверяем с НЦТ и МНВО.')


def main() -> None:
    data = json.loads((PRIVATE / 'teachers.json').read_text(encoding='utf-8'))
    pages = [cover(), programs(), grants(), thresholds(), ent(), profile(), dates(), topics(8, 'chem'), topics(9, 'bio'), books(),
             course(), schedule(), teacher(data[0]), parents(), trial(), price(), final(), sources()]
    OUT.mkdir(parents=True, exist_ok=True)
    pngs = []
    for i, html in enumerate(pages, 1):
        p = OUT / f'{i:02d}.png'
        shot(html, W, H, p)
        pngs.append(p)
    from PIL import Image
    ims = [Image.open(p).convert('RGB') for p in pngs]
    ims[0].save(OUT / 'ХимБио просто — для родителей.pdf', save_all=True, append_images=ims[1:], resolution=144)
    from pptx import Presentation
    from pptx.util import Emu
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    for p in pngs:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.shapes.add_picture(str(p), 0, 0, prs.slide_width, prs.slide_height)
    prs.save(OUT / 'ХимБио просто — для родителей.pptx')
    print(f'{len(pages)} slides -> {OUT}')


if __name__ == '__main__':
    main()
