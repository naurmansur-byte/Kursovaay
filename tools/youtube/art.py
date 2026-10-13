"""YouTube «Химия просто»: шапка канала 2560×1440 и обложка видео 1280×720 (Chrome-скриншоты HTML, стиль 2).

Запуск: .venv/Scripts/python tools/youtube/art.py   (результат: deliverables/youtube/banner.png, thumb-y001.png)
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools' / 'handout'), str(ROOT / 'tools' / 'slides')]
from handout import chrome  # noqa: E402
from slides import ATOM, inline  # noqa: E402

FONTS = (ROOT / 'content/brand/fonts').as_uri()
BASE = f"""
@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0400-045F; }}
@font-face {{ font-family: 'Unbounded'; font-weight: 200 900; src: url('{FONTS}/unbounded-latin-wght-normal.woff2') format('woff2'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-cyrillic-wght-normal.woff2') format('woff2'); unicode-range: U+0400-045F; }}
@font-face {{ font-family: 'Manrope'; font-weight: 200 800; src: url('{FONTS}/manrope-latin-wght-normal.woff2') format('woff2'); }}
* {{ box-sizing: border-box; }} html, body {{ margin: 0; overflow: hidden; }}
body {{ background: #151515; color: #F3F0E8; position: relative;
  background-image: linear-gradient(rgba(243,240,232,.05) 2px, transparent 2px), linear-gradient(90deg, rgba(243,240,232,.05) 2px, transparent 2px); }}
.plaque {{ display: inline-block; background: #F13A43; color: #fff; font-family: 'Unbounded'; font-weight: 800; text-transform: uppercase; transform: rotate(-3deg); }}
sub, sup {{ font-family: 'Manrope'; font-weight: 800; font-size: .6em; line-height: 0; }} sub {{ vertical-align: -.25em; }}
"""

# Шапка: всё важное — в безопасной зоне 1546×423 по центру (видна на всех устройствах).
BANNER = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
body {{ width: 2560px; height: 1440px; background-size: 96px 96px; }}
.safe {{ position: absolute; left: 507px; top: 508px; width: 1546px; height: 423px; display: flex; align-items: center; gap: 70px; }}
.safe .atom {{ position: static; width: 330px; height: 330px; transform: rotate(-12deg); flex: none; }}
h1 {{ margin: 0; font: 800 120px/1 'Unbounded'; text-transform: uppercase; letter-spacing: -.01em; }}
.plaque {{ margin-top: 26px; padding: 12px 28px 16px; font-size: 40px; }}
p {{ margin: 28px 0 0; font: 700 40px/1.3 'Manrope'; color: #B9B3A8; }}
.slash {{ position: absolute; top: -200px; bottom: -200px; width: 220px; background: #F13A43; transform: skewX(-14deg); opacity: .9; }}
</style></head><body>
<div class="slash" style="left:180px"></div><div class="slash" style="right:120px; width:90px"></div>
<div class="safe">{ATOM}<div><h1>Химия просто</h1><div class="plaque">подготовка к ЕНТ</div><p>Разборы тем и задач по химии · 11 класс</p></div></div>
</body></html>"""

THUMB = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
body {{ width: 1280px; height: 720px; background-size: 64px 64px; padding: 60px 70px; }}
.tag {{ font: 800 28px 'Manrope'; letter-spacing: .14em; color: #F3F0E8; display: flex; align-items: center; gap: 12px; }}
.tag i {{ width: 14px; height: 14px; border-radius: 50%; background: #F13A43; }}
h1 {{ margin: 40px 0 0; font: 800 132px/1 'Unbounded'; text-transform: uppercase; letter-spacing: -.02em; }}
.plaque {{ margin-top: 24px; padding: 14px 34px 20px; font-size: 92px; }}
.formula {{ position: absolute; right: 70px; bottom: 70px; padding: 22px 34px; background: #F3F0E8; color: #151515; font: 800 64px 'Unbounded'; transform: rotate(3deg); }}
.atom {{ position: absolute; right: 90px; top: 50px; width: 300px; height: 300px; transform: rotate(-12deg); }}
</style></head><body>
<div class="tag"><i></i>ХИМИЯ ДЛЯ ЕНТ</div><h1>Моль</h1><div class="plaque">за 10 минут</div>
{ATOM}<div class="formula">{inline('n = m / M')}</div>
</body></html>"""


def shot(doc: str, w: int, h: int, out: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / 'p.html'
        page.write_text(doc, encoding='utf-8')
        subprocess.run([chrome(), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        f'--window-size={w},{h}', f'--screenshot={out}', page.as_uri()], check=True, capture_output=True, timeout=120)


if __name__ == '__main__':
    out = ROOT / 'deliverables' / 'youtube'
    out.mkdir(parents=True, exist_ok=True)
    shot(BANNER, 2560, 1440, out / 'banner.png')
    shot(THUMB, 1280, 720, out / 'thumb-y001.png')
    print(f'YouTube art -> {out}')
