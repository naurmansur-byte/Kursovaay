// Y004 — трейлер канала «ХимБио просто»: для кого канал и что на нём разбираем. 1920×1080, ~1 мин.
// Химия — красный акцент, биология — зелёный (SUBJECT).
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F, SUBJECT } from '../theme.js';
import { Appear, Atom, Dna, Kinetic, Row, Sfx, enter, punch } from '../kit.jsx';
import { Slam, TopicIntro, useW } from '../scenes.jsx';

const RED = SUBJECT.chem;
const GREEN = SUBJECT.bio;
const Abs = ({ x, y, children, style }) => <div style={{ position: 'absolute', left: x, top: y, ...style }}>{children}</div>;

const Chip = ({ children, at, color = C.fg, fill }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps);
  return (
    <div style={{ transform: `scale(${p}) rotate(-2deg)`, opacity: p, padding: '16px 30px', border: `4px solid ${color}`, background: fill ?? C.bg, fontFamily: F.body, fontWeight: 800, fontSize: 42, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>{children}</div>
  );
};

const Title = ({ scene }) => (
  <TopicIntro scene={scene} tag="О канале" title="ХимБио просто" plaque="химия + биология"
    items={[['Разборы тем ЕНТ', 'разбираем'], ['Сложные задачи — по шагам', 'решаем'], ['Ловушки, где теряют баллы', 'ловушки'], ['Короткие уроки на 3–5 минут', 'выпускаем']]} />
);

// Шкала ЕНТ: 140 баллов, профиль хим-био — 100.
const Who = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tP, tBar, t100] = [W('профиль', 77), W('химия', 92), W('сто', 180)];
  const parts = [['история РК', 20, C.faint], ['мат. грамотность', 10, C.faint], ['чтение', 10, C.faint], ['химия', 50, RED], ['биология', 50, GREEN]];
  const total = 1640;
  let x = 0;
  return (
    <AbsoluteFill>
      <Kinetic at={tP} y={150} size={80} rotate={-3}>Профиль «химия — биология»</Kinetic>
      <Abs x={140} y={420} style={{ width: total }}>
        {parts.map(([name, pts, col], i) => {
          const w = (pts / 140) * total;
          const at = tBar + i * 5;
          const p = frame < at ? 0 : enter(frame, at, fps);
          const left = x;
          x += w;
          return (
            <div key={name} style={{ position: 'absolute', left, width: w - 6, top: 0 }}>
              <div style={{ height: 110, background: col, transform: `scaleX(${p})`, transformOrigin: 'left', display: 'grid', placeItems: 'center', fontFamily: F.display, fontWeight: 800, fontSize: pts >= 50 ? 56 : 34, color: C.fg }}>{p > 0.6 ? pts : ''}</div>
              <div style={{ marginTop: 14, fontFamily: F.body, fontWeight: 800, fontSize: pts >= 50 ? 38 : 24, color: pts >= 50 ? C.fg : C.muted, opacity: p }}>{name}</div>
            </div>
          );
        })}
      </Abs>
      <Slam at={t100} y={680} size={120}>100 из 140</Slam>
      <Sfx at={tP} name="whoosh" />{parts.map((_, i) => <Sfx key={i} at={tBar + i * 5} name="tick" volume={0.4} />)}<Sfx at={t100} name="boom" volume={0.5} />
    </AbsoluteFill>
  );
};

const Topics = ({ scene, title, color, icon, chips }) => {
  const W = useW(scene);
  const times = chips.map(([, stem], i) => W(stem, 30 + i * 30));
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={110} rotate={-4} plaque bg={color}>{title}</Kinetic>
      <Abs x={140} y={420}>{icon}</Abs>
      <Abs x={560} y={400} style={{ width: 1260, display: 'flex', flexWrap: 'wrap', gap: 24 }}>
        {chips.map(([text], i) => <Chip key={text} at={times[i]} color={color} fill={i % 2 ? undefined : color}>{text}</Chip>)}
      </Abs>
      <Sfx at={2} name="whoosh" />{times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
    </AbsoluteFill>
  );
};

const Chem = ({ scene }) => (
  <Topics scene={scene} title="Химия" color={RED} icon={<Atom size={330} at={2} speed={1.2} />}
    chips={[['моль и расчёты', 'моль'], ['ОВР и электролиз', 'окислительно'], ['неорганика', 'неорганика'], ['органика', 'органика'], ['задачи на смеси и выход', 'смеси']]} />
);

const Bio = ({ scene }) => (
  <Topics scene={scene} title="Биология" color={GREEN} icon={<Dna size={380} at={2} color={GREEN} />}
    chips={[['клетка и биохимия', 'клетка'], ['физиология', 'физиология'], ['генетика и решётка Пеннета', 'генетика'], ['эволюция', 'эволюция']]} />
);

// Карточка шага: влетает слева.
const Step = ({ n, t, at, col, x }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 14, stiffness: 140 });
  return (
    <Abs x={x - (1 - p) * 200} y={430} style={{ opacity: Math.min(1, p * 2) }}>
      <div style={{ width: 480, padding: '36px 40px', background: col, color: C.fg, transform: 'rotate(-3deg)' }}>
        <div style={{ font: `800 80px ${F.display}` }}>{n}</div>
        <div style={{ font: `800 54px ${F.display}`, textTransform: 'uppercase' }}>{t}</div>
      </div>
    </Abs>
  );
};

const How = ({ scene }) => {
  const W = useW(scene);
  const steps = [['1', 'Почему', W('почему', 77), RED], ['2', 'Алгоритм', W('алгоритм', 128), GREEN], ['3', 'Задача ЕНТ', W('задача', 169), RED]];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={84} rotate={-3}>Как устроено каждое видео</Kinetic>
      {steps.map(([n, t, at, col], i) => <Step key={n} n={n} t={t} at={at} col={col} x={150 + i * 560} />)}
      <Sfx at={2} name="whoosh" />{steps.map(([n, , at]) => <Sfx key={n} at={at} name="pop" volume={0.45} />)}
    </AbsoluteFill>
  );
};

const Course = ({ scene }) => {
  const W = useW(scene);
  const [tC, tH, tG, tS, tD] = [W('онлайн', 72), W('химия', 124), W('группы', 165), W('старт', 203), W('директ', 298)];
  return (
    <AbsoluteFill>
      <Kinetic at={tC} y={150} size={100} rotate={-4} plaque>Онлайн-курс</Kinetic>
      <Row y={400} style={{ gap: 22 }}>
        <Chip at={tH} color={GREEN} fill={GREEN}>химия + биология</Chip>
        <Chip at={tG}>группы по 5</Chip>
        <Chip at={tS} color={RED} fill={RED}>старт 1 ноября</Chip>
      </Row>
      <Appear at={tD - 20} y={600}><div style={{ font: `700 44px ${F.body}`, color: C.muted }}>Запись — в директ Instagram</div></Appear>
      <Kinetic at={tD} y={680} size={100} rotate={-2}>@himbio.prosto</Kinetic>
      <Sfx at={tC} name="whoosh" />{[tH, tG, tS].map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}<Sfx at={tD} name="whoosh" />
    </AbsoluteFill>
  );
};

const Cta = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tSub = W('подписывайся', 2);
  const pulse = 1 + 0.05 * Math.sin(frame / 6);
  return (
    <AbsoluteFill>
      <Row y={200} style={{ gap: 60, alignItems: 'center' }}>
        <Atom size={260} at={2} speed={1.2} /><Dna size={300} at={6} color={GREEN} />
      </Row>
      <Row y={560}>
        <div style={{ transform: `scale(${punch(frame, tSub + 4, 0.25) * pulse}) rotate(-3deg)`, padding: '30px 70px', background: RED, borderRadius: 80, font: `800 72px ${F.display}`, color: '#fff', whiteSpace: 'nowrap' }}>ПОДПИСАТЬСЯ</div>
      </Row>
      <Appear at={W('разборы', 51)} y={780}><div style={{ font: `800 46px ${F.body}`, color: C.fg }}>разборы всех тем ЕНТ по химии и биологии</div></Appear>
      <Sfx at={tSub + 4} name="boom" volume={0.5} /><Sfx at={W('разборы', 51)} name="ding" volume={0.45} />
    </AbsoluteFill>
  );
};

export const SCENES = { title: Title, who: Who, chem: Chem, bio: Bio, how: How, course: Course, cta: Cta };
export const TAILS = { title: 20, who: 24, chem: 16, bio: 16, how: 16, course: 24, cta: 70 };
