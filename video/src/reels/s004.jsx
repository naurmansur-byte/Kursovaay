// S004 — Рубрика «Факт за 10 секунд» · водородные связи в ДНК. Рилс на шаблоне series.jsx.
import { makeSeries } from './series.jsx';

export const { SCENES, TAILS } = makeSeries({
  "kind": "fact",
  "name": [
    "Факт",
    "за 10 секунд"
  ],
  "nameStem": "десять",
  "sub": "то, что нельзя вывести логикой",
  "subStem": "нельзя",
  "icon": "dna",
  "factTitle": "Связи в ДНК",
  "fact": [
    [
      "\\text{А} = \\text{Т}",
      "аденин",
      20,
      "2 связи"
    ],
    [
      "\\text{Г} \\equiv \\text{Ц}",
      "гуанин",
      80,
      "3 связи"
    ]
  ],
  "factCaption": "водородные связи между основаниями двух цепей",
  "check": {
    "question": "Сколько водородных связей в паре Г–Ц?",
    "answer": "3",
    "stem": "три"
  }
});
