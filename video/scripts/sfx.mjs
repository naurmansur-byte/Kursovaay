// Синтез звуковых эффектов в public/sfx/*.wav. Звуки сгенерированы кодом — права на них наши.
// Запуск: npm run sfx
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SR = 44100;
const out = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../public/sfx');
await mkdir(out, { recursive: true });

const wav = (samples) => {
  const buf = Buffer.alloc(44 + samples.length * 2);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + samples.length * 2, 4); buf.write('WAVE', 8);
  buf.write('fmt ', 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 2, 28); buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34);
  buf.write('data', 36); buf.writeUInt32LE(samples.length * 2, 40);
  samples.forEach((s, i) => buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, s)) * 32767), 44 + i * 2));
  return buf;
};
const gen = (sec, fn) => Array.from({ length: Math.round(sec * SR) }, (_, i) => fn(i / SR, sec));
let seed = 7;
const noise = () => ((seed = (seed * 16807) % 2147483647) / 2147483647) * 2 - 1;

// Свист пролёта: шум с плавающим фильтром.
let lp = 0;
const whoosh = gen(0.42, (t, d) => {
  const cut = 0.02 + 0.25 * Math.sin((Math.PI * t) / d);
  lp += cut * (noise() - lp);
  return lp * 1.8 * Math.sin((Math.PI * t) / d) ** 2;
});
// Щелчок-поп: тон с падением высоты.
const pop = gen(0.12, (t) => Math.sin(2 * Math.PI * (900 - 4500 * t) * t) * Math.exp(-t * 38) * 0.8);
// Звонок правильного ответа.
const ding = gen(0.9, (t) => (Math.sin(2 * Math.PI * 1318.5 * t) + 0.5 * Math.sin(2 * Math.PI * 1975.5 * t)) * Math.exp(-t * 5) * 0.45);
// Гудок ошибки.
const buzz = gen(0.38, (t) => Math.sign(Math.sin(2 * Math.PI * (110 + 6 * Math.sin(40 * t)) * t)) * Math.exp(-t * 6) * 0.22);
// Удар: низкий тон с падением.
const boom = gen(0.55, (t) => (Math.sin(2 * Math.PI * (70 - 40 * t) * t) * 0.9 + noise() * Math.exp(-t * 40) * 0.25) * Math.exp(-t * 7));
// Тик таймера.
const tick = gen(0.03, (t) => Math.sin(2 * Math.PI * 2200 * t) * Math.exp(-t * 180) * 0.5);

for (const [name, s] of Object.entries({ whoosh, pop, ding, buzz, boom, tick })) {
  await writeFile(path.join(out, `${name}.wav`), wav(s));
}
console.log('sfx ->', out);
