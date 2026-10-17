"""Обложки YouTube 1280×720 для длинных видео (стиль 2). Запуск: .venv/Scripts/python tools/youtube/thumbs_wide.py [y009 …]"""
from __future__ import annotations

from pathlib import Path

from art import BASE, shot

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'deliverables' / 'youtube'

ITEMS = [
    ('y005', '#F13A43', 'ЕНТ · химия', 'Растворы', '3 задачи с ловушками', ['массовая доля', 'разбавление', 'избыток']),
    ('y006', '#F13A43', 'ЕНТ · химия', 'Хим. связь', '3 ловушки ЕНТ', ['вид связи', 'полярность CO₂', 'решётки']),
    ('y007', '#1F7A4A', 'ЕНТ · биология', 'Кровь', '3 ловушки ЕНТ', ['лёгочная артерия', 'круги', 'группы крови']),
    ('y008', '#1F7A4A', 'ЕНТ · биология', 'Иммунитет', 'и дыхание', ['вакцина', 'резус-конфликт', 'вдох']),
    ('y009', '#F13A43', 'ЕНТ · химия #01', 'Формула', 'как читать запись', ['индекс', 'коэффициент', 'заряд']),
    ('y010', '#F13A43', 'ЕНТ · химия #02', 'Валентность', '3 задачи с ловушками', ['формула', 'массовая доля', 'уравнение']),
    ('y011', '#1F7A4A', 'ЕНТ · биология #01', 'Клетка', '3 задачи с ловушками', ['структуры', 'тип клетки', 'размер по шкале']),
    ('y012', '#1F7A4A', 'ЕНТ · биология #02', 'ДНК', 'и вещества клетки', ['углеводы', 'Чаргафф', 'длина ДНК']),
]


def page(accent: str, tag: str, title: str, plaque: str, chips: list[str]) -> str:
    chips_html = ''.join(f'<div class="chip">{c}</div>' for c in chips)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
body {{ width: 1280px; height: 720px; background-size: 64px 64px; padding: 64px 72px; }}
.plaque {{ background: {accent}; padding: 10px 26px 16px; font-size: 56px; margin-top: 20px; }}
.tag {{ font: 800 30px 'Manrope'; letter-spacing: .14em; text-transform: uppercase; display: flex; align-items: center; gap: 12px; }}
.tag i {{ width: 16px; height: 16px; border-radius: 50%; background: {accent}; }}
h1 {{ margin: 40px 0 0; font: 800 104px/1 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; white-space: nowrap; }}
.chips {{ position: absolute; left: 72px; bottom: 70px; display: flex; gap: 14px; }}
.chip {{ border: 4px solid #F3F0E8; padding: 10px 20px; font: 800 30px 'Manrope'; text-transform: uppercase; white-space: nowrap; }}
.slash {{ position: absolute; top: -120px; bottom: -120px; right: 90px; width: 150px; background: {accent}; transform: skewX(-14deg); opacity: .9; }}
.q {{ position: absolute; right: 70px; top: 190px; font: 800 230px/1 'Unbounded'; color: #F3F0E8; transform: rotate(8deg); }}
</style></head><body><div class="slash"></div><div class="q">?</div>
<div class="tag"><i></i>ХИМБИО ПРОСТО · {tag}</div><h1>{title}</h1><div class="plaque">{plaque}</div>
<div class="chips">{chips_html}</div></body></html>"""


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    import sys
    only = set(sys.argv[1:])
    for vid, accent, tag, title, plaque, chips in ITEMS:
        if only and vid not in only:
            continue
        shot(page(accent, tag, title, plaque, chips), 1280, 720, OUT / f'thumb-{vid}.png')
        print(OUT / f'thumb-{vid}.png')
