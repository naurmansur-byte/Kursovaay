// Помощник загрузки в YouTube Studio (Claude in Chrome, вкладка studio.youtube.com, интерфейс на русском).
// Загрузка: вставить ВЕСЬ текст файла в javascript_tool (eval и <script> Studio запрещает — CSP/Trusted Types); затем: window.__META = JSON.parse(await document.getElementById('meta-in').files[0].text());
// Запуск: __run('R004', {day: 19}); длинное из 4 частей: __run('Y009', {day: 19, parts: 4, size: 30195580}).
// Проверка без сохранения: добавить dry: true, потом __closeUpload().
// Итог — в __log[id]: {ok:true,...} | {error:'limit'} | {error:'date/time mismatch',...} | {error:...}. Пока идёт — __busy === id.
// Порядок см. tools/social/YT_UPLOAD.md.
window.__sleep = ms => new Promise(r => setTimeout(r, ms));
window.__waitFor = async (fn, ms = 30000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { const v = fn(); if (v) return v; await __sleep(300); } return null; };
window.__setBox = (el, text) => { el.focus(); document.execCommand('selectAll', false); document.execCommand('insertText', false, text); el.dispatchEvent(new Event('input', { bubbles: true })); };
for (const id of ['vid-in', ...Array.from({ length: 14 }, (_, i) => 'p' + (i + 1)), 'meta-in', 'thumb-in']) {
  if (!document.getElementById(id)) { const i = document.createElement('input'); i.type = 'file'; i.id = id; i.setAttribute('aria-label', 'claude ' + id); i.style.cssText = 'position:fixed;left:0;top:0;width:8px;height:8px;opacity:0.01;z-index:99999'; document.body.appendChild(i); }
}
window.__setFiles = (input, file) => { const dt = new DataTransfer(); dt.items.add(file); input.files = dt.files; input.dispatchEvent(new Event('change', { bubbles: true })); };
window.__pickPlaylists = async (names) => {
  const d = document.querySelector('ytcp-uploads-dialog');
  d.querySelector('ytcp-video-metadata-playlists ytcp-dropdown-trigger, ytcp-video-metadata-playlists ytcp-text-dropdown-trigger').click();
  let pd = await __waitFor(() => { const x = document.querySelector('ytcp-playlist-dialog'); return x && x.querySelector('li') ? x : null; }, 15000);
  if (!pd) {
    // 20.11: окно бывает без <li> — ищем строки по названию и жмём их чекбокс.
    const x = document.querySelector('ytcp-playlist-dialog');
    const labels = x ? [...x.querySelectorAll('*')].filter(e => e.children.length === 0 && names.includes(e.textContent.trim()) && e.offsetParent !== null) : [];
    if (labels.length) {
      for (const lab of labels) {
        let row = lab; for (let k = 0; k < 6 && row && !row.querySelector('[role=checkbox], ytcp-checkbox-lit, tp-yt-paper-checkbox'); k++) row = row.parentElement;
        const cb = row && row.querySelector('[role=checkbox], ytcp-checkbox-lit, tp-yt-paper-checkbox');
        const checked = cb && (cb.getAttribute('aria-checked') === 'true' || cb.hasAttribute('checked'));
        if (cb && !checked) cb.click();
      }
      await __sleep(500);
      const ok = [...x.querySelectorAll('ytcp-button, button')].find(b => /ОК|Готово/.test(b.innerText) && b.offsetParent !== null);
      ok && ok.click(); await __sleep(800);
      return true;
    }
  }
  if (!pd) {  // при лимите загрузки список пуст: «У вас нет плейлистов»
    const x = document.querySelector('ytcp-playlist-dialog');
    const ok = x && [...x.querySelectorAll('ytcp-button, button')].find(b => /ОК|Готово/.test(b.innerText) && b.offsetParent !== null);
    ok && ok.click(); await __sleep(800);
    return false;
  }
  for (const li of pd.querySelectorAll('li')) {
    const t = li.innerText.trim();
    const cb = li.querySelector('[role=checkbox], ytcp-checkbox-lit, tp-yt-paper-checkbox');
    if (!cb) continue;
    const checked = cb.getAttribute('aria-checked') === 'true' || cb.hasAttribute('checked');
    if (names.includes(t) !== checked) cb.click();
  }
  await __sleep(500);
  const done = [...pd.querySelectorAll('ytcp-button, button')].find(b => /Готово/.test(b.innerText));
  done && done.click();
  await __sleep(800);
  return true;
};
// Диалог после «Запланировать»: «Публикация видео запланирована» или «Обработка видео … мы установим …».
// У подтверждённого канала (с 19.11) перед планированием всплывает «Проверка видео ещё продолжается… ОК» — нажимаем ОК;
// итоговое окно тогда пишет «Видео опубликовано», хотя в списке видео стоит «Отложенная публикация» (проверено 19.11).
window.__ackPrecheck = () => { const w = [...document.querySelectorAll('ytcp-prechecks-warning-dialog')].find(x => x.offsetParent !== null && /Проверка видео/.test(x.innerText)); if (!w) return false; const ok = [...w.querySelectorAll('ytcp-button, button')].find(b => /^\s*ОК\s*$/.test(b.innerText) && b.offsetParent !== null); if (ok) { ok.click(); return true; } return false; };
window.__doneDlg = () => { __ackPrecheck(); return [...document.querySelectorAll('ytcp-video-share-dialog, ytcp-uploads-still-processing-dialog')].find(x => /запланирована|установим|опубликовано/.test(x.innerText) && x.offsetParent !== null); };
window.__closeDone = async () => { for (const x of document.querySelectorAll('ytcp-video-share-dialog, ytcp-uploads-still-processing-dialog')) { const c = [...x.querySelectorAll('ytcp-button, button')].find(b => /Закрыть/.test(b.innerText) && b.offsetParent !== null); c && c.click(); } await __sleep(600); };
// Закрыть окно загрузки без сохранения (после лимита черновик не создаётся — проверено 18.11).
window.__closeUpload = async () => { const d = document.querySelector('ytcp-uploads-dialog'); const c = d && d.querySelector('#ytcp-uploads-dialog-close-button, #close-button, [aria-label="Закрыть"]'); c && c.click(); await __sleep(2000); return !!c; };
window.__openUpload = async () => {
  await __closeDone();
  const cb = [...document.querySelectorAll('button')].find(b => b.getAttribute('aria-label') === 'Создать');
  cb.click();
  await __sleep(800);
  const item = [...document.querySelectorAll('tp-yt-paper-item, [role=menuitem]')].find(e => /Добавить видео|Загрузить видео/.test(e.innerText));
  item.click();
  return await __waitFor(() => document.querySelector('ytcp-uploads-dialog input[type=file]'), 8000);
};
// Выбор дня в календаре ноября 2026 (ввод текста в поле даты не работает — нужен клик по числу).
window.__pickDay = (dayNum, monthRe = /НОЯБ\. 2026/) => {
  const dp = document.querySelector('ytcp-date-picker');
  if (!dp) return 'no picker';
  const month = [...dp.querySelectorAll('div.calendar-month')].find(m => monthRe.test(m.innerText.split('\n')[0]));
  if (!month) return 'no month';
  const day = [...month.querySelectorAll('span.calendar-day')].find(s => s.innerText.trim() === String(dayNum));
  if (!day) return 'no day';
  day.click();
  return 'clicked';
};
window.__fill = async (m) => {
  const d = document.querySelector('ytcp-uploads-dialog');
  const boxes = await __waitFor(() => { if (!m.dry && /Загрузка недоступна/.test(d.innerText)) return 'LIMIT'; const b = d.querySelectorAll('#textbox'); return b.length >= 2 ? b : null; }, 60000);
  if (boxes === 'LIMIT' && !m.dry) return { error: 'limit' };
  if (!boxes) return { error: 'no details form' };
  await __sleep(1500);
  const limited = () => !m.dry && /Загрузка недоступна/.test(d.innerText);
  if (limited()) return { error: 'limit' };
  __setBox(boxes[0], m.title);
  __setBox(boxes[1], m.description);
  // Своё превью (канал подтверждён 19.11): input загрузчика значка в окне загрузки.
  if (m.thumbFile) {
    const tin = d.querySelector('ytcp-thumbnails-compact-editor-uploader input[type=file], #file-loader');
    if (!tin) return { error: 'no thumbnail input' };
    __setFiles(tin, m.thumbFile);
    await __sleep(4000);
  }
  d.querySelector('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]').click();
  await __sleep(400);
  const alt = () => d.querySelector('tp-yt-paper-radio-button[name="VIDEO_HAS_ALTERED_CONTENT_YES"]');
  if (!alt()) { d.querySelector('#toggle-button').click(); await __waitFor(alt, 5000); }
  alt().click();
  const plOk = await __pickPlaylists(m.playlists);
  const plText = d.querySelector('ytcp-video-metadata-playlists').innerText.replace(/\s+/g, ' ').trim();
  if (limited()) return { error: 'limit' };
  if (!m.dry && (!plOk || /Выберите плейлист/.test(plText))) return { error: 'playlist not set', plText };
  for (let i = 0; i < 3; i++) { d.querySelector('#next-button').click(); await __sleep(1500); }
  d.querySelector('#second-container-expand-button').click();
  await __sleep(1200);
  const dateText = m.day + ' нояб.';
  const trig = d.querySelector('#datepicker-trigger');
  if (!trig.innerText.trim().startsWith(dateText)) {
    trig.click();
    await __waitFor(() => document.querySelector('ytcp-date-picker div.calendar-month'), 5000);
    await __sleep(500);
    __pickDay(m.day);
    await __sleep(1200);
  }
  const ti = [...d.querySelectorAll('ytcp-visibility-scheduler input, ytcp-datetime-picker input')].find(e => /^\d\d:\d\d$/.test(e.value));
  ti.focus(); ti.select(); document.execCommand('insertText', false, m.time);
  ti.dispatchEvent(new Event('input', { bubbles: true }));
  ti.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));
  ti.dispatchEvent(new Event('change', { bubbles: true }));
  ti.blur();
  await __sleep(800);
  const dateNow = d.querySelector('#datepicker-trigger').innerText, timeNow = ti.value;
  if (!dateNow.trim().startsWith(dateText) || timeNow !== m.time) return { error: 'date/time mismatch', dateNow, timeNow };
  if (m.dry) return { dry: true, date: dateNow, time: timeNow, pl: plText };  // проверка без сохранения
  d.querySelector('#done-button').click();
  const share = await __waitFor(__doneDlg, 300000);
  return { ok: !!share, date: dateNow, time: timeNow, pl: plText, res: share ? share.innerText.replace(/\n+/g, ' | ').slice(0, 160) : 'no share dialog' };
};
window.__log = window.__log || {};
window.__run = (id, opts = {}) => {
  window.__busy = id;
  (async () => {
    try {
      const m = { ...__META[id], day: opts.day ?? __META[id].day, time: '10:00', dry: !!opts.dry };
      if (opts.thumb) { m.thumbFile = document.getElementById('thumb-in').files[0]; if (!m.thumbFile || !m.thumbFile.name.toLowerCase().includes(id.toLowerCase())) { __log[id] = { error: 'wrong thumb ' + (m.thumbFile && m.thumbFile.name) }; return; } }
      if (!m.title || !m.day) { __log[id] = { error: 'no meta/day' }; return; }
      let file;
      if (opts.parts) {
        const fs = Array.from({ length: opts.parts }, (_, i) => document.getElementById('p' + (i + 1)).files[0]);
        const bad = fs.findIndex((f, i) => !f || f.name !== `${id}.mp4.part${i + 1}`);
        if (bad >= 0) { __log[id] = { error: 'wrong parts ' + fs.map(f => f && f.name).join(',') }; return; }
        file = new File(fs, id + '.mp4', { type: 'video/mp4' });
        if (opts.size && file.size !== opts.size) { __log[id] = { error: 'size ' + file.size }; return; }
      } else {
        file = document.getElementById('vid-in').files[0];
        if (!file || file.name !== id + '.mp4') { __log[id] = { error: 'wrong file ' + (file && file.name) }; return; }
      }
      const yt = await __openUpload();
      __setFiles(yt, file);
      __log[id] = await __fill(m);
    } catch (e) { __log[id] = { error: String(e) }; }
    finally { window.__busy = null; }
  })();
  return 'started ' + id;
};
'helpers v5 ready';
