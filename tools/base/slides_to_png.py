"""Слайды-сканы из PDF базы → PNG по странице (самая крупная картинка страницы).

    python -I tools/base/slides_to_png.py "<pdf>" "<папка>" [первая] [последняя]

Имена p001.png … — их читает tools/textbooks/ocr.ps1 (Windows OCR) и Read для просмотра.
"""
import io
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader

pdf, out = Path(sys.argv[1]), Path(sys.argv[2])
first = int(sys.argv[3]) if len(sys.argv) > 3 else 1
r = PdfReader(str(pdf))
last = int(sys.argv[4]) if len(sys.argv) > 4 else len(r.pages)
out.mkdir(parents=True, exist_ok=True)
n = 0
for i in range(first - 1, last):
    ims = r.pages[i].images
    if not ims:
        continue
    best = max(ims, key=lambda im: len(im.data))
    img = Image.open(io.BytesIO(best.data)).convert('RGB')
    if img.width > 1600:
        img = img.resize((1600, int(img.height * 1600 / img.width)))
    img.save(out / f'p{i + 1:03d}.png')
    n += 1
print('ok', n, 'из', len(r.pages))
