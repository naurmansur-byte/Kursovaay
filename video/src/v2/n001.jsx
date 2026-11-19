// N001 — химия, задание № 3 официального образца НЦТ (testcenter.kz, obr_var_test_06.pdf), текст дословно.
// Ответ C) 4,48: n(KCl) = 29,8 / 74,5 = 0,4 моль; 2KCl → 2K + Cl₂ (конспект недели 10: электролиз расплава); n(Cl₂) = 0,2; V = 4,48 л.
import { makeNct } from './nct.jsx';

export const { TAILS, Comp } = makeNct({
  subject: 'chem',
  subjectName: 'химия',
  num: 3,
  question: 'При электролизе расплава 29,8 г хлорида калия выделился хлор объёмом (л, н.у.)',
  options: [['A', '3,36'], ['B', '2,24'], ['C', '4,48'], ['D', '1,12']],
  right: 'C',
  timerY: 1080,
  steps: [
    { html: '2KCl → 2K + Cl<sub>2</sub>', stem: 'два' },
    { html: 'n(KCl) = 29,8 : 74,5 = 0,4 моль', stem: 'соли' },
    { html: 'n(Cl<sub>2</sub>) = 0,4 : 2 = 0,2 моль', stem: 'хлора' },
    { html: 'V = 0,2 · 22,4 = 4,48 л', stem: 'умножаем' },
  ],
  finalStep: true,
  answerNote: { text: 'хлора вдвое меньше, чем соли', stem: 'вдвое' },
  noteY: 1080,
});
