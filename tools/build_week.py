"""Сборка недели целиком (новый формат комплекта) с рисунками pics/*.png — и раскладка в папку материалов.

Презентации уроков (PPTX + PDF), раздатки ученику (PDF), материалы преподавателю (DOCX), памятка (PNG).
Запуск из корня: .venv/Scripts/python tools/build_week.py biology/week-01      (химия: week-04)
Результат: exports/<неделя>/ и копия в «00 Материалы ХимБио просто/Курс — для преподавателей/Химия|Биология/Неделя NN — тема/».
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools' / d) for d in ('handout', 'slides', 'memo')] + [str(ROOT / 'tools')]
import handout  # noqa: E402
import lesson_deck  # noqa: E402
import memo  # noqa: E402
from export_lesson_kit import export_docx  # noqa: E402
from teacher_drive import week_dir  # noqa: E402

MATERIALS = ROOT / '00 Материалы ХимБио просто'
KEY = re.compile(r'^## (?:Ключ|Для преподавателя|Преподавател|Только преподавателю)', re.M)
STUDENT = [('notes-student', '1 Конспект'), ('pre-work', '2 Закрепление после урока 1'), ('homework', '3 Домашняя работа'),
           ('quiz', '4 Контроль (урок 2)'), ('calc-track', '5 Расчётный трек')]
TEACHER = [('lesson-1-plan', 'Урок 1 — план'), ('lesson-2-plan', 'Урок 2 — план'), ('homework-solutions', 'ДЗ — решения и критерии'),
           ('teacher-notes', 'Заметки преподавателю'), ('quiz', 'Контроль — с ключом'),
           ('calc-track-solutions', 'Расчётный трек — решения')]


def build(week: str) -> Path:
    src, out = ROOT / 'course' / week, ROOT / 'exports' / week
    n = int(week[-2:])
    dest = week_dir(week)
    for sub in ('Ученику', 'Преподавателю'):
        (dest / sub).mkdir(parents=True, exist_ok=True)

    for k in (1, 2):
        lesson_deck.main([week, str(k)])
        for ext in ('pdf', 'pptx'):
            shutil.copy2(out / f'lesson-{k}-slides.{ext}', dest / f'Урок {k} — презентация.{ext}')

    for name, title in STUDENT:
        md = src / f'{name}.md'
        if not md.exists():  # расчётный трек есть только в неделях 6–22 химии
            continue
        text = md.read_text(encoding='utf-8')
        cut = KEY.search(text) if name == 'quiz' else None
        pdf = out / 'student' / f'{name}.pdf'
        handout.main(str(md.relative_to(ROOT)), str(pdf.relative_to(ROOT)), text[:cut.start()] if cut else None)
        shutil.copy2(pdf, dest / 'Ученику' / f'{title}.pdf')

    for name, title in TEACHER:
        if not (src / f'{name}.md').exists():
            continue
        docx = out / 'teacher' / f'{name}.docx'
        export_docx((src / f'{name}.md').read_text(encoding='utf-8'), docx, base=src)
        shutil.copy2(docx, dest / 'Преподавателю' / f'{title}.docx')

    memo.build(week)
    for png in sorted((out / 'memo').glob('memo-*.png')):
        shutil.copy2(png, dest / 'Ученику' / f'Памятка {png.stem.split("-")[1]}.png')
    print(f'Week {week} -> {dest}')
    return dest


if __name__ == '__main__':
    for w in sys.argv[1:]:
        build(w)
