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
    # 20.11.2026: без нумерации в названиях (Мансур)
    ('y013', '#F13A43', 'ЕНТ · химия', '<span style="font-size:78px">Классы веществ</span>', '5 задач с ловушками', ['оксиды', 'индикаторы', 'соли']),
    ('y014', '#1F7A4A', 'ЕНТ · биология', 'Мембрана', 'и ферменты · 5 задач', ['осмос', 'насос', 'фермент']),
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


# Светлые обложки разборов пробников ЕНТ (Мансур 20.11.2026: разборы — светлый стиль).
LIGHT = [
    ('z001', '#E2333C', 'РАЗБОР ЕНТ · ХИМИЯ', 'Разбор ЕНТ', 'химия · 10 заданий', ['решение', 'ловушки', 'пауза — реши сам']),
]


def page_light(accent: str, tag: str, title: str, plaque: str, chips: list[str]) -> str:
    chips_html = ''.join(f'<div class="chip">{c}</div>' for c in chips)
    opts = ''.join(f'<div class="o{" ok" if l == "B" else ""}"><b>{l})</b>{"✓" if l == "B" else ""}</div>' for l in 'ABCD')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
body {{ width: 1280px; height: 720px; padding: 64px 72px; background: #F6F4EE; color: #161616;
       background-image: linear-gradient(rgba(22,22,22,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(22,22,22,.07) 1px, transparent 1px); background-size: 64px 64px; }}
.tag {{ font: 800 30px 'Manrope'; letter-spacing: .14em; display: flex; align-items: center; gap: 12px; color: #161616; }}
.tag i {{ width: 16px; height: 16px; border-radius: 50%; background: {accent}; }}
h1 {{ margin: 40px 0 0; font: 800 94px/1 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; white-space: nowrap; color: #161616; }}
.pl {{ display: inline-block; margin-top: 22px; background: {accent}; color: #fff; padding: 10px 26px 16px; font: 800 52px 'Unbounded'; text-transform: uppercase; transform: rotate(-2deg); }}
.chips {{ position: absolute; left: 72px; bottom: 70px; display: flex; gap: 14px; }}
.chip {{ border: 4px solid #161616; padding: 10px 20px; font: 800 30px 'Manrope'; text-transform: uppercase; white-space: nowrap; background: #fff; }}
.card {{ position: absolute; right: 60px; top: 190px; width: 270px; background: #fff; box-shadow: 0 18px 40px rgba(0,0,0,.14); padding: 26px 30px; transform: rotate(5deg); }}
.o {{ display: flex; justify-content: space-between; font: 400 54px 'Times New Roman', serif; padding: 4px 12px; color: #161616; }}
.o.ok {{ background: #D9F1E1; border-left: 10px solid #1F7A4A; color: #1F7A4A; font-weight: 700; }}
</style></head><body>
<div class="tag"><i></i>ХИМБИО ПРОСТО · {tag}</div><h1>{title}</h1><div class="pl">{plaque}</div>
<div class="card">{opts}</div><div class="chips">{chips_html}</div></body></html>"""


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    import sys
    only = set(sys.argv[1:])
    for vid, accent, tag, title, plaque, chips in ITEMS:
        if only and vid not in only:
            continue
        shot(page(accent, tag, title, plaque, chips), 1280, 720, OUT / f'thumb-{vid}.png')
        print(OUT / f'thumb-{vid}.png')
    for vid, accent, tag, title, plaque, chips in LIGHT:
        if only and vid not in only:
            continue
        shot(page_light(accent, tag, title, plaque, chips), 1280, 720, OUT / f'thumb-{vid}.png')
        print(OUT / f'thumb-{vid}.png')
