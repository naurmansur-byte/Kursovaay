import React from 'react';
import { Composition } from 'remotion';
import { Reel } from './Reel.jsx';
import { buildPlan } from './plan.js';
import r001Timing from './reels/r001.timing.json';
import r002Timing from './reels/r002.timing.json';
import { TAILS as r002Tails } from './reels/r002.jsx';
import r003Timing from './reels/r003.timing.json';
import { TAILS as r003Tails } from './reels/r003.jsx';
import { Avatar, HighlightCover, HIGHLIGHTS } from './brand.jsx';
import { CarouselSlide, CAROUSEL_SIZE } from './carousel.jsx';

const FPS = 30;

// Ролики: id → тайминги озвучки и свои паузы.
const REELS = [
  { id: 'R001', timing: r001Timing },
  { id: 'R002', timing: r002Timing, tails: r002Tails },
  { id: 'R003', timing: r003Timing, tails: r003Tails },
];

export const Root = () => (
  <>
    {REELS.map(({ id, timing, tails }) => {
      const plan = { ...buildPlan(timing, FPS, tails), silent: Boolean(timing.placeholder) };
      return (
        <Composition key={id} id={id} component={Reel} durationInFrames={plan.total} fps={FPS} width={1080} height={1920} defaultProps={{ plan, reel: id }} />
      );
    })}
    {Array.from({ length: CAROUSEL_SIZE }, (_, i) => (
      <Composition key={i} id={`About-${i + 1}`} component={CarouselSlide} durationInFrames={60} fps={FPS} width={1080} height={1350} defaultProps={{ n: i + 1 }} />
    ))}
    <Composition id="Avatar" component={Avatar} durationInFrames={1} fps={FPS} width={1080} height={1080} />
    {HIGHLIGHTS.map((h) => (
      <Composition key={h.id} id={`Highlight-${h.id}`} component={HighlightCover} durationInFrames={1} fps={FPS} width={1080} height={1920} defaultProps={{ icon: h.id }} />
    ))}
  </>
);
