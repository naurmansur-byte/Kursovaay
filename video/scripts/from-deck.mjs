// Видео-урок из презентации: manifest.json + PNG (tools/slides/lesson_deck.py --manifest) -> src/reels/<id>.script.json и public/youtube/<id>/.
// Запуск: node scripts/from-deck.mjs ../exports/youtube/Y001 y001 [rate]
import { copyFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [deckDir, id, rate = '-4%'] = process.argv.slice(2);
const manifest = JSON.parse(await readFile(path.resolve(root, deckDir, 'manifest.json'), 'utf8'));
const pub = path.join(root, 'public/youtube', id);
await mkdir(pub, { recursive: true });
const scenes = [];
for (const [k, page] of manifest.entries()) {
  const sid = `p${String(k + 1).padStart(2, '0')}`;
  await copyFile(path.resolve(root, deckDir, 'png', page.png), path.join(pub, `${sid}.png`));
  scenes.push({ id: sid, text: page.voice || '' });
}
await writeFile(path.join(root, 'src/reels', `${id}.script.json`),
  JSON.stringify({ id: id.toUpperCase(), voice: 'ru-RU-DmitryNeural', rate, scenes }, null, 2));
console.log(`${scenes.length} slides -> public/youtube/${id}, src/reels/${id}.script.json`);
