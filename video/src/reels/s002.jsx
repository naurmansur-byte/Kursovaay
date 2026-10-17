// S002 — Рубрика «Найди ошибку» · химия недели 1. Рилс на шаблоне series.jsx.
import { makeSeries } from './series.jsx';

export const { SCENES, TAILS } = makeSeries({
  "kind": "error",
  "name": [
    "Найди",
    "ошибку"
  ],
  "nameStem": "ошибку",
  "sub": "в решении одна ошибка",
  "subStem": "одна",
  "icon": "atom",
  "task": [
    "Сколько всего атомов в записи",
    "$2\\,\\mathrm{Ca(OH)_2}\\ ?"
  ],
  "steps": [
    "$\\mathrm{Ca(OH)_2}:\\ \\mathrm{Ca}=1,\\ \\mathrm{O}=2,\\ \\mathrm{H}=2",
    "$\\mathrm{2Ca(OH)_2}:\\ \\mathrm{Ca}=2,\\ \\mathrm{O}=2,\\ \\mathrm{H}=2",
    "$\\text{всего}:\\ 2 + 2 + 2 = 6"
  ],
  "wrongStep": 1,
  "stepSize": 34,
  "stepStems": [
    [
      "одной",
      20
    ],
    [
      "двух",
      80
    ],
    [
      "всего",
      150
    ]
  ],
  "fix": "Коэффициент 2 умножает всю формулу: O — 4, H — 4",
  "fixStem": "коэффициент",
  "answer": "10 атомов",
  "answerStem": "десять"
});
