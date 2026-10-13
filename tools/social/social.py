"""Заготовки для соцсетей в стиле 2: шаблоны сторис, пост для таргета, карусель для Threads (Chrome-скриншоты HTML).

Запуск: .venv/Scripts/python tools/social/social.py
Результат: deliverables/stories/*.png, deliverables/ads/*.png, deliverables/threads/*.png
Сторис: всё важное в зоне 250–1580 px по высоте (сверху профиль, снизу строка ответа Instagram).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools' / 'youtube')]
from art import ATOM, BASE, shot  # noqa: E402

CSS = BASE + """
body { background-size: 72px 72px; font-family: 'Manrope'; }
.tag { position: absolute; left: 80px; font: 800 30px 'Manrope'; letter-spacing: .14em; display: flex; align-items: center; gap: 14px; }
.tag i { width: 16px; height: 16px; border-radius: 50%; background: #F13A43; }
.plaque { padding: .1em .26em .16em; }
.big { font: 800 112px/1.02 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; margin: 0; }
.card { background: #1D1D1D; border: 4px solid #F3F0E8; box-shadow: 16px 16px 0 #F3F0E8; }
.muted { color: #B9B3A8; }
.chips { display: flex; flex-wrap: wrap; gap: 16px; }
.chip { border: 4px solid #F3F0E8; padding: 12px 24px; font: 800 34px 'Manrope'; text-transform: uppercase; white-space: nowrap; }
.chip.red { background: #F13A43; border-color: #F13A43; }
.slash { position: absolute; width: 150px; background: #F13A43; transform: skewX(-14deg); }
.atom { position: absolute; }
"""


def dna(w: int = 200, h: int = 420) -> str:
    """Спираль ДНК: две нити и перекладины."""
    turns, amp, cx = 1.6, w * 0.36, w / 2
    ys = [k * h / 80 for k in range(81)]
    x = lambda y, s: cx + s * amp * math.sin(2 * math.pi * turns * y / h)  # noqa: E731
    strand = lambda s: 'M' + ' L'.join(f'{x(y, s):.1f} {y:.1f}' for y in ys)  # noqa: E731
    rungs = ''.join(f'<line x1="{x(y, 1):.1f}" y1="{y:.1f}" x2="{x(y, -1):.1f}" y2="{y:.1f}" stroke="{"#F13A43" if k % 2 else "#F3F0E8"}" stroke-width="8" opacity=".85"/>'
                    for k, y in enumerate(ys[3::6]))
    return (f'<svg class="dna" viewBox="-10 -10 {w + 20} {h + 20}">{rungs}'
            f'<path d="{strand(1)}" fill="none" stroke="#F3F0E8" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="{strand(-1)}" fill="none" stroke="#F13A43" stroke-width="12" stroke-linecap="round"/></svg>')


def doc(w: int, h: int, css: str, body: str) -> str:
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body {{ width: {w}px; height: {h}px; }} {css}</style></head><body>{body}</body></html>'


# ── Шаблоны сторис 1080×1920 ───────────────────────────────

def story(head: str, inner: str = '', css: str = '', foot: str = '@himbio.prosto') -> str:
    return doc(1080, 1920, """
.head { position: absolute; left: 0; right: 0; top: 290px; text-align: center; }
.head .plaque { font-size: 92px; }
.foot { position: absolute; left: 0; right: 0; top: 1500px; text-align: center; font: 800 34px 'Manrope'; letter-spacing: .1em; text-transform: uppercase; }
""" + css, f'<div class="tag" style="top:250px"><i></i>ХИМБИО ПРОСТО</div>' * 0
        + f'<div class="head">{head}</div>{inner}<div class="foot">{foot}</div>')


FRAME = """
.frame { position: absolute; left: 245px; top: 470px; width: 590px; height: 960px; border: 4px dashed rgba(243,240,232,.35); }
.frame b { position: absolute; width: 70px; height: 70px; border: 10px solid #F13A43; }
"""
CORNERS = ''.join(f'<b style="{v}:-14px;{hh}:-14px;border-{"bottom" if v == "top" else "top"}:0;border-{"right" if hh == "left" else "left"}:0"></b>'
                  for v in ('top', 'bottom') for hh in ('left', 'right'))

BLANK_CARD = '.space { position: absolute; left: 90px; right: 90px; top: 470px; height: 960px; }'

STORIES = {
    # Новый рилс: скрин или видео ролика кладётся в рамку (стикер «Фото» в редакторе сторис), сверху — стикер-ссылка.
    'story-new-reel': story('<div class="plaque">Новый рилс</div>', f'<div class="frame">{CORNERS}</div>', FRAME, 'смотри полностью в профиле'),
    # Объявление: текст пишется в Instagram поверх карточки.
    'story-announcement': story('<div class="plaque">Объявление</div>', '<div class="space card"></div>', BLANK_CARD),
    # Вопрос: место под стикер «Вопросы» или «Опрос».
    'story-question': story('<div class="plaque">Вопрос</div><p class="muted" style="font:700 40px Manrope;margin:46px 0 0">спроси про ЕНТ — ответим в сторис</p>',
                            f'<div style="position:absolute;left:390px;top:1130px;width:300px;height:300px">{ATOM}</div>',
                            '.atom { position: static; width: 300px; height: 300px; transform: rotate(-12deg); opacity: .9; }'),
    # Задача дня и ответ: условие/решение пишется поверх карточки.
    'story-task': story('<div class="plaque">Задача дня</div>', '<div class="space card"></div>', BLANK_CARD, 'ответ — в следующей сторис'),
    'story-answer': story('<div class="plaque" style="background:#F3F0E8;color:#151515">Ответ ✓</div>', '<div class="space card"></div>', BLANK_CARD),
    # Чистый фон с подписью: для любых сторис.
    'story-blank': story('<div style="font:800 40px Manrope;letter-spacing:.14em;display:inline-flex;align-items:center;gap:16px"><i style="width:18px;height:18px;border-radius:50%;background:#F13A43"></i>ХИМБИО ПРОСТО</div>'),
}


# ── Пост для таргета: химия + биология ─────────────────────

AD_CSS = """
.icons { position: absolute; display: flex; align-items: center; gap: 40px; }
.icons .atom { position: static; transform: rotate(-12deg); }
.cta { position: absolute; left: 0; right: 0; bottom: 0; background: #F13A43; text-align: center; font: 800 40px 'Manrope'; text-transform: uppercase; letter-spacing: .04em; }
"""


def ad(w: int, h: int, y: dict, size: int = 230) -> str:
    """y: вертикальные позиции блоков (tag, h1, para, chips, cta) — свои для 4:5 и 9:16."""
    return doc(w, h, AD_CSS + f'.icons .atom {{ width: {size}px; height: {size}px; }} .dna {{ width: {int(size * .55)}px; height: {int(size * 1.2)}px; }}', f"""
<div class="slash" style="top:-60px;height:{y['h1'] + 60}px;right:70px;width:60px"></div>
<div class="tag" style="top:{y['tag']}px"><i></i>ХИМБИО ПРОСТО · ЕНТ</div>
<div style="position:absolute;left:80px;top:{y['h1']}px">
  <h1 class="big" style="font-size:104px">Химия<br>и биология</h1>
  <div class="plaque" style="font-size:58px;margin-top:34px">подготовка к ЕНТ</div>
</div>
<p style="position:absolute;left:80px;top:{y['para']}px;width:540px;font:700 44px/1.3 Manrope;margin:0">Объясняем, почему работает способ решения. Решаем задачи в формате теста.</p>
<div class="icons" style="right:90px;top:{y['para'] - 10}px">{ATOM}{dna()}</div>
<div class="chips" style="position:absolute;left:80px;right:60px;top:{y['chips']}px"><span class="chip">онлайн</span><span class="chip">группы по 5</span><span class="chip red">старт 1 ноября</span></div>
<div class="cta" style="top:{y['cta']}px;bottom:auto;padding:34px 0">Запись — в директ @himbio.prosto</div>
""")


# ── Threads: мем «9 баллов по хим-био» ─────────────────────

T1 = doc(1080, 1350, """
.sheet { position: absolute; left: 90px; right: 90px; top: 150px; padding: 60px 64px; }
.row { display: flex; justify-content: space-between; align-items: baseline; padding: 26px 0; border-bottom: 3px solid rgba(243,240,232,.2); font: 700 50px 'Manrope'; }
.row b { font: 800 64px 'Unbounded'; }
.total { margin-top: 50px; display: flex; align-items: center; gap: 36px; }
.nine { font: 800 300px/0.9 'Unbounded'; color: #F13A43; transform: rotate(-4deg); }
""", """
<div class="sheet card">
  <div style="font:800 32px Manrope;letter-spacing:.14em" class="muted">МОЙ РЕЗУЛЬТАТ ЕНТ · ПРОФИЛЬ</div>
  <div class="row" style="margin-top:30px"><span>Химия</span><b>4 <span class="muted" style="font-size:40px">/ 50</span></b></div>
  <div class="row"><span>Биология</span><b>5 <span class="muted" style="font-size:40px">/ 50</span></b></div>
  <div class="total"><div class="nine">9</div><div style="font:800 54px/1.15 Unbounded;text-transform:uppercase">баллов<br>по хим-био</div></div>
</div>
<div style="position:absolute;left:0;right:0;top:1150px;text-align:center;font:800 64px Unbounded;text-transform:uppercase">куда поступать? 🙂</div>
""")

T2 = doc(1080, 1350, AD_CSS + '.icons .atom { width: 230px; height: 230px; } .dna { width: 130px; height: 270px; }', f"""
<div class="tag" style="top:110px"><i></i>ХИМБИО ПРОСТО · ЕНТ</div>
<div style="position:absolute;left:80px;right:80px;top:200px">
  <p style="font:800 50px/1.25 Manrope;margin:0" class="muted">Чтобы не спрашивать, куда поступать с 9 баллами,</p>
  <h1 class="big" style="font-size:100px;margin-top:30px">готовься<br>к ЕНТ</h1>
  <div class="plaque" style="font-size:60px;margin-top:26px">химия + биология</div>
  <div class="chips" style="margin-top:56px"><span class="chip">онлайн</span><span class="chip">группы по 5</span><span class="chip red">старт 1 ноября</span></div>
</div>
<div class="icons" style="right:110px;top:820px">{ATOM}{dna()}</div>
<div class="cta" style="padding:36px 0">Запись — в директ @himbio.prosto</div>
""")


# Биология: тот же дизайн в зелёной гамме — два варианта на выбор Мансуру.
BIO = doc(1080, 1350, AD_CSS + '.dna { width: 200px; height: 440px; }', f"""
<div class="slash" style="top:-60px;height:250px;right:70px;width:60px"></div>
<div class="tag" style="top:100px"><i></i>ХИМБИО ПРОСТО · БИОЛОГИЯ</div>
<div style="position:absolute;left:80px;top:190px">
  <h1 class="big" style="font-size:112px">Биология<br>к ЕНТ</h1>
  <div class="plaque" style="font-size:58px;margin-top:34px">разберёмся вместе</div>
</div>
<p style="position:absolute;left:80px;top:640px;width:560px;font:700 44px/1.3 Manrope;margin:0">Клетка, генетика, эволюция — по шагам и с задачами в формате теста.</p>
<div class="icons" style="right:120px;top:560px">{dna()}</div>
<div class="chips" style="position:absolute;left:80px;right:60px;top:1010px"><span class="chip">онлайн</span><span class="chip">группы по 5</span><span class="chip red">старт 1 ноября</span></div>
<div class="cta" style="top:1240px;bottom:auto;padding:34px 0">Запись — в директ @himbio.prosto</div>
""")
BIO_VARIANTS = {
    'bio-a-black-green': {'#F13A43': '#1F7A4A'},                                     # фон чёрный, акцент тёмно-зелёный
    'bio-b-green-bg': {'#F13A43': '#2E9E5B', '#151515': '#0E2A1D', '#1D1D1D': '#143726'},  # фон тёмно-зелёный, акцент зелёный
}


if __name__ == '__main__':
    if '--bio' in sys.argv:
        (ROOT / 'deliverables' / 'brand-bio').mkdir(parents=True, exist_ok=True)
        for name, swap in BIO_VARIANTS.items():
            html = BIO
            for a, b in swap.items():
                html = html.replace(a, b)
            shot(html, 1080, 1350, ROOT / 'deliverables' / 'brand-bio' / f'{name}.png')
        sys.exit()
    out = ROOT / 'deliverables'
    for name, html in STORIES.items():
        (out / 'stories').mkdir(parents=True, exist_ok=True)
        shot(html, 1080, 1920, out / 'stories' / f'{name}.png')
    (out / 'ads').mkdir(parents=True, exist_ok=True)
    shot(ad(1080, 1350, {'tag': 100, 'h1': 190, 'para': 640, 'chips': 1010, 'cta': 1240}), 1080, 1350, out / 'ads' / 'target-feed-4x5.png')
    # 9:16: снизу ~300 px закрывает кнопка рекламы — призыв выше.
    shot(ad(1080, 1920, {'tag': 270, 'h1': 370, 'para': 840, 'chips': 1230, 'cta': 1420}, 250), 1080, 1920, out / 'ads' / 'target-story-9x16.png')
    (out / 'threads').mkdir(parents=True, exist_ok=True)
    shot(T1, 1080, 1350, out / 'threads' / 'threads-1.png')
    shot(T2, 1080, 1350, out / 'threads' / 'threads-2.png')
    print(f'Social -> {out}/stories, ads, threads')
