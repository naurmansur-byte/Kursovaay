// R019 — Химия, неделя 8: pH 0,01 М HCl = 2. Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "0{,}01\\ \\text{М HCl}",
    "visualStem": "соляной",
    "lines": [
      [
        "Водородный показатель?",
        "пэ-аш",
        10,
        {
          "plaque": true,
          "size": 68
        }
      ]
    ]
  },
  "question": [
    "\\text{pH раствора 0,01 М HCl:}"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "0{,}01"
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
      "12"
    ]
  ],
  "explain": {
    "title": "Сильная кислота",
    "rows": [
      [
        "сильная кислота — распад полностью",
        "сильный",
        10
      ],
      [
        "$[\\text{H}^+] = 0{,}01 = 10^{-2}",
        "концентрация",
        60
      ],
      [
        "$\\text{pH} = -\\lg[\\text{H}^+] = 2",
        "логарифм",
        130,
        true
      ]
    ]
  },
  "trap": {
    "main": "концентрация ≠ pH",
    "stem": "ноль",
    "wrong": [
      "А",
      "Г"
    ]
  },
  "answer": {
    "slam": "pH 2",
    "stem": "двум",
    "right": "В",
    "size": 200
  },
  "icon": "atom"
});
