// Y003 — «Генетика за 3 минуты»: законы Менделя и решётка Пеннета, моушн-урок 1920×1080 (биология, зелёный акцент).
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Atom, Card, Dna, Kinetic, Label, Option, Pea, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { A, Slam, TopicIntro, useW } from '../scenes.jsx';

const Abs = ({ x, y, children, style }) => <div style={{ position: 'absolute', left: x, top: y, ...style }}>{children}</div>;
const Big = ({ children, size = 72, color = C.fg, style }) => (
  <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: 1, color, whiteSpace: 'nowrap', ...style }}>{children}</div>
);
const Txt = ({ children, size = 44, color = C.fg, style }) => (
  <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: size, lineHeight: 1.2, color, ...style }}>{children}</div>
);
// Генотип с горошиной: [ген, цвет].
const G = ({ g, color, size = 110, at = 0, tex = 70 }) => (
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
    <Pea color={color} size={size} at={at} />
    <TeX tex={`\\mathrm{${g}}`} size={tex} />
  </div>
);
const Show = ({ at, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps);
  return <div style={{ opacity: Math.min(1, p * 2), transform: `translateY(${(1 - p) * 40}px)` }}>{children}</div>;
};

// ── Вступление ─────────────────────────────────────────────

const Title = ({ scene }) => (
  <TopicIntro scene={scene} tag="ЕНТ · биология" title="Генетика" plaque="за 3 минуты" icon="dna"
    items={[['Гены и аллели', 'гены'], ['Доминантный и рецессивный', 'доминантные'], ['Законы Менделя', 'законы'], ['Решётка Пеннета', 'решётку'], ['Задача ЕНТ — реши сам', 'задача']]} />
);

const Hook = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tP, tG, tF1, tQ, tF2] = [W('жёлтый', 32), W('зелёным', 51), W('потомки', 83), W('куда', 155), W('следующем', 233)];
  const rows = [['P', 230, tP], ['F₁', 480, tF1], ['F₂', 730, tF2]];
  return (
    <AbsoluteFill>
      {rows.map(([l, y, at]) => frame >= at && <Abs key={l} x={260} y={y + 20}><Big size={90} color={C.accent}>{l}</Big></Abs>)}
      <Abs x={520} y={230}><div style={{ display: 'flex', alignItems: 'center', gap: 40 }}><Pea color="yellow" size={150} at={tP} /><Big size={90}>{frame >= tG ? '×' : ''}</Big><Pea color="green" size={150} at={tG} /></div></Abs>
      <Abs x={520} y={480}><div style={{ display: 'flex', gap: 30 }}>{[0, 1, 2, 3].map((i) => <Pea key={i} color="yellow" size={150} at={tF1 + i * 4} />)}</div></Abs>
      {frame >= tQ && frame < tF2 && <Abs x={1300} y={470}><Big size={160} color={C.accent} style={{ transform: `rotate(${Math.sin((frame - tQ) / 5) * 8}deg)` }}>?</Big></Abs>}
      <Abs x={520} y={730}><div style={{ display: 'flex', gap: 30 }}>{['yellow', 'yellow', 'yellow', 'green'].map((c, i) => <Pea key={i} color={c} size={150} at={tF2 + i * 4} />)}</div></Abs>
      <Sfx at={tP} name="pop" /><Sfx at={tG} name="pop" />{[0, 1, 2, 3].map((i) => <Sfx key={i} at={tF1 + i * 4} name="tick" volume={0.35} />)}
      <Sfx at={tQ} name="whoosh" /><Sfx at={tF2} name="boom" volume={0.5} />
    </AbsoluteFill>
  );
};

// Пара гомологичных хромосом с локусом A / a.
const Homologs = ({ at }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps);
  const bar = (x, label, hot) => (
    <g key={x}>
      <rect x={x} y="20" width="90" height="460" rx="45" fill={C.card} stroke={C.fg} strokeWidth="8" />
      <rect x={x} y="210" width="90" height="56" fill={hot ? C.accent : C.muted} />
      <text x={x + 45} y="252" textAnchor="middle" fontFamily={F.display} fontWeight="800" fontSize="44" fill={C.fg}>{label}</text>
    </g>
  );
  return <svg width="340" height="500" viewBox="0 0 340 500" style={{ transform: `scale(${p})` }}>{bar(40, 'A', true)}{bar(210, 'a', false)}</svg>;
};

const Gene = ({ scene }) => {
  const W = useW(scene);
  const [tGen, tAl, tD, tR] = [W('ген', 37), W('аллели', 119), W('доминантный', 197), W('рецессивный', 257)];
  return (
    <AbsoluteFill>
      <Kinetic at={tGen} y={150} size={84} rotate={-3}>Ген и аллели</Kinetic>
      <Abs x={260} y={320}><Homologs at={tAl - 10} /></Abs>
      <Abs x={760} y={420}>
        <div style={{ display: 'grid', gap: 40 }}>
          <Show at={tD}><div style={{ display: 'flex', alignItems: 'center', gap: 28 }}><TeX tex={A('\\mathrm{A}')} size={120} /><Txt>доминантный аллель</Txt></div></Show>
          <Show at={tR}><div style={{ display: 'flex', alignItems: 'center', gap: 28 }}><TeX tex="\mathrm{a}" size={120} /><Txt>рецессивный аллель</Txt></div></Show>
        </div>
      </Abs>
      <Sfx at={tGen} name="whoosh" /><Sfx at={tAl - 10} name="pop" /><Sfx at={tD} name="pop" volume={0.3} /><Sfx at={tR} name="pop" volume={0.3} />
    </AbsoluteFill>
  );
};

const Genotype = ({ scene }) => {
  const W = useW(scene);
  const [tG, t1, t2, t3, tF] = [W('генотип', 38), W('две', 56), W('большая', 91), W('маленькие', 140), W('фенотип', 245)];
  const cols = [['AA', 'yellow', t1], ['Aa', 'yellow', t2], ['aa', 'green', t3]];
  return (
    <AbsoluteFill>
      <Kinetic at={tG} y={150} size={84} rotate={-3} plaque>Генотип</Kinetic>
      <Row y={340} style={{ gap: 170 }}>
        {cols.map(([g, c, at]) => (
          <Show key={g} at={at}>
            <div style={{ textAlign: 'center' }}>
              <TeX tex={`\\mathrm{${g}}`} size={130} />
              <div style={{ marginTop: 20, minHeight: 170 }}><Pea color={c} size={170} at={tF} /></div>
            </div>
          </Show>
        ))}
      </Row>
      <Appear at={tF} y={790}><Label size={40} color={C.fg}>внешний вид признака — фенотип</Label></Appear>
      {cols.map(([g, , at]) => <Sfx key={g} at={at} name="pop" volume={0.35} />)}<Sfx at={tF} name="ding" volume={0.4} />
    </AbsoluteFill>
  );
};

const Dominance = ({ scene }) => {
  const W = useW(scene);
  const [tH, tR] = [W('поэтому', 98), W('рецессивный', 195, 1)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={84} rotate={-3}>Доминирование</Kinetic>
      <Row y={360} style={{ gap: 120 }}>
        <Show at={tH}><div style={{ display: 'flex', alignItems: 'center', gap: 30 }}><G g="Aa" color="yellow" size={190} at={tH} tex={90} /><Txt size={52}>гетерозигота — жёлтая</Txt></div></Show>
      </Row>
      <Row y={720}>
        <Show at={tR}><div style={{ display: 'flex', alignItems: 'center', gap: 24 }}><Pea color="green" size={110} at={tR} /><Txt size={46}>зелёный — только <span style={{ color: C.accent }}>aa</span></Txt></div></Show>
      </Row>
      <Sfx at={2} name="whoosh" /><Sfx at={tH} name="pop" /><Sfx at={tR} name="pop" />
    </AbsoluteFill>
  );
};

const Notation = ({ scene }) => {
  const W = useW(scene);
  const items = [['P', 'родители', W('пэ', 53)], ['G', 'гаметы', W('гэ', 91)], ['F₁', 'первое поколение', W('эф', 130)]];
  const tOne = W('каждая', 218);
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={84} rotate={-3}>Как записываем</Kinetic>
      <Row y={360} style={{ gap: 50 }}>
        {items.map(([s, t, at]) => (
          <Show key={s} at={at}>
            <div style={{ width: 460, padding: '34px 30px', background: C.card, border: `4px solid ${C.fg}`, textAlign: 'center' }}>
              <Big size={110} color={C.accent}>{s}</Big>
              <Txt size={40} style={{ marginTop: 16 }}>{t}</Txt>
            </div>
          </Show>
        ))}
      </Row>
      <Appear at={tOne} y={760}><Txt size={46}>каждая гамета несёт <span style={{ color: C.accent }}>один</span> аллель</Txt></Appear>
      <Sfx at={2} name="whoosh" />{items.map(([s, , at]) => <Sfx key={s} at={at} name="pop" volume={0.35} />)}<Sfx at={tOne} name="tick" volume={0.5} />
    </AbsoluteFill>
  );
};

// Схема скрещивания: строки P / G / F.
const Cross = ({ rows }) => (
  <div style={{ display: 'grid', gap: 26 }}>
    {rows.map(([label, content, at]) => (
      <Show key={label} at={at}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 40 }}>
          <Big size={64} color={C.accent} style={{ width: 120 }}>{label}</Big>
          {content}
        </div>
      </Show>
    ))}
  </div>
);
const Times = () => <Big size={64}>×</Big>;

const Law1 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tP, tG, tF] = [W('доминантная', 98), W('даёт', 157), W('все', 199)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={140} size={80} rotate={-3} plaque>I закон · единообразие</Kinetic>
      <Abs x={260} y={320}>
        <Cross rows={[
          ['P', <><G g="AA" color="yellow" at={tP} /><Times /><G g="aa" color="green" at={tP + 6} /></>, tP],
          ['G', <TeX tex={`\\mathrm{A} \\qquad\\qquad \\mathrm{a}`} size={70} />, tG],
          ['F₁', <><G g="Aa" color="yellow" at={tF} /><Big size={64} color={C.accent} style={{ transform: `scale(${punch(frame, tF + 10, 0.2)})` }}>100% жёлтые</Big></>, tF],
        ]} />
      </Abs>
      <Sfx at={2} name="whoosh" /><Sfx at={tP} name="pop" /><Sfx at={tG} name="tick" volume={0.5} /><Sfx at={tF} name="ding" volume={0.45} />
    </AbsoluteFill>
  );
};

const Law2 = ({ scene }) => {
  const W = useW(scene);
  const [tP, tBack, t3] = [W('скрещиваем', 82), W('зелёный', 141), W('три', 183)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={140} size={80} rotate={-3} plaque>II закон · расщепление</Kinetic>
      <Abs x={260} y={330}>
        <Cross rows={[['F₁', <><G g="Aa" color="yellow" at={tP} /><Times /><G g="Aa" color="yellow" at={tP + 6} /></>, tP]]} />
      </Abs>
      <Abs x={1000} y={330}><div style={{ display: 'flex', gap: 24 }}>{['yellow', 'yellow', 'yellow', 'green'].map((c, i) => <Pea key={i} color={c} size={140} at={(i === 3 ? tBack : t3) + i * 3} />)}</div></Abs>
      <Slam at={t3} y={660} size={120}>3 : 1</Slam>
      <Sfx at={2} name="whoosh" /><Sfx at={tP} name="pop" /><Sfx at={tBack} name="pop" /><Sfx at={t3} name="boom" volume={0.5} />
    </AbsoluteFill>
  );
};

// Решётка Пеннета 3×3 для Aa × Aa.
const CELL = 200;
const Grid = ({ tGam, tCells, kids, x, y }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const head = (t, at) => frame >= at && <div style={{ transform: `scale(${enter(frame, at, fps)})`, fontFamily: F.display, fontWeight: 800, fontSize: 80, color: t === 'A' ? C.fg : C.accent }}>{t}</div>;
  const box = (i, j, child) => (
    <div key={`${i}${j}`} style={{ position: 'absolute', left: j * CELL, top: i * CELL, width: CELL, height: CELL, border: `4px solid ${i && j ? C.fg : 'transparent'}`, background: i && j ? C.card : 'transparent', display: 'grid', placeItems: 'center', boxSizing: 'border-box' }}>{child}</div>
  );
  return (
    <div style={{ position: 'absolute', left: x, top: y, width: 3 * CELL, height: 3 * CELL }}>
      {box(0, 1, head('A', tGam))}{box(0, 2, head('a', tGam + 4))}{box(1, 0, head('A', tGam + 8))}{box(2, 0, head('a', tGam + 12))}
      {kids.map(([g, c], k) => box(1 + Math.floor(k / 2), 1 + (k % 2), frame >= tCells + k * 7 && (
        <div style={{ textAlign: 'center' }}><Pea color={c} size={96} at={tCells + k * 7} /><div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 44, color: C.fg }}>{g}</div></div>
      )))}
    </div>
  );
};
const KIDS = [['AA', 'yellow'], ['Aa', 'yellow'], ['Aa', 'yellow'], ['aa', 'green']];

const Punnett = ({ scene }) => {
  const W = useW(scene);
  const [tGam, tCells, tRatio] = [W('гаметы', 42), W('клетках', 175), W('один', 235)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={140} size={80} rotate={-3}>Решётка Пеннета</Kinetic>
      <Grid tGam={tGam} tCells={tCells} kids={KIDS} x={260} y={260} />
      <Abs x={1000} y={380}>
        <Show at={tRatio}>
          <Label size={36} color={C.accent}>генотипы потомков</Label>
          <TeX tex="\mathrm{AA : Aa : aa}" size={72} />
          <TeX tex={`= ${A('1 : 2 : 1')}`} size={90} />
        </Show>
      </Abs>
      <Sfx at={2} name="whoosh" />{[0, 4, 8, 12].map((d) => <Sfx key={d} at={tGam + d} name="tick" volume={0.4} />)}
      {KIDS.map((_, k) => <Sfx key={k} at={tCells + k * 7} name="pop" volume={0.3} />)}<Sfx at={tRatio} name="ding" volume={0.45} />
    </AbsoluteFill>
  );
};

const Trap = ({ title, hitAt, children }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, hitAt, 14, 18)}px)` }}>
      <Kinetic at={2} y={140} size={100} rotate={-4} color={C.bg} punchAt={hitAt}>{title}</Kinetic>
      {children}
      <Sfx at={2} name="whoosh" /><Sfx at={hitAt} name="buzz" volume={0.5} />
    </AbsoluteFill>
  );
};

const Trap1 = ({ scene }) => {
  const W = useW(scene);
  const [tPh, tGe, tRead] = [W('фенотипы', 56), W('генотипы', 121), W('читай', 165)];
  const panel = (title, tex, at) => (
    <Show at={at}>
      <div style={{ width: 640, padding: '34px 40px', background: C.bg, textAlign: 'center' }}>
        <Label size={38} color={C.fg}>{title}</Label>
        <div style={{ marginTop: 12 }}><TeX tex={tex} size={110} /></div>
      </div>
    </Show>
  );
  return (
    <Trap title="Ловушка" hitAt={tPh}>
      <Row y={380} style={{ gap: 60 }}>
        {panel('фенотипы', '3 : 1', tPh)}
        {panel('генотипы', '1 : 2 : 1', tGe)}
      </Row>
      <Appear at={tRead} y={760}><Txt size={50} color={C.bg}>Читай, что спрашивают!</Txt></Appear>
    </Trap>
  );
};

const TestCross = ({ scene }) => {
  const W = useW(scene);
  const [tQ, tA, tAll, tHalf] = [W('узнать', 10), W('анализирующее', 144), W('все', 216), W('половина', 327)];
  return (
    <AbsoluteFill>
      <Kinetic at={tA} y={140} size={72} rotate={-3} plaque>Анализирующее скрещивание</Kinetic>
      <Abs x={200} y={360}>
        <Show at={tQ}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 30 }}>
            <div style={{ textAlign: 'center' }}><Pea color="yellow" size={150} at={tQ} /><TeX tex="\mathrm{A?}" size={70} /></div>
            <Times />
            <G g="aa" color="green" size={150} at={tQ + 40} />
          </div>
        </Show>
      </Abs>
      <Abs x={940} y={320}>
        <div style={{ display: 'grid', gap: 50 }}>
          <Show at={tAll}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
              {[0, 1, 2, 3].map((i) => <Pea key={i} color="yellow" size={80} at={tAll + i * 3} />)}
              <Txt size={46}>→ <span style={{ color: C.accent }}>AA</span></Txt>
            </div>
          </Show>
          <Show at={tHalf}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
              {['yellow', 'yellow', 'green', 'green'].map((c, i) => <Pea key={i} color={c} size={80} at={tHalf + i * 3} />)}
              <Txt size={46}>→ <span style={{ color: C.accent }}>Aa</span></Txt>
            </div>
          </Show>
        </div>
      </Abs>
      <Sfx at={tQ} name="pop" /><Sfx at={tA} name="whoosh" /><Sfx at={tAll} name="ding" volume={0.4} /><Sfx at={tHalf} name="ding" volume={0.4} />
    </AbsoluteFill>
  );
};

const Trap2 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tAll, tY] = [W('всех', 153), W('жёлтых', 240)];
  const dimGreen = frame >= tY;
  return (
    <Trap title="Ловушка: от чего считать" hitAt={tY}>
      <Row y={330} style={{ gap: 40 }}>
        {KIDS.map(([g, c], i) => (
          <div key={i} style={{ textAlign: 'center', opacity: dimGreen && c === 'green' ? 0.25 : 1, padding: 12, background: C.bg }}>
            <Pea color={c} size={120} at={4 + i * 4} />
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 44, color: g === 'Aa' ? C.accent : C.fg }}>{g}</div>
          </div>
        ))}
      </Row>
      <Row y={640} style={{ gap: 60 }}>
        <Show at={tAll}><div style={{ padding: '20px 34px', background: C.bg }}><TeX tex="\mathrm{Aa}\ \text{среди всех:}\ \tfrac{2}{4} = \tfrac{1}{2}" size={58} /></div></Show>
        <Show at={tY}><div style={{ padding: '20px 34px', background: C.bg, transform: `scale(${punch(frame, tY + 6, 0.12)})` }}><TeX tex={`\\mathrm{Aa}\\ \\text{среди жёлтых:}\\ ${A('\\tfrac{2}{3}')}`} size={58} /></div></Show>
      </Row>
    </Trap>
  );
};

// ── Задача ЕНТ ─────────────────────────────────────────────

const OPTS = [['А', '0\\%'], ['Б', '25\\%'], ['В', '50\\%'], ['Г', '75\\%']];

const Task = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tQ, tP] = [W('гетерозиготный', 90), W('паузу', 302)];
  const left = interpolate(frame, [tP, scene.dur - 4], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const R = 34;
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={140} size={84} rotate={-3} plaque>Задача ЕНТ</Kinetic>
      <Appear at={tQ} y={320}>
        <Card width={1600}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Label>ЕНТ · выбери один ответ</Label>
            <svg width={2 * R + 12} height={2 * R + 12} viewBox={`${-R - 6} ${-R - 6} ${2 * R + 12} ${2 * R + 12}`}>
              <circle r={R} fill="none" stroke={C.faint} strokeWidth="8" />
              <circle r={R} fill="none" stroke={C.accent} strokeWidth="8" strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - left)} transform="rotate(-90)" />
            </svg>
          </div>
          <div style={{ marginTop: 20 }}><TeX tex="\text{Гетерозиготный жёлтый горох скрестили с зелёным.}" size={54} /></div>
          <div style={{ marginTop: 8 }}><TeX tex="\text{Какая доля потомков будет зелёной?}" size={54} /></div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 22, marginTop: 30 }}>
            {OPTS.map(([l, v], i) => <Option key={l} letter={l} value={v} unit="" at={tQ + 20 + i * 4} />)}
          </div>
        </Card>
      </Appear>
      {frame >= tP && <Abs x={1640} y={140}><Big size={110} color={C.accent} style={{ opacity: 0.6 + 0.4 * Math.sin((frame - tP) / 5) }}>❚❚</Big></Abs>}
      <Sfx at={2} name="whoosh" />{OPTS.map(([l], i) => <Sfx key={l} at={tQ + 20 + i * 4} name="tick" volume={0.5} />)}
      {[0, 1, 2, 3].map((k) => <Sfx key={k} at={tP + 20 + k * 30} name="tick" volume={0.35} />)}
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tG, tF, tHalf, tAns] = [W('гетерозигота', 46), W('получаем', 177), W('половина', 320), W('ответ', 362)];
  const states = frame >= tAns ? { А: 'dim', Б: 'dim', В: 'right', Г: 'dim' } : {};
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={140} size={84} rotate={-3}>Проверяем</Kinetic>
      <Abs x={260} y={240}>
        <Cross rows={[
          ['P', <><G g="Aa" color="yellow" size={76} at={tG} tex={54} /><Times /><G g="aa" color="green" size={76} at={tG + 6} tex={54} /></>, tG],
          ['G', <TeX tex={`\\mathrm{A},\\ \\mathrm{a} \\qquad\\quad \\mathrm{a}`} size={56} />, tG + 40],
          ['F', <><G g="Aa" color="yellow" size={76} at={tF} tex={54} /><G g="aa" color="green" size={76} at={tF + 8} tex={54} /><TeX tex={frame >= tHalf ? `= 1 : 1 \\Rightarrow ${A('50\\%')}` : '= 1 : 1'} size={64} /></>, tF],
        ]} />
      </Abs>
      {frame >= tAns && (
        <Row y={770} style={{ gap: 22 }}>
          {OPTS.map(([l, v]) => <div key={l} style={{ width: 300 }}><Option letter={l} value={v} unit="" state={states[l]} at={tAns} /></div>)}
        </Row>
      )}
      <Sfx at={2} name="whoosh" /><Sfx at={tG} name="pop" /><Sfx at={tF} name="pop" /><Sfx at={tHalf} name="pop" /><Sfx at={tAns} name="ding" volume={0.55} />
    </AbsoluteFill>
  );
};

// ── Курс и подписка ────────────────────────────────────────

const Chip = ({ children, red, at }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  return <div style={{ transform: `scale(${enter(frame, at, fps)})`, padding: '14px 28px', background: red ? C.accent : C.bg, border: `4px solid ${red ? C.accent : C.fg}`, fontFamily: F.body, fontWeight: 800, fontSize: 40, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>{children}</div>;
};

const Cta = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tC, tH, tOn, tG, tS, tD, tSub] = [W('химбио', 80), W('химия', 112), W('онлайн', 149), W('группы', 171), W('старт', 208), W('директ', 302), W('подпишись', 401)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={70} rotate={-3}>Так разбираем каждую тему</Kinetic>
      <Appear at={tC} y={300}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
          <Atom size={140} at={tC} speed={1.3} /><Dna size={160} at={tC} />
          <div>
            <div style={{ font: `800 84px ${F.display}`, color: C.fg, lineHeight: 1 }}>ХИМБИО ПРОСТО</div>
            <div style={{ font: `700 42px ${F.body}`, color: C.muted, marginTop: 8 }}>курс подготовки к ЕНТ</div>
          </div>
        </div>
      </Appear>
      <Row y={510} style={{ gap: 18 }}>
        <Chip at={tH} red>химия + биология</Chip><Chip at={tOn}>онлайн</Chip><Chip at={tG}>группы по 5</Chip><Chip at={tS} red>старт 1 ноября</Chip>
      </Row>
      <Appear at={tD - 20} y={650}><div style={{ font: `700 44px ${F.body}`, color: C.muted }}>Запись — в директ Instagram</div></Appear>
      <Kinetic at={tD} y={720} size={96} rotate={-2}>@himbio.prosto</Kinetic>
      {frame >= tSub && (
        <Abs x={1390} y={850}>
          <div style={{ transform: `scale(${punch(frame, tSub, 0.25)}) rotate(4deg)`, padding: '22px 44px', background: C.accent, borderRadius: 60, font: `800 40px ${F.display}`, color: '#fff', whiteSpace: 'nowrap' }}>ПОДПИСАТЬСЯ</div>
        </Abs>
      )}
      <Sfx at={2} name="whoosh" /><Sfx at={tC} name="whoosh" />{[tH, tOn, tG, tS].map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
      <Sfx at={tD} name="whoosh" /><Sfx at={tSub} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

export const SCENES = {
  title: Title, hook: Hook, gene: Gene, genotype: Genotype, dominance: Dominance, notation: Notation, law1: Law1, law2: Law2,
  punnett: Punnett, trap1: Trap1, testcross: TestCross, trap2: Trap2, task: Task, answer: Answer, cta: Cta,
};
export const TAILS = { title: 24, hook: 20, genotype: 16, law1: 20, law2: 20, punnett: 24, trap1: 24, testcross: 24, trap2: 30, task: 150, answer: 36, cta: 60 };
