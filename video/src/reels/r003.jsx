// R003 «Сколько атомов кислорода в 3H2SO4?» — индекс и коэффициент (лёгкая, авторская).
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { Appear, Atom, Card, Kinetic, Label, Option, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { A, CourseOutro, EngageScene, Slam, useW } from '../scenes.jsx';

const FORMULA = `${A('3')}\\mathrm{H_2SO}_{${A('4')}}`;

const Hook = ({ scene }) => {
  const W = useW(scene);
  const t1 = W('три', 2);
  const t2 = W('сколько', 40);
  return (
    <AbsoluteFill>
      <Appear at={t1} y={260}>
        <TeX tex={FORMULA} size={220} />
      </Appear>
      <Kinetic at={t2} y={640} size={100} rotate={-4} from="right" plaque punchAt={W('кислород', t2 + 10)}>
        Сколько атомов O?
      </Kinetic>
      <Row y={900}>
        <Atom size={320} at={t2} speed={1.6} />
      </Row>
      <Sfx at={t1} name="whoosh" />
      <Sfx at={t2} name="whoosh" />
      <Sfx at={W('кислород', t2 + 10)} name="pop" volume={0.45} />
    </AbsoluteFill>
  );
};

const Engage = ({ scene }) => (
  <EngageScene
    scene={scene}
    unit=""
    questionTex={['\\text{Сколько атомов кислорода}', '\\text{в } 3\\mathrm{H_2SO_4}?']}
    options={[
      ['А', '4'],
      ['Б', '7'],
      ['В', '12'],
      ['Г', '21'],
    ]}
  />
);

const Explain = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tK = W('коэффициент', 30);
  const tI = W('индекс', 90);
  const tEach = W('каждой', 130);
  return (
    <AbsoluteFill>
      <Appear at={2} y={240}>
        <TeX tex={FORMULA} size={190} />
      </Appear>
      <Appear at={tK} y={540}>
        <Card width={936} style={{ padding: '24px 36px' }}>
          <TeX tex={`${A('3')} = \\text{коэффициент: 3 молекулы}`} size={54} />
        </Card>
      </Appear>
      <Appear at={tI} y={720}>
        <Card width={936} style={{ padding: '24px 36px' }}>
          <TeX tex={`{}_{${A('4')}} = \\text{индекс: 4 атома O}`} size={54} />
        </Card>
      </Appear>
      <Row y={940} style={{ gap: 22 }}>
        {[0, 1, 2].map((i) => {
          const at = tEach + i * 4;
          if (frame < at) return null;
          return (
            <div key={i} style={{ transform: `scale(${enter(frame, at, fps)})`, border: `3px solid ${C.fg}`, padding: '14px 18px', textAlign: 'center' }}>
              <TeX tex="\mathrm{H_2SO_4}" size={56} />
              <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 44, color: C.accent, marginTop: 6 }}>4 O</div>
            </div>
          );
        })}
      </Row>
      <Sfx at={tK} name="pop" />
      <Sfx at={tI} name="pop" />
      {[0, 1, 2].map((i) => (
        <Sfx key={i} at={tEach + i * 4} name="tick" volume={0.5} />
      ))}
    </AbsoluteFill>
  );
};

const Trap = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const t4 = W('четыре', 40);
  const t21 = W('двадцать', 80);
  const dx = shake(frame, t4, 12, 16) + shake(frame, t21, 12, 16);
  const flash = frame < 6 ? 1 - frame / 6 : 0;
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${dx}px)` }}>
      <AbsoluteFill style={{ background: C.fg, opacity: flash }} />
      <Kinetic at={0} y={240} size={130} rotate={-6} color={C.bg} punchAt={t4}>Ловушка</Kinetic>
      <Appear at={W('забудешь', 10)} y={500}>
        <Card width={936}>
          <Label color={C.fg}>Забыли коэффициент 3</Label>
          <div style={{ marginTop: 12 }}>
            <TeX tex={`\\text{только индекс: } ${frame >= t4 ? A('4') : '\\;?'}`} size={60} />
          </div>
          {frame >= t21 && (
            <>
              <div style={{ marginTop: 18 }}>
                <Label color={C.fg}>Посчитали все атомы</Label>
              </div>
              <div style={{ marginTop: 12 }}>
                <TeX tex={`3\\cdot(2+1+4) = ${A('21')}`} size={60} />
              </div>
            </>
          )}
        </Card>
      </Appear>
      <Row y={1110} style={{ gap: 20 }}>
        <div style={{ background: C.bg, padding: 6 }}>
          <Option letter="А" value="4" unit="" state="wrong" at={t4 + 6} compact />
        </div>
        <div style={{ background: C.bg, padding: 6 }}>
          <Option letter="Г" value="21" unit="" state="wrong" at={t21 + 6} compact />
        </div>
      </Row>
      <Sfx at={1} name="whoosh" />
      <Sfx at={t4} name="buzz" volume={0.5} />
      <Sfx at={t21} name="buzz" volume={0.45} />
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const t12 = W('двенадцать', 40);
  const tAns = W('ответ', t12 + 30);
  return (
    <AbsoluteFill>
      <Appear at={2} y={300}>
        <div style={{ transform: `scale(${punch(frame, 2, 0.1)})` }}>
          <TeX tex={`${A('3')}\\cdot ${A('4')} = 12`} size={150} />
        </div>
      </Appear>
      <Slam at={t12} y={620} size={92}>12 атомов O</Slam>
      <Row y={940}>
        <Option letter="В" value="12" unit="" state="right" at={tAns} compact />
      </Row>
      <Sfx at={2} name="pop" />
      <Sfx at={t12} name="boom" volume={0.55} />
      <Sfx at={tAns} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Outro = ({ scene }) => <CourseOutro scene={scene} />;

export const SCENES = { hook: Hook, engage: Engage, explain: Explain, trap: Trap, answer: Answer, outro: Outro };
export const TAILS = { engage: 45 };
