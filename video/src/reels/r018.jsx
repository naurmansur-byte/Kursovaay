// R018 — Химия, неделя 8: реакция обмена идёт до конца — осадок BaSO₄. Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "atom",
    "visualStem": "реакций",
    "lines": [
      [
        "Идёт до конца?",
        "идёт",
        10,
        {
          "plaque": true
        }
      ]
    ]
  },
  "question": [
    "\\text{До конца идёт реакция:}"
  ],
  "cols": 1,
  "options": [
    [
      "А",
      "\\text{KCl} + \\text{NaNO}_3"
    ],
    [
      "Б",
      "\\text{BaCl}_2 + \\text{Na}_2\\text{SO}_4"
    ],
    [
      "В",
      "\\text{NaCl} + \\text{K}_2\\text{SO}_4"
    ],
    [
      "Г",
      "\\text{KNO}_3 + \\text{MgCl}_2"
    ]
  ],
  "explain": {
    "title": "Признак — осадок",
    "rows": [
      [
        "осадок, газ или вода",
        "осадок",
        20,
        true
      ],
      [
        "$\\text{Ba}^{2+} + \\text{SO}_4^{2-} = \\text{BaSO}_4\\downarrow",
        "бария",
        80
      ],
      [
        "остальные: всё сокращается",
        "остальных",
        150
      ]
    ]
  },
  "trap": {
    "main": "всё сократилось — реакции нет",
    "stem": "сокращения",
    "size": 52,
    "wrong": [
      "А"
    ]
  },
  "answer": {
    "slam": "осадок",
    "stem": "бария",
    "right": "Б",
    "size": 160
  },
  "icon": "atom"
});
