// Стиль 2 «ХимБио просто» (выбран Мансуром 13.10.2026): чёрная фактура, светлый текст, красный акцент.
export const C = {
  bg: '#151515',
  card: '#1D1D1D',
  fg: '#F3F0E8',
  muted: 'rgba(243, 240, 232, 0.62)',
  faint: 'rgba(243, 240, 232, 0.18)',
  accent: '#F13A43',
};

export const F = {
  display: '"Unbounded Variable", "Arial Black", sans-serif',
  body: '"Manrope Variable", "Segoe UI", sans-serif',
};

// Биология (решение Мансура 13.10.2026): тот же стиль 2, акцент тёмно-зелёный вместо красного.
export const BIO = { ...C, accent: '#1F7A4A' };
export const BIO_ACCENT_HEX = '#1F7A4A';

// Безопасная зона Reels: сверху метка и прогресс, снизу интерфейс Instagram.
export const SAFE = { x: 72, top: 230, subtitleY: 1400 };
export const ACCENT_HEX = '#F13A43';
