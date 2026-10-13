"""Памятка недели «ХимБио просто»: course/week-NN/memo.md -> карточки 1080×1920 (PNG) + PDF.

Разметка: `# Заголовок карточки`; строки `= крупно`, `- пункт`, `! ловушка`, `> примечание`, `**жирное**`.
Запуск: .venv/Scripts/python tools/memo/memo.py week-01   (результат: exports/week-01/memo/*.png и memo.pdf)
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / 'tools' / 'handout'), str(ROOT / 'tools' / 'slides')]
from handout import chrome, front_matter  # noqa: E402
from slides import ATOM, inline  # noqa: E402


def cards(text: str) -> tuple[dict, list[tuple[str, list[str]]]]:
    meta, body = front_matter(text)
    out: list[tuple[str, list[str]]] = []
    for line in body.splitlines():
        if line.startswith('# '):
            out.append((line[2:].strip(), []))
        elif line.strip() and out:
            out[-1][1].append(line.strip())
    return meta, out


def card_html(css: str, meta: dict, k: int, total: int, title: str, lines: list[str]) -> str:
    items = []
    for ln in lines:
        mark, rest = ln[:1], ln[1:].strip()
        if mark == '=':
            size = 'xs' if len(rest) > 30 else 's' if len(rest) > 20 else ''
            items.append(f'<div class="big {size}">{inline(rest)}</div>')
        elif mark == '-':
            items.append(f'<div class="item"><i></i><span>{inline(rest)}</span></div>')
        elif mark == '!':
            items.append(f'<div class="trap"><b>Ловушка</b>{inline(rest)}</div>')
        elif mark == '>':
            items.append(f'<div class="note">{inline(rest)}</div>')
        else:
            items.append(f'<p>{inline(ln)}</p>')
    counter = f'{k}/{total}' if total > 1 else ''
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{css}</style></head><body>'
            f'<div class="top"><span><i></i>ХИМБИО ПРОСТО · ЕНТ</span><span>{counter}</span></div>'
            f'<div class="plaque">Памятка · неделя {meta.get("week", "")}</div>'
            f'<h1>{inline(title)}</h1><div class="list">{"".join(items)}</div>'
            f'<div class="foot">{ATOM}<span>@himbio.prosto<br><small>сохрани, чтобы повторить перед пробником</small></span></div>'
            f'</body></html>')


def build(week: str) -> None:
    meta, items = cards((ROOT / 'course' / week / 'memo.md').read_text(encoding='utf-8'))
    css = (HERE / 'memo.css').read_text(encoding='utf-8').replace('{{FONTS}}', (ROOT / 'content/brand/fonts').as_uri())
    out = ROOT / 'exports' / week / 'memo'
    out.mkdir(parents=True, exist_ok=True)
    browser = chrome()
    pngs = []
    with tempfile.TemporaryDirectory() as tmp:
        for k, (title, lines) in enumerate(items, 1):
            page = Path(tmp) / f'card{k}.html'
            page.write_text(card_html(css, meta, k, len(items), title, lines), encoding='utf-8')
            png = out / f'memo-{k}.png'
            subprocess.run([browser, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                            '--window-size=1080,1920', f'--screenshot={png}', page.as_uri()], check=True, capture_output=True, timeout=120)
            pngs.append(png)
        doc = Path(tmp) / 'all.html'
        doc.write_text('<!doctype html><html><head><meta charset="utf-8"><style>@page{size:1080px 1920px;margin:0}body{margin:0}'
                       'img{display:block;width:1080px;height:1920px;break-after:page}</style></head><body>'
                       + ''.join(f'<img src="{p.as_uri()}">' for p in pngs) + '</body></html>', encoding='utf-8')
        subprocess.run([browser, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out.parent / "memo.pdf"}',
                        doc.as_uri()], check=True, capture_output=True, timeout=120)
    print(f'Memo: {len(pngs)} cards -> {out}, memo.pdf')


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'week-01')
