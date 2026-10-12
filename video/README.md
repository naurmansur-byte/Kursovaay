# Видео «Химия просто»

Reels и YouTube собирает Макс на ПК Мансура. Стек: Remotion 4 (React) + KaTeX + Edge TTS (`node-edge-tts`). Стиль 2 — `src/theme.js`.

## Установка (один раз)

Нужен Node.js LTS (`winget install OpenJS.NodeJS.LTS`). Затем в папке `video/`:

```
npm install
```

При первом рендере Remotion сам скачивает Chrome Headless Shell.

## Сборка ролика

```
npm run tts -- r001                                   # озвучка → public/audio/r001/*.mp3 и src/reels/r001.timing.json
npx remotion bundle src/index.js --out-dir build      # сборка проекта
npx remotion still build R001 out/stills/f150.png --frame=150   # проверочный кадр
npx remotion render build R001 out/R001.mp4 --codec=h264 --audio-codec=aac --crf=20
```

Готовый MP4 копируется в `deliverables/R001/` (в репозитории) для просмотра на пульте.

## Как устроено

- `src/reels/r001.script.json` — текст озвучки по сценам; меняешь текст → снова `npm run tts`.
- `src/reels/r001.jsx` — сцены. Анимации привязаны к словам озвучки через `wordFrame` (`src/plan.js`).
- `src/plan.js` — длительность сцен по реальной длине аудио, субтитры по 1–2 слова.
- `src/kit.jsx` — общие элементы стиля: кинетический текст, плашки, карточки, формулы KaTeX, атом, варианты ответа.
- `src/Reel.jsx` — фон, прогресс по сценам, субтитры, переходы, звук.

Новый ролик: `src/reels/rNNN.script.json` + `rNNN.jsx`, подключить в `Reel.jsx` (REELS) и `Root.jsx`.

## Лицензии и ограничения

- Remotion: бесплатно для физлиц и компаний до 3 сотрудников; при росте команды нужна платная лицензия (remotion.dev/license).
- Шрифты Unbounded и Manrope — SIL OFL 1.1 (пакеты Fontsource), KaTeX — MIT.
- **Edge TTS** обращается к онлайн-сервису озвучки Microsoft Edge без официального договора. Условия коммерческого использования не подтверждены: перед публикацией нужно решение Мансура (оставить или перейти на сервис с явной лицензией).
- Фоновой музыки нет: нужна музыка с лицензией.
