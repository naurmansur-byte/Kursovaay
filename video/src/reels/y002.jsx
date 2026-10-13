// Y002 — промо курса для YouTube, 1920×1080. Концепция: content/youtube/Y002-promo/brief.md
import React from 'react';
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Atom, Card, Flame, Kinetic, Label, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { A, Slam, TopicIntro, useW } from '../scenes.jsx';

const Abs = ({ x, y, children, style }) => <div style={{ position: 'absolute', left: x, top: y, ...style }}>{children}</div>;

// Плавный влёт элемента: снизу/сбоку, с поворотом.
const Fly = ({ at, x, y, from = [0, 300], rot = 0, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 14, stiffness: 140 });
  return (
    <Abs x={x + (1 - p) * from[0]} y={y + (1 - p) * from[1]} style={{ opacity: Math.min(1, p * 2), transform: `rotate(${rot * p}deg)` }}>
      {children}
    </Abs>
  );
};

const Hook = ({ scene }) => {
  const W = useW(scene);
  const [t1, t2, t3, t4] = [W('сорок', 2), W('восемьдесят', 40), W('химия', 80), W('почему', 200)];
  return (
    <AbsoluteFill>
      <Kinetic at={t1} y={200} size={140} rotate={-4}>40 заданий</Kinetic>
      <Kinetic at={t2} y={370} size={140} rotate={-3} from="right">80 минут</Kinetic>
      <Kinetic at={t3} y={560} size={130} rotate={-4} plaque punchAt={t3 + 4}>Химия</Kinetic>
      <Slam at={t4} y={770} size={90}>Почему её боятся?</Slam>
      <Abs x={1560} y={600}><Atom size={300} at={t1} speed={1.4} /></Abs>
      <Sfx at={t1} name="whoosh" /><Sfx at={t2} name="whoosh" /><Sfx at={t3} name="pop" volume={0.5} /><Sfx at={t4} name="boom" volume={0.6} />
    </AbsoluteFill>
  );
};

const Pain = ({ scene }) => {
  const W = useW(scene);
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={230} size={84} rotate={-3}>Дело не в том, что ты «не технарь»</Kinetic>
      <Slam at={W('три', 60)} y={480} size={170}>3 причины</Slam>
      <Kinetic at={W('теряют', 100)} y={760} size={64} rotate={-2} from="right">почему теряют баллы</Kinetic>
      <Sfx at={2} name="whoosh" /><Sfx at={W('три', 60)} name="boom" volume={0.55} />
    </AbsoluteFill>
  );
};

const Reason = ({ n, title, at, children, red = false }) => (
  <AbsoluteFill style={red ? { background: C.accent } : undefined}>
    <Kinetic at={at} y={190} size={100} rotate={-3} color={red ? C.bg : undefined}>{`#${n} · ${title}`}</Kinetic>
    {children}
  </AbsoluteFill>
);

const R1 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tq = W('задача', 90);
  return (
    <Reason n={1} title="Формулы без смысла" at={2}>
      <Appear at={W('выучил', 40)} y={470}><TeX tex="n = \dfrac{m}{M}" size={170} /></Appear>
      {frame >= tq && ['?', '??', '?'].map((q, i) => (
        <Fly key={i} at={tq + i * 5} x={[520, 1340, 1460][i]} y={[380, 360, 660][i]} rot={[-14, 10, -6][i]}>
          <div style={{ font: `800 150px ${F.display}`, color: C.accent }}>{q}</div>
        </Fly>
      ))}
      <Sfx at={2} name="whoosh" />{[0, 1, 2].map((i) => <Sfx key={i} at={tq + i * 5} name="pop" volume={0.3} />)}
    </Reason>
  );
};

const R2 = ({ scene }) => {
  const W = useW(scene);
  const t = W('пять', 40);
  const chips = ['4,6\\,\\text{г}', '8{,}8\\,\\text{г}\\ \\mathrm{CO_2}', '5{,}4\\,\\text{г}\\ \\mathrm{H_2O}', 'D_{\\mathrm{H_2}} = 23', '\\;?\\;'];
  const pos = [[260, 470, -6], [760, 430, 4], [1280, 500, -3], [520, 680, 5], [1080, 700, -8]];
  return (
    <Reason n={2} title="Теряешься в условии" at={2}>
      {chips.map((c, i) => (
        <Fly key={i} at={t + i * 4} x={pos[i][0]} y={pos[i][1]} from={[0, 200]} rot={pos[i][2]}>
          <div style={{ padding: '18px 30px', border: `4px solid ${i === 4 ? C.accent : C.fg}`, background: C.card }}>
            <TeX tex={c} size={66} color={i === 4 ? C.accent : C.fg} />
          </div>
        </Fly>
      ))}
      <Sfx at={2} name="whoosh" />{chips.map((_, i) => <Sfx key={i} at={t + i * 4} name="tick" volume={0.5} />)}
    </Reason>
  );
};

const R3 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const t50 = W('пятьдесят', 120);
  const tBad = W('неверный', t50 + 30);
  return (
    <AbsoluteFill style={{ transform: `translateX(${shake(frame, t50, 14, 20)}px)` }}>
      <Reason n={3} title="Ловушки" at={2} red>
        <Appear at={W('забыл', 20)} y={480}>
          <Card width={1420}>
            <TeX tex={`M(\\mathrm{H_2SO_4}) = 2 + 32 + 16 = ${frame >= t50 ? A('50') : '\\;?'}`} size={66} />
            <div style={{ marginTop: 16, font: `700 40px ${F.body}`, color: C.muted }}>забыли индекс 4 у кислорода — нужно 4 · 16 = 64, и M = 98</div>
          </Card>
        </Appear>
        {frame >= tBad && <Abs x={1620} y={680}><div style={{ font: `800 200px ${F.display}`, color: C.bg, transform: `scale(${punch(frame, tBad, 0.3)})` }}>✗</div></Abs>}
      </Reason>
      <Sfx at={2} name="whoosh" /><Sfx at={t50} name="buzz" volume={0.5} />
    </AbsoluteFill>
  );
};

const Method = ({ scene }) => {
  const W = useW(scene);
  const steps = [['1', 'Почему', W('почему', 90)], ['2', 'Алгоритм', W('алгоритм', 160)], ['3', 'Ловушки', W('ловушк', 230)]];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={160} size={86} rotate={-3}>«ХимБио просто» учит иначе</Kinetic>
      {steps.map(([n, t, at], i) => (
        <Fly key={n} at={at} x={150 + i * 560} y={470} from={[-200, 0]}>
          <div style={{ width: 480, padding: '36px 40px', background: i === 2 ? C.accent : C.fg, color: i === 2 ? '#fff' : C.bg, transform: 'rotate(-3deg)' }}>
            <div style={{ font: `800 80px ${F.display}` }}>{n}</div>
            <div style={{ font: `800 56px ${F.display}`, textTransform: 'uppercase' }}>{t}</div>
          </div>
        </Fly>
      ))}
      {[0, 1].map((i) => <Fly key={i} at={steps[i + 1][2] - 4} x={640 + i * 560} y={540} from={[-60, 0]}><div style={{ font: `800 90px ${F.display}`, color: C.accent }}>→</div></Fly>)}
      <Sfx at={2} name="whoosh" />{steps.map(([n, , at]) => <Sfx key={n} at={at} name="pop" volume={0.45} />)}
    </AbsoluteFill>
  );
};

const Task = ({ scene }) => {
  const W = useW(scene);
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={140} size={80} rotate={-3} plaque>Задача ЕНТ</Kinetic>
      <Abs x={120} y={420}><Flame size={360} at={W('сгорело', 6)} /></Abs>
      <Appear at={W('сгорело', 8)} y={380} dy={60}>
        <div style={{ marginLeft: 380 }}>
          <Card width={1280}>
            <Label>Повышенная сложность · авторская</Label>
            <div style={{ marginTop: 18, display: 'grid', gap: 12 }}>
              <TeX tex="m = 4{,}6\,\text{г}\ \to\ \mathrm{CO_2}\ 8{,}8\,\text{г} + \mathrm{H_2O}\ 5{,}4\,\text{г}" size={54} />
              <TeX tex="D_{\mathrm{H_2}} = 23.\quad \text{Формула?}" size={54} />
            </div>
          </Card>
        </div>
      </Appear>
      <Sfx at={2} name="whoosh" /><Sfx at={W('формула', 300)} name="tick" volume={0.5} />
    </AbsoluteFill>
  );
};

const S1 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tC, tC2, tH, tH2] = [W('углерод', 20), W('две', 70), W('водород', 120), W('шесть', 170)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={80} rotate={-3}>Шаг 1 · куда ушли атомы</Kinetic>
      <Fly at={tC} x={90} y={400} from={[-300, 0]}>
        <Card width={800}><Label>Углерод → CO₂</Label>
          <div style={{ marginTop: 14 }}><TeX tex={`n(\\mathrm{C}) = \\dfrac{8{,}8}{44} = ${frame >= tC2 ? A('0{,}2') : '\\;?'}`} size={60} /></div></Card>
      </Fly>
      <Fly at={tH} x={980} y={400} from={[300, 0]}>
        <Card width={800}><Label>Водород → H₂O</Label>
          <div style={{ marginTop: 14 }}><TeX tex={`n(\\mathrm{H}) = ${A('2')}\\cdot\\dfrac{5{,}4}{18} = ${frame >= tH2 ? A('0{,}6') : '\\;?'}`} size={60} /></div></Card>
      </Fly>
      <Sfx at={tC} name="whoosh" /><Sfx at={tC2} name="pop" /><Sfx at={tH} name="whoosh" /><Sfx at={tH2} name="pop" />
    </AbsoluteFill>
  );
};

const S2 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tCheck, tThree, tO] = [W('проверь', 60), W('три', 110), W('кислород', 220)];
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, tCheck, 14, 18)}px)` }}>
      <Kinetic at={2} y={140} size={110} rotate={-5} color={C.bg} punchAt={tCheck}>Ловушка: проверь массу</Kinetic>
      <Appear at={tThree} y={400}>
        <Card width={1640}>
          <TeX tex={`m(\\mathrm{C}) + m(\\mathrm{H}) = 2{,}4 + 0{,}6 = ${A('3{,}0')}\\,\\text{г} \\ne 4{,}6\\,\\text{г}`} size={60} />
          {frame >= tO && <div style={{ marginTop: 16 }}><TeX tex={`m(\\mathrm{O}) = 1{,}6\\,\\text{г}\\ \\to\\ n(\\mathrm{O}) = ${A('0{,}1')}\\ \\text{моль}`} size={60} /></div>}
        </Card>
      </Appear>
      <Sfx at={2} name="whoosh" /><Sfx at={tCheck} name="buzz" volume={0.5} /><Sfx at={tO} name="pop" />
    </AbsoluteFill>
  );
};

const S3 = ({ scene }) => {
  const W = useW(scene);
  const [tR, tF, tM, tOk] = [W('два', 4), W('формула', 60), W('сорок', 150), W('сходится', 260)];
  return (
    <AbsoluteFill>
      <Appear at={tR} y={150}><TeX tex={`\\mathrm{C : H : O} = 0{,}2 : 0{,}6 : 0{,}1 = ${A('2 : 6 : 1')}`} size={80} /></Appear>
      <Slam at={tF} y={360} size={150}><TeX tex="\mathrm{C_2H_6O}" size={190} /></Slam>
      <Appear at={tM} y={700}><TeX tex={`M = 24 + 6 + 16 = ${A('46')} = 23 \\cdot 2\\ \\checkmark`} size={70} /></Appear>
      <Sfx at={tR} name="pop" /><Sfx at={tF} name="boom" volume={0.6} /><Sfx at={tOk} name="ding" volume={0.55} />
    </AbsoluteFill>
  );
};

const Pivot = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tS = W('несколько', 40);
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={220} size={110} rotate={-4}>Сложная задача</Kinetic>
      <Kinetic at={tS} y={420} size={96} rotate={-3} plaque from="right">= несколько простых шагов</Kinetic>
      <Row y={680} style={{ gap: 40 }}>
        {[1, 2, 3, 4, 5].map((k) => {
          const at = tS + 8 + k * 4;
          const p = enter(frame, at, fps);
          return frame < at ? null : <div key={k} style={{ width: 120, height: 120, transform: `scale(${p}) rotate(-4deg)`, background: k === 5 ? C.accent : C.fg, color: k === 5 ? '#fff' : C.bg, display: 'grid', placeItems: 'center', font: `800 60px ${F.display}` }}>{k}</div>;
        })}
      </Row>
      <Sfx at={2} name="whoosh" /><Sfx at={tS} name="boom" volume={0.5} />{[1, 2, 3, 4, 5].map((k) => <Sfx key={k} at={tS + 8 + k * 4} name="tick" volume={0.45} />)}
    </AbsoluteFill>
  );
};

const Plan = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const blocks = ['Основа', 'Строение', 'Процессы', 'Неорганика', 'Органика', 'Пробники'];
  const t0 = W('ноября', 10);
  const fill = interpolate(frame, [t0, scene.dur - 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={110} rotate={-4}>Ноябрь → май</Kinetic>
      <Abs x={140} y={520} style={{ width: 1640 }}>
        <div style={{ height: 14, background: C.faint }}><div style={{ width: `${fill * 100}%`, height: '100%', background: C.accent }} /></div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 30 }}>
          {blocks.map((b, i) => {
            const on = fill >= i / (blocks.length - 1) - 0.001;
            return (
              <div key={b} style={{ textAlign: 'center', width: 250, opacity: on ? 1 : 0.35 }}>
                <div style={{ width: 34, height: 34, margin: '-62px auto 18px', background: on ? C.accent : C.faint, transform: 'rotate(45deg)' }} />
                <div style={{ font: `800 24px ${F.display}`, textTransform: 'uppercase', color: i === 5 && on ? C.accent : C.fg }}>{b}</div>
              </div>
            );
          })}
        </div>
      </Abs>
      <Appear at={W('пробники', 200)} y={760}><div style={{ font: `700 44px ${F.body}`, color: C.muted }}>все темы ЕНТ по химии + пробники в формате теста</div></Appear>
      <Sfx at={2} name="whoosh" /><Sfx at={t0} name="whoosh" volume={0.25} />
    </AbsoluteFill>
  );
};

// Ряд плашек, каждая выскакивает в свой момент.
const Chips = ({ items, y }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Row y={y} style={{ gap: 20 }}>
      {items.map(([c, at], i) => {
        const p = frame < at ? 0 : enter(frame, at, fps);
        return (
          <div key={c} style={{ opacity: p, transform: `translateY(${(1 - p) * 80}px)`, padding: '16px 30px', background: i === 1 ? C.accent : C.bg,
            border: `4px solid ${i === 1 ? C.accent : C.fg}`, font: `800 40px ${F.body}`, textTransform: 'uppercase', color: '#fff' }}>{c}</div>
        );
      })}
    </Row>
  );
};

const Format = ({ scene }) => {
  const W = useW(scene);
  const t = W('онлайн', 2);
  const tM = W('презентации', 120);
  const shots = [['slide-s01', 80, 210, -6], ['slide-s08', 560, 160, 4], ['slide-s16', 1000, 250, -3]];
  const chips = [['онлайн', t], ['группы по 5', W('пять', 30)], ['2 урока в неделю', W('два', 150)], ['ДЗ с проверкой', W('проверк', 260)]];
  return (
    <AbsoluteFill>
      {shots.map(([src, x, y, r], i) => (
        <Fly key={src} at={tM + i * 6} x={x} y={y} from={[i === 2 ? 400 : -400, 0]} rot={r}>
          <Img src={staticFile(`promo/${src}.png`)} style={{ width: 640, border: `6px solid ${C.fg}`, boxShadow: '0 30px 60px rgba(0,0,0,.5)' }} />
        </Fly>
      ))}
      {['memo-1', 'memo-2'].map((m, i) => (
        <Fly key={m} at={W('памятки', tM + 30) + i * 6} x={1480 + i * 130} y={120 + i * 60} from={[300, 0]} rot={i ? 6 : -4}>
          <Img src={staticFile(`promo/${m}.png`)} style={{ width: 300, border: `5px solid ${C.fg}` }} />
        </Fly>
      ))}
      <Chips items={chips} y={720} />
      {chips.map(([c, at]) => <Sfx key={c} at={at} name="pop" volume={0.35} />)}
      <Sfx at={tM} name="whoosh" />
    </AbsoluteFill>
  );
};

const Cta = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tS, tD, tSub] = [W('старт', 2), W('директ', 80), W('подпишись', 200)];
  return (
    <AbsoluteFill>
      <Kinetic at={tS} y={120} size={130} rotate={-4}>Старт</Kinetic>
      <Kinetic at={tS + 6} y={300} size={130} rotate={-3} plaque from="right" punchAt={tS + 10}>1 ноября</Kinetic>
      <Appear at={tD} y={560}><div style={{ font: `700 48px ${F.body}`, color: C.muted }}>Хочешь в группу — напиши в директ Instagram</div></Appear>
      <Kinetic at={tD + 6} y={640} size={110} rotate={-2}>@himbio.prosto</Kinetic>
      {frame >= tSub && (
        <Abs x={1380} y={860}>
          <div style={{ transform: `scale(${punch(frame, tSub, 0.25)})`, padding: '22px 44px', background: C.accent, borderRadius: 60, font: `800 40px ${F.display}`, color: '#fff', whiteSpace: 'nowrap' }}>ПОДПИСАТЬСЯ</div>
        </Abs>
      )}
      <Abs x={120} y={820}><Atom size={170} at={0} /></Abs>
      <Sfx at={tS} name="whoosh" /><Sfx at={tS + 10} name="boom" volume={0.55} /><Sfx at={tD + 6} name="whoosh" /><Sfx at={tSub} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

// Титул: о чём видео — в первые секунды.
const Title = ({ scene }) => (
  <TopicIntro scene={scene} tag="ЕНТ · химия" title="Химия на ЕНТ" plaque="не страшно"
    items={[['3 причины, почему теряют баллы', 'причины'], ['Разбор сложной задачи ЕНТ', 'разбор'], ['Как устроен курс «ХимБио просто»', 'курс']]} />
);

export const SCENES = { title: Title, hook: Hook, pain: Pain, r1: R1, r2: R2, r3: R3, method: Method, task: Task, s1: S1, s2: S2, s3: S3, pivot: Pivot, plan: Plan, format: Format, cta: Cta };
export const TAILS = { title: 24, hook: 14, task: 40, s3: 24, pivot: 16, format: 20, cta: 60 };
