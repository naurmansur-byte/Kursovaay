// V003 — монтаж v2 «Блиц: 3 вопроса». Биология, неделя 3 (конспект недели 3: Na⁺/K⁺-АТФаза 3 Na⁺ наружу и 2 K⁺ внутрь;
// глюкоза из крови в мозг — облегчённая диффузия; осмос — перенос растворителя). Голос — мужской (Мансур 19.11: женский не подошёл).
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, F } from '../theme.js';
import { Big, Center, Chip, CountBar, Counter, CtaScene, GREEN, Plaque, Pop, Sfx, Spoken, at, makeReel, sp } from './kit2.jsx';

const Ion = ({ n, el, size, color = C.fg }) => (
  <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: size, color, lineHeight: 1 }}>
    {n} {el}<sup style={{ fontSize: size * 0.5 }}>+</sup>
  </div>
);

const Question = (n, accent) => ({ scene }) => (
  <AbsoluteFill>
    <Counter n={n} />
    <Pop start={0} y={260}><Plaque size={44} bg={C.card} rotate={0}>Вопрос {n}</Plaque></Pop>
    <Spoken scene={scene} skip={1} y={420} size={92} accentWords={accent} />
    <CountBar start={scene.dur - 40} len={38} y={1120} />
  </AbsoluteFill>
);

const Dots = ({ start }) => {
  const f = useCurrentFrame();
  return (
    <Center y={1000} style={{ gap: 40 }}>
      {[0, 1, 2].map((i) => {
        const p = sp(f, start + i * 5);
        return <div key={i} style={{ width: 110, height: 110, borderRadius: '50%', border: `8px solid ${GREEN}`, transform: `scale(${p})` }} />;
      })}
    </Center>
  );
};

const SCENES = {
  hook: ({ scene }) => {
    const t = at(scene, 'три', scene.lead);
    return (
      <AbsoluteFill>
        <Pop start={t} y={300}><Big size={250} color={GREEN}>3</Big></Pop>
        <Pop start={t + 4} y={560}><Big size={110}>вопроса</Big></Pop>
        <Pop start={at(scene, 'мембрану', 30)} y={720}><Plaque size={60} bg="#1F7A4A">про мембрану</Plaque></Pop>
        <Dots start={at(scene, 'считай', 60)} />
        <Pop start={at(scene, 'угадаешь', 80)} y={1180}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 56, color: C.muted }}>считай, сколько угадаешь</div></Pop>
        <Sfx at={t} name="boom" volume={0.3} />
      </AbsoluteFill>
    );
  },
  q1: Question(1, ['натри', 'насос', 'цикл']),
  a1: ({ scene }) => (
    <AbsoluteFill>
      <Counter n={1} />
      <Sfx at={scene.lead} name="ding" volume={0.5} />
      <Pop start={scene.lead} y={300}><Ion n={3} el="Na" size={190} color={GREEN} /></Pop>
      <Pop start={scene.lead + 6} y={560}><Plaque size={60} bg="#1F7A4A">наружу</Plaque></Pop>
      <Pop start={at(scene, 'два', 30)} y={760}><Ion n={2} el="K" size={150} /></Pop>
      <Pop start={at(scene, 'внутрь', 50)} y={980}><Plaque size={54} bg={C.fg} color={C.bg}>внутрь</Plaque></Pop>
      <Pop start={at(scene, 'внутрь', 50) + 8} y={1130}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 44, color: C.muted }}>за один цикл насоса</div></Pop>
    </AbsoluteFill>
  ),
  q2: Question(2, ['глюкоз', 'мозг']),
  a2: ({ scene }) => (
    <AbsoluteFill>
      <Counter n={2} />
      <Sfx at={scene.lead} name="ding" volume={0.5} />
      <Pop start={scene.lead} y={330}><Plaque size={76} bg="#1F7A4A">Облегчённая<br />диффузия</Plaque></Pop>
      <Pop start={at(scene, 'белком', 40)} y={720}><Chip size={64}>с белком</Chip></Pop>
      <Pop start={at(scene, 'без', 60)} y={880}><Chip size={64}>без АТФ</Chip></Pop>
    </AbsoluteFill>
  ),
  q3: Question(3, ['осмос', 'мембран']),
  a3: ({ scene }) => (
    <AbsoluteFill>
      <Counter n={3} />
      <Sfx at={scene.lead} name="ding" volume={0.5} />
      <Pop start={scene.lead} y={280}><Big size={230} color="#6FA8FF">Вода</Big></Pop>
      <Pop start={at(scene, 'растворитель', 20)} y={560}><Plaque size={58} bg={C.fg} color={C.bg}>растворитель</Plaque></Pop>
      <Pop start={at(scene, 'туда', 60)} y={760}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 62, color: C.fg, textAlign: 'center', lineHeight: 1.2 }}>идёт туда, где<br /><span style={{ color: GREEN }}>растворённого вещества больше</span></div></Pop>
    </AbsoluteFill>
  ),
  cta: ({ scene }) => <CtaScene scene={scene} score />,
};

export const TAILS = { hook: 10, q1: 42, a1: 14, q2: 42, a2: 14, q3: 42, a3: 14, cta: 45 };
export const Comp = makeReel(SCENES, ['hook', 'q1', 'q2', 'q3', 'cta']);
