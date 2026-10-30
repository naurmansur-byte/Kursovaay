"""Приём преподавателя биологии: документ для отбора (с ключом и баллами) и задание кандидату (без ключей).

Запуск из корня: .venv/Scripts/python.exe -I tools/social/teacher_hiring.py <html_out_для_артефакта>
Результат: HTML для артефакта и два PDF в «00 Материалы ХимБио просто/Найм преподавателей/».
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools' / 'handout'))
from handout import chrome  # noqa: E402

FONTS = (ROOT / 'content/brand/fonts').as_uri()
OUT = ROOT / '00 Материалы ХимБио просто' / 'Найм преподавателей'

CSS = """
/* Рабочий документ отбора: зелёный акцент биологии, этапы по порядку, таблицы баллов, ключ в отдельных плашках. */
:root {
  --bg: #F3F2EC; --card: #FFFFFF; --ink: #141714; --muted: #5C625B; --line: #D6D9CF;
  --accent: #1F7A4A; --soft: #DDEFE4; --warn: #B4232B; --warn-soft: #FBE4E4;
  --display: 'Unbounded', 'Arial Black', sans-serif; --body: 'Manrope', 'Segoe UI', Arial, sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #121412; --card: #1A1D1A; --ink: #EEF0EA; --muted: #A3AA9F; --line: #2C302B;
  --accent: #5CC08A; --soft: #16301F; --warn: #FF6B70; --warn-soft: #3A1D1F; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #121412; --card: #1A1D1A; --ink: #EEF0EA; --muted: #A3AA9F; --line: #2C302B;
  --accent: #5CC08A; --soft: #16301F; --warn: #FF6B70; --warn-soft: #3A1D1F; color-scheme: dark }
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font: 500 16px/1.55 var(--body); margin: 0; }
.wrap { max-width: 980px; margin: 0 auto; padding-block: 40px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 44px; }
header { display: flex; flex-direction: column; gap: 14px; }
.eyebrow { font: 800 12px/1 var(--body); letter-spacing: .16em; text-transform: uppercase; color: var(--accent); }
h1 { font: 800 clamp(28px, 5vw, 44px)/1.08 var(--display); margin: 0; text-wrap: balance; letter-spacing: -.01em; }
.lead { font-size: 18px; max-width: 66ch; margin: 0; color: var(--muted); }
.facts { display: flex; flex-wrap: wrap; gap: 10px; margin: 6px 0 0; padding: 0; list-style: none; }
.facts li { border: 1.5px solid var(--line); border-radius: 999px; padding: 6px 14px; font-weight: 700; font-size: 14px; }
.facts b { font-family: var(--display); font-weight: 700; color: var(--accent); }
nav { display: flex; flex-wrap: wrap; gap: 8px 20px; font-weight: 800; font-size: 14px; }
nav a { color: var(--ink); text-decoration: none; border-bottom: 2px solid var(--line); padding-bottom: 2px; }
nav a:hover, nav a:focus-visible { border-color: var(--accent); outline: none; }
section { display: flex; flex-direction: column; gap: 16px; }
.sec-head { break-after: avoid; border-bottom: 3px solid var(--accent); padding-bottom: 10px; display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px 16px; }
h2 { font: 800 clamp(21px, 3.2vw, 28px)/1.15 var(--display); margin: 0; color: var(--accent); text-wrap: balance; }
.sec-head p { margin: 0; color: var(--muted); font-weight: 700; font-size: 14px; }
h3 { font: 800 17px/1.3 var(--body); margin: 0; text-wrap: balance; }
p { margin: 0; max-width: 72ch; }
.grid2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 16px; }
.card { min-width: 0; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px;
  display: flex; flex-direction: column; gap: 10px; break-inside: avoid; }
ul.dots { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px; }
ul.dots li::marker { color: var(--accent); }
.stages { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 12px; counter-reset: st; }
.stages li { counter-increment: st; display: grid; grid-template-columns: 52px minmax(0, 1fr) auto; gap: 4px 16px;
  background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 14px 18px; break-inside: avoid; }
.stages li::before { content: counter(st); font: 800 26px/1 var(--display); color: var(--accent); grid-row: span 2; padding-top: 2px; }
.stages .pts { font: 800 14px/1.3 var(--body); color: var(--muted); text-align: right; white-space: nowrap; }
.stages p { grid-column: 2 / 4; color: var(--muted); font-size: 15px; }
table { width: 100%; border-collapse: collapse; font-size: 15px; }
th { text-align: left; font: 800 12px/1.3 var(--body); text-transform: uppercase; letter-spacing: .08em; color: var(--muted);
  padding: 8px 10px; border-bottom: 2px solid var(--line); }
td { padding: 9px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
td.n { font-variant-numeric: tabular-nums; font-weight: 800; text-align: right; white-space: nowrap; }
tr.total td { font-weight: 800; border-bottom: none; }
.tbl { overflow-x: auto; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 6px 8px; }
.stop { background: var(--warn-soft); border-radius: 12px; padding: 16px 18px; display: flex; flex-direction: column; gap: 8px; break-inside: avoid; }
.stop h3 { color: var(--warn); }
.task { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 14px 18px; display: flex; flex-direction: column; gap: 8px; break-inside: avoid; }
.task .q b { color: var(--accent); }
.opts { margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 18px; font-size: 15px; }
.opts.six { grid-template-columns: repeat(3, minmax(0, 1fr)); }
@media (max-width: 560px) { .opts, .opts.six { grid-template-columns: minmax(0, 1fr); } }
.key { background: var(--soft); border-radius: 8px; padding: 8px 12px; font-size: 15px; }
.key b { color: var(--accent); }
.frag { background: var(--card); border: 1px dashed var(--accent); border-radius: 12px; padding: 16px 18px; display: flex; flex-direction: column; gap: 8px; }
.note { color: var(--muted); font-size: 14px; }
.blank { display: inline-block; min-width: 14ch; border-bottom: 1.5px solid var(--muted); color: var(--muted); }
footer { color: var(--muted); font-size: 13px; border-top: 1px solid var(--line); padding-top: 16px; }
@media (max-width: 560px) { .stages li { grid-template-columns: 40px minmax(0, 1fr); } .stages .pts { grid-column: 2; text-align: left; } .stages p { grid-column: 2; } }
@media print {
  @page { size: A4; margin: 14mm 13mm; }
  body { background: #fff; font-size: 12.5px; }
  .wrap { padding: 0; gap: 24px; max-width: none; }
  nav { display: none; }
  .card, .task, .stages li, .tbl { padding: 10px 12px; }
  .pb { break-before: page; }
  .tbl { break-inside: avoid; }
}
"""

# ---------- общее содержание ----------

ROLE = """
<section id="role">
  <div class="sec-head"><h2>Кого ищем</h2><p>курс 1 ноября 2026 — май 2027</p></div>
  <p>«ХимБио просто» — онлайн-подготовка к ЕНТ по химии и биологии для 11 класса. Два урока по 90 минут в неделю в Google Meet, домашние задания и вопросы — в Telegram. Курс уже написан: 23 содержательные недели и два учебных пробника. Преподаватель ведёт уроки по готовым комплектам, а не пишет курс с нуля.</p>
  <div class="grid2">
    <div class="card"><h3>Что делает преподаватель</h3><ul class="dots">
      <li>Ведёт два урока в неделю по плану и презентации недели.</li>
      <li>Заранее, за неделю до уроков, проверяет комплект недели: факты, ключи, время.</li>
      <li>Проверяет ДЗ в Telegram: строку теста и фото решений.</li>
      <li>Назначает ученику вариант A, B или C и ведёт карту пробелов.</li>
      <li>Проводит и разбирает два пробника в мае.</li>
    </ul></div>
    <div class="card"><h3>Обязательно</h3><ul class="dots">
      <li>Биология 7–11 классов на уровне всех 12 тем спецификации ЕНТ.</li>
      <li>Знает формат профильного предмета ЕНТ: 40 заданий, 50 баллов.</li>
      <li>Объясняет по учебникам из перечня НЦТ и замечает в них ошибки.</li>
      <li>Уверенно ведёт урок онлайн: Meet, демонстрация экрана, Telegram.</li>
      <li>Грамотная русская речь и письмо.</li>
    </ul></div>
    <div class="card"><h3>Желательно</h3><ul class="dots">
      <li>Опыт подготовки к ЕНТ или олимпиадам.</li>
      <li>Казахский язык.</li>
      <li>Химия на школьном уровне: курс связывает два предмета.</li>
    </ul></div>
    <div class="card"><h3>Условия</h3><ul class="dots">
      <li>Оплата: <span class="blank">заполняет Мансур</span></li>
      <li>Расписание групп: <span class="blank">заполняет Мансур</span></li>
      <li>Договор и испытательный срок: <span class="blank">заполняет Мансур</span></li>
    </ul></div>
  </div>
</section>
"""

STYLE = """
<section id="style">
  <div class="sec-head"><h2>Наш стиль преподавания</h2><p>это и проверяем на отборе</p></div>
  <div class="grid2">
    <div class="card"><h3>Порядок объяснения</h3><p>Всегда один: <b>почему → алгоритм → разные примеры → ловушка → ученик решает сам</b>. Ключ показываем после попытки. Ошибку ученика разбираем по причине, а не заменяем готовым ответом.</p></div>
    <div class="card"><h3>Только по учебникам НЦТ</h3><p>Определения, факты, числа — как в учебниках из перечня НЦТ: по ним составляют задания ЕНТ. В учебниках есть ошибки — говорим научно верно: «в учебнике написано…, верно…».</p></div>
    <div class="card"><h3>Формат ЕНТ с первой недели</h3><p>Один ответ, несколько ответов (2/1/0 балла), соответствие, задания к контексту. Опыт и график читаем по схеме: что меняли, где контроль, вывод только в пределах данных.</p></div>
    <div class="card"><h3>Урок и тон</h3><p>Урок 2 недели: 20 минут вопросов и повторения, разбор ДЗ, практика в формате ЕНТ, 10-минутный контроль. С учеником — на «ты», коротко, без воды. Балл и грант не обещаем; вариант A/B/C — маршрут, а не прогноз.</p></div>
  </div>
</section>
"""

STAGES = """
<section id="stages">
  <div class="sec-head"><h2>Этапы отбора</h2><p>100 баллов, проходной — 70</p></div>
  <ol class="stages">
    <li><h3>Анкета и звонок</h3><span class="pts">15 минут · без баллов</span><p>Образование, опыт, свободные часы, техника для онлайн-урока. Рассказываем о курсе и стиле. Отправляем «Задание кандидату».</p></li>
    <li><h3>Задание по предмету</h3><span class="pts">60 минут дома · 40 баллов</span><p>Задания в формате ЕНТ, ошибки учебников, ответ ученику в Telegram — часть 1 задания кандидату.</p></li>
    <li><h3>Проверка фрагмента курса</h3><span class="pts">30 минут дома · 20 баллов</span><p>Фрагмент конспекта, в котором шесть ошибок: найти и исправить. Так преподаватель будет проверять комплекты недель.</p></li>
    <li><h3>Пробный урок</h3><span class="pts">20 минут в Meet · 30 баллов</span><p>Тема на выбор из двух. Мы играем учеников, один из нас ошибается. Смотрим порядок объяснения и работу с ошибкой.</p></li>
    <li><h3>Беседа о методике</h3><span class="pts">20 минут · 10 баллов</span><p>Пять вопросов о ситуациях на курсе: ученик, родитель, ошибка в материале.</p></li>
  </ol>
  <div class="stop"><h3>Стоп-факторы — отказ при любой сумме</h3><ul class="dots">
    <li>Научная ошибка, которую кандидат повторяет и после подсказки.</li>
    <li>Обещание балла или гранта ученику или родителю.</li>
    <li>На пробном уроке сразу даёт ответ вместо разбора ошибки ученика.</li>
    <li>Опоздание на пробный урок без предупреждения.</li>
  </ul></div>
  <p><b>Решение.</b> 70 баллов и больше, стоп-факторов нет — предлагаем первую неделю как испытательную: преподаватель проверяет комплект недели и ведёт уроки, мы смотрим запись и даём обратную связь.</p>
</section>
"""

# ---------- задание кандидату ----------

def opts(*items: str) -> str:
    cls = 'opts six' if len(items) == 6 else 'opts'
    return f'<ul class="{cls}">' + ''.join(f'<li>{L}) {t}</li>' for L, t in zip('АБВГДЕ', items)) + '</ul>'


def task(num: str, kind: str, q: str, body: str = '', key: str = '', show_key: bool = False) -> str:
    k = f'<div class="key">{key}</div>' if show_key and key else ''
    return f'<div class="task"><div class="q"><b>{num}.</b> <span class="note">{kind}</span> {q}</div>{body}{k}</div>'


def candidate(show_key: bool) -> str:
    K = show_key
    T = []
    T.append(task('1', 'Один ответ.', 'Какое вещество — полисахарид?', opts('сахароза', 'мальтоза', 'гликоген', 'глюкоза'),
                  '<b>В.</b> Гликоген — полисахарид; сахароза и мальтоза — дисахариды, глюкоза — моносахарид.', K))
    T.append(task('2', 'Один ответ.', 'Где проходит световая фаза фотосинтеза?', opts('в строме хлоропласта', 'в тилакоидах', 'в матриксе митохондрии', 'в цитоплазме'),
                  '<b>Б.</b> Световая фаза — тилакоиды, темновая — строма.', K))
    T.append(task('3', 'Один ответ.', 'Сколько молекул АТФ даёт кислородный этап распада глюкозы в учебной модели?', opts('2', '36', '38', '4'),
                  '<b>Б.</b> Гликолиз — 2, кислородный этап — 36, всего — 38.', K))
    T.append(task('4', 'Один ответ.', 'Какой набор хромосом у первичного ядра эндосперма цветковых?', opts('n', '2n', '3n', '4n'),
                  '<b>В.</b> Спермий n + центральная клетка 2n = 3n.', K))
    T.append(task('5', 'Один ответ.', 'Как работает Na⁺/K⁺-насос за один цикл?', opts('2 Na⁺ наружу, 3 K⁺ внутрь', '3 Na⁺ наружу, 2 K⁺ внутрь', '3 K⁺ наружу, 2 Na⁺ внутрь', '1 Na⁺ и 1 K⁺ в одну сторону'),
                  '<b>Б.</b> 3 Na⁺ наружу, 2 K⁺ внутрь.', K))
    T.append(task('6', 'Один ответ.', 'Главная функция цитокининов:', opts('деление клеток', 'образование корней', 'рост междоузлий', 'закрывание устьиц'),
                  '<b>А.</b> Цитокинины — деление клеток; корнеобразование — ауксин, междоузлия — гиббереллин.', K))
    T.append(task('7', 'Несколько ответов (2 балла).', 'Какие утверждения о ДНК верны?',
                  opts('между А и Т — две водородные связи', 'между Г и Ц — три водородные связи', 'расстояние между соседними парами — 3,4 нм',
                       'один виток — около 10 пар и 3,4 нм', 'в ДНК есть урацил', 'репликация консервативная'),
                  '<b>АБГ.</b> Между парами 0,34 нм; урацил — в РНК; репликация полуконсервативная.', K))
    T.append(task('8', 'Несколько ответов (2 балла).', 'Что верно о первичной моче?',
                  opts('в ней есть глюкоза', 'в ней есть крупные белки', 'за сутки её образуется около 180 л', 'в ней есть эритроциты',
                       'глюкоза из неё возвращается в кровь в канальце', 'её около 1,5 л в сутки'),
                  '<b>АВД.</b> Крупные белки и клетки крови задерживаются; 1,5 л — конечная моча.', K))
    T.append(task('9', 'Несколько ответов (2 балла).', 'Какие признаки относятся к грибам?',
                  opts('запасают крахмал', 'клеточная стенка из хитина', 'есть хлоропласты', 'запасают гликоген', 'нет ядра', 'питаются всасыванием'),
                  '<b>БГЕ.</b> Хитин, гликоген, всасывание; хлоропластов нет, ядро есть.', K))
    T.append(task('10', 'Соответствие (2 балла).', 'Учёный — открытие. А) А. Флеминг; Б) М. Мезельсон и Ф. Сталь.',
                  opts('полуконсервативная репликация ДНК', 'пенициллин', 'теория естественного отбора', 'законы наследования') .replace('<li>А)', '<li>1)').replace('<li>Б)', '<li>2)').replace('<li>В)', '<li>3)').replace('<li>Г)', '<li>4)'),
                  '<b>А2 Б1.</b> Флеминг — пенициллин, 1928; Мезельсон и Сталь — полуконсервативная репликация, 1958.', K))
    T.append(task('11', 'Соответствие (2 балла).', 'Фаза митоза — событие. А) метафаза; Б) анафаза.',
                  opts('удвоение ДНК', 'двухроматидные хромосомы выстроены на экваторе', 'сестринские хроматиды расходятся к полюсам', 'вокруг хромосом образуются ядра').replace('<li>А)', '<li>1)').replace('<li>Б)', '<li>2)').replace('<li>В)', '<li>3)').replace('<li>Г)', '<li>4)'),
                  '<b>А2 Б3.</b> Удвоение ДНК — S-период интерфазы, не митоз.', K))
    ctx = ('<div class="frag"><p><b>Контекст к заданиям 12–15.</b> У двух взрослых измерили уровень глюкозы в крови натощак, через 1 и через 2 часа после сладкого завтрака. Данные условные.</p>'
           '<div class="tbl"><table><tr><th>Время</th><th>Человек 1, ммоль/л</th><th>Человек 2, ммоль/л</th></tr>'
           '<tr><td>натощак</td><td class="n">5,0</td><td class="n">5,0</td></tr><tr><td>через 1 час</td><td class="n">7,5</td><td class="n">11,0</td></tr>'
           '<tr><td>через 2 часа</td><td class="n">5,5</td><td class="n">10,0</td></tr></table></div></div>')
    T.append(ctx)
    T.append(task('12', 'Контекст.', 'У кого через 2 часа уровень глюкозы вернулся почти к исходному?', opts('у человека 2', 'у человека 1', 'у обоих', 'ни у кого'), '<b>Б.</b> 5,5 против 5,0 натощак.', K))
    T.append(task('13', 'Контекст.', 'Какой гормон снижает уровень глюкозы в крови?', opts('глюкагон', 'адреналин', 'тироксин', 'инсулин'), '<b>Г.</b> Инсулин.', K))
    T.append(task('14', 'Контекст.', 'Где образуется этот гормон?', opts('в поджелудочной железе', 'в щитовидной железе', 'в надпочечниках', 'в печени'), '<b>А.</b> Поджелудочная железа — железа смешанной секреции.', K))
    T.append(task('15', 'Контекст.', 'Какой вывод можно сделать по этим данным?', opts('у человека 2 сахарный диабет — это доказано', 'у человека 2 через 2 часа глюкоза остаётся высокой; одного измерения для диагноза мало',
                                                                                       'у человека 1 нет инсулина', 'через 3 часа у человека 2 будет 5,0'),
                  '<b>Б.</b> Вывод только в пределах данных: диагноз и продолжение ряда таблица не показывает.', K))
    errs = [
        ('«Насос выкачивает 2 иона натрия, вкачивая 1 ион калия».', '3 Na⁺ наружу, 2 K⁺ внутрь за цикл.', 'Биология 9, § 23, с. 100'),
        ('«Нередуцирующие сахара — полисахариды. Самой распространённой является сахароза».', 'Сахароза — дисахарид: глюкоза + фруктоза.', 'Биология 10 ЕМН, ч. 1, § 4, с. 21'),
        ('«…толстых нитей актина и тонких нитей миозина».', 'Толстые нити — миозин, тонкие — актин.', 'Биология 10 ЕМН, ч. 2, § 111, с. 181'),
        ('Ферменты, как и катализаторы, «существенно сдвигают равновесие в сторону продуктов».', 'Катализатор не смещает равновесие, а ускоряет его достижение.', 'Биология 9, § 11, с. 50–51'),
    ]
    err_html = ''.join(
        f'<div class="task"><div class="q"><b>{16 + i}.</b> <span class="note">Ошибка учебника (3 балла).</span> {q} Что неверно? Как вы скажете это ученику?</div>'
        + (f'<div class="key"><b>Верно:</b> {a} <span class="note">Источник ошибки: {s}.</span> 1 балл — нашёл ошибку, 2 — дал научно верную формулировку и фразу для ученика «в учебнике написано…, верно…».</div>' if K else '')
        + '</div>' for i, (q, a, s) in enumerate(errs))
    T.append(err_html)
    T.append(task('20', 'Ответ ученику (8 баллов).',
                  'Ученик прислал в Telegram: «У мамы II группа, у папы III, оба гетерозиготы. Ребёнок с IV группой — 50 %: у каждого родителя есть один нужный аллель». Напишите ему ответ, как в Telegram: 5–8 предложений. Укажите ошибку, верный ответ и способ проверки.',
                  '', '<b>Верно: 25 %.</b> Iᴬi × Iᴮi: гаметы Iᴬ, i и Iᴮ, i; потомки IᴬIᴮ, Iᴬi, Iᴮi, ii — по 1/4. Причина ошибки: ученик взял вероятность от одного родителя (1/2), а нужно перемножить 1/2 × 1/2. '
                  'Критерии: 3 — верный ответ и решётка или перечень гамет; 3 — названа причина ошибки; 2 — тон нашего стиля: на «ты», коротко, сначала вопрос или подсказка, способ проверки.', K))
    part1 = ('<section id="part1"><div class="sec-head"><h2>Часть 1. Задание по предмету</h2><p>60 минут · 40 баллов</p></div>'
             '<p class="note">Задания 1–6 и 12–15 — по 1 баллу; 7–11 — по 2 балла (несколько ответов: 2 — всё верно, 1 — одна ошибка; соответствие: 2 — обе пары, 1 — одна); 16–19 — по 3 балла; 20 — 8 баллов. Ответы 1–15 — строкой: <code>1В 2Б … 7АБГ … 10: А2 Б1</code> (пример оформления, не ответы).</p>'
             + ''.join(T) + '</section>')
    frag = """
<section id="part2" class="pb"><div class="sec-head"><h2>Часть 2. Проверка фрагмента курса</h2><p>30 минут · 20 баллов</p></div>
<p>Перед вами фрагмент конспекта для учеников. В нём шесть научных ошибок. Выпишите каждую и дайте верную формулировку. Ошибки оформления и стиля не считаются.</p>
<div class="frag">
<p>Митотический цикл включает интерфазу и митоз. В S-периоде интерфазы удваивается число хромосом. В профазе хромосомы спирализуются и становятся хорошо видны. В метафазе двухроматидные хромосомы выстраиваются на экваторе, нити веретена связаны с областью центромер.</p>
<p>В анафазе к полюсам расходятся гомологичные хромосомы. В телофазе вокруг хромосом образуются ядра, затем делится цитоплазма. У лука 2n = 16, поэтому после митоза в каждой дочерней клетке 8 хромосом.</p>
<p>В первом делении мейоза расходятся гомологичные хромосомы, поэтому из клетки 2n получаются клетки с набором n. Кроссинговер — обмен участками несестринских хроматид — происходит в профазе II.</p>
<p>У цветковых при двойном оплодотворении один спермий сливается с яйцеклеткой, второй — с центральной клеткой; так образуется эндосперм с набором 2n. Яйцеклетка человека содержит 23 хромосомы, это набор 2n.</p>
</div>
__KEY2__
</section>
"""
    key2 = ('<div class="key"><b>Ключ.</b> 1) В S-периоде удваивается ДНК, число хромосом не меняется. 2) В анафазе митоза расходятся сестринские хроматиды. '
            '3) После митоза у лука в каждой клетке 16 хромосом — 2n сохраняется. 4) Кроссинговер — в профазе I. 5) Эндосперм — 3n. 6) Яйцеклетка — набор n (23 хромосомы). '
            '<br>Баллы: по 3 за каждую найденную и исправленную ошибку (1 — нашёл, 2 — исправил верно) = 18; ещё 2 — если нет ложных «исправлений» верных фраз.</div>') if K else ''
    lesson = """
<section id="part3"><div class="sec-head"><h2>Пробный урок</h2><p>20 минут в Google Meet</p></div>
<p>Выберите одну тему и подготовьте 20 минут урока. Мы пришлём страницу нашего конспекта по этой теме; свои слайды или доска — по желанию.</p>
<div class="grid2">
  <div class="card"><h3>Тема А. Осмос и плазмолиз</h3><p>Неделя 3: почему вода идёт в клетку или из неё, тургор и плазмолиз в растительной клетке.</p></div>
  <div class="card"><h3>Тема Б. Моногибридное скрещивание</h3><p>Неделя 15: единообразие F₁, расщепление 3 : 1 в F₂, анализирующее скрещивание.</p></div>
</div>
<div class="tbl"><table><tr><th>Минуты</th><th>Что делаете</th></tr>
<tr><td class="n">0–3</td><td>Вопрос группе на повторение: что нужно помнить к этой теме.</td></tr>
<tr><td class="n">3–10</td><td>Объяснение по порядку: почему → алгоритм → разные примеры → ловушка.</td></tr>
<tr><td class="n">10–15</td><td>Одно задание в формате ЕНТ; ученики отвечают, ключ — после попытки.</td></tr>
<tr><td class="n">15–20</td><td>Разбор ошибки одного «ученика» и короткий итог.</td></tr></table></div>
<p class="note">Учеников играем мы; один из нас ответит неверно. Нам важно, как вы найдёте причину ошибки.</p>
</section>
"""
    return part1 + frag.replace('__KEY2__', key2) + lesson


# ---------- только для отбора ----------

RUBRIC = """
<section id="rubric">
  <div class="sec-head"><h2>Как оцениваем</h2><p>этапы 2–5 · 100 баллов</p></div>
  <div class="tbl"><table>
    <tr><th>Этап</th><th>Что смотрим</th><th>Баллы</th></tr>
    <tr><td>Задание по предмету</td><td>Ключ ниже: 1–6, 12–15 — по 1; 7–11 — по 2; ошибки учебников 16–19 — по 3; ответ ученику — 8</td><td class="n">40</td></tr>
    <tr><td>Фрагмент курса</td><td>Шесть ошибок по 3 балла; 2 — без ложных исправлений</td><td class="n">20</td></tr>
    <tr><td>Пробный урок</td><td>Таблица ниже</td><td class="n">30</td></tr>
    <tr><td>Беседа</td><td>Пять вопросов по 2 балла</td><td class="n">10</td></tr>
    <tr class="total"><td>Всего</td><td>Проходной балл — 70, без стоп-факторов</td><td class="n">100</td></tr>
  </table></div>
  <h3>Пробный урок — 30 баллов</h3>
  <div class="tbl"><table>
    <tr><th>Критерий</th><th>Высший балл, если</th><th>Баллы</th></tr>
    <tr><td>Научная точность</td><td>Нет ошибок в фактах и терминах; термины — как в учебниках НЦТ</td><td class="n">8</td></tr>
    <tr><td>Порядок объяснения</td><td>Почему → алгоритм → разные примеры → ловушка; не читает конспект вслух</td><td class="n">6</td></tr>
    <tr><td>Работа с ошибкой</td><td>Не даёт ответ сразу: спрашивает ход, находит причину, ученик исправляет сам</td><td class="n">6</td></tr>
    <tr><td>Формат ЕНТ</td><td>Задание в формате ЕНТ, ключ после попытки, вывод в пределах данных</td><td class="n">4</td></tr>
    <tr><td>Время</td><td>Уложился в 20 минут, этапы по плану</td><td class="n">3</td></tr>
    <tr><td>Онлайн</td><td>Виден экран, хороший звук, обращается к ученикам по именам, держит темп</td><td class="n">3</td></tr>
  </table></div>
  <div class="card"><h3>Какие ошибки играем на пробном уроке</h3><ul class="dots">
    <li>Тема А: «В солёной воде вода входит в клетку, потому что соль притягивает её внутрь». Верно: вода выходит из клетки в более концентрированный раствор — плазмолиз.</li>
    <li>Тема Б: «Аа × Аа даёт 3 : 1 по генотипу». Верно: 3 : 1 по фенотипу, по генотипу 1 : 2 : 1.</li>
  </ul></div>
</section>
"""

INTERVIEW = """
<section id="interview">
  <div class="sec-head"><h2>Беседа о методике</h2><p>5 вопросов · по 2 балла</p></div>
  <div class="tbl"><table>
    <tr><th>Вопрос</th><th>Хороший ответ содержит</th></tr>
    <tr><td>Ученик спрашивает: «Это точно будет на ЕНТ?»</td><td>Не обещает и не придумывает частоту темы: тема есть в спецификации — значит, может быть; учим по учебникам перечня НЦТ.</td></tr>
    <tr><td>В учебнике и в нашем конспекте — разные формулировки. Что сделаете?</td><td>Проверит по учебнику 10–11 класса ЕМН и научному смыслу, сообщит Мансуру; ученику — научно верно и одна фраза «в учебнике написано…».</td></tr>
    <tr><td>Половина группы не сделала ДЗ. Ваши действия?</td><td>Выясняет причину, коротко разбирает общую часть на уроке, не ругает при всех, сообщает Мансуру, если повторяется.</td></tr>
    <tr><td>Родитель спрашивает, поступит ли ребёнок на грант.</td><td>Не обещает; рассказывает о карте пробелов, результатах контроля и пробников, что делать дальше.</td></tr>
    <tr><td>Как вы понимаете, что ученик понял тему?</td><td>Задание без подсказки, объяснение своими словами, ключ после попытки; одна верная буква — ещё не понимание.</td></tr>
  </table></div>
  <p class="note">2 балла — ответ содержит главное из колонки; 1 — частично; 0 — противоречит нашему стилю.</p>
</section>
"""

AFTER = """
<section id="after">
  <div class="sec-head"><h2>После решения</h2><p>первая неделя</p></div>
  <ol class="stages">
    <li><h3>Знакомство с курсом</h3><span class="pts">2–3 часа</span><p>«Начните здесь», программа биологии, неделя 1 целиком: план, презентации, конспект, ДЗ, решения.</p></li>
    <li><h3>Проверка недели заранее</h3><span class="pts">до первого урока</span><p>Замечания — в лист замечаний: файл, страница, что не так, как правильно; «критично» — ошибка в биологии или ключе.</p></li>
    <li><h3>Испытательная неделя</h3><span class="pts">2 урока</span><p>Ведёт уроки по плану; смотрим запись и разбираем вместе по таблице пробного урока.</p></li>
  </ol>
</section>
"""


def page_guide(fonts_html: str) -> str:
    return f"""<title>Приём преподавателя биологии</title>
<meta name="claude:viewport-fit-sides" content="cover">
{fonts_html}
<style>{CSS}</style>
<div class="wrap">
<header>
  <div class="eyebrow">ХимБио просто · найм</div>
  <h1>Приём преподавателя биологии</h1>
  <p class="lead">По этому документу мы отбираем преподавателя: кого ищем, наш стиль, пять этапов, задание с ключом и таблицы баллов. Кандидату отправляем отдельный файл «Задание кандидату» — без ключей.</p>
  <ul class="facts"><li><b>5</b> этапов</li><li><b>100</b> баллов</li><li>проходной — <b>70</b></li><li>пробный урок — <b>20</b> минут</li></ul>
  <nav aria-label="Разделы"><a href="#role">Кого ищем</a><a href="#style">Стиль</a><a href="#stages">Этапы</a><a href="#rubric">Оценка</a><a href="#part1">Задание и ключ</a><a href="#interview">Беседа</a><a href="#after">После решения</a></nav>
</header>
{ROLE}{STYLE}{STAGES}{RUBRIC}{candidate(True)}{INTERVIEW}{AFTER}
<footer>ХимБио просто · 30.10.2026. Задания авторские; факты — по учебникам из перечня НЦТ, ошибки учебников — из нашей таблицы ERRATA. Проходной балл и испытательная неделя — предложение, условия работы заполняет Мансур.</footer>
</div>
"""


def page_candidate(fonts_html: str) -> str:
    return f"""<title>Задание кандидату — биология</title>
{fonts_html}
<style>{CSS}</style>
<div class="wrap">
<header>
  <div class="eyebrow">ХимБио просто · преподаватель биологии</div>
  <h1>Задание кандидату</h1>
  <p class="lead">Спасибо за интерес к работе. Задание займёт около 90 минут: часть 1 — 60 минут, часть 2 — 30. Пользоваться учебниками можно. Ответы пришлите одним сообщением или файлом; после проверки договоримся о пробном уроке.</p>
  <ul class="facts"><li>часть 1 — <b>20</b> заданий</li><li>часть 2 — <b>6</b> ошибок</li><li>пробный урок — <b>20</b> минут</li></ul>
</header>
{STYLE}
{candidate(False)}
<footer>ХимБио просто · онлайн-подготовка к ЕНТ по химии и биологии. Задания авторские, это не задания НЦТ.</footer>
</div>
"""


def pdf(html: str, out: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / 'page.html'
        src.write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"></head><body>' + html + '</body></html>', encoding='utf-8')
        subprocess.run([chrome(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out}', src.as_uri()],
                       check=True, capture_output=True)


def main() -> None:
    out = Path(sys.argv[1])
    google = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Unbounded:wght@700;800&display=swap">')
    out.write_text(page_guide(google), encoding='utf-8')
    local = (f"<style>@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0400-045F; }}"
             f"@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-latin-wght-normal.woff2') format('woff2'); }}"
             f"@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0400-045F; }}"
             f"@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-latin-wght-normal.woff2') format('woff2'); }}</style>")
    OUT.mkdir(parents=True, exist_ok=True)
    pdf(page_guide(local), OUT / 'Приём преподавателя биологии — для отбора.pdf')
    pdf(page_candidate(local), OUT / 'Задание кандидату — биология.pdf')
    print(out, OUT)


if __name__ == '__main__':
    main()
