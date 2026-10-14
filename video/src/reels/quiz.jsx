// Шаблон рилса-вопроса ЕНТ: hook → engage → explain → trap → answer → outro. Ролик задаётся конфигом (makeQuiz).
// Тайминги появления — по словам озвучки: [стем, запасной кадр]. Формулы — KaTeX (строка с префиксом '$').
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Atom, Card, Dna, Kinetic, Option, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { CourseOutro, EngageScene, Slam, useW } from '../scenes.jsx';

// Строка: '$...' — формула, иначе — текст.
const Line = ({ value, size = 52, color = C.fg }) =>
  value.startsWith('$') ? (
    <TeX tex={value.slice(1)} size={size + 6} color={color} />
  ) : (
    <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: size, lineHeight: 1.2, color }}>{value}</div>
  );

const Visual = ({ v, at }) => {
  if (!v) return null;
  if (v === 'atom') return <Atom size={300} at={at} speed={1.2} />;
  if (v === 'dna') return <Dna size={260} at={at} />;
  return (
    <Card width={900} style={{ display: 'flex', justifyContent: 'center' }}>
      <TeX tex={v} size={v.length > 25 ? 68 : 88} />
    </Card>
  );
};

export const makeQuiz = (q) => {
  const Hook = ({ scene }) => {
    const W = useW(scene);
    const tV = W(q.hook.visualStem || '', 4);
    return (
      <AbsoluteFill>
        <Appear at={tV} y={q.hook.visualY ?? 300}>
          <Visual v={q.hook.visual} at={tV} />
        </Appear>
        {q.hook.lines.map(([text, stem, fb, o = {}], i) => {
          const at = W(stem, fb);
          return (
            <React.Fragment key={i}>
              <Kinetic at={at} y={o.y ?? 760 + i * 150} size={o.size ?? 104} rotate={-4} from={i % 2 ? 'right' : 'left'} plaque={o.plaque} punchAt={o.plaque ? at + 4 : undefined}>
                {text}
              </Kinetic>
              <Sfx at={at} name={o.plaque ? 'boom' : 'whoosh'} volume={o.plaque ? 0.5 : 0.35} />
            </React.Fragment>
          );
        })}
      </AbsoluteFill>
    );
  };

  const Engage = ({ scene }) => (
    <EngageScene scene={scene} unit="" cols={q.cols ?? 1} questionSize={q.questionSize ?? 52} questionTex={q.question} options={q.options} />
  );

  const Explain = ({ scene }) => {
    const frame = useCurrentFrame();
    const W = useW(scene);
    const times = q.explain.rows.map(([, stem, fb]) => W(stem, fb));
    return (
      <AbsoluteFill>
        <Kinetic at={0} y={240} size={96} rotate={-3} plaque>{q.explain.title}</Kinetic>
        <Appear at={2} y={430}>
          <Card width={936}>
            <div style={{ display: 'grid', gap: 30 }}>
              {q.explain.rows.map(([value, , , red], i) =>
                frame < times[i] ? null : (
                  <div key={i} style={{ transform: `scale(${0.9 + 0.1 * enter(frame, times[i], 30)})`, transformOrigin: 'left center', borderLeft: `10px solid ${red ? C.accent : C.faint}`, paddingLeft: 24 }}>
                    <Line value={value} size={q.explain.size ?? 50} />
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

  const Trap = ({ scene }) => {
    const frame = useCurrentFrame();
    const W = useW(scene);
    const tHit = W(q.trap.stem, 20);
    const tSub = q.trap.sub ? W(q.trap.sub[1], tHit + 40) : null;
    return (
      <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, tHit, 14, 18)}px)` }}>
        <Kinetic at={0} y={240} size={130} rotate={-6} color={C.bg} punchAt={tHit}>Ловушка</Kinetic>
        <Appear at={8} y={470}>
          <Card width={936}>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: q.trap.size ?? 60, color: C.fg, lineHeight: 1.15 }}>{q.trap.main}</div>
            {q.trap.sub && frame >= tSub && <div style={{ marginTop: 26 }}><Line value={q.trap.sub[0]} size={46} /></div>}
          </Card>
        </Appear>
        {(q.trap.wrong || []).map((letter, i) => {
          const opt = q.options.find(([l]) => l === letter);
          return (
            <Row key={letter} y={1010 + i * 130}>
              <div style={{ background: C.bg, padding: 6 }}><Option letter={letter} value={opt[1]} unit="" state="wrong" at={tHit + i * 6} compact /></div>
            </Row>
          );
        })}
        <Sfx at={1} name="whoosh" /><Sfx at={tHit} name="buzz" volume={0.5} />
        {tSub != null && <Sfx at={tSub} name="pop" volume={0.4} />}
      </AbsoluteFill>
    );
  };

  const Answer = ({ scene }) => {
    const frame = useCurrentFrame();
    const W = useW(scene);
    const tS = W(q.answer.stem, 20);
    const tAns = W('ответ', tS + 40);
    const opt = q.options.find(([l]) => l === q.answer.right);
    return (
      <AbsoluteFill>
        <Row y={300}><Visual v={q.answer.visual ?? q.hook.visual} at={2} /></Row>
        <Slam at={tS} y={800} size={q.answer.size ?? 120}>{q.answer.slam}</Slam>
        <Row y={1080}>
          <div style={{ transform: `scale(${punch(frame, tAns, 0.12)})` }}><Option letter={opt[0]} value={opt[1]} unit="" state="right" at={tAns} compact /></div>
        </Row>
        <Sfx at={tS} name="boom" volume={0.5} /><Sfx at={tAns} name="ding" volume={0.5} />
      </AbsoluteFill>
    );
  };

  const Outro = ({ scene }) => <CourseOutro scene={scene} icon={q.icon ?? 'atom'} />;

  return { SCENES: { hook: Hook, engage: Engage, explain: Explain, trap: Trap, answer: Answer, outro: Outro }, TAILS: { engage: 60 } };
};
