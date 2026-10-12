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

const timing = { id: script.id, scenes: [] };
for (const scene of script.scenes) {
  const file = path.join(outDir, `${scene.id}.mp3`);
  const tts = new EdgeTTS({
    voice: script.voice,
    lang: 'ru-RU',
    outputFormat: 'audio-24khz-96kbitrate-mono-mp3',
    rate: script.rate || '+0%',
    saveSubtitles: true,
    timeout: 30000,
  });
  await tts.ttsPromise(scene.text, file);
  const words = JSON.parse(await readFile(`${file}.json`, 'utf8')).map((w) => ({ t: w.part, start: w.start, end: w.end }));
  await rm(`${file}.json`);
  const speechEnd = words.length ? words[words.length - 1].end : 1000;
  timing.scenes.push({ id: scene.id, audio: `audio/${reel}/${scene.id}.mp3`, speechEndMs: speechEnd, words });
  console.log(`${scene.id}: ${(speechEnd / 1000).toFixed(2)} s, ${words.length} words`);
}
await writeFile(path.join(root, 'src/reels', `${reel}.timing.json`), JSON.stringify(timing, null, 2));
const total = timing.scenes.reduce((s, x) => s + x.speechEndMs, 0) / 1000;
console.log(`Speech total ${total.toFixed(1)} s -> src/reels/${reel}.timing.json`);
