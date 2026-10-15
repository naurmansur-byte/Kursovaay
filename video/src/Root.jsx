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
import a004Timing from './reels/a004.timing.json';
import { TAILS as a004Tails } from './reels/a004.jsx';
import r004Timing from './reels/r004.timing.json';
import { TAILS as r004Tails } from './reels/r004.jsx';
import r005Timing from './reels/r005.timing.json';
import { TAILS as r005Tails } from './reels/r005.jsx';
import r006Timing from './reels/r006.timing.json';
import { TAILS as r006Tails } from './reels/r006.jsx';
import r007Timing from './reels/r007.timing.json';
import { TAILS as r007Tails } from './reels/r007.jsx';
import b004Timing from './reels/b004.timing.json';
import { TAILS as b004Tails } from './reels/b004.jsx';
import b005Timing from './reels/b005.timing.json';
import { TAILS as b005Tails } from './reels/b005.jsx';
import b006Timing from './reels/b006.timing.json';
import { TAILS as b006Tails } from './reels/b006.jsx';
import b007Timing from './reels/b007.timing.json';
import { TAILS as b007Tails } from './reels/b007.jsx';
import y005Timing from './reels/y005.timing.json';
import { TAILS as y005Tails } from './reels/y005.jsx';
import y006Timing from './reels/y006.timing.json';
import { TAILS as y006Tails } from './reels/y006.jsx';
import y007Timing from './reels/y007.timing.json';
import { TAILS as y007Tails } from './reels/y007.jsx';
import y008Timing from './reels/y008.timing.json';
import { TAILS as y008Tails } from './reels/y008.jsx';
import r008Timing from './reels/r008.timing.json';
import { TAILS as r008Tails } from './reels/r008.jsx';
import r009Timing from './reels/r009.timing.json';
import { TAILS as r009Tails } from './reels/r009.jsx';
import r010Timing from './reels/r010.timing.json';
import { TAILS as r010Tails } from './reels/r010.jsx';
import r011Timing from './reels/r011.timing.json';
import { TAILS as r011Tails } from './reels/r011.jsx';
import b008Timing from './reels/b008.timing.json';
import { TAILS as b008Tails } from './reels/b008.jsx';
import b009Timing from './reels/b009.timing.json';
import { TAILS as b009Tails } from './reels/b009.jsx';
import b010Timing from './reels/b010.timing.json';
import { TAILS as b010Tails } from './reels/b010.jsx';
import b011Timing from './reels/b011.timing.json';
import { TAILS as b011Tails } from './reels/b011.jsx';
import r012Timing from './reels/r012.timing.json';
import { TAILS as r012Tails } from './reels/r012.jsx';
import r013Timing from './reels/r013.timing.json';
import { TAILS as r013Tails } from './reels/r013.jsx';
import r014Timing from './reels/r014.timing.json';
import { TAILS as r014Tails } from './reels/r014.jsx';
import r015Timing from './reels/r015.timing.json';
import { TAILS as r015Tails } from './reels/r015.jsx';
import b012Timing from './reels/b012.timing.json';
import { TAILS as b012Tails } from './reels/b012.jsx';
import b013Timing from './reels/b013.timing.json';
import { TAILS as b013Tails } from './reels/b013.jsx';
import b014Timing from './reels/b014.timing.json';
import { TAILS as b014Tails } from './reels/b014.jsx';
import b015Timing from './reels/b015.timing.json';
import { TAILS as b015Tails } from './reels/b015.jsx';

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
  { id: 'A003', timing: a003Timing, tails: a003Tails },
  { id: 'A004', timing: a004Timing, tails: a004Tails },  // анонс YouTube-канала  // хук «миф: не нужно зубрить все учебники»
  { id: 'R004', timing: r004Timing, tails: r004Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R005', timing: r005Timing, tails: r005Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R006', timing: r006Timing, tails: r006Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R007', timing: r007Timing, tails: r007Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'B004', timing: b004Timing, tails: b004Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B005', timing: b005Timing, tails: b005Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B006', timing: b006Timing, tails: b006Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B007', timing: b007Timing, tails: b007Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'R008', timing: r008Timing, tails: r008Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R009', timing: r009Timing, tails: r009Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R010', timing: r010Timing, tails: r010Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R011', timing: r011Timing, tails: r011Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'B008', timing: b008Timing, tails: b008Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B009', timing: b009Timing, tails: b009Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B010', timing: b010Timing, tails: b010Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B011', timing: b011Timing, tails: b011Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'R012', timing: r012Timing, tails: r012Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R013', timing: r013Timing, tails: r013Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R014', timing: r014Timing, tails: r014Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'R015', timing: r015Timing, tails: r015Tails },  // рилс-вопрос (quiz.jsx)
  { id: 'B012', timing: b012Timing, tails: b012Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B013', timing: b013Timing, tails: b013Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B014', timing: b014Timing, tails: b014Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
  { id: 'B015', timing: b015Timing, tails: b015Tails, subject: 'bio' },  // рилс-вопрос (quiz.jsx)
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
    {(() => {
      const plan = buildPlan(y005Timing, FPS, y005Tails);
      return <Composition id="Y005" component={Reel} durationInFrames={plan.total} fps={FPS} width={1920} height={1080} defaultProps={{ plan, reel: 'Y005' }} />;
    })()}
    {(() => {
      const plan = buildPlan(y006Timing, FPS, y006Tails);
      return <Composition id="Y006" component={Reel} durationInFrames={plan.total} fps={FPS} width={1920} height={1080} defaultProps={{ plan, reel: 'Y006' }} />;
    })()}
    {(() => {
      const plan = buildPlan(y007Timing, FPS, y007Tails);
      return <Composition id="Y007" component={Reel} durationInFrames={plan.total} fps={FPS} width={1920} height={1080} defaultProps={{ plan, reel: 'Y007', subject: 'bio' }} />;
    })()}
    {(() => {
      const plan = buildPlan(y008Timing, FPS, y008Tails);
      return <Composition id="Y008" component={Reel} durationInFrames={plan.total} fps={FPS} width={1920} height={1080} defaultProps={{ plan, reel: 'Y008', subject: 'bio' }} />;
    })()}
    <Composition id="Avatar" component={Avatar} durationInFrames={1} fps={FPS} width={1080} height={1080} />
    {HIGHLIGHTS.map((h) => (
      <Composition key={h.id} id={`Highlight-${h.id}`} component={HighlightCover} durationInFrames={1} fps={FPS} width={1080} height={1920} defaultProps={{ icon: h.id }} />
    ))}
  </>
);
