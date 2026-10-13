// B002 «Нет ядра — нет ДНК?» — прокариотическая клетка: ДНК в нуклеоиде (биология, зелёный акцент).
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Card, Kinetic, Option, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { CourseOutro, EngageScene, Slam, useW } from '../scenes.jsx';

// Бактериальная клетка: стенка, мембрана, рибосомы, кольцевая ДНК (нуклеоид), плазмида. hotDna — подсветить ДНК.
const RIBO = [[150, 120], [230, 300], [330, 170], [560, 110], [690, 280], [760, 150], [470, 330], [120, 250], [640, 360], [400, 90], [800, 260], [280, 380]];
const Bacterium = ({ width = 900, at = 0, hotDna, showNucleus }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 13, stiffness: 140 });
  const t = (frame - at) / fps;
  const hot = hotDna != null && frame >= hotDna;
  const dna = Array.from({ length: 49 }, (_, k) => {
    const a = (k / 48) * Math.PI * 2;
    const r = 120 + 28 * Math.sin(a * 6 + t * 1.5) + 12 * Math.cos(a * 11);
    return `${(450 + r * 1.35 * Math.cos(a)).toFixed(1)} ${(240 + r * 0.62 * Math.sin(a)).toFixed(1)}`;
  });
  return (
    <svg width={width} height={width * 0.55} viewBox="0 0 900 490" style={{ transform: `scale(${p})` }}>
      <rect x="10" y="10" width="880" height="470" rx="235" fill={C.card} stroke={C.fg} strokeWidth="12" />
      <rect x="34" y="34" width="832" height="422" rx="211" fill="none" stroke={C.muted} strokeWidth="5" strokeDasharray="14 10" />
      {RIBO.map(([x, y]) => <circle key={`${x}${y}`} cx={x} cy={y + 20} r="11" fill={C.fg} opacity="0.55" />)}
      <path d={`M${dna.join(' L')} Z`} fill="none" stroke={hot ? C.accent : C.fg} strokeWidth={hot ? 12 : 8} strokeLinejoin="round" style={{ filter: hot ? `drop-shadow(0 0 14px ${C.accent})` : undefined }} />
      <circle cx="760" cy="370" r="34" fill="none" stroke={C.accent} strokeWidth="7" />
      {showNucleus && (
        <g>
          <circle cx="450" cy="245" r="70" fill="none" stroke={C.fg} strokeWidth="6" strokeDasharray="10 8" />
          <text x="450" y="265" textAnchor="middle" fontFamily={F.display} fontWeight="800" fontSize="64" fill={C.fg}>?</text>
        </g>
      )}
    </svg>
  );
};

const Hook = ({ scene }) => {
  const W = useW(scene);
  const [tB, tN, tD] = [W('бактерии', 6), W('ядра', 28), W('днк', 112)];
  return (
    <AbsoluteFill>
      <Row y={300}><Bacterium width={936} at={tB} showNucleus /></Row>
      <Kinetic at={tN} y={900} size={120} rotate={-4}>Нет ядра —</Kinetic>
      <Kinetic at={tD} y={1060} size={104} rotate={-4} plaque from="right" punchAt={tD + 4}>нет ДНК?</Kinetic>
      <Sfx at={tB} name="pop" /><Sfx at={tN} name="whoosh" /><Sfx at={tD} name="boom" volume={0.55} />
    </AbsoluteFill>
  );
};

const OPTIONS = [
  ['А', '\\text{ДНК нет}'],
  ['Б', '\\text{ДНК в ядре}'],
  ['В', '\\text{ДНК в нуклеоиде}'],
  ['Г', '\\text{рибосом нет}'],
];

const Engage = ({ scene }) => (
  <EngageScene scene={scene} unit="" cols={1} questionSize={52} questionTex={['\\text{Что верно о бактерии?}']} options={OPTIONS} />
);

const Tag = ({ at, children, red }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  return (
    <div style={{ transform: `scale(${enter(frame, at, fps)})`, padding: '12px 26px', border: `4px solid ${red ? C.accent : C.fg}`, background: red ? C.accent : C.bg, fontFamily: F.body, fontWeight: 800, fontSize: 40, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>{children}</div>
  );
};

const Cell = ({ scene }) => {
  const W = useW(scene);
  const [tP, tN, tD, tC, tNu] = [W('прокариот', 30), W('ядра', 91), W('днк', 117), W('цитоплазме', 188), W('нуклеоида', 212)];
  return (
    <AbsoluteFill>
      <Kinetic at={tP} y={240} size={100} rotate={-3} plaque>Прокариот</Kinetic>
      <Row y={430}><Bacterium width={936} at={2} hotDna={tD} /></Row>
      <Row y={1000} style={{ gap: 16, flexWrap: 'wrap' }}>
        <Tag at={tN}>ядра нет ✗</Tag>
        <Tag at={tD} red>ДНК есть ✓</Tag>
      </Row>
      <Row y={1110} style={{ gap: 16 }}>
        <Tag at={tC}>в цитоплазме</Tag>
        <Tag at={tNu} red>нуклеоид</Tag>
      </Row>
      <Sfx at={tP} name="whoosh" /><Sfx at={tN} name="tick" volume={0.5} /><Sfx at={tD} name="pop" /><Sfx at={tC} name="tick" volume={0.5} /><Sfx at={tNu} name="pop" />
    </AbsoluteFill>
  );
};

const Trap = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tNot, tR] = [W('не', 78), W('рибосомы', 157)];
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, tNot, 14, 18)}px)` }}>
      <Kinetic at={0} y={240} size={130} rotate={-6} color={C.bg} punchAt={tNot}>Ловушка</Kinetic>
      <Appear at={8} y={470}>
        <Card width={936}>
          <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 64, color: C.fg, lineHeight: 1.15 }}>нет ядра ≠ нет ДНК</div>
          {frame >= tR && <div style={{ marginTop: 26, fontFamily: F.body, fontWeight: 800, fontSize: 48, color: C.fg }}>рибосомы есть → синтез белка</div>}
        </Card>
      </Appear>
      <Row y={1000}>
        <div style={{ background: C.bg, padding: 6 }}><Option letter="А" value={OPTIONS[0][1]} unit="" state="wrong" at={tNot} compact /></div>
      </Row>
      {frame >= tR && (
        <Row y={1130}>
          <div style={{ background: C.bg, padding: 6 }}><Option letter="Г" value={OPTIONS[3][1]} unit="" state="wrong" at={tR} compact /></div>
        </Row>
      )}
      <Sfx at={1} name="whoosh" /><Sfx at={tNot} name="buzz" volume={0.5} /><Sfx at={tR} name="buzz" volume={0.35} />
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tD, tAns] = [W('днк', 26), W('ответ', 130)];
  return (
    <AbsoluteFill>
      <Row y={280}><Bacterium width={760} at={2} hotDna={tD} /></Row>
      <Slam at={tD} y={780} size={68}>ДНК в нуклеоиде</Slam>
      <Row y={1080}><div style={{ transform: `scale(${punch(frame, tAns, 0.12)})` }}><Option letter="В" value={OPTIONS[2][1]} unit="" state="right" at={tAns} compact /></div></Row>
      <Sfx at={tD} name="boom" volume={0.5} /><Sfx at={tAns} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Outro = ({ scene }) => <CourseOutro scene={scene} icon="dna" />;

export const SCENES = { hook: Hook, engage: Engage, cell: Cell, trap: Trap, answer: Answer, outro: Outro };
export const TAILS = { engage: 60 };
