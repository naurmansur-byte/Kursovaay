"""Личные карточки ученикам (без баллов) и записка преподавателям «Как идём дальше».

    python tools/forms/placement_people.py

Всё читается из закрытого results.json и кладётся туда же, в «00 Материалы ХимБио просто/Стартовый тест/» (вне Git).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'social')]
import placement as pl  # noqa: E402
from placement_report import OUT, common_errors, decide, score  # noqa: E402
from social import doc, shot  # noqa: E402
from teacher_hiring import FONTS, pdf  # noqa: E402

INK, PAPER, MUTED, CARD, LINE, GREEN, LGREEN, RED = '#151515', '#F3F0E8', '#B9B3A8', '#1D1D1D', '#3A3A38', '#1F7A4A', '#3FA65F', '#F13A43'
DATES = ['02–08.11', '09–15.11', '16–22.11', '23–29.11', '30.11–06.12', '07–13.12', '14–20.12', '21–27.12']
TAG = {'fast': 'быстрее', 'norm': 'обычно', 'full': 'подробно', 'now': 'уже идёт'}
ROUTE = {2: 'A', 1: 'B', 0: 'C'}
SUBJECTS = (('chem', 'Химия', pl.CHEM, pl.CHEM_WEEKS), ('bio', 'Биология', pl.BIO, pl.BIO_WEEKS))

CARD_CSS = f"""
html, body {{ overflow: hidden; }}
.p {{ padding: 64px 64px 0; }}
.eye {{ font: 800 24px 'Manrope'; letter-spacing: .14em; color: {MUTED}; }}
h1 {{ margin: 16px 0 0; font: 800 84px/1.05 'Unbounded'; color: {PAPER}; }}
.sub {{ margin-top: 10px; font: 700 34px 'Manrope'; color: {LGREEN}; }}
.s {{ margin-top: 30px; padding: 26px 30px 28px; background: {CARD}; border: 3px solid {LINE}; }}
.s b {{ display: block; font: 800 26px 'Unbounded'; text-transform: uppercase; color: {PAPER}; margin-bottom: 12px; }}
.s p {{ margin: 0; font: 700 32px/1.3 'Manrope'; color: {PAPER}; }} .s p + p {{ margin-top: 8px; }}
.s.hi {{ background: {GREEN}; border-color: {GREEN}; }}
.foot {{ position: absolute; left: 64px; right: 64px; bottom: 50px; font: 700 27px/1.3 'Manrope'; color: {MUTED}; }}
"""


def card(name: str, c: dict) -> str:
    rows = lambda xs: ''.join(f'<p>{x}</p>' for x in xs)
    return doc(1080, 1350, CARD_CSS, f"""<div class="p"><div class="eye">ХИМБИО ПРОСТО · ЛИЧНО ДЛЯ ТЕБЯ</div><h1>{name}</h1><div class="sub">Твоя карта старта</div>
<div class="s hi"><b>Твоя сильная сторона</b><p>{c['strong']}</p></div>
<div class="s"><b>Уже получается</b>{rows(c['have'])}</div>
<div class="s"><b>С этого начинаем</b>{rows(c['start'])}</div>
<div class="s"><b>Совет на ближайшие недели</b><p>{c['tip']}</p></div></div>
<div class="foot">Это не оценка и не рейтинг. Просто точка, от которой мы идём вместе.</div>""")


NOTE_CSS = f"""
@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-cyrillic-wght-normal.woff2') format('woff2'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }}
@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-latin-wght-normal.woff2') format('woff2'); }}
@page {{ size: A4; margin: 13mm 13mm; }}
body {{ font: 500 10.3pt/1.36 'Manrope', Arial, sans-serif; color: #141714; margin: 0; }}
h1 {{ font: 800 21pt/1.15 'Unbounded', Arial; margin: 2mm 0 1mm; }}
h2 {{ font: 800 10.5pt/1.2 'Unbounded', Arial; margin: 4.5mm 0 1.6mm; break-after: avoid; }}
.eye {{ font: 800 8.5pt 'Manrope'; letter-spacing: .12em; color: #5C625B; }} .sub {{ color: #5C625B; }}
p {{ margin: 0 0 1.6mm; }} ul {{ margin: 0; padding-left: 5mm; }} li {{ margin-bottom: 1mm; }}
table {{ width: 100%; border-collapse: collapse; margin-bottom: 2mm; break-inside: avoid; }}
th, td {{ padding: .9mm 1.6mm; border-bottom: .3mm solid #D6D9CF; text-align: left; font-size: 9.6pt; }} th {{ color: #5C625B; font-weight: 800; }}
td.r, th.r {{ text-align: center; padding: .9mm 0; width: 8.5mm; font-weight: 800; }}
.A {{ background: #DDEFE4; }} .B {{ background: #FFF3C4; }} .C {{ background: #FBE4E4; }}
.fast {{ font-weight: 800; color: #1F7A4A; }} .full {{ font-weight: 800; color: #B4232B; }} .norm, .now {{ color: #5C625B; }}
"""


def teacher_note(blocks: dict) -> str:
    res, verdict = {}, {}
    for code, _, data, names in SUBJECTS:
        res[code] = {n: score(data, a) for n, a in blocks[code]['answers'].items()}
        verdict[code] = {w: decide([r['weeks'][w] for r in res[code].values()]) for w in names}
    label = lambda v: f'<span class="{v}">{TAG[v]}</span>'
    now = {c: {**v, 1: 'now'} for c, v in verdict.items()}  # неделя 1 уже идёт
    plan = ''.join(f"<tr><td>{w} · {DATES[w - 1]}</td><td>{pl.CHEM_WEEKS[w]}</td><td>{label(now['chem'][w])}</td>"
                   f"<td>{pl.BIO_WEEKS[w]}</td><td>{label(now['bio'][w])}</td></tr>" for w in range(1, 9))

    def routes(code, title):
        heads = ''.join(f'<th class="r">{w}</th>' for w in range(1, 9))
        rows = ''
        for n, r in res[code].items():
            rows += f'<tr><td>{n}</td>' + ''.join(f'<td class="r {ROUTE[r["weeks"][w]]}">{ROUTE[r["weeks"][w]]}</td>' for w in range(1, 9)) + '</tr>'
        return f'<table><tr><th>{title}, неделя</th>{heads}</tr>{rows}</table>'

    def later(code, names):
        ws = [w for w in names if w > 8 and verdict[code][w] == 'full']
        return ', '.join(f'{w} ({names[w]})' for w in ws)

    def traps(code, data):
        return ''.join(f'<li>Неделя {w}. {q}: выбрали «{said}», верно «{ok}».</li>' for w, q, said, ok in common_errors(data, res[code], blocks[code]['labels']))

    return f"""<style>{NOTE_CSS}</style>
<div class="eye">ХИМБИО ПРОСТО · ДЛЯ ПРЕПОДАВАТЕЛЕЙ · ИМЕНА И РЕЗУЛЬТАТЫ УЧЕНИКОВ НЕ ПЕРЕСЫЛАТЬ</div>
<h1>Как идём дальше</h1><p class="sub">Стартовый тест и план до Нового года. Это предложение: ждём ваших правок.</p>
<h2>Что произошло</h2>
<p>Трое учеников прошли стартовый тест: химию 02.11, биологию 03.11. В каждом тесте 44 вопроса, по 2 на неделю курса 1–22, так что оценка грубая. Вопросы авторские, преподаватель их ещё не проверял. Полная картина — в двух инфографиках, они приложены.</p>
<h2>Что меняем</h2>
<ul><li><b>Сетку недель не двигаем.</b> Темы, даты, материалы и контроль остаются.</li>
<li><span class="fast">быстрее</span> — на уроке 1 вместо объяснения с нуля короткая проверка и повторение, затем задания формата ЕНТ. Урок 2 и контроль как обычно.</li>
<li><span class="norm">обычно</span> — по плану урока.</li>
<li><span class="full">подробно</span> — по плану без сокращений, больше времени на образец и вопросы.</li></ul>
<h2>План до Нового года</h2>
<table><tr><th>Неделя</th><th>Химия</th><th></th><th>Биология</th><th></th></tr>{plan}</table>
<p>Неделю 1 оставляем как есть, она уже идёт. Первые недели «быстрее»: химия — неделя 3, биология — неделя 6. После Нового года подробно: химия — {later('chem', pl.CHEM_WEEKS)}; биология — {later('bio', pl.BIO_WEEKS)}.</p>
<h2>Варианты ДЗ: ориентир на старт</h2>
<p>A — углубление, B — закрепление, C — поддержка. Букву выбираете вы: тест только подсказка, важнее объяснение ученика и контроль недели.</p>
{routes('chem', 'Химия')}{routes('bio', 'Биология')}
<h2>Где никто не ответил верно</h2>
<p>Эти вопросы стоит разобрать на уроках своих недель.</p>
<p><b>Химия</b></p><ul>{traps('chem', pl.CHEM)}</ul>
<p style="margin-top:2mm"><b>Биология</b></p><ul>{traps('bio', pl.BIO)}</ul>
<h2>Как говорим с учениками и родителями</h2>
<ul><li>Баллы не называем и никого не сравниваем. В общем чате результаты не обсуждаем.</li>
<li>Мансур проводит встречу с учениками: знакомство, сильные стороны группы, план. Имён и баллов на слайдах нет.</li>
<li>Каждый ученик получает личную карту: что получается и с чего начинаем. Родители получают короткое сообщение без цифр.</li>
<li>«Не знаю» хвалим: это честный ответ, с ним легче работать.</li></ul>
<h2>Что нужно от вас</h2>
<ul><li>Посмотреть вопросы и ключ своего предмета: нет ли ошибок.</li><li>Подтвердить план недель или написать, что поменять.</li><li>Назначать варианты ДЗ с учётом таблицы выше.</li></ul>"""


def key_doc(title: str, data, names) -> str:
    rows = ''.join(f"<tr><td>{i}</td><td>{w} · {names[w]}</td><td>{lvl}</td><td>{q}<br><span class=\"norm\">{' · '.join(pl.lettered(o))}</span></td><td><b>{pl.lettered(o)[k]}</b></td></tr>"
                   for i, (w, lvl, q, o, k) in enumerate(data, 1))
    return (f'<style>{NOTE_CSS} table {{ break-inside: auto; }} tr {{ break-inside: avoid; }}</style><div class="eye">ХИМБИО ПРОСТО · ТОЛЬКО ПРЕПОДАВАТЕЛЮ</div><h1>Стартовый тест: {title}</h1>'
            '<p class="sub">Вопросы и ключ. Черновик, ждёт вашей проверки. В форме в каждом вопросе есть ещё вариант «Не знаю».</p>'
            f'<table><tr><th>№</th><th>Неделя</th><th>Ур.</th><th>Вопрос и варианты</th><th>Ответ</th></tr>{rows}</table>')


def main() -> None:
    blocks = json.loads((OUT / 'results.json').read_text(encoding='utf-8'))
    cards = OUT / 'Личные карты учеников'
    cards.mkdir(exist_ok=True)
    for name, c in blocks['cards'].items():
        shot(card(name, c), 1080, 1350, cards / f'{name} — карта старта.png')
    pdf(teacher_note(blocks), OUT / 'Как идём дальше — преподавателям.pdf')
    for _, title, data, names in SUBJECTS:
        pdf(key_doc(title.lower(), data, names), OUT / f'Вопросы и ключ — {title.lower()}.pdf')
    print('ok', len(blocks['cards']), 'карты и записка')


if __name__ == '__main__':
    main()
