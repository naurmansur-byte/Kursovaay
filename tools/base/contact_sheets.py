"""Листы-превью слайдов (по 6 на лист, с номером страницы) для чтения сканов глазами.

    python -I tools/base/contact_sheets.py "<папка с pNNN.png>" "<папка выхода>" [на лист]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

src, out = Path(sys.argv[1]), Path(sys.argv[2])
per = int(sys.argv[3]) if len(sys.argv) > 3 else 6
out.mkdir(parents=True, exist_ok=True)
files = sorted(src.glob('p*.png'))
W, H, cols = 760, 430, 2
for k in range(0, len(files), per):
    chunk = files[k:k + per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new('RGB', (W * cols, H * rows), 'white')
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        im = Image.open(f).convert('RGB')
        im.thumbnail((W - 10, H - 10))
        x, y = (i % cols) * W + 5, (i // cols) * H + 5
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 70, y + 30], fill='black')
        d.text((x + 8, y + 8), f.stem, fill='white')
    sheet.save(out / f'sheet_{k // per + 1:02d}.jpg', quality=82)
print('листов', (len(files) + per - 1) // per)
