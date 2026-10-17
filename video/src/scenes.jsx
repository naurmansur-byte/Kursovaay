// Шаблонные сцены Reels: выбор ответа (ЕНТ), крупная плашка-удар, аутро с призывом в комментарии.
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { C, F } from './theme.js';
import { wordFrame } from './plan.js';
import { Appear, Atom, Card, Dna, Kinetic, Label, Option, Row, Sfx, TeX, enter } from './kit.jsx';

export const A = (s) => `\\textcolor{${C.accent}}{${s}}`;

export const useW = (scene) => {
  const { fps } = useVideoConfig();
  return (stem, fallback = 0, nth = 0) => wordFrame(scene, fps, stem, fallback, nth);
};

// Крупное число или ответ, влетает «ударом».
export const Slam = ({ at, y, children, size = 260 }) => {
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

// Карточка «выбери ответ» с таймером. options: [['А', '0{,}5'], ...]
// cols={1} — для длинных текстовых вариантов (по одному в строке).
export const EngageScene = ({ scene, questionTex, options, unit, cols = 2, questionSize = 56 }) => {
  const frame = useCurrentFrame();
  const left = interpolate(frame, [2, scene.dur - 2], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
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
          <div style={{ marginTop: 26, display: 'grid', gap: 10 }}>
            {(Array.isArray(questionTex) ? questionTex : [questionTex]).map((t) => (
              <TeX key={t} tex={t} size={questionSize} />
            ))}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: cols === 1 ? '1fr' : '1fr 1fr', gap: cols === 1 ? 14 : 22, marginTop: 34 }}>
            {options.map(([l, v], i) => (
              <Option key={l} letter={l} value={v} unit={unit} at={4 + i * 3} />
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

// Титул YouTube-ролика (16:9): сразу видно, о чём видео. Слева тема, справа «В этом видео» — пункты появляются под голос.
// items: [['текст пункта', 'стем слова из озвучки'], ...]
export const TopicIntro = ({ scene, tag, title, plaque, items, icon = 'atom' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const pt = enter(frame, 2, fps);
  const pp = enter(frame, 10, fps, { damping: 10, stiffness: 200, mass: 0.6 });
  const times = items.map(([, stem], i) => W(stem, 30 + i * 20));
  return (
    <AbsoluteFill>
      <div style={{ position: 'absolute', left: 120, top: 200, width: 860 }}>
        <div style={{ opacity: pt }}><Label size={36}>{tag}</Label></div>
        <div style={{ marginTop: 24, transform: `translateX(${(1 - pt) * -400}px)`, opacity: pt, fontFamily: F.display, fontWeight: 800, fontSize: 112, lineHeight: 1.02, textTransform: 'uppercase', color: C.fg }}>{title}</div>
        {frame >= 10 && (
          <div style={{ display: 'inline-block', marginTop: 30, transform: `scale(${interpolate(pp, [0, 1], [1.8, 1])}) rotate(-3deg)`, transformOrigin: 'left center', background: C.accent, padding: '10px 26px 16px', fontFamily: F.display, fontWeight: 800, fontSize: 64, textTransform: 'uppercase', color: C.fg }}>{plaque}</div>
        )}
        <div style={{ marginTop: 50 }}>{icon === 'dna' ? <Dna size={260} at={6} /> : <Atom size={230} at={6} speed={1.3} />}</div>
      </div>
      <div style={{ position: 'absolute', left: 1060, top: 220, width: 760 }}>
        <div style={{ opacity: pt }}><Label size={34} color={C.accent}>В этом видео</Label></div>
        <div style={{ marginTop: 26, display: 'grid', gap: 22 }}>
          {items.map(([text], i) => {
            const at = times[i];
            if (frame < at) return null;
            const p = enter(frame, at, fps);
            return (
              <div key={text} style={{ display: 'flex', alignItems: 'center', gap: 22, opacity: p, transform: `translateX(${(1 - p) * 120}px)` }}>
                <div style={{ width: 64, height: 64, flex: 'none', background: C.accent, display: 'grid', placeItems: 'center', fontFamily: F.display, fontWeight: 800, fontSize: 34, color: C.fg }}>{i + 1}</div>
                <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 46, lineHeight: 1.15, color: C.fg }}>{text}</div>
              </div>
            );
          })}
        </div>
      </div>
      <Sfx at={2} name="whoosh" />
      <Sfx at={10} name="boom" volume={0.45} />
      {times.map((t, i) => <Sfx key={i} at={t} name="pop" volume={0.3} />)}
    </AbsoluteFill>
  );
};

// Аутро-приглашение на курс: логотип, факты о курсе (только утверждённые), слово для комментариев.
// Голос: «Хочешь решать такие задачи? Курс «ХимБио просто», старт первого ноября. Пиши «курс» в комментариях!»
export const CourseOutro = ({ scene, word = 'курс', icon = 'atom' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tCourse = W('курс', 40);
  const tStart = W('старт', tCourse + 20);
  const tWrite = W('пиши', tStart + 30);
  const tWord = W(word, tWrite + 6, 1);
  const letters = word.toUpperCase().split('');
  const letterSize = Math.min(200, (930 / letters.length - 42) / 0.85);
  const chips = [
    ['онлайн', tCourse + 10],
    ['химия + биология', tCourse + 14],
    ['старт 1 ноября', tStart],
  ];
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={200} size={80} rotate={-3}>Хочешь решать</Kinetic>
      <Kinetic at={3} y={295} size={80} rotate={-3} from="right">такие задачи?</Kinetic>
      <Appear at={tCourse} y={410}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
          {icon === 'dna' ? <Dna size={120} at={tCourse} /> : <Atom size={110} at={tCourse} speed={1.4} />}
          <div>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 62, lineHeight: 1, color: C.fg, whiteSpace: 'nowrap' }}>ХИМБИО ПРОСТО</div>
            <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: 40, color: C.muted, marginTop: 8 }}>курс подготовки к ЕНТ</div>
          </div>
        </div>
      </Appear>
      <Row y={590} style={{ gap: 12, flexWrap: 'wrap' }}>
        {chips.map(([text, at], i) =>
          frame < at ? null : (
            <div key={text} style={{ transform: `scale(${enter(frame, at, fps)})`, border: `3px solid ${i === 2 ? C.accent : C.fg}`, background: i === 2 ? C.accent : 'transparent', padding: '8px 20px', fontFamily: F.body, fontWeight: 800, fontSize: 34, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>
              {text}
            </div>
          )
        )}
      </Row>
      <Kinetic at={tWrite} y={790} size={84} rotate={-3} from="right">Пиши</Kinetic>
      <Kinetic at={tWrite + 3} y={890} size={70} rotate={-3}>в комментариях</Kinetic>
      <Row y={1020} style={{ gap: 6 }}>
        {frame >= tWord &&
          letters.map((ch, i) => {
            const p = enter(frame, tWord + i * 3, fps, { damping: 11, stiffness: 200 });
            return (
              <div key={i} style={{ transform: `translateY(${(1 - p) * -160}px) rotate(${(1 - p) * (i % 2 ? 18 : -18) - 4}deg)`, opacity: Math.min(1, p * 2), background: C.accent, fontFamily: F.display, fontWeight: 800, fontSize: letterSize, lineHeight: 1, padding: '14px 18px 22px', color: C.fg }}>
                {ch}
              </div>
            );
          })}
      </Row>
      <Sfx at={tCourse} name="whoosh" />
      <Sfx at={tStart} name="pop" volume={0.4} />
      <Sfx at={tWrite} name="whoosh" />
      {letters.map((_, i) => (
        <Sfx key={i} at={tWord + i * 3} name="pop" volume={0.3} />
      ))}
    </AbsoluteFill>
  );
};

// Аутро: «Хочешь памятку? Пиши «СЛОВО» в комментариях» + логотип.
export const OutroScene = ({ scene, word, writeStem = 'пиши', wordStem }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const W = useW(scene);
  const tWrite = W(writeStem, 20);
  const tWord = W(wordStem ?? word, tWrite + 6);
  const letters = word.toUpperCase().split('');
  // Буквы-плашки должны уместиться в 930 px: на букву ≈ 0.85 em + поля.
  const letterSize = Math.min(210, (930 / letters.length - 42) / 0.85);
  return (
    <AbsoluteFill>
      <Kinetic at={0} y={240} size={78} rotate={-3}>Хочешь памятку?</Kinetic>
      <Kinetic at={tWrite} y={370} size={96} rotate={-3} from="right">Пиши</Kinetic>
      <Kinetic at={tWrite + 3} y={480} size={80} rotate={-3}>в комментариях</Kinetic>
      <Row y={630} style={{ gap: 6 }}>
        {frame >= tWord &&
          letters.map((ch, i) => {
            const p = enter(frame, tWord + i * 3, fps, { damping: 11, stiffness: 200 });
            return (
              <div key={i} style={{ transform: `translateY(${(1 - p) * -160}px) rotate(${(1 - p) * (i % 2 ? 18 : -18) - 4}deg)`, opacity: Math.min(1, p * 2), background: C.accent, fontFamily: F.display, fontWeight: 800, fontSize: letterSize, lineHeight: 1, padding: '14px 18px 22px', color: C.fg }}>
                {ch}
              </div>
            );
          })}
      </Row>
      <Appear at={tWord + 16} y={930}>
        <div style={{ fontFamily: F.body, fontWeight: 800, fontSize: 54, color: C.fg, textTransform: 'uppercase', letterSpacing: '0.04em' }}>→ пришлю памятку</div>
      </Appear>
      <Appear at={tWord + 22} y={1060}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
          <Atom size={150} at={0} />
          <div>
            <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 64, color: C.fg }}>ХИМБИО ПРОСТО</div>
            <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: 40, color: C.muted }}>подготовка к ЕНТ по химии</div>
          </div>
        </div>
      </Appear>
      <Sfx at={tWrite} name="whoosh" />
      {letters.map((_, i) => (
        <Sfx key={i} at={tWord + i * 3} name="pop" volume={0.3} />
      ))}
    </AbsoluteFill>
  );
};
