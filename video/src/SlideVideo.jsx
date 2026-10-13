// Видео-урок для YouTube 1920×1080: слайды презентации + озвучка, плавные переходы и лёгкое приближение.
import React from 'react';
import { AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { useFonts } from './Reel.jsx';

const FADE = 10;

const Slide = ({ src, dur }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, FADE], [0, 1], { extrapolateRight: 'clamp' });
  const zoom = interpolate(frame, [0, dur + FADE], [1, 1.015]);
  return (
    <AbsoluteFill style={{ opacity, transform: `scale(${zoom})` }}>
      <Img src={src} style={{ width: '100%', height: '100%' }} />
    </AbsoluteFill>
  );
};

export const SlideVideo = ({ plan, dir }) => {
  useFonts();
  return (
    <AbsoluteFill style={{ background: '#151515' }}>
      {plan.scenes.map((s) => (
        <Sequence key={s.id} from={s.from} durationInFrames={s.dur + FADE} name={s.id}>
          <Slide src={staticFile(`${dir}/${s.id}.png`)} dur={s.dur} />
          {s.audio && (
            <Sequence from={s.lead}>
              <Audio src={staticFile(s.audio)} />
            </Sequence>
          )}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
