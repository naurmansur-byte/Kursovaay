// Стиль 2 «ХимБио просто» (выбран Мансуром 13.10.2026): чёрная фактура, светлый текст, акцент по предмету.
// Цвет предмета: химия — красный, биология — тёмно-зелёный (решение Мансура 13.10.2026).
export const SUBJECT = { chem: '#F13A43', bio: '#1F7A4A' };

// Акцент задаёт ролик (Reel → setSubject) до отрисовки сцен; все элементы читают C.accent.
let accent = SUBJECT.chem;
export const setSubject = (subject = 'chem') => {
  accent = SUBJECT[subject] ?? SUBJECT.chem;
};

export const C = {
  bg: '#151515',
  card: '#1D1D1D',
  fg: '#F3F0E8',
  muted: 'rgba(243, 240, 232, 0.62)',
  faint: 'rgba(243, 240, 232, 0.18)',
  get accent() {
    return accent;
  },
  // Полупрозрачная подложка акцента (выбранный вариант ответа).
  get accentSoft() {
    return `${accent}29`;
  },
};

export const F = {
  display: '"Unbounded Variable", "Arial Black", sans-serif',
  body: '"Manrope Variable", "Segoe UI", sans-serif',
};

// Безопасная зона Reels: сверху метка и прогресс, снизу интерфейс Instagram.
export const SAFE = { x: 72, top: 230, subtitleY: 1400 };
