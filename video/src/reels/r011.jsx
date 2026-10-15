// R011 — Химия, неделя 7: ионная связь — металл + неметалл. Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "\\text{HCl} \\quad \\text{NaCl} \\quad \\text{Cl}_2",
    "visualStem": "хлороводород",
    "lines": [
      [
        "Где ионная связь?",
        "ионная",
        60,
        {
          "plaque": true,
          "size": 84
        }
      ]
    ]
  },
  "question": [
    "\\text{Ионная связь — в веществе:}"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "\\text{HCl}"
    ],
    [
      "Б",
      "\\text{Cl}_2"
    ],
    [
      "В",
      "\\text{NaCl}"
    ],
    [
      "Г",
      "\\text{H}_2\\text{O}"
    ]
  ],
  "explain": {
    "title": "Тип связи",
    "rows": [
      [
        "металл + неметалл → ионная",
        "металлом",
        10,
        true
      ],
      [
        "$\\text{NaCl:}\\ \\text{Na}^+\\,\\text{Cl}^-",
        "ионы",
        70
      ],
      [
        "неметаллы → ковалентная",
        "ковалентная",
        100
      ],
      [
        "$\\text{Cl}_2\\text{ — неполярная}",
        "неполярная",
        120
      ],
      [
        "$\\text{HCl, H}_2\\text{O — полярная}",
        "разными",
        150
      ]
    ]
  },
  "trap": {
    "main": "HCl — два неметалла → ковалентная",
    "stem": "хлороводороде",
    "size": 52,
    "wrong": [
      "А"
    ]
  },
  "answer": {
    "slam": "NaCl",
    "stem": "хлориде",
    "right": "В",
    "size": 220
  },
  "icon": "atom"
});
