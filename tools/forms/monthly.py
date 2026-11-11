"""Проверка знаний за месяц (4 недели) в Google Формах → ключ для преподавателя и Apps Script.

    python tools/forms/monthly.py

Пишет course/monthly/README.md и tools/forms/monthly.gs. Код .gs дописывают в проект Apps Script
«ХимБио — стартовый тест (формы)» и запускают createMonthlyChecks: создаёт по форме-тесту на предмет, таблицу ответов
с листом «По неделям» и кладёт всё в папку «4 Проверка знаний за месяц». Уже созданные формы пропускает.
После создания в каждой форме вручную: «Настройки» → «Тест» → «Публикация оценок: сразу после отправки» и три
переключателя показа (как у проверки понимания — Apps Script этого не умеет).

На неделю 5 заданий в формате ЕНТ: 3 с одним ответом (1 балл), соответствие из двух пар (2 вопроса по 1 баллу),
несколько ответов — 3 верных из 6 (2 балла, в Форме только за полностью верный выбор). Итого 7 баллов на неделю.
Задания — по конспектам недель (notes-student.md); не повторяют пробники недель и проверку понимания.
"""
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FOLDER_ID = '1Oz0NHzqXxsS34_CVf1MNLW55MNGjxEjg'  # «ХимБио просто / 4 Проверка знаний за месяц»
DONT_KNOW = 'Не знаю'
SUBJECT = {'chem': 'химия', 'bio': 'биология'}

# Задание: ('one', вопрос, [верный, неверный ×3], объяснение)
#          ('match', вопрос, [A, B], [варианты 1–4], [номер для A, номер для B] (с нуля), объяснение)
#          ('multi', вопрос, [6 вариантов], {номера верных}, объяснение)
MONTHS = {
    1: {
        'weeks': {
            'chem': {1: 'Язык химии', 2: 'Формулы, масса, реакции', 3: 'Классы веществ', 4: 'Моль и газы'},
            'bio': {1: 'Клетка', 2: 'Вещества клетки', 3: 'Мембрана и ферменты', 4: 'АТФ, дыхание, фотосинтез'},
        },
        'chem': {
            1: [
                ('one', 'Что обозначает запись 3Mg²⁺?', ['Три иона магния, заряд каждого +2', 'Один ион магния с зарядом +3', 'Три иона магния, заряд каждого +6', 'Три атома магния в одной молекуле'],
                 'Коэффициент 3 — число частиц, верхний индекс 2+ — заряд одного иона.'),
                ('one', 'Что больше: 0,35 г или 400 мг?', ['400 мг', '0,35 г', 'Они равны', 'Сравнить нельзя'],
                 '0,35 г = 350 мг, а 400 мг > 350 мг. Сравнивать можно только в одних единицах.'),
                ('one', '18 г — это 30 % массы образца. Какова масса образца?', ['60 г', '5,4 г', '54 г', '48 г'],
                 'Целое = часть ÷ (процент ÷ 100) = 18 ÷ 0,3 = 60 г.'),
                ('match', 'Установите соответствие между записью и общим зарядом всех частиц в ней', ['2SO₄²⁻', '3Na⁺'], ['−4', '+3', '−2', '+1'], [0, 1],
                 '2 × (−2) = −4; 3 × (+1) = +3. Заряд одного иона умножаем на число ионов.'),
                ('multi', 'Выберите верные утверждения', ['O₂ — нейтральная молекула из двух атомов', 'O²⁻ — один ион с зарядом −2', 'Индекс показывает число атомов элемента в одной частице',
                                                     'Твёрдый NaCl состоит из молекул NaCl', 'Коэффициент показывает заряд частицы', 'Na — это символы двух элементов: N и a'], {0, 1, 2},
                 'NaCl — решётка из ионов Na⁺ и Cl⁻; коэффициент — число частиц; Na — один символ натрия.'),
            ],
            2: [
                ('one', 'Формула оксида натрия по валентностям Na (I) и O (II)', ['Na₂O', 'NaO', 'NaO₂', 'Na₃O'],
                 'Наименьшее общее число для I и II — 2: индекс Na = 2 ÷ 1 = 2, индекс O = 2 ÷ 2 = 1.'),
                ('one', 'Чему равна Mᵣ(MgCl₂)? Aᵣ(Mg) = 24, Aᵣ(Cl) = 35,5', ['95', '59,5', '95 г', '83'],
                 '24 + 2 × 35,5 = 95. Относительная масса — без единиц; 59,5 получается, если потерять индекс 2.'),
                ('one', 'Массовая доля алюминия в Al₂O₃. Aᵣ(Al) = 27, Aᵣ(O) = 16', ['52,9 %', '47,1 %', '26,5 %', '36,0 %'],
                 'Mᵣ = 2 × 27 + 3 × 16 = 102; ω(Al) = 54 ÷ 102 ≈ 0,529 = 52,9 %. 47,1 % — доля кислорода.'),
                ('match', 'Установите соответствие между формулой и её Mᵣ. Aᵣ(H) = 1, Aᵣ(O) = 16, Aᵣ(Ca) = 40', ['H₂O', 'CaO'], ['18', '56', '20', '44'], [0, 1],
                 'Mᵣ(H₂O) = 2 × 1 + 16 = 18; Mᵣ(CaO) = 40 + 16 = 56.'),
                ('multi', 'Выберите верные утверждения о реакции 2H₂ + O₂ → 2H₂O', ['Это реакция соединения', 'Атомов водорода слева и справа по 4',
                                                                             'В замкнутой системе масса воды равна сумме масс прореагировавших H₂ и O₂', 'Справа два разных вещества',
                                                                             'Коэффициент 2 перед H₂O меняет состав воды', 'Перед O₂ стоит коэффициент 2'], {0, 1, 2},
                 'Справа одно вещество — вода; коэффициент меняет число молекул, а не состав; перед O₂ коэффициент 1.'),
            ],
            3: [
                ('one', 'Какой оксид несолеобразующий?', ['NO', 'SO₃', 'MgO', 'ZnO'],
                 'CO и NO — несолеобразующие. SO₃ — кислотный, MgO — основный, ZnO — амфотерный.'),
                ('one', 'Название вещества Fe(OH)₂', ['Гидроксид железа (II)', 'Гидроксид железа (III)', 'Оксид железа (II)', 'Сульфат железа (II)'],
                 'Группы OH — это гидроксид; римская цифра — валентность железа, здесь II.'),
                ('one', 'Что образуется при нагревании гидроксида меди (II) Cu(OH)₂?', ['CuO и H₂O', 'Cu и H₂O', 'CuO и H₂', 'Cu и O₂'],
                 'Cu(OH)₂ → CuO + H₂O при нагревании: голубой осадок превращается в чёрный CuO.'),
                ('match', 'Установите соответствие между реагентами и признаком реакции', ['BaCl₂ + H₂SO₄', 'Na₂CO₃ + HCl'],
                 ['Выпадает осадок', 'Выделяется газ', 'Раствор становится малиновым', 'Видимых изменений нет'], [0, 1],
                 'BaCl₂ + H₂SO₄ → BaSO₄↓ + 2HCl; Na₂CO₃ + 2HCl → 2NaCl + CO₂↑ + H₂O.'),
                ('multi', 'Какие вещества относятся к основаниям?', ['NaOH', 'Ca(OH)₂', 'Fe(OH)₂', 'HCl', 'Cu(OH)Cl', 'Na₂O'], {0, 1, 2},
                 'Основание — металл и группы OH. HCl — кислота, Cu(OH)Cl — основная соль (есть кислотный остаток), Na₂O — оксид.'),
            ],
            4: [
                ('one', 'Какова масса 2 моль воды? M(H₂O) = 18 г/моль', ['36 г', '18 г', '9 г', '20 г'],
                 'm = n × M = 2 × 18 = 36 г.'),
                ('one', 'Какой объём займут 0,5 моль кислорода при н. у.?', ['11,2 л', '22,4 л', '44,8 л', '16 л'],
                 'V = n × Vₘ = 0,5 × 22,4 = 11,2 л.'),
                ('one', 'Относительная плотность газа по воздуху равна 2. Молярная масса газа', ['58 г/моль', '29 г/моль', '14,5 г/моль', '32 г/моль'],
                 'M = D × M(воздуха) = 2 × 29 = 58 г/моль.'),
                ('match', 'Установите соответствие между порцией вещества и количеством вещества. M(H₂O) = 18 г/моль', ['6,72 л H₂ (н. у.)', '9 г H₂O'], ['0,3 моль', '0,5 моль', '3 моль', '0,2 моль'], [0, 1],
                 'n(H₂) = 6,72 ÷ 22,4 = 0,3 моль; n(H₂O) = 9 ÷ 18 = 0,5 моль. Vₘ — только для газа.'),
                ('multi', 'Выберите верные утверждения', ['В 1 моль вещества содержится Nₐ частиц', 'Молярная масса — масса 1 моль вещества',
                                                     'Объёмы реагирующих газов относятся как небольшие целые числа', 'Относительная плотность газа измеряется в г/л',
                                                     'Коэффициенты уравнения показывают отношение масс веществ', 'Нормальные условия — это температура 25 °C'], {0, 1, 2},
                 'D — отношение без единиц; коэффициенты — отношение моль; н. у. — 0 °C (273 K) и 101,3 кПа.'),
            ],
        },
        'bio': {
            1: [
                ('one', 'Что из перечисленного — орган?', ['Головной мозг', 'Нервная ткань', 'Митохондрия', 'Нервная система'],
                 'Клетка → ткань → орган → система органов → организм. Мозг — орган, митохондрия — структура клетки.'),
                ('one', 'Сколько микрометров в 0,05 мм?', ['50 мкм', '5 мкм', '500 мкм', '0,5 мкм'],
                 '1 мм = 1000 мкм, поэтому 0,05 × 1000 = 50 мкм.'),
                ('one', 'Масштабная линейка соответствует 15 мкм, клетка занимает 2 длины линейки. Какова длина клетки?', ['30 мкм', '15 мкм', '7,5 мкм', '60 мкм'],
                 'Длина = реальная длина линейки × число её длин = 15 × 2 = 30 мкм.'),
                ('match', 'Установите соответствие между клеткой и признаком', ['Бактерия', 'Живая клетка кожи человека'],
                 ['Нет оформленного ядра', 'Есть ядро, нет клеточной стенки и хлоропластов', 'Есть хлоропласты и крупная вакуоль', 'Нет мембраны'], [0, 1],
                 'Бактерия — прокариот без оформленного ядра. Клетка кожи — эукариотическая животная: стенки и хлоропластов нет.'),
                ('multi', 'Какие структуры есть и в клетке мякоти листа, и в клетке кожи человека?', ['Ядро', 'Митохондрии', 'Аппарат Гольджи', 'Хлоропласты', 'Клеточная стенка', 'Крупная центральная вакуоль'], {0, 1, 2},
                 'Хлоропласты, клеточная стенка и крупная центральная вакуоль — признаки растительной клетки.'),
            ],
            2: [
                ('one', 'Какой углевод — полисахарид?', ['Целлюлоза', 'Сахароза', 'Глюкоза', 'Лактоза'],
                 'Целлюлоза, крахмал и гликоген — полисахариды. Сахароза и лактоза — дисахариды, глюкоза — моносахарид.'),
                ('one', 'Какая структура белка состоит из нескольких цепей-субъединиц?', ['Четвертичная', 'Первичная', 'Вторичная', 'Третичная'],
                 'Четвертичная структура — несколько субъединиц; у гемоглобина их четыре. Есть не у всех белков.'),
                ('one', 'Сколько энергии выделяется при полном окислении 1 г жира?', ['Около 39,1 кДж', 'Около 17,6 кДж', 'Около 3,9 кДж', 'Около 391 кДж'],
                 '1 г жира — около 39,1 кДж, почти вдвое больше, чем 1 г углеводов (17,6 кДж).'),
                ('match', 'Установите соответствие между нуклеиновой кислотой и признаком', ['ДНК', 'РНК'],
                 ['Двуцепочечная, сахар — дезоксирибоза', 'Одноцепочечная, есть урацил', 'Мономер — аминокислота', 'Состоит из глицерина и жирных кислот'], [0, 1],
                 'ДНК: две цепи, дезоксирибоза, тимин. РНК: одна цепь, рибоза, урацил.'),
                ('multi', 'Выберите верные утверждения об углеводах', ['Лактоза состоит из глюкозы и галактозы', 'Целлюлоза построена из остатков β-глюкозы', 'Рибоза — пентоза',
                                                                   'Гликоген — запасной углевод растений', 'Сахароза даёт положительную пробу Фелинга', 'Галактоза — дисахарид'], {0, 1, 2},
                 'Гликоген — запас животных и грибов; сахароза даёт отрицательную пробу Фелинга; галактоза — моносахарид.'),
            ],
            3: [
                ('one', 'Как глюкоза поступает в эритроцит?', ['Облегчённой диффузией', 'Активным транспортом', 'Фагоцитозом', 'Осмосом'],
                 'В эритроцит глюкоза идёт облегчённой диффузией: по градиенту, с белком-переносчиком, без затраты энергии.'),
                ('one', 'Какой ион тормозит амилазу слюны в изученном примере?', ['Cu²⁺', 'Na⁺', 'Cl⁻', 'K⁺'],
                 'Na⁺ и Cl⁻ стимулируют амилазу слюны, Cu²⁺ тормозит.'),
                ('one', 'Толщина клеточной мембраны в учебном описании', ['Около 7,5 нм', 'Около 7,5 мкм', 'Около 0,75 мм', 'Около 75 нм'],
                 'Жидкостно-мозаичная модель (Сингер и Николсон, 1972): толщина мембраны около 7,5 нм.'),
                ('match', 'Установите соответствие между ингибитором и тем, как он действует', ['Конкурентный ингибитор', 'Неконкурентный ингибитор'],
                 ['Похож на субстрат и занимает активный центр', 'Связывается вне активного центра и меняет форму фермента', 'Ускоряет реакцию', 'Сам становится продуктом реакции'], [0, 1],
                 'Конкурентный — аналог субстрата в активном центре; неконкурентный связывается вне его и меняет конформацию.'),
                ('multi', 'Какие процессы требуют затраты энергии?', ['Работа Na⁺/K⁺-насоса', 'Эндоцитоз', 'Экзоцитоз', 'Простая диффузия O₂', 'Осмос', 'Облегчённая диффузия'], {0, 1, 2},
                 'Насос, эндоцитоз и экзоцитоз — активные процессы. Диффузия и осмос идут по градиенту без затраты энергии.'),
            ],
            4: [
                ('one', 'Сколько мембран у митохондрии?', ['Две', 'Одна', 'Три', 'Мембран нет'],
                 'Митохондрия имеет две мембраны; внутренняя образует складки — кристы.'),
                ('one', 'Где находятся дыхательная цепь и АТФ-синтетаза?', ['На кристах — складках внутренней мембраны митохондрии', 'В матриксе митохондрии', 'На наружной мембране митохондрии', 'В строме хлоропласта'],
                 'Кристы — складки внутренней мембраны с дыхательной цепью и АТФ-синтетазой; в матриксе — ферменты цикла Кребса.'),
                ('one', 'Энергия гидролиза АТФ, которую берут для учебных расчётов', ['Около 30,6 кДж/моль', 'Около 17,6 кДж/моль', 'Около 306 кДж/моль', 'Около 3,06 кДж/моль'],
                 'АТФ + H₂O → АДФ + H₃PO₄, около 30,6 кДж/моль.'),
                ('match', 'Установите соответствие между процессом и источником энергии', ['Фотосинтез', 'Хемосинтез'],
                 ['Свет', 'Окисление неорганических веществ', 'Гидролиз АТФ пищи', 'Тепло тела животного'], [0, 1],
                 'Фотосинтез использует энергию света, хемосинтез — энергию окисления неорганических веществ (Виноградский).'),
                ('multi', 'Выберите верные утверждения о фотосинтезе', ['Хлоропласт окружён двумя мембранами', 'Граны собраны из тилакоидов', 'Углерод органического вещества берётся из CO₂',
                                                                     'Темновая фаза идёт только ночью', 'Фотосинтез идёт в митохондриях', 'Для фотосинтеза не нужна вода'], {0, 1, 2},
                 'Темновая фаза не использует свет напрямую, но идёт не только ночью; фотосинтез — в хлоропластах; вода нужна, из неё образуется O₂.'),
            ],
        },
    },
}


def lettered(opts, nums=False):
    return [f'{i + 1}) {o}' if nums else f'{"ABCDEF"[i]}) {o}' for i, o in enumerate(opts)]


def build(month: int, subj: str) -> dict:
    data = MONTHS[month][subj]
    rnd = random.Random(f'month-{month}-{subj}')
    ones = [t for w in sorted(data) for t in data[w] if t[0] == 'one']
    pos = [i % 4 for i in range(len(ones))]
    while True:
        rnd.shuffle(pos)
        if all(a != b for a, b in zip(pos, pos[1:])):
            break
    pos = iter(pos)
    multis = iter(rnd.sample(['ACE', 'BDF', 'ADF', 'BCE', 'ABF', 'CDE', 'BEF', 'ACD'], 4))
    items, n = [], 0
    for w in sorted(data):
        assert [t[0] for t in data[w]] == ['one', 'one', 'one', 'match', 'multi'], (subj, w)
        for t in data[w]:
            kind = t[0]
            n += 1
            if kind == 'one':
                _, q, opts, why = t
                assert len(opts) == 4 and len(set(opts)) == 4, q
                k = next(pos)
                wrong = opts[1:]
                rnd.shuffle(wrong)
                o = wrong[:k] + [opts[0]] + wrong[k:]
                items.append(dict(n=n, w=w, kind=kind, q=q, o=lettered(o), a=[lettered(o)[k]], pts=1, why=why))
            elif kind == 'match':
                _, q, left, opts, ans, why = t
                order = list(range(4))
                rnd.shuffle(order)
                o = [opts[i] for i in order]
                a = [order.index(ans[0]), order.index(ans[1])]
                assert a[0] != a[1]
                items.append(dict(n=n, w=w, kind=kind, q=q, left=left, o=lettered(o, True), a=[lettered(o, True)[x] for x in a], pts=2, why=why))
            else:
                _, q, opts, right, why = t
                assert len(opts) == 6 and len(right) == 3 and all(',' not in x for x in opts), q
                slots = [ 'ABCDEF'.index(x) for x in next(multis)]  # места верных: свой набор букв у каждого задания
                good = [opts[i] for i in sorted(right)]
                bad = [opts[i] for i in range(6) if i not in right]
                rnd.shuffle(good)
                rnd.shuffle(bad)
                o = [good.pop() if i in slots else bad.pop() for i in range(6)]
                a = [lettered(o)[i] for i in slots]
                items.append(dict(n=n, w=w, kind=kind, q=q, o=lettered(o), a=a, pts=2, why=why))
    return dict(month=month, subject=subj, subjectName=SUBJECT[subj].capitalize(),
                weeks={str(k): v for k, v in MONTHS[month]['weeks'][subj].items()}, items=items)


def gs_form(c: dict) -> dict:
    wk = sorted(int(x) for x in c['weeks'])
    title = f"ХимБио просто — проверка знаний за месяц {c['month']}: {SUBJECT[c['subject']]}, недели {wk[0]}–{wk[-1]}"
    intro = (f"Проверка знаний за месяц {c['month']}: недели {wk[0]}–{wk[-1]}. Это не оценка: так видно, какую неделю стоит повторить.\n\n"
             f"• {len(c['items'])} заданий, около 40 минут, как на ЕНТ: с одним ответом, на соответствие и с несколькими ответами.\n"
             '• Можно таблицу Менделеева, таблицу растворимости и калькулятор. Конспект и подсказки — нельзя.\n'
             '• Не знаешь — выбери «Не знаю». Угаданный ответ спрячет тему, которую нужно повторить.\n'
             '• После отправки нажми «Посмотреть баллы»: там ошибки, верные ответы и объяснения.')
    qs = []
    for it in c['items']:
        base = f"{it['n']}. {it['q']}"
        if it['kind'] == 'one':
            qs.append(dict(w=it['w'], type='one', title=base, o=it['o'] + [DONT_KNOW], a=it['a'][0], pts=1, why=it['why']))
        elif it['kind'] == 'match':
            for j, side in enumerate('AB'):
                qs.append(dict(w=it['w'], type='one', title=f"{base} — {side}) {it['left'][j]}", o=it['o'] + [DONT_KNOW], a=it['a'][j], pts=1, why=it['why']))
        else:
            qs.append(dict(w=it['w'], type='multi', title=base, help='Выбери три верных ответа.', o=it['o'], a=it['a'], pts=2, why=it['why']))
    return dict(title=title, intro=intro, weeks=c['weeks'], questions=qs)


def teacher_md(checks: list) -> str:
    L = ['# Проверка знаний за месяц — Google Формы\n',
         '**Черновик, ждёт проверки преподавателя.** Задания авторские, по конспектам недель курса (учебники НЦТ). Это не задания НЦТ. '
         'Пробники недель и проверку понимания не повторяют.\n',
         '## Как проводить\n',
         '- **Когда:** в конце каждой четвёртой недели, около 40 минут. Ссылку на форму преподаватель кидает в чат группы.',
         '- **Что внутри:** по 5 заданий на неделю в формате ЕНТ: 3 с одним ответом (1 балл), соответствие из двух пар (по 1 баллу за пару), '
         'несколько ответов — 3 верных из 6 (2 балла; в Форме только за полностью верный выбор). 7 баллов на неделю, 28 за месяц.',
         '- **Что видит ученик:** после отправки — баллы, ошибки, верные ответы и объяснения.',
         '- **Что видит преподаватель:** в таблице ответов лист «По неделям»: баллы каждого ученика по каждой неделе '
         '(зелёный 6–7, жёлтый 4–5, красный 0–3). Неделю, где у группы много красного, повторяем.\n',
         '## Где лежит\n',
         'Папка «4 Проверка знаний за месяц» в «ХимБио просто» на Google Диске. Генератор — `tools/forms/monthly.py` → `monthly.gs`, '
         'функция `createMonthlyChecks` в проекте Apps Script «ХимБио — стартовый тест (формы)».\n',
         '## Ссылки\n', '<!-- links -->', '_Появятся после создания форм._', '<!-- /links -->\n', '## Ключи\n']
    for c in checks:
        wk = sorted(int(x) for x in c['weeks'])
        L += [f"### {c['subjectName']}, месяц {c['month']} (недели {wk[0]}–{wk[-1]})\n", '| № | Неделя | Задание | Варианты | Ответ |', '|---|---|---|---|---|']
        for it in c['items']:
            q = it['q'] + (f" (A — {it['left'][0]}; B — {it['left'][1]})" if it['kind'] == 'match' else '')
            ans = ('A — ' + it['a'][0] + '; B — ' + it['a'][1]) if it['kind'] == 'match' else ', '.join(it['a'])
            L.append(f"| {it['n']} | {it['w']} | {q} | {' · '.join(it['o'])} | **{ans}** |")
        L.append('')
    return '\n'.join(L)


GS = r'''/**
 * ХимБио просто — проверка знаний за месяц (химия, биология). Сгенерировано tools/forms/monthly.py — правки вносить там.
 * Запуск: функция createMonthlyChecks → «Выполнить». Формы-тесты, таблицы ответов с листом «По неделям», папка «4 Проверка знаний за месяц».
 * Уже созданные формы (то же название в папке) пропускает. Ссылки — в журнале выполнения.
 */
const MON_FOLDER_ID = '__FOLDER__';
const MON_NAME_Q = 'Имя и фамилия';
const MON_ROWS = 301;
const MON_FORMS = __FORMS__;

function createMonthlyChecks() {
  const folder = DriveApp.getFolderById(MON_FOLDER_ID);
  const out = ['Папка: ' + folder.getUrl()];
  MON_FORMS.forEach(f => out.push(monBuild_(f, folder)));
  Logger.log(out.join('\n'));
}

function monBuild_(f, folder) {
  const old = folder.getFilesByName(f.title);
  if (old.hasNext()) return 'есть: ' + f.title + ' — ' + FormApp.openById(old.next().getId()).getPublishedUrl();
  const form = FormApp.create(f.title);
  form.setDescription(f.intro).setIsQuiz(true).setProgressBar(true).setAllowResponseEdits(false)
    .setPublishingSummary(false).setShowLinkToRespondAgain(false)
    .setConfirmationMessage('Спасибо! Нажми «Посмотреть баллы»: там ошибки, верные ответы и объяснения.');
  form.addTextItem().setTitle(MON_NAME_Q).setRequired(true);
  let week = null;
  f.questions.forEach(q => {
    if (q.w !== week) { week = q.w; form.addPageBreakItem().setTitle('Неделя ' + week + ': ' + f.weeks[String(week)]); }
    const it = q.type === 'multi' ? form.addCheckboxItem() : form.addMultipleChoiceItem();
    it.setTitle(q.title).setPoints(q.pts).setRequired(q.type !== 'multi');
    if (q.help) it.setHelpText(q.help);
    it.setChoices(q.o.map(o => it.createChoice(o, q.type === 'multi' ? q.a.indexOf(o) >= 0 : o === q.a)));
    const ans = q.type === 'multi' ? q.a.join(', ') : q.a;
    it.setFeedbackForCorrect(FormApp.createFeedback().setText('Верно. ' + q.why).build());
    it.setFeedbackForIncorrect(FormApp.createFeedback().setText('Верный ответ: ' + ans + '. ' + q.why).build());
  });
  const ss = SpreadsheetApp.create(f.title + ' — ответы');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  let resp = null;
  for (let i = 0; i < 20 && !resp; i++) {
    SpreadsheetApp.flush();
    resp = SpreadsheetApp.openById(ss.getId()).getSheets().filter(s => s.getFormUrl())[0] || null;
    if (!resp) Utilities.sleep(1000);
  }
  if (resp) monSummary_(SpreadsheetApp.openById(ss.getId()), resp, f);
  DriveApp.getFileById(form.getId()).moveTo(folder);
  DriveApp.getFileById(ss.getId()).moveTo(folder);
  return f.title + ': ' + form.getPublishedUrl() + ' | редактирование — ' + form.getEditUrl() + ' | таблица — ' + ss.getUrl();
}

function monSummary_(ss, resp, f) {
  ss.setSpreadsheetLocale('en_US');  // формулы с запятыми
  SpreadsheetApp.flush();
  const lastCol = resp.getRange(1, resp.getMaxColumns()).getA1Notation().replace(/\d+/g, '');
  const sh = ss.getSheets().filter(s => !s.getFormUrl())[0] || ss.insertSheet();
  sh.setName('По неделям');
  ss.setActiveSheet(sh);
  ss.moveActiveSheet(1);
  const R = "'" + resp.getName().replace(/'/g, "''") + "'!";
  const esc = s => String(s).replace(/"/g, '""');
  const range = 'INDIRECT("' + esc(R + 'A2:' + lastCol + MON_ROWS) + '")';
  const col = title => 'INDEX(' + range + ',0,MATCH("' + esc(title) + '",' + R + '1:1,0))';
  const name = col(MON_NAME_Q);
  const hit = q => '(' + col(q.title) + '="' + esc(q.type === 'multi' ? q.a.join(', ') : q.a) + '")*' + q.pts;
  const weeks = Object.keys(f.weeks).map(Number).sort((a, b) => a - b);
  const max = f.questions.reduce((s, q) => s + q.pts, 0);
  const head = ['Ученик', 'Всего из ' + max].concat(weeks.map(w => 'Н' + w + ' ' + f.weeks[String(w)] + ' (из ' + f.questions.filter(q => q.w === w).reduce((s, q) => s + q.pts, 0) + ')'));
  sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight('bold').setWrap(true).setVerticalAlignment('top');
  sh.getRange(2, 1).setValue('Средний балл группы');
  sh.getRange(3, 1).setFormula('=ARRAYFORMULA(IFERROR(IF(' + name + '="",,' + name + '),))');
  sh.getRange(3, 2).setFormula('=ARRAYFORMULA(IFERROR(IF(' + name + '="",,' + f.questions.map(hit).join('+') + '),))');
  sh.getRange(2, 2).setFormula('=IFERROR(ROUND(AVERAGE(B3:B),1),)');
  weeks.forEach((w, i) => {
    const c = 3 + i;
    const L = sh.getRange(1, c).getA1Notation().replace(/\d+/g, '');
    sh.getRange(3, c).setFormula('=ARRAYFORMULA(IFERROR(IF(' + name + '="",,' + f.questions.filter(q => q.w === w).map(hit).join('+') + '),))');
    sh.getRange(2, c).setFormula('=IFERROR(ROUND(AVERAGE(' + L + '3:' + L + '),1),)');
  });
  const data = sh.getRange(3, 3, MON_ROWS, weeks.length);
  const rule = (expr, color) => SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=AND(ISNUMBER(C3),' + expr + ')').setBackground(color).setRanges([data]).build();
  sh.setConditionalFormatRules([rule('C3>=6', '#c8e6c9'), rule('AND(C3>=4,C3<6)', '#fff3c4'), rule('C3<4', '#f8c9c4')]);
  sh.setFrozenRows(2);
  sh.setFrozenColumns(2);
  sh.setColumnWidth(1, 200);
  sh.setColumnWidths(3, weeks.length, 120);
  sh.setRowHeight(1, 60);
  sh.getRange(1, 1, 2, 2 + weeks.length).setBackground('#eef3ff');
  sh.getRange(1, 4 + weeks.length).setValue('Неделя: 6–7 — знает (зелёный), 4–5 — повторить (жёлтый), 0–3 — с нуля (красный). «Не знаю» = 0.');
}
'''


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = [build(1, 'chem'), build(1, 'bio')]
    forms = [gs_form(c) for c in checks]
    (ROOT / 'tools/forms/monthly.gs').write_text(
        GS.replace('__FOLDER__', FOLDER_ID).replace('__FORMS__', json.dumps(forms, ensure_ascii=False, indent=1)), encoding='utf-8')
    out = ROOT / 'course/monthly/README.md'
    out.parent.mkdir(exist_ok=True)
    md = teacher_md(checks)
    if out.exists():
        old = out.read_text(encoding='utf-8')
        a, b = old.find('<!-- links -->'), old.find('<!-- /links -->')
        if a >= 0 and b > a:
            md = md[:md.find('<!-- links -->')] + old[a:b] + md[md.find('<!-- /links -->'):]
    out.write_text(md + '\n', encoding='utf-8')
    for c, f in zip(checks, forms):
        print(c['subject'], len(c['items']), 'заданий,', len(f['questions']), 'вопросов формы,', sum(q['pts'] for q in f['questions']), 'баллов;',
              'буквы одиночных:', ''.join(it['a'][0][0] for it in c['items'] if it['kind'] == 'one'))


if __name__ == '__main__':
    main()
