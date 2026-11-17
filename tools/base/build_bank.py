"""Банк вопросов из базы «Био-Хим Жалпы база»: переводы ru_*.py и факты_*.py → банк по неделям курса.

    python -I tools/base/build_bank.py "<папка Банк вопросов>"

Файл перевода: FILE, SUBJECT ('bio' по умолчанию или 'chem') и списки
  Q — (номер, вопрос, [A–D], ответ, неделя, статус, заметка);
  M — несколько ответов: (номер, вопрос, [6 вариантов], 'буквы', неделя, статус, заметка);
  F — факты без вариантов: (номер, вопрос, ответ, неделя, статус, заметка).
Пишет в ту же закрытую папку (вне Git): банк_ru.json, «Банк вопросов — по неделям.md», «Банк вопросов.csv».
Статусы: ок — брать после сверки преподавателем; проверить — сверить с учебником; спорно — переписать; вне курса — не брать;
дубль — повтор.
"""
import csv
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

DIR = Path(sys.argv[1])
WEEKS = {
    'bio': {1: 'Клетка', 2: 'Вещества клетки', 3: 'Мембрана и ферменты', 4: 'АТФ, дыхание, фотосинтез', 5: 'Питание и пищеварение',
            6: 'Транспорт, кровь, кровообращение', 7: 'Дыхание', 8: 'Выделение и кожа', 9: 'Опора и движение', 10: 'Нервная система и органы чувств',
            11: 'Гормоны и регуляция у растений', 12: 'Деление клетки', 13: 'Размножение и развитие', 14: 'ДНК и генетический код', 15: 'Законы Менделя',
            16: 'Пол, группы крови, взаимодействие генов', 17: 'Изменчивость и селекция', 18: 'Систематика и многообразие', 19: 'Эволюция',
            20: 'Экология', 21: 'Микробы, болезни, биотехнологии', 22: 'Методы биологии'},
    'chem': {1: 'Язык химии', 2: 'Формулы и доли', 3: 'Классы веществ', 4: 'Моль', 5: 'Растворы и выход', 6: 'Атом и ПЗ', 7: 'Связь и решётки',
             8: 'Электролиты и гидролиз', 9: 'ОВР', 10: 'Электролиз', 11: 'Теплота и скорость', 12: 'Равновесие', 13: 'Металлы', 14: 'Al и переходные металлы',
             15: 'C, Si, N, P', 16: 'Галогены, O, S', 17: 'Алканы и галогенпроизводные', 18: 'Непредельные, арены, нефть', 19: 'Спирты, фенол, альдегиды',
             20: 'Кислоты, эфиры, жиры', 21: 'Углеводы, амины, белки', 22: 'Полимеры'},
}
SUBJ = {'bio': 'Биология', 'chem': 'Химия'}


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm_status(s: str) -> str:
    return 'дубль' if s.startswith('дубль') else s


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    kk = {q['id']: q for q in json.loads((DIR / 'тесты_kk.json').read_text(encoding='utf-8'))}
    bank, facts = [], []
    for f in sorted(list(DIR.glob('ru_*.py')) + list(DIR.glob('факты_*.py'))):
        mod = load(f)
        subj, stem = getattr(mod, 'SUBJECT', 'bio'), Path(mod.FILE).stem
        for n, q, opts, ans, week, status, note in getattr(mod, 'Q', []):
            src = kk.get(f'{stem}#{n}', {})
            assert len(opts) == 4 and ans in ('', 'A', 'B', 'C', 'D'), (stem, n)
            assert ans or status in ('спорно', 'вне курса'), (stem, n, status)
            bank.append(dict(id=f'{stem}#{n}', subject=subj, kind='one', week=week, status=norm_status(status), dup=status if status.startswith('дубль') else '',
                             q=q, o=opts, a=ans, author=src.get('author', ''), note=note, q_kk=src.get('q', '')))
        for n, q, opts, ans, week, status, note in getattr(mod, 'M', []):
            assert len(opts) == 6 and set(ans) <= set('ABCDEF'), (stem, n)
            bank.append(dict(id=f'{stem}#{n}', subject=subj, kind='multi', week=week, status=norm_status(status), dup='', q=q, o=opts, a=ans,
                             author='', note=note, q_kk=''))
        for n, q, a, week, status, note in getattr(mod, 'F', []):
            facts.append(dict(id=f'{stem}#{n}', subject=subj, week=week, status=norm_status(status), q=q, a=a, note=note))
    clash = [b for b in bank if b['author'] and b['a'] and b['author'] != b['a']]
    (DIR / 'банк_ru.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1), encoding='utf-8')
    (DIR / 'факты_ru.json').write_text(json.dumps(facts, ensure_ascii=False, indent=1), encoding='utf-8')

    ok = ('ок', 'проверить')
    L = ['# Банк вопросов из базы «Био-Хим Жалпы база» — по неделям курса', '',
         'Закрытый файл: не для учеников и не для Git. Перевод с казахского по смыслу. Ответы определены по конспектам курса и учебникам НЦТ; '
         'где у автора есть ответы («Нт 9», «Теория талдау 4»), они сверены. Это вопросы автора канала в формате ЕНТ, а не задания НЦТ. '
         'Перед тем как взять вопрос в пробник, его проверяет преподаватель.', '',
         f'Расхождения с ответами автора: {len(clash)}.', '']
    stats = []
    for subj in ('bio', 'chem'):
        qs = [b for b in bank if b['subject'] == subj]
        fs = [x for x in facts if x['subject'] == subj]
        if not qs and not fs:
            continue
        st = Counter(b['status'] for b in qs)
        good = [b for b in qs if b['status'] in ok]
        goodf = [x for x in fs if x['status'] in ok]
        stats.append(f"{SUBJ[subj]}: вопросов {len(qs)} (брать {len(good)}), фактов {len(fs)} (брать {len(goodf)}); {dict(st)}")
        by_week = defaultdict(list)
        for b in good:
            by_week[b['week']].append(b)
        byf = defaultdict(list)
        for x in goodf:
            byf[x['week']].append(x)
        L += [f'# {SUBJ[subj]}', '', f'Вопросов {len(qs)}: можно брать {st["ок"]} «ок» и {st["проверить"]} «проверить»; '
              f'не брать — {st["спорно"]} «спорно», {st["вне курса"]} «вне курса», {st["дубль"]} дублей. Фактов без вариантов: {len(goodf)}.', '',
              '| Неделя | Тема | Вопросов | Фактов |', '|---|---|---|---|']
        L += [f'| {w} | {t} | {len(by_week.get(w, []))} | {len(byf.get(w, []))} |' for w, t in WEEKS[subj].items()]
        for w, t in WEEKS[subj].items():
            if not by_week.get(w) and not byf.get(w):
                continue
            L += ['', f'## {SUBJ[subj]}, неделя {w}. {t}', '']
            for b in by_week.get(w, []):
                mark = '' if b['status'] == 'ок' else ' · проверить'
                letters = 'ABCDEF'[:len(b['o'])]
                L.append(f"**{b['q']}**{' (несколько ответов)' if b['kind'] == 'multi' else ''} _({b['id']}{mark})_  ")
                L.append('  '.join(f"{'**' if x in b['a'] else ''}{x}) {o}{'**' if x in b['a'] else ''}" for x, o in zip(letters, b['o'])) + '  ')
                if b['note']:
                    L.append(f"_Заметка: {b['note']}_")
                L.append('')
            if byf.get(w):
                L += ['Факты (вопрос → ответ):', '']
                L += [f"- {x['q']} → **{x['a']}** _({x['id']}{' · проверить' if x['status'] == 'проверить' else ''})_" for x in byf[w]]
                L.append('')
        bad = [b for b in qs if b['status'] in ('спорно', 'вне курса')] + [x for x in fs if x['status'] in ('спорно', 'вне курса')]
        L += ['', f'## {SUBJ[subj]}: не берём — {len(bad)}', '', '| Источник | Вопрос | Статус | Почему |', '|---|---|---|---|']
        L += [f"| {b['id']} | {b['q']} | {b['status']} | {b['note']} |" for b in bad]
        L.append('')
    (DIR / 'Банк вопросов — по неделям.md').write_text('\n'.join(L) + '\n', encoding='utf-8')

    with open(DIR / 'Банк вопросов.csv', 'w', encoding='utf-8-sig', newline='') as fh:  # BOM — чтобы Excel понял кириллицу
        w = csv.writer(fh, delimiter=';')
        w.writerow(['Предмет', 'id', 'Неделя', 'Тема', 'Вид', 'Статус', 'Вопрос', 'A', 'B', 'C', 'D', 'E', 'F', 'Ответ', 'Ответ автора', 'Заметка', 'Оригинал (каз.)'])
        for b in sorted(bank, key=lambda x: (x['subject'], x['week'], x['id'])):
            o = b['o'] + [''] * (6 - len(b['o']))
            w.writerow([SUBJ[b['subject']], b['id'], b['week'], WEEKS[b['subject']][b['week']], 'несколько' if b['kind'] == 'multi' else 'один',
                        b['dup'] or b['status'], b['q'], *o, b['a'], b['author'], b['note'], b['q_kk']])
        for x in sorted(facts, key=lambda x: (x['subject'], x['week'], x['id'])):
            w.writerow([SUBJ[x['subject']], x['id'], x['week'], WEEKS[x['subject']][x['week']], 'факт', x['status'], x['q'], '', '', '', '', '', '', x['a'], '', x['note'], ''])
    print('\n'.join(stats))
    print('расхождений с автором:', len(clash), [(b['id'], b['author'], b['a']) for b in clash])


if __name__ == '__main__':
    main()
