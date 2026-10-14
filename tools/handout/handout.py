"""Раздатка «ХимБио просто»: Markdown урока -> оформленный PDF (стиль 2, светлая печатная версия).

Разметка (см. docs/STYLE.md, раздел «Разметка для раздаток»):
  front matter:  ---\\nweek: 1\\ntitle: ...\\nsubtitle: ...\\n---
  блоки:         > [!rule] Запомни / > [!trap] Ловушка / > [!example] Разберём / > [!try] Попробуй
Запуск: .venv/Scripts/python tools/handout/handout.py course/week-01/notes-student.md exports/week-01/student/notes-student.pdf
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LABELS = {'rule': 'Запомни', 'trap': 'Ловушка', 'example': 'Разберём', 'try': 'Попробуй'}


def front_matter(text: str) -> tuple[dict, str]:
    meta = {}
    if text.startswith('---'):
        head, _, text = text[3:].partition('\n---')
        for line in head.strip().splitlines():
            key, _, value = line.partition(':')
            meta[key.strip()] = value.strip()
        text = text.lstrip('\n')
    return meta, text


def callouts(text: str) -> str:
    """> [!type] Заголовок + строки '>' -> <div class="callout type"> с Markdown внутри."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        m = re.match(r'^>\s*\[!(\w+)\]\s*(.*)$', lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        kind, title = m.group(1), m.group(2) or LABELS.get(m.group(1), '')
        body = []
        i += 1
        while i < len(lines) and lines[i].startswith('>'):
            body.append(re.sub(r'^>\s?', '', lines[i]))
            i += 1
        inner = '\n'.join(body)
        out += [f'<div class="callout {kind}" markdown="1">', f'<div class="callout-title">{title}</div>', '', inner, '', '</div>', '']
    return '\n'.join(out)


def build_html(src: Path, text: str | None = None) -> str:
    """text — готовый Markdown вместо файла (например, контроль без ключа); рисунки всё равно ищутся от папки src."""
    meta, body = front_matter(src.read_text(encoding='utf-8') if text is None else text)
    body = re.sub(r'^# .*\n', '', body, count=1)  # заголовок рисует шапка
    html = markdown.markdown(callouts(body), extensions=['tables', 'md_in_html', 'sane_lists', 'nl2br'])

    def pic(m: re.Match) -> str:  # рисунки: путь от папки .md; если файла ещё нет — рамка с описанием
        f = (src.parent / m.group(2)).resolve()
        return f'<img class="pic" src="{f.as_uri()}" alt="">' if f.exists() else f'<span class="pic-missing">Рисунок: {m.group(1)}</span>'
    html = re.sub(r'<img alt="([^"]*)" src="(?![a-z]+:)([^"]+)"\s*/?>', pic, html)
    css =(HERE / 'handout.css').read_text(encoding='utf-8').replace('{{FONTS}}', (ROOT / 'content/brand/fonts').as_uri())
    week = meta.get('week', '')
    label = meta.get('label') or f'Неделя {week}'  # label: своя плашка и подпись страницы вместо «Неделя N»
    # format: phone — узкая страница под экран телефона, крупный текст (ДЗ, памятки).
    phone = ('<style>@page { size: 90mm 160mm; margin: 6mm 5mm 9mm; @bottom-left { content: none; } }'
             'body { font-size: 11pt; } h1 { font-size: 17pt; } h2 { font-size: 11.5pt; margin-top: 6mm; }'
             '.cover { padding-bottom: 4mm; } .plaque { margin-top: 4mm; font-size: 9pt; } table { font-size: 9pt; }'
             '.callout { padding: 3.5mm 4mm 2mm; }</style>') if meta.get('format') == 'phone' else ''
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<style>{css}</style><style>@page {{ @bottom-left {{ content: "ХимБио просто · {label.lower()}"; }} }}</style>{phone}</head><body>
<header class="cover">
  <div class="brand"><span class="dot"></span>ХИМБИО ПРОСТО · ЕНТ</div>
  <div class="plaque">{label}</div>
  <h1>{meta.get("title", "")}</h1>
  <p class="subtitle">{meta.get("subtitle", "")}</p>
</header>
<main>{html}</main></body></html>'''


def chrome() -> str:
    for p in [r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
              r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', shutil.which('chromium') or '', shutil.which('google-chrome') or '']:
        if p and Path(p).exists():
            return p
    raise RuntimeError('Chrome/Edge not found for PDF printing')


def main(src: str, pdf: str, text: str | None = None) -> None:
    src_path, pdf_path = (ROOT / src).resolve(), (ROOT / pdf).resolve()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = pdf_path.with_suffix('.html')
    html_path.write_text(build_html(src_path, text), encoding='utf-8')
    subprocess.run([chrome(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf_path}', html_path.as_uri()],
                   check=True, capture_output=True, timeout=120)
    print(f'PDF: {pdf_path} ({pdf_path.stat().st_size // 1024} KB), HTML: {html_path.name}')


if __name__ == '__main__':
    main(*sys.argv[1:3])
