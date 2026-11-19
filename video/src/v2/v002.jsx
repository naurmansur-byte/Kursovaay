// V002 — монтаж v2 «Ловушка: неправильно → правильно». Биология, неделя 3: облегчённая диффузия и активный транспорт
// (конспект недели 3: «Канал не насос…», глюкоза из крови в мозг — облегчённая диффузия, Na⁺/K⁺-АТФаза против градиентов).
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { C, F } from '../theme.js';
import { Big, Center, Chip, CtaScene, GREEN, GUT, Membrane, Plaque, Pop, RED, Sfx, Stamp, at, clamp, makeReel, sp } from './kit2.jsx';

const YEL = '#F2C94C';

const Column = ({ x, start, title, arrow, color, sub }) => {
  const f = useCurrentFrame();
  const p = sp(f, start);
  if (f < start) return null;
  const bob = Math.sin(f / 6) * 14 * (arrow === '↓' ? 1 : -1);
  return (
    <div style={{ position: 'absolute', top: 560, left: x, width: 440, height: 640, background: C.card, border: `5px solid ${color}`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 24, opacity: Math.min(1, p * 1.5), transform: `translateY(${(1 - p) * 80}px)` }}>
      <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 52, color: C.fg, textAlign: 'center', lineHeight: 1.1, whiteSpace: 'pre-line' }}>{title}</div>
      <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 200, color, lineHeight: 1, transform: `translateY(${bob}px)` }}>{arrow}</div>
      <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 50, color, textAlign: 'center', lineHeight: 1.15, whiteSpace: 'pre-line' }}>{sub}</div>
    </div>
  );
};

const SCENES = {
  hook: ({ scene }) => {
    const f = useCurrentFrame();
    const a1 = at(scene, 'глюкоза', scene.lead);
    const a3 = at(scene, 'тратит', 100);
    return (
      <AbsoluteFill>
        <Pop start={a1} y={240}><Big size={104}>Глюкоза</Big></Pop>
        <Pop start={a1 + 6} y={370}><div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 50, color: C.muted }}>входит в клетку через белок</div></Pop>
        <Center y={470}><Membrane mode="carrier" t={f} h={560} top="снаружи" bottom="клетка" /></Center>
        <Pop start={a3} y={1080}><Plaque size={86} bg={RED}>Тратит АТФ?</Plaque></Pop>
        <Sfx at={a3} name="pop" volume={0.5} />
      </AbsoluteFill>
    );
  },
  myth: ({ scene }) => (
    <AbsoluteFill>
      <Stamp start={scene.lead} text="НЕТ!" y={430} />
      <Pop start={at(scene, 'ловушка', 30)} y={860}><Plaque size={64} bg={C.fg} color={C.bg}>частая ловушка ЕНТ</Plaque></Pop>
    </AbsoluteFill>
  ),
  passive: ({ scene }) => {
    const f = useCurrentFrame();
    return (
      <AbsoluteFill>
        <Pop start={scene.lead} y={230}><Plaque size={56} bg="#1F7A4A" rotate={-1}>Облегчённая диффузия</Plaque></Pop>
        <Center y={410}><Membrane mode="carrier" t={f} h={540} top="кровь — глюкозы много" bottom="клетка мозга — мало" /></Center>
        <Pop start={at(scene, 'градиент', 60)} y={975}><Chip>по градиенту</Chip></Pop>
        <Pop start={at(scene, 'белок', 90)} y={1085}><Chip>через белок-переносчик</Chip></Pop>
        <Pop start={at(scene, 'без', 130)} y={1195}><Chip>без АТФ</Chip></Pop>
      </AbsoluteFill>
    );
  },
  active: ({ scene }) => {
    const f = useCurrentFrame();
    const tr = at(scene, 'тратит', 100);
    return (
      <AbsoluteFill>
        <Pop start={scene.lead} y={230}><Plaque size={56} bg="#8A3B3F" rotate={1}>Активный транспорт</Plaque></Pop>
        <Center y={410}><Membrane mode="pump" t={f} atp={interpolate(f, [tr, tr + 10], [0, 1], clamp)} h={540} top="снаружи — Na⁺ много" bottom="внутри — мало" /></Center>
        <Pop start={at(scene, 'насос', 20)} y={975}><Chip tone={YEL}>натрий-калиевый насос</Chip></Pop>
        <Pop start={at(scene, 'против', 50)} y={1085}><Chip tone={YEL}>против градиента</Chip></Pop>
        <Pop start={tr} y={1195}><Chip tone={YEL}>тратит АТФ</Chip></Pop>
        <Sfx at={tr} name="boom" volume={0.3} />
      </AbsoluteFill>
    );
  },
  rule: ({ scene }) => (
    <AbsoluteFill>
      <Pop start={scene.lead} y={250}><Plaque size={54} bg={C.fg} color={C.bg}>Смотри на градиент,<br />а не на белок</Plaque></Pop>
      <Column x={GUT} start={at(scene, 'пассивно', 90)} title={'по\nградиенту'.toUpperCase()} arrow="↓" color={GREEN} sub={'пассивно,\nбез АТФ'} />
      <Column x={1080 - GUT - 440} start={at(scene, 'против', 120)} title={'против\nградиента'.toUpperCase()} arrow="↑" color={YEL} sub={'нужна\nэнергия АТФ'} />
    </AbsoluteFill>
  ),
  cta: ({ scene }) => <CtaScene scene={scene} />,
};

export const TAILS = { hook: 14, myth: 10, passive: 16, active: 16, rule: 24, cta: 45 };
export const Comp = makeReel(SCENES, ['hook', 'myth', 'rule', 'cta']);
