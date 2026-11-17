"""Слайды «вопрос → ответ» из PDF базы (например, «Нт-1»): страница с вопросом, следующая — тот же вопрос и ответ.

    python -I tools/base/slides_qa.py "<pdf>" "<выход .json>"

В PDF текст набран с разрядкой («К ө м е й  с а ң …»): одиночный пробел — между буквами, двойной — между словами.
Служебные строки автора (контакты) отбрасываются.
"""
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

SKIP = re.compile(r'ТЕЛЕГРАМ|ВАТСАП|ИНСТАГРАМ|ҚАЛДАРЫҢ|^\d+$', re.I)


def unspace(line: str) -> str:
    words = re.split(r'\s{2,}', line.strip())
    return ' '.join(w.replace(' ', '') for w in words if w)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    pdf, out = Path(sys.argv[1]), Path(sys.argv[2])
    pages = []
    for p in PdfReader(str(pdf)).pages:
        lines = [unspace(x) for x in (p.extract_text() or '').splitlines()]
        pages.append([x for x in lines if x and not SKIP.search(x)])
    qa, i = [], 0
    while i < len(pages):
        ja = ' '.join(pages[i]).strip()
        jb = ' '.join(pages[i + 1]).strip() if i + 1 < len(pages) else ''
        if ja.endswith(':') and jb.startswith(ja) and len(jb) > len(ja):
            qa.append({'id': f'{pdf.stem}#{len(qa) + 1}', 'q': ja.rstrip(':').strip(), 'a': jb[len(ja):].strip()})
            i += 2
            continue
        if ':' in ja and not ja.endswith(':'):  # вопрос и ответ на одной странице
            q, _, ans = ja.partition(':')
            qa.append({'id': f'{pdf.stem}#{len(qa) + 1}', 'q': q.strip(), 'a': ans.strip()})
        i += 1
    out.write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(qa), 'пар →', out)
    for x in qa[:4]:
        print(' ', x['q'], '→', x['a'])


if __name__ == '__main__':
    main()
