// R017 — Химия, неделя 8: гидролиз Na₂CO₃ — щелочная среда. Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "\\text{Na}_2\\text{CO}_3 + \\text{H}_2\\text{O}",
    "visualStem": "карбоната",
    "lines": [
      [
        "Какая среда?",
        "среда",
        20,
        {
          "plaque": true
        }
      ]
    ]
  },
  "question": [
    "\\text{Среда раствора Na}_2\\text{CO}_3\\text{:}"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "\\text{кислая}"
    ],
    [
      "Б",
      "\\text{нейтральная}"
    ],
    [
      "В",
      "\\text{щелочная}"
    ],
    [
      "Г",
      "\\text{pH} < 7"
    ]
  ],
  "explain": {
    "title": "Гидролиз по аниону",
    "rows": [
      [
        "сильное основание + слабая кислота",
        "сильным",
        10
      ],
      [
        "$\\text{CO}_3^{2-} + \\text{H}_2\\text{O} \\rightleftarrows",
        "карбонат-ион",
        60
      ],
      [
        "$\\rightleftarrows \\text{HCO}_3^- + \\text{OH}^-",
        "гидроксид-ионы",
        90,
        true
      ],
      [
        "гидроксид-ионы → щелочная",
        "поэтому",
        120
      ],
      [
        "фенолфталеин — малиновый",
        "фенолфталеин",
        160
      ]
    ]
  },
  "trap": {
    "main": "соль ≠ нейтральная среда",
    "stem": "соль",
    "wrong": [
      "Б"
    ]
  },
  "answer": {
    "slam": "щелочная",
    "stem": "щелочная",
    "right": "В",
    "size": 120
  },
  "icon": "atom"
});
