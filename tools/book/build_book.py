"""Книги «Конспект ЕНТ: химия» и «Конспект ЕНТ: биология» — PDF из готовых комплектов недель 1–23.

Глава = неделя: конспект ученика (notes-student.md) без ссылок на уроки и ДЗ, памятка (memo.md),
«Что легко перепутать» из выжимки недели (course/textbooks/*-NN-*.md). В конце — ошибки учебников из ERRATA.md
(основная таблица, без колонки «Как проверено»).
Запуск: .venv/Scripts/python.exe -I tools/book/build_book.py chem bio
Результат: «00 Материалы ХимБио просто/Конспект ЕНТ/Конспект ЕНТ — химия.pdf» (и биология).
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from datetime import date
from html import escape
from pathlib import Path

import markdown
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools' / 'handout')]
from handout import callouts, chrome, front_matter  # noqa: E402

OUT = ROOT / '00 Материалы ХимБио просто' / 'Конспект ЕНТ'
CACHE = ROOT / 'exports' / 'book' / 'pics'
WEEKS = range(1, 24)
SUBJ = {
    'chem': dict(name='химия', title='Конспект ЕНТ: химия', src=ROOT / 'course', digest='chem', book='Химия', accent='#F13A43',
                 books='Химия 7–11 класс (Оспанова, Аухадиева, Белоусова; Мектеп)'),
    'bio': dict(name='биология', title='Конспект ЕНТ: биология', src=ROOT / 'course' / 'biology', digest='bio', book='Биология', accent='#1F7A4A',
                books='Биология 7–11 класс (Мектеп и Атамұра)'),
}
ROUTING = re.compile(r'^(После урока \d+|Теперь выполни|Выполни \[|Выполни закрепление|Ключи открывай)|pre-work\.md|homework\.md', re.M)
MD = ['tables', 'md_in_html', 'sane_lists', 'nl2br']
SERVICE = re.compile(r'выжимк|Макс|Мартин|\bT\d\d\b|комплект недели|не давать|не брать|не включаем|в задания|в заданиях курса')


def pic_uri(path: Path) -> str:
    """Рисунок — в JPEG шириной до 1400 px (кэш), чтобы книга весила десятки, а не сотни мегабайт."""
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.md5(f'{path}{path.stat().st_mtime}'.encode()).hexdigest()[:12]
    out = CACHE / f'{path.stem}-{key}.jpg'
    if not out.exists():
        im = Image.open(path).convert('RGB')
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(out, 'JPEG', quality=86, optimize=True)
    return out.as_uri()


def drop_callouts(body: str, title_re: str) -> str:
    out, skip = [], False
    for line in body.splitlines():
        if re.match(rf'^>\s*\[!\w+\]\s*({title_re})', line):
            skip = True
            continue
        if skip and line.startswith('>'):
            continue
        skip = False
        out.append(line)
    return '\n'.join(out)


def notes(week_dir: Path) -> tuple[dict, str]:
    meta, body = front_matter((week_dir / 'notes-student.md').read_text(encoding='utf-8'))
    body = re.sub(r'^# .*\n', '', body, count=1)
    body = ''.join(p for p in re.split(r'(?m)^(?=## )', body) if not p.startswith('## Перед уроком'))
    body = re.sub(r'(?m)^(## .*?)\s+—\s+после урока \d+\s*$', r'\1', body)
    body = drop_callouts(body, r'Перед уроком|После урока')
    body = '\n\n'.join(p for p in re.split(r'\n\s*\n', body) if not ROUTING.search(p))
    body = re.sub(r'\[([^\]]+)\]\([^)]+\.md\)', r'\1', body)
    html = markdown.markdown(callouts(body), extensions=MD)

    def pic(m: re.Match) -> str:
        f = (week_dir / m.group(2)).resolve()
        return f'<img class="pic" src="{pic_uri(f)}" alt="{m.group(1)}">' if f.exists() else ''
    return meta, re.sub(r'<img alt="([^"]*)" src="(?![a-z]+:)([^"]+)"\s*/?>', pic, html)


def inline(s: str) -> str:
    return markdown.markdown(s).removeprefix('<p>').removesuffix('</p>')


def memo(week_dir: Path, skip_facts: bool) -> str:
    f = week_dir / 'memo.md'
    if not f.exists():
        return ''
    _, body = front_matter(f.read_text(encoding='utf-8'))
    cards = []
    for block in re.split(r'(?m)^# ', body)[1:]:
        title, *lines = block.strip().splitlines()
        if skip_facts and title.startswith('Факты ЕНТ'):
            continue
        items, keys, warns = [], [], []
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                items.append(f'<li>{inline(line[2:])}</li>')
            elif line.startswith('= '):
                keys.append(f'<p class="key">{inline(line[2:])}</p>')
            elif line.startswith('! '):
                warns.append(f'<p class="warn">{inline(line[2:])}</p>')
        cards.append(f'<div class="mcard"><h4>{escape(title)}</h4>{"<ul>" + "".join(items) + "</ul>" if items else ""}{"".join(keys)}{"".join(warns)}</div>')
    return f'<div class="block-title">Памятка недели</div><div class="memo">{"".join(cards)}</div>' if cards else ''


def traps(prefix: str, n: int) -> str:
    files = sorted((ROOT / 'course' / 'textbooks').glob(f'{prefix}-{n:02d}-*.md'))
    if not files:
        return ''
    text = files[0].read_text(encoding='utf-8')
    m = re.search(r'(?ms)^## Что легко перепутать[^\n]*\n(.*?)(?=^## |\Z)', text)
    if not m or not m.group(1).strip():
        return ''
    return ('<div class="callout trap mix"><div class="callout-title">Что легко перепутать</div>'
            + markdown.markdown(m.group(1).strip(), extensions=MD) + '</div>')


def errata(book: str) -> str:
    lines = (ROOT / 'course' / 'textbooks' / 'ERRATA.md').read_text(encoding='utf-8').splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith('| Учебник'))
    rows, current = [], ''
    for line in lines[start + 2:]:
        if not line.startswith('|'):
            break
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 4:
            continue
        current = current if cells[0].lower().startswith('то же') else cells[0]
        if current.startswith(book):
            right = ' '.join(x for x in re.split(r'(?<=[.;])\s+', cells[3]) if not SERVICE.search(x))
            rows.append((re.sub(r'\s*\(.*?\)', '', current).strip(), cells[1], cells[2], right))

    def order(row):
        cls, part = re.search(r'(\d+)', row[0]), re.search(r'ч\. (\d)', row[0])
        return (int(cls.group(1)) if cls else 0, int(part.group(1)) if part else 0)
    rows.sort(key=order)
    out, last = [], None
    for b, where, wrong, right in rows:
        if b != last:
            if last:
                out.append('</tbody></table>')
            out.append(f'<h3 class="eb">{escape(b)}</h3><table class="err"><thead><tr><th>Где</th><th>В учебнике</th><th>Как правильно</th></tr></thead><tbody>')
            last = b
        out.append(f'<tr><td>{inline(where)}</td><td>{inline(wrong)}</td><td>{inline(right)}</td></tr>')
    if last:
        out.append('</tbody></table>')
    return ''.join(out), len(rows)


BOOK_CSS = """
@page { @bottom-left { content: "ХимБио просто · {TITLE}"; } }
@page :first { @bottom-left { content: none; } @bottom-right { content: none; } }
:root { --accent: {ACCENT}; }
.book-cover { height: 255mm; display: flex; flex-direction: column; justify-content: space-between; padding: 6mm 0 0; break-after: page; }
.book-cover h1 { font-size: 40pt; max-width: none; margin-top: 30mm; }
.book-cover .lead { font-size: 13pt; color: var(--muted); max-width: 140mm; font-weight: 600; }
.book-cover .bar { height: 9mm; background: var(--accent); transform: rotate(-1.5deg); margin: 6mm 0 10mm; width: 70%; }
.book-cover .colophon { font-size: 9pt; color: var(--muted); border-top: 2px solid var(--ink); padding-top: 4mm; }
.toc { break-after: page; }
.toc h2::before, .errata > h2::before { background: var(--accent); }
.toc ol { list-style: none; padding: 0; margin: 4mm 0 0; display: grid; gap: 1.6mm; }
.toc ol li { display: grid; grid-template-columns: 22mm 1fr; font-size: 10.5pt; border-bottom: 1px solid var(--line); padding-bottom: 1.4mm; }
.toc ol li b { font-family: 'Unbounded', sans-serif; font-size: 9pt; color: var(--accent); }
.howto { margin-top: 8mm; }
.chapter { break-before: page; }
.ch-head { border-bottom: 2.5px solid var(--ink); padding-bottom: 5mm; margin-bottom: 5mm; }
.ch-head .plaque { background: var(--accent); margin-top: 0; transform: none; }
.ch-head .ch-title { margin: 4mm 0 0; font: 800 21pt/1.1 'Unbounded', sans-serif; text-transform: uppercase; letter-spacing: -.01em; }
.block-title { margin: 9mm 0 3mm; font: 800 13.5pt/1.2 'Unbounded', sans-serif; text-transform: uppercase; color: var(--accent); break-after: avoid; }
.memo { display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm; }
.mcard { border: 1.5px solid var(--ink); padding: 3.5mm 4mm 2mm; break-inside: avoid; font-size: 9.4pt; }
.mcard h4 { margin: 0 0 2mm; font: 800 9pt/1.25 'Unbounded', sans-serif; text-transform: uppercase; }
.mcard ul { padding-left: 4.5mm; margin-bottom: 2mm; }
.mcard .key { background: var(--tint); padding: 1.5mm 2.5mm; font-weight: 700; margin-bottom: 1.6mm; }
.mcard .warn { color: var(--accent); font-weight: 700; margin-bottom: 1.6mm; }
.mix { break-inside: auto; }
.mix ul { margin-bottom: 1mm; }
.errata { break-before: page; }
.errata .intro { color: var(--muted); }
h3.eb { margin: 6mm 0 2mm; font: 800 10pt/1.3 'Manrope', sans-serif; break-after: avoid; }
table.err { font-size: 8.6pt; break-inside: auto; }
table.err td:first-child { width: 22mm; font-weight: 700; }
table.err td:nth-child(2) { width: 42%; }
table.err tr { break-inside: avoid; }
"""


def build(key: str) -> Path:
    s = SUBJ[key]
    chapters, toc = [], []
    for n in WEEKS:
        wd = s['src'] / f'week-{n:02d}'
        meta, body = notes(wd)
        title = meta.get('title', f'Неделя {n}')
        has_facts = 'Факты ЕНТ недели' in body
        toc.append(f'<li><b>Неделя {n}</b><span>{escape(title)}</span></li>')
        chapters.append(f'<section class="chapter"><div class="ch-head"><div class="plaque">Неделя {n}</div>'
                        f'<div class="ch-title">{escape(title)}</div></div>{body}{memo(wd, has_facts)}{traps(s["digest"], n)}</section>')
    err_html, n_err = errata(s['book'])
    today = date.today().strftime('%d.%m.%Y')
    css = ((ROOT / 'tools' / 'handout' / 'handout.css').read_text(encoding='utf-8').replace('{{FONTS}}', (ROOT / 'content/brand/fonts').as_uri())
           + BOOK_CSS.replace('{TITLE}', s['title'].lower()).replace('{ACCENT}', s['accent']))
    html = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{s['title']}</title><style>{css}</style></head><body>
<section class="book-cover">
  <div><div class="brand"><span class="dot"></span>ХИМБИО ПРОСТО · ПОДГОТОВКА К ЕНТ</div>
  <h1>{s['title']}</h1><div class="bar"></div>
  <p class="lead">23 недели курса в одной книге: конспекты, памятки, факты ЕНТ и типичные ловушки. По учебникам из перечня НЦТ: {s['books']}.</p></div>
  <div class="colophon">Пособие для учеников курса «ХимБио просто». Версия от {today}; материалы проверяются преподавателем курса. Задания и рисунки — авторские; текст учебников не воспроизводится, указаны страницы для сверки.</div>
</section>
<section class="toc"><h2>Содержание</h2><ol>{''.join(toc)}<li><b>Конец</b><span>Ошибки школьных учебников и как правильно</span></li></ol>
<div class="howto"><h2>Как пользоваться</h2><ul>
<li>Одна глава — одна неделя курса. Сначала конспект, затем памятка и «Что легко перепутать».</li>
<li>Блоки «Запомни» — правила и формулы, «Ловушка» — частые ошибки, «Разберём» — решённые примеры, «Проверь себя» — вопросы для самопроверки.</li>
<li>«Факты ЕНТ недели» — то, что спрашивают на экзамене дословно: имена, даты, числа, названия.</li>
<li>В ссылках вида «Х10-1 с. 6» или «Б9 § 12» — учебник из перечня НЦТ, класс, часть и страница. В конце книги — ошибки этих учебников и верные формулировки.</li>
</ul></div></section>
{''.join(chapters)}
<section class="errata"><h2>Ошибки школьных учебников и как правильно</h2>
<p class="intro">В учебниках из перечня НЦТ встречаются опечатки, неверные ответы задач и устаревшие числа. Ниже — {n_err} мест, которые мы нашли при подготовке курса, и как правильно. На ЕНТ опирайся на верную формулировку.</p>
{err_html}</section>
</body></html>"""
    tmp = ROOT / 'exports' / 'book' / f'{key}.html'
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(html, encoding='utf-8')
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = OUT / f'Конспект ЕНТ — {s["name"]}.pdf'
    subprocess.run([chrome(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', tmp.as_uri()],
                   check=True, capture_output=True, timeout=900)
    print(f'{pdf} ({pdf.stat().st_size // 1024 // 1024} MB), ошибок учебников: {n_err}')
    return pdf


if __name__ == '__main__':
    for k in sys.argv[1:] or ['chem', 'bio']:
        build(k)
