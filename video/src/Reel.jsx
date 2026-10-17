import React, { useEffect, useState } from 'react';
import { AbsoluteFill, Audio, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import '@fontsource-variable/unbounded';
import '@fontsource-variable/manrope';
import 'katex/dist/katex.min.css';
import { C, F, SAFE, setSubject } from './theme.js';
import { subtitleChunks } from './plan.js';
import { Background, enter } from './kit.jsx';
import { SCENES as R001 } from './reels/r001.jsx';
import { SCENES as R002 } from './reels/r002.jsx';
import { SCENES as R003 } from './reels/r003.jsx';
import { SCENES as Y001 } from './reels/y001.jsx';
import { SCENES as Y002 } from './reels/y002.jsx';
import { SCENES as B001 } from './reels/b001.jsx';
import { SCENES as B002 } from './reels/b002.jsx';
import { SCENES as B003 } from './reels/b003.jsx';
import { SCENES as Y003 } from './reels/y003.jsx';
import { SCENES as Y004 } from './reels/y004.jsx';
import { SCENES as A001 } from './reels/a001.jsx';
import { SCENES as A002 } from './reels/a002.jsx';
import { SCENES as A003 } from './reels/a003.jsx';
import { SCENES as A004 } from './reels/a004.jsx';
import { SCENES as R004 } from './reels/r004.jsx';
import { SCENES as R005 } from './reels/r005.jsx';
import { SCENES as R006 } from './reels/r006.jsx';
import { SCENES as R007 } from './reels/r007.jsx';
import { SCENES as B004 } from './reels/b004.jsx';
import { SCENES as B005 } from './reels/b005.jsx';
import { SCENES as B006 } from './reels/b006.jsx';
import { SCENES as B007 } from './reels/b007.jsx';
import { SCENES as Y005 } from './reels/y005.jsx';
import { SCENES as Y006 } from './reels/y006.jsx';
import { SCENES as Y007 } from './reels/y007.jsx';
import { SCENES as Y008 } from './reels/y008.jsx';
import { SCENES as Y009 } from './reels/y009.jsx';
import { SCENES as Y010 } from './reels/y010.jsx';
import { SCENES as Y011 } from './reels/y011.jsx';
import { SCENES as Y012 } from './reels/y012.jsx';
import { SCENES as S001 } from './reels/s001.jsx';
import { SCENES as S002 } from './reels/s002.jsx';
import { SCENES as S003 } from './reels/s003.jsx';
import { SCENES as S004 } from './reels/s004.jsx';
import { SCENES as R008 } from './reels/r008.jsx';
import { SCENES as R009 } from './reels/r009.jsx';
import { SCENES as R010 } from './reels/r010.jsx';
import { SCENES as R011 } from './reels/r011.jsx';
import { SCENES as B008 } from './reels/b008.jsx';
import { SCENES as B009 } from './reels/b009.jsx';
import { SCENES as B010 } from './reels/b010.jsx';
import { SCENES as B011 } from './reels/b011.jsx';
import { SCENES as R012 } from './reels/r012.jsx';
import { SCENES as R013 } from './reels/r013.jsx';
import { SCENES as R014 } from './reels/r014.jsx';
import { SCENES as R015 } from './reels/r015.jsx';
import { SCENES as B012 } from './reels/b012.jsx';
import { SCENES as B013 } from './reels/b013.jsx';
import { SCENES as B014 } from './reels/b014.jsx';
import { SCENES as B015 } from './reels/b015.jsx';
import { SCENES as R016 } from './reels/r016.jsx';
import { SCENES as R017 } from './reels/r017.jsx';
import { SCENES as R018 } from './reels/r018.jsx';
import { SCENES as R019 } from './reels/r019.jsx';
import { SCENES as B016 } from './reels/b016.jsx';
import { SCENES as B017 } from './reels/b017.jsx';
import { SCENES as B018 } from './reels/b018.jsx';
import { SCENES as B019 } from './reels/b019.jsx';

// Props ролика сериализуются в JSON, поэтому сцены подключаются здесь, по id ролика.
const REELS = { R001, R002, R003, Y001, Y002, B001, B002, B003, Y003, Y004, A001, A002, A003, A004, R004, R005, R006, R007, B004, B005, B006, B007, Y005, Y006, Y007, Y008, Y009, Y010, Y011, Y012, S001, S002, S003, S004, R008, R009, R010, R011, B008, B009, B010, B011, R012, R013, R014, R015, B012, B013, B014, B015, R016, R017, R018, R019, B016, B017, B018, B019 };

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

// subject: 'chem' (красный) или 'bio' (зелёный) — цвет акцента всего ролика.
export const Reel = ({ plan, reel, subject = 'chem' }) => {
  setSubject(subject);
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
