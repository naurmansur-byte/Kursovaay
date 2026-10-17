"""Сторис v2 — новые интерактивные форматы 1080×1920 в стиле 2 (химия — красный, биология — зелёный).

Запуск: .venv/Scripts/python tools/social/stories2.py
Результат: deliverables/stories-v2/*.png и копия в «00 Материалы ХимБио просто/Instagram и Threads/Сторис — новые форматы/».
Всё важное — в зоне 250–1580 px по высоте. Текст, стикеры «Опрос», «Викторина», «Шкала», «Отсчёт», «Ссылка», «Фото»
добавляются в редакторе Instagram на пустые места. Как пользоваться — content/social/STORIES-V2.md.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
from social import ATOM, doc, dna, shot  # noqa: E402

ROOT = HERE.parents[1]
RED, GREEN, INK, PAPER, MUTED = '#F13A43', '#1F7A4A', '#151515', '#F3F0E8', '#B9B3A8'

CSS = """
.plaque { padding: .08em .26em .16em; }
.u { font-family: 'Unbounded'; font-weight: 800; text-transform: uppercase; letter-spacing: -.02em; line-height: 1; margin: 0; }
.abs { position: absolute; }
.card { background: #1D1D1D; border: 5px solid #F3F0E8; }
.hint { font: 800 40px 'Manrope'; color: #B9B3A8; letter-spacing: .04em; }
.atom { position: absolute; }
.dna { position: absolute; }
"""


def story(css: str, body: str) -> str:
    return doc(1080, 1920, CSS + css, body)


def arrow(x: int, y: int, color: str = PAPER, flip: bool = False, w: int = 170) -> str:
    """Рисованная стрелка вниз — показывает, куда ставить стикер."""
    tr = 'scale(-1,1) translate(-170,0)' if flip else ''
    return (f'<svg class="abs" style="left:{x}px;top:{y}px" width="{w}" height="{w}" viewBox="0 0 170 170"><g transform="{tr}">'
            f'<path d="M20 20 C 110 20, 130 70, 110 140" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M80 118 L110 146 L136 112" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g></svg>')


def icon(subj: str, x: int, y: int, size: int, rot: int = -12) -> str:
    if subj == 'bio':
        return dna().replace('class="dna"', f'class="dna" style="left:{x}px;top:{y}px;width:{size * .5:.0f}px;height:{size}px;transform:rotate({rot}deg)"').replace(RED, GREEN)
    return ATOM.replace('class="atom"', f'class="atom" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({rot}deg)"', 1)


SUBJ = {'chem': ('химия', RED), 'bio': ('биология', GREEN)}

# 1. Правда или миф? — утверждение на карточке, ниже стикер «Опрос» (Правда / Миф).
MYTH = story("""
.lines { background-image: repeating-linear-gradient(transparent 0 70px, rgba(21,21,21,.10) 70px 73px); }
""", f"""
<div class="abs u plaque" style="left:80px;top:290px;font-size:104px;background:{GREEN};color:#fff;transform:rotate(-4deg)">Правда</div>
<p class="abs" style="left:120px;top:470px;margin:0;font:800 italic 52px Manrope;color:{MUTED}">или</p>
<div class="abs u plaque" style="left:300px;top:440px;font-size:130px;background:{RED};color:#fff;transform:rotate(3deg)">миф?</div>
<div class="abs lines" style="left:90px;right:90px;top:690px;height:540px;background-color:{PAPER};transform:rotate(-1.5deg);box-shadow:18px 18px 0 {RED}"></div>
<p class="abs u" style="left:120px;top:660px;font-size:150px;color:{RED};opacity:.9">“</p>
{arrow(780, 1260)}<p class="abs hint" style="left:440px;top:1300px">голосуй</p>
""")


# 2. Квиз ЕНТ — вопрос на карточке, ниже стикер «Викторина» с 3–4 вариантами.
def quiz(subj: str) -> str:
    name, acc = SUBJ[subj]
    return story(f"""
.q {{ position: absolute; right: -120px; top: 180px; font: 800 1150px/1 'Unbounded'; color: transparent; -webkit-text-stroke: 8px rgba(243,240,232,.07); }}
""", f"""<div class="q">?</div>
<div class="abs u plaque" style="left:80px;top:300px;font-size:116px;background:{acc};color:#fff;transform:rotate(-3deg)">Квиз ЕНТ</div>
<div class="abs" style="left:90px;top:470px;border:4px solid {PAPER};padding:10px 26px;font:800 36px Manrope;letter-spacing:.12em;text-transform:uppercase">{name}</div>
{icon(subj, 840, 440, 150)}
<div class="abs card" style="left:90px;right:90px;top:600px;height:420px;box-shadow:18px 18px 0 {acc}"></div>
<p class="abs hint" style="left:90px;top:1090px">выбери ответ</p>{arrow(420, 1060, acc, w=130)}
""")


# 3. Найди ошибку — «решение в тетради» с ошибкой, ответ — в следующей сторис.
FIND = story(f"""
.nb {{ background-color: {PAPER}; background-image: linear-gradient(90deg, transparent 118px, {RED} 118px 122px, transparent 122px),
  repeating-linear-gradient(transparent 0 66px, rgba(21,21,21,.12) 66px 69px); }}
""", f"""
<p class="abs u" style="left:80px;top:290px;font-size:128px">Найди</p>
<p class="abs u" style="left:80px;top:490px;font-size:128px;color:{RED}">ошибку</p>
<svg class="abs" style="left:40px;top:400px" width="1000" height="280" viewBox="0 0 1000 230"><path d="M60 150 C 60 25, 940 15, 960 130 C 980 250, 300 275, 120 245 C 40 230, 30 150, 90 110" fill="none" stroke="{PAPER}" stroke-width="9" stroke-linecap="round"/></svg>
<div class="abs nb" style="left:80px;right:80px;top:720px;height:730px;transform:rotate(1.5deg);box-shadow:-18px 18px 0 {RED}"></div>
<p class="abs" style="left:0;right:0;top:1500px;text-align:center;font:800 34px Manrope;letter-spacing:.1em;text-transform:uppercase">ответ — в следующей сторис</p>
""")

# 4. Насколько ты уверен? — тема на карточке, ниже стикер «Шкала».
SLIDER = story("", f"""
<p class="abs u" style="left:80px;top:290px;font-size:92px">Насколько</p>
<div class="abs u plaque" style="left:80px;top:410px;font-size:92px;background:{RED};color:#fff;transform:rotate(-3deg)">ты уверен?</div>
<div class="abs card" style="left:90px;right:90px;top:620px;height:420px;box-shadow:18px 18px 0 {GREEN}"></div>
<div class="abs" style="left:90px;right:90px;top:1130px;height:26px;border-radius:13px;background:linear-gradient(90deg,{RED},#D99A1E,{GREEN})"></div>
<p class="abs" style="left:90px;top:1180px;margin:0;font:800 34px Manrope;color:{MUTED}">не знаю</p>
<p class="abs" style="right:90px;top:1180px;margin:0;font:800 34px Manrope;color:{MUTED}">знаю на 100</p>
""")

# 5. До ЕНТ осталось — отрывной календарь; число дней пишется в Instagram, ниже стикер «Отсчёт».
COUNT = story("", f"""
<div class="abs" style="left:190px;top:330px;width:700px;height:860px;background:{PAPER};transform:rotate(-2deg);box-shadow:20px 20px 0 {RED}">
<div style="height:210px;background:{RED};display:flex;align-items:center;justify-content:center"><p class="u" style="font-size:56px;color:#fff;text-align:center;line-height:1.15">До ЕНТ<br>осталось</p></div>
<div style="position:absolute;left:150px;top:-36px;width:44px;height:90px;border-radius:22px;background:{INK};border:6px solid {PAPER}"></div>
<div style="position:absolute;right:150px;top:-36px;width:44px;height:90px;border-radius:22px;background:{INK};border:6px solid {PAPER}"></div>
<p class="u" style="position:absolute;left:0;right:0;bottom:60px;text-align:center;font-size:64px;color:{INK}">дней</p>
</div>
<p class="abs hint" style="left:0;right:0;top:1300px;text-align:center">включи напоминание ↓</p>
""")

# 6. Химия vs Биология — ниже стикер «Опрос» («Что сложнее?», «Что учишь сейчас?» …).
VS = story(f"""
.half {{ position: absolute; inset: 0; }}
""", f"""
<div class="half" style="background:{RED};clip-path:polygon(0 0,100% 0,100% 38%,0 62%)"></div>
<div class="half" style="background:{GREEN};clip-path:polygon(0 62%,100% 38%,100% 100%,0 100%)"></div>
<div class="abs u plaque" style="left:50%;top:270px;transform:translateX(-50%) rotate(-2deg);font-size:64px;background:{INK};color:{PAPER};white-space:nowrap">Что сложнее?</div>
<p class="abs u" style="left:80px;top:610px;font-size:140px;color:#fff;transform:rotate(-23deg);transform-origin:left">Химия</p>
<p class="abs u" style="right:60px;top:1250px;font-size:118px;color:#fff;transform:rotate(-23deg);transform-origin:right">Биология</p>
{icon('chem', 700, 380, 220).replace(RED, INK)}{icon('bio', 170, 1180, 300, 18).replace(GREEN, INK)}
<div class="abs" style="left:430px;top:850px;width:220px;height:220px;border-radius:50%;background:{INK};border:8px solid {PAPER};display:flex;align-items:center;justify-content:center"><p class="u" style="font-size:96px">vs</p></div>
""")


# 7. Факт за 10 секунд — факт на карточке, сохрани.
def fact(subj: str) -> str:
    name, acc = SUBJ[subj]
    watch = (f'<svg class="abs" style="left:770px;top:260px;transform:rotate(12deg)" width="230" height="260" viewBox="0 0 230 260">'
             f'<rect x="95" y="6" width="40" height="30" rx="6" fill="{PAPER}"/><circle cx="115" cy="150" r="96" fill="none" stroke="{PAPER}" stroke-width="14"/>'
             f'<path d="M115 150 L115 84" stroke="{acc}" stroke-width="14" stroke-linecap="round"/><path d="M115 150 A66 66 0 0 1 172 117 L115 150 Z" fill="{acc}"/></svg>')
    return story("", f"""{watch}
<p class="abs u" style="left:80px;top:300px;font-size:170px">Факт</p>
<div class="abs u plaque" style="left:80px;top:490px;font-size:72px;background:{acc};color:#fff;transform:rotate(-3deg)">за 10 секунд</div>
<div class="abs" style="left:90px;top:640px;border:4px solid {PAPER};padding:10px 26px;font:800 36px Manrope;letter-spacing:.12em;text-transform:uppercase">{name} · ЕНТ</div>
<div class="abs" style="left:90px;right:90px;top:760px;height:620px;background:{PAPER};transform:rotate(-1.5deg);box-shadow:18px 18px 0 {acc}"></div>
<p class="abs u" style="right:130px;top:700px;font-size:200px;color:{acc};transform:rotate(8deg)">!</p>
<p class="abs" style="left:0;right:0;top:1500px;text-align:center;font:800 34px Manrope;letter-spacing:.1em;text-transform:uppercase">сохрани, чтобы не забыть</p>
""")


# 8. Новое видео на YouTube — в окно кладём обложку (стикер «Фото»), ниже стикер «Ссылка».
YT = story("", f"""
<p class="abs u" style="left:80px;top:290px;font-size:104px">Новое видео</p>
<div class="abs u plaque" style="left:80px;top:420px;font-size:84px;background:{RED};color:#fff;transform:rotate(-3deg)">на YouTube</div>
<div class="abs" style="left:80px;right:80px;top:600px;height:540px;border:6px solid {PAPER};background:#1D1D1D;transform:rotate(-1deg)">
<div style="position:absolute;inset:24px;border:4px dashed rgba(243,240,232,.25);display:flex;align-items:center;justify-content:center"><p style="font:700 34px Manrope;color:{MUTED}">обложка видео</p></div></div>
<div class="abs" style="left:80px;right:80px;top:1175px;height:10px;background:rgba(243,240,232,.25)"><div style="width:38%;height:10px;background:{RED}"></div>
<div style="position:absolute;left:38%;top:-11px;width:32px;height:32px;margin-left:-16px;border-radius:50%;background:{RED}"></div></div>
<div class="abs" style="right:40px;top:1030px;width:210px;height:148px;border-radius:40px;background:{RED};transform:rotate(-8deg);display:flex;align-items:center;justify-content:center">
<svg width="70" height="80" viewBox="0 0 70 80"><path d="M4 4 L66 40 L4 76 Z" fill="#fff"/></svg></div>
{arrow(150, 1250, PAPER, w=140)}<p class="abs hint" style="left:320px;top:1300px">смотри по ссылке</p>
""")

# 9. Закулисье недели — три полароида под фото с уроков, материалов, разборов.
POL = """<div class="abs" style="left:{x}px;top:{y}px;width:430px;height:510px;background:#F3F0E8;transform:rotate({r}deg);box-shadow:14px 14px 0 {c}">
<div style="position:absolute;left:20px;top:20px;right:20px;height:390px;background:#262626"></div>
<div style="position:absolute;left:150px;top:-26px;width:130px;height:46px;background:rgba(243,240,232,.55);transform:rotate(-4deg)"></div></div>"""
WEEK = story("", f"""
<p class="abs u" style="left:80px;top:280px;font-size:112px">Неделя</p>
<div class="abs u plaque" style="left:80px;top:410px;font-size:80px;background:{GREEN};color:#fff;transform:rotate(-3deg)">в ХимБио</div>
{POL.format(x=80, y=600, r=-6, c=RED)}{POL.format(x=570, y=700, r=5, c=GREEN)}{POL.format(x=300, y=1050, r=-2, c=RED)}
""")

# 10. Вы спросили — мы отвечаем: стикер-вопрос в первый «пузырь», ответ — во второй.
QA = story("", f"""
<p class="abs u" style="left:80px;top:280px;font-size:84px">Вы спросили —</p>
<div class="abs u plaque" style="left:80px;top:395px;font-size:84px;background:{RED};color:#fff;transform:rotate(-3deg)">мы отвечаем</div>
<div class="abs" style="left:80px;width:780px;top:590px;height:300px;background:#2A2A2A;border-radius:48px 48px 48px 10px"></div>
<div class="abs" style="right:80px;width:840px;top:940px;height:560px;background:{PAPER};border-radius:48px 48px 10px 48px;box-shadow:16px 16px 0 {GREEN}"></div>
<div class="abs" style="right:80px;top:1520px;font:800 30px Manrope;color:{MUTED};letter-spacing:.08em">@HIMBIO.PROSTO ✓</div>
""")

STORIES = {
    '01-pravda-ili-mif': MYTH,
    '02-kviz-himiya': quiz('chem'),
    '03-kviz-biologiya': quiz('bio'),
    '04-naidi-oshibku': FIND,
    '05-naskolko-uveren': SLIDER,
    '06-do-ent-ostalos': COUNT,
    '07-himiya-vs-biologiya': VS,
    '08-fakt-himiya': fact('chem'),
    '09-fakt-biologiya': fact('bio'),
    '10-novoe-video-youtube': YT,
    '11-nedelya-v-himbio': WEEK,
    '12-vy-sprosili': QA,
}

if __name__ == '__main__':
    out = ROOT / 'deliverables' / 'stories-v2'
    out.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:]
    for name, html in STORIES.items():
        if not only or any(o in name for o in only):
            shot(html, 1080, 1920, out / f'{name}.png')
    mat = ROOT / '00 Материалы ХимБио просто' / 'Instagram и Threads' / 'Сторис — новые форматы'
    mat.mkdir(parents=True, exist_ok=True)
    for f in out.glob('*.png'):
        shutil.copy2(f, mat / f.name)
    print(f'{len(STORIES)} stories -> {out}')
