// Шаблон рубрик Reels: «Правда или миф?», «Найди ошибку», «Химия vs Биология», «Факт за 10 секунд».
// Ролик задаётся конфигом (makeSeries). Тайминги — по словам озвучки: [стем, запасной кадр]. '$…' — формула KaTeX.
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F, SUBJECT } from '../theme.js';
import { Appear, Atom, Card, Dna, Kinetic, Label, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { CourseOutro, Slam, useW } from '../scenes.jsx';

const Line = ({ value, size = 50, color = C.fg }) =>
  value.startsWith('$') ? (
    <TeX tex={value.slice(1)} size={size + 8} color={color} />
  ) : (
    <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: size, lineHeight: 1.22, color }}>{value}</div>
  );

const Ring = ({ scene, from = 2, R = 40 }) => {
  const frame = useCurrentFrame();
  const left = interpolate(frame, [from, scene.dur - 2], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <svg width={2 * R + 12} height={2 * R + 12} viewBox={`${-R - 6} ${-R - 6} ${2 * R + 12} ${2 * R + 12}`}>
      <circle r={R} fill="none" stroke={C.faint} strokeWidth="9" />
      <circle r={R} fill="none" stroke={C.accent} strokeWidth="9" strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - left)} transform="rotate(-90)" />
    </svg>
  );
};

const Icon = ({ icon, at, size = 240 }) => (icon === 'dna' ? <Dna size={size} at={at} /> : icon === 'both' ? (
  <div style={{ display: 'flex', gap: 60, alignItems: 'center' }}><Atom size={size * 0.85} at={at} speed={1.3} /><Dna size={size} at={at} /></div>
) : <Atom size={size} at={at} speed={1.3} />);

// Титул рубрики: две строки названия, подзаголовок, значок.
const Hook = (cfg) => ({ scene }) => {
  const W = useW(scene);
  const [a, b] = cfg.name;
  const t2 = W(cfg.nameStem ?? '', 8);
  const tSub = W(cfg.subStem ?? '', t2 + 20);
  return (
    <AbsoluteFill>
      <Appear at={2} y={300}><Label size={40} color={C.accent}>новая рубрика</Label></Appear>
      <Kinetic at={2} y={420} size={130} rotate={-4}>{a}</Kinetic>
      <Kinetic at={t2} y={590} size={130} rotate={-4} from="right" plaque punchAt={t2 + 4}>{b}</Kinetic>
      <Appear at={tSub} y={800}><div style={{ font: `800 50px ${F.body}`, color: C.muted, textAlign: 'center' }}>{cfg.sub}</div></Appear>
      <Row y={940}><Icon icon={cfg.icon} at={tSub} /></Row>
      <Sfx at={2} name="whoosh" /><Sfx at={t2} name="boom" volume={0.5} /><Sfx at={tSub} name="pop" volume={0.35} />
    </AbsoluteFill>
  );
};

// Штамп-вердикт: как Slam, но со своим цветом плашки.
const Stamp = ({ at, y, size, bg, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 10, stiffness: 220, mass: 0.6 });
  return (
    <Row y={y}>
      <div style={{ transform: `scale(${interpolate(p, [0, 1], [2.4, 1])}) rotate(-6deg)`, opacity: Math.min(1, p * 3), background: bg, color: C.fg, fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: 1, padding: `${size * 0.1}px ${size * 0.2}px ${size * 0.14}px`, whiteSpace: 'nowrap', border: `8px solid ${C.fg}` }}>
        {children}
      </div>
    </Row>
  );
};

// ---------- «Правда или миф?»
const Statement = (cfg, n) => ({ scene }) => {
  const st = cfg.statements[n - 1];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={260} size={84} rotate={-3} plaque>{`Утверждение ${n} из ${cfg.statements.length}`}</Kinetic>
      <Appear at={2} y={460}>
        <Card width={936}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Label>правда или миф?</Label>
            <Ring scene={scene} />
          </div>
          <div style={{ marginTop: 28, font: `800 64px ${F.display}`, lineHeight: 1.14, color: C.fg }}>{st.text}</div>
        </Card>
      </Appear>
      <Row y={1060} style={{ gap: 40 }}>
        {['правда', 'миф'].map((w) => (
          <div key={w} style={{ border: `4px solid ${C.fg}`, padding: '16px 46px', font: `800 54px ${F.display}`, textTransform: 'uppercase', color: C.fg }}>{w}</div>
        ))}
      </Row>
      <Sfx at={1} name="whoosh" />{[20, 35, 50].map((t) => <Sfx key={t} at={t} name="tick" volume={0.4} />)}
    </AbsoluteFill>
  );
};

const Verdict = (cfg, n) => ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const st = cfg.statements[n - 1];
  const myth = st.verdict === 'myth';
  const tX = W(st.stem, 30);
  return (
    <AbsoluteFill style={{ transform: `translateX(${myth ? shake(frame, 2, 14, 16) : 0}px)` }}>
      <Stamp at={2} y={330} size={myth ? 200 : 150} bg={myth ? SUBJECT.chem : C.accent}>{myth ? 'МИФ' : 'ПРАВДА'}</Stamp>
      <Appear at={tX} y={700}>
        <Card width={936}>
          <Line value={st.explain} size={54} />
        </Card>
      </Appear>
      <Sfx at={2} name={myth ? 'buzz' : 'ding'} volume={0.5} /><Sfx at={tX} name="pop" volume={0.4} />
    </AbsoluteFill>
  );
};

// ---------- «Найди ошибку»
const SolutionCard = ({ cfg, times, frame, mark = false }) => (
  <Card width={936}>
    <Label>{cfg.solTitle ?? 'решение'}</Label>
    <div style={{ marginTop: 22, display: 'grid', gap: 26 }}>
      {cfg.steps.map((value, i) => {
        if (times && frame < times[i]) return null;
        const bad = mark && i === cfg.wrongStep;
        return (
          <div key={i} style={{ position: 'relative', borderLeft: `10px solid ${C.faint}`, paddingLeft: 24, opacity: mark && !bad ? 0.5 : 1 }}>
            <Line value={value} size={cfg.stepSize ?? 50} />
            {bad && <div style={{ position: 'absolute', inset: '-14px -18px -14px -8px', border: `7px solid ${SUBJECT.chem}`, borderRadius: 60, transform: `scale(${enter(frame, 2, 30)}) rotate(-1.5deg)` }} />}
          </div>
        );
      })}
    </div>
  </Card>
);

const Task = (cfg) => ({ scene }) => (
  <AbsoluteFill>
    <Kinetic at={0} y={260} size={90} rotate={-3} plaque>Задача</Kinetic>
    <Appear at={4} y={480}>
      <Card width={936}><div style={{ display: 'grid', gap: 16 }}>{cfg.task.map((t) => <Line key={t} value={t} size={58} />)}</div></Card>
    </Appear>
    <Sfx at={1} name="whoosh" />
  </AbsoluteFill>
);

const Solution = (cfg) => ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const times = cfg.stepStems.map(([stem, fb]) => W(stem, fb));
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={260} size={80} rotate={-3}>Где ошибка?</Kinetic>
      <Appear at={2} y={440}><SolutionCard cfg={cfg} times={times} frame={frame} /></Appear>
      {times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
    </AbsoluteFill>
  );
};

const Pause = (cfg) => ({ scene }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={260} size={100} rotate={-4} plaque punchAt={4}>Нашёл?</Kinetic>
      <Appear at={0} y={440}><SolutionCard cfg={cfg} frame={frame} /></Appear>
      <Row y={1080}><Ring scene={scene} R={56} /></Row>
      {[10, 30, 50, 70].map((t) => <Sfx key={t} at={t} name="tick" volume={0.45} />)}
    </AbsoluteFill>
  );
};

const Reveal = (cfg) => ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tFix = W(cfg.fixStem, 40);
  const tAns = W(cfg.answerStem, tFix + 60);
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={240} size={90} rotate={-3} plaque bg={SUBJECT.chem}>Ошибка!</Kinetic>
      <Appear at={0} y={400}><SolutionCard cfg={cfg} frame={frame} mark /></Appear>
      <Appear at={tFix} y={880}>
        <Card width={936} style={{ borderColor: C.accent }}><Line value={cfg.fix} size={48} /></Card>
      </Appear>
      <Slam at={tAns} y={1110} size={110}>{cfg.answer}</Slam>
      <Sfx at={2} name="buzz" volume={0.45} /><Sfx at={tFix} name="pop" volume={0.4} /><Sfx at={tAns} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

// ---------- «Химия vs Биология»
const VsHook = (cfg) => ({ scene }) => {
  const W = useW(scene);
  const tB = W('биологи', 20);
  const tSub = W(cfg.subStem ?? '', tB + 20);
  return (
    <AbsoluteFill>
      <Appear at={2} y={290}><Label size={40} color={C.fg}>новая рубрика</Label></Appear>
      <Kinetic at={2} y={400} size={120} rotate={-4} plaque bg={SUBJECT.chem}>Химия</Kinetic>
      <Kinetic at={tB - 6} y={560} size={90} rotate={0}>vs</Kinetic>
      <Kinetic at={tB} y={690} size={120} rotate={-4} from="right" plaque bg={SUBJECT.bio}>Биология</Kinetic>
      <Appear at={tSub} y={900}><div style={{ font: `800 50px ${F.body}`, color: C.muted, textAlign: 'center' }}>{cfg.sub}</div></Appear>
      <Row y={1020}><Icon icon="both" at={tSub} size={200} /></Row>
      <Sfx at={2} name="whoosh" /><Sfx at={tB} name="boom" volume={0.5} /><Sfx at={tSub} name="pop" volume={0.35} />
    </AbsoluteFill>
  );
};

const Side = (cfg, key) => ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const s = cfg[key];
  const color = key === 'chem' ? SUBJECT.chem : SUBJECT.bio;
  const times = s.rows.map(([, stem, fb]) => W(stem, fb));
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={100} rotate={-3} plaque bg={color}>{key === 'chem' ? 'Химия' : 'Биология'}</Kinetic>
      <Appear at={2} y={450}>
        <Card width={936}>
          <Label>{s.question}</Label>
          <div style={{ marginTop: 24, display: 'grid', gap: 26 }}>
            {s.rows.map(([value, , , big], i) =>
              frame < times[i] ? null : (
                <div key={i} style={{ transform: `scale(${0.9 + 0.1 * enter(frame, times[i], 30)})`, transformOrigin: 'left center', borderLeft: `10px solid ${big ? color : C.faint}`, paddingLeft: 24 }}>
                  <Line value={value} size={big ? 58 : 50} />
                </div>
              )
            )}
          </div>
        </Card>
      </Appear>
      <Sfx at={1} name="whoosh" />{times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
    </AbsoluteFill>
  );
};

const Link = (cfg) => ({ scene }) => (
  <AbsoluteFill>
    <Kinetic at={0} y={420} size={96} rotate={-3}>Одна молекула —</Kinetic>
    <Kinetic at={10} y={570} size={96} rotate={-3} from="right" plaque>две темы ЕНТ</Kinetic>
    <Row y={820}><Icon icon="both" at={14} size={220} /></Row>
    <Sfx at={1} name="whoosh" /><Sfx at={10} name="boom" volume={0.45} />
  </AbsoluteFill>
);

// ---------- «Факт за 10 секунд»
const Fact = (cfg) => ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const times = cfg.fact.map(([, stem, fb]) => W(stem, fb));
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={84} rotate={-3} plaque>{cfg.factTitle}</Kinetic>
      <div style={{ position: 'absolute', top: 470, left: 72, right: 72, display: 'grid', gap: 40 }}>
        {cfg.fact.map(([value, , , note], i) => {
          if (frame < times[i]) return null;
          const p = enter(frame, times[i], fps);
          return (
            <div key={i} style={{ opacity: p, transform: `translateX(${(1 - p) * 140}px)`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', border: `4px solid ${C.fg}`, background: C.card, padding: '26px 40px' }}>
              <TeX tex={value} size={96} />
              <div style={{ font: `800 54px ${F.display}`, color: C.accent, textTransform: 'uppercase' }}>{note}</div>
            </div>
          );
        })}
      </div>
      {cfg.factCaption && frame >= times[times.length - 1] + 20 && (
        <Row y={980}><div style={{ font: `800 46px ${F.body}`, color: C.muted, textAlign: 'center', maxWidth: 900 }}>{cfg.factCaption}</div></Row>
      )}
      <Sfx at={1} name="whoosh" />{times.map((t, i) => <Sfx key={i} at={t} name="boom" volume={0.4} />)}
    </AbsoluteFill>
  );
};

const Check = (cfg) => ({ scene }) => {
  const W = useW(scene);
  const tA = W(cfg.check.stem, 60);
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={260} size={90} rotate={-3} plaque>Проверь себя</Kinetic>
      <Appear at={4} y={460}><Card width={936}><Line value={cfg.check.question} size={60} /></Card></Appear>
      <Slam at={tA} y={850} size={260}>{cfg.check.answer}</Slam>
      <Sfx at={1} name="whoosh" /><Sfx at={tA} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

export const makeSeries = (cfg) => {
  const SCENES = { outro: ({ scene }) => <CourseOutro scene={scene} icon={cfg.icon === 'dna' ? 'dna' : 'atom'} /> };
  const TAILS = { outro: 36 };
  if (cfg.kind === 'myth') {
    SCENES.hook = Hook(cfg);
    cfg.statements.forEach((_, i) => {
      SCENES[`s${i + 1}`] = Statement(cfg, i + 1);
      SCENES[`v${i + 1}`] = Verdict(cfg, i + 1);
      TAILS[`s${i + 1}`] = 60;
      TAILS[`v${i + 1}`] = 20;
    });
  } else if (cfg.kind === 'error') {
    Object.assign(SCENES, { hook: Hook(cfg), task: Task(cfg), sol: Solution(cfg), pause: Pause(cfg), reveal: Reveal(cfg) });
    Object.assign(TAILS, { task: 16, sol: 20, pause: 75, reveal: 30 });
  } else if (cfg.kind === 'vs') {
    Object.assign(SCENES, { hook: VsHook(cfg), chem: Side(cfg, 'chem'), bio: Side(cfg, 'bio'), link: Link(cfg) });
    Object.assign(TAILS, { chem: 30, bio: 30, link: 20 });
  } else if (cfg.kind === 'fact') {
    Object.assign(SCENES, { hook: Hook(cfg), fact: Fact(cfg), check: Check(cfg) });
    Object.assign(TAILS, { fact: 40, check: 30 });
  }
  return { SCENES, TAILS };
};
