// R016 — Химия, неделя 9: степень окисления серы в H₂SO₄ (+6). Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "\\text{H}_2\\text{SO}_4",
    "visualStem": "серная",
    "lines": [
      [
        "Степень окисления?",
        "степень",
        30,
        {
          "plaque": true,
          "size": 84
        }
      ]
    ]
  },
  "question": [
    "\\text{Степень окисления S}",
    "\\text{в H}_2\\text{SO}_4\\text{:}"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "+2"
    ],
    [
      "Б",
      "+4"
    ],
    [
      "В",
      "+6"
    ],
    [
      "Г",
      "-2"
    ]
  ],
  "explain": {
    "title": "Сумма = 0",
    "rows": [
      [
        "$\\text{H}^{+1},\\ \\ \\text{O}^{-2}",
        "водород",
        10
      ],
      [
        "$2\\cdot(+1) + 4\\cdot(-2) = -6",
        "два",
        60
      ],
      [
        "сумма в молекуле = 0",
        "сумма",
        120
      ],
      [
        "$\\text{S} = +6",
        "сера",
        160,
        true
      ]
    ]
  },
  "trap": {
    "main": "не забудь кислород",
    "stem": "плюс",
    "wrong": [
      "А"
    ]
  },
  "answer": {
    "slam": "+6",
    "stem": "шесть",
    "right": "В",
    "size": 260
  },
  "icon": "atom"
});
