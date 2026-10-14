// R006 — Химия, неделя 7: полярные связи, но неполярная молекула CO₂. Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "\\text{O} = \\text{C} = \\text{O}",
    "visualStem": "углекислого",
    "lines": [
      [
        "Связи полярные",
        "полярные",
        50
      ],
      [
        "А молекула?",
        "молекула",
        90,
        {
          "plaque": true
        }
      ]
    ]
  },
  "question": [
    "\\text{Молекула CO}_2\\text{ —}"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "\\text{полярная}"
    ],
    [
      "Б",
      "\\text{неполярная}"
    ],
    [
      "В",
      "\\text{ионная}"
    ],
    [
      "Г",
      "\\text{металлическая}"
    ]
  ],
  "explain": {
    "title": "Смотри на форму",
    "rows": [
      [
        "$\\text{ЭО: O} = 3{,}5 > \\text{C} = 2{,}5",
        "электроотрицательнее",
        10
      ],
      [
        "каждая связь C—O полярная",
        "полярная",
        70
      ],
      [
        "$\\overset{\\delta-}{\\text{O}} \\leftarrow \\overset{\\delta+}{\\text{C}} \\rightarrow \\overset{\\delta-}{\\text{O}}",
        "линейная",
        110,
        true
      ],
      [
        "диполи гасят друг друга",
        "гасят",
        160
      ]
    ]
  },
  "trap": {
    "main": "полярная связь ≠ полярная молекула",
    "stem": "полярность",
    "size": 54,
    "wrong": [
      "А"
    ],
    "sub": [
      "H₂O — угловая → полярная",
      "воды"
    ]
  },
  "answer": {
    "slam": "неполярная",
    "stem": "неполярная",
    "right": "Б",
    "size": 110
  },
  "icon": "atom"
});
