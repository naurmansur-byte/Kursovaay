"""Сборник недели, 1920×1080 в стиле 2: задания в формате ЕНТ по теме недели, преподаватель решает на экране вместе с учениками.

Запуск: .venv/Scripts/python tools/social/sbornik.py chem-1 bio-1
Источник — course/week-NN/sbornik.json и course/biology/week-NN/sbornik.json: те же доли, что на ЕНТ, в 2,5 раза короче
(10 один ответ, 2 к тексту, 2 соответствие, 2 несколько ответов; уровни A/B/C = 8/5/3).
Результат — в папке недели: «Ученику/6 Сборник недели.pdf» (без ответов), «Преподавателю/Сборник недели — с решениями.pdf».
Варианты перемешиваются с постоянным зерном: повторный запуск даёт те же буквы, а порядок верных букв проверяется.
"""
from __future__ import annotations

import json
import random
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
from social import doc, shot  # noqa: E402
from teacher_drive import week_dir  # noqa: E402

ROOT = HERE.parents[1]
W, H = 1920, 1080
INK, PAPER, MUTED, CARD, LINE = '#151515', '#F3F0E8', '#B9B3A8', '#1D1D1D', '#3A3A38'
ACCENT = {'chem': '#F13A43', 'bio': '#3FA65F'}
NAME = {'chem': 'Химия', 'bio': 'Биология'}
BLOCK = {'one': '1–10 · один ответ', 'text': '11–12 · вопросы к тексту', 'match': '13–14 · соответствие', 'many': '15–16 · несколько ответов, верных не больше трёх'}


def path(code: str) -> Path:
    subject, week = code.split('-')
    return ROOT / 'course' / ('biology' if subject == 'bio' else '') / f'week-{int(week):02d}' / 'sbornik.json'


def check(t: dict) -> None:
    qs = t['single'] + t['context']['questions'] + t['matching'] + t['multi']
    assert (len(t['single']), len(t['context']['questions']), len(t['matching']), len(t['multi'])) == (10, 2, 2, 2), t['week']
    levels = [q['level'] for q in qs]
    assert (levels.count('A'), levels.count('B'), levels.count('C')) == (8, 5, 3), levels
    for q in t['single'] + t['context']['questions']:
        assert len(q['wrong']) == 3 and len({q['a'], *q['wrong']}) == 4, q['q']
    for q in t['matching']:
        opts = [b for _, b in q['items']] + q['extra']
        assert len(q['items']) == 2 and len(opts) == 4 and len(set(opts)) == 4, q['q']
    for q in t['multi']:
        assert 1 <= len(q['right']) <= 3 and len(q['right']) + len(q['wrong']) == 6, q['q']
    assert all(q['why'] for q in qs)


def good(letters: list[str]) -> bool:
    """Буквы не должны идти подряд, по кругу или слишком часто одна и та же."""
    if max(letters.count(c) for c in 'ABCD') > 4 or min(letters.count(c) for c in 'ABCD') < 2:
        return False
    if any(letters[i] == letters[i + 1] == letters[i + 2] for i in range(len(letters) - 2)):
        return False
    return not any(all(letters[i] == letters[i + p] for i in range(len(letters) - p)) for p in (2, 3, 4))


def tasks(t: dict) -> list[dict]:
    """Перемешанные задания с буквами."""
    seed = sum(map(ord, t['subject'])) * 100 + t['week']
    choice = t['single'] + t['context']['questions']
    for attempt in range(10000):
        rnd = random.Random(seed + attempt)
        rows = [rnd.sample([q['a'], *q['wrong']], 4) for q in choice]
        if good(['ABCD'[o.index(q['a'])] for o, q in zip(rows, choice)]):
            break
    else:
        raise SystemExit('нет подходящего порядка букв')
    out = []
    for i, (o, q) in enumerate(zip(rows, choice), 1):
        out.append(dict(n=i, kind='one' if i <= 10 else 'text', q=q['q'], why=q['why'], options=o, right=[o.index(q['a'])]))
    for i, q in enumerate(t['matching'], 13):
        o = rnd.sample([b for _, b in q['items']] + q['extra'], 4)
        out.append(dict(n=i, kind='match', q=q['q'], why=q['why'], options=o, items=[a for a, _ in q['items']], right=[o.index(b) for _, b in q['items']]))
    for i, q in enumerate(t['multi'], 15):
        o = rnd.sample(q['right'] + q['wrong'], 6)
        out.append(dict(n=i, kind='many', q=q['q'], why=q['why'], options=o, right=sorted(o.index(x) for x in q['right'])))
    return out


def answer(q: dict) -> str:
    if q['kind'] == 'match':
        return f'A{q["right"][0] + 1} B{q["right"][1] + 1}'
    return ''.join('ABCDEF'[i] for i in q['right'])


def css(a: str) -> str:
    return f"""
html, body {{ overflow: hidden; }}
.top {{ position: absolute; left: 90px; right: 90px; top: 52px; display: flex; justify-content: space-between; font: 800 24px 'Manrope'; letter-spacing: .1em; color: {MUTED}; text-transform: uppercase; }}
.w {{ position: absolute; left: 90px; right: 90px; top: 120px; bottom: 56px; display: flex; flex-direction: column; gap: 30px; }}
.h {{ display: flex; gap: 34px; align-items: baseline; }}
.h b {{ font: 800 66px/1 'Unbounded'; color: {a}; }} .h p {{ margin: 0; font: 800 58px/1.22 'Manrope'; color: {PAPER}; }}
.txt {{ font: 700 34px/1.36 'Manrope'; color: {PAPER}; background: {CARD}; border-left: 8px solid {a}; padding: 22px 30px; }}
.o {{ display: grid; grid-template-columns: 1fr 1fr; gap: 26px 56px; }}
.o div {{ display: flex; gap: 20px; font: 700 50px/1.22 'Manrope'; color: {PAPER}; }} .o i {{ flex: none; font: 800 44px/1.36 'Unbounded'; color: {MUTED}; font-style: normal; width: 62px; }}
.o .ok, .o .ok i {{ color: {a}; }}
.m {{ display: grid; grid-template-columns: 1fr 1.25fr; gap: 56px; }} .m .o {{ grid-template-columns: 1fr; gap: 14px; }}
.ans {{ margin-top: auto; padding: 20px 30px; background: {CARD}; border-left: 8px solid {a}; font: 700 33px/1.32 'Manrope'; color: {PAPER}; }} .ans b {{ color: {a}; }}
.cv {{ position: absolute; left: 110px; top: 250px; right: 110px; }}
.cv .plaque {{ background: {a if a != ACCENT['bio'] else '#1F7A4A'}; font-size: 44px; padding: 12px 30px 18px; }}
.cv h1 {{ margin: 44px 0 0; font: 800 96px/1.08 'Unbounded'; text-transform: uppercase; color: {PAPER}; }}
.cv h2 {{ margin: 22px 0 0; font: 700 46px/1.25 'Manrope'; color: {MUTED}; }}
.cv p {{ margin: 60px 0 0; font: 700 36px/1.35 'Manrope'; color: {PAPER}; }}
"""


def cover(t: dict, teacher: bool) -> str:
    how = 'Решаем вместе: вы показываете на экране, ученики думают, отвечают и спрашивают.' if teacher else 'Решаем вместе с преподавателем: смотри, спрашивай, отвечай.'
    return doc(W, H, css(ACCENT[t['subject']]), f"""<div class="cv"><span class="plaque">{NAME[t['subject']]} · неделя {t['week']}</span>
<h1>Сборник недели</h1><h2>{t['topic']}</h2><p>{how}</p></div>""")


def opts(q: dict, teacher: bool, numbers: bool = False) -> str:
    mark = lambda i: ' class="ok"' if teacher and i in q['right'] else ''
    label = lambda i: i + 1 if numbers else 'ABCDEF'[i]
    return '<div class="o">' + ''.join(f'<div{mark(i)}><i>{label(i)}</i><span>{o}</span></div>' for i, o in enumerate(q['options'])) + '</div>'


def page(t: dict, q: dict, teacher: bool) -> str:
    head = f'<div class="h"><b>{q["n"]}</b><p>{q["q"]}</p></div>'
    if q['kind'] == 'match':
        left = '<div class="o" style="grid-template-columns:1fr">' + ''.join(f'<div><i>{"AB"[i]}</i><span>{x}</span></div>' for i, x in enumerate(q['items'])) + '</div>'
        body = f'<div class="m">{left}{opts(q, teacher, numbers=True)}</div>'
    else:
        body = opts(q, teacher)
    text = f'<div class="txt">{t["context"]["text"]}</div>' if q['kind'] == 'text' else ''
    ans = f'<div class="ans"><b>Ответ: {answer(q)}.</b> {q["why"]}</div>' if teacher else ''
    return doc(W, H, css(ACCENT[t['subject']]), f"""<div class="top"><span>{NAME[t['subject']]} · неделя {t['week']}</span><span>{BLOCK[q['kind']]}</span></div>
<div class="w">{text}{head}{body}{ans}</div>""")


def save(pages: list[str], out: Path) -> None:
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmp:
        ims = []
        for i, html in enumerate(pages):
            p = Path(tmp) / f'{i:02d}.png'
            shot(html, W, H, p)
            ims.append(Image.open(p).convert('RGB'))
        ims[0].save(out, save_all=True, append_images=ims[1:], resolution=144)


def main() -> None:
    for code in sys.argv[1:]:
        src = path(code)
        t = json.loads(src.read_text(encoding='utf-8'))
        check(t)
        qs = tasks(t)
        dest = week_dir(src.parent.relative_to(ROOT / 'course').as_posix())
        save([cover(t, False)] + [page(t, q, False) for q in qs], dest / 'Ученику' / '6 Сборник недели.pdf')
        save([cover(t, True)] + [page(t, q, True) for q in qs], dest / 'Преподавателю' / 'Сборник недели — с решениями.pdf')
        print(code, ' '.join(f'{q["n"]}{answer(q)}' for q in qs), '->', dest.name)


if __name__ == '__main__':
    main()
