// B014 — Биология, неделя 4: кислород фотосинтеза — из воды (фотолиз). Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "\\text{H}_2\\text{O}\\ \\ \\text{или}\\ \\ \\text{CO}_2\\,?",
    "visualStem": "растение",
    "lines": [
      [
        "Откуда кислород?",
        "откуда",
        40,
        {
          "plaque": true,
          "size": 84
        }
      ]
    ]
  },
  "question": [
    "\\text{Кислород фотосинтеза — из:}"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "\\text{CO}_2"
    ],
    [
      "Б",
      "\\text{воды}"
    ],
    [
      "В",
      "\\text{глюкозы}"
    ],
    [
      "Г",
      "\\text{хлорофилла}"
    ]
  ],
  "explain": {
    "title": "Фотолиз воды",
    "rows": [
      [
        "световая фаза — тилакоиды",
        "световой",
        5
      ],
      [
        "$\\text{фотолиз: H}_2\\text{O} \\to \\text{O}_2",
        "фотолиз",
        60,
        true
      ],
      [
        "$\\text{углерод CO}_2 \\to \\text{глюкоза}",
        "углерод",
        130
      ]
    ]
  },
  "trap": {
    "main": "выделяется кислород воды",
    "stem": "выделяется",
    "wrong": [
      "А"
    ]
  },
  "answer": {
    "slam": "из воды",
    "stem": "воды",
    "right": "Б",
    "size": 140
  },
  "icon": "dna"
});
