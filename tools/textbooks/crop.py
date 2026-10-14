"""Вырезает полосы со страниц учебника для сверки чисел и формулировок.

    .venv/Scripts/python.exe -I tools/textbooks/crop.py <out_dir> <book>:<page>:<top>:<bottom>[:<left>:<right>] ...

book — номер книги okulyk (527, 450, 702 ...), page — номер страницы PDF,
top/bottom/left/right — доли страницы от 0 до 1. Узкие вырезки (до 800 px)
увеличиваются в 2 раза, широкие сжимаются до 1200 px. Файлы: <out_dir>/<book>-p<page>-<n>.png.
Картинки страниц лежат в _textbooks/img/<book>/pNNNN.png (вне Git).
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    out = Path(argv[0])
    out.mkdir(parents=True, exist_ok=True)
    for n, spec in enumerate(argv[1:], 1):
        parts = spec.split(':')
        book, page = parts[0], int(parts[1])
        top, bottom = float(parts[2]), float(parts[3])
        left, right = (float(parts[4]), float(parts[5])) if len(parts) >= 6 else (0.0, 1.0)
        im = Image.open(ROOT / '_textbooks' / 'img' / book / f'p{page:04d}.png')
        w, h = im.size
        c = im.crop((int(w * left), int(h * top), int(w * right), int(h * bottom)))
        if c.width <= 800:
            c = c.resize((c.width * 2, c.height * 2))
        elif c.width > 1200:
            c = c.resize((1200, int(c.height * 1200 / c.width)))
        dst = out / f'{book}-p{page}-{n}.png'
        c.save(dst)
        print(dst, c.size)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
