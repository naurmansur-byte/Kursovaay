// Общие элементы стиля 2: фон, кинетический текст, плашки, формулы, атом, варианты ответа.
import React from 'react';
import katex from 'katex';
import { AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F, SAFE } from './theme.js';

export const enter = (frame, at, fps, config = { damping: 14, stiffness: 170, mass: 0.7 }) =>
  frame < at ? 0 : spring({ frame: frame - at, fps, config });

// «Удар» масштабом: короткий всплеск после момента at.
export const punch = (frame, at, amount = 0.22, len = 9) =>
  frame < at ? 1 : 1 + amount * Math.max(0, 1 - (frame - at) / len) * Math.cos(((frame - at) / len) * Math.PI * 0.5);

export const shake = (frame, at, len = 12, px = 14) =>
  frame < at || frame > at + len ? 0 : Math.sin((frame - at) * 2.4) * px * (1 - (frame - at) / len);

// Звуковой эффект из public/sfx (генерируется `npm run sfx`).
export const Sfx = ({ at, name, volume = 0.35 }) =>
  at == null || at < 0 ? null : (
    <Sequence from={at} durationInFrames={30} layout="none">
      <Audio src={staticFile(`sfx/${name}.wav`)} volume={volume} />
    </Sequence>
  );

export const Row = ({ y, children, style }) => (
  <div style={{ position: 'absolute', top: y, left: SAFE.x, right: SAFE.x, display: 'flex', justifyContent: 'center', ...style }}>
    {children}
  </div>
);

// Плёночное зерно и тонкая сетка тетради.
export const Background = () => {
  const frame = useCurrentFrame();
  const jitter = Math.floor(frame / 2) % 6;
  const dx = [0, -37, 21, -11, 43, -26][jitter];
  const dy = [0, 29, -17, 41, -33, 12][jitter];
  return (
    <AbsoluteFill style={{ background: C.bg }}>
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${C.faint} 1px, transparent 1px), linear-gradient(90deg, ${C.faint} 1px, transparent 1px)`,
          backgroundSize: '72px 72px',
          opacity: 0.22,
        }}
      />
      <svg width="1200" height="2040" style={{ position: 'absolute', left: -60 + dx, top: -60 + dy, opacity: 0.09 }}>
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};

// Кинетическая строка: влетает сбоку с наклоном и размытием; plaque — красная плашка.
export const Kinetic = ({ children, at = 0, y, size = 110, rotate = -4, from = 'left', plaque = false, punchAt, color, weight = 800, bg }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const p = enter(frame, at, fps);
  if (frame < at) return null;
  const x = interpolate(p, [0, 1], [from === 'left' ? -1300 : 1300, 0]);
  const blur = interpolate(p, [0, 0.85, 1], [16, 1.5, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const s = punchAt != null ? punch(frame, punchAt) : 1;
  // Уменьшить шрифт, чтобы строка с плашкой и наклоном влезла в безопасную зону (Unbounded ≈ 0.86 em на букву).
  if (typeof children === 'string') {
    const room = Math.min(width, 1700) - 2 * SAFE.x - 40;
    size = Math.min(size, room / (children.length * 0.86 + (plaque ? 0.44 : 0)));
  }
  return (
    <Row y={y}>
      <div
        style={{
          transform: `translateX(${x}px) rotate(${rotate}deg) scale(${s})`,
          filter: blur > 0.2 ? `blur(${blur}px)` : undefined,
          fontFamily: F.display,
          fontWeight: weight,
          fontSize: size,
          lineHeight: 1.02,
          letterSpacing: '-0.02em',
          textTransform: 'uppercase',
          color: color ?? C.fg,
          background: plaque ? bg ?? C.accent : 'transparent',
          padding: plaque ? `${size * 0.1}px ${size * 0.22}px ${size * 0.14}px` : 0,
          whiteSpace: 'nowrap',
        }}
      >
        {children}
      </div>
    </Row>
  );
};

// Плавное появление снизу (для спокойных блоков с формулами).
export const Appear = ({ at = 0, y, children, dy = 40 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 200, stiffness: 120 });
  return (
    <Row y={y}>
      <div style={{ opacity: p, transform: `translateY(${(1 - p) * dy}px)` }}>{children}</div>
    </Row>
  );
};

export const TeX = ({ tex, size = 80, color = C.fg, display = false }) => (
  <div
    style={{ fontSize: size, color, lineHeight: 1.2, whiteSpace: 'nowrap' }}
    dangerouslySetInnerHTML={{ __html: katex.renderToString(tex, { throwOnError: false, strict: false, displayMode: display, output: 'html' }) }}
  />
);

export const Card = ({ children, width = 900, style }) => (
  <div
    style={{
      width,
      background: C.card,
      border: `3px solid ${C.fg}`,
      boxShadow: `14px 14px 0 ${C.fg}`,
      padding: '40px 48px',
      boxSizing: 'border-box',
      ...style,
    }}
  >
    {children}
  </div>
);

export const Label = ({ children, color = C.muted, size = 34 }) => (
  <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: size, letterSpacing: '0.14em', textTransform: 'uppercase', color }}>{children}</div>
);

// Атом: три орбиты, электроны бегут по кругу.
export const Atom = ({ size = 320, at = 0, speed = 1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 12, stiffness: 120 });
  const t = (frame - at) / fps;
  const orbits = [0, 60, 120];
  return (
    <svg width={size} height={size} viewBox="-200 -200 400 400" style={{ transform: `scale(${p}) rotate(${t * 18 * speed}deg)` }}>
      {orbits.map((r, i) => {
        const a = t * (2.2 + i * 0.5) * speed + i * 2;
        const ex = Math.cos(a) * 180;
        const ey = Math.sin(a) * 62;
        return (
          <g key={r} transform={`rotate(${r})`}>
            <ellipse rx="180" ry="62" fill="none" stroke={C.fg} strokeWidth="10" />
            <circle cx={ex} cy={ey} r="15" fill={C.accent} />
          </g>
        );
      })}
      <circle r="30" fill={C.accent} />
    </svg>
  );
};

// Спираль ДНК (биология): нити бегут по фазе — спираль «крутится».
export const Dna = ({ size = 200, at = 0, speed = 1, color }) => {
  const ac = color ?? C.accent;
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 12, stiffness: 120 });
  const t = (frame - at) / fps;
  const h = 400;
  const w = 180;
  const x = (y, s) => w / 2 + s * w * 0.4 * Math.sin((2 * Math.PI * 1.5 * y) / h + t * 2.4 * speed);
  const ys = Array.from({ length: 61 }, (_, k) => (k * h) / 60);
  const strand = (s) => 'M' + ys.map((y) => `${x(y, s).toFixed(1)} ${y.toFixed(1)}`).join(' L');
  return (
    <svg width={size * 0.5} height={size} viewBox={`-10 -10 ${w + 20} ${h + 20}`} style={{ transform: `scale(${p})` }}>
      {ys.filter((_, k) => k % 5 === 2).map((y, k) => (
        <line key={y} x1={x(y, 1)} y1={y} x2={x(y, -1)} y2={y} stroke={k % 2 ? ac : C.fg} strokeWidth="9" opacity="0.85" />
      ))}
      <path d={strand(1)} fill="none" stroke={C.fg} strokeWidth="13" strokeLinecap="round" />
      <path d={strand(-1)} fill="none" stroke={ac} strokeWidth="13" strokeLinecap="round" />
    </svg>
  );
};

// Горошина для задач Менделя: жёлтая или зелёная, с бликом.
export const PEA = { yellow: '#F2C94C', green: '#3FA65F' };
export const Pea = ({ color = 'yellow', size = 120, at = 0, label }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 10, stiffness: 200, mass: 0.6 });
  const fill = PEA[color] ?? color;
  return (
    <div style={{ display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: 8, transform: `scale(${p})` }}>
      <svg width={size} height={size} viewBox="-50 -50 100 100">
        <circle r="46" fill={fill} stroke={C.bg} strokeWidth="3" />
        <ellipse cx="-16" cy="-18" rx="14" ry="9" fill="#fff" opacity="0.45" transform="rotate(-30 -16 -18)" />
      </svg>
      {label && <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: size * 0.32, color: C.fg }}>{label}</div>}
    </div>
  );
};

// Пламя: два языка огня с мерцанием.
export const Flame = ({ size = 300, at = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 12, stiffness: 120 });
  const t = (frame - at) / fps;
  const fl = 1 + 0.06 * Math.sin(t * 17) + 0.04 * Math.sin(t * 29);
  const sway = 4 * Math.sin(t * 9);
  // Пламя с тремя языками: центральный высокий, боковые ниже.
  const flame =
    'M0 -190 C 22 -140, 62 -118, 58 -62 C 82 -92, 106 -70, 106 -8 C 110 88, 60 150, 0 150 C -60 150, -110 88, -106 -8 C -102 -66, -76 -84, -62 -118 C -46 -78, -30 -86, -24 -128 C -16 -158, -6 -172, 0 -190 Z';
  return (
    <svg width={size} height={size} viewBox="-200 -200 400 400" style={{ transform: `scale(${p})`, transformOrigin: '50% 90%' }}>
      <g transform={`translate(0 140) rotate(${sway}) scale(1 ${fl}) translate(0 -140)`}>
        <path d={flame} fill={C.accent} />
        <path d={flame} fill={C.fg} transform="translate(0 78) scale(0.5 0.48)" />
      </g>
    </svg>
  );
};

// Варианты ответа как в бланке ЕНТ. state: { [letter]: 'right' | 'wrong' | 'dim' }
export const OPTIONS = [
  ['А', '0{,}5'],
  ['Б', '0{,}98'],
  ['В', '1'],
  ['Г', '2'],
];

export const Option = ({ letter, value, state, at = 0, compact = false, unit = 'моль' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps);
  const right = state === 'right';
  const wrong = state === 'wrong';
  const ring = right ? C.accent : C.fg;
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 16,
        padding: compact ? '14px 22px' : '14px 18px',
        border: `3px solid ${right ? C.accent : C.faint}`,
        background: right ? C.accentSoft : 'transparent',
        opacity: state === 'dim' ? 0.35 : p,
        transform: `scale(${0.85 + 0.15 * p})`,
        position: 'relative',
      }}
    >
      <div
        style={{
          width: 56,
          height: 56,
          flex: 'none',
          borderRadius: '50%',
          border: `4px solid ${ring}`,
          background: right ? C.accent : 'transparent',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: F.display,
          fontWeight: 800,
          fontSize: 32,
          color: C.fg,
        }}
      >
        {letter}
      </div>
      <TeX tex={unit ? `${value}\\ \\text{${unit}}` : value} size={compact ? 54 : 46} />
      {wrong && <div style={{ position: 'absolute', left: -8, right: -8, top: '50%', height: 8, background: C.accent, transform: 'rotate(-6deg)' }} />}
    </div>
  );
};
