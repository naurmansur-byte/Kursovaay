"""Презентация урока «Химия просто» (новый формат): course/week-NN/lesson-K-slides.md -> PPTX + PDF.

Урок = части (`# Название`), у каждой части вопрос (`? …`) и связка с прошлой частью (`↳ …`).
Слайды части: `## Тип: Заголовок` — Понятие, Схема, Пример (раскрывается по шагам), Ловушка,
Практика (после неё автоматически «Проверим» из блока «Ответы:»), Итог, Дома. Строки `> …` — заметки преподавателю.
Запуск: .venv/Scripts/python tools/slides/lesson_deck.py week-01 1 [--keep-png]
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from slides import ATOM, body_html, inline, page, render  # noqa: E402

TAGS = {'понятие': 'Понятие', 'схема': 'Схема', 'пример': 'Разберём', 'ловушка': 'Ловушка', 'практика': 'Попробуй сам',
        'итог': 'Итог', 'дома': 'Дома'}


def parse(text: str) -> tuple[dict, list[dict]]:
    meta = {}
    if text.startswith('---'):
        head, _, text = text[3:].partition('\n---')
        meta = {k.strip(): v.strip() for k, _, v in (ln.partition(':') for ln in head.strip().splitlines())}
    parts, part, slide = [], None, None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith('# '):
            part = {'title': line[2:].strip(), 'question': '', 'link': '', 'notes': [], 'slides': []}
            parts.append(part)
            slide = None
        elif part is None:
            continue
        elif line.startswith('## '):
            kind, _, title = line[3:].partition(':')
            title, _, hint = title.strip().partition(' · ')
            slide = {'kind': kind.strip().lower(), 'title': title.strip(), 'hint': hint.strip(), 'lines': [], 'answers': [], 'notes': []}
            part['slides'].append(slide)
        elif line.startswith('>'):
            (slide or part)['notes'].append(line.lstrip('> ').strip())
        elif slide is None and line.startswith('?'):
            part['question'] = line[1:].strip()
        elif slide is None and line.startswith('↳'):
            part['link'] = line[1:].strip()
        elif slide is not None and line.strip():
            if line.strip().lower() == 'ответы:':
                slide['in_answers'] = True
            elif slide.get('in_answers'):
                slide['answers'].append(line.strip())
            else:
                slide['lines'].append(line.strip())
    return meta, parts


def build(week: str, lesson: str) -> None:
    src = ROOT / 'course' / week / f'lesson-{lesson}-slides.md'
    meta, parts = parse(src.read_text(encoding='utf-8'))
    css = ((HERE / 'slides.css').read_text(encoding='utf-8') + (HERE / 'lesson.css').read_text(encoding='utf-8')).replace(
        '{{FONTS}}', (ROOT / 'content/brand/fonts').as_uri())
    wk, ls = meta.get('week', week[-1]), meta.get('lesson', lesson)
    n = len(parts)

    def top(i: int | None, dark: bool) -> str:
        bars = ''.join(f'<b class="{"on" if i is not None and k <= i else ""}"></b>' for k in range(n))
        where = f'Часть {i + 1} · {html.escape(parts[i]["title"])}' if i is not None else ''
        return (f'<div class="top"><span><i></i>ХИМИЯ ПРОСТО · НЕДЕЛЯ {wk} · УРОК {ls}</span>'
                f'<span class="where">{where}<span class="bars">{bars}</span></span></div>')

    def content(i, tag, title, inner, cls='light', extra=''):
        return page(css, top(i, cls != 'light') + f'<div class="tag {tag[1]}">{tag[0]}</div><h2><span>{inline(title)}</span></h2>{extra}{inner}', cls)

    pages: list[tuple[str, str]] = []
    pages.append((page(css, '<div class="top"><span><i></i>ХИМИЯ ПРОСТО · ПОДГОТОВКА К ЕНТ</span><span></span></div>'
                       f'<div class="plaque">Неделя {wk} · урок {ls}</div><h1 class="cover-title">{inline(meta.get("title", ""))}</h1>'
                       f'<p class="cover-goal">{inline(meta.get("goal", ""))}</p>{ATOM}', 'dark cover'), 'Обложка урока.'))
    agenda = ''.join(f'<li><span>{k + 1}</span>{inline(p["title"])}</li>' for k, p in enumerate(parts))
    pages.append((page(css, top(None, False) + f'<h2><i></i>План урока</h2><ol class="agenda">{agenda}</ol>', 'light'),
                  'План урока: части по порядку.'))

    for i, part in enumerate(parts):
        link = f'<p class="link">{inline(part["link"])}</p>' if part['link'] else ''
        pages.append((page(css, top(i, True) + f'<div class="plaque small">Часть {i + 1} из {n}</div>'
                           f'<h1 class="part-title">{inline(part["title"])}</h1>'
                           + (f'<p class="question">{inline(part["question"])}</p>' if part['question'] else '') + link, 'dark part'),
                      '\n'.join(part['notes']) or part['title']))
        for s in part['slides']:
            kind, notes = s['kind'], '\n'.join(s['notes'])
            label = TAGS.get(kind, kind.capitalize())
            if kind == 'схема':
                formula, *rows = s['lines']
                items = ''.join(f'<div><b>{inline(a)}</b><span>{inline(b)}</span></div>'
                                for a, _, b in (r.partition(' — ') for r in rows))
                pages.append((content(i, (label, ''), s['title'], f'<div class="scheme"><div class="big">{inline(formula)}</div>'
                                                                   f'<div class="keys">{items}</div></div>'), notes))
            elif kind == 'пример':
                steps = [re.sub(r'^\d+[.)]\s*', '', ln) for ln in s['lines']]
                for k in range(1, len(steps) + 1):
                    lis = ''.join(f'<li class="{"now" if j == k - 1 else ""}">{inline(st)}</li>' for j, st in enumerate(steps[:k]))
                    pages.append((content(i, (label, ''), s['title'], f'<ol class="steps">{lis}</ol>'), notes))
            elif kind == 'ловушка':
                main, _ = body_html(s['lines'], dark=True)
                pages.append((content(i, (label, 'inv'), s['title'], f'<div class="body">{main}</div>', 'trapbg'), notes))
            elif kind == 'практика':
                timer = f'<div class="timer">{html.escape(s["hint"])}</div>' if s['hint'] else ''
                tasks = ''.join(f'<li>{inline(re.sub(r"^\d+[.)]\s*", "", ln))}</li>' for ln in s['lines'])
                pages.append((content(i, (label, ''), s['title'], f'<ol class="tasks">{tasks}</ol>', extra=timer), notes))
                if s['answers']:
                    ans = ''.join(f'<li>{inline(re.sub(r"^\d+[.)]\s*", "", ln))}</li>' for ln in s['answers'])
                    pages.append((content(i, ('Проверим', ''), s['title'], f'<ol class="tasks answers">{ans}</ol>', 'dark'),
                                  'Показать после попытки.\n' + notes))
            elif kind == 'итог':
                lis = ''.join(f'<li>{inline(ln.lstrip("- "))}</li>' for ln in s['lines'])
                pages.append((content(i, (label, ''), s['title'], f'<ul class="recap">{lis}</ul>', 'dark'), notes))
            else:  # понятие, дома и прочее
                main, calls = body_html(s['lines'], dark=False)
                pages.append((content(i, (label, ''), s['title'], f'<div class="body">{main}</div><div class="callouts">{calls}</div>'),
                              notes))

    out = ROOT / 'exports' / week
    render(pages, out / f'lesson-{lesson}-slides.pptx', out / f'lesson-{lesson}-slides.pdf',
           keep=out / f'lesson-{lesson}-png' if '--keep-png' in sys.argv else None)
    print(f'Lesson deck: {len(pages)} slides, {n} parts -> {out / f"lesson-{lesson}-slides.pptx"}')


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
