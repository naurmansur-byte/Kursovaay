// Монтаж v2 (19.11.2026, на пробу Мансуру): всё крупно и по центру, удар-зум на каждой склейке,
// караоке-субтитры по словам, таймер на раздумье, рисованные анимации (клетка, мембрана), финал «запись на курс».
import React, { useEffect, useState } from 'react';
import { AbsoluteFill, Audio, Sequence, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import '@fontsource-variable/unbounded';
import '@fontsource-variable/manrope';
import 'katex/dist/katex.min.css';
import { C, F, SUBJECT, setSubject } from '../theme.js';
import { wordFrame } from '../plan.js';
import { Background, Sfx, TeX } from '../kit.jsx';

export const FPS = 30;
export const RED = '#F13A43';
export const GREEN = '#3FBF74';  // светлый зелёный для текста и галочек на чёрном (фирменный #1F7A4A — для заливок)
export const W = 1080;
// Светлый акцент для текста на чёрном: химия — светло-красный, биология — светло-зелёный.
export const HOT = () => (C.accent === SUBJECT.chem ? '#FF6B70' : GREEN);
const isChem = () => C.accent === SUBJECT.chem;
export const GUT = 72;

export const useFonts2 = () => {
  const [handle] = useState(() => delayRender('fonts-v2'));
  useEffect(() => {
    Promise.all([
      document.fonts.load('800 100px "Unbounded Variable"', 'АБВ'),
      document.fonts.load('800 50px "Manrope Variable"', 'АБВ'),
      document.fonts.load('60px KaTeX_Main'),
    ]).then(() => continueRender(handle), () => continueRender(handle));
  }, [handle]);
};

export const at = (scene, stem, fallback = 0, nth = 0) => wordFrame(scene, FPS, stem, fallback, nth);
export const sp = (frame, start, cfg = { damping: 13, stiffness: 190, mass: 0.6 }) =>
  frame < start ? 0 : spring({ frame: frame - start, fps: FPS, config: cfg });
export const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };

// Элемент по центру на высоте y.
export const Center = ({ y, children, style }) => (
  <div style={{ position: 'absolute', top: y, left: GUT, right: GUT, display: 'flex', justifyContent: 'center', ...style }}>{children}</div>
);

// Появление «пружиной» снизу с увеличением.
export const Pop = ({ start = 0, y, children, from = 0.6, dy = 60 }) => {
  const f = useCurrentFrame();
  const p = sp(f, start);
  if (f < start) return null;
  return (
    <Center y={y}>
      <div style={{ transform: `translateY(${(1 - p) * dy}px) scale(${from + (1 - from) * p})`, opacity: Math.min(1, p * 1.6) }}>{children}</div>
    </Center>
  );
};

// Крупный заголовок (Unbounded).
export const Big = ({ children, size = 120, color = C.fg, align = 'center', lh = 1.02 }) => (
  <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: lh, color, textAlign: align, textTransform: 'uppercase', letterSpacing: '-0.01em' }}>{children}</div>
);

// Плашка: цветной фон, тёмный или светлый текст.
export const Plaque = ({ children, bg = C.accent, color = C.fg, size = 64, rotate = -2, pad = '14px 30px 20px' }) => (
  <div style={{ background: bg, color, padding: pad, fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: 1.05, textTransform: 'uppercase', transform: `rotate(${rotate}deg)`, textAlign: 'center' }}>{children}</div>
);

// Чип-проверка: «✓ по градиенту» / «✗ АТФ».
export const Chip = ({ ok = true, tone, children, size = 52 }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 18, background: C.card, border: `3px solid ${tone ?? (ok ? GREEN : RED)}`, padding: '12px 28px 16px', fontFamily: F.body, fontWeight: 800, fontSize: size, color: C.fg }}>
    <span style={{ color: tone ?? (ok ? GREEN : RED), fontSize: size * 1.1 }}>{ok ? '✓' : '✗'}</span>
    {children}
  </div>
);

// Речь сцены словами: каждое слово проявляется, когда звучит (кинетический текст вопроса).
export const Spoken = ({ scene, y, size = 84, skip = 0, color = C.fg, accentWords = [] }) => {
  const f = useCurrentFrame();
  const words = scene.words.slice(skip);
  return (
    <div style={{ position: 'absolute', top: y, left: GUT, right: GUT, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: `${size * 0.12}px ${size * 0.28}px` }}>
      {words.map((w, i) => {
        const s = scene.lead + Math.round((w.start / 1000) * FPS);
        const p = sp(f, s, { damping: 12, stiffness: 240, mass: 0.5 });
        const t = w.t.trim();
        const hot = accentWords.some((a) => t.toLowerCase().startsWith(a));
        return (
          <span key={i} style={{ fontFamily: F.body, fontWeight: 800, fontSize: size, lineHeight: 1.1, color: hot ? HOT() : color, opacity: f < s ? 0.12 : 1, transform: `translateY(${(1 - p) * 24}px)`, display: 'inline-block' }}>
            {t}
          </span>
        );
      })}
    </div>
  );
};

// Таймер-кольцо: 3 → 2 → 1, щелчок каждую секунду.
export const TimerRing = ({ start = 0, seconds = 3, y = 1180, size = 300 }) => {
  const f = useCurrentFrame();
  const len = seconds * FPS;
  const k = interpolate(f, [start, start + len], [0, 1], clamp);
  const left = Math.max(1, seconds - Math.floor((f - start) / FPS));
  const r = size / 2 - 16;
  const c = 2 * Math.PI * r;
  const beat = f >= start ? 1 + 0.1 * Math.max(0, 1 - ((f - start) % FPS) / 8) : 1;
  return (
    <>
      {Array.from({ length: seconds }, (_, i) => <Sfx key={i} at={start + i * FPS} name="tick" volume={0.6} />)}
      <Center y={y}>
        <div style={{ position: 'relative', width: size, height: size, transform: `scale(${beat})` }}>
          <svg width={size} height={size} style={{ position: 'absolute', inset: 0, transform: 'rotate(-90deg)' }}>
            <circle cx={size / 2} cy={size / 2} r={r} stroke={C.faint} strokeWidth={22} fill="none" />
            <circle cx={size / 2} cy={size / 2} r={r} stroke={HOT()} strokeWidth={22} fill="none" strokeDasharray={c} strokeDashoffset={c * k} strokeLinecap="round" />
          </svg>
          <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: F.display, fontWeight: 800, fontSize: size * 0.48, color: C.fg }}>{left}</div>
        </div>
      </Center>
    </>
  );
};

// Полоса обратного отсчёта (пауза на ответ в блице).
export const CountBar = ({ start, len, y = 1180 }) => {
  const f = useCurrentFrame();
  if (f < start) return null;
  const k = interpolate(f, [start, start + len], [1, 0], clamp);
  return (
    <>
      <Sfx at={start} name="tick" volume={0.6} />
      <Sfx at={start + Math.round(len / 2)} name="tick" volume={0.6} />
      <div style={{ position: 'absolute', top: y, left: GUT + 60, right: GUT + 60, height: 26, background: C.faint }}>
        <div style={{ width: `${k * 100}%`, height: '100%', background: HOT() }} />
      </div>
      <Center y={y + 46}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 40, letterSpacing: '0.12em', color: C.muted }}>ДУМАЙ…</div></Center>
    </>
  );
};

// Вариант ответа во всю ширину.
export const Opt = ({ letter, text, state = 'idle', start = 0, y }) => {
  const f = useCurrentFrame();
  const p = sp(f, start);
  if (f < start) return null;
  const right = state === 'right';
  const dim = state === 'dim';
  const bg = right ? '#1F7A4A' : C.card;
  const border = right ? GREEN : dim ? C.faint : C.fg;
  return (
    <div style={{ position: 'absolute', top: y, left: GUT, right: GUT, height: 140, display: 'flex', alignItems: 'center', gap: 30, padding: '0 36px', background: bg, border: `4px solid ${border}`, boxShadow: right ? `0 0 60px ${GREEN}66` : 'none', opacity: (dim ? 0.35 : 1) * Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * 120}px)` }}>
      <div style={{ width: 84, height: 84, borderRadius: '50%', background: right ? C.fg : 'transparent', border: `4px solid ${right ? C.fg : border}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: F.display, fontWeight: 800, fontSize: 46, color: right ? '#1F7A4A' : C.fg }}>{letter}</div>
      <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 58, color: C.fg }}>{text}</div>
    </div>
  );
};

// Штамп «НЕТ!»: падает сверху, трясёт кадр.
export const Stamp = ({ start, text, y = 560, color = RED }) => {
  const f = useCurrentFrame();
  if (f < start) return null;
  const p = sp(f, start, { damping: 9, stiffness: 260, mass: 0.6 });
  return (
    <>
      <Sfx at={start} name="buzz" volume={0.45} />
      <Center y={y}>
        <div style={{ transform: `scale(${2.4 - 1.4 * p}) rotate(-8deg)`, opacity: Math.min(1, p * 2), border: `14px solid ${color}`, padding: '10px 50px 26px', fontFamily: F.display, fontWeight: 800, fontSize: 230, color, lineHeight: 1 }}>{text}</div>
      </Center>
    </>
  );
};

// Растительная клетка: progress 0 — тургор, 1 — плазмолиз; salt — точки соли снаружи; flow — стрелки воды наружу.
export const PlantCell = ({ size = 560, progress = 0, salt = 0, flow = 0, t = 0 }) => {
  const d = 22 + progress * 95;
  const vac = d + 50;
  const dots = [[40, 90], [90, 520], [530, 60], [560, 330], [30, 300], [300, 30], [300, 575], [520, 540], [70, 30], [575, 160], [20, 450], [450, 20]];
  const arrow = (x1, y1, x2, y2, k) => {
    const o = (t % 30) / 30;
    const ax = x1 + (x2 - x1) * o * 0.4;
    const ay = y1 + (y2 - y1) * o * 0.4;
    const bx = ax + (x2 - x1) * 0.6;
    const by = ay + (y2 - y1) * 0.6;
    const ang = Math.atan2(by - ay, bx - ax);
    return (
      <g key={k} opacity={flow}>
        <line x1={ax} y1={ay} x2={bx} y2={by} stroke="#6FA8FF" strokeWidth={10} strokeLinecap="round" />
        <polygon points={`${bx},${by} ${bx - 26 * Math.cos(ang - 0.5)},${by - 26 * Math.sin(ang - 0.5)} ${bx - 26 * Math.cos(ang + 0.5)},${by - 26 * Math.sin(ang + 0.5)}`} fill="#6FA8FF" />
      </g>
    );
  };
  return (
    <svg width={size} height={size} viewBox="0 0 600 600">
      {dots.map(([x, y], i) => <circle key={i} cx={x} cy={y} r={10} fill={C.fg} opacity={salt * 0.75} />)}
      <rect x={90} y={90} width={420} height={420} rx={50} fill="none" stroke="#5E9E3A" strokeWidth={30} />
      <rect x={105 + d} y={105 + d} width={390 - 2 * d} height={390 - 2 * d} rx={30 + progress * 120} fill="#1F7A4A" fillOpacity={0.55} stroke={GREEN} strokeWidth={6} />
      <rect x={105 + vac} y={105 + vac} width={Math.max(20, 390 - 2 * vac)} height={Math.max(20, 390 - 2 * vac)} rx={40 + progress * 80} fill="#6FA8FF" fillOpacity={0.35} stroke="#6FA8FF" strokeWidth={4} />
      <circle cx={105 + d + 48} cy={105 + d + 48} r={24} fill={C.fg} opacity={0.85} />
      {arrow(300, 300 - 150 + d, 300, 30, 'u')}
      {arrow(300, 300 + 150 - d, 300, 570, 'd')}
      {arrow(300 - 150 + d, 300, 30, 300, 'l')}
      {arrow(300 + 150 - d, 300, 570, 300, 'r')}
    </svg>
  );
};

// Мембрана с белком. mode: 'carrier' — глюкоза сверху вниз по градиенту; 'pump' — Na⁺ снизу вверх против градиента + вспышка АТФ.
export const Membrane = ({ mode = 'carrier', t = 0, atp = 0, w = 936, h = 640, top = 'кровь', bottom = 'клетка' }) => {
  const mid = h / 2;
  const heads = [];
  for (let x = 14; x < w; x += 30) {
    if (Math.abs(x - w / 2) < 80) continue;
    heads.push(x);
  }
  const pump = mode === 'pump';
  const color = pump ? '#F2C94C' : C.fg;
  // Частицы: много с одной стороны, мало с другой.
  const many = [[90, 70], [210, 120], [330, 60], [620, 90], [740, 140], [860, 70], [150, 190], [800, 210], [420, 150], [560, 180]];
  const few = [[170, h - 120], [770, h - 95]];
  const hi = many.map(([x, y]) => [x, 70 + y * 0.62]);  // верх: много (снаружи / в крови)
  const lo = few;  // низ: мало
  const P = ({ x, y, s = 1, k }) => pump ? (
    <g key={k} transform={`translate(${x},${y}) scale(${s})`}>
      <circle r={24} fill={color} />
      <text y={11} textAnchor="middle" fontSize={30} fontWeight={800} fill="#151515" fontFamily="Manrope Variable">+</text>
    </g>
  ) : (
    <polygon key={k} transform={`translate(${x},${y}) scale(${s})`} points="0,-26 22,-13 22,13 0,26 -22,13 -22,-13" fill="none" stroke={color} strokeWidth={6} />
  );
  // Движущиеся через белок частицы.
  const movers = [0, 1, 2].map((i) => {
    const o = ((t + i * 20) % 60) / 60;
    const y = pump ? interpolate(o, [0, 1], [h - 90, 90]) : interpolate(o, [0, 1], [90, h - 90]);
    return <P key={`m${i}`} k={`m${i}`} x={w / 2} y={y} s={0.9} />;
  });
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
      {hi.map(([x, y], i) => <P key={`h${i}`} k={`h${i}`} x={x} y={y} />)}
      {lo.map(([x, y], i) => <P key={`l${i}`} k={`l${i}`} x={x} y={y} />)}
      {heads.map((x) => (
        <g key={x}>
          <line x1={x} y1={mid - 40} x2={x} y2={mid - 4} stroke={C.muted} strokeWidth={4} />
          <line x1={x} y1={mid + 4} x2={x} y2={mid + 40} stroke={C.muted} strokeWidth={4} />
          <circle cx={x} cy={mid - 46} r={13} fill={C.fg} opacity={0.85} />
          <circle cx={x} cy={mid + 46} r={13} fill={C.fg} opacity={0.85} />
        </g>
      ))}
      <rect x={w / 2 - 78} y={mid - 100} width={156} height={200} rx={44} fill={pump ? '#8A3B3F' : '#1F7A4A'} stroke={pump ? RED : GREEN} strokeWidth={6} />
      <rect x={w / 2 - 22} y={mid - 100} width={44} height={200} fill="#151515" opacity={0.55} />
      {movers}
      {pump && atp > 0 && (
        <g transform={`translate(${w / 2 + 160},${mid}) scale(${0.6 + 0.4 * atp})`} opacity={Math.min(1, atp * 1.5)}>
          <rect x={-80} y={-80} width={330} height={160} rx={20} fill="#151515" opacity={0.85} />
          <polygon points="0,-70 18,-18 64,-18 26,10 40,62 0,30 -40,62 -26,10 -64,-18 -18,-18" fill="#F2C94C" />
          <text x={80} y={24} fontSize={64} fontWeight={800} fill="#F2C94C" fontFamily="Unbounded Variable">АТФ</text>
        </g>
      )}
      <rect x={0} y={0} width={w} height={48} fill="#151515" opacity={0.9} />
      <text x={w / 2} y={36} textAnchor="middle" fontSize={36} fontWeight={800} fill={C.muted} fontFamily="Manrope Variable">{top}</text>
      <rect x={0} y={h - 50} width={w} height={50} fill="#151515" opacity={0.9} />
      <text x={w / 2} y={h - 14} textAnchor="middle" fontSize={36} fontWeight={800} fill={C.muted} fontFamily="Manrope Variable">{bottom}</text>
    </svg>
  );
};

// Счётчик вопросов блица в правом верхнем углу.
export const Counter = ({ n, total = 3 }) => (
  <div style={{ position: 'absolute', top: 150, right: GUT, fontFamily: F.display, fontWeight: 800, fontSize: 72, color: C.fg }}>
    <span style={{ color: HOT() }}>{n}</span>/{total}
  </div>
);

// Финал: запись на курс.
export const CtaScene = ({ scene, score = false }) => {
  const f = useCurrentFrame();
  const sign = at(scene, 'запис', 40);
  const dm = at(scene, 'директ', 80);
  const bob = Math.sin(f / 5) * 10;
  const brandAt = score ? sign - 6 : scene.lead;
  return (
    <AbsoluteFill>
      {score && f < brandAt && (
        <>
          <Pop start={scene.lead} y={420}><Big size={120}>Сколько<br />из 3?</Big></Pop>
          <Pop start={at(scene, 'коммент', 20)} y={760}><Plaque size={60} bg={C.fg} color={C.bg}>пиши в комменты</Plaque></Pop>
        </>
      )}
      <Pop start={brandAt} y={330}><Big size={92}>ХимБио<br />просто</Big></Pop>
      <Pop start={brandAt + 8} y={560}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 48, color: C.muted, textAlign: 'center' }}>химия и биология к ЕНТ</div></Pop>
      <Pop start={sign} y={720}><Plaque size={96} bg={C.accent} rotate={-3}>Запись<br />на курс</Plaque></Pop>
      <Sfx at={sign} name="boom" volume={0.35} />
      <Pop start={dm} y={1060}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 22, background: C.fg, color: C.bg, padding: '22px 40px 26px', borderRadius: 80, fontFamily: F.body, fontWeight: 800, fontSize: 56, transform: `translateY(${bob}px)` }}>
          <svg width="58" height="58" viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z" fill={C.bg} /></svg>
          пиши в директ
        </div>
      </Pop>
      <Pop start={dm + 6} y={1200}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 52, color: HOT() }}>@himbio.prosto</div></Pop>
      <Sfx at={dm} name="pop" volume={0.5} />
    </AbsoluteFill>
  );
};

// Верх: метка бренда + сегменты прогресса по сценам.
const TopBar = ({ plan }) => {
  const f = useCurrentFrame();
  const segs = plan.scenes;
  return (
    <>
      <div style={{ position: 'absolute', top: 70, left: GUT, right: GUT, display: 'flex', gap: 8 }}>
        {segs.map((s) => {
          const k = interpolate(f, [s.from, s.from + s.dur], [0, 1], clamp);
          return <div key={s.id} style={{ flex: s.dur, height: 8, background: C.faint }}><div style={{ width: `${k * 100}%`, height: '100%', background: C.fg }} /></div>;
        })}
      </div>
      <div style={{ position: 'absolute', top: 104, left: GUT, fontFamily: F.body, fontWeight: 800, fontSize: 28, letterSpacing: '0.16em', color: C.muted }}>ХИМБИО ПРОСТО · {isChem() ? 'ХИМИЯ' : 'БИОЛОГИЯ'} ЕНТ</div>
    </>
  );
};

// Караоке: строка до ~3 слов, звучащее слово — зелёная плашка.
const Karaoke = ({ plan, hide }) => {
  const f = useCurrentFrame();
  for (const s of plan.scenes) {
    if (hide.includes(s.id) || f < s.from || f >= s.from + s.dur) continue;
    const ws = s.words.map((w) => ({ t: w.t.replace(/[—«»"]/g, '').trim(), at: s.from + s.lead + Math.round((w.start / 1000) * FPS) })).filter((w) => w.t);
    const lines = [];
    let cur = [];
    for (const w of ws) {
      const len = cur.reduce((a, x) => a + x.t.length + 1, 0) + w.t.length;
      if (cur.length && (len > 20 || cur.length >= 3 || /[.!?:]$/.test(cur[cur.length - 1].t))) { lines.push(cur); cur = []; }
      cur.push(w);
    }
    if (cur.length) lines.push(cur);
    const line = [...lines].reverse().find((l) => f >= l[0].at);
    if (!line) return null;
    return (
      <div style={{ position: 'absolute', top: 1390, left: GUT - 20, right: GUT - 20, display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: 14, zIndex: 5 }}>
        {line.map((w, i) => {
          const on = f >= w.at && (i === line.length - 1 || f < line[i + 1].at);
          const p = sp(f, w.at, { damping: 12, stiffness: 300, mass: 0.4 });
          return (
            <span key={i} style={{ fontFamily: F.body, fontWeight: 800, fontSize: 66, textTransform: 'uppercase', color: f < w.at ? 'rgba(243,240,232,0.35)' : C.fg, background: on ? C.accent : 'transparent', padding: '4px 14px 10px', transform: on ? `scale(${1 + 0.08 * p})` : 'none', display: 'inline-block', textShadow: '0 4px 18px rgba(0,0,0,0.7)' }}>
              {w.t.replace(/[.,!?:]$/, '')}
            </span>
          );
        })}
      </div>
    );
  }
  return null;
};

// Склейка «удар-зум»: сцена влетает из увеличения 1.18 → 1 за 7 кадров, дальше лёгкий наезд; белая вспышка 2 кадра.
const ZoomCut = ({ index, dur, children }) => {
  const f = useCurrentFrame();
  const k = index === 0 ? 1 : Math.min(1, f / 7);
  const e = 1 - (1 - k) ** 3;
  const s = (1.18 - 0.18 * e) * interpolate(f, [0, dur], [1, 1.035]);
  return (
    <AbsoluteFill style={{ transform: `scale(${s})` }}>
      {children}
      {index > 0 && f < 3 && <AbsoluteFill style={{ background: '#fff', opacity: 0.35 * (1 - f / 3) }} />}
    </AbsoluteFill>
  );
};

export const makeReel = (scenesById, hide = [], subject = 'bio') => ({ plan }) => {
  setSubject(subject);
  useFonts2();
  return (
    <AbsoluteFill style={{ background: C.bg }}>
      <Background />
      {plan.scenes.map((s) => {
        const Scene = scenesById[s.id];
        return (
          <Sequence key={s.id} from={s.from} durationInFrames={s.dur} name={s.id}>
            <ZoomCut index={s.index} dur={s.dur}><Scene scene={s} /></ZoomCut>
            {s.index > 0 && <Sfx at={0} name="whoosh" volume={0.22} />}
            {s.audio && (
              <Sequence from={s.lead}>
                <Audio src={staticFile(s.audio)} />
              </Sequence>
            )}
          </Sequence>
        );
      })}
      <TopBar plan={plan} />
      <Karaoke plan={plan} hide={hide} />
    </AbsoluteFill>
  );
};

export { TeX, Sfx };
