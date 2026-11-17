"""Вопросы из тестов базы «Био-Хим Жалпы база» (PDF/DOCX с текстом) → JSON.

    python -I tools/base/extract_tests.py "<папка Файлы канала>" "<выход .json>"

Формат файлов: вопрос (с номером «N.» или без), затем строки «A) … B) … C) … D) …».
В «Нт 9 жауаптары» верный вариант помечен «+» в конце строки — его берём как ответ автора.
Файлы и тексты базы в Git не кладём: выход пишется в закрытую папку «00 Материалы…/База Био-Хим».
"""
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
TESTS = ['Нт 5 ', 'Нт 7.pdf', 'Нт 8.pdf', 'Нт 9 жауаптары.pdf', 'Нт 10.pdf', 'Нт 11.pdf', 'Нұсқа талдау 6.pdf']  # начало имени файла
OPT = re.compile(r'^\s*([ABCDАВСД])\s*[\)\.]\s*(.*)$')


def text_of(path: Path) -> str:
    return '\n'.join((p.extract_text() or '') for p in PdfReader(str(path)).pages)


def norm(s: str) -> str:
    s = s.replace('ə', 'ә').replace('Ə', 'Ә')  # латинская шва в PDF → казахская ә
    return re.sub(r'\s+', ' ', s).strip()


def parse(text: str) -> list[dict]:
    qs, cur = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = OPT.match(line)
        if m and cur is not None and len(cur['o']) < 4:
            body = m.group(2)
            right = body.rstrip().endswith('+')
            body = norm(body.rstrip().rstrip('+'))
            if right:
                cur['author'] = 'ABCD'[len(cur['o'])]
            cur['o'].append(body)
            continue
        if cur is not None and len(cur['o']) == 4 or cur is None:
            cur = {'q': '', 'o': [], 'author': ''}
            qs.append(cur)
        if cur['o']:  # продолжение последнего варианта
            cur['o'][-1] = norm(cur['o'][-1] + ' ' + line)
        else:
            cur['q'] = norm(cur['q'] + ' ' + re.sub(r'^\d+\s*[\.\)]\s*', '', line))
    return [q for q in qs if q['q'] and len(q['o']) == 4]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    bank = []
    for name in TESTS:
        f = next(p for p in sorted(SRC.iterdir()) if p.name.startswith(name) and p.suffix == '.pdf')
        qs = parse(text_of(f))
        for i, q in enumerate(qs, 1):
            bank.append({'id': f'{f.stem}#{i}', 'file': f.name, 'n': i, **q})
        print(f'{f.name:28} вопросов: {len(qs):3}  с ответом автора: {sum(1 for q in qs if q["author"])}')
    OUT.write_text(json.dumps(bank, ensure_ascii=False, indent=1), encoding='utf-8')
    print('всего', len(bank), '→', OUT)


if __name__ == '__main__':
    main()
