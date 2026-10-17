"""Папка «Курс — для преподавателей» для Google Диска: программа, диагностика и все недели по порядку.

Запуск: .venv/Scripts/python tools/teacher_drive.py
Результат: «00 Материалы ХимБио просто/Курс — для преподавателей/» (эту папку целиком загружают на Google Диск).
Недели: Химия|Биология/«Неделя 01 — тема» — номер с нулём, чтобы на Диске порядок был 01, 02 … 10, а не 1, 10, 2.
Старые папки «Курс химии|биологии/Неделя N» переносятся сюда. Новые недели сразу пишет tools/build_week.py.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools' / 'handout')]

MATERIALS = ROOT / '00 Материалы ХимБио просто'
PACK = MATERIALS / 'Курс — для преподавателей'


def title(week: str) -> str:
    """Тема недели — из заголовка конспекта; символы, запрещённые в именах файлов Windows, убираются."""
    m = re.search(r'^title:\s*(.+)$', (ROOT / 'course' / week / 'notes-student.md').read_text(encoding='utf-8'), re.M)
    t = m.group(1).strip() if m else ''
    return re.sub(r'[<>:"/\\|?*]', '', t).rstrip('. ')


def week_dir(week: str) -> Path:
    """course/week-NN или course/biology/week-NN → папка недели в пакете для преподавателей."""
    n = int(week[-2:])
    subj = 'Биология' if week.startswith('biology') else 'Химия'
    t = title(week)
    return PACK / subj / (f'Неделя {n:02d} — {t}' if t else f'Неделя {n:02d}')


def migrate() -> None:
    for old_root, prefix in (('Курс химии', ''), ('Курс биологии', 'biology/')):
        base = MATERIALS / old_root
        if not base.exists():
            continue
        for d in sorted(base.glob('Неделя *')):
            new = week_dir(f'{prefix}week-{int(d.name.split()[1]):02d}')
            if new.exists():
                print(f'skip (exists): {new}')
                continue
            new.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), str(new))
            print(f'{d.relative_to(MATERIALS)} -> {new.relative_to(MATERIALS)}')
        if not any(base.iterdir()):
            base.rmdir()


def docs() -> None:
    import handout
    tmp = ROOT / 'exports' / 'teacher-drive'
    items = [
        ('course/teacher-pack/00-drive-start.md', '00 Начните здесь.pdf'),
        ('course/PROGRAM.md', '01 Программа — химия.pdf'),
        ('course/biology/PROGRAM.md', '02 Программа — биология.pdf'),
        ('course/diagnostic/student.md', '03 Входная диагностика/Химия — лист ученика.pdf'),
        ('course/diagnostic/teacher.md', '03 Входная диагностика/Химия — ключ и уровни.pdf'),
        ('course/biology/diagnostic/student.md', '03 Входная диагностика/Биология — лист ученика.pdf'),
        ('course/biology/diagnostic/teacher.md', '03 Входная диагностика/Биология — ключ и уровни.pdf'),
    ]
    for i, (src, name) in enumerate(items):
        pdf = tmp / f'{i:02d}.pdf'
        handout.main(src, str(pdf.relative_to(ROOT)))
        dest = PACK / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf, dest)


if __name__ == '__main__':
    PACK.mkdir(parents=True, exist_ok=True)
    migrate()
    docs()
    print(f'Pack -> {PACK}')
