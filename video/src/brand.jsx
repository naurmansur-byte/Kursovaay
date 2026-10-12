// Оформление Instagram в стиле 2: аватар 1080×1080 и обложки «Актуального» 1080×1920.
import React from 'react';
import { AbsoluteFill } from 'remotion';
import '@fontsource-variable/unbounded';
import '@fontsource-variable/manrope';
import { C, F } from './theme.js';
import { Atom, Background } from './kit.jsx';
import { useFonts } from './Reel.jsx';

export const Avatar = () => (
  <AbsoluteFill style={{ background: C.bg }}>
    <Background />
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center' }}>
      <Atom size={780} at={-90} speed={0} />
    </AbsoluteFill>
  </AbsoluteFill>
);

const Flask = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 200 200">
    <path d="M78 22 h44 M86 22 v52 L42 160 a14 14 0 0 0 12 20 h92 a14 14 0 0 0 12 -20 L114 74 V22" fill="none" stroke={C.fg} strokeWidth="11" strokeLinejoin="round" strokeLinecap="round" />
    <path d="M62 128 h76 l18 34 a8 8 0 0 1 -7 12 H51 a8 8 0 0 1 -7 -12 Z" fill={C.accent} />
    <circle cx="92" cy="148" r="7" fill={C.fg} />
    <circle cx="112" cy="138" r="5" fill={C.fg} />
  </svg>
);

const ICONS = {
  course: () => <Atom size={620} at={-90} speed={0} />,
  join: () => (
    <div style={{ width: 420, height: 420, background: C.accent, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: 'rotate(-4deg)' }}>
      <svg width="300" height="300" viewBox="0 0 100 100">
        <path d="M14 50 H78 M54 24 L80 50 L54 76" fill="none" stroke={C.fg} strokeWidth="13" strokeLinecap="square" strokeLinejoin="miter" />
      </svg>
    </div>
  ),
  solutions: () => <Flask size={560} />,
  ent: () => (
    <div style={{ background: C.accent, padding: '30px 50px 44px', transform: 'rotate(-4deg)', fontFamily: F.display, fontWeight: 800, fontSize: 210, lineHeight: 1, color: C.fg }}>ЕНТ</div>
  ),
  faq: () => <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 520, lineHeight: 1, color: C.fg }}>?</div>,
};

export const HIGHLIGHTS = [
  { id: 'course', title: 'О курсе' },
  { id: 'join', title: 'Запись' },
  { id: 'solutions', title: 'Разборы' },
  { id: 'ent', title: 'ЕНТ' },
  { id: 'faq', title: 'Вопросы' },
];

export const HighlightCover = ({ icon }) => {
  useFonts();
  const Icon = ICONS[icon];
  return (
    <AbsoluteFill style={{ background: C.bg }}>
      <Background />
      <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center' }}>
        <Icon />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
