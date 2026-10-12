// Раскладка сцен по кадрам из таймингов озвучки.
const LEAD = 4;
const TAIL = 8;
const EXTRA_TAIL = { engage: 24, answer: 16, outro: 36 };

export function buildPlan(timing, fps) {
  let from = 0;
  const scenes = timing.scenes.map((s, index) => {
    const lead = index === 0 ? 10 : LEAD;
    const tail = EXTRA_TAIL[s.id] ?? TAIL;
    const voice = Math.ceil((s.speechEndMs / 1000) * fps);
    const dur = lead + voice + tail;
    const scene = { ...s, index, from, lead, dur };
    from += dur;
    return scene;
  });
  return { fps, total: from, scenes };
}

const norm = (w) => w.toLowerCase().replace(/ё/g, 'е').replace(/[^a-zа-я0-9]/g, '');

// Кадр (от начала сцены), когда звучит n-е слово, начинающееся на stem; иначе fallback.
export function wordFrame(scene, fps, stem, fallback = 0, nth = 0) {
  const key = norm(stem);
  let seen = 0;
  for (const w of scene.words) {
    if (norm(w.t).startsWith(key)) {
      if (seen === nth) return scene.lead + Math.round((w.start / 1000) * fps);
      seen += 1;
    }
  }
  return fallback;
}

// Субтитры по 1–2 слова с абсолютными кадрами.
export function subtitleChunks(plan) {
  const out = [];
  for (const s of plan.scenes) {
    const ws = s.words;
    for (let i = 0; i < ws.length; ) {
      const a = ws[i];
      const b = ws[i + 1];
      const at = a.t.trim();
      const pair = b && at.length + b.t.trim().length <= 14 && !/[.,:;!?—]$/.test(at);
      const words = pair ? [a, b] : [a];
      out.push({
        text: words.map((w) => w.t.replace(/[—:]/g, '').trim().replace(/[.,]$/, '')).filter(Boolean).join(' '),
        from: s.from + s.lead + Math.round((a.start / 1000) * plan.fps),
        sceneEnd: s.from + s.dur,
      });
      i += words.length;
    }
  }
  return out.map((c, i) => ({ ...c, to: Math.min(out[i + 1]?.from ?? c.sceneEnd, c.sceneEnd) }));
}
