// Y001 — «Моль для ЕНТ», моушн-урок для YouTube, 1920×1080. Сценарий с озвучкой — y001.script.json.
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Atom, Card, Kinetic, Label, Option, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { A, Slam, TopicIntro, useW } from '../scenes.jsx';

const Abs = ({ x, y, children, style }) => <div style={{ position: 'absolute', left: x, top: y, ...style }}>{children}</div>;

// Влёт элемента снизу/сбоку, с поворотом.
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

// Значение появляется в момент at, до этого — «?».
const Q = (frame, at, s) => (frame >= at ? A(s) : '\\;?');

const Chip = ({ children, red = false, size = 40 }) => (
  <div style={{ padding: '14px 28px', background: red ? C.accent : C.bg, border: `4px solid ${red ? C.accent : C.fg}`, font: `800 ${size}px ${F.body}`, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>{children}</div>
);

// Молекула воды: O в центре, два H под углом 104,5°.
const Water = ({ size = 400, at = 0, hotH }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 12, stiffness: 120 });
  const t = (frame - at) / fps;
  const hot = hotH != null && frame >= hotH;
  const hs = hot ? punch(frame, hotH, 0.35, 12) : 1;
  const H = [[-118, 92], [118, 92]];
  return (
    <svg width={size} height={size} viewBox="-200 -200 400 400" style={{ transform: `scale(${p}) rotate(${Math.sin(t * 1.6) * 5}deg)` }}>
      {H.map(([x, y]) => <line key={x} x1="0" y1="-30" x2={x} y2={y - 30} stroke={C.fg} strokeWidth="16" />)}
      <circle cx="0" cy="-30" r="100" fill={C.fg} />
      <text x="0" y="-2" textAnchor="middle" fontFamily={F.display} fontWeight="800" fontSize="90" fill={C.bg}>O</text>
      {H.map(([x, y]) => (
        <g key={x} transform={`translate(${x} ${y - 30}) scale(${hs})`}>
          <circle r="62" fill={hot ? C.accent : C.card} stroke={C.fg} strokeWidth="8" />
          <text y="22" textAnchor="middle" fontFamily={F.display} fontWeight="800" fontSize="60" fill={C.fg}>H</text>
        </g>
      ))}
    </svg>
  );
};

// Сосуд с газом: молекулы мечутся внутри.
const GasBox = ({ at, x, y, tex, vAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 14, stiffness: 140 });
  const t = (frame - at) / fps;
  return (
    <Abs x={x} y={y + (1 - p) * 200} style={{ opacity: Math.min(1, p * 2), width: 420 }}>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 14 }}><TeX tex={tex} size={64} /></div>
      <div style={{ position: 'relative', height: 250, border: `5px solid ${C.fg}`, background: C.card, overflow: 'hidden' }}>
        {Array.from({ length: 12 }, (_, i) => (
          <div key={i} style={{ position: 'absolute', width: 22, height: 22, borderRadius: '50%', background: i % 3 ? C.fg : C.accent,
            left: 195 + 170 * Math.sin(t * (1.3 + (i % 4) * 0.4) + i * 1.7), top: 115 + 95 * Math.cos(t * (1.1 + (i % 3) * 0.5) + i * 2.3) }} />
        ))}
        {vAt != null && frame >= vAt && (
          <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, padding: '10px 0 14px', background: C.accent, textAlign: 'center', font: `800 52px ${F.display}`, color: C.fg, transform: `scale(${punch(frame, vAt, 0.2)})` }}>22,4 л</div>
        )}
      </div>
    </Abs>
  );
};

// ── Вступление ─────────────────────────────────────────────

const Hook = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [t1, tL, tN, tM, tQ] = [W('восемнадцать', 2), W('ложки', 80), W('шестьсот', 140), W('молекул', 175), W('как', 215)];
  const groups = ['602', '000', '000', '000', '000', '000', '000', '000'];
  return (
    <AbsoluteFill style={{ transform: `translateX(${shake(frame, tQ, 12, 16)}px)` }}>
      <Kinetic at={t1} y={170} size={150} rotate={-4}>18 г воды</Kinetic>
      <Appear at={tL} y={370}><div style={{ font: `700 46px ${F.body}`, color: C.muted }}>≈ столовая ложка</div></Appear>
      <Row y={480} style={{ gap: 22 }}>
        {groups.map((g, i) => {
          const at = tN + i * 3;
          const p = enter(frame, at, fps, { damping: 12, stiffness: 200 });
          return frame < at ? null : (
            <div key={i} style={{ font: `800 64px ${F.display}`, color: i ? C.fg : C.accent, opacity: Math.min(1, p * 2), transform: `translateY(${(1 - p) * -90}px)` }}>{g}</div>
          );
        })}
      </Row>
      <Appear at={tM} y={580}><Label size={40}>молекул</Label></Appear>
      <Slam at={tQ} y={700} size={96}>Как их сосчитать?</Slam>
      <Sfx at={t1} name="whoosh" />{groups.map((_, i) => <Sfx key={i} at={tN + i * 3} name="tick" volume={0.4} />)}<Sfx at={tQ} name="boom" volume={0.6} />
    </AbsoluteFill>
  );
};

const Intro = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tMol, tEnt, tSteps, tTask] = [W('моль', 26), W('ент', 150), W('шагам', 215), W('задача', 255)];
  const steps = ['моль', 'M', 'n = m/M', 'N', 'V газа'];
  return (
    <AbsoluteFill>
      <Slam at={tMol} y={170} size={200}>Моль</Slam>
      <Kinetic at={tEnt} y={470} size={72} rotate={-3} from="right">почти в каждой задаче ЕНТ</Kinetic>
      <Row y={680} style={{ gap: 18 }}>
        {[...steps, 'задача ЕНТ'].map((s, i) => {
          const at = i < steps.length ? tSteps + i * 4 : tTask;
          const p = enter(frame, at, fps);
          return frame < at ? null : (
            <div key={s} style={{ transform: `scale(${p}) rotate(-3deg)`, padding: '14px 26px', background: i === steps.length ? C.accent : C.fg,
              color: i === steps.length ? C.fg : C.bg, font: `800 38px ${F.display}`, whiteSpace: 'nowrap' }}>{s}</div>
          );
        })}
      </Row>
      <Sfx at={tMol} name="boom" volume={0.55} /><Sfx at={tEnt} name="whoosh" />
      {steps.map((_, i) => <Sfx key={i} at={tSteps + i * 4} name="pop" volume={0.3} />)}<Sfx at={tTask} name="ding" volume={0.45} />
    </AbsoluteFill>
  );
};

// ── Что такое моль ─────────────────────────────────────────

const Pack = ({ scene }) => {
  const W = useW(scene);
  const [tE, tP, tM] = [W('яйца', 60), W('бумагу', 105), W('моль', 305)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={160} size={84} rotate={-3}>Считаем пачками</Kinetic>
      <Fly at={tE} x={150} y={360} from={[-300, 0]}>
        <div style={{ width: 460, display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 14, padding: 26, border: `4px solid ${C.fg}`, background: C.card, boxSizing: 'border-box' }}>
          {Array.from({ length: 10 }, (_, i) => <div key={i} style={{ height: 92, borderRadius: '50% 50% 46% 46% / 60% 60% 40% 40%', background: C.fg }} />)}
        </div>
        <div style={{ marginTop: 26, font: `800 48px ${F.display}`, color: C.fg }}>десяток = 10</div>
      </Fly>
      <Fly at={tP} x={740} y={360} from={[0, 300]}>
        <div style={{ position: 'relative', width: 420, height: 246 }}>
          {Array.from({ length: 7 }, (_, i) => (
            <div key={i} style={{ position: 'absolute', left: 10 + i * 4, top: 200 - i * 30, width: 380, height: 40, background: i % 2 ? C.card : C.fg, border: `3px solid ${C.fg}`, transform: `rotate(${(i % 3) - 1}deg)` }} />
          ))}
        </div>
        <div style={{ marginTop: 26, font: `800 48px ${F.display}`, color: C.fg }}>пачка = 500</div>
      </Fly>
      <Fly at={tM} x={1300} y={340} from={[300, 0]} rot={-4}>
        <div style={{ width: 470, height: 270, background: C.accent, display: 'grid', placeItems: 'center', font: `800 110px ${F.display}`, color: C.fg }}>МОЛЬ</div>
        <div style={{ marginTop: 26, font: `800 48px ${F.display}`, color: C.accent }}>= ?</div>
      </Fly>
      <Sfx at={2} name="whoosh" /><Sfx at={tE} name="pop" /><Sfx at={tP} name="pop" /><Sfx at={tM} name="boom" volume={0.55} />
    </AbsoluteFill>
  );
};

const Avogadro = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tN, tDeg, tName] = [W('шесть', 36), W('двадцать', 90), W('авогадро', 210)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={170} size={110} rotate={-4}>1 моль</Kinetic>
      <Appear at={tN} y={390}>
        <div style={{ transform: `scale(${punch(frame, tDeg, 0.18)})` }}>
          <TeX tex={`N_A = ${frame >= tDeg ? A('6{,}02 \\cdot 10^{23}') : '6{,}02 \\cdot 10^{\\;?}'}\\ \\text{моль}^{-1}`} size={120} />
        </div>
      </Appear>
      <Appear at={W('частиц', 120)} y={600}><div style={{ font: `700 44px ${F.body}`, color: C.muted }}>= 602 000 000 000 000 000 000 000 частиц</div></Appear>
      <Kinetic at={tName} y={720} size={70} rotate={-3} plaque>постоянная Авогадро</Kinetic>
      <Sfx at={2} name="whoosh" /><Sfx at={tDeg} name="pop" /><Sfx at={tName} name="ding" volume={0.45} />
    </AbsoluteFill>
  );
};

// Пачка частиц: квадрат с точками.
const Box = ({ at, label }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps);
  return (
    <div style={{ transform: `scale(${p})`, textAlign: 'center' }}>
      <div style={{ width: 190, height: 190, border: `4px solid ${C.fg}`, background: C.card, display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', placeItems: 'center', padding: 14, boxSizing: 'border-box' }}>
        {Array.from({ length: 25 }, (_, i) => <div key={i} style={{ width: 18, height: 18, borderRadius: '50%', background: i % 4 ? C.fg : C.accent }} />)}
      </div>
      {label && <div style={{ marginTop: 12, font: `800 32px ${F.display}`, color: C.muted }}>{label}</div>}
    </div>
  );
};

const Amount = ({ scene }) => {
  const W = useW(scene);
  const [tK, tN, tU, tTwo] = [W('количество', 66), W('буква', 128), W('моль', 190), W('два', 225)];
  return (
    <AbsoluteFill>
      <Kinetic at={tK} y={160} size={92} rotate={-3}>Количество вещества</Kinetic>
      <Fly at={tN} x={220} y={300} from={[-300, 0]}><TeX tex={A('n')} size={300} /></Fly>
      <Fly at={tU} x={180} y={720} from={[-200, 0]}><Chip>единица — моль</Chip></Fly>
      <Fly at={tTwo} x={820} y={330} from={[300, 0]}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
          <Box at={tTwo} label="1 моль" />
          <div style={{ font: `800 80px ${F.display}`, color: C.accent }}>→</div>
          <Box at={tTwo + 8} label="2 моль" />
          <Box at={tTwo + 12} />
        </div>
        <div style={{ marginTop: 34, font: `700 44px ${F.body}`, color: C.muted }}>2 моль — частиц вдвое больше</div>
      </Fly>
      <Sfx at={tK} name="whoosh" /><Sfx at={tN} name="pop" /><Sfx at={tTwo} name="whoosh" /><Sfx at={tTwo + 8} name="pop" volume={0.3} /><Sfx at={tTwo + 12} name="pop" volume={0.3} />
    </AbsoluteFill>
  );
};

// ── Молярная масса ─────────────────────────────────────────

const Weigh = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tQ = W('сколько', 120);
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={220} size={100} rotate={-4}>В задачах — граммы</Kinetic>
      <Slam at={tQ} y={480} size={110}>Сколько весит 1 моль?</Slam>
      <Abs x={1540} y={720}><div style={{ font: `800 160px ${F.display}`, color: C.accent, transform: `rotate(${frame >= tQ ? Math.sin((frame - tQ) / 4) * 8 : 0}deg)` }}>?</div></Abs>
      <Sfx at={2} name="whoosh" /><Sfx at={tQ} name="boom" volume={0.55} />
    </AbsoluteFill>
  );
};

const Molar = ({ scene }) => {
  const W = useW(scene);
  const [tT, tM, tU, tS] = [W('молярная', 50), W('эм', 104), W('граммах', 120), W('складываем', 205)];
  return (
    <AbsoluteFill>
      <Kinetic at={tT} y={160} size={90} rotate={-3} plaque>Молярная масса</Kinetic>
      <Fly at={tM} x={300} y={340} from={[-300, 0]}><TeX tex={A('M')} size={280} /></Fly>
      <Fly at={tU} x={700} y={420} from={[300, 0]}><Chip size={56}>г/моль</Chip></Fly>
      <Appear at={tS} y={700}>
        <Card width={1500}><div style={{ font: `800 50px ${F.body}`, color: C.fg }}>Складываем атомные массы <span style={{ color: C.accent }}>с учётом индексов</span></div></Card>
      </Appear>
      <Sfx at={tT} name="whoosh" /><Sfx at={tM} name="pop" /><Sfx at={tU} name="pop" volume={0.3} /><Sfx at={tS} name="whoosh" volume={0.3} />
    </AbsoluteFill>
  );
};

const H2SO4 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tH, tS, tO, tSum] = [W('получаем', 130), W('тридцать', 200), W('шестьдесят', 325), W('девяносто', 405)];
  const hot = (at) => frame >= at && frame < at + 60;
  const sub = (d, at) => (hot(at) ? A(d) : d);
  const parts = [['H', '2 \\cdot 1 = 2', tH], ['S', '32', tS], ['O', '4 \\cdot 16 = 64', tO]];
  return (
    <AbsoluteFill>
      <Appear at={2} y={160}>
        <TeX tex={`\\mathrm{${hot(tH) ? A('H') : 'H'}}_{${sub('2', tH)}}\\mathrm{${hot(tS) ? A('S') : 'S'}}\\mathrm{${hot(tO) ? A('O') : 'O'}}_{${sub('4', tO)}}`} size={200} />
      </Appear>
      {parts.map(([el, tex, at], i) => (
        <Fly key={el} at={at} x={170 + i * 560} y={470} from={[0, 200]}>
          <div style={{ width: 460, padding: '24px 30px', border: `4px solid ${C.fg}`, background: C.card, textAlign: 'center' }}>
            <Label>{el}</Label>
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: 8 }}><TeX tex={tex} size={66} /></div>
          </div>
        </Fly>
      ))}
      <Appear at={tSum} y={740}>
        <div style={{ transform: `scale(${punch(frame, tSum + 20, 0.12)})` }}><TeX tex={`M(\\mathrm{H_2SO_4}) = 2 + 32 + 64 = ${A('98')}\\ \\text{г/моль}`} size={76} /></div>
      </Appear>
      <Sfx at={2} name="whoosh" />{parts.map(([el, , at]) => <Sfx key={el} at={at} name="pop" />)}<Sfx at={tSum + 20} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

// Красная сцена-ловушка.
const Trap = ({ title, at = 2, hitAt, children }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, hitAt ?? at, 14, 18)}px)` }}>
      <Kinetic at={at} y={160} size={110} rotate={-4} color={C.bg} punchAt={hitAt}>{title}</Kinetic>
      {children}
      <Sfx at={at} name="whoosh" /><Sfx at={hitAt} name="buzz" volume={0.5} />
    </AbsoluteFill>
  );
};

const Trap1 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [t0, t50] = [W('забыть', 45), W('пятьдесят', 125)];
  return (
    <Trap title="Ловушка: индекс" hitAt={t50}>
      <Appear at={t0} y={420}>
        <Card width={1300}>
          <div style={{ position: 'relative', display: 'inline-block' }}>
            <TeX tex={`M = 2 + 32 + 16 = ${frame >= t50 ? '50' : '\\;?'}`} size={80} />
            {frame >= t50 && <div style={{ position: 'absolute', left: -10, right: -10, top: '52%', height: 10, background: C.accent, transform: 'rotate(-4deg)' }} />}
          </div>
          {frame >= t50 + 25 && <div style={{ marginTop: 22 }}><TeX tex={`\\mathrm{O_4}:\\ 4 \\cdot 16 = ${A('64')} \\ \\Rightarrow\\ M = ${A('98')}`} size={64} /></div>}
        </Card>
      </Appear>
      {frame >= t50 && <Abs x={1600} y={640}><div style={{ font: `800 220px ${F.display}`, color: C.bg, transform: `scale(${punch(frame, t50, 0.3)})` }}>✗</div></Abs>}
    </Trap>
  );
};

// ── n = m/M ────────────────────────────────────────────────

const Formula = ({ scene }) => {
  const W = useW(scene);
  const [tF, tm, tM] = [W('количество', 68), W('масса', 115), W('молярную', 150)];
  const legend = [['n', 'количество, моль', tF + 6], ['m', 'масса, г', tm], ['M', 'молярная масса, г/моль', tM]];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={86} rotate={-3}>Главная формула</Kinetic>
      <Slam at={tF} y={320} size={150}><TeX tex="n = \dfrac{m}{M}" size={150} /></Slam>
      {legend.map(([s, t, at], i) => (
        <Fly key={s} at={at} x={130 + i * 560} y={740} from={[0, 120]}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
            <TeX tex={A(s)} size={70} />
            <div style={{ font: `700 38px ${F.body}`, color: C.fg }}>— {t}</div>
          </div>
        </Fly>
      ))}
      <Sfx at={2} name="whoosh" /><Sfx at={tF} name="boom" volume={0.55} />{legend.slice(1).map(([s, , at]) => <Sfx key={s} at={at} name="pop" volume={0.3} />)}
    </AbsoluteFill>
  );
};

// Пример по шагам: условие → M → ответ.
const Example = ({ title, given, molar, calc, tM, tC, tAns }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={74} rotate={-3} plaque>{title}</Kinetic>
      <Appear at={4} y={330}><TeX tex={given} size={76} /></Appear>
      <Appear at={tM} y={480}><TeX tex={molar} size={66} /></Appear>
      <Appear at={tC} y={630}>
        <div style={{ transform: `scale(${punch(frame, tAns, 0.16)})` }}><TeX tex={calc(frame >= tAns)} size={96} /></div>
      </Appear>
      <Sfx at={2} name="whoosh" /><Sfx at={tM} name="pop" volume={0.3} /><Sfx at={tC} name="whoosh" volume={0.3} /><Sfx at={tAns} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Ex49 = ({ scene }) => {
  const W = useW(scene);
  return (
    <Example title="Граммы → моли" tM={W('молярная', 110)} tC={W('сорок', 195, 1)} tAns={W('половина', 258)}
      given="m(\mathrm{H_2SO_4}) = 49\,\text{г}.\quad n\ -\ ?"
      molar="M(\mathrm{H_2SO_4}) = 98\ \text{г/моль}"
      calc={(on) => `n = \\dfrac{49}{98} = ${on ? A('0{,}5') + '\\ \\text{моль}' : '\\;?'}`} />
  );
};

const Ex88 = ({ scene }) => {
  const W = useW(scene);
  return (
    <Example title="Моли → граммы" tM={W('молярная', 130)} tC={W('два', 214, 1)} tAns={W('восемьдесят', 278)}
      given="n(\mathrm{CO_2}) = 2\ \text{моль}.\quad m\ -\ ?"
      molar="M(\mathrm{CO_2}) = 12 + 2 \cdot 16 = 44\ \text{г/моль}"
      calc={(on) => `m = n \\cdot M = 2 \\cdot 44 = ${on ? A('88') + '\\ \\text{г}' : '\\;?'}`} />
  );
};

// ── Число частиц ───────────────────────────────────────────

const Particles = ({ scene }) => {
  const W = useW(scene);
  const [tF, tA] = [W('количество', 76), W('авогадро', 150)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={170} size={110} rotate={-4}>Число частиц</Kinetic>
      <Slam at={tF} y={400} size={150}><TeX tex="N = n \cdot N_A" size={150} /></Slam>
      <Appear at={tA} y={740}><TeX tex="N_A = 6{,}02 \cdot 10^{23}\ \text{моль}^{-1}" size={60} color={C.muted} /></Appear>
      <Sfx at={2} name="whoosh" /><Sfx at={tF} name="boom" volume={0.55} /><Sfx at={tA} name="pop" volume={0.3} />
    </AbsoluteFill>
  );
};

const WaterScene = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [t1, tQ, tTwo, t2] = [W('три', 48), W('атомов', 170), W('два', 270, 1), W('шесть', 372)];
  return (
    <AbsoluteFill>
      <Abs x={110} y={260}><Water size={480} at={2} hotH={tTwo} /></Abs>
      <Appear at={2} y={170}><div style={{ marginLeft: 560 }}><TeX tex="n(\mathrm{H_2O}) = 0{,}5\ \text{моль}" size={70} /></div></Appear>
      <Abs x={680} y={350}>
        <div style={{ width: 1150, display: 'grid', gap: 40 }}>
          {frame >= t1 && <div><Label>молекул</Label><TeX tex="N(\mathrm{H_2O}) = 0{,}5 \cdot 6{,}02 \cdot 10^{23} = 3{,}01 \cdot 10^{23}" size={58} /></div>}
          {frame >= tQ && <div><Label color={C.accent}>атомов водорода</Label>
            <TeX tex={`N(\\mathrm{H}) = ${frame >= tTwo ? A('2') + ' \\cdot 3{,}01 \\cdot 10^{23}' : '\\;?'}${frame >= t2 ? ' = ' + A('6{,}02 \\cdot 10^{23}') : ''}`} size={58} /></div>}
        </div>
      </Abs>
      {frame >= tTwo && <Abs x={420} y={640}><div style={{ font: `800 90px ${F.display}`, color: C.accent, transform: `scale(${punch(frame, tTwo, 0.3)}) rotate(-6deg)` }}>×2</div></Abs>}
      <Sfx at={2} name="whoosh" /><Sfx at={t1} name="pop" volume={0.3} /><Sfx at={tQ} name="whoosh" volume={0.3} /><Sfx at={tTwo} name="pop" /><Sfx at={t2} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Trap2 = ({ scene }) => {
  const W = useW(scene);
  const [tNot, tRead, tMul] = [W('не', 56), W('читай', 98), W('умножай', 215)];
  return (
    <Trap title="Молекулы ≠ атомы" hitAt={tNot}>
      <Appear at={tRead} y={430}>
        <Card width={1500}>
          <div style={{ font: `800 52px ${F.body}`, color: C.fg }}>Читай вопрос до конца: что спрашивают?</div>
        </Card>
      </Appear>
      <Appear at={tMul} y={700}>
        <div style={{ padding: '24px 40px', background: C.bg }}><TeX tex={`N(\\text{атомов}) = N(\\text{молекул}) \\cdot ${A('\\text{индекс}')}`} size={60} /></div>
      </Appear>
    </Trap>
  );
};

// ── Газы ───────────────────────────────────────────────────

const Gas = ({ scene }) => {
  const W = useW(scene);
  const [tNU, tOne, tV] = [W('нормальных', 108), W('один', 138), W('двадцать', 185)];
  const gases = ['\\mathrm{H_2}', '\\mathrm{O_2}', '\\mathrm{CO_2}'];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={84} rotate={-3}>Газы: через объём</Kinetic>
      <Appear at={tNU} y={290}><Chip size={34}>н. у.: 0 °C · 101,3 кПа</Chip></Appear>
      {gases.map((g, i) => <GasBox key={g} at={tOne + i * 5} x={230 + i * 520} y={400} tex={`1\\ \\text{моль}\\ ${g}`} vAt={tV + i * 5} />)}
      <Sfx at={2} name="whoosh" /><Sfx at={tNU} name="pop" volume={0.3} />
      {gases.map((g, i) => <Sfx key={g} at={tOne + i * 5} name="pop" volume={0.3} />)}{gases.map((g, i) => <Sfx key={g + 'v'} at={tV + i * 5} name="tick" volume={0.5} />)}
    </AbsoluteFill>
  );
};

// Цепочка «узел → действие → узел».
const Node = ({ tex, red }) => (
  <div style={{ width: 380, padding: '30px 0', background: red ? C.accent : C.card, border: `5px solid ${red ? C.accent : C.fg}`, display: 'flex', justifyContent: 'center' }}><TeX tex={tex} size={72} /></div>
);
const Op = ({ tex }) => (
  <div style={{ textAlign: 'center' }}>
    <TeX tex={tex} size={50} color={C.accent} />
    <div style={{ font: `800 90px ${F.display}`, color: C.fg, lineHeight: 0.9 }}>→</div>
  </div>
);

const O2 = ({ scene }) => {
  const W = useW(scene);
  const [tD, tH, tMul, t16] = [W('делим', 100), W('половина', 160), W('умножаем', 212), W('шестнадцать', 260)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={160} size={84} rotate={-3}>Кислород, н. у.</Kinetic>
      <Fly at={6} x={150} y={430} from={[-300, 0]}><Node tex="11{,}2\ \text{л}" /></Fly>
      <Fly at={tD} x={560} y={420} from={[0, -120]}><Op tex="\div 22{,}4" /></Fly>
      <Fly at={tH} x={770} y={430} from={[0, 200]}><Node tex="0{,}5\ \text{моль}" /></Fly>
      <Fly at={tMul} x={1190} y={420} from={[0, -120]}><Op tex="\times 32" /></Fly>
      <Fly at={t16} x={1390} y={430} from={[300, 0]}><Node tex="16\ \text{г}" red /></Fly>
      <Appear at={tMul} y={700}><TeX tex="M(\mathrm{O_2}) = 2 \cdot 16 = 32\ \text{г/моль}" size={54} color={C.muted} /></Appear>
      <Sfx at={2} name="whoosh" /><Sfx at={tD} name="pop" volume={0.3} /><Sfx at={tH} name="pop" /><Sfx at={tMul} name="pop" volume={0.3} /><Sfx at={t16} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Trap3 = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tGas, tNU, tWater, tLiq] = [W('газов', 60), W('условиях', 106), W('вода', 148), W('жидкость', 198)];
  return (
    <Trap title="22,4 — только для газов" hitAt={tLiq}>
      <Row y={380} style={{ gap: 30 }}>
        {frame >= tGas && <div style={{ transform: `scale(${punch(frame, tGas)})` }}><Chip>газ ✓</Chip></div>}
        {frame >= tNU && <div style={{ transform: `scale(${punch(frame, tNU)})` }}><Chip>н. у. ✓</Chip></div>}
      </Row>
      <Appear at={tWater} y={560}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 40, padding: '26px 44px', background: C.bg }}>
          <TeX tex="\mathrm{H_2O}" size={90} />
          <div style={{ font: `800 50px ${F.body}`, color: C.fg }}>при н. у. — жидкость</div>
          {frame >= tLiq && <div style={{ font: `800 110px ${F.display}`, color: C.accent, transform: `scale(${punch(frame, tLiq, 0.3)})` }}>✗</div>}
        </div>
      </Appear>
    </Trap>
  );
};

// ── Схема: всё через моль ──────────────────────────────────

const HubMap = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tC, tm, tN, tV] = [W('центре', 95), W('массы', 150), W('числа', 225), W('объёма', 340)];
  const cx = 960;
  const cy = 540;
  const draw = (at) => interpolate(frame, [at, at + 14], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  // Подписи: «÷» над линией (к молям), «×» под линией (обратно).
  const spokes = [
    { at: tm, x1: 560, y1: cy, x2: cx - 150, y2: cy, op: '\\div M', back: '\\times M', lx: 585, ly: cy - 78, by: cy + 14 },
    { at: tN, x1: 1360, y1: cy, x2: cx + 150, y2: cy, op: '\\div N_A', back: '\\times N_A', lx: 1135, ly: cy - 78, by: cy + 14 },
    { at: tV, x1: cx, y1: 800, x2: cx, y2: cy + 150, op: '\\div 22{,}4', back: '\\times 22{,}4', lx: cx + 20, ly: 702, by: 702, side: true },
  ];
  const nodes = [
    { at: tm, x: 140, y: cy - 70, tex: 'm,\\ \\text{г}' },
    { at: tN, x: 1360, y: cy - 70, tex: 'N,\\ \\text{штук}' },
    { at: tV, x: cx - 210, y: 800, tex: 'V,\\ \\text{л}\\ (\\text{газ, н. у.})', w: 420 },
  ];
  const pc = enter(frame, tC, fps, { damping: 11, stiffness: 160 });
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={80} rotate={-3}>Всё через моль</Kinetic>
      <svg width="1920" height="1080" style={{ position: 'absolute', left: 0, top: 0 }}>
        {spokes.map((s) => {
          const k = draw(s.at);
          return k > 0 && <line key={s.op} x1={s.x1} y1={s.y1} x2={s.x1 + (s.x2 - s.x1) * k} y2={s.y1 + (s.y2 - s.y1) * k} stroke={C.fg} strokeWidth="8" />;
        })}
      </svg>
      {spokes.map((s) => frame >= s.at + 10 && (
        <React.Fragment key={s.op}>
          <Abs x={s.side ? s.lx : s.lx} y={s.ly} style={{ width: s.side ? undefined : 200, display: 'flex', justifyContent: 'center' }}><TeX tex={s.op} size={50} color={C.accent} /></Abs>
          <Abs x={s.side ? s.lx - 200 : s.lx} y={s.by} style={{ width: 180, display: 'flex', justifyContent: s.side ? 'flex-end' : 'center' }}><TeX tex={s.back} size={36} color={C.muted} /></Abs>
        </React.Fragment>
      ))}
      {nodes.map((n) => frame >= n.at && (
        <Abs key={n.tex} x={n.x} y={n.y} style={{ transform: `scale(${enter(frame, n.at, fps)})` }}>
          <div style={{ width: n.w ?? 420, height: n.w ? 100 : 140, border: `5px solid ${C.fg}`, background: C.card, display: 'grid', placeItems: 'center' }}><TeX tex={n.tex} size={n.w ? 46 : 64} /></div>
        </Abs>
      ))}
      {frame >= tC && (
        <Abs x={cx - 150} y={cy - 150} style={{ transform: `scale(${pc})` }}>
          <div style={{ width: 300, height: 300, borderRadius: '50%', background: C.accent, display: 'grid', placeItems: 'center', textAlign: 'center' }}>
            <div><TeX tex="n" size={110} /><div style={{ font: `800 40px ${F.display}`, color: C.fg }}>МОЛЬ</div></div>
          </div>
        </Abs>
      )}
      <Sfx at={2} name="whoosh" /><Sfx at={tC} name="boom" volume={0.5} />{[tm, tN, tV].map((at) => <Sfx key={at} at={at} name="whoosh" volume={0.3} />)}
    </AbsoluteFill>
  );
};

// ── Задача ЕНТ ─────────────────────────────────────────────

const TASK_OPTIONS = [['А', '3{,}01 \\cdot 10^{23}'], ['Б', '6{,}02 \\cdot 10^{23}'], ['В', '1{,}2 \\cdot 10^{24}'], ['Г', '0{,}5']];

const TaskCard = ({ states = {}, at = 0, timer }) => (
  <Card width={1600}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <Label>ЕНТ · выбери один ответ</Label>
      {timer}
    </div>
    <div style={{ marginTop: 22 }}><TeX tex="\text{Сколько атомов кислорода в } 22\,\text{г}\ \mathrm{CO_2}\text{?}" size={60} /></div>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 22, marginTop: 34 }}>
      {TASK_OPTIONS.map(([l, v], i) => <Option key={l} letter={l} value={v} unit="" at={at + i * 4} state={states[l]} />)}
    </div>
  </Card>
);

const Task = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tQ, tP] = [W('сколько', 72), W('паузу', 230)];
  const left = interpolate(frame, [tP, scene.dur - 4], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const R = 34;
  const timer = (
    <svg width={2 * R + 12} height={2 * R + 12} viewBox={`${-R - 6} ${-R - 6} ${2 * R + 12} ${2 * R + 12}`}>
      <circle r={R} fill="none" stroke={C.faint} strokeWidth="8" />
      <circle r={R} fill="none" stroke={C.accent} strokeWidth="8" strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - left)} transform="rotate(-90)" />
    </svg>
  );
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={84} rotate={-3} plaque>Задача ЕНТ</Kinetic>
      <Appear at={tQ} y={330}><TaskCard at={tQ + 20} timer={timer} /></Appear>
      {frame >= tP && <Abs x={1640} y={150}><div style={{ font: `800 110px ${F.display}`, color: C.accent, opacity: 0.6 + 0.4 * Math.sin((frame - tP) / 5) }}>❚❚</div></Abs>}
      <Sfx at={2} name="whoosh" /><Sfx at={tQ} name="whoosh" volume={0.3} />{TASK_OPTIONS.map(([l], i) => <Sfx key={l} at={tQ + 20 + i * 4} name="tick" volume={0.5} />)}
      {[0, 1, 2, 3].map((k) => <Sfx key={k} at={tP + 20 + k * 30} name="tick" volume={0.35} />)}
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [t1, tHalf, t2, tMol, t3, tB] = [W('двадцать', 45), W('половина', 108), W('каждой', 190), W('целый', 320), W('шесть', 345), W('б', 465)];
  const states = frame >= tB ? { А: 'dim', Б: 'right', В: 'dim', Г: 'dim' } : {};
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={84} rotate={-3}>Проверяем</Kinetic>
      <Abs x={160} y={300}>
        <div style={{ display: 'grid', gap: 28 }}>
          {frame >= t1 && <TeX tex={`n(\\mathrm{CO_2}) = \\dfrac{22}{44} = ${Q(frame, tHalf, '0{,}5')}\\ \\text{моль}`} size={64} />}
          {frame >= t2 && <TeX tex={`\\text{в }\\mathrm{CO_2}\\text{ два атома O} \\ \\Rightarrow\\ n(\\mathrm{O}) = ${Q(frame, tMol, '1')}\\ \\text{моль}`} size={60} />}
          {frame >= t3 && <TeX tex={`N(\\mathrm{O}) = 1 \\cdot 6{,}02 \\cdot 10^{23} = ${A('6{,}02 \\cdot 10^{23}')}`} size={60} />}
        </div>
      </Abs>
      {frame >= tB && (
        <Row y={760} style={{ gap: 22 }}>
          {TASK_OPTIONS.map(([l, v]) => <div key={l} style={{ width: 360 }}><Option letter={l} value={v} unit="" state={states[l]} at={tB} /></div>)}
        </Row>
      )}
      <Sfx at={2} name="whoosh" /><Sfx at={tHalf} name="pop" volume={0.3} /><Sfx at={tMol} name="pop" /><Sfx at={tB} name="ding" volume={0.55} />
    </AbsoluteFill>
  );
};

// ── Курс и подписка ────────────────────────────────────────

const Cta = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tC, tOn, tG, tS, tD, tSub] = [W('химия', 70), W('онлайн', 135), W('группы', 160), W('старт', 200), W('директ', 295), W('подпишись', 395)];
  const chips = [['онлайн', tOn], ['группы по 5', tG], ['старт 1 ноября', tS]];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={150} size={70} rotate={-3}>Так разбираем каждую тему</Kinetic>
      <Appear at={tC} y={300}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 30 }}>
          <Atom size={150} at={tC} speed={1.4} />
          <div>
            <div style={{ font: `800 84px ${F.display}`, color: C.fg, lineHeight: 1 }}>ХИМБИО ПРОСТО</div>
            <div style={{ font: `700 42px ${F.body}`, color: C.muted, marginTop: 8 }}>курс подготовки к ЕНТ по химии</div>
          </div>
        </div>
      </Appear>
      <Row y={510} style={{ gap: 20 }}>
        {chips.map(([c, at], i) => {
          const p = frame < at ? 0 : enter(frame, at, fps);
          return frame < at ? null : <div key={c} style={{ transform: `scale(${p})` }}><Chip red={i === 2}>{c}</Chip></div>;
        })}
      </Row>
      <Appear at={tD - 20} y={650}><div style={{ font: `700 44px ${F.body}`, color: C.muted }}>Запись — в директ Instagram</div></Appear>
      <Kinetic at={tD} y={720} size={96} rotate={-2}>@himbio.prosto</Kinetic>
      {frame >= tSub && (
        <Abs x={1390} y={850}>
          <div style={{ transform: `scale(${punch(frame, tSub, 0.25)}) rotate(4deg)`, padding: '22px 44px', background: C.accent, borderRadius: 60, font: `800 40px ${F.display}`, color: '#fff', whiteSpace: 'nowrap' }}>ПОДПИСАТЬСЯ</div>
        </Abs>
      )}
      <Sfx at={2} name="whoosh" /><Sfx at={tC} name="whoosh" />{chips.map(([c, at]) => <Sfx key={c} at={at} name="pop" volume={0.35} />)}
      <Sfx at={tD} name="whoosh" /><Sfx at={tSub} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

// Титул: о чём видео — в первые секунды.
const Title = ({ scene }) => (
  <TopicIntro scene={scene} tag="ЕНТ · химия" title="Моль" plaque="за 4 минуты"
    items={[['Молярная масса', 'молярную'], ['Главная формула n = m/M', 'главную'], ['Число частиц', 'частиц'], ['Газы и 22,4 л/моль', 'газы'], ['Задача ЕНТ — реши сам', 'задача']]} />
);

export const SCENES = {
  title: Title, hook: Hook, intro: Intro, pack: Pack, avogadro: Avogadro, amount: Amount, weigh: Weigh, molar: Molar, h2so4: H2SO4, trap1: Trap1,
  formula: Formula, ex49: Ex49, ex88: Ex88, particles: Particles, water: WaterScene, trap2: Trap2, gas: Gas, o2: O2, trap3: Trap3,
  map: HubMap, task: Task, answer: Answer, cta: Cta,
};
export const TAILS = { title: 24, hook: 16, intro: 10, pack: 24, h2so4: 24, trap1: 30, ex49: 24, ex88: 24, water: 24, o2: 24, trap3: 14, map: 40, task: 150, answer: 36, cta: 60 };
