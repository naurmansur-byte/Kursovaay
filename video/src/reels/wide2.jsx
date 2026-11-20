// Шаблон YouTube 16:9, версия 2 (Мансур 20.11.2026: 8–10 минут, тёмный стиль, больше деталей, сильнее монтаж и захват внимания).
// hook → title → p1…pN (теория, можно с рисунком из конспекта) → (q, e, t, a) × N задач → sum → cta.
// Отличия от wide.jsx: крючок в первые секунды, рисунки справа от теории с медленным наездом, счётчик «Теория 2/6 · Задача 3/5»,
// любое число задач, концовка без даты старта. Тайминги — по словам озвучки: [текст, стем, запасной кадр, красная?].
import React from 'react';
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import katex from 'katex';
import { C, F } from '../theme.js';
import { Appear, Atom, Card, Dna, Kinetic, Label, Option, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { Slam, TopicIntro, useW } from '../scenes.jsx';

const Abs = ({ x, y, children, style }) => <div style={{ position: 'absolute', left: x, top: y, ...style }}>{children}</div>;

const Mixed = ({ value, size, color, wrap }) => (
  <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: size, lineHeight: 1.25, color, whiteSpace: wrap ? 'normal' : 'nowrap' }}>
    {value.split(/\$([^$]+)\$/).map((part, i) =>
      i % 2 ? (
        <span key={i} style={{ fontSize: '1.1em', fontWeight: 400, whiteSpace: 'nowrap' }} dangerouslySetInnerHTML={{ __html: katex.renderToString(part, { throwOnError: false, strict: false, output: 'html' }) }} />
      ) : (
        <span key={i}>{part}</span>
      )
    )}
  </div>
);

const Line = ({ value, size = 54, color = C.fg, wrap = false }) =>
  value.startsWith('$') && value.indexOf('$', 1) === -1 ? (
    <TeX tex={value.slice(1)} size={size + 6} color={color} />
  ) : value.includes('$') ? (
    <Mixed value={value} size={size} color={color} wrap={wrap} />
  ) : (
    <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: size, lineHeight: 1.2, color, whiteSpace: wrap ? 'normal' : 'nowrap' }}>{value}</div>
  );

const Chip = ({ children, red, at }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  return <div style={{ transform: `scale(${enter(frame, at, fps)})`, padding: '14px 28px', background: red ? C.accent : C.bg, border: `4px solid ${red ? C.accent : C.fg}`, fontFamily: F.body, fontWeight: 800, fontSize: 40, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>{children}</div>;
};

// Счётчик в правом верхнем углу: где зритель сейчас.
const Badge = ({ text }) => (
  <div style={{ position: 'absolute', right: 80, top: 40, padding: '8px 20px 10px', border: `3px solid ${C.fg}`, fontFamily: F.body, fontWeight: 800, fontSize: 30, letterSpacing: '0.12em', color: C.fg, background: C.bg }}>{text}</div>
);

// Рисунок из конспекта на белой карточке с медленным наездом.
const Pic = ({ src, at, width = 820, x, y }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 16, stiffness: 140, mass: 0.8 });
  const zoom = 1 + Math.min(0.06, (frame - at) / 3000);
  return (
    <Abs x={x} y={y} style={{ width, opacity: p, transform: `translateX(${(1 - p) * 140}px) rotate(${(1 - p) * 2}deg)` }}>
      <div style={{ background: '#fff', padding: 18, boxShadow: `14px 14px 0 ${C.accent}`, overflow: 'hidden' }}>
        <Img src={staticFile(src)} style={{ width: '100%', display: 'block', transform: `scale(${zoom})`, transformOrigin: 'center' }} />
      </div>
    </Abs>
  );
};

const Rows = ({ rows, times, size, gap = 24, wrap = false }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ display: 'grid', gap }}>
      {rows.map(([value, , , red], i) =>
        frame < times[i] ? null : (
          <div key={i} style={{ transform: `scale(${0.92 + 0.08 * enter(frame, times[i], 30)})`, transformOrigin: 'left center', borderLeft: `10px solid ${red ? C.accent : C.faint}`, paddingLeft: 26, background: red && frame - times[i] < 24 ? `${C.accent}22` : 'transparent' }}>
            <Line value={value} size={size} wrap={wrap} />
          </div>
        )
      )}
    </div>
  );
};

export const makeWide2 = (cfg) => {
  const N = cfg.tasks.length;
  const P = (cfg.points || []).length;

  // Крючок: 2–3 строки крупно + рисунок/вопрос + плашка «досмотри».
  const Hook = ({ scene }) => {
    const frame = useCurrentFrame();
    const W = useW(scene);
    const h = cfg.hook;
    const times = h.lines.map(([, stem, fb]) => W(stem, fb));
    const tT = W(h.tease[1], h.tease[2]);
    return (
      <AbsoluteFill>
        {h.lines.map(([text, , , red], i) => (
          <Kinetic key={i} at={times[i]} y={200 + i * 150} size={i === 0 ? 96 : 84} rotate={i % 2 ? 2 : -3} plaque={!!red} punchAt={times[i]}>{text}</Kinetic>
        ))}
        {h.img && <Pic src={h.img[0]} at={W(h.img[1], h.img[2])} x={1040} y={660} width={720} />}
        {frame >= tT && (
          <Abs x={140} y={700}>
            <div style={{ transform: `scale(${punch(frame, tT, 0.2)}) rotate(-2deg)`, transformOrigin: 'left center', padding: '18px 34px', background: C.fg, color: C.bg, font: `800 48px ${F.display}`, whiteSpace: 'nowrap' }}>{h.tease[0]}</div>
          </Abs>
        )}
        {times.map((t, i) => <Sfx key={i} at={t} name={i === 0 ? 'boom' : 'whoosh'} volume={0.4} />)}
        <Sfx at={tT} name="ding" volume={0.45} />
      </AbsoluteFill>
    );
  };

  const Title = ({ scene }) => <TopicIntro scene={scene} tag={cfg.tag} title={cfg.title} plaque={cfg.plaque} icon={cfg.icon} items={cfg.items} />;

  const Question = (n) => ({ scene }) => {
    const frame = useCurrentFrame();
    const q = cfg.tasks[n - 1];
    const left = interpolate(frame, [20, scene.dur - 2], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    const R = 34;
    return (
      <AbsoluteFill>
        <Badge text={`ЗАДАЧА ${n}/${N}`} />
        <Kinetic at={0} y={150} size={74} rotate={-3} plaque>{`Задача ${n} из ${N}`}</Kinetic>
        <Appear at={2} y={262}>
          <Card width={1560} style={{ padding: q.cols === 1 ? '30px 44px' : undefined }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Label>ЕНТ · выбери один ответ · поставь на паузу ⏸</Label>
              <svg width={2 * R + 12} height={2 * R + 12} viewBox={`${-R - 6} ${-R - 6} ${2 * R + 12} ${2 * R + 12}`}>
                <circle r={R} fill="none" stroke={C.faint} strokeWidth="8" />
                <circle r={R} fill="none" stroke={C.accent} strokeWidth="8" strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - left)} transform="rotate(-90)" />
              </svg>
            </div>
            <div style={{ marginTop: 22, display: 'grid', gap: 8 }}>
              {q.question.map((t) => <TeX key={t} tex={t} size={q.questionSize ?? 56} />)}
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: q.cols === 1 ? '1fr' : '1fr 1fr', gap: q.cols === 1 ? 8 : 20, marginTop: q.cols === 1 ? 18 : 30 }}>
              {q.options.map(([l, v], i) => <Option key={l} letter={l} value={v} unit="" at={6 + i * 3} compact={q.cols === 1} />)}
            </div>
          </Card>
        </Appear>
        {[6, 9, 12, 15].map((t) => <Sfx key={t} at={t} name="tick" volume={0.45} />)}
      </AbsoluteFill>
    );
  };

  const Explain = (n) => ({ scene }) => {
    const W = useW(scene);
    const q = cfg.tasks[n - 1];
    const times = q.explain.rows.map(([, stem, fb]) => W(stem, fb));
    const img = q.explain.img;
    return (
      <AbsoluteFill>
        <Badge text={`ЗАДАЧА ${n}/${N}`} />
        <Kinetic at={0} y={175} size={80} rotate={-3} plaque>{q.explain.title}</Kinetic>
        {img ? (
          <>
            <Abs x={80} y={310} style={{ width: 960 }}><Card width={960} style={{ padding: '30px 38px' }}><Rows rows={q.explain.rows} times={times} size={42} gap={18} wrap /></Card></Abs>
            <Pic src={img[0]} at={W(img[1], img[2])} x={1090} y={320} width={760} />
          </>
        ) : (
          <Appear at={2} y={310}><Card width={1500}><Rows rows={q.explain.rows} times={times} size={50} gap={26} wrap /></Card></Appear>
        )}
        {times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
      </AbsoluteFill>
    );
  };

  const Trap = (n) => ({ scene }) => {
    const frame = useCurrentFrame();
    const W = useW(scene);
    const q = cfg.tasks[n - 1];
    const tHit = W(q.trap.stem, 20);
    return (
      <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, tHit, 14, 18)}px)` }}>
        <Kinetic at={0} y={160} size={110} rotate={-5} color={C.bg} punchAt={tHit}>Ловушка</Kinetic>
        <Appear at={8} y={340}>
          <Card width={1400}>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 58, color: C.fg, lineHeight: 1.15 }}>{q.trap.main}</div>
          </Card>
        </Appear>
        <Row y={700} style={{ gap: 24 }}>
          {(q.trap.wrong || []).map((letter, i) => {
            const opt = q.options.find(([l]) => l === letter);
            return <div key={letter} style={{ background: C.bg, padding: 6 }}><Option letter={letter} value={opt[1]} unit="" state="wrong" at={tHit + i * 6} compact /></div>;
          })}
        </Row>
        <Sfx at={1} name="whoosh" /><Sfx at={tHit} name="buzz" volume={0.5} />
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
        <Badge text={`ЗАДАЧА ${n}/${N}`} />
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
    const [tC, tH, tOn, tS, tD, tSub] = [W('химбио', 80), W('химия', 112), W('онлайн', 149), W('запись', 190), W('директ', 260), W('подпишись', 340)];
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
          <Chip at={tH} red>химия + биология</Chip><Chip at={tOn}>онлайн</Chip><Chip at={tS} red>запись открыта</Chip>
        </Row>
        <Appear at={tD - 20} y={650}><div style={{ font: `700 44px ${F.body}`, color: C.muted }}>Запись — в директ Instagram</div></Appear>
        <Kinetic at={tD} y={720} size={96} rotate={-2}>@himbio.prosto</Kinetic>
        {frame >= tSub && (
          <Abs x={1290} y={850}>
            <div style={{ transform: `scale(${punch(frame, tSub, 0.25)}) rotate(4deg)`, padding: '22px 44px', background: C.accent, borderRadius: 60, font: `800 40px ${F.display}`, color: '#fff', whiteSpace: 'nowrap' }}>ПОДПИСАТЬСЯ</div>
          </Abs>
        )}
        <Sfx at={2} name="whoosh" /><Sfx at={tC} name="whoosh" />{[tH, tOn, tS].map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
        <Sfx at={tD} name="whoosh" /><Sfx at={tSub} name="ding" volume={0.5} />
      </AbsoluteFill>
    );
  };

  // Теория: заголовок, строки по словам; если есть рисунок — строки слева, рисунок справа.
  const Point = (n) => ({ scene }) => {
    const W = useW(scene);
    const p = cfg.points[n - 1];
    const times = p.rows.map(([, stem, fb]) => W(stem, fb));
    return (
      <AbsoluteFill>
        <Badge text={`ТЕОРИЯ ${n}/${P}`} />
        <Kinetic at={0} y={150} size={76} rotate={-3} plaque>{p.title}</Kinetic>
        {p.img ? (
          <>
            <Abs x={80} y={290} style={{ width: 960 }}><Card width={960} style={{ padding: '28px 36px' }}><Rows rows={p.rows} times={times} size={38} gap={14} wrap /></Card></Abs>
            <Pic src={p.img[0]} at={W(p.img[1], p.img[2])} x={1090} y={300} width={760} />
          </>
        ) : (
          <Appear at={2} y={300}><Card width={1600}><Rows rows={p.rows} times={times} size={p.size ?? 54} gap={p.gap ?? 24} wrap /></Card></Appear>
        )}
        <Sfx at={1} name="whoosh" />
        {times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.3} />)}
      </AbsoluteFill>
    );
  };

  const Summary = ({ scene }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();
    const W = useW(scene);
    const sm = cfg.summary;
    const times = sm.rows.map(([, stem, fb]) => W(stem, fb));
    const tN = W(sm.next[1], times[times.length - 1] + 60);
    return (
      <AbsoluteFill>
        <Badge text="ИТОГ" />
        <Kinetic at={0} y={150} size={90} rotate={-3} plaque>Итог</Kinetic>
        <div style={{ position: 'absolute', left: 160, top: 300, width: 1600, display: 'grid', gap: 22 }}>
          {sm.rows.map(([text], i) => {
            const at = times[i];
            if (frame < at) return null;
            const pr = enter(frame, at, fps);
            return (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 26, opacity: pr, transform: `translateX(${(1 - pr) * 120}px)` }}>
                <div style={{ width: 64, height: 64, flex: 'none', background: C.accent, display: 'grid', placeItems: 'center', fontFamily: F.display, fontWeight: 800, fontSize: 34, color: C.fg }}>{i + 1}</div>
                <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 46, lineHeight: 1.15, color: C.fg }}>{text}</div>
              </div>
            );
          })}
        </div>
        {frame >= tN && (
          <Abs x={160} y={800}>
            <div style={{ transform: `scale(${punch(frame, tN, 0.2)})`, transformOrigin: 'left center', padding: '18px 34px', border: `4px solid ${C.fg}`, font: `800 42px ${F.body}`, color: C.fg, whiteSpace: 'nowrap' }}>{sm.next[0]}</div>
          </Abs>
        )}
        <Sfx at={1} name="whoosh" />
        {times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.35} />)}
        <Sfx at={tN} name="ding" volume={0.45} />
      </AbsoluteFill>
    );
  };

  const SCENES = { hook: Hook, title: Title, cta: Cta, sum: Summary };
  const TAILS = { hook: 20, title: 24, cta: 60, sum: 30 };
  (cfg.points || []).forEach((_, i) => {
    SCENES[`p${i + 1}`] = Point(i + 1);
    TAILS[`p${i + 1}`] = 30;
  });
  for (let n = 1; n <= N; n++) {
    SCENES[`q${n}`] = Question(n);
    SCENES[`e${n}`] = Explain(n);
    SCENES[`t${n}`] = Trap(n);
    SCENES[`a${n}`] = Answer(n);
    TAILS[`q${n}`] = 110;  // пауза «подумай» с таймером
    TAILS[`e${n}`] = 20;
    TAILS[`a${n}`] = 24;
    TAILS[`t${n}`] = 16;
  }
  return { SCENES, TAILS };
};
