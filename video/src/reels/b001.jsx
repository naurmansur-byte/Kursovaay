// B001 «Два жёлтых гороха — откуда зелёный?» — моногибридное скрещивание Aa × Aa (биология, зелёный акцент).
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Card, Kinetic, Label, Option, Pea, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { A, CourseOutro, EngageScene, Slam, useW } from '../scenes.jsx';

const Sign = ({ children, size = 120, color = C.fg }) => (
  <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: 1, color }}>{children}</div>
);

const Hook = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tY, tDown, tG, tQ] = [W('жёлтых', 20), W('потомков', 90), W('зелёный', 110), W('откуда', 150)];
  return (
    <AbsoluteFill>
      <Row y={330} style={{ gap: 40, alignItems: 'center' }}>
        <Pea color="yellow" size={240} at={tY} label="♀" />
        {frame >= tY + 6 && <Sign size={130}>×</Sign>}
        <Pea color="yellow" size={240} at={tY + 6} label="♂" />
      </Row>
      {frame >= tDown && <Row y={720}><Sign size={150} color={C.accent}>↓</Sign></Row>}
      <Row y={880}>
        <div style={{ transform: `scale(${punch(frame, tG, 0.25)})` }}><Pea color="green" size={300} at={tG} /></div>
      </Row>
      <Kinetic at={tQ} y={1220} size={110} rotate={-4} plaque>Откуда?</Kinetic>
      <Sfx at={tY} name="pop" /><Sfx at={tY + 6} name="pop" /><Sfx at={tDown} name="whoosh" /><Sfx at={tG} name="boom" volume={0.55} /><Sfx at={tQ} name="whoosh" />
    </AbsoluteFill>
  );
};

const Engage = ({ scene }) => (
  <EngageScene
    scene={scene}
    unit=""
    questionTex={['\\text{Жёлтый} \\times \\text{жёлтый}', '\\text{Доля зелёных потомков?}']}
    questionSize={52}
    options={[['А', '0\\%'], ['Б', '25\\%'], ['В', '50\\%'], ['Г', '75\\%']]}
  />
);

const Gene = ({ color, tex, text, at }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
    <Pea color={color} size={110} at={at} />
    <TeX tex={tex} size={80} />
    <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 44, color: C.fg }}>{text}</div>
  </div>
);

const Parents = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tA, ta, tP, tH] = [W('жёлтый', 2), W('зелёный', 60), W('оба', 170), W('гетерозиготы', 185)];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={84} rotate={-3}>Кто сильнее?</Kinetic>
      <Appear at={tA} y={420}>
        <Card width={936}>
          <Gene color="yellow" tex={`\\mathrm{${A('A')}}`} text="жёлтый — доминантный" at={tA} />
          {frame >= ta && <div style={{ marginTop: 24 }}><Gene color="green" tex="\mathrm{a}" text="зелёный — рецессивный" at={ta} /></div>}
        </Card>
      </Appear>
      {frame >= tP && (
        <Row y={900}>
          <div style={{ transform: `scale(${punch(frame, tP, 0.2)}) rotate(-3deg)`, background: C.accent, padding: '20px 40px 26px', fontFamily: F.display, fontWeight: 800, fontSize: 92, color: C.fg, whiteSpace: 'nowrap' }}>
            P: ♀Aa × ♂Aa
          </div>
        </Row>
      )}
      <Appear at={tH} y={1140}><Label size={44} color={C.fg}>оба родителя — гетерозиготы</Label></Appear>
      <Sfx at={tA} name="pop" /><Sfx at={ta} name="pop" /><Sfx at={tP} name="boom" volume={0.5} />
    </AbsoluteFill>
  );
};

// Решётка Пеннета 3×3: шапки — гаметы, внутри — генотипы потомков.
const CELL = 270;
const Punnett = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const [tGrid, tGam, tCells] = [W('решётку', 18), W('гамет', 110), W('получаем', 150)];
  const kids = [['AA', 'yellow'], ['Aa', 'yellow'], ['Aa', 'yellow'], ['aa', 'green']];
  const head = (txt, at) => frame >= at && (
    <div style={{ transform: `scale(${enter(frame, at, fps)})`, fontFamily: F.display, fontWeight: 800, fontSize: 96, color: txt === 'A' ? C.fg : C.accent }}>{txt}</div>
  );
  const box = (i, j, child) => (
    <div key={`${i}${j}`} style={{ position: 'absolute', left: j * CELL, top: i * CELL, width: CELL, height: CELL, border: `4px solid ${i && j ? C.fg : 'transparent'}`, background: i && j ? C.card : 'transparent', display: 'grid', placeItems: 'center', boxSizing: 'border-box' }}>{child}</div>
  );
  return (
    <AbsoluteFill>
      <Kinetic at={tGrid} y={240} size={84} rotate={-3} plaque>Решётка Пеннета</Kinetic>
      {frame >= tGrid && (
        <div style={{ position: 'absolute', left: (1080 - 3 * CELL) / 2, top: 440, width: 3 * CELL, height: 3 * CELL, opacity: enter(frame, tGrid, fps) }}>
          {box(0, 0, <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 34, color: C.muted, textAlign: 'center', lineHeight: 1.2 }}>гаметы</div>)}
          {box(0, 1, head('A', tGam))}{box(0, 2, head('a', tGam + 4))}
          {box(1, 0, head('A', tGam + 8))}{box(2, 0, head('a', tGam + 12))}
          {kids.map(([g, c], k) => {
            const at = tCells + k * 7;
            return box(1 + Math.floor(k / 2), 1 + (k % 2), frame >= at && (
              <div style={{ textAlign: 'center' }}>
                <Pea color={c} size={120} at={at} />
                <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 52, color: C.fg }}>{g}</div>
              </div>
            ));
          })}
        </div>
      )}
      <Sfx at={tGrid} name="whoosh" />{[0, 4, 8, 12].map((d) => <Sfx key={d} at={tGam + d} name="tick" volume={0.45} />)}
      {kids.map((_, k) => <Sfx key={k} at={tCells + k * 7} name="pop" volume={0.35} />)}
    </AbsoluteFill>
  );
};

const Trap = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const [tHet, tAlso, tG] = [W('гетерозигота', 40), W('тоже', 75), W('зелёный', 185)];
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${shake(frame, tAlso, 14, 18)}px)` }}>
      <Kinetic at={0} y={240} size={130} rotate={-6} color={C.bg} punchAt={tAlso}>Ловушка</Kinetic>
      <Appear at={tHet} y={480}>
        <Card width={936}>
          <Gene color="yellow" tex="\mathrm{Aa}" text="— тоже жёлтый!" at={tHet} />
          {frame >= tG && <div style={{ marginTop: 28 }}><Gene color="green" tex="\mathrm{aa}" text="— только так зелёный" at={tG} /></div>}
        </Card>
      </Appear>
      <Sfx at={1} name="whoosh" /><Sfx at={tAlso} name="buzz" volume={0.5} /><Sfx at={tG} name="pop" />
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const W = useW(scene);
  const [t4, tQ, tAns] = [W('одна', 40), W('двадцать', 70), W('ответ', 130)];
  return (
    <AbsoluteFill>
      <Row y={300} style={{ gap: 30 }}>
        {['yellow', 'yellow', 'yellow', 'green'].map((c, i) => <Pea key={i} color={c} size={170} at={4 + i * 5} />)}
      </Row>
      <Slam at={t4} y={620} size={150}><TeX tex="\tfrac{1}{4}" size={170} /></Slam>
      <Appear at={tQ} y={920}><TeX tex={`= ${A('25\\%')}\\ \\text{зелёных}`} size={84} /></Appear>
      <Row y={1120}><Option letter="Б" value="25\%" unit="" state="right" at={tAns} compact /></Row>
      {[0, 1, 2, 3].map((i) => <Sfx key={i} at={4 + i * 5} name="pop" volume={0.3} />)}
      <Sfx at={t4} name="boom" volume={0.5} /><Sfx at={tAns} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Outro = ({ scene }) => <CourseOutro scene={scene} icon="dna" />;

export const SCENES = { hook: Hook, engage: Engage, parents: Parents, punnett: Punnett, trap: Trap, answer: Answer, outro: Outro };
export const TAILS = { engage: 60, punnett: 14 };
