// R001 «49 г H2SO4 — сколько моль?», короткая версия (~27 с). Сценарий — content/reels/R001-moles-h2so4/reel-max.md
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from '../theme.js';
import { wordFrame } from '../plan.js';
import { Appear, Atom, Card, Kinetic, Label, Option, OPTIONS, Row, Sfx, TeX, enter, punch, shake } from '../kit.jsx';
import { CourseOutro } from '../scenes.jsx';

const A = (s) => `\\textcolor{${C.accent}}{${s}}`;
const useW = (scene) => {
  const { fps } = useVideoConfig();
  return (stem, fallback = 0, nth = 0) => wordFrame(scene, fps, stem, fallback, nth);
};

// Крупное число-удар поверх сцены.
const Slam = ({ at, y, children, size = 260 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at) return null;
  const p = enter(frame, at, fps, { damping: 10, stiffness: 220, mass: 0.6 });
  return (
    <Row y={y}>
      <div style={{ transform: `scale(${interpolate(p, [0, 1], [2.4, 1])}) rotate(-4deg)`, opacity: Math.min(1, p * 3), background: C.accent, color: C.fg, fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: 1, padding: `${size * 0.08}px ${size * 0.16}px ${size * 0.12}px`, whiteSpace: 'nowrap' }}>
        {children}
      </div>
    </Row>
  );
};

const Hook = ({ scene }) => {
  const W = useW(scene);
  const t1 = W('сорок', 2);
  const t2 = W('сколько', 22);
  return (
    <AbsoluteFill>
      <Kinetic at={t1} y={280} size={230} rotate={-5}>49 г</Kinetic>
      <Appear at={W('серной', 8)} y={560}>
        <TeX tex="\mathrm{H_2SO_4}" size={150} />
      </Appear>
      <Kinetic at={t2} y={790} size={100} rotate={-4} from="right" plaque punchAt={W('моль', t2 + 8)}>
        Сколько моль?
      </Kinetic>
      <Row y={1010}>
        <Atom size={340} at={t2} speed={1.6} />
      </Row>
      <Sfx at={t1} name="whoosh" />
      <Sfx at={t2} name="whoosh" />
      <Sfx at={W('моль', t2 + 8)} name="pop" volume={0.45} />
    </AbsoluteFill>
  );
};

const Engage = ({ scene }) => {
  const frame = useCurrentFrame();
  const t0 = 2;
  const left = interpolate(frame, [t0, scene.dur - 2], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const R = 34;
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={92} rotate={-3} plaque>Твой ответ?</Kinetic>
      <Appear at={1} y={450}>
        <Card>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Label>ЕНТ · выбери один ответ</Label>
            <svg width={2 * R + 12} height={2 * R + 12} viewBox={`${-R - 6} ${-R - 6} ${2 * R + 12} ${2 * R + 12}`}>
              <circle r={R} fill="none" stroke={C.faint} strokeWidth="8" />
              <circle r={R} fill="none" stroke={C.accent} strokeWidth="8" strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - left)} transform="rotate(-90)" />
            </svg>
          </div>
          <div style={{ marginTop: 26 }}>
            <TeX tex="\text{Сколько моль в }49\,\text{г}\ \mathrm{H_2SO_4}?" size={58} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 22, marginTop: 34 }}>
            {OPTIONS.map(([l, v], i) => (
              <Option key={l} letter={l} value={v} at={4 + i * 3} />
            ))}
          </div>
        </Card>
      </Appear>
      {[4, 7, 10, 13].map((t) => (
        <Sfx key={t} at={t} name="tick" volume={0.5} />
      ))}
    </AbsoluteFill>
  );
};

const Molar = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const t2 = W('два', 30);
  const t32 = W('тридцать', 55);
  const t64 = W('шестьдесят', 80);
  const t98 = W('девяносто', 110);
  let expr = '';
  if (frame >= t2) expr += '2\\cdot1';
  if (frame >= t32) expr += ' + 32';
  if (frame >= t64) expr += ` + ${A('4')}\\cdot16`;
  const chips = [
    ['2', 'H', t2],
    ['1', 'S', t32],
    ['4', 'O', t64],
  ];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={76} rotate={-3}>Молярная масса</Kinetic>
      <Appear at={2} y={400}>
        <TeX tex="\mathrm{H_2SO_4}" size={160} />
      </Appear>
      <Row y={640} style={{ gap: 28 }}>
        {chips.map(([n, el, at]) => {
          const p = enter(frame, at, fps);
          return frame < at ? null : (
            <div key={el} style={{ transform: `scale(${p})`, border: `3px solid ${el === 'O' ? C.accent : C.fg}`, padding: '10px 30px', fontFamily: F.display, fontWeight: 800, fontSize: 64, color: C.fg }}>
              <span style={{ color: el === 'O' ? C.accent : C.fg }}>{n}</span> {el}
            </div>
          );
        })}
      </Row>
      <Appear at={t2} y={840}>
        <Card width={936}>
          <TeX tex="M(\mathrm{H_2SO_4}) =" size={66} />
          <div style={{ marginTop: 10, minHeight: 80 }}>
            <TeX tex={expr || '\\;'} size={72} />
          </div>
        </Card>
      </Appear>
      <Slam at={t98} y={1170} size={140}>98 г/моль</Slam>
      <Sfx at={t2} name="pop" />
      <Sfx at={t32} name="pop" />
      <Sfx at={t64} name="pop" />
      <Sfx at={t98} name="boom" volume={0.6} />
    </AbsoluteFill>
  );
};

const Trap = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const t50 = W('пятьдесят', 50);
  const tTrap = W('ловушка', t50 + 15);
  const dx = shake(frame, t50, 14, 18) + shake(frame, tTrap, 10, 10);
  const flash = interpolate(frame, [0, 6], [1, 0], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ background: C.accent, transform: `translateX(${dx}px)` }}>
      <AbsoluteFill style={{ background: C.fg, opacity: flash }} />
      <Kinetic at={0} y={240} size={130} rotate={-6} color={C.bg} punchAt={tTrap}>Ловушка</Kinetic>
      <Appear at={W('забыл', 4)} y={500}>
        <Card width={936}>
          <Label color={C.fg}>Забыли индекс 4 у кислорода</Label>
          <div style={{ marginTop: 20 }}>
            <TeX tex={`M = 2\\cdot1 + 32 + 16 = ${frame >= t50 ? A('50') : '\\;?'}`} size={66} />
          </div>
          {frame >= t50 + 6 && (
            <div style={{ marginTop: 16 }}>
              <TeX tex={`n = \\dfrac{49}{50} = ${A('0{,}98')}`} size={66} />
            </div>
          )}
        </Card>
      </Appear>
      <Row y={1080}>
        <div style={{ background: C.bg, padding: 6 }}>
          <Option letter="Б" value="0{,}98" state="wrong" at={t50 + 10} compact />
        </div>
      </Row>
      <Sfx at={1} name="whoosh" />
      <Sfx at={t50} name="buzz" volume={0.5} />
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tNum = W('сорок', 30);
  const tHalf = W('половин', 70);
  const tAns = W('ответ', tHalf + 30);
  const tex = frame < tNum ? 'n = \\dfrac{m}{M}' : 'n = \\dfrac{49\\,\\text{г}}{98\\,\\text{г/моль}}';
  return (
    <AbsoluteFill>
      <Appear at={2} y={300}>
        <div style={{ transform: `scale(${punch(frame, tNum, 0.12)})` }}>
          <TeX tex={tex} size={108} />
        </div>
      </Appear>
      <Slam at={tHalf} y={700} size={150}>0,5 моль</Slam>
      <Row y={1000}>
        <Option letter="А" value="0{,}5" state="right" at={tAns} compact />
      </Row>
      <Appear at={tAns + 10} y={1160}>
        <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: 40, color: C.muted }}>
          проверка: 0,5 · 98 = 49 г ✓
        </div>
      </Appear>
      <Sfx at={tNum} name="pop" />
      <Sfx at={tHalf} name="boom" volume={0.5} />
      <Sfx at={tAns} name="ding" volume={0.5} />
    </AbsoluteFill>
  );
};

const Outro = ({ scene }) => <CourseOutro scene={scene} />;

export const SCENES = { hook: Hook, engage: Engage, molar: Molar, trap: Trap, answer: Answer, outro: Outro };
