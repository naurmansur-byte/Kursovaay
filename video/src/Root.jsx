import React from 'react';
import { Composition } from 'remotion';
import { Reel } from './Reel.jsx';
import { buildPlan } from './plan.js';
import r001Timing from './reels/r001.timing.json';
import r002Timing from './reels/r002.timing.json';
import { TAILS as r002Tails } from './reels/r002.jsx';
import r003Timing from './reels/r003.timing.json';
import { TAILS as r003Tails } from './reels/r003.jsx';
import b001Timing from './reels/b001.timing.json';
import { TAILS as b001Tails } from './reels/b001.jsx';
import b002Timing from './reels/b002.timing.json';
import { TAILS as b002Tails } from './reels/b002.jsx';
import b003Timing from './reels/b003.timing.json';
import { TAILS as b003Tails } from './reels/b003.jsx';
import { Avatar, HighlightCover, HIGHLIGHTS } from './brand.jsx';
import { CarouselSlide, CAROUSEL_HB_SIZE, CAROUSEL_SIZE } from './carousel.jsx';
import y001Timing from './reels/y001.timing.json';
import { TAILS as y001Tails } from './reels/y001.jsx';
import y002Timing from './reels/y002.timing.json';
import { TAILS as y002Tails } from './reels/y002.jsx';
import y003Timing from './reels/y003.timing.json';
import { TAILS as y003Tails } from './reels/y003.jsx';
import y004Timing from './reels/y004.timing.json';
import { TAILS as y004Tails } from './reels/y004.jsx';
import a001Timing from './reels/a001.timing.json';
import { TAILS as a001Tails } from './reels/a001.jsx';
import a002Timing from './reels/a002.timing.json';
import { TAILS as a002Tails } from './reels/a002.jsx';
import a003Timing from './reels/a003.timing.json';
import { TAILS as a003Tails } from './reels/a003.jsx';

const FPS = 30;

// Ролики: id → тайминги озвучки и свои паузы.
const REELS = [
  { id: 'R001', timing: r001Timing },
  { id: 'R002', timing: r002Timing, tails: r002Tails },
  { id: 'R003', timing: r003Timing, tails: r003Tails },
  { id: 'B001', timing: b001Timing, tails: b001Tails, subject: 'bio' },
  { id: 'B002', timing: b002Timing, tails: b002Tails, subject: 'bio' },
  { id: 'B003', timing: b003Timing, tails: b003Tails, subject: 'bio' },
  { id: 'A001', timing: a001Timing, tails: a001Tails },  // реклама для учеников, хук «100 из 140»
  { id: 'A002', timing: a002Timing, tails: a002Tails },  // хук «Стоп + ловушка»
  { id: 'A003', timing: a003Timing, tails: a003Tails },  // хук «миф: не нужно зубрить все учебники»
];

export const Root = () => (
  <>
    {REELS.map(({ id, timing, tails, subject = 'chem' }) => {
      const plan = { ...buildPlan(timing, FPS, tails), silent: Boolean(timing.placeholder) };
      return (
        <Composition key={id} id={id} component={Reel} durationInFrames={plan.total} fps={FPS} width={1080} height={1920} defaultProps={{ plan, reel: id, subject }} />
      );
    })}
    {Array.from({ length: CAROUSEL_SIZE }, (_, i) => (
      <Composition key={i} id={`About-${i + 1}`} component={CarouselSlide} durationInFrames={60} fps={FPS} width={1080} height={1350} defaultProps={{ n: i + 1 }} />
    ))}
    {Array.from({ length: CAROUSEL_HB_SIZE }, (_, i) => (
      <Composition key={`hb${i}`} id={`AboutHB-${i + 1}`} component={CarouselSlide} durationInFrames={60} fps={FPS} width={1080} height={1350} defaultProps={{ n: i + 1, set: 'hb' }} />
    ))}
    {(() => {
      const plan = buildPlan(y001Timing, FPS, y001Tails);
      return <Composition id="Y001" component={Reel} durationInFrames={plan.total} fps={FPS} width={1920} height={1080} defaultProps={{ plan, reel: 'Y001' }} />;
    })()}
    {(() => {
      const plan = buildPlan(y002Timing, FPS, y002Tails);
      return <Composition id="Y002" component={Reel} durationInFrames={plan.total} fps={FPS} width={1920} height={1080} defaultProps={{ plan, reel: 'Y002' }} />;
    })()}
    {(() => {
      const plan = buildPlan(y003Timing, FPS, y003Tails);
      return <Composition id="Y003" component={Reel} durationInFrames={plan.total} fps={FPS} width={1920} height={1080} defaultProps={{ plan, reel: 'Y003', subject: 'bio' }} />;
    })()}
    {(() => {
      const plan = buildPlan(y004Timing, FPS, y004Tails);
      return <Composition id="Y004" component={Reel} durationInFrames={plan.total} fps={FPS} width={1920} height={1080} defaultProps={{ plan, reel: 'Y004' }} />;
    })()}
    <Composition id="Avatar" component={Avatar} durationInFrames={1} fps={FPS} width={1080} height={1080} />
    {HIGHLIGHTS.map((h) => (
      <Composition key={h.id} id={`Highlight-${h.id}`} component={HighlightCover} durationInFrames={1} fps={FPS} width={1080} height={1920} defaultProps={{ icon: h.id }} />
    ))}
  </>
);
