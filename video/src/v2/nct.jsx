// Формат «задание ЕНТ» (Мансур 19.11.2026): настоящее задание из официального образца ЕНТ (testcenter.kz) дословно;
// в ролике говорим и пишем просто «задание ЕНТ», без «образец» и «НЦТ» (решение Мансура 19.11),
// как на бумаге теста → таймер → решение по шагам → ответ (+ ловушка) → «запись на курс». Монтаж v2 (kit2).
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, F } from '../theme.js';
import { CtaScene, GREEN, GUT, HOT, Plaque, Pop, RED, Sfx, TimerRing, at, makeReel, sp } from './kit2.jsx';

const INK = '#141414';

// Карточка «как в тесте»: белый лист, Times, номер, варианты A) B) C) D).
// mode: 'plain' | 'answer' (правильный — зелёный, ловушка — зачёркнута красным, остальные бледные).
const Paper = ({ cfg, mode = 'plain', start = 0, trapAt = 1e9, rightAt = 0 }) => {
  const f = useCurrentFrame();
  const p = sp(f, start);
  return (
    <div style={{ position: 'absolute', top: cfg.paperY ?? 330, left: GUT - 16, right: GUT - 16, background: '#F7F5EF', color: INK, padding: '34px 40px 30px', boxShadow: '0 24px 70px rgba(0,0,0,0.55)', transform: `translateY(${(1 - p) * 70}px) scale(${0.94 + 0.06 * p})`, opacity: Math.min(1, p * 1.6) }}>
      <div style={{ fontFamily: '"Times New Roman", Times, serif', fontSize: cfg.textSize ?? 56, lineHeight: 1.2 }}>
        <b>{cfg.num}.</b> {cfg.question}
      </div>
      <div style={{ marginTop: 22, display: 'flex', flexDirection: 'column', gap: 8 }}>
        {cfg.options.map(([l, t]) => {
          const isRight = mode === 'answer' && l === cfg.right && f >= rightAt;
          const isTrap = mode === 'answer' && l === cfg.trap && f >= trapAt;
          const dim = mode === 'answer' && !isRight && !isTrap && f >= rightAt;
          return (
            <div key={l} style={{ position: 'relative', display: 'flex', alignItems: 'center', gap: 14, padding: '6px 14px', fontFamily: '"Times New Roman", Times, serif', fontSize: cfg.optSize ?? 60, background: isRight ? '#CDEFD8' : isTrap ? '#FBD9DA' : 'transparent', borderLeft: `10px solid ${isRight ? GREEN : isTrap ? RED : 'transparent'}`, opacity: dim ? 0.35 : 1 }}>
              <span style={{ fontWeight: 700 }}>{l})</span> <span>{t}</span>
              {isRight && <span style={{ marginLeft: 'auto', fontFamily: F.display, fontWeight: 800, fontSize: 46, color: '#1F7A4A' }}>✓</span>}
              {isTrap && <div style={{ position: 'absolute', left: 60, right: 40, top: '52%', height: 6, background: RED }} />}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// Шаг решения: крупная строка на чёрном, появляется по слову озвучки.
const Step = ({ html, start, y, final = false, size }) => {
  const f = useCurrentFrame();
  const p = sp(f, start);
  if (f < start) return null;
  return (
    <div style={{ position: 'absolute', top: y, left: GUT, right: GUT, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * -90}px)` }}>
      <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: size ?? (final ? 84 : 70), color: final ? INK : C.fg, background: final ? HOT() : 'transparent', padding: final ? '6px 26px 14px' : 0, whiteSpace: 'nowrap' }} dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
};

export const makeNct = (cfg) => {
  const SCENES = {
    hook: ({ scene }) => (
      <AbsoluteFill>
        <Pop start={0} y={210}><Plaque size={42} bg={C.accent} rotate={-1}>Задание ЕНТ · {cfg.subjectName}</Plaque></Pop>
        <Paper cfg={cfg} start={4} />
        <Sfx at={4} name="whoosh" volume={0.3} />
      </AbsoluteFill>
    ),
    timer: ({ scene }) => (
      <AbsoluteFill>
        <Pop start={-30} y={210}><Plaque size={42} bg={C.accent} rotate={-1}>Задание ЕНТ · {cfg.subjectName}</Plaque></Pop>
        <Paper cfg={cfg} start={-30} />
        <TimerRing start={scene.lead} seconds={3} y={cfg.timerY ?? 1150} size={250} />
      </AbsoluteFill>
    ),
    solve: ({ scene }) => (
      <AbsoluteFill>
        <Pop start={0} y={220}><Plaque size={56} bg={C.fg} color={C.bg}>Решение</Plaque></Pop>
        {cfg.steps.map((s, i) => (
          <Step key={i} html={s.html} start={at(scene, s.stem, 20 + i * 60, s.nth ?? 0)} y={400 + i * 170} final={i === cfg.steps.length - 1 && cfg.finalStep} size={s.size} />
        ))}
      </AbsoluteFill>
    ),
    answer: ({ scene }) => {
      const r = scene.lead + 2;
      const trap = cfg.trap ? at(scene, 'ловушк', 80) : 1e9;
      return (
        <AbsoluteFill>
          <Sfx at={r} name="ding" volume={0.5} />
          <Pop start={-30} y={210}><Plaque size={42} bg={C.accent} rotate={-1}>Задание ЕНТ · {cfg.subjectName}</Plaque></Pop>
          <Paper cfg={cfg} mode="answer" start={-30} rightAt={r} trapAt={trap} />
          {cfg.trap && <Sfx at={trap} name="buzz" volume={0.35} />}
          {cfg.trapNote && <Pop start={trap + 6} y={cfg.noteY ?? 1170}><Plaque size={44} bg={RED} rotate={-1}>{cfg.trapNote}</Plaque></Pop>}
          {cfg.answerNote && <Pop start={at(scene, cfg.answerNote.stem, 60)} y={cfg.noteY ?? 1170}><Plaque size={44} bg={C.card} rotate={0}>{cfg.answerNote.text}</Plaque></Pop>}
        </AbsoluteFill>
      );
    },
    cta: ({ scene }) => <CtaScene scene={scene} />,
  };
  const TAILS = { hook: 12, timer: 40, solve: 24, answer: 24, cta: 45 };
  return { TAILS, Comp: makeReel(SCENES, ['hook', 'timer', 'cta'], cfg.subject) };
};
