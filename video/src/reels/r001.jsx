// R001 «49 г H2SO4 — сколько моль?»: сцены. Сценарий — content/reels/R001-moles-h2so4/reel-max.md
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F, ACCENT_HEX } from '../theme.js';
import { wordFrame } from '../plan.js';
import { Appear, Atom, Card, Kinetic, Label, Option, OPTIONS, Row, TeX, enter, punch, shake } from '../kit.jsx';

const A = (s) => `\\textcolor{${ACCENT_HEX}}{${s}}`;
const useW = (scene) => {
  const { fps } = useVideoConfig();
  return (stem, fallback = 0, nth = 0) => wordFrame(scene, fps, stem, fallback, nth);
};

const Hook = ({ scene }) => {
  const W = useW(scene);
  return (
    <AbsoluteFill>
      <Kinetic at={W('сорок', 2)} y={280} size={230} rotate={-5}>49 г</Kinetic>
      <Appear at={W('серной', 10)} y={560}>
        <TeX tex="\mathrm{H_2SO_4}" size={150} />
      </Appear>
      <Kinetic at={W('сколько', 26)} y={790} size={100} rotate={-4} from="right" plaque punchAt={W('моль', 34)}>
        Сколько моль?
      </Kinetic>
      <Row y={1010}>
        <Atom size={340} at={W('сколько', 26)} />
      </Row>
    </AbsoluteFill>
  );
};

const Engage = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const t0 = W('выбери', 6);
  const tEnd = scene.dur - 4;
  const left = interpolate(frame, [t0, tEnd], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const R = 34;
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={92} rotate={-3} plaque>Твой ответ?</Kinetic>
      <Appear at={2} y={450}>
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
              <Option key={l} letter={l} value={v} at={W('ответ', 8) + i * 4} />
            ))}
          </div>
        </Card>
      </Appear>
      <Appear at={W('напиши', 30)} y={1130}>
        <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: 46, color: C.muted }}>Напиши вариант в комментариях</div>
      </Appear>
    </AbsoluteFill>
  );
};

const Method = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const cut = frame >= W('сокращаются', 120);
  const g = cut ? A('\\cancel{\\text{г}}') : '\\text{г}';
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={70} rotate={-3}>Количество вещества</Kinetic>
      <Appear at={W('масса', 10)} y={420}>
        <TeX tex={`n = \\dfrac{m}{M}`} size={190} />
      </Appear>
      <Appear at={W('граммы', 90)} y={880}>
        <Card width={880} style={{ display: 'flex', justifyContent: 'center' }}>
          <TeX tex={`\\dfrac{${g}}{${g}/\\text{моль}} = ${cut ? A('\\text{моль}') : '\\text{моль}'}`} size={96} />
        </Card>
      </Appear>
    </AbsoluteFill>
  );
};

const Molar = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tH = W('водород', 20);
  const t32 = W('тридцать', 60);
  const t64 = W('шестьдесят', 90);
  const t98 = W('девяносто', 130);
  let expr = '';
  if (frame >= tH) expr += '2\\cdot1';
  if (frame >= t32) expr += ' + 32';
  if (frame >= t64) expr += ` + ${A('4')}\\cdot16`;
  const chips = [
    ['2', 'H', W('водород', 20)],
    ['1', 'S', W('сера', 45)],
    ['4', 'O', W('кислород', 75)],
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
      <Appear at={tH} y={840}>
        <Card width={936} style={{ minHeight: 300 }}>
          <TeX tex="M(\mathrm{H_2SO_4}) =" size={66} />
          <div style={{ marginTop: 10, minHeight: 80 }}>
            <TeX tex={expr || '\\;'} size={72} />
          </div>
          {frame >= t98 && (
            <div style={{ marginTop: 22, transform: `scale(${punch(frame, t98, 0.18)})`, transformOrigin: 'left center' }}>
              <TeX tex={`= ${A('98\\,\\text{г/моль}')}`} size={92} />
            </div>
          )}
        </Card>
      </Appear>
    </AbsoluteFill>
  );
};

const Trap = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const t50 = W('пятьдесят', 70);
  const dx = shake(frame, t50);
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={240} size={120} rotate={-6} plaque punchAt={1}>Ловушка</Kinetic>
      <Appear at={W('забудешь', 16)} y={500}>
        <Card width={936} style={{ transform: `translateX(${dx}px)` }}>
          <Label>Забыли индекс 4 у кислорода</Label>
          <div style={{ marginTop: 20 }}>
            <TeX tex={`M = 2\\cdot1 + 32 + 16 = ${frame >= t50 ? A('50') : '\\;?'}`} size={66} />
          </div>
          {frame >= W('неверный', t50 + 10) && (
            <div style={{ marginTop: 16 }}>
              <TeX tex={`n = \\dfrac{49}{50} = ${A('0{,}98')}`} size={66} />
            </div>
          )}
        </Card>
      </Appear>
      <Row y={1060}>
        <Option letter="Б" value="0{,}98" state="wrong" at={W('неверный', t50 + 10)} compact />
      </Row>
    </AbsoluteFill>
  );
};

const Answer = ({ scene }) => {
  const frame = useCurrentFrame();
  const W = useW(scene);
  const tHalf = W('половин', 50);
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={76} rotate={-3}>Решаем</Kinetic>
      <Appear at={W('делим', 4)} y={400}>
        <TeX tex={`n = \\dfrac{49\\,\\text{г}}{98\\,\\text{г/моль}}`} size={130} />
      </Appear>
      <Kinetic at={tHalf} y={760} size={140} rotate={-4} plaque punchAt={tHalf + 2} from="right">0,5 моль</Kinetic>
      <Row y={1060}>
        <Option letter="А" value="0{,}5" state="right" at={W('правильн', tHalf + 30)} compact />
      </Row>
    </AbsoluteFill>
  );
};

const Check = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tOk = W('сходится', 90);
  const draw = enter(frame, tOk, fps, { damping: 200, stiffness: 90 });
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={250} size={76} rotate={-3}>Проверка</Kinetic>
      <Appear at={W('половин', 10)} y={470}>
        <Card width={880} style={{ display: 'flex', justifyContent: 'center' }}>
          <TeX tex={`m = 0{,}5 \\cdot 98 = ${A('49\\,\\text{г}')}`} size={86} />
        </Card>
      </Appear>
      {frame >= tOk && (
        <Row y={800}>
          <svg width="260" height="260" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="44" fill="none" stroke={C.accent} strokeWidth="7" />
            <path d="M28 52 L44 67 L73 35" fill="none" stroke={C.fg} strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" strokeDasharray="70" strokeDashoffset={70 * (1 - draw)} />
          </svg>
        </Row>
      )}
    </AbsoluteFill>
  );
};

const Outro = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tWrite = W('напиши', 40);
  const tWord = W('моль', tWrite + 30, 1);
  const letters = 'МОЛЬ'.split('');
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={240} size={78} rotate={-3}>Хочешь памятку?</Kinetic>
      <Kinetic at={tWrite} y={370} size={96} rotate={-3} from="right">Напиши</Kinetic>
      <Kinetic at={tWrite + 4} y={480} size={80} rotate={-3}>в комментариях</Kinetic>
      <Row y={630} style={{ gap: 6 }}>
        {frame >= tWord &&
          letters.map((ch, i) => {
            const p = enter(frame, tWord + i * 3, fps, { damping: 11, stiffness: 200 });
            return (
              <div key={i} style={{ transform: `translateY(${(1 - p) * -160}px) rotate(${(1 - p) * (i % 2 ? 18 : -18) - 4}deg)`, opacity: Math.min(1, p * 2), background: C.accent, fontFamily: F.display, fontWeight: 800, fontSize: 210, lineHeight: 1, padding: '14px 18px 22px', color: C.fg }}>
                {ch}
              </div>
            );
          })}
      </Row>
      <Appear at={W('пришлю', tWord + 20)} y={930}>
        <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 54, color: C.fg, textTransform: 'uppercase', letterSpacing: '0.04em' }}>→ пришлю памятку</div>
      </Appear>
      <Appear at={W('пришлю', tWord + 20) + 6} y={1060}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
          <Atom size={150} at={0} />
          <div>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 64, color: C.fg }}>ХИМИЯ ПРОСТО</div>
            <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: 40, color: C.muted }}>подготовка к ЕНТ по химии</div>
          </div>
        </div>
      </Appear>
    </AbsoluteFill>
  );
};

export const SCENES = { hook: Hook, engage: Engage, method: Method, molar: Molar, trap: Trap, answer: Answer, check: Check, outro: Outro };
