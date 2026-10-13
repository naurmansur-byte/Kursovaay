// B003 «Сколько хромосом в яйцеклетке?» — мейоз: 2n = 46 → n = 23 (биология, зелёный акцент).
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Card, Kinetic, Label, Option, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { A, CourseOutro, EngageScene, Slam, useW } from '../scenes.jsx';

// Хромосома в форме X (две хроматиды); при появлении слегка покачивается.
const Chromo = ({ size = 90, color = C.fg, rot = 0, at = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 11, stiffness: 180 });
  const sway = Math.sin((frame - at) / 9 + rot) * 4;
  return (
    <svg width={size} height={size} viewBox="-50 -50 100 100" style={{ transform: `scale(${p}) rotate(${rot + sway}deg)` }}>
      <rect x="-11" y="-46" width="22" height="92" rx="11" fill={color} transform="rotate(18)" />
      <rect x="-11" y="-46" width="22" height="92" rx="11" fill={color} transform="rotate(-18)" />
      <circle r="9" fill={C.bg} />
    </svg>
  );
};

// Клетка-кружок с подписью набора внутри.
const CellDot = ({ size, label, at, color = C.fg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 12, stiffness: 160 });
  return (
    <div style={{ width: size, height: size, borderRadius: '50%', border: `8px solid ${color}`, background: C.card, display: 'grid', placeItems: 'center', transform: `scale(${p})`, boxSizing: 'border-box' }}>
      <TeX tex={label} size={size * 0.2} />
    </div>
  );
};

const SCATTER = [[130, 360, -20], [330, 300, 15], [760, 320, 30], [950, 430, -10], [110, 700, 40], [970, 720, -35], [110, 910, 10], [970, 900, 25]];

const Hook = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [t46, tQ] = [W('сорок', 42), W('яйцеклетке', 130)];
  return (
    <AbsoluteFill>
      {SCATTER.map(([x, y, r], i) => (
        <div key={i} style={{ position: 'absolute', left: x - 50, top: y - 50 }}><Chromo size={110} rot={r} at={4 + i * 3} color={i % 3 ? C.fg : C.accent} /></div>
      ))}
      <Row y={600}><div style={{ transform: `scale(${punch(frame, t46, 0.2)})`, fontFamily: F.display, fontWeight: 800, fontSize: 320, color: C.fg, lineHeight: 1 }}>{frame >= t46 ? '46' : ''}</div></Row>
      <Appear at={t46 + 6} y={950}><Label size={46} color={C.fg}>хромосом в клетке тела</Label></Appear>
      <Kinetic at={tQ} y={1130} size={100} rotate={-4} plaque>А в яйцеклетке?</Kinetic>
      {SCATTER.map((_, i) => <Sfx key={i} at={4 + i * 3} name="tick" volume={0.3} />)}
      <Sfx at={t46} name="boom" volume={0.55} /><Sfx at={tQ} name="whoosh" />
    </AbsoluteFill>
  );
};

const Engage = ({ scene }) => (
  <EngageScene
    scene={scene}
    unit=""
    questionSize={50}
    questionTex={['\\text{В клетке тела — } 46 \\text{ хромосом}', '\\text{Сколько в яйцеклетке?}']}
    options={[['А', '92'], ['Б', '46'], ['В', '23'], ['Г', '22']]}
  />
);

const Meiosis = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tM, tHalf, t2n, tN] = [W('мейоз', 87), W('вдвое', 133), W('диплоидного', 158), W('гаплоидный', 222)];
  return (
    <AbsoluteFill>
      <Kinetic at={2} y={240} size={110} rotate={-4} plaque>Мейоз</Kinetic>
      <Row y={430}><CellDot size={300} label={`2n = 46`} at={t2n - 10} /></Row>
      {frame >= tM && (
        <Row y={760}><div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 64, color: C.accent }}>↓ ÷ 2</div></Row>
      )}
      <Row y={870}><CellDot size={260} label={`n = ${A('23')}`} at={tN} color={C.accent} /></Row>
      <Appear at={tHalf} y={1160}><TeX tex={`2n \\to ${A('n')}`} size={84} /></Appear>
      <Sfx at={2} name="whoosh" /><Sfx at={t2n - 10} name="pop" /><Sfx at={tM} name="whoosh" volume={0.3} /><Sfx at={tN} name="pop" /><Sfx at={tHalf} name="tick" volume={0.5} />
    </AbsoluteFill>
  );
};

const Trap = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [t22, tX, tAll] = [W('двадцать', 47), W('половая', 168), W('всего', 239)];
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, t22, 14, 18)}px)` }}>
      <Kinetic at={0} y={240} size={130} rotate={-6} color={C.bg} punchAt={t22}>Ловушка</Kinetic>
      <Appear at={t22} y={480}>
        <Card width={936}>
          <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'flex-end', gap: 30 }}>
            <div style={{ textAlign: 'center' }}>
              <TeX tex="22" size={104} />
              <Label color={C.fg}>аутосомы</Label>
            </div>
            {frame >= tX && <div style={{ textAlign: 'center' }}><TeX tex="+\ \mathrm{X}" size={104} /><Label color={C.fg}>половая</Label></div>}
            {frame >= tAll && <div style={{ textAlign: 'center', transform: `scale(${punch(frame, tAll, 0.2)})` }}><TeX tex="=\ 23" size={104} /><Label color={C.fg}>всего</Label></div>}
          </div>
        </Card>
      </Appear>
      <Row y={1000}>
        <div style={{ background: C.bg, padding: 6 }}><Option letter="Г" value="22" unit="" state="wrong" at={t22} compact /></div>
      </Row>
      <Sfx at={1} name="whoosh" /><Sfx at={t22} name="buzz" volume={0.5} /><Sfx at={tX} name="pop" /><Sfx at={tAll} name="ding" volume={0.45} />
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const W = useW(scene);
  const [tF, tSum, tAns] = [W('оплодотворении', 12), W('сорок', 93), W('ответ', 135)];
  return (
    <AbsoluteFill>
      <Kinetic at={tF} y={240} size={84} rotate={-3}>Оплодотворение</Kinetic>
      <Row y={430} style={{ gap: 30, alignItems: 'center' }}>
        <CellDot size={220} label="n" at={tF + 4} color={C.accent} />
        <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 100, color: C.fg }}>+</div>
        <CellDot size={150} label="n" at={tF + 10} />
      </Row>
      <Slam at={tSum} y={760} size={110}><TeX tex="23 + 23 = 46" size={110} /></Slam>
      <Row y={1080}><Option letter="В" value="23" unit="" state="right" at={tAns} compact /></Row>
      <Sfx at={tF} name="whoosh" /><Sfx at={tSum} name="boom" volume={0.5} /><Sfx at={tAns} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Outro = ({ scene }) => <CourseOutro scene={scene} icon="dna" />;

export const SCENES = { hook: Hook, engage: Engage, meiosis: Meiosis, trap: Trap, answer: Answer, outro: Outro };
export const TAILS = { engage: 60 };
