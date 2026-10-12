#!/usr/bin/env node
// Node 22+ and Chromium; no npm dependencies. Run: node content/brand/render-sketches.mjs
import {createServer} from 'node:http';
import {spawn} from 'node:child_process';
import {access, mkdir, mkdtemp, readFile, rm, writeFile} from 'node:fs/promises';
import {dirname, extname, join, resolve, sep} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';

const root = resolve(process.argv[2] || dirname(fileURLToPath(import.meta.url)));
const browserPath = process.env.CHROMIUM_PATH || '/usr/bin/chromium';
const frames = [1, 2, 3].flatMap(style => [
  {id: `style-${style}-avatar`, output: `style-${style}/avatar.png`, height: 1080},
  {id: `style-${style}-hook`, output: `style-${style}/frame-hook.png`, height: 1920},
  {id: `style-${style}-formula`, output: `style-${style}/frame-formula.png`, height: 1920},
]);
const mime = {'.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.ttf': 'font/ttf', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml'};
const resourceErrors = new Set();
const server = createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (pathname === '/favicon.ico') { response.writeHead(204).end(); return; }
    const path = resolve(root, `.${pathname}`);
    if (path !== root && !path.startsWith(root + sep)) {
      response.writeHead(403).end(); return;
    }
    const bytes = await readFile(path);
    response.writeHead(200, {'Content-Type': mime[extname(path)] || 'application/octet-stream',
      'Cache-Control': 'no-store'}).end(bytes);
  } catch (error) {
    resourceErrors.add(`${request.url}: ${error.code || error.message}`);
    response.writeHead(404).end();
  }
});

class DevTools {
  constructor(socket) {
    this.socket = socket;
    this.nextId = 0;
    this.pending = new Map();
    socket.addEventListener('message', event => {
      const reply = JSON.parse(event.data);
      const entry = this.pending.get(reply.id);
      if (!entry) return;
      this.pending.delete(reply.id);
      clearTimeout(entry.timer);
      if (reply.error) entry.reject(new Error(reply.error.message));
      else entry.resolve(reply.result);
    });
    socket.addEventListener('close', () => {
      for (const entry of this.pending.values()) {
        clearTimeout(entry.timer);
        entry.reject(new Error('Chromium closed the DevTools connection'));
      }
      this.pending.clear();
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.nextId;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`Chromium timed out: ${method}`));
      }, 20_000);
      this.pending.set(id, {resolve, reject, timer});
      this.socket.send(JSON.stringify({id, method, params, ...(sessionId ? {sessionId} : {})}));
    });
  }
}

let temporary;
let browser;
let client;
let browserLog = '';
try {
  if (typeof WebSocket !== 'function') throw new Error('Use Node 22 or newer (native WebSocket required)');
  await access(join(root, 'sketches.html'));
  await access(browserPath);
  temporary = await mkdtemp(join(tmpdir(), 'brand-sketches-'));
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  const origin = `http://127.0.0.1:${server.address().port}`;
  browser = spawn(browserPath, ['--headless', '--no-sandbox', '--disable-dev-shm-usage',
    '--no-first-run', '--no-default-browser-check', '--hide-scrollbars',
    '--force-device-scale-factor=1', '--remote-debugging-port=0',
    `--user-data-dir=${join(temporary, 'profile')}`, 'about:blank'], {
    stdio: ['ignore', 'ignore', 'pipe'],
    env: {...process.env, XDG_CONFIG_HOME: join(temporary, 'config'),
      XDG_CACHE_HOME: join(temporary, 'cache')},
  });
  const endpoint = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Chromium did not start DevTools')), 15_000);
    browser.once('error', error => { clearTimeout(timer); reject(error); });
    browser.once('exit', code => { clearTimeout(timer); reject(new Error(`Chromium exited (${code})`)); });
    browser.stderr.on('data', chunk => {
      browserLog = (browserLog + chunk.toString()).slice(-32_768);
      const match = browserLog.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (match) { clearTimeout(timer); resolve(match[1]); }
    });
  });
  const socket = new WebSocket(endpoint);
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('DevTools connection timed out')), 10_000);
    socket.addEventListener('open', () => {clearTimeout(timer); resolve();}, {once: true});
    socket.addEventListener('error', () => {clearTimeout(timer); reject(new Error('DevTools connection failed'));}, {once: true});
  });
  client = new DevTools(socket);
  const {targetId} = await client.send('Target.createTarget', {url: 'about:blank'});
  const {sessionId} = await client.send('Target.attachToTarget', {targetId, flatten: true});
  const page = (method, params) => client.send(method, params, sessionId);
  await page('Page.enable');
  await page('Runtime.enable');
  for (const frame of frames) {
    await page('Emulation.setDeviceMetricsOverride', {
      width: 1080, height: frame.height, deviceScaleFactor: 1, mobile: false,
    });
    const navigation = await page('Page.navigate', {url: `${origin}/sketches.html?frame=${frame.id}`});
    if (navigation.errorText) throw new Error(`${frame.id}: ${navigation.errorText}`);
    const ready = await page('Runtime.evaluate', {awaitPromise: true, returnByValue: true,
      expression: `(async () => {
        if (document.readyState !== 'complete') {
          await new Promise(resolve => window.addEventListener('load', resolve, {once: true}));
        }
        await document.fonts.ready;
        await Promise.all([...document.images].map(img => img.complete ? Promise.resolve() :
          new Promise((resolve, reject) => {
            img.addEventListener('load', resolve, {once: true});
            img.addEventListener('error', () => reject(new Error('Image failed: ' + img.src)), {once: true});
          })));
        const target = document.getElementById(${JSON.stringify(frame.id)});
        if (!target || !target.matches('article.canvas')) throw new Error('Missing article.canvas');
        const css = document.createElement('style');
        css.textContent = '* {animation: none !important; transition: none !important; caret-color: transparent !important}';
        document.head.append(css);
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        const rect = target.getBoundingClientRect();
        const fonts = [...document.fonts];
        const textSizes = [...target.querySelectorAll('*')].filter(el => {
          if (el.closest('.katex-mathml, .vlist-s')) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 1 && rect.height > 1 && style.visibility !== 'hidden' &&
            [...el.childNodes].some(node => node.nodeType === Node.TEXT_NODE && node.textContent.replace(/\u200B/g, '').trim());
        }).map(el => parseFloat(getComputedStyle(el).fontSize)).filter(Number.isFinite);
        return {width: rect.width, height: rect.height, x: rect.x, y: rect.y,
          minimumTextPx: textSizes.length ? Math.min(...textSizes) : null,
          visible: [...document.querySelectorAll('article.canvas')].filter(el => el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden').map(el => el.id),
          fonts: [...new Set(fonts.filter(font => font.status === 'loaded').map(font => font.family))],
          failedFonts: fonts.filter(font => font.status === 'error').map(font => font.family),
          failedImages: [...document.images].filter(img => !img.naturalWidth).map(img => img.src),
          katex: !!target.querySelector('.katex .katex-mathml')};
      })()`});
    if (ready.exceptionDetails) throw new Error(`${frame.id}: ${ready.exceptionDetails.exception?.description || ready.exceptionDetails.text}`);
    const state = ready.result.value;
    if (state.width !== 1080 || state.height !== frame.height || state.x !== 0 || state.y !== 0) {
      throw new Error(`${frame.id}: expected canvas at 0,0 sized 1080×${frame.height}; got ${JSON.stringify(state)}`);
    }
    if (frame.height === 1920 && (state.minimumTextPx === null || state.minimumTextPx < 39.99)) throw new Error(`${frame.id}: visible text below 40 px: ${state.minimumTextPx}`);
    if (state.visible.length !== 1 || state.visible[0] !== frame.id) throw new Error(`${frame.id}: query must reveal only this canvas`);
    if (state.failedFonts.length || state.failedImages.length) throw new Error(`${frame.id}: resource loading failed: ${JSON.stringify(state)}`);
    if (frame.id.endsWith('-formula') && !state.katex) throw new Error(`${frame.id}: no KaTeX formula found`);
    if (resourceErrors.size) throw new Error(`Local resources failed: ${[...resourceErrors].join('; ')}`);
    const screenshot = await page('Page.captureScreenshot', {format: 'png', fromSurface: true,
      captureBeyondViewport: false, clip: {x: 0, y: 0, width: 1080, height: frame.height, scale: 1}});
    const png = Buffer.from(screenshot.data, 'base64');
    if (!png.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10])) ||
      png.toString('ascii', 12, 16) !== 'IHDR' || png.readUInt32BE(16) !== 1080 || png.readUInt32BE(20) !== frame.height) {
      throw new Error(`${frame.id}: invalid PNG dimensions`);
    }
    await mkdir(dirname(join(root, frame.output)), {recursive: true});
    await writeFile(join(root, frame.output), png);
    console.log(`${frame.output}: 1080×${frame.height}; fonts: ${state.fonts.join(', ') || 'none (no text)'}`);
  }
  console.log('Rendered 9 PNG sketches.');
} catch (error) {
  console.error(error.message);
  if (browserLog) console.error(browserLog.trim());
  process.exitCode = 1;
} finally {
  if (client) {
    try { await client.send('Browser.close'); } catch {}
    client.socket.close();
  }
  if (browser && browser.exitCode === null) {
    await new Promise(resolve => {
      const timer = setTimeout(() => {browser.kill('SIGKILL'); resolve();}, 3000);
      browser.once('exit', () => {clearTimeout(timer); resolve();});
      browser.kill('SIGTERM');
    });
  }
  if (server.listening) await new Promise(resolve => server.close(resolve));
  if (temporary) await rm(temporary, {recursive: true, force: true});
}
