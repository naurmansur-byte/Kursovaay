// Контрольные кадры ролика одним браузером: node scripts/stills.mjs Y001 [доля сцены, по умолчанию 0.92]
// Берёт по кадру из каждой сцены (после `npx remotion bundle src/index.js --out-dir build`) → out/stills/<id>/<scene>.png
import { openBrowser, renderStill, selectComposition } from '@remotion/renderer';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const id = process.argv[2] || 'Y001';
const at = Number(process.argv[3] || 0.92);
const serveUrl = path.resolve('build');
const outDir = path.resolve('out/stills', id.toLowerCase());
await mkdir(outDir, { recursive: true });

const browser = await openBrowser('chrome');
const composition = await selectComposition({ serveUrl, id, puppeteerInstance: browser });
const onlyScenes = process.argv[4] ? new Set(process.argv[4].split(',')) : null;  // 3-й аргумент: только эти сцены
for (const s of composition.props.plan.scenes.filter((x) => !onlyScenes || onlyScenes.has(x.id))) {
  const frame = s.from + Math.floor(s.dur * at);
  await renderStill({ composition, serveUrl, frame, output: path.join(outDir, `${String(s.index).padStart(2, '0')}-${s.id}.png`), puppeteerInstance: browser, scale: 0.5 });
  console.log(s.id, frame);
}
await browser.close({ silent: true });
