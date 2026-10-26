// P001 — рилс «Бесплатная неделя»: тест 28 + 28 → личный разбор → пробные уроки → итог для родителей → «НЕДЕЛЯ» в комментариях.
// Без дат (сроки недели решает Мансур), без размера групп и без цены. По плану course/diagnostic (T39) и странице «Бесплатная неделя».
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Atom, Dna, Kinetic, Label, Row, Sfx, enter, punch } from '../kit.jsx';
import { Slam, useW } from '../scenes.jsx';
import { Chip, GREEN, Plaque } from './a001.jsx';

// 1. Хук: «Бесплатная неделя» — попробуй до оплаты.
const Hook = ({ scene }) => {
  const W = useW(scene);
  const [tWeek, tTry] = [W('неделя', 8), W('попробуй', 40)];
  return (
    <AbsoluteFill>
      <Row y={300}><Plaque at={0} bg={C.accent} size={96} rotate={-4}>Бесплатная</Plaque></Row>
      <Row y={480}><Plaque at={tWeek} bg={GREEN} size={150} rotate={-3}>неделя</Plaque></Row>
      <Appear at={tWeek + 8} y={720}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
          <Atom size={120} at={tWeek + 8} speed={1.4} />
          <Dna size={140} at={tWeek + 8} color={GREEN} />
          <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 62, lineHeight: 1.05, color: C.fg }}>ХИМБИО<br />ПРОСТО</div>
        </div>
      </Appear>
      <Row y={1000}><Chip at={tTry} bg={C.fg} border={C.fg} size={46}><span style={{ color: C.bg }}>попробуй курс до оплаты</span></Chip></Row>
      <Sfx at={0} name="boom" volume={0.5} /><Sfx at={tWeek} name="whoosh" /><Sfx at={tTry} name="pop" />
    </AbsoluteFill>
  );
};

// 2. Входной тест: 28 + 28 заданий.
const Test = ({ scene }) => {
  const W = useW(scene);
  const [tTest, t28, tChem, tBio, tFormat] = [W('входной', 4), W('двадцать', 20), W('химии', 34), W('биологии', 60), W('формате', 80)];
  return (
    <AbsoluteFill>
      <Kinetic at={tTest} y={230} size={96} rotate={-3} plaque>1. Входной тест</Kinetic>
      <Slam at={t28} y={430} size={230}>28 + 28</Slam>
      <Row y={760} style={{ gap: 22 }}>
        <Plaque at={tChem} bg={C.accent} size={60} rotate={-3}>химия</Plaque>
        <Plaque at={tBio} bg={GREEN} size={60} rotate={-2}>биология</Plaque>
      </Row>
      <Row y={940}><Chip at={tFormat} size={42}>задания в формате ЕНТ</Chip></Row>
      <Sfx at={tTest} name="whoosh" /><Sfx at={t28} name="boom" volume={0.5} /><Sfx at={tChem} name="pop" /><Sfx at={tBio} name="pop" /><Sfx at={tFormat} name="tick" />
    </AbsoluteFill>
  );
};

// 3. Личный разбор с преподавателем.
const Review = ({ scene }) => {
  const W = useW(scene);
  const [tTalk, tErr, tFix] = [W('разбор', 6), W('ошибки', 40), W('подтянуть', 60)];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={230} size={96} rotate={-3} plaque bg={GREEN}>2. Личный разбор</Kinetic>
      <Kinetic at={tTalk + 6} y={400} size={70} rotate={-2} from="right">с преподавателем</Kinetic>
      <Row y={600} style={{ flexDirection: 'column', alignItems: 'center', gap: 26 }}>
        <Chip at={tErr} bg={C.accent} border={C.accent} size={50}>где ошибки</Chip>
        <Chip at={tFix} size={50}>что подтянуть первым</Chip>
      </Row>
      <Sfx at={0} name="whoosh" /><Sfx at={tTalk + 6} name="whoosh" /><Sfx at={tErr} name="pop" /><Sfx at={tFix} name="pop" />
    </AbsoluteFill>
  );
};

// 4. Пробные уроки: химия и биология, онлайн, с ДЗ.
const CARDS = [['химия', 'chem'], ['биология', 'bio']];
const Lessons = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tChem, tBio, tOnline, tHw] = [W('химии', 20), W('биологии', 30), W('онлайн', 50), W('домашним', 60)];
  const at = [tChem, tBio];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={230} size={92} rotate={-3} plaque>3. Пробные уроки</Kinetic>
      <div style={{ position: 'absolute', top: 440, left: 90, right: 90, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 30 }}>
        {CARDS.map(([s, kind], k) => {
          const p = enter(frame, at[k], fps);
          return (
            <div key={k} style={{ opacity: p, transform: `translateY(${(1 - p) * 60}px) rotate(${k ? 2 : -2}deg)`, background: kind === 'chem' ? C.accent : GREEN, padding: '40px 30px 46px', textAlign: 'center' }}>
              {kind === 'chem' ? <Atom size={130} at={at[k]} speed={1.2} /> : <Dna size={150} at={at[k]} color={C.fg} />}
              <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 52, textTransform: 'uppercase', color: C.fg, marginTop: 18 }}>{s}</div>
            </div>
          );
        })}
      </div>
      <Row y={940} style={{ gap: 20 }}>
        <Chip at={tOnline} size={44}>онлайн</Chip>
        <Chip at={tHw} bg={C.fg} border={C.fg} size={44}><span style={{ color: C.bg }}>+ домашка</span></Chip>
      </Row>
      <Sfx at={0} name="whoosh" /><Sfx at={tChem} name="pop" /><Sfx at={tBio} name="pop" /><Sfx at={tOnline} name="tick" /><Sfx at={tHw} name="tick" />
    </AbsoluteFill>
  );
};

// 5. Итог для родителей: уровень и план.
const Report = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tParents, tLevel, tPlan] = [W('родителей', 14), W('уровень', 30), W('план', 50)];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={230} size={96} rotate={-3} plaque bg={GREEN}>4. Итог</Kinetic>
      <Kinetic at={tParents} y={400} size={74} rotate={-2} from="right">для родителей</Kinetic>
      {frame >= tLevel && (
        <Row y={580}>
          <div style={{ transform: `scale(${punch(frame, tLevel, 0.3)}) rotate(-3deg)`, background: C.fg, padding: '22px 40px 28px', fontFamily: F.display, fontWeight: 800, fontSize: 84, color: C.bg, whiteSpace: 'nowrap' }}>УРОВЕНЬ</div>
        </Row>
      )}
      <Row y={780}><Plaque at={tPlan} bg={C.accent} size={72} rotate={-3}>+ план к ЕНТ</Plaque></Row>
      <Appear at={tPlan + 10} y={980}>
        <div style={{ textAlign: 'center' }}><Label size={42} color={C.muted}>по химии и по биологии</Label></div>
      </Appear>
      <Sfx at={0} name="whoosh" /><Sfx at={tParents} name="whoosh" /><Sfx at={tLevel} name="boom" volume={0.45} /><Sfx at={tPlan} name="pop" />
    </AbsoluteFill>
  );
};

// 6. Призыв: «НЕДЕЛЯ» в комментариях, места ограничены, старт курса 1 ноября.
const Outro = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tWrite, tWord, tLimit, tStart] = [W('пиши', 30), W('неделя', 40), W('места', 70), W('старт', 90)];
  const letters = 'НЕДЕЛЯ'.split('');
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={200} size={80} rotate={-3}>Хочешь на</Kinetic>
      <Kinetic at={3} y={295} size={80} rotate={-3} from="right">бесплатную неделю?</Kinetic>
      <Kinetic at={tWrite} y={480} size={84} rotate={-3} from="right">Пиши</Kinetic>
      <Kinetic at={tWrite + 3} y={580} size={70} rotate={-3}>в комментариях</Kinetic>
      <Row y={710} style={{ gap: 6 }}>
        {frame >= tWord &&
          letters.map((ch, i) => {
            const p = enter(frame, tWord + i * 3, fps, { damping: 11, stiffness: 200 });
            return (
              <div key={i} style={{ transform: `translateY(${(1 - p) * -160}px) rotate(${(1 - p) * (i % 2 ? 18 : -18) - 4}deg)`, opacity: Math.min(1, p * 2), background: C.accent, fontFamily: F.display, fontWeight: 800, fontSize: 118, lineHeight: 1, padding: '14px 16px 22px', color: C.fg }}>
                {ch}
              </div>
            );
          })}
      </Row>
      <Row y={960} style={{ gap: 16 }}>
        <Chip at={tLimit} size={40}>места ограничены</Chip>
      </Row>
      <Row y={1080}><Plaque at={tStart} bg={GREEN} size={62} rotate={-3}>старт курса 1 ноября</Plaque></Row>
      <Sfx at={0} name="whoosh" /><Sfx at={tWrite} name="whoosh" />
      {letters.map((_, i) => <Sfx key={i} at={tWord + i * 3} name="pop" volume={0.3} />)}
      <Sfx at={tLimit} name="tick" /><Sfx at={tStart} name="pop" />
    </AbsoluteFill>
  );
};

export const SCENES = { hook: Hook, test: Test, review: Review, lessons: Lessons, report: Report, outro: Outro };
export const TAILS = { hook: 14, test: 20, review: 16, lessons: 16, report: 20, outro: 45 };
