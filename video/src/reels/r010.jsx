// R010 — Химия, неделя 3: несолеобразующие оксиды — CO и NO. Рилс-вопрос на шаблоне quiz.jsx.
import { makeQuiz } from './quiz.jsx';

export const { SCENES, TAILS } = makeQuiz({
  "hook": {
    "visual": "\\text{CO}_2 \\quad \\text{CO} \\quad \\text{SO}_3",
    "visualStem": "углекислый",
    "lines": [
      [
        "Не образует солей?",
        "образует",
        20,
        {
          "plaque": true,
          "size": 84
        }
      ]
    ]
  },
  "question": [
    "\\text{Несолеобразующий оксид:}"
  ],
  "cols": 2,
  "options": [
    [
      "А",
      "\\text{CO}_2"
    ],
    [
      "Б",
      "\\text{SO}_3"
    ],
    [
      "В",
      "\\text{CO}"
    ],
    [
      "Г",
      "\\text{CaO}"
    ]
  ],
  "explain": {
    "title": "Классы оксидов",
    "rows": [
      [
        "$\\text{основные: CaO, Na}_2\\text{O}",
        "основными",
        40
      ],
      [
        "$\\text{кислотные: CO}_2\\text{, SO}_3",
        "кислотными",
        60
      ],
      [
        "$\\text{несолеобразующие: CO, NO}",
        "угарный",
        120,
        true
      ]
    ]
  },
  "trap": {
    "main": "углекислый газ — кислотный оксид",
    "stem": "углекислый",
    "size": 52,
    "wrong": [
      "А"
    ]
  },
  "answer": {
    "slam": "CO",
    "stem": "угарный",
    "right": "В",
    "size": 260
  },
  "icon": "atom"
});
