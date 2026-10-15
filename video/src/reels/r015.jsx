// R015 — Химия, неделя 7: в метане углерод sp³, 109°28′. Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "\\text{CH}_4",
    "visualStem": "метан",
    "lines": [
      [
        "Гибридизация?",
        "гибридизация",
        30,
        {
          "plaque": true
        }
      ]
    ]
  },
  "question": [
    "\\text{Гибридизация C в CH}_4"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "sp"
    ],
    [
      "Б",
      "sp^2"
    ],
    [
      "В",
      "sp^3"
    ],
    [
      "Г",
      "\\text{нет}"
    ]
  ],
  "explain": {
    "title": "Тетраэдр",
    "rows": [
      [
        "4 одинаковые σ-связи C—H",
        "четыре",
        10
      ],
      [
        "$1s + 3p \\to 4\\ sp^3",
        "смешиваются",
        60
      ],
      [
        "$\\text{тетраэдр, } 109^\\circ 28'",
        "тетраэдра",
        120,
        true
      ]
    ]
  },
  "trap": {
    "main": "120° — это треугольник, не метан",
    "stem": "эс-пэ-два",
    "size": 52,
    "wrong": [
      "Б"
    ]
  },
  "answer": {
    "slam": "sp³",
    "stem": "эс-пэ-три",
    "right": "В",
    "size": 220
  },
  "icon": "atom"
});
