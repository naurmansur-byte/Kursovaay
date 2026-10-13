// A002 — тот же рекламный рилс, хук «Стоп + ловушка» (прерывание шаблона и ошибка): 3H₂SO₄ — 4 атома O? Мимо, 12.
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, F } from '../theme.js';
import { Kinetic, Row, Sfx, TeX, punch, shake } from '../kit.jsx';
import { Slam, useW } from '../scenes.jsx';
import { BODY, GREEN, Logo } from './a001.jsx';

const Hook = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tQ, tFour, tMiss, t12] = [W('сколько', 10), W('четыре', 40), W('мимо', 55), W('двенадцать', 65)];
  return (
    <AbsoluteFill style={{ transform: `translateX(${shake(frame, tMiss, 12, 16)}px)` }}>
      <Kinetic at={0} y={220} size={150} rotate={-5} plaque punchAt={0}>Стоп!</Kinetic>
      <Row y={470}><div style={{ transform: `scale(${punch(frame, tQ, 0.15)})` }}><TeX tex="3\mathrm{H_2SO_4}" size={190} /></div></Row>
      {frame >= tQ && <Row y={760}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 56, textTransform: 'uppercase', color: C.muted }}>сколько атомов кислорода?</div></Row>}
      {frame >= tFour && (
        <Row y={880}>
          <div style={{ position: 'relative', fontFamily: F.display, fontWeight: 800, fontSize: 150, color: C.fg }}>
            4?
            {frame >= tMiss && <div style={{ position: 'absolute', left: -20, right: -20, top: '50%', height: 18, background: C.accent, transform: 'rotate(-12deg)' }} />}
          </div>
        </Row>
      )}
      <Slam at={t12} y={1080} size={150}>12</Slam>
      <Sfx at={0} name="boom" volume={0.6} /><Sfx at={tQ} name="whoosh" /><Sfx at={tFour} name="pop" /><Sfx at={tMiss} name="buzz" volume={0.5} /><Sfx at={t12} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Catch = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tTens, tCatch, tCourse] = [W('десятки', 20), W('лови', 35), W('курс', 45)];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={260} size={86} rotate={-3}>Таких ловушек</Kinetic>
      <Kinetic at={tTens} y={380} size={96} rotate={-3} from="right" plaque>на ЕНТ — десятки</Kinetic>
      {frame >= tCatch && (
        <Row y={600}>
          <div style={{ transform: `scale(${punch(frame, tCatch, 0.35, 12)}) rotate(-5deg)`, fontFamily: F.display, fontWeight: 800, fontSize: 180, lineHeight: 1, color: C.fg }}>ЛОВИ!</div>
        </Row>
      )}
      <Logo at={tCourse} />
      <Sfx at={1} name="whoosh" /><Sfx at={tTens} name="whoosh" /><Sfx at={tCatch} name="boom" volume={0.5} /><Sfx at={tCourse} name="pop" />
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: 8, background: GREEN }} />
    </AbsoluteFill>
  );
};

export const SCENES = { hook: Hook, catch: Catch, ...BODY };
export const TAILS = { cta: 45 };
