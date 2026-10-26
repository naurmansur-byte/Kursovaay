"""Карусели «полезное» для Instagram (1080×1350, стиль 2): химия — лайфхаки к задачам, биология — ловушки ЕНТ.

Факты — из выжимок course/textbooks/*.md (недели 1–7). Запуск: .venv/Scripts/python tools/social/lifehacks.py
Результат: deliverables/instagram/lifehacks-chem/NN.png, deliverables/instagram/lifehacks-bio/NN.png.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools' / 'youtube')]
from art import BASE, shot  # noqa: E402

PAPER, MUTED = '#F3F0E8', '#B9B3A8'


def css(accent: str) -> str:
    return BASE + f"""
body {{ width: 1080px; height: 1350px; background-size: 72px 72px; font-family: 'Manrope'; padding: 72px 72px 0; }}
.plaque {{ background: {accent}; }}
.top {{ display: flex; justify-content: space-between; font: 800 26px 'Manrope'; letter-spacing: .14em; }}
.top span:first-child {{ display: flex; align-items: center; gap: 12px; }} .top i {{ width: 16px; height: 16px; border-radius: 50%; background: {accent}; }}
.top .n {{ color: {MUTED}; }}
.kicker {{ margin-top: 70px; padding: 12px 26px 16px; font-size: 34px; }}
h1 {{ margin: 40px 0 0; font: 800 100px/1.02 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }}
h2 {{ margin: 70px 0 0; font: 800 70px/1.05 'Unbounded'; text-transform: uppercase; letter-spacing: -.01em; }}
.lead {{ margin-top: 48px; font: 700 44px/1.35 'Manrope'; color: {MUTED}; }}
.card {{ margin-top: 60px; border: 4px solid {PAPER}; background: #1D1D1D; box-shadow: 14px 14px 0 {accent}; padding: 38px 42px; }}
.row {{ font: 700 46px/1.4 'Manrope'; padding: 10px 0 10px 26px; border-left: 10px solid #3A3A3A; margin-bottom: 18px; }}
.row.hot {{ border-left-color: {accent}; }}
.row b {{ color: #fff; }}
.f {{ font: 800 58px/1.3 'Manrope'; }}
.note {{ margin-top: 50px; font: 700 40px/1.4 'Manrope'; color: {MUTED}; }}
.note b {{ color: {accent}; }}
.num {{ position: absolute; right: 64px; bottom: 40px; font: 800 300px/1 'Unbounded'; color: rgba(243,240,232,.06); }}
.swipe {{ position: absolute; left: 72px; bottom: 64px; font: 800 30px 'Manrope'; letter-spacing: .12em; text-transform: uppercase; }}
.swipe b {{ color: {accent}; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 14px; margin-top: 46px; }}
.chip {{ border: 4px solid {PAPER}; padding: 10px 20px; font: 800 30px 'Manrope'; text-transform: uppercase; }}
.chip.hot {{ background: {accent}; border-color: {accent}; }}
.big {{ margin-top: 60px; font: 800 120px/1 'Unbounded'; }}
"""


def page(accent: str, subject: str, k: int, total: int, body: str) -> str:
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css(accent)}</style></head><body>'
            f'<div class="top"><span><i></i>ХИМБИО ПРОСТО · ЕНТ</span><span class="n">{subject} · {k}/{total}</span></div>{body}'
            f'<div class="num">{k:02d}</div></body></html>')


CHEM = ('#F13A43', 'ХИМИЯ', 'lifehacks-chem', [
    '<div class="plaque kicker">ЕНТ · химия</div><h1 style="font-size:86px">5 лайфхаков<br>к задачам<br>по химии</h1>'
    '<div class="lead">Правила, на которых теряют баллы чаще всего. Сохрани, чтобы проверять себя перед тестом.</div>'
    '<div class="swipe">листай <b>→</b></div>',
    '<h2>1. Всё через моль</h2><div class="card"><div class="row hot f">n = m / M</div><div class="row f">n = V / V<sub>m</sub></div>'
    '<div class="row f">n = N / N<sub>A</sub></div></div>'
    '<div class="note">Масса → <b>моль</b> → коэффициенты → <b>моль</b> → ответ. Сравнивают и переводят только моли.</div>',
    '<h2>2. Доля — на массу раствора</h2><div class="card"><div class="row hot f">ω = m(вещества) / m(раствора)</div>'
    '<div class="row">раствор = вещество + вода</div><div class="row">10 г соли + 90 г воды → <b>10 %</b>, а не 11,1 %</div></div>'
    '<div class="note">Долили воду — вещество то же, раствор больше. Упарили — раствор меньше.</div>',
    '<h2>3. Кто в недостатке</h2><div class="card"><div class="row f">2H<sub>2</sub> + O<sub>2</sub> → 2H<sub>2</sub>O</div>'
    '<div class="row">4 г H<sub>2</sub>: 2 моль → 2 / 2 = 1</div><div class="row hot">16 г O<sub>2</sub>: 0,5 моль → 0,5 / 1 = <b>0,5</b></div></div>'
    '<div class="note">Меньшая дробь — <b>O<sub>2</sub> в недостатке</b>, хотя масса водорода меньше. Продукт считают по недостатку.</div>',
    '<h2>4. Примеси и выход</h2><div class="card"><div class="row hot">m(чистого) = m(образца) × (1 − ω примесей)</div>'
    '<div class="row">m(практ.) = η × m(теор.)</div><div class="row">m(теор.) = m(практ.) / η</div></div>'
    '<div class="note">В уравнение — только <b>чистое</b> вещество. Выход считают к продукту, сначала — теоретический.</div>',
    '<h2>5. Проверь единицы</h2><div class="card"><div class="row hot">мл → л перед c = n / V</div>'
    '<div class="row">V<sub>m</sub> = 22,4 л/моль — только газы при н. у.</div><div class="row">M — г/моль, M<sub>r</sub> — без единиц</div>'
    '<div class="row">c — моль на литр <b>раствора</b>, не воды</div></div>',
    '<div class="plaque kicker">Курс «ХимБио просто»</div><h1>Разберём<br>с тобой</h1>'
    '<div class="lead">Химия и биология к ЕНТ в одном курсе — по учебникам из перечня НЦТ и в формате теста.</div>'
    '<div class="chips"><div class="chip">онлайн</div><div class="chip">химия + биология</div><div class="chip hot">старт 1 ноября</div></div>'
    '<div class="big">Пиши<br>«курс»</div><div class="note">в директ или в комментарии</div>',
])

BIO = ('#1F7A4A', 'БИОЛОГИЯ', 'lifehacks-bio', [
    '<div class="plaque kicker">ЕНТ · биология</div><h1 style="font-size:86px">6 ловушек<br>ЕНТ по<br>биологии</h1>'
    '<div class="lead">На них ошибаются даже те, кто учил. Сохрани и проверь себя.</div><div class="swipe">листай <b>→</b></div>',
    '<h2>1. Нет ядра ≠ нет ДНК</h2><div class="card"><div class="row">Бактерия — прокариот: <b>ядра нет</b></div>'
    '<div class="row hot">ДНК есть — кольцевая, в нуклеоиде</div><div class="row">Рибосомы тоже есть</div></div>',
    '<h2>2. АТФ: 2 + 36 = 38</h2><div class="card"><div class="row">Гликолиз, цитоплазма — <b>2 АТФ</b></div>'
    '<div class="row">Кислородный этап, митохондрии — <b>36 АТФ</b></div><div class="row hot f">Всего на глюкозу — 38</div></div>',
    '<h2>3. Артерия — от сердца</h2><div class="card"><div class="row hot">Лёгочная артерия — <b>венозная</b> кровь</div>'
    '<div class="row">Лёгочные вены — <b>артериальная</b> кровь</div></div>'
    '<div class="note">Артерию и вену различают по <b>направлению</b>, а не по крови.</div>',
    '<h2>4. Донор и реципиент</h2><div class="card"><div class="row hot">I группа — универсальный <b>донор</b></div>'
    '<div class="row">IV группа — универсальный <b>реципиент</b></div></div>'
    '<div class="note">Сейчас переливают <b>одногруппную</b> кровь.</div>',
    '<h2>5. Вакцина ≠ сыворотка</h2><div class="card"><div class="row">Вакцина — ослабленные или убитые микробы → <b>активный</b> иммунитет</div>'
    '<div class="row hot">Сыворотка — <b>готовые антитела</b> → пассивный, недолгий</div></div>',
    '<h2>6. Кислород — из воды</h2><div class="card"><div class="row hot">Кислород фотосинтеза — из <b>воды</b> (фотолиз)</div>'
    '<div class="row">CO<sub>2</sub> даёт углерод для глюкозы</div><div class="row">Световая фаза — тилакоиды, темновая — строма</div></div>',
    '<div class="plaque kicker">Курс «ХимБио просто»</div><h1>Разберём<br>с тобой</h1>'
    '<div class="lead">Химия и биология к ЕНТ в одном курсе — по учебникам из перечня НЦТ и в формате теста.</div>'
    '<div class="chips"><div class="chip">онлайн</div><div class="chip">химия + биология</div><div class="chip hot">старт 1 ноября</div></div>'
    '<div class="big">Пиши<br>«курс»</div><div class="note">в директ или в комментарии</div>',
])

if __name__ == '__main__':
    for accent, subject, folder, slides in (CHEM, BIO):
        out = ROOT / 'deliverables' / 'instagram' / folder
        out.mkdir(parents=True, exist_ok=True)
        for k, body in enumerate(slides, 1):
            shot(page(accent, subject, k, len(slides), body), 1080, 1350, out / f'{k:02d}.png')
        print(out, len(slides))
