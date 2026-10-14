# Учебники: распознавание и поиск

Инструменты Макса для учебной базы (`course/textbooks/`). Сами учебники лежат в `_textbooks/` (в `.gitignore`): `pdf/` — исходники, `img/` — склеенные страницы, `ocr/` — текст по страницам (`=== PDF p. N ===`). Номер файла — ID на okulyk.kz; список — `course/textbooks/README.md`.

Python — из `.venv` с флагом `-I` (файлы скачаны из интернета; скрипты лежат отдельно от данных).

```powershell
# 1. Скачать книгу (нужен Referer; ID — из таблицы)
curl.exe -s -A "Mozilla/5.0" -e "https://okulyk.kz/download-pdf/?527" -o "_textbooks\pdf\527.pdf" "https://pdf.okulyk.kz/527/527.pdf"

# 2. Склеить полосы страниц в PNG (×2 для распознавания)
.\.venv\Scripts\python.exe -I tools\textbooks\pdfimgs.py "$PWD\_textbooks\pdf" "$PWD\_textbooks\img" 2 527

# 3. Распознать (Windows OCR, русский; ~100 с на книгу)
.\tools\textbooks\ocr.ps1 -ImgRoot "$PWD\_textbooks\img" -OutRoot "$PWD\_textbooks\ocr" -Ids 527

# Поиск по всем книгам: книга, страница, строка
[Console]::OutputEncoding = [Text.Encoding]::UTF8
.\.venv\Scripts\python.exe -I tools\textbooks\tbfind.py "$PWD\_textbooks\ocr" "Шванн|Шлейден" 527 528

# Сверка справочников фактов (course/ent-base) со всеми учебниками -> таблица
.\.venv\Scripts\python.exe -I tools\textbooks\factcheck.py "$PWD\_textbooks\ocr" factcheck.md

# Заголовки параграфов по тексту (для карты INDEX)
.\.venv\Scripts\python.exe -I tools\textbooks\heads.py "$PWD\_textbooks\ocr" heads.txt 350 527

# Вырезки страниц для сверки чисел: книга:страница:верх:низ[:лево:право] (доли страницы)
.\.venv\Scripts\python.exe -I tools\textbooks\crop.py <папка> 527:89:0.6:0.7 450:74:0.3:0.95
```

Биология 8 (346) имеет текстовый слой: текст берётся `pypdf` напрямую (`page.extract_text()`), маркеры страниц те же.

Ограничения: распознавание ~90 %; формулы, индексы, числа и фамилии в переносах теряются. Отсутствие в поиске — повод посмотреть страницу (`_textbooks/img/<ID>/pNNNN.png`), а не доказательство. Всё, что идёт в выжимку, Макс сверяет по картинке страницы.
