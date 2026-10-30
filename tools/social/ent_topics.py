"""Страница и PDF «Темы ЕНТ по учебникам»: темы спецификации НЦТ по химии (19) и биологии (12) → учебник, §, страницы → неделя курса.

Данные — по course/textbooks/INDEX.md и заголовкам выжимок course/textbooks/*.md (номера страниц печатные).
Запуск: .venv/Scripts/python.exe -I tools/social/ent_topics.py <html_out>
PDF кладётся в «00 Материалы ХимБио просто/Продажи/».
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools' / 'handout')]
from handout import chrome  # noqa: E402

PDF = ROOT / '00 Материалы ХимБио просто' / 'Продажи' / 'Темы ЕНТ по учебникам.pdf'
FONTS = (ROOT / 'content/brand/fonts').as_uri()

CHEM = [
    ('01', 'Состав и строение атома; химическая связь и структура вещества',
     'Протоны, нейтроны, изотопы, радиоактивность, электронные формулы; электроотрицательность, виды связи, гибридизация, кристаллические решётки.',
     ['Х7 § 5–7 · с. 40–51', 'Х8 § 1–3, 30, 35–39 · с. 4–13, 109–111, 126–136', 'Х10-1 § 1–6, 10–18 · с. 5–44, 60–91'], '1, 6, 7'),
    ('02', 'Периодический закон и периодическая система',
     'Закон Менделеева, строение таблицы, как меняются радиус, металлические свойства и электроотрицательность по периоду и группе.',
     ['Х8 § 30–34 · с. 109–125', 'Х10-1 § 7–9 · с. 45–59'], '6'),
    ('03', 'ОВР; электролиз',
     'Степень окисления, электронный баланс, окислители и восстановители, полуреакции; ряд напряжений, гальванический элемент, электролиз расплавов и растворов.',
     ['Х9-1 § 19–20 · с. 72–80', 'Х10-1 § 43–51 · с. 178–211'], '9, 10, 23'),
    ('04', 'Кинетика; химическое равновесие',
     'Тепловой эффект и закон Гесса; скорость, закон действующих масс, правило Вант-Гоффа, катализ; константа равновесия, принцип Ле Шателье.',
     ['Х8 § 22–23 · с. 80–85', 'Х9-1 § 14–18 · с. 59–71', 'Х10-1 § 28–42 · с. 116–177'], '11, 12'),
    ('05', 'Ионные равновесия в растворах электролитов; гидролиз солей',
     'Электролиты и степень диссоциации, ионные уравнения, pH и индикаторы, гидролиз, качественные реакции на ионы.',
     ['Х9-1 § 1–12 · с. 4–53', 'Х11-2 § 53–57 · с. 53–72'], '8'),
    ('06', 'Общая характеристика металлов и неметаллов; производство металлов',
     'Физические и химические свойства металлов, ряд активности, способы получения, сплавы, коррозия.',
     ['Х8 § 14 · с. 49–51', 'Х9-1 § 21–23 · с. 81–97', 'Х11-2 § 58 · с. 73–75'], '13–16'),
    ('07', 'Элементы 1, 2 и 13 групп и их соединения',
     'Щелочные и щёлочноземельные металлы, кальций, жёсткость воды; алюминий, амфотерные оксид и гидроксид.',
     ['Х8 § 55 · с. 200–201', 'Х9-1 § 25–27 · с. 100–117', 'Х10-2 § 57–59 · с. 28–38', 'Х11-2 § 68 · с. 113'], '13, 14'),
    ('08', 'Элементы 14 группы и их соединения',
     'Углерод: аллотропия, оксиды, угольная кислота, карбонаты, CO₂ со щёлочью; кремний, SiO₂, силикаты.',
     ['Х8 § 51–53 · с. 180–195', 'Х9-2 § 43–45 · с. 56–65', 'Х11-1 § 37–41 · с. 155–178'], '15'),
    ('09', 'Элементы 15 группы и их соединения',
     'Азот, аммиак и его синтез, соли аммония, азотная кислота и нитраты; фосфор, фосфорная кислота, удобрения.',
     ['Х9-2 § 36–42 · с. 31–56', 'Х11-2 § 42–46 · с. 5–24'], '15'),
    ('10', 'Элементы 16 группы; контактное производство серной кислоты',
     'Кислород и озон, сера, H₂S, SO₂, серная кислота; обжиг пирита, контактный аппарат, олеум.',
     ['Х8 § 29 · с. 104–106', 'Х9-2 § 31–34 · с. 16–29', 'Х11-2 § 47–51 · с. 24–44'], '16'),
    ('11', 'Элементы 17 группы и их соединения',
     'Галогены и их активность, хлор, хлороводород и соляная кислота, хлориды, распознавание галогенид-ионов.',
     ['Х9-1 § 12 · с. 50–52', 'Х9-2 § 28–30 · с. 3–15', 'Х10-2 § 54–55 · с. 15–21'], '16'),
    ('12', 'Переходные элементы; комплексные соединения',
     'Хром, марганец, железо, медь, цинк; комплексные соединения; чугун и сталь, биологическая роль металлов.',
     ['Х11-2 § 60–61 · с. 80–88', 'Х11-2 § 67–69 · с. 108–117'], '14'),
    ('13', 'Углеводороды',
     'Классификация, гомологи, номенклатура, изомерия; алканы, циклоалканы, алкены, алкадиены, алкины, арены.',
     ['Х9-2 § 49–59 · с. 86–138', 'Х10-2 § 60–77 · с. 41–120', 'Х11-1 § 1–3 · с. 5–16'], '17, 18'),
    ('14', 'Кислородсодержащие органические соединения',
     'Спирты, фенол, альдегиды и кетоны, карбоновые кислоты, сложные эфиры, жиры, мыла.',
     ['Х9-2 § 63–66 · с. 151–163', 'Х10-2 § 83–90 · с. 145–178', 'Х11-1 § 6–13 · с. 27–55'], '19, 20'),
    ('15', 'Углеводы',
     'Глюкоза и фруктоза, сахароза, крахмал и целлюлоза; гидролиз и брожение.',
     ['Х9-2 § 67 · с. 164–167', 'Х11-1 § 18–22 · с. 74–86'], '21'),
    ('16', 'Азотсодержащие органические соединения',
     'Амины и анилин, аминокислоты, белки и цветные реакции, ферменты.',
     ['Х9-2 § 68 · с. 169–171', 'Х11-1 § 14–17 · с. 61–70', 'Х11-1 § 23–25 · с. 86–98'], '21'),
    ('17', 'Синтетические полимеры; новые материалы; нефть',
     'Полимеризация и поликонденсация, пластмассы, каучуки и резина, волокна; природный газ, нефть, перегонка и крекинг.',
     ['Х9-2 § 60–62 · с. 138–150', 'Х10-2 § 74–75, 78–82 · с. 102–110, 121–143', 'Х11-1 § 30–33 · с. 120–134'], '18, 22'),
    ('18', 'Расчёты: закон действующих масс, выход, смеси, олеум, электролиз',
     'Моль и газовый объём, доли и растворы, избыток, выход по стадиям, смеси (система уравнений), олеум, расчёты по электролизу и кинетике.',
     ['Х8 § 15–19, 40–41 · с. 54–71, 137–146', 'Х9-1 § 13, 24 · с. 53–55, 97–99', 'Х10-1 § 20–27 · с. 95–115',
      'Х11-1 § 39 · с. 163–164', 'Х11-2 § 49–50 · с. 32–36'], '4, 5, 10–12, 16, 23'),
    ('19', 'Формула по продуктам сгорания',
     'Вывод молекулярной формулы по массам CO₂ и H₂O и плотности паров; функциональные группы и распознавание.',
     ['Х10-2 § 60–69 · с. 41–82', 'Х11-1 § 34–35 · с. 139–147'], '17, 22, 23'),
]

BIO = [
    ('01', 'Разнообразие, биосфера, экосистема, популяция; влияние человека',
     'Систематика и таксоны, царства, отделы растений, типы животных; цепи и пирамиды, правило 10 %, популяции, факторы, взаимоотношения, круговороты, Харди — Вайнберг, экологические проблемы Казахстана.',
     ['Б7м § 9–12 · с. 38–56', 'Б7а § 8–10 · с. 36–48', 'Б8 § 6–9, 54–60 · с. 24–40, 212–239', 'Б9 § 3–9 · с. 12–45',
      'Б11-2 § 57–68, 70 · с. 111–172, 176–180'], '18, 20'),
    ('02', 'Питание',
     'Углеводы, липиды, белки как вещества пищи; фотосинтез и хемосинтез; типы питания, пищеварение, ферменты, витамины.',
     ['Б7а § 15, 23 · с. 61–63, 89–91', 'Б8 § 7, 10–15 · с. 28–29, 41–65', 'Б9 § 10, 12 · с. 46–49, 54–57', 'Б11-1 § 6–13 · с. 34–78'], '2, 4, 5'),
    ('03', 'Транспорт веществ',
     'Мембрана, диффузия, осмос, активный транспорт; ксилема и флоэма; кровь, иммунитет, группы крови, сердце и круги кровообращения, гемоглобин.',
     ['Б7а § 20 · с. 77–80', 'Б8 § 16–24 · с. 66–102', 'Б9 § 13–15', 'Б10-1 § 20, 26–27, 32–39', 'Б11-1 § 14–19 · с. 80–105'], '3, 6'),
    ('04', 'Дыхание',
     'АТФ, три этапа энергетического обмена, брожение, утомление мышц; газообмен у растений и животных, дыхательная система человека и её регуляция.',
     ['Б7а § 25–28 · с. 96–110', 'Б8 § 25–27 · с. 103–112', 'Б9 § 16–17 · с. 73–79', 'Б10-1 § 40–45', 'Б11-1 § 22 · с. 114–117'], '4, 7'),
    ('05', 'Выделение',
     'Органы выделения, нефрон: фильтрация, реабсорбция, секреция; АДГ и водный баланс, кожа, гемодиализ.',
     ['Б8 § 28–30 · с. 113–123', 'Б9 § 18–21 · с. 80–95', 'Б10-1 § 50–60 · с. 202–236'], '8, 11'),
    ('06', 'Движение. Биофизика',
     'Скелет, строение кости, соединения костей, мышцы, саркомер и скользящие нити; потенциал покоя и действия.',
     ['Б8 § 31–37 · с. 124–149', 'Б9 § 23 · с. 100–102', 'Б10-2 § 100–101 · с. 138–145', 'Б10-2 § 111–117 · с. 180–206'], '9, 10'),
    ('07', 'Координация и регуляция',
     'Нервная система, нейрон и синапс, рефлекс и рефлекторная дуга, органы чувств; железы и гормоны, гомеостаз, терморегуляция; фитогормоны.',
     ['Б7а § 32, 35–43', 'Б7м § 39–40 · с. 160–179', 'Б8 § 38–44 · с. 150–175', 'Б9 § 22–25, 27–28 · с. 96–123', 'Б10-2 § 102–110 · с. 148–179', 'Б11-1 § 21–26 · с. 111–139'], '10, 11'),
    ('08', 'Размножение. Рост и развитие',
     'Гаметогенез, бесполое и половое размножение, вегетативное размножение, двойное оплодотворение, жизненные циклы растений, онтогенез.',
     ['Б7а § 52–59 · с. 194–216', 'Б8 § 46–49 · с. 180–196', 'Б10-2 § 62–63 · с. 9–16', 'Б11-1 § 27–31 · с. 140–158'], '12, 13'),
    ('09', 'Клеточный цикл. Клеточная биология',
     'Строение клетки и органоиды, мембрана, хромосомы, клеточный цикл, митоз и мейоз, счёт хромосом и ДНК.',
     ['Б9 § 30–32 · с. 132–145', 'Б10-1 § 1, 18–30 · с. 5–10, 79–138', 'Б10-2 с. 4–13'], '1, 3, 12'),
    ('10', 'Наследственность и изменчивость; селекция; эволюция',
     'Законы Менделя, генетика пола, сцепление, группы крови, взаимодействие генов; изменчивость, мутации, селекция; эволюционные учения, отбор, видообразование, доказательства эволюции.',
     ['Б9 § 33–39, 41 · с. 145–171, 177–182', 'Б9 § 53–61 · с. 229–262', 'Б10-2 § 67–99 · с. 30–136', 'Б11-1 § 32–33 · с. 159–170'], '15–17, 19'),
    ('11', 'Молекулярная биология и биохимия',
     'Вода и минеральные вещества, углеводы, липиды, белки, ферменты, нуклеиновые кислоты; репликация, генетический код, транскрипция, трансляция.',
     ['Б8 § 3–5 · с. 15–23', 'Б9 § 11, 29', 'Б10-1 § 2–17 · с. 11–78', 'Б11-1 § 2–5 · с. 11–32'], '1–4, 14'),
    ('12', 'Микробиология и биотехнология; биомедицина и биоинформатика',
     'Бактерии и вирусы, инфекции, антибиотики, микробиологические методы, генная инженерия, клонирование; микроскопы, ПЦР, эпигенетика, ЭКО, моноклональные антитела, диализ.',
     ['Б7а § 60–63 · с. 219–230', 'Б7м § 63–66 · с. 240–253', 'Б10-2 § 122–124 · с. 220–230', 'Б11-2 § 35–56 · с. 4–110'], '21, 22'),
]

BOOKS_CHEM = [('Х7', 'Химия, 7 класс', 'Оспанова, Аухадиева, Белоусова; Мектеп'),
              ('Х8', 'Химия, 8 класс', 'те же авторы; Мектеп, 2018'),
              ('Х9-1, Х9-2', 'Химия, 9 класс, ч. 1–2', 'те же авторы; Мектеп, 2019'),
              ('Х10-1, Х10-2', 'Химия, 10 класс ЕМН, ч. 1–2', 'те же авторы; Мектеп, 2019'),
              ('Х11-1, Х11-2', 'Химия, 11 класс ЕМН, ч. 1–2', 'те же авторы; Мектеп')]
BOOKS_BIO = [('Б7м', 'Биология, 7 класс', 'Очкур, Курмангалиева; Мектеп, 2017'),
             ('Б7а', 'Биология, 7 класс', 'Соловьева, Ибраимова, Алина; Атамұра, 2017'),
             ('Б8', 'Биология, 8 класс', 'Соловьева, Ибраимова; Атамұра, 2018'),
             ('Б9', 'Биология, 9 класс', 'Асанов, Соловьева, Ибраимова; Атамұра, 2019'),
             ('Б10-1, Б10-2', 'Биология, 10 класс ЕМН, ч. 1–2', 'Очкур, Курмангалиева, Нуртаева; Мектеп, 2019'),
             ('Б11-1, Б11-2', 'Биология, 11 класс ЕМН, ч. 1–2', 'Абылайханова, Қалыбаева, Пәрімбекова; Мектеп')]

CSS = """
/* Каталог: шапка, две секции тем (химия — красный, биология — зелёный), справочник учебников. */
:root {
  --bg: #F5F2EB; --card: #FFFFFF; --ink: #151515; --muted: #615C53; --line: #DCD5C7;
  --chem: #C8232C; --bio: #1F7A4A; --chem-soft: #FBE4E4; --bio-soft: #DDEFE4;
  --display: 'Unbounded', 'Arial Black', sans-serif; --body: 'Manrope', 'Segoe UI', Arial, sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #131312; --card: #1C1B19; --ink: #F1EDE4; --muted: #A8A296; --line: #2F2D29;
  --chem: #FF6B70; --bio: #5CC08A; --chem-soft: #3A1D1F; --bio-soft: #16301F; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #131312; --card: #1C1B19; --ink: #F1EDE4; --muted: #A8A296; --line: #2F2D29;
  --chem: #FF6B70; --bio: #5CC08A; --chem-soft: #3A1D1F; --bio-soft: #16301F; color-scheme: dark }
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font: 500 16px/1.55 var(--body); margin: 0; }
.wrap { max-width: 1080px; margin: 0 auto; padding-block: 40px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 48px; }
header { display: flex; flex-direction: column; gap: 14px; }
.eyebrow { font: 800 12px/1 var(--body); letter-spacing: .16em; text-transform: uppercase; color: var(--muted); }
h1 { font: 800 clamp(28px, 5vw, 46px)/1.08 var(--display); margin: 0; text-wrap: balance; letter-spacing: -.01em; }
.lead { font-size: 18px; max-width: 64ch; margin: 0; color: var(--muted); }
.facts { display: flex; flex-wrap: wrap; gap: 10px; margin: 6px 0 0; padding: 0; list-style: none; }
.facts li { border: 1.5px solid var(--line); border-radius: 999px; padding: 6px 14px; font-weight: 700; font-size: 14px; }
.facts b { font-family: var(--display); font-weight: 700; }
nav { display: flex; flex-wrap: wrap; gap: 8px 20px; font-weight: 800; font-size: 14px; }
nav a { color: var(--ink); text-decoration: none; border-bottom: 2px solid var(--line); padding-bottom: 2px; }
nav a:hover, nav a:focus-visible { border-color: var(--ink); outline: none; }
section { display: flex; flex-direction: column; gap: 16px; }
.sec-head { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  border-bottom: 3px solid var(--accent); padding-bottom: 10px; }
h2 { font: 800 clamp(22px, 3.4vw, 30px)/1.1 var(--display); margin: 0; color: var(--accent); }
.sec-head p { margin: 0; color: var(--muted); font-weight: 600; font-size: 14px; }
.chem { --accent: var(--chem); --soft: var(--chem-soft); } .bio { --accent: var(--bio); --soft: var(--bio-soft); }
.topics { display: flex; flex-direction: column; gap: 10px; }
.topic { display: grid; grid-template-columns: 64px minmax(0, 1fr) 120px; gap: 6px 18px; background: var(--card);
  border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; break-inside: avoid; }
.num { font: 800 26px/1 var(--display); color: var(--accent); font-variant-numeric: tabular-nums; padding-top: 2px; }
.body { min-width: 0; display: flex; flex-direction: column; gap: 6px; }
h3 { font: 800 17px/1.3 var(--body); margin: 0; text-wrap: balance; }
.what { margin: 0; color: var(--muted); font-size: 15px; max-width: 68ch; }
.refs { display: flex; flex-wrap: wrap; gap: 6px; margin: 4px 0 0; padding: 0; list-style: none; }
.refs li { background: var(--soft); border-radius: 6px; padding: 3px 9px; font-size: 14px; font-weight: 600; font-variant-numeric: tabular-nums; }
.refs b { font-weight: 800; color: var(--accent); }
.week { text-align: right; font-size: 12px; color: var(--muted); font-weight: 700; text-transform: uppercase; letter-spacing: .06em; }
.week b { display: block; margin-top: 4px; font: 700 15px/1.3 var(--body); text-transform: none; letter-spacing: 0; color: var(--ink); }
.books { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 16px; }
.books > div { min-width: 0; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; }
.books h3 { margin-bottom: 8px; color: var(--accent); }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
td { padding: 7px 0; border-top: 1px solid var(--line); vertical-align: top; }
td:first-child { font-weight: 800; white-space: nowrap; padding-right: 14px; }
td span { display: block; color: var(--muted); font-size: 13px; }
.how { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr)); gap: 16px; margin: 0; padding: 0; list-style: none; counter-reset: s; }
.how li { counter-increment: s; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; font-size: 15px; }
.how li::before { content: counter(s); display: block; font: 800 22px/1 var(--display); margin-bottom: 8px; color: var(--muted); }
footer { color: var(--muted); font-size: 13px; border-top: 1px solid var(--line); padding-top: 16px; }
@media (max-width: 640px) {
  .topic { grid-template-columns: 44px minmax(0, 1fr); }
  .num { font-size: 20px; }
  .week { grid-column: 2; text-align: left; }
  .week b { display: inline; margin: 0 0 0 6px; }
}
@media print {
  @page { size: A4; margin: 14mm 12mm; }
  body { background: #fff; font-size: 12px; }
  .wrap { padding: 0; gap: 22px; max-width: none; }
  nav { display: none; }
  .topic { padding: 10px 12px; grid-template-columns: 44px minmax(0, 1fr) 96px; }
  h3 { font-size: 14px; } .what, .refs li { font-size: 12px; }
  section { break-before: page; } section:first-of-type { break-before: auto; }
}
"""


def topic_rows(items: list) -> str:
    out = []
    for num, title, what, refs, weeks in items:
        chips = ''.join(f'<li><b>{escape(r.split(" ", 1)[0])}</b> {escape(r.split(" ", 1)[1])}</li>' for r in refs)
        out.append(f'<article class="topic"><div class="num">{num}</div><div class="body"><h3>{escape(title)}</h3>'
                   f'<p class="what">{escape(what)}</p><ul class="refs">{chips}</ul></div>'
                   f'<div class="week">недели курса<b>{weeks}</b></div></article>')
    return '\n'.join(out)


def books(rows: list) -> str:
    return '<table>' + ''.join(f'<tr><td>{escape(a)}</td><td>{escape(b)}<span>{escape(c)}</span></td></tr>' for a, b, c in rows) + '</table>'


def page(fonts_html: str) -> str:
    return f"""<title>Темы ЕНТ по учебникам</title>
<meta name="claude:viewport-fit-sides" content="cover">
{fonts_html}
<style>{CSS}</style>
<div class="wrap">
<header>
  <div class="eyebrow">ХимБио просто · подготовка к ЕНТ</div>
  <h1>Темы ЕНТ по химии и биологии: что учить и где читать</h1>
  <p class="lead">Каждая тема спецификации НЦТ — с учебником, параграфами и страницами. Учебники — из перечня НЦТ, по которым составляют задания ЕНТ. В последней колонке — неделя нашего курса, где тема разбирается.</p>
  <ul class="facts"><li><b>19</b> тем по химии</li><li><b>12</b> тем по биологии</li><li><b>40</b> заданий и <b>50</b> баллов на предмет</li></ul>
  <nav aria-label="Разделы"><a href="#chem">Химия</a><a href="#bio">Биология</a><a href="#books">Учебники</a><a href="#how">Как готовиться</a></nav>
</header>
<section class="chem" id="chem">
  <div class="sec-head"><h2>Химия</h2><p>19 тем · Х — химия, номер — класс</p></div>
  <div class="topics">
{topic_rows(CHEM)}
  </div>
</section>
<section class="bio" id="bio">
  <div class="sec-head"><h2>Биология</h2><p>12 тем · Б — биология, номер — класс</p></div>
  <div class="topics">
{topic_rows(BIO)}
  </div>
</section>
<section id="books">
  <div class="sec-head" style="--accent: var(--ink)"><h2>Учебники</h2><p>перечень НЦТ: химия — 2024, биология — 2026</p></div>
  <div class="books">
    <div class="chem"><h3>Химия</h3>{books(BOOKS_CHEM)}</div>
    <div class="bio"><h3>Биология</h3>{books(BOOKS_BIO)}</div>
  </div>
</section>
<section id="how">
  <div class="sec-head" style="--accent: var(--ink)"><h2>Как готовиться по этому списку</h2></div>
  <ol class="how">
    <li>Начинай тему с учебника 8–9 класса: там основа. Затем читай параграфы 10–11 класса ЕМН — там детали, которые спрашивают на ЕНТ.</li>
    <li>Номера страниц — печатные, как внизу страницы учебника. В разных изданиях они могут немного сдвигаться — ищи по номеру параграфа.</li>
    <li>В некоторых учебниках есть ошибки и устаревшие числа. На курсе мы разбираем верные формулировки — в ответах ЕНТ опирайся на них.</li>
    <li>После каждой темы проверь себя заданиями в формате ЕНТ: один ответ, несколько ответов, соответствие, задания к тексту.</li>
  </ol>
</section>
<footer>ХимБио просто · составлено 30.10.2026 по учебникам из перечня НЦТ. Темы — по спецификации ЕНТ по химии и биологии; правила экзамена на 2027 год могут уточниться — сверяем с НЦТ.</footer>
</div>
"""


def main() -> None:
    out = Path(sys.argv[1])
    google = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Unbounded:wght@700;800&display=swap">')
    out.write_text(page(google), encoding='utf-8')
    local = (f"<style>@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0400-045F; }}"
             f"@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-latin-wght-normal.woff2') format('woff2'); }}"
             f"@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0400-045F; }}"
             f"@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-latin-wght-normal.woff2') format('woff2'); }}</style>")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / 'ent-topics.html'
        src.write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"></head><body>' + page(local) + '</body></html>', encoding='utf-8')
        PDF.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([chrome(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={PDF}', src.as_uri()],
                       check=True, capture_output=True)
    print(out, PDF)


if __name__ == '__main__':
    main()
