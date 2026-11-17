"""Банк вопросов из базы «Био-Хим Жалпы база»: переводы ru_*.py + оригиналы тесты_kk.json → банк по неделям.

    python -I tools/base/build_bank.py "<папка Банк вопросов>"

Пишет в ту же закрытую папку (вне Git): банк_ru.json, «Банк вопросов — по неделям.md», «Банк вопросов.csv» (для Excel).
Статусы: ок — можно брать после сверки преподавателем; проверить — сверить с учебником; спорно — переписать;
вне курса — не брать; дубль — повтор другого вопроса.
"""
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

DIR = Path(sys.argv[1])
WEEKS = {1: 'Клетка', 2: 'Вещества клетки', 3: 'Мембрана и ферменты', 4: 'АТФ, дыхание, фотосинтез', 5: 'Питание и пищеварение',
         6: 'Транспорт, кровь, кровообращение', 7: 'Дыхание', 8: 'Выделение и кожа', 9: 'Опора и движение', 10: 'Нервная система и органы чувств',
         11: 'Гормоны', 12: 'Деление клетки', 13: 'Размножение и развитие', 14: 'ДНК и генетический код', 15: 'Законы Менделя',
         16: 'Пол, группы крови, взаимодействие генов', 17: 'Изменчивость и селекция', 18: 'Систематика и многообразие', 19: 'Эволюция',
         20: 'Экология', 21: 'Микробы, болезни, биотехнологии', 22: 'Методы биологии'}


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FILE, mod.Q


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    kk = {q['id']: q for q in json.loads((DIR / 'тесты_kk.json').read_text(encoding='utf-8'))}
    bank = []
    for f in sorted(DIR.glob('ru_*.py')):
        file, rows = load(f)
        stem = Path(file).stem
        for n, q, opts, ans, week, status, note in rows:
            src = kk.get(f'{stem}#{n}', {})
            assert len(opts) == 4, (file, n)
            assert ans in ('', 'A', 'B', 'C', 'D'), (file, n)
            assert ans or status in ('спорно', 'вне курса'), (file, n, status)
            bank.append(dict(id=f'{stem}#{n}', file=file, n=n, week=week, status='дубль' if status.startswith('дубль') else status, dup=status if status.startswith('дубль') else '',
                             q=q, o=opts, a=ans, author=src.get('author', ''), note=note, q_kk=src.get('q', ''), o_kk=src.get('o', [])))
    # сверка с ответами автора, где они есть
    clash = [b for b in bank if b['author'] and b['a'] and b['author'] != b['a']]
    (DIR / 'банк_ru.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1), encoding='utf-8')

    st = Counter(b['status'] for b in bank)
    usable = [b for b in bank if b['status'] in ('ок', 'проверить')]
    by_week = defaultdict(list)
    for b in usable:
        by_week[b['week']].append(b)
    L = ['# Банк вопросов из базы «Био-Хим Жалпы база» — по неделям курса биологии', '',
         'Закрытый файл, не для учеников и не для Git. Перевод с казахского по смыслу; ответы определены по конспектам и учебникам НЦТ, '
         'у «Нт 9» сверены с ответами автора. Это вопросы автора канала в формате ЕНТ, а не задания НЦТ.', '',
         f'Всего вопросов: {len(bank)}. Можно брать: {st["ок"]} «ок» и {st["проверить"]} «проверить» (сверить с учебником). '
         f'Не брать: {st["спорно"]} «спорно», {st["вне курса"]} «вне курса», {st["дубль"]} дублей.', '',
         f'Расхождения с ответами автора: {len(clash)}.' + (' ' + '; '.join(f"{b['id']}: автор {b['author']}, у нас {b['a']}" for b in clash) if clash else ''), '',
         '| Неделя | Тема | Вопросов |', '|---|---|---|']
    L += [f'| {w} | {WEEKS[w]} | {len(by_week.get(w, []))} |' for w in WEEKS]
    for w in WEEKS:
        qs = by_week.get(w, [])
        if not qs:
            continue
        L += ['', f'## Неделя {w}. {WEEKS[w]} — {len(qs)}', '']
        for b in qs:
            mark = '' if b['status'] == 'ок' else ' · проверить'
            L.append(f"**{b['q']}** _({b['id']}{mark})_  ")
            L.append('  '.join(f"{'**' if L_ == b['a'] else ''}{L_}) {o}{'**' if L_ == b['a'] else ''}" for L_, o in zip('ABCD', b['o'])) + '  ')
            if b['note']:
                L.append(f"_Заметка: {b['note']}_")
            L.append('')
    bad = [b for b in bank if b['status'] in ('спорно', 'вне курса')]
    L += ['', f'## Не берём — {len(bad)}', '', '| Вопрос | Статус | Почему |', '|---|---|---|']
    L += [f"| {b['id']}: {b['q']} | {b['status']} | {b['note']} |" for b in bad]
    (DIR / 'Банк вопросов — по неделям.md').write_text('\n'.join(L) + '\n', encoding='utf-8')

    import csv
    with open(DIR / 'Банк вопросов.csv', 'w', encoding='utf-8-sig', newline='') as fh:  # BOM — чтобы Excel понял кириллицу
        w = csv.writer(fh, delimiter=';')
        w.writerow(['id', 'Неделя', 'Тема', 'Статус', 'Вопрос', 'A', 'B', 'C', 'D', 'Ответ', 'Ответ автора', 'Заметка', 'Оригинал (каз.)'])
        for b in sorted(bank, key=lambda x: (x['week'], x['id'])):
            w.writerow([b['id'], b['week'], WEEKS[b['week']], b['dup'] or b['status'], b['q'], *b['o'], b['a'], b['author'], b['note'], b['q_kk']])
    xl = 'csv'
    print(f'{len(bank)} вопросов: {dict(st)}; можно брать {len(usable)}; расхождений с автором {len(clash)}; {xl}')
    print('по неделям:', {w: len(v) for w, v in sorted(by_week.items())})


if __name__ == '__main__':
    main()
