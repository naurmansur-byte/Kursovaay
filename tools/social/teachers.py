"""Карусель «Знакомьтесь: преподаватели» 1080×1350 в стиле 2 (химия — красный, биология — зелёный).

Запуск: .venv/Scripts/python tools/social/teachers.py
Данные и фото — вне Git: «00 Материалы ХимБио просто/Преподаватели/teachers.json» (+ фото рядом).
Если файла нет, рисуется шаблон с заглушками в deliverables/instagram/teachers-template/.
Формат teachers.json: [{"name": "...", "subject": "chem|bio", "photo": "file.jpg",
  "stats": [["10", "лет преподаёт"], ["6", "выпусков ЕНТ"]], "facts": ["...", "..."], "quote": "..."}]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
from social import ATOM, doc, dna, shot  # noqa: E402

ROOT = HERE.parents[1]
PRIVATE = ROOT / '00 Материалы ХимБио просто' / 'Преподаватели'
RED, GREEN, INK, PAPER = '#F13A43', '#1F7A4A', '#151515', '#F3F0E8'
SUBJ = {'chem': ('Химия', RED), 'bio': ('Биология', GREEN)}

PLACEHOLDER = [
    {'name': 'Имя Фамилия', 'subject': 'chem', 'photo': '', 'stats': [['N', 'лет преподаёт'], ['N', 'выпусков ЕНТ']],
     'facts': ['Образование: вуз, специальность', 'Опыт: школа, курсы, ЕНТ'], 'quote': 'Одна фраза преподавателя о предмете'},
    {'name': 'Имя Фамилия', 'subject': 'bio', 'photo': '', 'stats': [['N', 'лет преподаёт'], ['N', 'выпусков ЕНТ']],
     'facts': ['Образование: вуз, специальность', 'Опыт: школа, курсы, ЕНТ'], 'quote': 'Одна фраза преподавателя о предмете'},
]

CAMERA = (f'<svg viewBox="0 0 120 96" width="150"><rect x="6" y="20" width="108" height="70" rx="12" fill="none" stroke="{PAPER}" stroke-width="7"/>'
          f'<path d="M38 20 L46 6 H74 L82 20" fill="none" stroke="{PAPER}" stroke-width="7" stroke-linejoin="round"/>'
          f'<circle cx="60" cy="55" r="20" fill="none" stroke="{PAPER}" stroke-width="7"/></svg>')

COVER = doc(1080, 1350, """
.slash { position: absolute; top: -200px; bottom: -200px; transform: skewX(-14deg); }
h1 { position: absolute; left: 80px; top: 360px; margin: 0; font: 800 132px/1 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }
.plaque { position: absolute; left: 80px; top: 640px; padding: 14px 34px 22px; font-size: 52px; white-space: nowrap; }
.lead { position: absolute; left: 80px; top: 820px; width: 800px; font: 700 42px/1.3 'Manrope'; color: #B9B3A8; margin: 0; }
.atom { position: absolute; right: 70px; top: 90px; width: 260px; height: 260px; transform: rotate(-12deg); }
.dna { position: absolute; right: 110px; bottom: 90px; width: 170px; height: 360px; transform: rotate(14deg); }
.swipe { position: absolute; left: 80px; bottom: 90px; font: 800 34px 'Manrope'; letter-spacing: .12em; text-transform: uppercase; }
.swipe b { color: #F13A43; }
""", f"""<div class="slash" style="left:-60px;width:120px;background:{RED}"></div><div class="slash" style="left:90px;width:36px;background:{GREEN}"></div>
{ATOM}{dna().replace('#F13A43', GREEN)}
<h1>Знакомь&shy;тесь</h1><div class="plaque">наши преподаватели</div>
<p class="lead">Кто ведёт уроки химии и биологии в «ХимБио просто»</p>
<div class="swipe">листай <b>→</b></div>""")


def teacher(t: dict) -> str:
    subj, acc = SUBJ[t['subject']]
    photo = PRIVATE / t['photo'] if t.get('photo') else None
    if photo and photo.exists():
        pic = f'<img src="{photo.as_uri()}" style="width:100%;height:100%;object-fit:cover;object-position:50% 35%;display:block">'
    else:
        pic = (f'<div class="ph">{CAMERA}<p>фото по пояс,<br>светлый фон</p></div>')
    stats = ''.join(f'<div class="stat"><b>{n}</b><span>{lbl}</span></div>' for n, lbl in t['stats'][:2])
    facts = ''.join(f'<li><i></i>{f}</li>' for f in t['facts'][:3])
    return doc(1080, 1350, f"""
.plaque {{ position: absolute; left: 80px; top: 100px; padding: 12px 30px 18px; font-size: 46px; background: {acc}; z-index: 2; }}
.stats {{ position: absolute; left: 80px; top: 250px; width: 340px; display: flex; flex-direction: column; gap: 40px; }}
.stat b {{ display: block; font: 800 150px/1 'Unbounded'; color: {PAPER}; }}
.stat span {{ display: block; margin-top: 8px; font: 800 34px/1.2 'Manrope'; color: #B9B3A8; text-transform: uppercase; letter-spacing: .04em; }}
.photo {{ position: absolute; left: 470px; top: 90px; width: 530px; height: 680px; border: 6px solid {PAPER};
  box-shadow: -20px 20px 0 {acc}; transform: rotate(3deg); background: #1D1D1D; overflow: hidden; }}
.ph {{ height: 100%; border: 4px dashed rgba(243,240,232,.35); margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 24px; }}
.ph p {{ margin: 0; text-align: center; font: 700 34px/1.3 'Manrope'; color: #B9B3A8; }}
.who {{ position: absolute; left: 80px; top: 840px; width: 920px; display: flex; flex-direction: column; gap: 28px; }}
h2 {{ margin: 0; font: 800 76px/1.02 'Unbounded'; text-transform: uppercase; letter-spacing: -.01em; }}
ul {{ margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 14px; }}
li {{ font: 700 34px/1.25 'Manrope'; display: flex; gap: 18px; align-items: baseline; }}
li i {{ flex: none; width: 18px; height: 18px; background: {acc}; transform: translateY(-4px); }}
.quote {{ position: absolute; left: 80px; right: 80px; bottom: 70px; padding: 22px 30px 24px 104px; background: {PAPER}; color: {INK};
  font: 800 34px/1.25 'Manrope'; transform: rotate(-1.5deg); }}
.quote::before {{ content: '«'; position: absolute; left: 26px; top: 14px; font: 800 64px/1 'Unbounded'; color: {acc}; }}
""", f"""<div class="plaque">{subj}</div><div class="stats">{stats}</div>
<div class="photo">{pic}</div><div class="who"><h2>{t['name']}</h2><ul>{facts}</ul></div><div class="quote">{t['quote']}</div>""")


FINAL = doc(1080, 1350, """
h2 { position: absolute; left: 80px; top: 110px; margin: 0; font: 800 96px/1.02 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }
.rows { position: absolute; left: 80px; right: 80px; top: 400px; display: flex; flex-direction: column; gap: 22px; }
.row { display: flex; align-items: center; gap: 30px; padding: 26px 32px; background: #1D1D1D; border: 4px solid #F3F0E8; font: 800 40px/1.2 'Manrope'; }
.row b { flex: none; width: 76px; height: 76px; display: flex; align-items: center; justify-content: center; font: 800 40px 'Unbounded'; color: #fff; }
.cta { position: absolute; left: 80px; right: 80px; bottom: 90px; padding: 30px 36px 34px; background: #F13A43; color: #fff; transform: rotate(-2deg); font: 800 44px/1.25 'Manrope'; }
.cta span { font-family: 'Unbounded'; }
""", f"""<h2>Как проходят<br>уроки</h2>
<div class="rows">
<div class="row"><b style="background:{RED}">1</b>Онлайн в Google Meet, вечером</div>
<div class="row"><b style="background:{GREEN}">2</b>2 урока в неделю по каждому предмету</div>
<div class="row"><b style="background:{RED}">3</b>ДЗ в Telegram — с проверкой</div>
<div class="row"><b style="background:{GREEN}">4</b>Раз в месяц — пробник в формате ЕНТ</div>
</div>
<div class="cta">Напиши в директ <span>«ПРОГРАММА»</span> — пришлём программу курса</div>""")


def main() -> None:
    data_file = PRIVATE / 'teachers.json'
    if data_file.exists():
        data = json.loads(data_file.read_text(encoding='utf-8'))
        out = ROOT / '00 Материалы ХимБио просто' / 'Instagram и Threads' / 'Карусель — преподаватели'
    else:
        data = PLACEHOLDER
        out = ROOT / 'deliverables' / 'instagram' / 'teachers-template'
    out.mkdir(parents=True, exist_ok=True)
    pages = [COVER] + [teacher(t) for t in data] + [FINAL]
    for i, html in enumerate(pages, 1):
        shot(html, 1080, 1350, out / f'{i:02d}.png')
    print(f'{len(pages)} slides -> {out}')


if __name__ == '__main__':
    main()
