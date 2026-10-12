// R002 «Формула по продуктам сгорания» (сложная, авторская). Решение — content/reels/R002-combustion-formula/solution.md
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Card, Flame, Kinetic, Label, Option, Row, Sfx, TeX, punch, shake } from '../kit.jsx';
import { A, CourseOutro, EngageScene, Slam, useW } from '../scenes.jsx';

const Hook = ({ scene }) => {
  const W = useW(scene);
  const t1 = W('сгорело', 2);
  const t2 = W('какая', 40);
  return (
    <AbsoluteFill>
      <Kinetic at={t1} y={270} size={220} rotate={-5}>4,6 г</Kinetic>
      <Appear at={W('вещества', 20)} y={540}>
        <TeX tex="\to\ \mathrm{CO_2}\ 8{,}8\,\text{г} + \mathrm{H_2O}\ 5{,}4\,\text{г}" size={66} />
      </Appear>
      <Kinetic at={t2} y={720} size={100} rotate={-4} from="right" plaque punchAt={W('формула', t2 + 10)}>
        Какая формула?
      </Kinetic>
      <Row y={960}>
        <Flame size={330} at={t1 + 4} />
      </Row>
      <Sfx at={t1} name="whoosh" />
      <Sfx at={t2} name="whoosh" />
      <Sfx at={W('формула', t2 + 10)} name="pop" volume={0.45} />
    </AbsoluteFill>
  );
};

const Engage = ({ scene }) => (
  <EngageScene
    scene={scene}
    unit=""
    questionTex={[
      'm = 4{,}6\\,\\text{г}\\quad D_{\\mathrm{H_2}} = 23',
      '\\mathrm{CO_2}\\!: 8{,}8\\,\\text{г}\\quad \\mathrm{H_2O}\\!: 5{,}4\\,\\text{г}',
    ]}
    options={[
      ['А', '\\mathrm{C_2H_6}'],
      ['Б', '\\mathrm{C_2H_6O}'],
      ['В', '\\mathrm{CH_4O}'],
      ['Г', '\\mathrm{C_3H_8}'],
    ]}
  />
);

const Atoms = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tC = W('углерод', 4);
  const tC2 = W('две', 40);
  const tH = W('водород', 60);
  const tH2 = W('шесть', 90);
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={80} rotate={-3}>Куда ушли атомы</Kinetic>
      <Appear at={tC} y={430}>
        <Card width={936}>
          <Label>Углерод → CO₂</Label>
          <div style={{ marginTop: 14, transform: `scale(${punch(frame, tC2, 0.08)})`, transformOrigin: 'left center' }}>
            <TeX tex={`n(\\mathrm{C}) = \\dfrac{8{,}8}{44} = ${frame >= tC2 ? A('0{,}2') : '\\;?'}\\ \\text{моль}`} size={66} />
          </div>
        </Card>
      </Appear>
      <Appear at={tH} y={800}>
        <Card width={936}>
          <Label>Водород → H₂O · в молекуле воды 2 атома H</Label>
          <div style={{ marginTop: 14, transform: `scale(${punch(frame, tH2, 0.08)})`, transformOrigin: 'left center' }}>
            <TeX tex={`n(\\mathrm{H}) = ${A('2')}\\cdot\\dfrac{5{,}4}{18} = ${frame >= tH2 ? A('0{,}6') : '\\;?'}\\ \\text{моль}`} size={66} />
          </div>
        </Card>
      </Appear>
      <Sfx at={tC} name="whoosh" volume={0.25} />
      <Sfx at={tC2} name="pop" />
      <Sfx at={tH} name="whoosh" volume={0.25} />
      <Sfx at={tH2} name="pop" />
    </AbsoluteFill>
  );
};

const Trap = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tCheck = W('проверь', 15);
  const tSum = W('углерод', 40);
  const tOnly = W('три', 70);
  const tO = W('кислород', 110);
  const dx = shake(frame, tCheck, 14, 18) + shake(frame, tOnly, 10, 10);
  const flashOn = frame < 6 ? 1 - frame / 6 : 0;
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${dx}px)` }}>
      <AbsoluteFill style={{ background: C.fg, opacity: flashOn }} />
      <Kinetic at={0} y={240} size={130} rotate={-6} color={C.bg} punchAt={tCheck}>Ловушка</Kinetic>
      <Appear at={tSum} y={470}>
        <Card width={936}>
          <Label color={C.fg}>Проверь массу</Label>
          <div style={{ marginTop: 14 }}>
            <TeX tex={`m(\\mathrm{C}) + m(\\mathrm{H}) = 2{,}4 + 0{,}6 = ${frame >= tOnly ? A('3{,}0') : '\\;?'}\\,\\text{г}`} size={48} />
          </div>
          {frame >= tOnly && (
            <div style={{ marginTop: 10, transform: `scale(${punch(frame, tOnly, 0.1)})`, transformOrigin: 'left center' }}>
              <TeX tex={`3{,}0 \\ne 4{,}6\\ !`} size={64} />
            </div>
          )}
          {frame >= tO && (
            <div style={{ marginTop: 10 }}>
              <TeX tex={`m(\\mathrm{O}) = 4{,}6 - 3{,}0 = 1{,}6\\,\\text{г}`} size={58} />
              <TeX tex={`n(\\mathrm{O}) = \\dfrac{1{,}6}{16} = ${A('0{,}1')}\\ \\text{моль}`} size={58} />
            </div>
          )}
        </Card>
      </Appear>
      <Row y={1200}>
        <div style={{ background: C.bg, padding: 6 }}>
          <Option letter="А" value="\mathrm{C_2H_6}" unit="" state="wrong" at={tO} compact />
        </div>
      </Row>
      <Sfx at={1} name="whoosh" />
      <Sfx at={tCheck} name="buzz" volume={0.5} />
      <Sfx at={tO} name="pop" />
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tRatio = W('два', 10);
  const tF = W('формула', 50);
  const tM = W('сорок', 90);
  const tAns = W('ответ', tM + 30);
  return (
    <AbsoluteFill>
      <Appear at={2} y={270}>
        <TeX tex="\mathrm{C : H : O} = 0{,}2 : 0{,}6 : 0{,}1" size={70} />
      </Appear>
      <Appear at={tRatio} y={380}>
        <div style={{ transform: `scale(${punch(frame, tRatio, 0.12)})` }}>
          <TeX tex={`= ${A('2 : 6 : 1')}`} size={92} />
        </div>
      </Appear>
      <Slam at={tF} y={580} size={150}>
        <TeX tex="\mathrm{C_2H_6O}" size={170} />
      </Slam>
      <Appear at={tM} y={900}>
        <TeX tex={`M = 24 + 6 + 16 = ${A('46')} = 2\\cdot 23\\ \\checkmark`} size={50} />
      </Appear>
      <Row y={1060}>
        <Option letter="Б" value="\mathrm{C_2H_6O}" unit="" state="right" at={tAns} compact />
      </Row>
      <Sfx at={tRatio} name="pop" />
      <Sfx at={tF} name="boom" volume={0.55} />
      <Sfx at={tAns} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Outro = ({ scene }) => <CourseOutro scene={scene} />;

export const SCENES = { hook: Hook, engage: Engage, atoms: Atoms, trap: Trap, answer: Answer, outro: Outro };
export const TAILS = { engage: 60 };
