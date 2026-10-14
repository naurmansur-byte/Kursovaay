// A004 «Мы на YouTube» — короткий рилс-анонс канала: хук → какие разборы есть → ссылка в профиле.
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Kinetic, Row, Sfx, enter, punch } from '../kit.jsx';
import { useW } from '../scenes.jsx';

// Кнопка «плей» (без логотипа сервиса).
const Play = ({ at, size = 360 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 10, stiffness: 180, mass: 0.6 });
  const pulse = 1 + 0.04 * Math.sin(((frame - at) / fps) * 6);
  return (
    <div style={{ transform: `scale(${interpolate(p, [0, 1], [0.3, 1]) * pulse}) rotate(-4deg)`, width: size, height: size * 0.7, borderRadius: size * 0.18, background: C.accent, display: 'grid', placeItems: 'center', boxShadow: `14px 14px 0 ${C.fg}` }}>
      <svg width={size * 0.34} height={size * 0.34} viewBox="0 0 10 10"><polygon points="2,1 9,5 2,9" fill="#fff" /></svg>
    </div>
  );
};

const Hook = ({ scene }) => {
  const W = useW(scene);
  const [tS, tY] = [W('стоп', 0), W('youtube', 20)];
  return (
    <AbsoluteFill>
      <Kinetic at={tS} y={260} size={150} rotate={-6} punchAt={tS + 3}>Стоп!</Kinetic>
      <Row y={520}><Play at={tY - 6} /></Row>
      <Kinetic at={tY} y={900} size={110} rotate={-4} plaque from="right" punchAt={tY + 4}>Мы на YouTube</Kinetic>
      <Sfx at={tS} name="boom" volume={0.5} /><Sfx at={tY - 6} name="pop" /><Sfx at={tY} name="whoosh" />
    </AbsoluteFill>
  );
};

const TILES = [['Растворы', 'химия', 'растворы'], ['Химическая связь', 'химия', 'химическая'], ['Кровообращение', 'биология', 'кровообращение'], ['Иммунитет и дыхание', 'биология', 'иммунитет']];

const Tile = ({ title, subject, at, i }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps);
  return (
    <div style={{ transform: `translateX(${(1 - p) * (i % 2 ? 300 : -300)}px)`, opacity: Math.min(1, p * 2), display: 'flex', alignItems: 'center', gap: 26, width: 900, background: C.card, border: `4px solid ${C.fg}`, padding: '22px 28px', boxSizing: 'border-box' }}>
      <div style={{ width: 150, height: 96, flex: 'none', background: subject === 'химия' ? '#F13A43' : '#1F7A4A', display: 'grid', placeItems: 'center' }}>
        <svg width="44" height="44" viewBox="0 0 10 10"><polygon points="2,1 9,5 2,9" fill="#fff" /></svg>
      </div>
      <div>
        <div style={{ font: `800 ${title.length > 16 ? 36 : 40}px ${F.display}`, color: C.fg, lineHeight: 1.05, textTransform: 'uppercase', whiteSpace: 'nowrap' }}>{title}</div>
        <div style={{ font: `800 32px ${F.body}`, color: C.muted, marginTop: 6, textTransform: 'uppercase', letterSpacing: '.08em' }}>{subject} · 3 задачи ЕНТ</div>
      </div>
    </div>
  );
};

const List = ({ scene }) => {
  const W = useW(scene);
  const times = TILES.map(([, , stem], i) => W(stem, 40 + i * 20));
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={210} size={88} rotate={-3} plaque>Полные разборы</Kinetic>
      {TILES.map(([title, subject], i) => (
        <Row key={title} y={410 + i * 185}><Tile title={title} subject={subject} at={times[i]} i={i} /></Row>
      ))}
      {times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
    </AbsoluteFill>
  );
};

const Link = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tL, tP, tS] = [W('ссылка', 0), W('профиле', 20), W('подписывайся', 60)];
  const pp = enter(frame, tP, fps);
  return (
    <AbsoluteFill>
      <Kinetic at={tL} y={230} size={110} rotate={-4}>Ссылка —</Kinetic>
      <Kinetic at={tP} y={370} size={110} rotate={-4} plaque from="right" punchAt={tP + 4}>в профиле</Kinetic>
      <Appear at={tP} y={600}>
        <div style={{ width: 900, background: C.card, border: `4px solid ${C.fg}`, boxShadow: `14px 14px 0 ${C.accent}`, padding: '34px 40px', boxSizing: 'border-box' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
            <div style={{ width: 120, height: 120, borderRadius: '50%', border: `6px solid ${C.accent}`, display: 'grid', placeItems: 'center', font: `800 44px ${F.display}`, color: C.fg }}>ХБ</div>
            <div>
              <div style={{ font: `800 52px ${F.body}`, color: C.fg }}>@himbio.prosto</div>
              <div style={{ font: `700 34px ${F.body}`, color: C.muted, marginTop: 6 }}>ХимБио просто · ЕНТ</div>
            </div>
          </div>
          <div style={{ marginTop: 30, display: 'flex', alignItems: 'center', gap: 18, padding: '18px 24px', border: `4px solid ${C.accent}`, transform: `scale(${punch(frame, tP + 8, 0.1)})` }}>
            <svg width="40" height="40" viewBox="0 0 10 10"><polygon points="2,1 9,5 2,9" fill={C.accent} /></svg>
            <div style={{ font: `800 40px ${F.body}`, color: C.fg }}>YouTube — разборы ЕНТ</div>
          </div>
        </div>
      </Appear>
      {frame >= tP + 10 && (
        <Row y={1010}>
          <svg width="120" height="120" viewBox="0 0 10 10" style={{ transform: `translateY(${Math.sin(((frame - tP) / fps) * 6) * 12}px) rotate(180deg)`, opacity: pp }}>
            <polygon points="5,1 9,6 6,6 6,9 4,9 4,6 1,6" fill={C.accent} />
          </svg>
        </Row>
      )}
      {frame >= tS && (
        <Row y={1180}>
          <div style={{ transform: `scale(${punch(frame, tS, 0.25)}) rotate(-3deg)`, padding: '24px 54px', background: C.accent, borderRadius: 70, font: `800 56px ${F.display}`, color: '#fff' }}>ПОДПИСЫВАЙСЯ</div>
        </Row>
      )}
      <Sfx at={tL} name="whoosh" /><Sfx at={tP} name="boom" volume={0.45} /><Sfx at={tS} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

export const SCENES = { hook: Hook, list: List, link: Link };
export const TAILS = { hook: 10, list: 16, link: 50 };
