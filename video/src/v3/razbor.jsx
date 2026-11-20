// Разбор пробника ЕНТ — светлый стиль (Мансур 20.11.2026: разборы — светлые, видео по темам — тёмные). 16:9.
// intro → (qN задание дословно + пауза, sN решение по шагам с разбором вариантов, aN ответ + ловушка) × N → outro.
// Строки решения: [текст с $TeX$, стем, запасной кадр, вид 'main' | 'ok' | 'no'].
import React, { useEffect, useState } from 'react';
import { AbsoluteFill, Audio, Sequence, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame } from 'remotion';
import katex from 'katex';
import '@fontsource-variable/unbounded';
import '@fontsource-variable/manrope';
import 'katex/dist/katex.min.css';
import { F } from '../theme.js';
import { wordFrame } from '../plan.js';
import { Sfx } from '../kit.jsx';

const FPS = 30;
const L = { bg: '#F6F4EE', ink: '#161616', muted: '#6E6A63', line: 'rgba(22,22,22,0.08)', card: '#FFFFFF', green: '#1F7A4A', greenSoft: '#D9F1E1', red: '#E2333C', redSoft: '#FCDDDE' };
const ACC = { chem: '#E2333C', bio: '#1F7A4A' };
const SERIF = '"Times New Roman", Times, serif';
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const sp = (f, s, cfg = { damping: 14, stiffness: 180, mass: 0.6 }) => (f < s ? 0 : spring({ frame: f - s, fps: FPS, config: cfg }));
const at = (scene, stem, fb = 0, nth = 0) => wordFrame(scene, FPS, stem, fb, nth);

const useFontsL = () => {
  const [h] = useState(() => delayRender('fonts-razbor'));
  useEffect(() => {
    Promise.all([document.fonts.load('800 100px "Unbounded Variable"', 'АБВ'), document.fonts.load('800 50px "Manrope Variable"', 'АБВ'), document.fonts.load('60px KaTeX_Main')])
      .then(() => continueRender(h), () => continueRender(h));
  }, [h]);
};

const Mixed = ({ value, size, color = L.ink, weight = 800, font = F.body }) => (
  <span style={{ fontFamily: font, fontWeight: weight, fontSize: size, lineHeight: 1.25, color }}>
    {value.split(/\$([^$]+)\$/).map((part, i) =>
      i % 2 ? <span key={i} style={{ fontSize: '1.08em', fontWeight: 400, whiteSpace: 'nowrap' }} dangerouslySetInnerHTML={{ __html: katex.renderToString(part, { throwOnError: false, strict: false, output: 'html' }) }} /> : <span key={i}>{part}</span>
    )}
  </span>
);

const Abs = ({ x, y, w, children, style }) => <div style={{ position: 'absolute', left: x, top: y, width: w, ...style }}>{children}</div>;

// Лист задания «как в тесте».
const Paper = ({ t, n, size = 50, optSize = 48, w = 1500, x = 210, y = 200, mode = 'plain', rightAt = 0, trapAt = 1e9, start = 0, dimWrong = true }) => {
  const f = useCurrentFrame();
  const p = sp(f, start);
  return (
    <Abs x={x} y={y} w={w} style={{ background: L.card, padding: '34px 44px 30px', boxShadow: '0 18px 50px rgba(0,0,0,0.12)', border: `1px solid ${L.line}`, transform: `translateY(${(1 - p) * 50}px)`, opacity: Math.min(1, p * 1.6) }}>
      <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 24, letterSpacing: '0.14em', color: L.muted, marginBottom: 14 }}>ЗАДАНИЕ {n} · ЕНТ · ОДИН ПРАВИЛЬНЫЙ ОТВЕТ</div>
      <div style={{ fontFamily: SERIF, fontSize: size, lineHeight: 1.22, color: L.ink }}><Mixed value={t.question} size={size} font={SERIF} weight={400} /></div>
      <div style={{ marginTop: 18, display: 'grid', gap: 6 }}>
        {t.options.map(([l, v]) => {
          const right = mode === 'answer' && l === t.right && f >= rightAt;
          const trap = mode === 'answer' && t.trap && l === t.trap && f >= trapAt;
          const dim = mode === 'answer' && dimWrong && !right && !trap && f >= rightAt;
          return (
            <div key={l} style={{ position: 'relative', display: 'flex', gap: 14, alignItems: 'center', padding: '4px 14px', background: right ? L.greenSoft : trap ? L.redSoft : 'transparent', borderLeft: `8px solid ${right ? L.green : trap ? L.red : 'transparent'}`, opacity: dim ? 0.35 : 1 }}>
              <span style={{ fontFamily: SERIF, fontWeight: 700, fontSize: optSize, color: L.ink }}>{l})</span>
              <Mixed value={v} size={optSize} font={SERIF} weight={400} />
              {right && <span style={{ marginLeft: 'auto', fontFamily: F.display, fontWeight: 800, fontSize: optSize, color: L.green }}>✓</span>}
              {trap && <div style={{ position: 'absolute', left: 70, right: 30, top: '52%', height: 4, background: L.red }} />}
            </div>
          );
        })}
      </div>
    </Abs>
  );
};

const Timer = ({ start, seconds = 4, x, y, size = 150, acc }) => {
  const f = useCurrentFrame();
  if (f < start) return null;
  const k = interpolate(f, [start, start + seconds * FPS], [0, 1], clamp);
  const left = Math.max(1, seconds - Math.floor((f - start) / FPS));
  const r = size / 2 - 10, c = 2 * Math.PI * r;
  return (
    <Abs x={x} y={y} style={{ width: size, height: size }}>
      {Array.from({ length: seconds }, (_, i) => <Sfx key={i} at={start + i * FPS} name="tick" volume={0.5} />)}
      <svg width={size} height={size} style={{ position: 'absolute', transform: 'rotate(-90deg)' }}>
        <circle cx={size / 2} cy={size / 2} r={r} stroke="rgba(22,22,22,0.12)" strokeWidth={14} fill="none" />
        <circle cx={size / 2} cy={size / 2} r={r} stroke={acc} strokeWidth={14} fill="none" strokeDasharray={c} strokeDashoffset={c * k} strokeLinecap="round" />
      </svg>
      <div style={{ position: 'absolute', inset: 0, display: 'grid', placeItems: 'center', fontFamily: F.display, fontWeight: 800, fontSize: size * 0.42, color: L.ink }}>{left}</div>
    </Abs>
  );
};

const Plaque = ({ children, bg, color = '#fff', size = 44, rotate = -1.5 }) => (
  <div style={{ display: 'inline-block', background: bg, color, padding: '10px 24px 14px', fontFamily: F.display, fontWeight: 800, fontSize: size, textTransform: 'uppercase', transform: `rotate(${rotate}deg)`, whiteSpace: 'nowrap' }}>{children}</div>
);

const Chip = ({ children, start }) => {
  const f = useCurrentFrame();
  const p = sp(f, start);
  if (f < start) return null;
  return <div style={{ transform: `scale(${0.7 + 0.3 * p})`, border: `3px solid ${L.ink}`, padding: '10px 22px 12px', fontFamily: F.body, fontWeight: 800, fontSize: 34, color: L.ink, textTransform: 'uppercase', whiteSpace: 'nowrap', background: L.card }}>{children}</div>;
};

export const makeRazbor = (cfg) => {
  const N = cfg.tasks.length;
  const acc = ACC[cfg.subject] || ACC.chem;

  const Intro = ({ scene }) => {
    const f = useCurrentFrame();
    const p = sp(f, 2);
    return (
      <AbsoluteFill>
        <Abs x={160} y={230} w={1600}>
          <div style={{ opacity: p, transform: `translateX(${(1 - p) * -120}px)`, fontFamily: F.display, fontWeight: 800, fontSize: 116, lineHeight: 1.02, color: L.ink, textTransform: 'uppercase' }} dangerouslySetInnerHTML={{ __html: cfg.title }} />
          <div style={{ marginTop: 26 }}>{f >= 10 && <Plaque bg={acc} size={56}>{cfg.plaque}</Plaque>}</div>
        </Abs>
        <Abs x={160} y={680} w={1600} style={{ display: 'flex', gap: 18 }}>
          {cfg.chips.map(([c, stem, fb], i) => <Chip key={i} start={at(scene, stem, fb)}>{c}</Chip>)}
        </Abs>
        <Sfx at={2} name="whoosh" /><Sfx at={10} name="pop" volume={0.4} />
      </AbsoluteFill>
    );
  };

  const Q = (n) => ({ scene }) => {
    const t = cfg.tasks[n - 1];
    const pauseAt = Math.max(30, scene.dur - 4 * FPS - 6);
    return (
      <AbsoluteFill>
        <Paper t={t} n={n} size={t.size ?? 60} optSize={t.optSize ?? 56} x={140} y={170} w={1400} start={2} />
        <Timer start={pauseAt} seconds={4} x={1600} y={230} size={170} acc={acc} />
        <Abs x={1590} y={420} w={200} style={{ textAlign: 'center', fontFamily: F.body, fontWeight: 800, fontSize: 30, color: L.muted }}>{useCurrentFrame() >= pauseAt ? 'ПАУЗА — РЕШИ' : ''}</Abs>
        <Sfx at={2} name="whoosh" volume={0.3} />
      </AbsoluteFill>
    );
  };

  const S = (n) => ({ scene }) => {
    const f = useCurrentFrame();
    const t = cfg.tasks[n - 1];
    const times = t.steps.map(([, stem, fb]) => at(scene, stem, fb));
    return (
      <AbsoluteFill>
        <Paper t={t} n={n} size={t.size ? 28 : 34} optSize={t.optSize ? 27 : 34} x={70} y={170} w={790} start={-30} />
        <Abs x={900} y={180} w={940}>
          <Plaque bg={L.ink} size={40}>Решение</Plaque>
          <div style={{ marginTop: 26, display: 'grid', gap: 16 }}>
            {t.steps.map(([v, , , kind], i) => {
              if (f < times[i]) return null;
              const p = sp(f, times[i]);
              const col = kind === 'no' ? L.red : kind === 'ok' ? L.green : kind === 'main' ? acc : 'rgba(22,22,22,0.18)';
              const mark = kind === 'no' ? '✗' : kind === 'ok' ? '✓' : kind === 'main' ? '→' : '•';
              return (
                <div key={i} style={{ display: 'flex', gap: 16, alignItems: 'flex-start', opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * 60}px)`, background: kind === 'main' ? '#fff' : 'transparent', padding: kind === 'main' ? '10px 16px' : '2px 16px', borderLeft: `8px solid ${col}` }}>
                  <span style={{ fontFamily: F.display, fontWeight: 800, fontSize: 36, color: col, lineHeight: 1.2 }}>{mark}</span>
                  <div><Mixed value={v} size={38} /></div>
                </div>
              );
            })}
          </div>
        </Abs>
        {times.map((x, i) => <Sfx key={i} at={x} name="pop" volume={0.3} />)}
      </AbsoluteFill>
    );
  };

  const A = (n) => ({ scene }) => {
    const f = useCurrentFrame();
    const t = cfg.tasks[n - 1];
    const r = scene.lead + 2;
    const tr = t.trapNote ? at(scene, 'ловушк', 60) : 1e9;
    const p = sp(f, r, { damping: 9, stiffness: 220, mass: 0.6 });
    return (
      <AbsoluteFill>
        <Paper t={t} n={n} size={t.size ?? 52} optSize={t.optSize ?? 50} x={140} y={170} w={1200} start={-30} mode="answer" rightAt={r} trapAt={t.trap ? tr : 1e9} />
        <Abs x={1400} y={240} w={420} style={{ transform: `scale(${0.4 + 0.6 * p}) rotate(-6deg)`, opacity: Math.min(1, p * 2), textAlign: 'center' }}>
          <div style={{ border: `10px solid ${L.green}`, padding: '16px 10px 22px', background: '#fff' }}>
            <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 40, color: L.green, letterSpacing: '0.1em' }}>ОТВЕТ</div>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 170, color: L.green, lineHeight: 1 }}>{t.right}</div>
          </div>
        </Abs>
        {t.trapNote && f >= tr && (
          <Abs x={160} y={t.noteY ?? 820} w={1600}>
            <div style={{ transform: `scale(${0.8 + 0.2 * sp(f, tr)})`, transformOrigin: 'left center', display: 'inline-block', background: L.redSoft, borderLeft: `10px solid ${L.red}`, padding: '14px 26px 16px' }}>
              <span style={{ fontFamily: F.display, fontWeight: 800, fontSize: 34, color: L.red, marginRight: 16 }}>ЛОВУШКА</span>
              <Mixed value={t.trapNote} size={36} />
            </div>
          </Abs>
        )}
        <Sfx at={r} name="ding" volume={0.5} />
        {t.trapNote && <Sfx at={tr} name="buzz" volume={0.3} />}
      </AbsoluteFill>
    );
  };

  const Outro = ({ scene }) => {
    const f = useCurrentFrame();
    const tCta = at(scene, 'запис', 200);
    const tSub = at(scene, 'подпишись', tCta + 90);
    return (
      <AbsoluteFill>
        <Abs x={160} y={170} w={1600}><Plaque bg={L.ink} size={52}>Что повторить</Plaque></Abs>
        <Abs x={160} y={320} w={1600} style={{ display: 'flex', flexWrap: 'wrap', gap: 16 }}>
          {cfg.review.map(([c, stem, fb], i) => <Chip key={i} start={at(scene, stem, fb)}>{c}</Chip>)}
        </Abs>
        {f >= tCta && (
          <Abs x={160} y={600} w={1600} style={{ opacity: sp(f, tCta) }}>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 72, color: L.ink }}>ХИМБИО ПРОСТО</div>
            <div style={{ marginTop: 14, display: 'flex', gap: 18, alignItems: 'center' }}>
              <Plaque bg={acc} size={44}>запись на курс</Plaque>
              <span style={{ fontFamily: F.body, fontWeight: 800, fontSize: 44, color: L.ink }}>директ Instagram @himbio.prosto</span>
            </div>
          </Abs>
        )}
        {f >= tSub && <Abs x={1360} y={860} w={400}><div style={{ transform: `scale(${0.6 + 0.4 * sp(f, tSub)}) rotate(3deg)`, background: L.red, color: '#fff', borderRadius: 60, padding: '18px 34px', fontFamily: F.display, fontWeight: 800, fontSize: 36, textAlign: 'center' }}>ПОДПИСАТЬСЯ</div></Abs>}
        <Sfx at={tCta} name="whoosh" /><Sfx at={tSub} name="ding" volume={0.45} />
      </AbsoluteFill>
    );
  };

  // Оболочка: светлый фон с сеткой, верхняя полоса с прогрессом, субтитры, склейка-шторка.
  const Top = ({ plan }) => {
    const f = useCurrentFrame();
    const cur = plan.scenes.find((s) => f >= s.from && f < s.from + s.dur);
    const m = cur && cur.id.match(/^[qsa](\d+)$/);
    const n = m ? +m[1] : null;
    const done = plan.scenes.filter((s) => /^a\d+$/.test(s.id) && f >= s.from + s.dur).length;
    return (
      <>
        <div style={{ position: 'absolute', left: 80, top: 52, fontFamily: F.body, fontWeight: 800, fontSize: 28, letterSpacing: '0.14em', color: L.ink, display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ width: 14, height: 14, borderRadius: '50%', background: acc, display: 'inline-block' }} />ХИМБИО ПРОСТО · {cfg.label}
        </div>
        {n && <div style={{ position: 'absolute', right: 80, top: 40, background: L.ink, color: '#fff', padding: '8px 22px 10px', fontFamily: F.body, fontWeight: 800, fontSize: 30, letterSpacing: '0.1em' }}>ЗАДАНИЕ {n}/{N}</div>}
        <div style={{ position: 'absolute', left: 80, right: 80, top: 112, height: 6, background: 'rgba(22,22,22,0.08)' }}>
          <div style={{ width: `${(done / N) * 100}%`, height: '100%', background: acc }} />
        </div>
      </>
    );
  };

  const Subs = ({ plan, hide }) => {
    const f = useCurrentFrame();
    const s = plan.scenes.find((x) => f >= x.from && f < x.from + x.dur);
    if (!s || hide.some((h) => (h instanceof RegExp ? h.test(s.id) : h === s.id))) return null;
    const ws = s.words.map((w) => ({ t: w.t.replace(/[«»"]/g, '').trim(), a: s.from + s.lead + Math.round((w.start / 1000) * FPS) })).filter((w) => w.t);
    const lines = [];
    let cur = [];
    for (const w of ws) {
      const len = cur.reduce((a, x) => a + x.t.length + 1, 0) + w.t.length;
      if (cur.length && (len > 26 || cur.length >= 4 || /[.!?:]$/.test(cur[cur.length - 1].t))) { lines.push(cur); cur = []; }
      cur.push(w);
    }
    if (cur.length) lines.push(cur);
    const line = [...lines].reverse().find((l) => f >= l[0].a);
    if (!line) return null;
    return (
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 44, display: 'flex', justifyContent: 'center' }}>
        <div style={{ background: L.ink, padding: '10px 26px 14px', display: 'flex', gap: 12 }}>
          {line.map((w, i) => {
            const on = f >= w.a && (i === line.length - 1 || f < line[i + 1].a);
            return <span key={i} style={{ fontFamily: F.body, fontWeight: 800, fontSize: 40, color: f < w.a ? 'rgba(255,255,255,0.4)' : on ? acc === ACC.bio ? '#7FE0A3' : '#FF8A8F' : '#fff' }}>{w.t.replace(/[.,!?:]$/, '')}</span>;
          })}
        </div>
      </div>
    );
  };

  const Wipe = ({ plan }) => {
    const f = useCurrentFrame();
    const s = plan.scenes.find((x) => x.index > 0 && f >= x.from && f < x.from + 9);
    if (!s) return null;
    const k = (f - s.from) / 9;
    return <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${interpolate(k, [0, 1], [-30, 110])}%`, width: '22%', background: acc, opacity: 0.9, transform: 'skewX(-12deg)' }} />;
  };

  const SCENES = { intro: Intro, outro: Outro };
  const TAILS = { intro: 20, outro: 60 };
  for (let n = 1; n <= N; n++) {
    SCENES[`q${n}`] = Q(n); SCENES[`s${n}`] = S(n); SCENES[`a${n}`] = A(n);
    TAILS[`q${n}`] = 4 * FPS + 10; TAILS[`s${n}`] = 24; TAILS[`a${n}`] = 30;
  }

  const Comp = ({ plan }) => {
    useFontsL();
    return (
      <AbsoluteFill style={{ background: L.bg }}>
        <AbsoluteFill style={{ backgroundImage: `linear-gradient(${L.line} 1px, transparent 1px), linear-gradient(90deg, ${L.line} 1px, transparent 1px)`, backgroundSize: '64px 64px' }} />
        {plan.scenes.map((s) => {
          const Scene = SCENES[s.id];
          return (
            <Sequence key={s.id} from={s.from} durationInFrames={s.dur} name={s.id}>
              <Scene scene={s} />
              {s.audio && <Sequence from={s.lead}><Audio src={staticFile(s.audio)} /></Sequence>}
            </Sequence>
          );
        })}
        <Top plan={plan} />
        <Subs plan={plan} hide={['intro', 'outro']} />
        <Wipe plan={plan} />
      </AbsoluteFill>
    );
  };

  return { SCENES, TAILS, Comp };
};
