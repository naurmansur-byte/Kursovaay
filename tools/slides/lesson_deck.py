"""Презентация урока «Химия просто» (новый формат): course/week-NN/lesson-K-slides.md -> PPTX + PDF.

Урок = части (`# Название`), у каждой части вопрос (`? …`) и связка с прошлой частью (`↳ …`).
Слайды части: `## Тип: Заголовок` — Понятие, Схема, Пример (раскрывается по шагам), Ловушка,
Практика (после неё автоматически «Проверим» из блока «Ответы:»), Итог, Дома, Курс. Строки `> …` — заметки преподавателю.
Для видео: `> 🎙 текст` — озвучка слайда/части, `> 🎙N текст` — озвучка N-го шага примера; в front matter `intro`, `agenda`,
`label` (метка сверху), `plaque` (плашка обложки). С --manifest пишет список слайдов с озвучкой (JSON).

Запуск: .venv/Scripts/python tools/slides/lesson_deck.py week-01 1 [--keep-png]
        .venv/Scripts/python tools/slides/lesson_deck.py --src content/youtube/Y001-mol/deck.md --out exports/youtube/Y001 --keep-png --manifest
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from slides import ATOM, body_html, inline, page, render  # noqa: E402

TAGS = {'понятие': 'Понятие', 'схема': 'Схема', 'пример': 'Разберём', 'ловушка': 'Ловушка', 'практика': 'Попробуй сам',
        'итог': 'Итог', 'дома': 'Дома', 'курс': 'Курс'}
VOICE = re.compile(r'^🎙\s*(\d*)\s*(.*)$')
NUM = re.compile(r'^\d+[.)]\s*')


def parse(text: str) -> tuple[dict, list[dict]]:
    meta = {}
    if text.startswith('---'):
        head, _, text = text[3:].partition('\n---')
        meta = {k.strip(): v.strip() for k, _, v in (ln.partition(':') for ln in head.strip().splitlines())}
    parts, part, slide = [], None, None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith('# '):
            part = {'title': line[2:].strip(), 'question': '', 'link': '', 'notes': [], 'slides': [], 'voice': '', 'steps': {}}
            parts.append(part)
            slide = None
        elif part is None:
            continue
        elif line.startswith('## '):
            kind, _, title = line[3:].partition(':')
            title, _, hint = title.strip().partition(' · ')
            slide = {'kind': kind.strip().lower(), 'title': title.strip(), 'hint': hint.strip(), 'lines': [], 'answers': [],
                     'notes': [], 'voice': '', 'steps': {}}
            part['slides'].append(slide)
        elif line.startswith('>'):
            note = line.lstrip('> ').strip()
            v = VOICE.match(note)
            target = slide or part
            if v and v.group(1):
                target['steps'][int(v.group(1))] = v.group(2)
            elif v:
                target['voice'] = (target['voice'] + ' ' + v.group(2)).strip()
            else:
                target['notes'].append(note)
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


def build(src: Path, out_pptx: Path, label: str, plaque: str, keep: Path | None, manifest: Path | None) -> None:
    meta, parts = parse(src.read_text(encoding='utf-8'))
    label = meta.get('label', label)
    plaque = meta.get('plaque', plaque)
    css = ((HERE / 'slides.css').read_text(encoding='utf-8') + (HERE / 'lesson.css').read_text(encoding='utf-8')).replace(
        '{{FONTS}}', (ROOT / 'content/brand/fonts').as_uri())
    n = len(parts)
    pages: list[tuple[str, str]] = []
    voices: list[str] = []

    def add(doc: str, notes: str, voice: str = '') -> None:
        pages.append((doc, notes))
        voices.append(voice)

    def top(i: int | None) -> str:
        bars = ''.join(f'<b class="{"on" if i is not None and k <= i else ""}"></b>' for k in range(n))
        where = f'Часть {i + 1} · {html.escape(parts[i]["title"])}' if i is not None else ''
        return f'<div class="top"><span><i></i>{html.escape(label)}</span><span class="where">{where}<span class="bars">{bars}</span></span></div>'

    def content(i, tag, title, inner, cls='light', extra=''):
        return page(css, top(i) + f'<div class="tag {tag[1]}">{tag[0]}</div><h2><span>{inline(title)}</span></h2>{extra}{inner}', cls)

    add(page(css, '<div class="top"><span><i></i>ХИМИЯ ПРОСТО · ПОДГОТОВКА К ЕНТ</span><span></span></div>'
             f'<div class="plaque">{html.escape(plaque)}</div><h1 class="cover-title">{inline(meta.get("title", ""))}</h1>'
             f'<p class="cover-goal">{inline(meta.get("goal", ""))}</p>{ATOM}', 'dark cover'), 'Обложка.', meta.get('intro', ''))
    agenda = ''.join(f'<li><span>{k + 1}</span>{inline(p["title"])}</li>' for k, p in enumerate(parts))
    add(page(css, top(None) + f'<h2><i></i><span>План</span></h2><ol class="agenda">{agenda}</ol>', 'light'), 'План: части по порядку.',
        meta.get('agenda', ''))

    for i, part in enumerate(parts):
        link = f'<p class="link">{inline(part["link"])}</p>' if part['link'] else ''
        add(page(css, top(i) + f'<div class="plaque small">Часть {i + 1} из {n}</div><h1 class="part-title">{inline(part["title"])}</h1>'
                 + (f'<p class="question">{inline(part["question"])}</p>' if part['question'] else '') + link, 'dark part'),
            '\n'.join(part['notes']) or part['title'], part['voice'])
        for s in part['slides']:
            kind, notes = s['kind'], '\n'.join(s['notes'])
            label_tag = TAGS.get(kind, kind.capitalize())
            if kind == 'схема':
                formula, *rows = s['lines']
                items = ''.join(f'<div><b>{inline(a)}</b><span>{inline(b)}</span></div>' for a, _, b in (r.partition(' — ') for r in rows))
                add(content(i, (label_tag, ''), s['title'], f'<div class="scheme"><div class="big">{inline(formula)}</div>'
                                                             f'<div class="keys">{items}</div></div>'), notes, s['voice'])
            elif kind == 'пример':
                steps = [NUM.sub('', ln) for ln in s['lines']]
                for k in range(1, len(steps) + 1):
                    lis = ''.join(f'<li class="{"now" if j == k - 1 else ""}">{inline(st)}</li>' for j, st in enumerate(steps[:k]))
                    add(content(i, (label_tag, ''), s['title'], f'<ol class="steps">{lis}</ol>'), notes,
                        s['steps'].get(k, s['voice'] if k == 1 else ''))
            elif kind == 'ловушка':
                main, _ = body_html(s['lines'], dark=True)
                add(content(i, (label_tag, 'inv'), s['title'], f'<div class="body">{main}</div>', 'trapbg'), notes, s['voice'])
            elif kind == 'практика':
                timer = f'<div class="timer">{html.escape(s["hint"])}</div>' if s['hint'] else ''
                tasks = ''.join(f'<li>{inline(NUM.sub("", ln))}</li>' for ln in s['lines'])
                add(content(i, (label_tag, ''), s['title'], f'<ol class="tasks">{tasks}</ol>', extra=timer), notes, s['voice'])
                if s['answers']:
                    ans = ''.join(f'<li>{inline(NUM.sub("", ln))}</li>' for ln in s['answers'])
                    add(content(i, ('Проверим', ''), s['title'], f'<ol class="tasks answers">{ans}</ol>', 'dark'),
                        'Показать после попытки.\n' + notes, s['steps'].get(1, ''))
            elif kind == 'итог':
                lis = ''.join(f'<li>{inline(ln.lstrip("- "))}</li>' for ln in s['lines'])
                add(content(i, (label_tag, ''), s['title'], f'<ul class="recap">{lis}</ul>', 'dark'), notes, s['voice'])
            else:  # понятие, дома, курс и прочее
                main, calls = body_html(s['lines'], dark=False)
                add(content(i, (label_tag, ''), s['title'], f'<div class="body">{main}</div><div class="callouts">{calls}</div>'),
                    notes, s['voice'])

    render(pages, out_pptx, out_pptx.with_suffix('.pdf'), keep=keep)
    if manifest:
        manifest.write_text(json.dumps([{'png': f's{k + 1:02d}.png', 'voice': v} for k, v in enumerate(voices)], ensure_ascii=False, indent=1),
                            encoding='utf-8')
    print(f'Deck: {len(pages)} slides, {n} parts -> {out_pptx}' + (f'; manifest {manifest}' if manifest else ''))


def main(argv: list[str]) -> None:
    keep_png = '--keep-png' in argv
    if '--src' in argv:
        src = ROOT / argv[argv.index('--src') + 1]
        out = ROOT / argv[argv.index('--out') + 1]
        out.mkdir(parents=True, exist_ok=True)
        build(src, out / 'deck.pptx', 'ХИМИЯ ПРОСТО', 'Химия для ЕНТ', out / 'png' if keep_png else None,
              out / 'manifest.json' if '--manifest' in argv else None)
        return
    week, lesson = argv[0], argv[1]
    meta_week = week[-2:].lstrip('0')
    out = ROOT / 'exports' / week
    build(ROOT / 'course' / week / f'lesson-{lesson}-slides.md', out / f'lesson-{lesson}-slides.pptx',
          f'ХИМИЯ ПРОСТО · НЕДЕЛЯ {meta_week} · УРОК {lesson}', f'Неделя {meta_week} · урок {lesson}',
          out / f'lesson-{lesson}-png' if keep_png else None, None)


if __name__ == '__main__':
    main(sys.argv[1:])
