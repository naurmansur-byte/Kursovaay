// Озвучка сцен через Edge TTS: public/audio/<id>/<scene>.mp3 + тайминги слов в src/reels/<id>.timing.json.
// Запуск: npm run tts -- r001
import { createRequire } from 'node:module';
import { mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { EdgeTTS } = require('node-edge-tts');

const reel = (process.argv[2] || 'r001').toLowerCase();
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const script = JSON.parse(await readFile(path.join(root, 'src/reels', `${reel}.script.json`), 'utf8'));
const outDir = path.join(root, 'public/audio', reel);
await mkdir(outDir, { recursive: true });

// --only id1,id2 — переозвучить только эти сцены; остальные берутся из прежнего timing.json, если текст не менялся.
const onlyArg = process.argv.indexOf('--only');
const only = onlyArg > 0 ? new Set(process.argv[onlyArg + 1].split(',')) : null;
const timingPath = path.join(root, 'src/reels', `${reel}.timing.json`);
const previous = only ? JSON.parse(await readFile(timingPath, 'utf8')).scenes : [];

// Аббревиатуры — по буквам (просьба Мансура: «ЕНТ» — чётко «Е-Эн-Тэ», а не слово). В тайминге буквы снова склеиваются в аббревиатуру.
const SPELL = { ЕНТ: ['Е', 'Эн', 'Тэ'], НЦТ: ['Эн', 'Цэ', 'Тэ'] };
const speak = (text) => Object.entries(SPELL).reduce(
  (s, [abbr, letters]) => s.replace(new RegExp(`(?<![А-Яа-яЁё])${abbr}(?![А-Яа-яЁё])`, 'g'), letters.join(' ')), text);
const unspell = (words) => {
  const out = [];
  for (let i = 0; i < words.length; i++) {
    const hit = Object.entries(SPELL).find(([, ls]) => ls.every((l, k) => words[i + k] && words[i + k].t.trim().replace(/[.,!?:;—«»]+$/, '') === l));
    if (!hit) { out.push(words[i]); continue; }
    const [abbr, ls] = hit;
    const last = words[i + ls.length - 1];
    out.push({ t: abbr + last.t.trim().slice(ls[ls.length - 1].length) + ' ', start: words[i].start, end: last.end });
    i += ls.length - 1;
  }
  return out;
};

const timing = { id: script.id, scenes: [] };
for (const scene of script.scenes) {
  const old = previous.find((s) => s.id === scene.id);
  if (only && !only.has(scene.id) && old) {
    timing.scenes.push(old);
    continue;
  }
  if (!scene.text) {  // слайд без озвучки — короткая пауза
    timing.scenes.push({ id: scene.id, audio: null, speechEndMs: 1800, words: [] });
    continue;
  }
  const file = path.join(outDir, `${scene.id}.mp3`);
  const tts = new EdgeTTS({
    voice: script.voice,
    lang: 'ru-RU',
    outputFormat: 'audio-24khz-96kbitrate-mono-mp3',
    rate: script.rate || '+0%',
    saveSubtitles: true,
    timeout: 30000,
  });
  // Edge TTS иногда отвечает 429 — повторить с нарастающей паузой.
  for (let attempt = 1; ; attempt++) {
    try {
      await tts.ttsPromise(speak(scene.text), file);
      break;
    } catch (e) {
      if (attempt >= 6) throw e;
      console.log(`${scene.id}: ${e.message}, retry ${attempt}`);
      await new Promise((r) => setTimeout(r, 5000 * attempt));
    }
  }
  const words = unspell(JSON.parse(await readFile(`${file}.json`, 'utf8')).map((w) => ({ t: w.part, start: w.start, end: w.end })));
  await rm(`${file}.json`);
  const speechEnd = words.length ? words[words.length - 1].end : 1000;
  timing.scenes.push({ id: scene.id, audio: `audio/${reel}/${scene.id}.mp3`, speechEndMs: speechEnd, words });
  console.log(`${scene.id}: ${(speechEnd / 1000).toFixed(2)} s, ${words.length} words`);
}
await writeFile(path.join(root, 'src/reels', `${reel}.timing.json`), JSON.stringify(timing, null, 2));
const total = timing.scenes.reduce((s, x) => s + x.speechEndMs, 0) / 1000;
console.log(`Speech total ${total.toFixed(1)} s -> src/reels/${reel}.timing.json`);
