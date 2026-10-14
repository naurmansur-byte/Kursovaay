// Шаблон YouTube-ролика 16:9 «3 задачи ЕНТ с ловушками»: title → (q, e, t, a) × 3 → cta. Ролик задаётся конфигом (makeWide).
// Тайминги — по словам озвучки: [стем, запасной кадр]. Строка с префиксом '$' — формула KaTeX.
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Atom, Card, Dna, Kinetic, Label, Option, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { Slam, TopicIntro, useW } from '../scenes.jsx';

const Abs = ({ x, y, children, style }) => <div style={{ position: 'absolute', left: x, top: y, ...style }}>{children}</div>;

const Line = ({ value, size = 54, color = C.fg }) =>
  value.startsWith('$') ? (
    <TeX tex={value.slice(1)} size={size + 6} color={color} />
  ) : (
    <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: size, lineHeight: 1.2, color }}>{value}</div>
  );

const Chip = ({ children, red, at }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  return <div style={{ transform: `scale(${enter(frame, at, fps)})`, padding: '14px 28px', background: red ? C.accent : C.bg, border: `4px solid ${red ? C.accent : C.fg}`, fontFamily: F.body, fontWeight: 800, fontSize: 40, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>{children}</div>;
};

export const makeWide = (cfg) => {
  const Title = ({ scene }) => <TopicIntro scene={scene} tag={cfg.tag} title={cfg.title} plaque={cfg.plaque} icon={cfg.icon} items={cfg.items} />;

  const Question = (n) => ({ scene }) => {
    const frame = useCurrentFrame();
    const q = cfg.tasks[n - 1];
    const left = interpolate(frame, [20, scene.dur - 2], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    const R = 34;
    return (
      <AbsoluteFill>
        <Kinetic at={0} y={175} size={78} rotate={-3} plaque>{`Задача ${n} из 3`}</Kinetic>
        <Appear at={2} y={300}>
          <Card width={1560}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Label>ЕНТ · выбери один ответ · поставь на паузу</Label>
              <svg width={2 * R + 12} height={2 * R + 12} viewBox={`${-R - 6} ${-R - 6} ${2 * R + 12} ${2 * R + 12}`}>
                <circle r={R} fill="none" stroke={C.faint} strokeWidth="8" />
                <circle r={R} fill="none" stroke={C.accent} strokeWidth="8" strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - left)} transform="rotate(-90)" />
              </svg>
            </div>
            <div style={{ marginTop: 22, display: 'grid', gap: 8 }}>
              {q.question.map((t) => <TeX key={t} tex={t} size={q.questionSize ?? 56} />)}
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginTop: 30 }}>
              {q.options.map(([l, v], i) => <Option key={l} letter={l} value={v} unit="" at={6 + i * 3} />)}
            </div>
          </Card>
        </Appear>
        {[6, 9, 12, 15].map((t) => <Sfx key={t} at={t} name="tick" volume={0.45} />)}
      </AbsoluteFill>
    );
  };

  const Explain = (n) => ({ scene }) => {
    const frame = useCurrentFrame();
    const W = useW(scene);
    const q = cfg.tasks[n - 1];
    const times = q.explain.rows.map(([, stem, fb]) => W(stem, fb));
    return (
      <AbsoluteFill>
        <Kinetic at={0} y={175} size={80} rotate={-3} plaque>{q.explain.title}</Kinetic>
        <Appear at={2} y={310}>
          <Card width={1500}>
            <div style={{ display: 'grid', gap: 26 }}>
              {q.explain.rows.map(([value, , , red], i) =>
                frame < times[i] ? null : (
                  <div key={i} style={{ transform: `scale(${0.92 + 0.08 * enter(frame, times[i], 30)})`, transformOrigin: 'left center', borderLeft: `10px solid ${red ? C.accent : C.faint}`, paddingLeft: 26 }}>
                    <Line value={value} size={50} />
                  </div>
                )
              )}
            </div>
          </Card>
        </Appear>
        {times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
      </AbsoluteFill>
    );
  };

  const Trap = (n) => ({ scene }) => {
    const frame = useCurrentFrame();
    const W = useW(scene);
    const q = cfg.tasks[n - 1];
    const tHit = W(q.trap.stem, 20);
    const tSub = q.trap.sub ? W(q.trap.sub[1], tHit + 40) : null;
    return (
      <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, tHit, 14, 18)}px)` }}>
        <Kinetic at={0} y={160} size={110} rotate={-5} color={C.bg} punchAt={tHit}>Ловушка</Kinetic>
        <Appear at={8} y={340}>
          <Card width={1400}>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 60, color: C.fg, lineHeight: 1.15 }}>{q.trap.main}</div>
            {q.trap.sub && frame >= tSub && <div style={{ marginTop: 24 }}><Line value={q.trap.sub[0]} size={46} /></div>}
          </Card>
        </Appear>
        <Row y={690} style={{ gap: 24 }}>
          {(q.trap.wrong || []).map((letter, i) => {
            const opt = q.options.find(([l]) => l === letter);
            return <div key={letter} style={{ background: C.bg, padding: 6 }}><Option letter={letter} value={opt[1]} unit="" state="wrong" at={tHit + i * 6} compact /></div>;
          })}
        </Row>
        <Sfx at={1} name="whoosh" /><Sfx at={tHit} name="buzz" volume={0.5} />
        {tSub != null && <Sfx at={tSub} name="pop" volume={0.4} />}
      </AbsoluteFill>
    );
  };

  const Answer = (n) => ({ scene }) => {
    const frame = useCurrentFrame();
    const W = useW(scene);
    const q = cfg.tasks[n - 1];
    const tS = W(q.answer.stem, 15);
    const tAns = W('ответ', tS + 40);
    const opt = q.options.find(([l]) => l === q.answer.right);
    return (
      <AbsoluteFill>
        <Kinetic at={0} y={175} size={78} rotate={-3}>{`Задача ${n}: ответ`}</Kinetic>
        <Slam at={tS} y={370} size={q.answer.size ?? 140}>{q.answer.slam}</Slam>
        <Row y={680}>
          <div style={{ transform: `scale(${punch(frame, tAns, 0.12)})` }}><Option letter={opt[0]} value={opt[1]} unit="" state="right" at={tAns} compact /></div>
        </Row>
        <Sfx at={tS} name="boom" volume={0.5} /><Sfx at={tAns} name="ding" volume={0.5} />
      </AbsoluteFill>
    );
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

  const SCENES = { title: Title, cta: Cta };
  const TAILS = { title: 24, cta: 60 };
  for (const n of [1, 2, 3]) {
    SCENES[`q${n}`] = Question(n);
    SCENES[`e${n}`] = Explain(n);
    SCENES[`t${n}`] = Trap(n);
    SCENES[`a${n}`] = Answer(n);
    TAILS[`q${n}`] = 110;  // пауза «подумай» с таймером
    TAILS[`a${n}`] = 24;
    TAILS[`t${n}`] = 16;
  }
  return { SCENES, TAILS };
};
