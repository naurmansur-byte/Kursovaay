// V001 — монтаж v2 «Вопрос на 3 секунды». Биология, неделя 3: осмос, плазмолиз (конспект недели 3, «Осмос и растительная клетка»).
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { C, F } from '../theme.js';
import { Big, Center, CtaScene, GREEN, Opt, PlantCell, Plaque, Pop, Sfx, Spoken, TimerRing, at, clamp, makeReel } from './kit2.jsx';

const OPTS = [['А', 'Лопнет'], ['Б', 'Плазмолиз'], ['В', 'Ничего не изменится'], ['Г', 'Тургор усилится']];
const Q = 'Клетка лука в крепком растворе соли:';

const Options = ({ start, gap = 6 }) => (
  <>
    <Center y={230}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 46, color: C.muted, textAlign: 'center' }}>{Q}</div></Center>
    {OPTS.map(([l, t], i) => <Opt key={l} letter={l} text={t} start={start + i * gap} y={330 + i * 170} />)}
  </>
);

const SCENES = {
  hook: ({ scene }) => {
    const f = useCurrentFrame();
    const a1 = at(scene, 'клетку', scene.lead);
    const a2 = at(scene, 'крепкий', 30);
    const a3 = at(scene, 'что', 80);
    const s = at(scene, 'соли', 60);
    return (
      <AbsoluteFill>
        <Pop start={a1} y={250}><Plaque size={40} bg={C.card} rotate={0}>Биология · ЕНТ</Plaque></Pop>
        <Pop start={a1} y={350}><Big size={100}>Клетка лука</Big></Pop>
        <Pop start={a2} y={480}><Plaque size={50} bg="#1F7A4A">в крепком растворе соли</Plaque></Pop>
        <Center y={600}><PlantCell size={540} salt={interpolate(f, [s, s + 12], [0, 1], clamp)} t={f} /></Center>
        <Pop start={a3} y={1170}><Big size={140} color={GREEN}>Что будет?</Big></Pop>
        <Sfx at={a3} name="pop" volume={0.5} />
      </AbsoluteFill>
    );
  },
  options: ({ scene }) => <AbsoluteFill><Options start={scene.lead} /></AbsoluteFill>,
  timer: ({ scene }) => (
    <AbsoluteFill>
      <Options start={-40} />
      <TimerRing start={scene.lead} seconds={3} y={1040} size={300} />
    </AbsoluteFill>
  ),
  answer: ({ scene }) => {
    const f = useCurrentFrame();
    const b = at(scene, 'плазм', 20);
    const go = at(scene, 'выходит', 80);
    const wall = at(scene, 'стенки', 150);
    return (
      <AbsoluteFill>
        <Sfx at={b} name="ding" volume={0.5} />
        <Opt letter="Б" text="Плазмолиз" state={f >= b ? 'right' : 'idle'} start={-40} y={240} />
        <Center y={420}><PlantCell size={620} salt={1} flow={interpolate(f, [go, go + 8], [0, 1], clamp)} progress={interpolate(f, [go, go + 50], [0, 1], clamp)} t={f} /></Center>
        <Pop start={wall} y={1080}><Plaque size={42} bg={C.card} rotate={0}>протопласт отходит от стенки</Plaque></Pop>
      </AbsoluteFill>
    );
  },
  rule: ({ scene }) => (
    <AbsoluteFill>
      <Pop start={scene.lead} y={300}><Plaque size={60} bg={C.fg} color={C.bg}>Запомни</Plaque></Pop>
      <Spoken scene={scene} skip={1} y={500} size={96} accentWords={['вода', 'больше']} />
    </AbsoluteFill>
  ),
  cta: ({ scene }) => <CtaScene scene={scene} />,
};

export const TAILS = { hook: 10, options: 6, timer: 40, answer: 20, rule: 20, cta: 45 };
export const Comp = makeReel(SCENES, ['hook', 'timer', 'rule', 'cta']);
