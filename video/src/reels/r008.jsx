// R008 — Химия, неделя 6: число нейтронов N = A − Z (³⁵Cl). Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "{}^{35}_{17}\\text{Cl}",
    "visualStem": "хлор",
    "lines": [
      [
        "Сколько нейтронов?",
        "нейтронов",
        60,
        {
          "plaque": true,
          "size": 84
        }
      ]
    ]
  },
  "question": [
    "\\text{Число нейтронов в } {}^{35}\\text{Cl}"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "17"
    ],
    [
      "Б",
      "18"
    ],
    [
      "В",
      "35"
    ],
    [
      "Г",
      "52"
    ]
  ],
  "explain": {
    "title": "A = Z + N",
    "rows": [
      [
        "$A = Z + N",
        "массовое",
        10,
        true
      ],
      [
        "$Z(\\text{Cl}) = 17",
        "семнадцать",
        60
      ],
      [
        "$N = 35 - 17 = 18",
        "нейтронов",
        120
      ]
    ]
  },
  "trap": {
    "main": "17 — протоны, 35 — все нуклоны",
    "stem": "семнадцать",
    "wrong": [
      "А",
      "В"
    ]
  },
  "answer": {
    "slam": "18",
    "stem": "восемнадцать",
    "right": "Б",
    "size": 260
  },
  "icon": "atom"
});
