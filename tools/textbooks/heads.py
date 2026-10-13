"""Find § headings in OCR body text: heads.py <ocr_dir> <out.txt> ids... -> 'id | § N | page | title'"""
import re, sys, pathlib

d, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
rx = re.compile(r'^\s*(?:§|S|\$|Ѕ|5|8)\s?(\d{1,3})\s?[.,]?\s+(.{4,90})$')
res = []
for code in sys.argv[3:]:
    page, seen = 0, {}
    lines = (d / f'{code}.txt').read_text('utf-8').splitlines()
    for i, line in enumerate(lines):
        m = re.match(r'=== PDF p\. (\d+) ===', line)
        if m:
            page = int(m.group(1)); continue
        h = rx.match(line)
        if not h:
            continue
        n, title = int(h.group(1)), h.group(2).strip()
        letters = re.sub(r'[^А-Яа-яЁё]', '', title)
        if len(letters) < 4:
            continue
        upper = sum(1 for c in letters if c.isupper()) / len(letters)
        if upper < 0.6 and not (i + 1 < len(lines) and False):
            continue
        if title.count('…') or re.search(r'\.{3,}|\d+\s*$', title):
            continue
        if n not in seen:
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if nxt and sum(1 for c in nxt if c.isupper()) > 0.6 * max(1, len(re.sub(r'[^А-Яа-яЁё]', '', nxt))):
                title += ' ' + nxt
            seen[n] = (page, title)
    res.append(f'##### {code}: {len(seen)} headings')
    for n in sorted(seen):
        res.append(f'§ {n} | p.{seen[n][0]} | {seen[n][1]}')
pathlib.Path(out).write_text('\n'.join(res), 'utf-8')
print('ok')
