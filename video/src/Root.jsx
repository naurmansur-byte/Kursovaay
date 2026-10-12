import React from 'react';
import { Composition } from 'remotion';
import { Reel } from './Reel.jsx';
import { buildPlan } from './plan.js';
import r001Timing from './reels/r001.timing.json';

const FPS = 30;

export const Root = () => {
  const r001 = { ...buildPlan(r001Timing, FPS), silent: Boolean(r001Timing.placeholder) };
  return (
    <Composition
      id="R001"
      component={Reel}
      durationInFrames={r001.total}
      fps={FPS}
      width={1080}
      height={1920}
      defaultProps={{ plan: r001, reel: 'R001' }}
    />
  );
};
