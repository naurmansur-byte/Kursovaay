// A003 — тот же рекламный рилс, хук «миф» (против общепринятого): зубрить все учебники 7–11 классов не нужно.
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Kinetic, Row, Sfx, enter, punch } from '../kit.jsx';
import { useW } from '../scenes.jsx';
import { BODY, GREEN, Logo, Plaque } from './a001.jsx';

// 16 учебников из перечня НЦТ: химия и биология, 7–11 классы (части 1–2 у старших классов).
const BOOKS = ['Х7', 'Х8', 'Х9·1', 'Х9·2', 'Х10·1', 'Х10·2', 'Х11·1', 'Х11·2', 'Б7', 'Б7', 'Б8', 'Б9', 'Б10·1', 'Б10·2', 'Б11·1', 'Б11·2'];

const Hook = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tBooks, tNot] = [W('учебники', 30), W('не', 40)];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={210} size={92} rotate={-3}>Зубрить все</Kinetic>
      <Kinetic at={4} y={320} size={92} rotate={-3} from="right">учебники?</Kinetic>
      <div style={{ position: 'absolute', top: 480, left: 90, right: 90, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
        {BOOKS.map((b, i) => {
          const p = enter(frame, 2 + i * 1.5, fps);
          return (
            <div key={i} style={{ opacity: p, transform: `translateY(${(1 - p) * -80}px) rotate(${(i % 3) - 1}deg)`, height: 120, background: i < 8 ? C.accent : GREEN, display: 'grid', placeItems: 'center', fontFamily: F.display, fontWeight: 800, fontSize: 34, color: C.fg }}>{b}</div>
          );
        })}
      </div>
      {frame >= tNot && (
        <Row y={680}>
          <div style={{ transform: `scale(${punch(frame, tNot, 0.3, 12)}) rotate(-8deg)`, background: C.fg, color: C.bg, padding: '18px 40px 26px', fontFamily: F.display, fontWeight: 800, fontSize: 120, lineHeight: 1, whiteSpace: 'nowrap', boxShadow: '0 20px 60px rgba(0,0,0,.6)' }}>НЕ НУЖНО</div>
        </Row>
      )}
      <Row y={1060}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 42, textTransform: 'uppercase', color: C.muted, opacity: frame >= tBooks ? 1 : 0 }}>16 учебников · 7–11 класс</div></Row>
      <Sfx at={0} name="whoosh" />{[0, 4, 8, 12].map((d) => <Sfx key={d} at={2 + d * 1.5} name="pop" volume={0.25} />)}<Sfx at={tNot} name="boom" volume={0.55} />
    </AbsoluteFill>
  );
};

const Catch = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tAsk, tCatch, tCourse] = [W('спрашивают', 20), W('лови', 40), W('курс', 50)];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={84} rotate={-3}>Нужно знать,</Kinetic>
      <Row y={370}><Plaque at={tAsk} bg={C.accent} size={70} rotate={-3}>что спрашивают</Plaque></Row>
      <Kinetic at={tAsk + 4} y={500} size={80} rotate={-3} from="right">на ЕНТ</Kinetic>
      {frame >= tCatch && (
        <Row y={680}>
          <div style={{ transform: `scale(${punch(frame, tCatch, 0.35, 12)}) rotate(-5deg)`, fontFamily: F.display, fontWeight: 800, fontSize: 170, lineHeight: 1, color: C.fg }}>ЛОВИ!</div>
        </Row>
      )}
      <Logo at={tCourse} />
      <Sfx at={1} name="whoosh" /><Sfx at={tAsk} name="pop" /><Sfx at={tCatch} name="boom" volume={0.5} /><Sfx at={tCourse} name="pop" />
    </AbsoluteFill>
  );
};

export const SCENES = { hook: Hook, catch: Catch, ...BODY };
export const TAILS = { cta: 45 };
