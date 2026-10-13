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


# Таргет v2 (14.10): объясняет, что «ХимБио» — это химия + биология в одном курсе, и что входит.
FACTS = [
    ('2 + 2', 'урока в неделю: химия пн/чт, биология вт/пт'),
    ('5', 'человек в группе · онлайн'),
    ('ДЗ', 'с проверкой · пробные ЕНТ'),
    ('1.11', 'старт курса · до конца мая'),
]


def ad2(w: int, h: int, y: dict, icon: int = 165) -> str:
    rows = ''.join(
        f'<div class="fact"><div class="num" style="background:{"#F13A43" if i % 2 == 0 else "#1F7A4A"}">{n}</div><div class="ft">{t}</div></div>'
        for i, (n, t) in enumerate(FACTS))
    return doc(w, h, AD_CSS + f"""
.pl {{ display: inline-block; font: 800 104px/1 'Unbounded'; text-transform: uppercase; color: #F3F0E8; padding: 12px 30px 20px; }}
.fact {{ display: flex; align-items: center; gap: 28px; margin-bottom: 26px; }}
.num {{ width: 150px; flex: none; text-align: center; padding: 16px 0 20px; font: 800 46px 'Unbounded'; color: #F3F0E8; transform: rotate(-3deg); }}
.ft {{ font: 800 40px/1.2 'Manrope'; color: #F3F0E8; }}
.icons .atom {{ width: {icon}px; height: {icon}px; }} .dna {{ width: {int(icon * .5)}px; height: {int(icon * 1.1)}px; }}
""", f"""
<div class="tag" style="top:{y['tag']}px"><i></i>ХИМБИО ПРОСТО · ЕНТ</div>
<div style="position:absolute;left:80px;top:{y['h1']}px">
  <div class="pl" style="background:#F13A43;transform:rotate(-4deg)">Химия</div><br>
  <div class="pl" style="background:#1F7A4A;transform:rotate(-3deg);margin-top:18px">+ биология</div>
  <div style="font:800 58px/1.15 Unbounded;text-transform:uppercase;margin-top:34px">к ЕНТ —<br>в одном курсе</div>
</div>
<div class="icons" style="right:60px;top:{y['h1'] + 280}px;gap:20px">{ATOM}{dna().replace('#F13A43', '#1F7A4A')}</div>
<div style="position:absolute;left:80px;right:80px;top:{y['facts']}px">{rows}</div>
<div class="cta" style="top:{y['cta']}px;bottom:auto;padding:34px 0">Запись — в директ @himbio.prosto</div>
""")


# Таргет v3 (14.10): две аудитории — ученики и родители. По решению Мансура верхней подписи нет, цена — блоком в баннере.
AUDIENCES = {
    'students': {
        'plaques': [('11 класс?', '#F13A43', -4), ('сдаёшь хим-био?', '#1F7A4A', -3)],
        'lead': 'Готовим к ЕНТ по химии и биологии: по учебникам из перечня НЦТ и в формате теста.',
        'facts': [('90', 'минут живого урока вечером, онлайн'), ('5', 'человек в группе — тебя слышат'),
                  ('ДЗ', 'с проверкой и пробный ЕНТ раз в месяц')],
        'cta': 'Напиши «ТЕСТ» в директ — бесплатный входной тест',
    },
    'parents': {
        'plaques': [('Ребёнок сдаёт', '#F3F0E8', -3), ('химию и биологию?', '#F13A43', -4)],
        'lead': 'Профиль ЕНТ для медицинских вузов. Готовим с ноября по май — оба предмета в одном курсе.',
        'facts': [('2 + 2', 'урока в неделю по 90 минут: химия и биология'), ('5', 'учеников в группе, живой преподаватель'),
                  ('ДЗ', 'проверяем каждую неделю, пробный ЕНТ раз в месяц')],
        'cta': 'Напишите «ПРОГРАММА» в директ — пришлём программу курса',
    },
}
PRICE = ('19 500 ₸ в месяц', 'химия + биология · оплата Kaspi')  # решение Мансура 14.10: цена — в рекламном баннере


def ad3(kind: str, w: int, h: int, y: dict, icon: int = 150) -> str:
    a = AUDIENCES[kind]
    pls = ''.join(f'<div class="pl" style="background:{bg};color:{"#151515" if bg == "#F3F0E8" else "#F3F0E8"};transform:rotate({r}deg);margin-top:{0 if i == 0 else 16}px">{t}</div><br>'
                  for i, (t, bg, r) in enumerate(a['plaques']))
    rows = ''.join(f'<div class="fact"><div class="num" style="background:{"#F13A43" if i % 2 == 0 else "#1F7A4A"};{"font-size:30px" if len(n) > 3 else ""}">{n}</div><div class="ft">{t}</div></div>'
                   for i, (n, t) in enumerate(a['facts']))
    return doc(w, h, AD_CSS + f"""
.pl {{ display: inline-block; white-space: nowrap; font: 800 {y.get('pl', 64)}px/1.05 'Unbounded'; text-transform: uppercase; padding: 10px 24px 16px; }}
.lead {{ font: 700 42px/1.3 'Manrope'; margin: 0; }}
.fact {{ display: flex; align-items: center; gap: 26px; margin-bottom: 22px; }}
.num {{ width: 150px; flex: none; text-align: center; padding: 14px 0 18px; font: 800 {y.get('num', 42)}px 'Unbounded'; color: #F3F0E8; transform: rotate(-3deg); }}
.ft {{ font: 800 36px/1.2 'Manrope'; color: #F3F0E8; }}
.icons .atom {{ width: {icon}px; height: {icon}px; }} .dna {{ width: {int(icon * .5)}px; height: {int(icon * 1.1)}px; }}
.cta {{ font-size: 36px; line-height: 1.25; padding: 30px 60px !important; }}
.price {{ position: absolute; left: 80px; display: flex; align-items: center; gap: 26px; }}
.price b {{ background: #F3F0E8; color: #151515; padding: 14px 26px 16px; font: 800 52px/1.05 'Unbounded'; white-space: nowrap; transform: rotate(-2deg); }}
.price span {{ font: 800 30px/1.25 'Manrope'; text-transform: uppercase; letter-spacing: .05em; }}
""", f"""
<div class="icons" style="right:60px;top:{y['icons']}px;gap:16px">{ATOM}{dna().replace('#F13A43', '#1F7A4A')}</div>
<div class="price" style="top:{y['price']}px"><b>{PRICE[0]}</b><span>{PRICE[1].replace(' · ', '<br>')}</span></div>
<div style="position:absolute;left:80px;right:80px;top:{y['h1']}px">{pls}</div>
<p class="lead" style="position:absolute;left:80px;right:90px;top:{y['lead']}px">{a['lead']}</p>
<div style="position:absolute;left:80px;right:80px;top:{y['facts']}px">{rows}</div>
<div class="cta" style="top:{y['cta']}px;bottom:auto">{a['cta']}</div>
""")


# Обложки YouTube 1280×720 в стиле обложки «Моль за 4 минуты» (tools/youtube/art.py).
def thumb(tag: str, h1: str, plaque: str, badge: str, icon: str, accent: str = '#F13A43') -> str:
    return doc(1280, 720, f"""
body {{ background-size: 64px 64px; padding: 60px 70px; }}
.t {{ font: 800 28px 'Manrope'; letter-spacing: .14em; display: flex; align-items: center; gap: 12px; }}
.t i {{ width: 14px; height: 14px; border-radius: 50%; background: {accent}; }}
h1 {{ margin: 40px 0 0; font: 800 120px/1 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }}
.plaque {{ margin-top: 24px; font-size: 80px; background: {accent}; }}
.badge {{ position: absolute; right: 70px; bottom: 70px; padding: 22px 34px; background: #F3F0E8; color: #151515; font: 800 56px 'Unbounded'; transform: rotate(3deg); }}
.ic {{ position: absolute; right: 90px; top: 40px; }}
.ic .atom {{ position: static; width: 280px; height: 280px; transform: rotate(-12deg); }}
.ic .dna {{ width: 170px; height: 340px; }}
""", f'<div class="t"><i></i>{tag}</div><h1>{h1}</h1><div class="plaque">{plaque}</div><div class="ic">{icon}</div><div class="badge">{badge}</div>')


THUMBS = {
    'thumb-y003': thumb('БИОЛОГИЯ ДЛЯ ЕНТ', 'Генетика', 'за 3 минуты', 'Aa × Aa', dna().replace('#F13A43', '#1F7A4A'), '#1F7A4A'),
    'thumb-y004': thumb('О КАНАЛЕ', 'ХимБио<br>просто', 'ЕНТ без паники', 'химия + био', ATOM + dna().replace('#F13A43', '#1F7A4A')),
}


if __name__ == '__main__':
    if '--bio' in sys.argv:
        (ROOT / 'deliverables' / 'brand-bio').mkdir(parents=True, exist_ok=True)
        for name, swap in BIO_VARIANTS.items():
            html = BIO
            for a, b in swap.items():
                html = html.replace(a, b)
            shot(html, 1080, 1350, ROOT / 'deliverables' / 'brand-bio' / f'{name}.png')
        # Шаблоны сторис для биологии: тот же дизайн, акцент тёмно-зелёный.
        (ROOT / 'deliverables' / 'stories-bio').mkdir(parents=True, exist_ok=True)
        for name, html in STORIES.items():
            shot(html.replace(ATOM, dna()).replace('#F13A43', '#1F7A4A'), 1080, 1920, ROOT / 'deliverables' / 'stories-bio' / f'{name}-bio.png')
        sys.exit()
    if '--ad2' in sys.argv:
        (ROOT / 'deliverables' / 'ads').mkdir(parents=True, exist_ok=True)
        shot(ad2(1080, 1350, {'tag': 90, 'h1': 170, 'facts': 720, 'cta': 1240}), 1080, 1350, ROOT / 'deliverables' / 'ads' / 'target-himbio-4x5.png')
        shot(ad2(1080, 1920, {'tag': 260, 'h1': 350, 'facts': 920, 'cta': 1420}, 175), 1080, 1920, ROOT / 'deliverables' / 'ads' / 'target-himbio-9x16.png')
        sys.exit()
    if '--ad3' in sys.argv:
        out = ROOT / 'deliverables' / 'ads'
        out.mkdir(parents=True, exist_ok=True)
        for kind in AUDIENCES:
            pl = 64 if kind == 'students' else 54
            shot(ad3(kind, 1080, 1350, {'icons': 60, 'h1': 230, 'lead': 470, 'facts': 660 if kind == 'students' else 680, 'price': 1020, 'cta': 1180, 'pl': pl}),
                 1080, 1350, out / f'target-{kind}-4x5.png')
            # 9:16: нижние ~300 px закрывает кнопка рекламы — призыв выше.
            shot(ad3(kind, 1080, 1920, {'icons': 220, 'h1': 400, 'lead': 650, 'facts': 860 if kind == 'students' else 880, 'price': 1250, 'cta': 1420, 'pl': pl}, 160),
                 1080, 1920, out / f'target-{kind}-9x16.png')
        sys.exit()
    if '--yt' in sys.argv:
        for name, html in THUMBS.items():
            shot(html, 1280, 720, ROOT / 'deliverables' / 'youtube' / f'{name}.png')
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
