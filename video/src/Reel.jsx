import React, { useEffect, useState } from 'react';
import { AbsoluteFill, Audio, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import '@fontsource-variable/unbounded';
import '@fontsource-variable/manrope';
import 'katex/dist/katex.min.css';
import { C, F, SAFE } from './theme.js';
import { subtitleChunks } from './plan.js';
import { Background, enter } from './kit.jsx';
import { SCENES as R001 } from './reels/r001.jsx';
import { SCENES as R002 } from './reels/r002.jsx';
import { SCENES as R003 } from './reels/r003.jsx';
import { SCENES as Y001 } from './reels/y001.jsx';
import { SCENES as Y002 } from './reels/y002.jsx';

// Props ролика сериализуются в JSON, поэтому сцены подключаются здесь, по id ролика.
const REELS = { R001, R002, R003, Y001, Y002 };

export const useFonts = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all([
      document.fonts.load('800 100px "Unbounded Variable"', 'АБВ'),
      document.fonts.load('700 50px "Manrope Variable"', 'АБВ'),
      document.fonts.load('60px KaTeX_Main'),
      document.fonts.load('italic 60px KaTeX_Math'),
    ]).then(() => continueRender(handle), () => continueRender(handle));
  }, [handle]);
};

// Метка бренда.
const BrandLabel = () => (
  <div style={{ position: 'absolute', top: 120, left: SAFE.x, display: 'flex', alignItems: 'center', gap: 14, fontFamily: F.body, fontWeight: 800, fontSize: 30, letterSpacing: '0.14em', color: C.fg }}>
    <span style={{ width: 16, height: 16, borderRadius: '50%', background: C.fg }} />
    ХИМБИО ПРОСТО · ЕНТ
  </div>
);

// Камера: сцена въезжает с чередующейся стороны и медленно приближается.
const Camera = ({ index, dur, children }) => {
  const frame = useCurrentFrame();
  const dir = index % 2 ? -1 : 1;
  const k = index === 0 ? 1 : interpolate(frame, [0, 7], [0, 1], { extrapolateRight: 'clamp' });
  const ease = 1 - (1 - k) ** 3;
  const zoom = interpolate(frame, [0, dur], index % 2 ? [1.07, 1] : [1, 1.07]);
  const blur = (1 - ease) * 14;
  return (
    <AbsoluteFill style={{ transform: `translateX(${dir * 460 * (1 - ease)}px) scale(${zoom})`, filter: blur > 0.3 ? `blur(${blur}px)` : undefined }}>
      {children}
    </AbsoluteFill>
  );
};

const NUMBER = /^(ноль|половин|два|две|двух|три|четыр|четвёрк|пять|пятьдесят|шест|сем|восем|девят|десят|тридцат|сорок|девяносто|сто|\d)/i;

const Subtitles = ({ plan }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const chunk = subtitleChunks(plan).find((c) => frame >= c.from && frame < c.to);
  if (!chunk) return null;
  const p = enter(frame, chunk.from, fps, { damping: 13, stiffness: 260, mass: 0.5 });
  const top = height > width ? SAFE.subtitleY : height - 150;  // горизонтальный кадр — субтитры внизу
  return (
    <div style={{ position: 'absolute', top, left: 0, right: 0, display: 'flex', justifyContent: 'center', zIndex: 5 }}>
      <div style={{ transform: `scale(${0.8 + 0.2 * p})`, background: C.fg, padding: '12px 26px 16px', fontFamily: F.body, fontWeight: 800, fontSize: 60, textTransform: 'uppercase', color: C.bg, maxWidth: 820, textAlign: 'center' }}>
        {chunk.text.split(' ').map((w, i) => (
          <span key={i} style={{ color: NUMBER.test(w) ? C.accent : C.bg }}>
            {i ? ' ' : ''}
            {w.replace(/[«»"]/g, '')}
          </span>
        ))}
      </div>
    </div>
  );
};

// Переход между сценами: красная косая полоса проносится через кадр.
const Cuts = ({ plan }) => {
  const frame = useCurrentFrame();
  const s = plan.scenes.find((x) => frame >= x.from && frame < x.from + 8);
  if (!s) return null;
  const k = (frame - s.from) / 8;
  const x = interpolate(k, [0, 1], [-700, 1500]);
  return <div style={{ position: 'absolute', top: -300, bottom: -300, left: x, width: s.index === 0 ? 900 : 260, background: C.accent, transform: 'skewX(-14deg)', opacity: 0.95 }} />;
};

export const Reel = ({ plan, reel }) => {
  useFonts();
  const scenes = REELS[reel];
  return (
    <AbsoluteFill style={{ background: C.bg }}>
      <Background />
      {plan.scenes.map((s) => {
        const Scene = scenes[s.id];
        return (
          <Sequence key={s.id} from={s.from} durationInFrames={s.dur} name={s.id}>
            <Camera index={s.index} dur={s.dur}>
              <Scene scene={s} />
            </Camera>
            {!plan.silent && (
              <Sequence from={s.lead}>
                <Audio src={staticFile(s.audio)} />
              </Sequence>
            )}
          </Sequence>
        );
      })}
      <BrandLabel />
      <Subtitles plan={plan} />
      <Cuts plan={plan} />
    </AbsoluteFill>
  );
};
