"""План загрузки на YouTube 19–21.11.2026 (решение Мансура 18.11): 4 длинных + 42 Shorts, по дню — всё в 10:00.

Тексты — из content/MANUAL-POSTING-28-10.md (Shorts 01–38, Y009–Y012) и подписи S001–S004 оттуда же.
Правки: «онлайн, старт 1 ноября» → «онлайн» (дата прошла); у длинных убрана последняя глава «Курс…» (концовка отрезана).
Запуск: .venv/Scripts/python.exe tools/social/yt_plan.py → u/yt/plan.json
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[2]
MD = (ROOT / 'content/MANUAL-POSTING-28-10.md').read_text(encoding='utf-8')
PL = {'chem_long': 'Химия к ЕНТ — по порядку', 'bio_long': 'Биология к ЕНТ — по порядку',
      'chem_short': 'Shorts: химия — вопросы ЕНТ', 'bio_short': 'Shorts: биология — вопросы ЕНТ'}


def block(header_re):
    m = re.search(header_re + r'.*?\n(.*?)(?=\n### |\n## |\Z)', MD, re.S)
    return m.group(1).strip() if m else None


def field(text, name):
    m = re.search(r'\*\*' + name + r':\*\*\s*(.*?)\n', text)
    return m.group(1).strip() if m else None


def desc(text):
    d = text.split('**Описание:**', 1)[1].strip()
    d = d.replace('онлайн, старт 1 ноября', 'онлайн')
    # Мансур 19.11: зовём записаться на курс
    d = d.replace('ЕНТ по химии и биологии. Instagram: @himbio.prosto', 'ЕНТ по химии и биологии. Запись на курс — в директ Instagram @himbio.prosto')
    return d


videos = []
for vid in ('Y009', 'Y011', 'Y010', 'Y012'):
    b = block(r'### ' + vid)
    d = desc(b)
    d = re.sub(r'\n\d+:\d\d Курс «ХимБио просто»', '', d)  # глава отрезанной концовки
    pl = PL['chem_long'] if 'Химия' in field(b, 'Название') else PL['bio_long']
    videos.append(dict(id=vid, kind='long', title=field(b, 'Название'), description=d, playlists=[pl],
                       thumb=f'deliverables/youtube/thumb-{vid.lower()}.png'))

for m in re.finditer(r'### Short (\d+) · ([RB]\d{3})', MD):
    b = block(re.escape(m.group(0)))
    sid = m.group(2)
    videos.append(dict(id=sid, kind='short', order=int(m.group(1)), title=field(b, 'Название'), description=desc(b),
                       playlists=[PL['chem_short'] if sid.startswith('R') else PL['bio_short']]))

S = {
    'S001': ('Правда или миф? 3 утверждения по биологии ЕНТ — сколько угадаешь? · биология', ['bio_short'], 'биология'),
    'S002': ('Найди ошибку в решении задачи по химии ЕНТ — в какой строке? · химия', ['chem_short'], 'химия'),
    'S003': ('Химия против биологии: одна молекула глюкозы — два вопроса ЕНТ', ['chem_short', 'bio_short'], 'химия #биология'),
    'S004': ('Факт за 10 секунд: водородные связи в ДНК · вопрос ЕНТ по биологии', ['bio_short'], 'биология'),
}
for sid, (title, pls, tags) in S.items():
    cap = block(r'### \d+ · ' + sid)
    first = cap.split('\n')[0].strip()
    d = (f'{first}\n\nКурс «ХимБио просто» — подготовка к ЕНТ по химии и биологии. Instagram: @himbio.prosto\n\n'
         f'#ЕНТ #{tags} #shorts')
    videos.append(dict(id=sid, kind='short', order=38 + int(sid[1:]), title=title, description=d,
                       playlists=[PL[p] for p in pls]))

longs = [v for v in videos if v['kind'] == 'long']
shorts = sorted([v for v in videos if v['kind'] == 'short'], key=lambda v: v['order'])
days = {'2026-11-19': longs[:2] + shorts[:13], '2026-11-20': longs[2:3] + shorts[13:27], '2026-11-21': longs[3:] + shorts[27:]}
plan = []
for day, vs in days.items():
    for v in vs:
        plan.append({**v, 'date': day, 'time': '10:00', 'file': f'u/yt/{v["id"]}.mp4'})
for v in plan:
    assert len(v['title']) <= 100, (v['id'], len(v['title']))
    assert '1 ноября' not in v['description'] and 'по 5' not in v['description'], v['id']
out = ROOT / 'u/yt/plan.json'
out.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding='utf-8')
for day in days:
    print(day, len([v for v in plan if v['date'] == day]), ' '.join(v['id'] for v in plan if v['date'] == day))
print('всего', len(plan))
