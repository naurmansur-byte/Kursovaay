"""Сборка учебных пробников (недели 24–25) в папку материалов.

Ученику: бланк (PDF под телефон) и карта ошибок (PDF). Преподавателю: план уроков, ключ и разбор (DOCX).
Запуск из корня: .venv/Scripts/python tools/build_mock.py chem-1 bio-1 chem-2 bio-2
Результат: exports/mocks/<пробник>/ и копия в «00 Материалы ХимБио просто/Курс — для преподавателей/Химия|Биология/Неделя 24|25 — Учебный пробник N/».
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools' / 'handout'), str(ROOT / 'tools')]
import handout  # noqa: E402
from export_lesson_kit import export_docx  # noqa: E402

PACK = ROOT / '00 Материалы ХимБио просто' / 'Курс — для преподавателей'
STUDENT = [('test', '1 Бланк пробника'), ('error-map', '2 Карта ошибок')]
TEACHER = [('lesson-plan', 'Уроки {a}–{b} — план'), ('key', 'Ключ'), ('solutions', 'Разбор')]


def build(mock: str) -> Path:
    src, out = ROOT / 'course' / 'mocks' / mock, ROOT / 'exports' / 'mocks' / mock
    n = int(mock[-1])
    week, (a, b) = (24, (47, 48)) if n == 1 else (25, (49, 50))
    dest = PACK / ('Биология' if mock.startswith('bio') else 'Химия') / f'Неделя {week} — Учебный пробник {n}'
    for sub in ('Ученику', 'Преподавателю'):
        (dest / sub).mkdir(parents=True, exist_ok=True)
    for name, title in STUDENT:
        md = src / f'{name}.md'
        pdf = out / 'student' / f'{name}.pdf'
        handout.main(str(md.relative_to(ROOT)), str(pdf.relative_to(ROOT)))
        shutil.copy2(pdf, dest / 'Ученику' / f'{title}.pdf')
    for name, title in TEACHER:
        docx = out / 'teacher' / f'{name}.docx'
        docx.parent.mkdir(parents=True, exist_ok=True)
        export_docx((src / f'{name}.md').read_text(encoding='utf-8'), docx, base=src)
        shutil.copy2(docx, dest / 'Преподавателю' / f'{title.format(a=a, b=b)}.docx')
    print(f'Mock {mock} -> {dest}')
    return dest


if __name__ == '__main__':
    for m in sys.argv[1:]:
        if not re.fullmatch(r'(chem|bio)-[12]', m):
            sys.exit(f'неизвестный пробник: {m}')
        build(m)
