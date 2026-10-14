// R007 — Химия, неделя 7: в тройной связи одна σ и две π. Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "\\text{N} \\equiv \\text{N}",
    "visualStem": "азота",
    "lines": [
      [
        "Тройная связь",
        "тройная",
        30
      ],
      [
        "Сколько пи-связей?",
        "сколько",
        70,
        {
          "plaque": true,
          "size": 80
        }
      ]
    ]
  },
  "question": [
    "\\text{Число } \\pi\\text{-связей в N}_2"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "0"
    ],
    [
      "Б",
      "1"
    ],
    [
      "В",
      "2"
    ],
    [
      "Г",
      "3"
    ]
  ],
  "explain": {
    "title": "Сигма и пи",
    "rows": [
      [
        "одна σ — вдоль оси ядер",
        "сигма",
        30
      ],
      [
        "остальные — π",
        "остальные",
        110
      ],
      [
        "$\\text{N} \\equiv \\text{N}:\\ 1\\sigma + 2\\pi",
        "две",
        170,
        true
      ]
    ]
  },
  "trap": {
    "main": "тройная ≠ три π-связи",
    "stem": "три",
    "wrong": [
      "Г"
    ]
  },
  "answer": {
    "slam": "2",
    "stem": "две",
    "right": "В",
    "size": 260
  },
  "icon": "atom"
});
