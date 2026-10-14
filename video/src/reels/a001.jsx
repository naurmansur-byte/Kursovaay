// A001 — рекламный рилс для учеников: хук «100 из 140» → «Лови — это наш курс» → формат, цена, старт → «ТЕСТ» в директ.
// Химия — красный акцент, биология — тёмно-зелёный (решение Мансура 13.10).
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Atom, Dna, Kinetic, Label, Row, Sfx, enter, punch } from '../kit.jsx';
import { Slam, useW } from '../scenes.jsx';

export const GREEN = '#1F7A4A';

export const Chip =({ children, at, bg = 'transparent', border = C.fg, size = 40 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  return (
    <div style={{ transform: `scale(${enter(frame, at, fps)})`, border: `4px solid ${border}`, background: bg, padding: '10px 24px 14px', fontFamily: F.body, fontWeight: 800, fontSize: size, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>
      {children}
    </div>
  );
};

export const Plaque = ({ children, at, bg, size = 84, rotate = -3, color = C.fg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 11, stiffness: 210, mass: 0.6 });
  return (
    <div style={{ display: 'inline-block', transform: `scale(${1.6 - 0.6 * p}) rotate(${rotate}deg)`, opacity: Math.min(1, p * 3), background: bg, padding: '12px 30px 18px', fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: 1, textTransform: 'uppercase', color, whiteSpace: 'nowrap' }}>
      {children}
    </div>
  );
};

// 1. Хук: «100 из 140» с первого кадра.
const Hook = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [t140, tChem, tBio] = [W('сорока', 14), W('химия', 40), W('биология', 52)];
  return (
    <AbsoluteFill>
      <Slam at={0} y={330} size={330}>100</Slam>
      {frame >= t140 && (
        <Row y={760}>
          <div style={{ transform: `scale(${punch(frame, t140, 0.3)})`, fontFamily: F.display, fontWeight: 800, fontSize: 120, color: C.fg, whiteSpace: 'nowrap' }}>
            из 140 <span style={{ color: C.muted, fontSize: 70 }}>на ЕНТ</span>
          </div>
        </Row>
      )}
      <Row y={960} style={{ flexDirection: 'column', alignItems: 'center', gap: 22 }}>
        <Plaque at={tChem} bg={C.accent} size={64}>химия — 50</Plaque>
        <Plaque at={tBio} bg={GREEN} size={64} rotate={-2}>биология — 50</Plaque>
      </Row>
      <Sfx at={0} name="boom" volume={0.55} /><Sfx at={t140} name="whoosh" /><Sfx at={tChem} name="pop" /><Sfx at={tBio} name="pop" />
    </AbsoluteFill>
  );
};

// 2. «Сдаёшь хим-био? Лови — это наш курс».
const Catch = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tClass, tCatch, tCourse] = [8, W('лови', 30), W('курс', 45)];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={260} size={100} rotate={-4} plaque>Сдаёшь хим-био?</Kinetic>
      <Kinetic at={tClass} y={420} size={80} rotate={-3} from="right" plaque bg={GREEN}>11 класс</Kinetic>
      {frame >= tCatch && (
        <Row y={640}>
          <div style={{ transform: `scale(${punch(frame, tCatch, 0.35, 12)}) rotate(-5deg)`, fontFamily: F.display, fontWeight: 800, fontSize: 210, lineHeight: 1, color: C.fg }}>ЛОВИ!</div>
        </Row>
      )}
      <Appear at={tCourse} y={940}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
          <Atom size={130} at={tCourse} speed={1.4} />
          <Dna size={150} at={tCourse} color={GREEN} />
          <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 66, lineHeight: 1.05, color: C.fg }}>ХИМБИО<br />ПРОСТО</div>
        </div>
      </Appear>
      <Sfx at={1} name="whoosh" /><Sfx at={tClass} name="whoosh" /><Sfx at={tCatch} name="boom" volume={0.5} /><Sfx at={tCourse} name="pop" />
    </AbsoluteFill>
  );
};

// 3. Курс: химия + биология, по учебникам НЦТ, формат теста.
const Course = ({ scene }) => {
  const W = useW(scene);
  const [tChem, tBio, tOne, tBooks, tTest] = [W('химия', 14), W('биология', 22), W('одном', 40), W('учебникам', 60), W('теста', 80)];
  return (
    <AbsoluteFill>
      <Row y={250}><Plaque at={tChem} bg={C.accent} size={120} rotate={-4}>Химия</Plaque></Row>
      <Row y={430}><Plaque at={tBio} bg={GREEN} size={110} rotate={-3}>+ биология</Plaque></Row>
      <Kinetic at={tOne} y={630} size={74} rotate={-2}>в одном курсе</Kinetic>
      <Row y={820} style={{ flexDirection: 'column', alignItems: 'center', gap: 22 }}>
        <Chip at={tBooks} border={C.fg}>по учебникам НЦТ</Chip>
        <Chip at={tTest} bg={C.accent} border={C.accent}>в формате теста ЕНТ</Chip>
      </Row>
      <Sfx at={tChem} name="pop" /><Sfx at={tBio} name="pop" /><Sfx at={tOne} name="whoosh" /><Sfx at={tBooks} name="tick" /><Sfx at={tTest} name="tick" />
    </AbsoluteFill>
  );
};

// 4. Неделя: 4 урока, 2 + 2, по 90 минут, группа 5 человек.
const DAYS = [['ПН', 'химия', 'chem'], ['ВТ', 'биология', 'bio'], ['ЧТ', 'химия', 'chem'], ['ПТ', 'биология', 'bio']];
const Week = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tFour, tChem, tBio, t90, t5] = [W('четыре', 2), W('химии', 30), W('биологии', 45), W('девяносто', 70), W('пять', 100)];
  const at = (k) => (k % 2 === 0 ? tChem : tBio) + Math.floor(k / 2) * 4;
  return (
    <AbsoluteFill>
      <Kinetic at={tFour} y={220} size={96} rotate={-3} plaque>4 урока в неделю</Kinetic>
      <div style={{ position: 'absolute', top: 420, left: 72, right: 72, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 26 }}>
        {DAYS.map(([d, s, kind], k) => {
          const p = enter(frame, at(k), fps);
          return (
            <div key={k} style={{ opacity: p, transform: `translateY(${(1 - p) * 60}px) rotate(${k % 2 ? 2 : -2}deg)`, background: kind === 'chem' ? C.accent : GREEN, padding: '26px 30px 30px' }}>
              <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 70, color: C.fg, lineHeight: 1 }}>{d}</div>
              <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 46, textTransform: 'uppercase', color: C.fg, marginTop: 12 }}>{s}</div>
              <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 38, color: C.fg, opacity: frame >= t90 ? 1 : 0.25, transform: `scale(${punch(frame, t90, 0.25)})`, transformOrigin: 'left center', marginTop: 8 }}>90 минут</div>
            </div>
          );
        })}
      </div>
      <Row y={1110}><Chip at={t5} bg={C.fg} border={C.fg} size={44}><span style={{ color: C.bg }}>5 человек в группе</span></Chip></Row>
      <Sfx at={tFour} name="whoosh" />{DAYS.map((_, k) => <Sfx key={k} at={at(k)} name="pop" volume={0.3} />)}<Sfx at={t90} name="ding" volume={0.4} /><Sfx at={t5} name="pop" />
    </AbsoluteFill>
  );
};

// Круглая наклейка скидки (решение Мансура 14.10: первым 20 — скидка 30 %).
const Sale = ({ at, y }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 10, stiffness: 200, mass: 0.6 });
  return (
    <Row y={y}>
      <div style={{ width: 300, height: 300, borderRadius: '50%', background: C.accent, boxShadow: `0 0 0 10px ${C.bg}, 0 0 0 16px ${C.fg}`, transform: `scale(${2 - p}) rotate(${10 + (1 - p) * 40}deg)`, opacity: Math.min(1, p * 3), display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 70, color: C.fg, whiteSpace: 'nowrap' }}>−30%</div>
        <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 32, textTransform: 'uppercase', color: C.fg, marginTop: 8 }}>первым 20</div>
      </div>
    </Row>
  );
};

// 5. Цена, скидка и старт.
const Price = ({ scene }) => {
  const W = useW(scene);
  const [tSum, tMonth, tBoth, tSale, tStart] = [W('девятнадцать', 2), W('месяц', 40), W('оба', 52), W('скидка', 70), W('старт', 100)];
  return (
    <AbsoluteFill>
      <Slam at={tSum} y={260} size={145}>19 500 ₸</Slam>
      <Kinetic at={tMonth} y={530} size={84} rotate={-2}>в месяц</Kinetic>
      <Row y={660}><Chip at={tBoth} size={42}>химия + биология вместе</Chip></Row>
      <Sale at={tSale} y={800} />
      <Row y={1170}><Plaque at={tStart} bg={GREEN} size={70} rotate={-4}>Старт 2 ноября</Plaque></Row>
      <Sfx at={tSum} name="boom" volume={0.5} /><Sfx at={tMonth} name="whoosh" /><Sfx at={tBoth} name="pop" /><Sfx at={tSale} name="boom" volume={0.55} /><Sfx at={tStart} name="pop" />
    </AbsoluteFill>
  );
};

// 6. Призыв: напиши нам в WhatsApp (кнопка рекламы ведёт в WhatsApp; решение Мансура 14.10).
const Cta = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tWa, tFree] = [W('ватсап', 14), W('бесплатный', 40)];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={240} size={110} rotate={-3}>Напиши нам</Kinetic>
      {frame >= tWa && (
        <Row y={450}>
          <div style={{ transform: `scale(${punch(frame, tWa, 0.3, 12)}) rotate(-4deg)`, background: '#25D366', padding: '20px 44px 28px', fontFamily: F.display, fontWeight: 800, fontSize: 130, lineHeight: 1, color: C.bg, whiteSpace: 'nowrap' }}>WhatsApp</div>
        </Row>
      )}
      <Appear at={tFree} y={760}>
        <div style={{ textAlign: 'center' }}>
          <Label size={50} color={C.fg}>бесплатный входной тест</Label>
        </div>
      </Appear>
      <Sfx at={1} name="whoosh" /><Sfx at={tWa} name="boom" volume={0.5} /><Sfx at={tFree} name="ding" volume={0.45} />
    </AbsoluteFill>
  );
};

// Логотип для переходов «лови наш курс» в вариантах A002/A003.
export const Logo = ({ at }) => (
  <Appear at={at} y={960}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
      <Atom size={130} at={at} speed={1.4} />
      <Dna size={150} at={at} color={GREEN} />
      <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 66, lineHeight: 1.05, color: C.fg }}>ХИМБИО<br />ПРОСТО</div>
    </div>
  </Appear>
);

// Общая часть всех вариантов: курс → неделя → цена → призыв.
export const BODY = { course: Course, week: Week, price: Price, cta: Cta };
export const SCENES = { hook: Hook, catch: Catch, ...BODY };
export const TAILS = { cta: 45 };
