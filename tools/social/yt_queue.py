"""Очередь догрузки на YouTube (план 19–21.11.2026, лимит 10 загрузок в сутки без проверки канала).

  .venv/Scripts/python.exe tools/social/yt_queue.py            — что грузить дальше (JSON по строке)
  .venv/Scripts/python.exe tools/social/yt_queue.py --done R004 — отметить загруженное (u/yt/done.txt)

День публикации: плановый из u/yt/plan.json, но не раньше сегодняшнего; если сегодня уже 09:50 или позже —
завтра (публикация всегда в 10:00 по Кызылорде, GMT+5). Порядок — как в плане.
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / 'u/yt/plan.json'
DONE = ROOT / 'u/yt/done.txt'
TZ = timezone(timedelta(hours=5))

done = DONE.read_text(encoding='utf-8').split() if DONE.exists() else []
if len(sys.argv) == 3 and sys.argv[1] == '--done':
    vid = sys.argv[2]
    if vid not in done:
        with DONE.open('a', encoding='utf-8') as f:
            f.write(vid + '\n')
    print('done:', vid, 'всего', len(set(done + [vid])))
    sys.exit()

now = datetime.now(TZ)
earliest = now.date() + timedelta(days=1 if (now.hour, now.minute) >= (9, 50) else 0)
plan = json.loads(PLAN.read_text(encoding='utf-8'))
left = [v for v in plan if v['id'] not in done]
print(f'# сейчас {now:%d.%m %H:%M}, осталось {len(left)} из {len(plan)}')
for v in left:
    day = max(datetime.strptime(v['date'], '%Y-%m-%d').date(), earliest)
    item = {'id': v['id'], 'day': day.day, 'month': day.month, 'planned': v['date'][8:]}
    if v['kind'] == 'long':
        item['parts'] = [f'u/yt/parts/{v["id"]}.mp4.part{i}' for i in range(1, 5)]
        item['size'] = (ROOT / v['file']).stat().st_size
    else:
        item['file'] = v['file']
    print(json.dumps(item, ensure_ascii=False))
