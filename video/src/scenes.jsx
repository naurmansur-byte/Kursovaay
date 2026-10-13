// Шаблонные сцены Reels: выбор ответа (ЕНТ), крупная плашка-удар, аутро с призывом в комментарии.
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F, ACCENT_HEX } from './theme.js';
import { wordFrame } from './plan.js';
import { Appear, Atom, Card, Kinetic, Label, Option, Row, Sfx, TeX, enter } from './kit.jsx';

export const A = (s) => `\\textcolor{${ACCENT_HEX}}{${s}}`;

export const useW = (scene) => {
  const { fps } = useVideoConfig();
  return (stem, fallback = 0, nth = 0) => wordFrame(scene, fps, stem, fallback, nth);
};

// Крупное число или ответ, влетает «ударом».
export const Slam = ({ at, y, children, size = 260 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 10, stiffness: 220, mass: 0.6 });
  return (
    <Row y={y}>
      <div style={{ transform: `scale(${interpolate(p, [0, 1], [2.4, 1])}) rotate(-4deg)`, opacity: Math.min(1, p * 3), background: C.accent, color: C.fg, fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: 1, padding: `${size * 0.08}px ${size * 0.16}px ${size * 0.12}px`, whiteSpace: 'nowrap' }}>
        {children}
      </div>
    </Row>
  );
};

// Карточка «выбери ответ» с таймером. options: [['А', '0{,}5'], ...]
export const EngageScene = ({ scene, questionTex, options, unit }) => {
  const frame = useCurrentFrame();
  const left = interpolate(frame, [2, scene.dur - 2], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const R = 34;
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={92} rotate={-3} plaque>Твой ответ?</Kinetic>
      <Appear at={1} y={450}>
        <Card>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Label>ЕНТ · выбери один ответ</Label>
            <svg width={2 * R + 12} height={2 * R + 12} viewBox={`${-R - 6} ${-R - 6} ${2 * R + 12} ${2 * R + 12}`}>
              <circle r={R} fill="none" stroke={C.faint} strokeWidth="8" />
              <circle r={R} fill="none" stroke={C.accent} strokeWidth="8" strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - left)} transform="rotate(-90)" />
            </svg>
          </div>
          <div style={{ marginTop: 26, display: 'grid', gap: 10 }}>
            {(Array.isArray(questionTex) ? questionTex : [questionTex]).map((t) => (
              <TeX key={t} tex={t} size={56} />
            ))}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 22, marginTop: 34 }}>
            {options.map(([l, v], i) => (
              <Option key={l} letter={l} value={v} unit={unit} at={4 + i * 3} />
            ))}
          </div>
        </Card>
      </Appear>
      {[4, 7, 10, 13].map((t) => (
        <Sfx key={t} at={t} name="tick" volume={0.5} />
      ))}
    </AbsoluteFill>
  );
};

// Аутро-приглашение на курс: логотип, факты о курсе (только утверждённые), слово для комментариев.
// Голос: «Хочешь решать такие задачи? Курс «ХимБио просто», старт первого ноября. Пиши «курс» в комментариях!»
export const CourseOutro = ({ scene, word = 'курс' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tCourse = W('курс', 40);
  const tStart = W('старт', tCourse + 20);
  const tWrite = W('пиши', tStart + 30);
  const tWord = W(word, tWrite + 6, 1);
  const letters = word.toUpperCase().split('');
  const letterSize = Math.min(200, (930 / letters.length - 42) / 0.85);
  const chips = [
    ['онлайн', tCourse + 10],
    ['группы по 5 человек', tCourse + 14],
    ['старт 1 ноября', tStart],
  ];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={200} size={80} rotate={-3}>Хочешь решать</Kinetic>
      <Kinetic at={3} y={295} size={80} rotate={-3} from="right">такие задачи?</Kinetic>
      <Appear at={tCourse} y={410}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
          <Atom size={110} at={tCourse} speed={1.4} />
          <div>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 62, lineHeight: 1, color: C.fg, whiteSpace: 'nowrap' }}>ХИМБИО ПРОСТО</div>
            <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: 40, color: C.muted, marginTop: 8 }}>курс подготовки к ЕНТ</div>
          </div>
        </div>
      </Appear>
      <Row y={590} style={{ gap: 12, flexWrap: 'wrap' }}>
        {chips.map(([text, at], i) =>
          frame < at ? null : (
            <div key={text} style={{ transform: `scale(${enter(frame, at, fps)})`, border: `3px solid ${i === 2 ? C.accent : C.fg}`, background: i === 2 ? C.accent : 'transparent', padding: '8px 20px', fontFamily: F.body, fontWeight: 800, fontSize: 34, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>
              {text}
            </div>
          )
        )}
      </Row>
      <Kinetic at={tWrite} y={790} size={84} rotate={-3} from="right">Пиши</Kinetic>
      <Kinetic at={tWrite + 3} y={890} size={70} rotate={-3}>в комментариях</Kinetic>
      <Row y={1020} style={{ gap: 6 }}>
        {frame >= tWord &&
          letters.map((ch, i) => {
            const p = enter(frame, tWord + i * 3, fps, { damping: 11, stiffness: 200 });
            return (
              <div key={i} style={{ transform: `translateY(${(1 - p) * -160}px) rotate(${(1 - p) * (i % 2 ? 18 : -18) - 4}deg)`, opacity: Math.min(1, p * 2), background: C.accent, fontFamily: F.display, fontWeight: 800, fontSize: letterSize, lineHeight: 1, padding: '14px 18px 22px', color: C.fg }}>
                {ch}
              </div>
            );
          })}
      </Row>
      <Sfx at={tCourse} name="whoosh" />
      <Sfx at={tStart} name="pop" volume={0.4} />
      <Sfx at={tWrite} name="whoosh" />
      {letters.map((_, i) => (
        <Sfx key={i} at={tWord + i * 3} name="pop" volume={0.3} />
      ))}
    </AbsoluteFill>
  );
};

// Аутро: «Хочешь памятку? Пиши «СЛОВО» в комментариях» + логотип.
export const OutroScene = ({ scene, word, writeStem = 'пиши', wordStem }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tWrite = W(writeStem, 20);
  const tWord = W(wordStem ?? word, tWrite + 6);
  const letters = word.toUpperCase().split('');
  // Буквы-плашки должны уместиться в 930 px: на букву ≈ 0.85 em + поля.
  const letterSize = Math.min(210, (930 / letters.length - 42) / 0.85);
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={240} size={78} rotate={-3}>Хочешь памятку?</Kinetic>
      <Kinetic at={tWrite} y={370} size={96} rotate={-3} from="right">Пиши</Kinetic>
      <Kinetic at={tWrite + 3} y={480} size={80} rotate={-3}>в комментариях</Kinetic>
      <Row y={630} style={{ gap: 6 }}>
        {frame >= tWord &&
          letters.map((ch, i) => {
            const p = enter(frame, tWord + i * 3, fps, { damping: 11, stiffness: 200 });
            return (
              <div key={i} style={{ transform: `translateY(${(1 - p) * -160}px) rotate(${(1 - p) * (i % 2 ? 18 : -18) - 4}deg)`, opacity: Math.min(1, p * 2), background: C.accent, fontFamily: F.display, fontWeight: 800, fontSize: letterSize, lineHeight: 1, padding: '14px 18px 22px', color: C.fg }}>
                {ch}
              </div>
            );
          })}
      </Row>
      <Appear at={tWord + 16} y={930}>
        <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 54, color: C.fg, textTransform: 'uppercase', letterSpacing: '0.04em' }}>→ пришлю памятку</div>
      </Appear>
      <Appear at={tWord + 22} y={1060}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
          <Atom size={150} at={0} />
          <div>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 64, color: C.fg }}>ХИМБИО ПРОСТО</div>
            <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: 40, color: C.muted }}>подготовка к ЕНТ по химии</div>
          </div>
        </div>
      </Appear>
      <Sfx at={tWrite} name="whoosh" />
      {letters.map((_, i) => (
        <Sfx key={i} at={tWord + i * 3} name="pop" volume={0.3} />
      ))}
    </AbsoluteFill>
  );
};
