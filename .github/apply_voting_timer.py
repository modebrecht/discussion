from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

MARKER = '/* ===== Voting + persistent exam timer ===== */'
if MARKER in text:
    raise SystemExit('Voting/timer patch already applied')

# 1) CSS.
style = r'''

  <style>
    /* ===== Voting + persistent exam timer ===== */
    .toolbar-action-btn.is-active{
      border-color:#0f172a;
      background:#0f172a;
      color:#fff;
      box-shadow:0 5px 12px rgba(15,23,42,.16);
    }
    .toolbar-action-btn.timer-finished{
      border-color:#fb7185;
      background:#fff1f2;
      color:#be123c;
    }
    .vote-badge{
      position:absolute;
      z-index:8;
      right:-6px;
      bottom:-7px;
      min-width:22px;
      height:22px;
      padding:0 5px;
      display:grid;
      place-items:center;
      border:2px solid #fff;
      border-radius:999px;
      background:#0f172a;
      color:#fff;
      box-shadow:0 4px 10px rgba(15,23,42,.2);
      font-size:11px;
      font-weight:850;
      line-height:1;
      pointer-events:none;
    }
    .vote-badge[hidden]{display:none}
    html.voting-mode .chip{cursor:pointer}

    .timer-panel{
      position:absolute;
      z-index:150;
      top:calc(100% + .55rem);
      right:3rem;
      width:min(330px,calc(100vw - 1rem));
      padding:.85rem;
      border:1px solid #dbe3ee;
      border-radius:17px;
      background:#fff;
      box-shadow:0 20px 48px rgba(15,23,42,.18);
      display:grid;
      gap:.72rem;
    }
    .timer-panel[hidden]{display:none}
    .timer-panel-title{font-size:.86rem;font-weight:850;color:#0f172a}
    .timer-panel-display{
      font-variant-numeric:tabular-nums;
      font-size:2rem;
      font-weight:850;
      letter-spacing:-.04em;
      color:#0f172a;
      text-align:center;
    }
    .timer-config-row,.timer-actions,.timer-presets{display:flex;align-items:center;gap:.42rem}
    .timer-config-row label{font-size:.78rem;font-weight:750;color:#475569}
    .timer-minutes{
      width:78px;
      min-height:36px;
      border:1px solid #dbe3ee;
      border-radius:10px;
      background:#f8fafc;
      color:#0f172a;
      padding:.35rem .5rem;
      font:750 .86rem/1 ui-sans-serif,system-ui,sans-serif;
    }
    .timer-presets{flex-wrap:wrap}
    .timer-preset{
      min-height:30px;
      padding:.32rem .5rem;
      border:1px solid #e2e8f0;
      border-radius:9px;
      background:#f8fafc;
      color:#334155;
      font-size:.76rem;
      font-weight:800;
      cursor:pointer;
    }
    .timer-preset:hover{background:#fff;border-color:#cbd5e1}
    .timer-actions .btn{flex:1 1 auto;min-height:36px}
    .timer-state-line{min-height:1.1em;text-align:center;color:#64748b;font-size:.76rem;font-weight:700}

    .timer-xl-overlay{
      position:fixed;
      z-index:5000;
      inset:0;
      display:grid;
      grid-template-rows:auto 1fr auto;
      min-height:100dvh;
      padding:clamp(1rem,2.4vw,2.5rem);
      background:#05070b;
      color:#fff;
    }
    .timer-xl-overlay[hidden]{display:none}
    .timer-xl-top{display:flex;align-items:center;justify-content:space-between;gap:1rem}
    .timer-xl-title{font-size:clamp(1rem,1.7vw,1.45rem);font-weight:800;color:#cbd5e1;letter-spacing:.02em}
    .timer-xl-close{
      width:48px;height:48px;border:1px solid #334155;border-radius:14px;background:#111827;color:#fff;
      font-size:1.25rem;font-weight:800;cursor:pointer;
    }
    .timer-xl-center{display:grid;place-items:center;text-align:center;align-content:center;gap:.4rem}
    .timer-xl-time{
      font-variant-numeric:tabular-nums;
      font-size:clamp(7rem,24vw,25rem);
      font-weight:900;
      line-height:.83;
      letter-spacing:-.075em;
      white-space:nowrap;
    }
    .timer-xl-end{font-size:clamp(1rem,2vw,1.7rem);font-weight:750;color:#94a3b8}
    .timer-xl-actions{display:flex;justify-content:center;gap:.65rem}
    .timer-xl-actions .btn{
      min-width:150px;
      min-height:48px;
      border-color:#334155;
      background:#111827;
      color:#fff;
      box-shadow:none;
    }
    .timer-xl-overlay.is-finished .timer-xl-time{color:#fb7185}
    html.timer-xl-active,html.timer-xl-active body{overflow:hidden}

    html[data-beamer-theme="dark"] .timer-panel{background:#0f172a;border-color:#334155;color:#e2e8f0}
    html[data-beamer-theme="dark"] .timer-panel-title,
    html[data-beamer-theme="dark"] .timer-panel-display{color:#f8fafc}
    html[data-beamer-theme="dark"] .timer-minutes,
    html[data-beamer-theme="dark"] .timer-preset{background:#111827;border-color:#334155;color:#e2e8f0}
    html[data-beamer-theme="dark"] .vote-badge{border-color:#0f172a;background:#f8fafc;color:#0f172a}

    @media (max-width:760px){
      .timer-panel{right:-.2rem;width:min(315px,calc(100vw - 1rem))}
      .timer-xl-time{font-size:clamp(5rem,28vw,11rem)}
      .timer-xl-actions .btn{min-width:120px}
    }
  </style>
'''
text = text.replace('</head>', style + '\n</head>', 1)

# 2) Toolbar buttons and compact timer panel.
settings_anchor = '        <button id="settingsBtn" type="button" class="btn settings-btn" aria-haspopup="true" aria-expanded="false" aria-label="Einstellungen" title="Einstellungen">⚙</button>\n'
if settings_anchor not in text:
    raise SystemExit('settings button anchor missing')
insert = r'''        <button id="voteBtn" type="button" class="btn toolbar-action-btn" aria-label="Voting" aria-pressed="false" title="Voting an/aus · Shift+Klick auf Chip: Stimme abziehen · Rechtsklick hier: Stimmen zurücksetzen">🗳</button>
        <button id="timerBtn" type="button" class="btn toolbar-action-btn" aria-haspopup="true" aria-expanded="false" aria-label="Timer" title="Timer">⏱</button>
        <div id="timerPanel" class="timer-panel" hidden>
          <div class="timer-panel-title">Prüfungstimer</div>
          <div id="timerDisplay" class="timer-panel-display">45:00</div>
          <div id="timerStateLine" class="timer-state-line">Bereit</div>
          <div class="timer-config-row">
            <label for="timerMinutes">Minuten</label>
            <input id="timerMinutes" class="timer-minutes" type="number" min="1" max="600" step="1" value="45" inputmode="numeric" />
          </div>
          <div class="timer-presets" aria-label="Timer presets">
            <button type="button" class="timer-preset" data-minutes="5">5</button>
            <button type="button" class="timer-preset" data-minutes="10">10</button>
            <button type="button" class="timer-preset" data-minutes="45">45</button>
            <button type="button" class="timer-preset" data-minutes="90">90</button>
          </div>
          <div class="timer-actions">
            <button id="timerStartPause" type="button" class="btn btn-primary">Start</button>
            <button id="timerReset" type="button" class="btn">Reset</button>
            <button id="timerXLBtn" type="button" class="btn">XL</button>
          </div>
        </div>
''' + settings_anchor
text = text.replace(settings_anchor, insert, 1)

# 3) XL overlay after main.
main_anchor = '  </main>\n\n  <script>\n'
if main_anchor not in text:
    raise SystemExit('main/script anchor missing')
xl = r'''  </main>

  <div id="timerXL" class="timer-xl-overlay" hidden aria-live="polite">
    <div class="timer-xl-top">
      <div class="timer-xl-title">Prüfungstimer</div>
      <button id="timerXLClose" type="button" class="timer-xl-close" aria-label="XL-Timer schliessen" title="XL-Ansicht schliessen">×</button>
    </div>
    <div class="timer-xl-center">
      <div id="timerXLDisplay" class="timer-xl-time">45:00</div>
      <div id="timerXLEnd" class="timer-xl-end">Bereit</div>
    </div>
    <div class="timer-xl-actions">
      <button id="timerXLToggle" type="button" class="btn">Start</button>
      <button id="timerXLReset" type="button" class="btn">Reset</button>
    </div>
  </div>

  <script>
'''
text = text.replace(main_anchor, xl, 1)

# 4) DOM refs.
ref_anchor = "    const presentBtn = document.getElementById('presentBtn');\n"
if ref_anchor not in text:
    raise SystemExit('present ref anchor missing')
refs = ref_anchor + r'''    const voteBtn = document.getElementById('voteBtn');
    const timerBtn = document.getElementById('timerBtn');
    const timerPanel = document.getElementById('timerPanel');
    const timerDisplay = document.getElementById('timerDisplay');
    const timerStateLine = document.getElementById('timerStateLine');
    const timerMinutesInput = document.getElementById('timerMinutes');
    const timerStartPauseBtn = document.getElementById('timerStartPause');
    const timerResetBtn = document.getElementById('timerReset');
    const timerXLBtn = document.getElementById('timerXLBtn');
    const timerXL = document.getElementById('timerXL');
    const timerXLDisplay = document.getElementById('timerXLDisplay');
    const timerXLEnd = document.getElementById('timerXLEnd');
    const timerXLClose = document.getElementById('timerXLClose');
    const timerXLToggle = document.getElementById('timerXLToggle');
    const timerXLReset = document.getElementById('timerXLReset');
'''
text = text.replace(ref_anchor, refs, 1)

# 5) State constants.
state_anchor = "    const CHIP_GROUPS = new Set(['pro','contra','fragen']);\n"
if state_anchor not in text:
    raise SystemExit('group constants anchor missing')
states = state_anchor + r'''    const TIMER_STORAGE_KEY = 'discussion.timer.v1';
    const DEFAULT_TIMER_MS = 45 * 60 * 1000;
    const MAX_TIMER_MS = 600 * 60 * 1000;
    let votingMode = false;
    let timerState = null;
    let timerTickHandle = null;
'''
text = text.replace(state_anchor, states, 1)

# 6) Voting + persistent timer functions after presentation helper.
presentation = r'''    function setPresentationMode(active){
      const on = Boolean(active);
      document.documentElement.classList.toggle('presentation-mode', on);
      if(presentBtn) presentBtn.setAttribute('aria-pressed', String(on));
      scheduleLayout();
    }
'''
if presentation not in text:
    raise SystemExit('presentation helper anchor missing')
functions = presentation + r'''

    function setVotingMode(active){
      votingMode = Boolean(active);
      document.documentElement.classList.toggle('voting-mode', votingMode);
      if(voteBtn){
        voteBtn.classList.toggle('is-active', votingMode);
        voteBtn.setAttribute('aria-pressed', String(votingMode));
      }
    }

    function syncVoteBadge(btn){
      if(!btn) return;
      const wrap = btn.closest('.btn-wrap');
      if(!wrap) return;
      let badge = wrap.querySelector('.vote-badge');
      if(!badge){
        badge = document.createElement('span');
        badge.className = 'vote-badge';
        wrap.appendChild(badge);
      }
      const votes = Math.max(0, Math.round(Number(btn.dataset.votes || '0')) || 0);
      badge.textContent = String(votes);
      badge.hidden = votes <= 0;
      badge.setAttribute('aria-hidden','true');
    }

    function changeChipVotes(btn, delta){
      if(!btn) return;
      const current = Math.max(0, Math.round(Number(btn.dataset.votes || '0')) || 0);
      const next = Math.max(0, current + Math.round(Number(delta) || 0));
      if(next === current) return;
      pushUndoSnapshot();
      btn.dataset.votes = String(next);
      syncVoteBadge(btn);
      saveChips();
    }

    function resetAllVotes(){
      if(!list) return;
      const voted = Array.from(list.querySelectorAll('.btn-item')).filter(btn => Number(btn.dataset.votes || '0') > 0);
      if(!voted.length) return;
      if(!window.confirm('Alle Stimmen auf 0 zurücksetzen?')) return;
      pushUndoSnapshot();
      voted.forEach(btn => {
        btn.dataset.votes = '0';
        syncVoteBadge(btn);
      });
      saveChips();
    }

    function normalizeTimerState(raw){
      const source = raw && typeof raw === 'object' ? raw : {};
      const duration = Math.min(MAX_TIMER_MS, Math.max(60 * 1000, Number(source.durationMs) || DEFAULT_TIMER_MS));
      let running = source.running === true;
      let endAt = Number(source.endAt);
      let remaining = Number(source.remainingMs);
      if(!Number.isFinite(remaining)) remaining = duration;
      remaining = Math.min(MAX_TIMER_MS, Math.max(0, remaining));
      if(running && Number.isFinite(endAt)){
        remaining = Math.max(0, endAt - Date.now());
        if(remaining <= 0){
          running = false;
          endAt = null;
        }
      }else{
        running = false;
        endAt = null;
      }
      return {
        durationMs: duration,
        running,
        endAt: Number.isFinite(endAt) ? endAt : null,
        remainingMs: remaining,
        xl: source.xl === true
      };
    }

    function loadTimerState(){
      const raw = readStorage(TIMER_STORAGE_KEY);
      if(raw){
        try{ return normalizeTimerState(JSON.parse(raw)); }
        catch(err){ console.warn('Timer state parse failed:', err); }
      }
      return normalizeTimerState(null);
    }

    function timerRemaining(now = Date.now()){
      if(!timerState) return DEFAULT_TIMER_MS;
      if(timerState.running && Number.isFinite(timerState.endAt)) return Math.max(0, timerState.endAt - now);
      return Math.max(0, Number(timerState.remainingMs) || 0);
    }

    function persistTimerState(){
      if(!timerState) return;
      const payload = {
        durationMs: timerState.durationMs,
        running: timerState.running,
        endAt: timerState.running ? timerState.endAt : null,
        remainingMs: timerRemaining(),
        xl: timerState.xl
      };
      writeStorage(TIMER_STORAGE_KEY, JSON.stringify(payload));
    }

    function formatTimer(ms){
      const totalSeconds = Math.max(0, Math.ceil(ms / 1000));
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;
      return String(minutes).padStart(2,'0') + ':' + String(seconds).padStart(2,'0');
    }

    function timerStatusText(remaining){
      if(remaining <= 0) return 'Zeit abgelaufen';
      if(timerState && timerState.running && Number.isFinite(timerState.endAt)){
        const end = new Date(timerState.endAt);
        return 'Ende ' + end.toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' });
      }
      if(timerState && timerState.remainingMs < timerState.durationMs) return 'Pausiert';
      return 'Bereit';
    }

    function syncTimerUI(){
      if(!timerState) return;
      let remaining = timerRemaining();
      if(timerState.running && remaining <= 0){
        timerState.running = false;
        timerState.endAt = null;
        timerState.remainingMs = 0;
        persistTimerState();
        remaining = 0;
      }else if(!timerState.running){
        timerState.remainingMs = remaining;
      }
      const label = formatTimer(remaining);
      const status = timerStatusText(remaining);
      if(timerDisplay) timerDisplay.textContent = label;
      if(timerStateLine) timerStateLine.textContent = status;
      if(timerXLDisplay) timerXLDisplay.textContent = label;
      if(timerXLEnd) timerXLEnd.textContent = status;
      if(timerStartPauseBtn) timerStartPauseBtn.textContent = timerState.running ? 'Pause' : 'Start';
      if(timerXLToggle) timerXLToggle.textContent = timerState.running ? 'Pause' : 'Start';
      if(timerMinutesInput){
        timerMinutesInput.disabled = timerState.running;
        if(document.activeElement !== timerMinutesInput){
          timerMinutesInput.value = String(Math.max(1, Math.round(timerState.durationMs / 60000)));
        }
      }
      document.querySelectorAll('.timer-preset').forEach(btn => { btn.disabled = timerState.running; });
      if(timerBtn){
        timerBtn.classList.toggle('is-active', timerState.running || timerState.xl);
        timerBtn.classList.toggle('timer-finished', remaining <= 0);
      }
      if(timerXL){
        timerXL.hidden = !timerState.xl;
        timerXL.classList.toggle('is-finished', remaining <= 0);
      }
      document.documentElement.classList.toggle('timer-xl-active', timerState.xl);
    }

    function setTimerMinutes(minutes){
      if(!timerState || timerState.running) return;
      const numeric = Number(minutes);
      if(!Number.isFinite(numeric)) return;
      const duration = Math.min(MAX_TIMER_MS, Math.max(60 * 1000, Math.round(numeric * 60000)));
      timerState.durationMs = duration;
      timerState.remainingMs = duration;
      timerState.endAt = null;
      persistTimerState();
      syncTimerUI();
    }

    function toggleTimerRunning(){
      if(!timerState) return;
      if(timerState.running){
        timerState.remainingMs = timerRemaining();
        timerState.running = false;
        timerState.endAt = null;
      }else{
        let remaining = timerRemaining();
        if(remaining <= 0) remaining = timerState.durationMs;
        timerState.remainingMs = remaining;
        timerState.running = true;
        timerState.endAt = Date.now() + remaining;
      }
      persistTimerState();
      syncTimerUI();
    }

    function resetTimer(){
      if(!timerState) return;
      timerState.running = false;
      timerState.endAt = null;
      timerState.remainingMs = timerState.durationMs;
      persistTimerState();
      syncTimerUI();
    }

    function setTimerXL(active){
      if(!timerState) return;
      timerState.xl = Boolean(active);
      persistTimerState();
      syncTimerUI();
    }
'''
text = text.replace(presentation, functions, 1)

# 7) Votes in chip creation.
metrics_anchor = "      btn.dataset.metrics = '0';\n"
if metrics_anchor not in text:
    raise SystemExit('chip metrics anchor missing')
text = text.replace(metrics_anchor, metrics_anchor + "      btn.dataset.votes = String(Math.max(0, Math.round(Number(options.votes || 0)) || 0));\n", 1)

# 8) Voting takes over normal chip click, but modifiers retain spotlight/focus.
alt_block = r'''        if(event.altKey){
          event.preventDefault();
          if(chipClickTimer){ clearTimeout(chipClickTimer); chipClickTimer = null; }
          toggleChipFocus(btn);
          btn.focus();
          return;
        }
'''
if alt_block not in text:
    raise SystemExit('alt click block missing')
vote_click = alt_block + r'''        if(votingMode){
          event.preventDefault();
          if(chipClickTimer){ clearTimeout(chipClickTimer); chipClickTimer = null; }
          changeChipVotes(btn, event.shiftKey ? -1 : 1);
          btn.focus();
          return;
        }
'''
text = text.replace(alt_block, vote_click, 1)

# Dblclick edits only outside voting mode.
dbl = r'''      btn.addEventListener('dblclick',(event)=>{
        event.preventDefault();
        if(chipClickTimer){ clearTimeout(chipClickTimer); chipClickTimer = null; }
        startChipEdit(btn);
      });
'''
if dbl not in text:
    raise SystemExit('dblclick block missing')
text = text.replace(dbl, r'''      btn.addEventListener('dblclick',(event)=>{
        event.preventDefault();
        if(chipClickTimer){ clearTimeout(chipClickTimer); chipClickTimer = null; }
        if(votingMode) return;
        startChipEdit(btn);
      });
''', 1)

# Keyboard Enter/Space votes while voting.
key_block = r'''        if(e.key==='Enter'||e.key===' '){
          e.preventDefault();
          cycleChipStage(btn);
        } else if(e.key==='Delete'){
'''
if key_block not in text:
    raise SystemExit('chip key block missing')
text = text.replace(key_block, r'''        if(e.key==='Enter'||e.key===' '){
          e.preventDefault();
          if(votingMode) changeChipVotes(btn, e.shiftKey ? -1 : 1);
          else cycleChipStage(btn);
        } else if(e.key==='Delete'){
''', 1)

# Sync vote badge after chip enters wrap.
append_anchor = "      wrap.appendChild(btn);\n      syncChipGroup(btn);\n"
if append_anchor not in text:
    raise SystemExit('chip append anchor missing')
text = text.replace(append_anchor, "      wrap.appendChild(btn);\n      syncVoteBadge(btn);\n      syncChipGroup(btn);\n", 1)

# Tooltip.
old_title = "      btn.title='Klick: Grösse · Doppelklick: Bearbeiten · Ctrl/Cmd+Klick/S: Spotlight · Alt+Klick/F: Fokus · Rechtsklick: Menü · Delete: Löschen';\n"
if old_title in text:
    text = text.replace(old_title, "      btn.title='Klick: Grösse · Voting aktiv: +1 Stimme (Shift: -1) · Doppelklick: Bearbeiten · Ctrl/Cmd+Klick/S: Spotlight · Alt+Klick/F: Fokus · Rechtsklick: Menü';\n", 1)

# 9) Save/load votes.
data_anchor = "          pinned: btn.dataset.pinned === '1',\n          group: btn.dataset.group || null\n"
if data_anchor not in text:
    raise SystemExit('chip data anchor missing')
text = text.replace(data_anchor, "          pinned: btn.dataset.pinned === '1',\n          group: btn.dataset.group || null,\n          votes: Math.max(0, Math.round(Number(btn.dataset.votes || '0')) || 0)\n", 1)

load_anchor = "        pinned: Boolean(item.pinned),\n        group: item.group || undefined\n"
if load_anchor not in text:
    raise SystemExit('chip load anchor missing')
text = text.replace(load_anchor, "        pinned: Boolean(item.pinned),\n        group: item.group || undefined,\n        votes: Math.max(0, Math.round(Number(item.votes || 0)) || 0)\n", 1)

# 10) Initialize timer after normal app initialization.
init_anchor = "    applyBeamerTheme(readStorage(BEAMER_THEME_KEY) === 'dark' ? 'dark' : 'light', false);\n"
if init_anchor not in text:
    raise SystemExit('init anchor missing')
text = text.replace(init_anchor, init_anchor + r'''    timerState = loadTimerState();
    persistTimerState();
    syncTimerUI();
    timerTickHandle = window.setInterval(syncTimerUI, 250);
    window.addEventListener('focus', syncTimerUI);
    document.addEventListener('visibilitychange', () => { if(!document.hidden) syncTimerUI(); });
    window.addEventListener('storage', event => {
      if(event.key !== TIMER_STORAGE_KEY || !event.newValue) return;
      try{
        timerState = normalizeTimerState(JSON.parse(event.newValue));
        syncTimerUI();
      }catch(_){}
    });
''', 1)

# 11) Wire voting and timer before masonry controls.
wire_anchor = r'''    if(presentBtn){
      presentBtn.addEventListener('click', () => {
        const active = document.documentElement.classList.contains('presentation-mode');
        setPresentationMode(!active);
      });
    }
'''
if wire_anchor not in text:
    raise SystemExit('present wiring anchor missing')
wires = wire_anchor + r'''

    if(voteBtn){
      voteBtn.addEventListener('click', () => setVotingMode(!votingMode));
      voteBtn.addEventListener('contextmenu', event => {
        event.preventDefault();
        resetAllVotes();
      });
    }

    if(timerBtn && timerPanel){
      const setTimerPanelOpen = open => {
        timerPanel.hidden = !open;
        timerBtn.setAttribute('aria-expanded', String(open));
        if(open && settingsPanel){
          settingsPanel.hidden = true;
          if(settingsBtn) settingsBtn.setAttribute('aria-expanded','false');
        }
      };
      timerBtn.addEventListener('click', event => {
        event.stopPropagation();
        setTimerPanelOpen(timerPanel.hidden);
      });
      timerPanel.addEventListener('click', event => event.stopPropagation());
      document.addEventListener('click', () => setTimerPanelOpen(false));
      document.addEventListener('keydown', event => {
        if(event.key === 'Escape' && !timerState?.xl) setTimerPanelOpen(false);
      });
    }

    if(timerMinutesInput){
      timerMinutesInput.addEventListener('change', () => setTimerMinutes(timerMinutesInput.value));
      timerMinutesInput.addEventListener('keydown', event => {
        if(event.key === 'Enter'){
          event.preventDefault();
          setTimerMinutes(timerMinutesInput.value);
          timerMinutesInput.blur();
        }
      });
    }
    document.querySelectorAll('.timer-preset').forEach(button => {
      button.addEventListener('click', () => setTimerMinutes(button.dataset.minutes));
    });
    if(timerStartPauseBtn) timerStartPauseBtn.addEventListener('click', toggleTimerRunning);
    if(timerResetBtn) timerResetBtn.addEventListener('click', resetTimer);
    if(timerXLBtn) timerXLBtn.addEventListener('click', () => setTimerXL(true));
    if(timerXLClose) timerXLClose.addEventListener('click', () => setTimerXL(false));
    if(timerXLToggle) timerXLToggle.addEventListener('click', toggleTimerRunning);
    if(timerXLReset) timerXLReset.addEventListener('click', resetTimer);
'''
text = text.replace(wire_anchor, wires, 1)

# 12) Settings button closes timer panel when opened.
settings_click = r'''      settingsBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        setSettingsOpen(settingsPanel.hidden);
      });
'''
if settings_click not in text:
    raise SystemExit('settings click anchor missing')
text = text.replace(settings_click, r'''      settingsBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        if(timerPanel){
          timerPanel.hidden = true;
          if(timerBtn) timerBtn.setAttribute('aria-expanded','false');
        }
        setSettingsOpen(settingsPanel.hidden);
      });
''', 1)

# Final checks.
required = [
    MARKER,
    'id="voteBtn"',
    'id="timerBtn"',
    'id="timerXL"',
    "const TIMER_STORAGE_KEY = 'discussion.timer.v1';",
    'function toggleTimerRunning()',
    'function resetAllVotes()',
    'votes: Math.max(0, Math.round(Number(btn.dataset.votes',
    'timerTickHandle = window.setInterval(syncTimerUI, 250);'
]
for item in required:
    if item not in text:
        raise SystemExit('missing expected patched item: ' + item)

path.write_text(text, encoding='utf-8')
