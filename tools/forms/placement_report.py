"""Инфографика стартового теста: что знают ученики, какие недели сжимать.

    python tools/forms/placement_report.py chem bio

Ответы учеников лежат вне Git: «00 Материалы ХимБио просто/Стартовый тест/results.json» (буквы A–D, N = «Не знаю»).
Ключ берётся из tools/forms/placement.py. Результат — PNG в той же папке.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'social')]
import placement as pl  # noqa: E402
from social import doc, shot  # noqa: E402

OUT = HERE.parents[1] / '00 Материалы ХимБио просто' / 'Стартовый тест'
W = 1400
INK, PAPER, MUTED, CARD, LINE = '#151515', '#F3F0E8', '#B9B3A8', '#1D1D1D', '#3A3A38'
GOOD, MID, BAD, GREY = '#3FA65F', '#E0A82E', '#F13A43', '#6B6862'
SUBJECT = {'chem': ('Химия', pl.CHEM, pl.CHEM_WEEKS, '#F13A43'), 'bio': ('Биология', pl.BIO, pl.BIO_WEEKS, '#1F7A4A')}
PLAN = range(1, 9)  # недели до Нового года
DECISION = {'fast': 'сжать', 'norm': 'обычно', 'full': 'полностью'}


def score(data, answers):
    """Баллы по неделям и счётчики ученика."""
    a = answers.split()
    assert len(a) == 44, len(a)
    key = ['ABCD'[k] for *_, k in data]
    weeks = {}
    for (w, *_), x, k in zip(data, a, key):
        weeks[w] = weeks.get(w, 0) + (x == k)
    right = sum(x == k for x, k in zip(a, key))
    dunno = a.count('N')
    return dict(a=a, weeks=weeks, right=right, dunno=dunno, wrong=44 - right - dunno)


def decide(vals):
    """Правило для маленькой группы: сжимаем знакомое, полностью — где никто не знает или половина на нуле."""
    n = len(vals)
    if max(vals) < 2 or vals.count(0) * 2 >= n:
        return 'full'
    if min(vals) >= 1 and vals.count(2) >= n - 1:
        return 'fast'
    return 'norm'


def common_errors(data, res, labels):
    """Вопросы, где никто не ответил верно."""
    rows = []
    for i, (w, _, q, opts, k) in enumerate(data):
        picks = [r['a'][i] for r in res.values()]
        if 'ABCD'[k] in picks:
            continue
        got = {}
        for p in picks:
            t = 'не знаю' if p == 'N' else opts['ABCD'.index(p)]
            got[t] = got.get(t, 0) + 1
        said = ', '.join(f'{t} ({n})' if n > 1 else t for t, n in sorted(got.items(), key=lambda x: -x[1]))
        rows.append((w, labels.get(str(i + 1), q), said, opts[k]))
    return rows


CSS = f"""
html, body {{ overflow: hidden; }}
.page {{ padding: 56px 60px 44px; }}
.eye {{ font: 800 22px 'Manrope'; letter-spacing: .16em; color: {MUTED}; }}
h1 {{ margin: 14px 0 8px; font: 800 58px/1.08 'Unbounded'; text-transform: uppercase; color: {PAPER}; }}
.sub {{ font: 700 26px/1.3 'Manrope'; color: {MUTED}; }}
h2 {{ margin: 44px 0 18px; font: 800 30px/1.1 'Unbounded'; text-transform: uppercase; color: {PAPER}; }}
.cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 34px; }}
.card2 {{ background: {CARD}; border: 3px solid {LINE}; padding: 24px 24px 22px; }}
.who {{ font: 800 26px 'Unbounded'; color: {PAPER}; }}
.num {{ font: 800 76px/1.05 'Unbounded'; color: {PAPER}; margin-top: 8px; }} .num small {{ font: 800 28px 'Unbounded'; color: {MUTED}; }}
.bar {{ display: flex; gap: 2px; height: 26px; margin: 14px 0 8px; }}
.bar i {{ display: block; height: 100%; }} .bar i:first-child {{ border-radius: 4px 0 0 4px; }} .bar i:last-child {{ border-radius: 0 4px 4px 0; }}
.cnt {{ font: 700 21px 'Manrope'; color: {MUTED}; }} .cnt b {{ color: {PAPER}; }}
.note {{ font: 600 22px/1.3 'Manrope'; color: {PAPER}; margin-top: 12px; }} .note span {{ color: {MUTED}; }}
.tbl {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 36px; }}
.hd, .row {{ display: grid; grid-template-columns: 44px 1fr 56px 56px 56px 132px; gap: 4px; align-items: center; }}
.hd {{ font: 800 19px 'Manrope'; color: {MUTED}; padding-bottom: 8px; }} .hd span {{ text-align: center; }}
.row {{ height: 54px; border-top: 1px solid {LINE}; }}
.row .n {{ font: 800 22px 'Manrope'; color: {MUTED}; }} .row .t {{ font: 700 22px/1.12 'Manrope'; color: {PAPER}; }}
.c {{ height: 40px; display: flex; align-items: center; justify-content: center; font: 800 24px 'Manrope'; border-radius: 4px; }}
.c2 {{ background: {GOOD}; color: {INK}; }} .c1 {{ background: {MID}; color: {INK}; }} .c0 {{ background: {BAD}; color: #fff; }}
.d {{ font: 800 20px 'Manrope'; text-align: center; padding: 7px 0; border-radius: 4px; }}
.fast {{ background: {PAPER}; color: {INK}; }} .norm {{ color: {MUTED}; }} .full {{ border: 2px solid {PAPER}; color: {PAPER}; padding: 5px 0; }}
.keys {{ display: flex; gap: 26px; flex-wrap: wrap; font: 700 21px 'Manrope'; color: {MUTED}; margin-top: 16px; }}
.keys i {{ display: inline-block; width: 20px; height: 20px; border-radius: 4px; vertical-align: -3px; margin-right: 8px; }}
.err {{ display: grid; grid-template-columns: 1.15fr 1.25fr .9fr; gap: 0 18px; }}
.err > div {{ padding: 11px 0; border-top: 1px solid {LINE}; font: 700 23px/1.25 'Manrope'; color: {PAPER}; }}
.err .h {{ border: 0; padding: 0 0 8px; font: 800 19px 'Manrope'; color: {MUTED}; }} .err .bad {{ color: {MUTED}; }}
.plan {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
.plan > div {{ background: {CARD}; border: 3px solid {LINE}; padding: 18px 22px; }}
.plan b {{ display: block; font: 800 22px 'Unbounded'; color: {PAPER}; text-transform: uppercase; }}
.plan p {{ margin: 8px 0 0; font: 700 23px/1.3 'Manrope'; color: {PAPER}; }} .plan span {{ color: {MUTED}; }}
.foot {{ margin-top: 30px; font: 600 20px/1.35 'Manrope'; color: {MUTED}; }}
"""


def page(code: str, block: dict) -> tuple[str, int]:
    subj, data, names, tint = SUBJECT[code]
    res = {n: score(data, a) for n, a in block['answers'].items()}
    order = sorted(res, key=lambda n: -res[n]['right'])
    cards = ''
    for n in order:
        r = res[n]
        good, weak, extra = block['notes'][n]
        seg = ''.join(f'<i style="flex:{v};background:{c}"></i>' for v, c in ((r['right'], GOOD), (r['dunno'], GREY), (r['wrong'], BAD)) if v)
        cards += (f'<div class="card2"><div class="who">{n}</div><div class="num">{r["right"]}<small> / 44</small></div><div class="bar">{seg}</div>'
                  f'<div class="cnt"><b>{r["right"]}</b> верно · <b>{r["dunno"]}</b> не знаю · <b>{r["wrong"]}</b> ошибок</div>'
                  f'<div class="note"><span>Сильное:</span> {good}</div><div class="note"><span>Слабое:</span> {weak}</div><div class="note"><span>{extra}</span></div></div>')
    heads = ''.join(f'<span>{n[:3]}</span>' for n in order)
    verdict = {w: decide([res[n]['weeks'][w] for n in order]) for w in names}

    def half(ws):
        rows = ''.join(f'<div class="row"><div class="n">{w}</div><div class="t">{names[w]}</div>'
                       + ''.join(f'<div class="c c{res[n]["weeks"][w]}">{res[n]["weeks"][w]}</div>' for n in order)
                       + f'<div class="d {verdict[w]}">{DECISION[verdict[w]]}</div></div>' for w in ws)
        return f'<div><div class="hd"><div></div><div>Неделя курса</div>{heads}<div></div></div>{rows}</div>'

    errs = common_errors(data, res, block['labels'])
    err_rows = ''.join(f'<div>{q} <span style="color:{MUTED}">· нед. {w}</span></div><div class="bad">{said}</div><div>{ok}</div>' for w, q, said, ok in errs)

    def plan(kind):
        ws = [str(w) for w in PLAN if verdict[w] == kind]
        return ', '.join(ws) or '—'

    late = [str(w) for w in names if verdict[w] == 'full' and w not in PLAN]
    body = f"""<div class="page">
<div class="eye">ХИМБИО ПРОСТО · ТОЛЬКО ДЛЯ ПРЕПОДАВАТЕЛЯ</div>
<h1>Стартовый тест: <span style="color:{tint if code == 'chem' else GOOD}">{subj.lower()}</span></h1>
<div class="sub">{len(res)} ученика · 44 вопроса, по 2 на неделю курса · {block['date']}</div>
<div class="cards">{cards}</div>
<h2>Что знают по неделям</h2>
<div class="tbl">{half(range(1, 12))}{half(range(12, 23))}</div>
<div class="keys"><span><i style="background:{GOOD}"></i>2 — знает</span><span><i style="background:{MID}"></i>1 — повторить</span><span><i style="background:{BAD}"></i>0 — с нуля</span></div>
<div class="keys" style="margin-top:8px"><span><b style="color:{PAPER}">сжать</b> — знают все или двое, а третий на 1</span><span><b style="color:{PAPER}">полностью</b> — никто не набрал 2 или половина на 0</span></div>
<h2>Никто не ответил верно</h2>
<div class="err"><div class="h">Вопрос</div><div class="h">Что выбрали</div><div class="h">Верно</div>{err_rows}</div>
<h2>Что делаем до Нового года</h2>
<div class="plan"><div><b>Сжать</b><p><span>недели</span> {plan('fast')}</p></div><div><b>Обычно</b><p><span>недели</span> {plan('norm')}</p></div><div><b>Полностью</b><p><span>недели</span> {plan('full')}</p></div></div>
<div class="foot">Позже, полностью: недели {', '.join(late) or '—'}. По 2 вопроса на неделю — грубая оценка, решение проверяем контролем недели. Результаты ученикам сообщаем лично.</div>
</div>"""
    h = 1935 + 84 * len(errs)
    return doc(W, h, CSS, body), h


def main() -> None:
    blocks = json.loads((OUT / 'results.json').read_text(encoding='utf-8'))
    for code in sys.argv[1:] or ['chem', 'bio']:
        html, h = page(code, blocks[code])
        out = OUT / f'{SUBJECT[code][0]} — инфографика.png'
        shot(html, W, h, out)
        print('ok', out.name, h)


if __name__ == '__main__':
    main()
