"""Stitch the image strips of each PDF page into one PNG (optionally upscaled).
Usage: pdfimgs.py <pdf_dir> <img_dir> <scale> [ids...]"""
import io, sys, pathlib
from pypdf import PdfReader
from PIL import Image

src, dst, scale = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), float(sys.argv[3])
ids = set(sys.argv[4:])
for f in sorted(src.glob('*.pdf')):
    if ids and f.stem not in ids:
        continue
    od = dst / f.stem
    od.mkdir(parents=True, exist_ok=True)
    r = PdfReader(str(f))
    n = 0
    for i, p in enumerate(r.pages, 1):
        out = od / f'p{i:04d}.png'
        if out.exists():
            n += 1
            continue
        try:
            strips = [Image.open(io.BytesIO(im.data)).convert('L') for im in p.images]
        except Exception as e:
            print(f.stem, i, 'ERR', e)
            continue
        if not strips:
            continue
        w = max(s.width for s in strips)
        page = Image.new('L', (w, sum(s.height for s in strips)), 255)
        y = 0
        for s in strips:
            page.paste(s, (0, y))
            y += s.height
        if scale != 1:
            page = page.resize((int(page.width * scale), int(page.height * scale)), Image.LANCZOS)
        page.save(out)
        n += 1
    print(f.stem, len(r.pages), 'pages', n, 'images', flush=True)
