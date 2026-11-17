"""Тест практики недели N: 30 вопросов с одним ответом A–D на закрепление темы недели.

Решают на первом (лекционном) занятии недели, если осталось время; если нет — преподаватель проходит тест с учениками позже.
Когда именно — решает преподаватель. Это не пробник недели (тот — в формате ЕНТ, решают на экране вместе).

Запуск: .venv/Scripts/python.exe tools/social/practice.py chem-3 bio-3 …   (или all — все недели, где есть practice.json)
Источник — course/week-NN/practice.json и course/biology/week-NN/practice.json:
  {"subject": "chem"|"bio", "week": N, "topic": "…", "questions": [{"q": …, "a": верный, "wrong": [3 неверных], "why": …}, …30]}
Вопросы — по конспекту курса и учебникам НЦТ; часть идей взята из банка переведённых вопросов (переписаны своими словами и сверены).
Результат — в папке недели, подпапка «Тест практики»: «Тест практики N.pdf» (ученику, без ответов)
и «Тест практики N — ответы.pdf» (преподавателю: верный вариант выделен, короткое объяснение, ключ).
Варианты перемешиваются с постоянным зерном: повторный запуск даёт те же буквы; буквы распределены ровно, без серий.
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE.parent), str(ROOT / 'tools' / 'handout')]
from handout import chrome  # noqa: E402
from teacher_drive import week_dir  # noqa: E402

N = 30
ACCENT = {'chem': '#D9272F', 'bio': '#1F7A4A'}
NAME = {'chem': 'Химия', 'bio': 'Биология'}
FONTS = (ROOT / 'content/brand/fonts').as_uri()
FOLDER = 'Тест практики'


def path(code: str) -> Path:
    subject, week = code.split('-')
    return ROOT / 'course' / ('biology' if subject == 'bio' else '') / f'week-{int(week):02d}' / 'practice.json'


def all_codes() -> list[str]:
    out = []
    for subj, base in (('chem', ROOT / 'course'), ('bio', ROOT / 'course' / 'biology')):
        out += [f'{subj}-{int(p.parent.name[-2:])}' for p in sorted(base.glob('week-*/practice.json'))]
    return out


def check(t: dict) -> None:
    qs = t['questions']
    assert len(qs) == N, (t['subject'], t['week'], len(qs))
    seen = set()
    for q in qs:
        assert len(q['wrong']) == 3 and len({q['a'], *q['wrong']}) == 4, q['q']
        assert q['why'].strip(), q['q']
        assert q['q'] not in seen, ('повтор', q['q'])
        seen.add(q['q'])


def good(letters: list[str]) -> bool:
    """Каждая буква 6–9 раз, нет трёх одинаковых подряд, нет повторяющегося узора."""
    if max(letters.count(c) for c in 'ABCD') > 9 or min(letters.count(c) for c in 'ABCD') < 6:
        return False
    if any(letters[i] == letters[i + 1] == letters[i + 2] for i in range(len(letters) - 2)):
        return False
    return not any(all(letters[i] == letters[i + p] for i in range(k, k + 8)) for p in (2, 3, 4) for k in range(len(letters) - p - 8))


def tasks(t: dict) -> list[dict]:
    seed = int(hashlib.md5(f'practice-{t["subject"]}-{t["week"]}'.encode()).hexdigest()[:8], 16)
    for attempt in range(20000):
        rnd = random.Random(seed + attempt * 7919)
        rows = [rnd.sample([q['a'], *q['wrong']], 4) for q in t['questions']]
        if good(['ABCD'[o.index(q['a'])] for o, q in zip(rows, t['questions'])]):
            break
    else:
        raise SystemExit('нет подходящего порядка букв')
    return [dict(n=i, q=q['q'], why=q['why'], options=o, right=o.index(q['a'])) for i, (o, q) in enumerate(zip(rows, t['questions']), 1)]


def css(a: str) -> str:
    return f"""
@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }}
@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-latin-wght-normal.woff2') format('woff2'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }}
@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-latin-wght-normal.woff2') format('woff2'); }}
@page {{ size: A4; margin: 13mm 14mm 14mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font: 500 10.6pt/1.38 'Manrope', Arial, sans-serif; color: #151515; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.hd {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2.4pt solid {a}; padding-bottom: 7pt; margin-bottom: 9pt; }}
.hd .tag {{ font: 800 8.5pt 'Manrope'; letter-spacing: .12em; text-transform: uppercase; color: {a}; }}
.hd h1 {{ margin: 3pt 0 0; font: 800 19pt/1.1 'Unbounded'; }}
.hd h2 {{ margin: 3pt 0 0; font: 700 11pt/1.25 'Manrope'; color: #555; }}
.hd .who {{ text-align: right; font: 600 9pt/1.6 'Manrope'; color: #555; white-space: nowrap; }}
.how {{ font: 600 9.4pt/1.4 'Manrope'; color: #333; background: #F3F0E8; border-left: 3pt solid {a}; padding: 5pt 8pt; margin-bottom: 9pt; }}
.q {{ break-inside: avoid; padding: 5.5pt 0 6pt; border-bottom: .6pt solid #DDD8CE; }}
.q p {{ margin: 0 0 3pt; font-weight: 700; }}
.q p b {{ font: 800 10pt 'Unbounded'; color: {a}; margin-right: 5pt; }}
.o {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5pt 14pt; padding-left: 17pt; }}
.o span i {{ font-style: normal; font-weight: 800; color: #777; margin-right: 4pt; }}
.o .ok {{ font-weight: 800; color: {a}; }} .o .ok i {{ color: {a}; }}
.why {{ margin: 3pt 0 0 17pt; font: 500 9.2pt/1.35 'Manrope'; color: #444; }}
.why b {{ color: {a}; }}
.grid {{ break-inside: avoid; margin-top: 12pt; }}
.grid h3 {{ margin: 0 0 5pt; font: 800 10pt 'Unbounded'; }}
.grid table {{ border-collapse: collapse; width: 100%; table-layout: fixed; }}
.grid td {{ border: .8pt solid #BBB; height: 19pt; font: 700 9pt 'Manrope'; padding: 2pt 4pt; vertical-align: top; color: #666; }}
.grid td b {{ color: {a}; font: 800 10.5pt 'Unbounded'; }}
.foot {{ margin-top: 10pt; font: 500 8pt/1.35 'Manrope'; color: #777; }}
"""


def grid(qs: list[dict], teacher: bool) -> str:
    rows = []
    for k in range(0, N, 10):
        cells = ''.join(f'<td>{q["n"]}{" <b>" + "ABCD"[q["right"]] + "</b>" if teacher else ""}</td>' for q in qs[k:k + 10])
        rows.append(f'<tr>{cells}</tr>')
    title = 'Ключ' if teacher else 'Бланк ответов'
    return f'<div class="grid"><h3>{title}</h3><table>{"".join(rows)}</table></div>'


def html(t: dict, qs: list[dict], teacher: bool) -> str:
    a = ACCENT[t['subject']]
    how = ('Для преподавателя. Тест на закрепление: решаем на первом занятии недели, если осталось время, иначе — разбираем позже. '
           'Верный вариант выделен, под вопросом — короткое объяснение. Ключ — в начале и в конце.') if teacher else \
          ('Выбери один верный ответ из четырёх и запиши букву в бланк в конце. Не угадывай: если не уверен, отметь вопрос — разберём вместе.')
    body = [f"""<div class="hd"><div><div class="tag">{NAME[t['subject']]} · неделя {t['week']} · ХимБио просто</div>
<h1>Тест практики {t['week']}{' — ответы' if teacher else ''}</h1><h2>{escape(t['topic'])}</h2></div>
<div class="who">{'' if teacher else 'Имя ____________________<br>Дата ____________ Верно ____ / 30'}</div></div>
<div class="how">{how}</div>"""]
    if teacher:
        body.append(grid(qs, True))
    for q in qs:
        opts = ''.join(f'<span{" class=ok" if teacher and i == q["right"] else ""}><i>{"ABCD"[i]})</i>{o}</span>' for i, o in enumerate(q['options']))
        why = f'<div class="why"><b>Ответ {"ABCD"[q["right"]]}.</b> {q["why"]}</div>' if teacher else ''
        body.append(f'<div class="q"><p><b>{q["n"]}</b>{q["q"]}</p><div class="o">{opts}</div>{why}</div>')
    body.append(grid(qs, teacher))
    body.append('<div class="foot">Вопросы составлены по конспекту курса и учебникам НЦТ. Это тренировочный тест курса «ХимБио просто», а не задания НЦТ. '
                'Материал проверяется преподавателем.</div>')
    return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{css(a)}</style></head><body>{"".join(body)}</body></html>'


def pdf(page: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / 'p.html'
        src.write_text(page, encoding='utf-8')
        subprocess.run([chrome(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out}', src.as_uri()],
                       check=True, capture_output=True, timeout=300)


def main() -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    codes = all_codes() if sys.argv[1:] == ['all'] else sys.argv[1:]
    for code in codes:
        src = path(code)
        t = json.loads(src.read_text(encoding='utf-8'))
        check(t)
        qs = tasks(t)
        dest = week_dir(src.parent.relative_to(ROOT / 'course').as_posix()) / FOLDER
        pdf(html(t, qs, False), dest / f'Тест практики {t["week"]}.pdf')
        pdf(html(t, qs, True), dest / f'Тест практики {t["week"]} — ответы.pdf')
        print(code, ''.join('ABCD'[q['right']] for q in qs), '->', dest.parent.name)


if __name__ == '__main__':
    main()
