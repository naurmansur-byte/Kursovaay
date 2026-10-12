// Карусель «Кто мы» для Instagram: 7 слайдов 1080×1350, стиль 2. Рендер кадра 45 (анимации успели встать).
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { C, F, SAFE } from './theme.js';
import { Atom, Background, Card, Kinetic, Row } from './kit.jsx';
import { useFonts } from './Reel.jsx';

const Big = ({ children, size = 64, color = C.fg, weight = 800, font = F.display, style }) => (
  <div style={{ fontFamily: font, fontWeight: weight, fontSize: size, lineHeight: 1.1, color, ...style }}>{children}</div>
);
const Text = ({ children, size = 46, color = C.fg, style }) => (
  <div style={{ fontFamily: F.body, fontWeight: 700, fontSize: size, lineHeight: 1.3, color, ...style }}>{children}</div>
);

const SLIDES = [
  // 1. Обложка
  () => (
    <>
      <Kinetic at={0} y={250} size={190} rotate={-5}>Химия</Kinetic>
      <Kinetic at={0} y={470} size={170} rotate={-4} plaque from="right">Просто</Kinetic>
      <Row y={720}>
        <Text size={48} style={{ textAlign: 'center' }}>подготовка к ЕНТ по химии<br />для 11 класса</Text>
      </Row>
      <Row y={880}>
        <Atom size={300} at={-60} speed={0} />
      </Row>
      <Row y={1210}>
        <Text size={38} color={C.muted}>листай →</Text>
      </Row>
    </>
  ),
  // 2. Боль
  () => (
    <>
      <Kinetic at={0} y={230} size={92} rotate={-3}>Знаешь правило,</Kinetic>
      <Kinetic at={0} y={345} size={92} rotate={-3} from="right">но теряешься</Kinetic>
      <Kinetic at={0} y={470} size={100} rotate={-4} plaque>в задаче?</Kinetic>
      <Row y={720}>
        <Card width={920}>
          <Text size={50}>
            Разбираем, <span style={{ color: C.accent }}>почему</span> работает способ, — и решаем на разных примерах: от простых до самых сложных заданий ЕНТ.
          </Text>
        </Card>
      </Row>
    </>
  ),
  // 3. Как идём — последовательность
  () => (
    <>
      <Kinetic at={0} y={220} size={110} rotate={-4} plaque>Как идём</Kinetic>
      {[
        ['1', 'Основа', 'формулы, уравнения, расчёты'],
        ['2', 'Связи', 'соединяем темы между собой'],
        ['3', 'Сложные задачи', 'формат ЕНТ и ловушки'],
      ].map(([n, h, t], i) => (
        <div key={n} style={{ position: 'absolute', top: 470 + i * 240, left: SAFE.x + 20, right: SAFE.x, display: 'flex', alignItems: 'center', gap: 40 }}>
          <Big size={170} color={C.accent} style={{ width: 130, textAlign: 'center' }}>{n}</Big>
          <div>
            <Big size={62}>{h}</Big>
            <Text size={42} color={C.muted}>{t}</Text>
          </div>
        </div>
      ))}
    </>
  ),
  // 4. Формат
  () => (
    <>
      <Kinetic at={0} y={220} size={110} rotate={-4} plaque>Формат</Kinetic>
      {[
        ['онлайн', 'уроки в Google Meet'],
        ['2 × 90 мин', 'два урока в неделю'],
        ['5 человек', 'в группе — успеваем каждого'],
      ].map(([h, t], i) => (
        <div key={h} style={{ position: 'absolute', top: 430 + i * 210, left: SAFE.x + 20, right: SAFE.x }}>
          <Big size={92} style={{ textTransform: 'uppercase' }}>{h}</Big>
          <Text size={42} color={C.muted}>{t}</Text>
        </div>
      ))}
      <Row y={1100} style={{ gap: 14, flexWrap: 'wrap' }}>
        {['ДЗ с проверкой', 'Telegram', 'пробники и отчёт'].map((t) => (
          <div key={t} style={{ border: `3px solid ${C.fg}`, padding: '10px 22px', fontFamily: F.body, fontWeight: 800, fontSize: 36, textTransform: 'uppercase', color: C.fg, whiteSpace: 'nowrap' }}>{t}</div>
        ))}
      </Row>
    </>
  ),
  // 5. Призыв
  () => (
    <>
      <Kinetic at={0} y={230} size={150} rotate={-5}>Старт</Kinetic>
      <Kinetic at={0} y={420} size={140} rotate={-4} plaque from="right">1 ноября</Kinetic>
      <Row y={700}>
        <Card width={920}>
          <Big size={60}>Запись:</Big>
          <Text size={50} style={{ marginTop: 12 }}>
            напиши нам <span style={{ color: C.accent }}>в директ</span>
            <br />— расскажем о курсе
          </Text>
        </Card>
      </Row>
      <Row y={1080}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
          <Atom size={120} at={-60} speed={0} />
          <Big size={60}>ХИМИЯ ПРОСТО</Big>
        </div>
      </Row>
    </>
  ),
];

export const CAROUSEL_SIZE = SLIDES.length;

export const CarouselSlide = ({ n }) => {
  useFonts();
  const Slide = SLIDES[n - 1];
  return (
    <AbsoluteFill style={{ background: C.bg }}>
      <Background />
      <div style={{ position: 'absolute', top: 70, left: SAFE.x, right: SAFE.x, display: 'flex', justifyContent: 'space-between', fontFamily: F.body, fontWeight: 800, fontSize: 30, letterSpacing: '0.14em', color: C.fg }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <span style={{ width: 16, height: 16, borderRadius: '50%', background: C.accent }} />
          ХИМИЯ ПРОСТО · ЕНТ
        </span>
        <span style={{ color: C.muted }}>{n}/{SLIDES.length}</span>
      </div>
      <Slide />
    </AbsoluteFill>
  );
};
