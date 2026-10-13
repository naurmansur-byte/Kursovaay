"""Карта уроков «ХимБио просто»: темы недель из обеих программ + статус комплекта + видео по теме → одна HTML-страница.

Запуск: .venv/Scripts/python tools/map/lesson_map.py <выходной .html>
Статусы правятся в STATUS ниже (после каждой принятой задачи Мартина), темы берутся из course/PROGRAM.md и course/biology/PROGRAM.md.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UPDATED = '13.10.2026'

# Статус учебной недели (номер У). done — комплект готов и принят Максом; work — в работе у Мартина; next — следующая в очереди.
STATUS = {
    'chem': {1: ('done', 'Комплект и 2 презентации готовы · ждёт проверки преподавателем'),
             2: ('done', 'Комплект и 2 презентации готовы · ждёт проверки преподавателем'),
             3: ('next', 'Следующая у Мартина'),
             4: ('queue', 'В очереди'), 5: ('queue', 'В очереди')},
    'bio': {1: ('work', 'Мартин делает сейчас (T15)'),
            2: ('queue', 'В очереди')},
}
# Видео по теме недели: (неделя У, название, площадка).
VIDEOS = {
    'chem': {1: [('Атомы кислорода в 3H₂SO₄', 'Reels')],
             4: [('49 г H₂SO₄ — сколько моль?', 'Reels'), ('Моль за 4 минуты', 'YouTube')],
             22: [('Формула по продуктам сгорания', 'Reels'), ('Химия на ЕНТ — не страшно', 'YouTube')]},
    'bio': {1: [('Нет ядра — нет ДНК?', 'Reels')],
            12: [('Хромосомы в яйцеклетке', 'Reels')],
            15: [('Два жёлтых гороха', 'Reels'), ('Генетика за 3 минуты', 'YouTube')]},
}
LABEL = {'done': 'Готово', 'work': 'В работе', 'next': 'Следующая', 'queue': 'В очереди', 'todo': 'Не начато'}
DAYS = {'chem': (0, 3), 'bio': (1, 4)}  # пн/чт и вт/пт от понедельника недели


def grid(md: str) -> list[dict]:
    sec = re.search(r'^## Календарная сетка[^\n]*\n(.*?)(?=^## )', md, re.S | re.M).group(1)
    rows = []
    for ln in sec.splitlines():
        if not ln.startswith('|') or '---' in ln or 'К / даты' in ln:
            continue
        c = [re.sub(r'\*\*', '', x.strip()) for x in ln.strip('|').split('|')]
        k, dates = c[0].split(' / ')
        rows.append({'k': int(k), 'dates': dates, 'u': c[1], 'l1': c[2], 'l2': c[3], 'res': c[4]})
    return rows


def monday(dates: str) -> dt.date:
    d, m = re.match(r'(\d\d)(?:\.(\d\d))?', dates).groups()
    if m is None:
        m = re.search(r'\.(\d\d)$', dates).group(1)
    mon = int(m)
    return dt.date(2026 if mon >= 9 else 2027, mon, int(d))


def cell(subj: str, row: dict) -> dict:
    u = row['u']
    base = {'subj': subj, 'u': u}
    if u.startswith('пауза'):
        return {**base, 'kind': 'pause', 'title': row['l1']}
    if u.startswith('резерв'):
        return {**base, 'kind': 'reserve', 'title': 'Резерв: ' + row['l1'][0].lower() + row['l1'][1:]}
    n = int(u.split(' / ')[0])
    lessons = u.split(' / ')[1]
    mock = 'пробник' in row['l1'].lower()
    st, note = STATUS[subj].get(n, ('todo', ''))
    first, *rest = row['l1'].split('; ')
    m = monday(row['dates'])
    d1, d2 = (m + dt.timedelta(days=x) for x in DAYS[subj])
    wd = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    return {**base, 'kind': 'mock' if mock else 'week', 'n': n, 'lessons': lessons, 'title': first[0].upper() + first[1:],
            'details': '; '.join(rest), 'practice': row['l2'], 'status': st, 'note': note,
            'when': f'{wd[d1.weekday()]} {d1.day}.{d1.month:02d} · {wd[d2.weekday()]} {d2.day}.{d2.month:02d}',
            'due': (m - dt.timedelta(days=7)).strftime('%d.%m'),
            'videos': VIDEOS[subj].get(n, [])}


def build() -> str:
    chem = grid((ROOT / 'course' / 'PROGRAM.md').read_text(encoding='utf-8'))
    bio = grid((ROOT / 'course' / 'biology' / 'PROGRAM.md').read_text(encoding='utf-8'))
    weeks = [{'k': c['k'], 'dates': c['dates'], 'chem': cell('chem', c), 'bio': cell('bio', b)} for c, b in zip(chem, bio)]
    data = json.dumps({'weeks': weeks, 'labels': LABEL, 'updated': UPDATED}, ensure_ascii=False)
    tpl = (Path(__file__).with_name('template.html')).read_text(encoding='utf-8')
    return tpl.replace('/*DATA*/null', data)


if __name__ == '__main__':
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'exports' / 'lesson-map.html'
    out.write_text(build(), encoding='utf-8')
    print(f'Lesson map -> {out}')
