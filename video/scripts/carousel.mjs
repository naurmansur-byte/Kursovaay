// Слайды карусели одним браузером: node scripts/carousel.mjs AboutHB 5 → out/carousel/AboutHB-1.png …
// Нужен свежий бандл (npx remotion bundle src/index.js --out-dir build). Кадр 45 — анимации уже встали.
import { openBrowser, renderStill, selectComposition } from '@remotion/renderer';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const [prefix = 'AboutHB', count = '5'] = process.argv.slice(2);
const serveUrl = path.resolve(process.env.BUILD || 'build');  // BUILD=build-alt, если build занят рендером
const outDir = path.resolve('out/carousel');
await mkdir(outDir, { recursive: true });
const browser = await openBrowser('chrome');
for (let n = 1; n <= Number(count); n++) {
  const id = `${prefix}-${n}`;
  const composition = await selectComposition({ serveUrl, id, puppeteerInstance: browser });
  await renderStill({ composition, serveUrl, frame: 45, output: path.join(outDir, `${id}.png`), puppeteerInstance: browser });
  console.log(id);
}
await browser.close({ silent: true });
