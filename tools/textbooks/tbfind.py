"""Search OCR texts of textbooks: tbfind.py <ocr_dir> <regex> [ids...] -> 'id p.N: line'"""
import re, sys, pathlib

sys.stdout.reconfigure(encoding='utf-8')
d, rx = pathlib.Path(sys.argv[1]), re.compile(sys.argv[2], re.I)
ids = sys.argv[3:]
files = [d / f'{i}.txt' for i in ids] if ids else sorted(d.glob('*.txt'))
for f in files:
    if not f.exists():
        continue
    page = 0
    for line in f.read_text('utf-8').splitlines():
        m = re.match(r'=== PDF p\. (\d+) ===', line)
        if m:
            page = int(m.group(1))
            continue
        if rx.search(line):
            print(f'{f.stem} p.{page}: {line.strip()[:110]}')
