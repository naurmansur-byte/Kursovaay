# T08 — ученические материалы недель 1–2

Семь файлов переписаны по новому STYLE: короткие фразы, front matter и блоки rule/trap/example/try. Задания, числовые данные, ID, баллы и длительности сохранены. По новому решению Мансура сначала проходит урок: после него ученик читает конспект, выполняет закрепление и всю общую часть G1–G8. После второго урока — один вариант A/B/C и исправления. Общая нагрузка прежняя: 25 + 20 + 35 + 30 + 25 + 15 = 150 минут. Исходные ключи преподавателя не изменены. Материалы ждут проверки Макса.

**PDF ещё не собраны.** Пробная печать через `tools/handout/handout.py` завершилась таймаутом Chromium через 120 секунд. По T08 сборка оставлена Максу. Метаданные и преобразование разметки в ученический HTML проверены для всех семи файлов.

| Неделя | Материал | Исходник для проверки и печати |
|---|---|---|
| 1 | Закрепление после урока 1 | [pre-work.md](../../course/week-01/pre-work.md) |
| 1 | ДЗ | [homework.md](../../course/week-01/homework.md) |
| 1 | Контроль без ключа | [quiz-student.md](week-01/quiz-student.md) |
| 2 | Конспект | [notes-student.md](../../course/week-02/notes-student.md) |
| 2 | Закрепление после урока 3 | [pre-work.md](../../course/week-02/pre-work.md) |
| 2 | ДЗ | [homework.md](../../course/week-02/homework.md) |
| 2 | Контроль без ключа | [quiz-student.md](week-02/quiz-student.md) |

Для контроля использовать копии `quiz-student.md` из этой папки: исходные `course/week-0N/quiz.md` сохраняют преподавательский раздел, а генератор печатает весь переданный файл. Копии содержат только ученическую часть.

После установки пакета `markdown` и при доступном Chrome/Chromium — из корня репозитория:

```bash
python tools/handout/handout.py course/week-01/pre-work.md deliverables/T08/week-01/pre-work.pdf
python tools/handout/handout.py course/week-01/homework.md deliverables/T08/week-01/homework.pdf
python tools/handout/handout.py deliverables/T08/week-01/quiz-student.md deliverables/T08/week-01/quiz.pdf
python tools/handout/handout.py course/week-02/notes-student.md deliverables/T08/week-02/notes-student.pdf
python tools/handout/handout.py course/week-02/pre-work.md deliverables/T08/week-02/pre-work.pdf
python tools/handout/handout.py course/week-02/homework.md deliverables/T08/week-02/homework.pdf
python tools/handout/handout.py deliverables/T08/week-02/quiz-student.md deliverables/T08/week-02/quiz.pdf
```

Осталось собрать эти семь PDF, проверить вёрстку и закоммитить готовые файлы. Презентации и материалы преподавателя в T08 не пересобирались. Максу также нужно согласовать прежние README и планы недель с новым порядком выдачи материалов: в них ещё встречается предварительное чтение и разделение общей части ДЗ между уроками и после второго урока.
