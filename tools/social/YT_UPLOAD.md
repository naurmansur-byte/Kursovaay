# Догрузка видео на YouTube через Chrome (ноябрь 2026)

Решение Мансура 18.11.2026: ролики и Shorts — через YouTube Studio в Chrome (не Metricool), по плану 19–21.11, всё в 10:00, сразу в плейлисты. Концовка «старт 1 ноября» отрезана (`trim_outro.py`), тексты — `yt_plan.py` → `u/yt/plan.json`, `u/yt/meta.json`.

Без проверки канала YouTube даёт **10 загрузок за 24 часа** (окно скользящее: место освобождается через сутки после каждой загрузки). Проверку (телефон + код) проходит только Мансур. Пароли, телефон, коды не вводить.

## Порядок одного запуска

1. Инструменты Claude in Chrome — одной загрузкой ToolSearch: `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__file_upload,mcp__claude-in-chrome__find,mcp__claude-in-chrome__computer`.
2. Очередь: `.venv/Scripts/python.exe tools/social/yt_queue.py` — по строке на видео: `id`, `day` (число ноября для публикации), `file` или `parts` + `size`. Пусто — всё загружено, закончить.
3. `tabs_context_mcp` → новая вкладка → `https://studio.youtube.com/channel/UCcOi8TQWVWLYnOjxLTHM-DA/videos/short` (аккаунт уже вошёл; если просит вход — остановиться, сообщить Мансуру).
4. Вставить **весь текст** `tools/social/yt_studio_helper.js` в `javascript_tool` (eval и `<script>` Studio не пускает). Ответ: `helpers v4 ready`.
5. `find` → ссылки на input «claude meta-in», «claude vid-in», «claude p1»…«claude p4». `file_upload` `u/yt/meta.json` в meta-in, затем JS: `window.__META = JSON.parse(await document.getElementById('meta-in').files[0].text()); Object.keys(__META).length` → 46.
6. Для каждого видео очереди по порядку:
   - Short: `file_upload` его `file` в vid-in. Длинное: 4 отдельных `file_upload` частей в p1…p4 (каждая < 10 МБ). **Каждый `file_upload` — отдельным сообщением, без JS рядом** (иначе рвётся связь); если связь оборвалась — проверить `document.getElementById('p1').files[0]?.name` и повторить только недошедшее.
   - JS: `__run('R004', {day: 19})` или `__run('Y009', {day: 19, parts: 4, size: 30195580})`.
   - Ждать итога короткими вызовами (каждый < 45 с): `await __waitFor(() => !__busy, 40000); JSON.stringify(__log['R004'])`. Длинным видео нужно до нескольких минут.
   - `{ok: true, …}` → `.venv/Scripts/python.exe tools/social/yt_queue.py --done R004`, дальше.
   - `{error: 'limit'}` → `await __closeUpload()` (черновик не остаётся). Окно скользящее: подождать ~5 минут (несколько вызовов `await __sleep(40000)`) и повторить это же видео; после 6 неудачных попыток подряд — закончить запуск.
   - Любая другая ошибка → скриншот, не нажимать «Запланировать» вручную наугад; `__closeUpload()`, повторить видео один раз; снова ошибка — закончить и описать.
7. В конце: закрыть свою вкладку; дописать в `STATUS.md` (раздел YouTube) одну строку: дата, что загружено, на какие дни, сколько осталось; коммит `YouTube: догрузка ДД.ММ` и `git pull -q --rebase && git push -q`.

Что делает `__run`: «Создать → Добавить видео», название и описание из meta, «Нет, не для детей», «Изменённый контент — да», плейлисты из meta (личные «Коран», «Domi», «Тед» не трогает — снимает только то, чего нет в списке видео, а их там никогда нет), «Доступ → Запланировать», число в календаре, 10:00, «Запланировать». Свои значки (обложки) без проверки канала недоступны — не ставим.
