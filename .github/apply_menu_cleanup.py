from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, got {count}')
    text = text.replace(old, new, 1)

# Remove the beamer theme quick button; theme is a setting now.
replace_once(
'''        <button id="themeBtn" type="button" class="btn toolbar-action-btn" aria-label="Beamer-Dunkelmodus" aria-pressed="false" title="Beamer-Dunkelmodus">◐</button>\n''',
'',
'theme toolbar button')

# Restructure settings into clear sections and move shape/theme controls there.
replace_once(
'''        <div id="settingsPanel" class="settings-panel" hidden>
          <div class="settings-title">Chip-Abstände</div>
          <label class="settings-row" for="chipPadding">
            <span class="settings-row-head"><span>Padding</span><output id="chipPaddingValue">4 / 8 px</output></span>
            <input id="chipPadding" type="range" min="1" max="12" step="0.5" value="4" />
          </label>
          <label class="settings-row" for="chipMargin">
            <span class="settings-row-head"><span>Margin</span><output id="chipMarginValue">2 px</output></span>
            <input id="chipMargin" type="range" min="0" max="16" step="1" value="2" />
          </label>
        </div>''',
'''        <div id="settingsPanel" class="settings-panel" hidden>
          <div class="settings-title">Einstellungen</div>
          <div class="settings-section">
            <div class="menu-section-title">Darstellung</div>
            <div class="settings-choice-row">
              <span>Form</span>
              <div class="segmented-control" role="group" aria-label="Form der Chips">
                <button id="shapeRounded" class="segmented-btn" type="button" aria-pressed="false">Rechteck</button>
                <button id="shapePill" class="segmented-btn" type="button" aria-pressed="false">Pill</button>
              </div>
            </div>
            <div class="settings-choice-row">
              <span>Beamer</span>
              <div class="segmented-control" role="group" aria-label="Beamer-Darstellung">
                <button id="themeLightBtn" class="segmented-btn" type="button" aria-pressed="false">Hell</button>
                <button id="themeDarkBtn" class="segmented-btn" type="button" aria-pressed="false">Dunkel</button>
              </div>
            </div>
          </div>
          <div class="settings-section">
            <div class="menu-section-title">Abstände</div>
            <label class="settings-row" for="chipPadding">
              <span class="settings-row-head"><span>Padding</span><output id="chipPaddingValue">4 / 8 px</output></span>
              <input id="chipPadding" type="range" min="1" max="12" step="0.5" value="4" />
            </label>
            <label class="settings-row" for="chipMargin">
              <span class="settings-row-head"><span>Margin</span><output id="chipMarginValue">2 px</output></span>
              <input id="chipMargin" type="range" min="0" max="16" step="1" value="2" />
            </label>
          </div>
        </div>''',
'settings panel')

# Give timer controls clearer hierarchy.
replace_once(
'''          <div id="timerStateLine" class="timer-state-line">Bereit</div>
          <div class="timer-config-row">''',
'''          <div id="timerStateLine" class="timer-state-line">Bereit</div>
          <div class="menu-section-title">Dauer</div>
          <div class="timer-config-row">''',
'timer duration heading')
replace_once(
'''          <div class="timer-actions">
            <button id="timerStartPause"''',
'''          <div class="menu-section-title">Steuerung</div>
          <div class="timer-actions">
            <button id="timerStartPause"''',
'timer controls heading')

# Richer but still compact export menu.
replace_once(
'''          <div id="exportMenu" class="export-menu" hidden role="menu" aria-label="Exportformat">
            <button type="button" class="export-menu-btn" data-export-format="json" role="menuitem">JSON</button>
            <button type="button" class="export-menu-btn" data-export-format="png" role="menuitem">PNG</button>
            <button type="button" class="export-menu-btn" data-export-format="svg" role="menuitem">SVG</button>
          </div>''',
'''          <div id="exportMenu" class="export-menu" hidden role="menu" aria-label="Exportformat">
            <div class="menu-section-title">Export</div>
            <button type="button" class="export-menu-btn" data-export-format="json" role="menuitem"><strong>JSON</strong><span>Backup</span></button>
            <button type="button" class="export-menu-btn" data-export-format="png" role="menuitem"><strong>PNG</strong><span>Bild</span></button>
            <button type="button" class="export-menu-btn" data-export-format="svg" role="menuitem"><strong>SVG</strong><span>Vektor</span></button>
          </div>''',
'export menu')

# Structure chip context menu.
replace_once(
'''      chipMenu.innerHTML = `
        <button type="button" class="chip-menu-btn" data-action="edit">✎ Bearbeiten</button>
        <button type="button" class="chip-menu-btn" data-action="pin">📌 Anpinnen</button>
        <div class="chip-menu-sep"></div>
        <button type="button" class="chip-menu-btn" data-group=""><span class="chip-menu-dot"></span>Keine Gruppe</button>
        <button type="button" class="chip-menu-btn" data-group="pro"><span class="chip-menu-dot pro"></span>Pro</button>
        <button type="button" class="chip-menu-btn" data-group="contra"><span class="chip-menu-dot contra"></span>Contra</button>
        <button type="button" class="chip-menu-btn" data-group="fragen"><span class="chip-menu-dot fragen"></span>Fragen</button>`;''',
'''      chipMenu.innerHTML = `
        <div class="chip-menu-section-title">Chip</div>
        <button type="button" class="chip-menu-btn" data-action="edit">✎ Bearbeiten</button>
        <button type="button" class="chip-menu-btn" data-action="pin">📌 Anpinnen</button>
        <div class="chip-menu-sep"></div>
        <div class="chip-menu-section-title">Gruppe</div>
        <button type="button" class="chip-menu-btn" data-group=""><span class="chip-menu-dot"></span>Ohne Gruppe</button>
        <button type="button" class="chip-menu-btn" data-group="pro"><span class="chip-menu-dot pro"></span>Pro</button>
        <button type="button" class="chip-menu-btn" data-group="contra"><span class="chip-menu-dot contra"></span>Contra</button>
        <button type="button" class="chip-menu-btn" data-group="fragen"><span class="chip-menu-dot fragen"></span>Fragen</button>`;''',
'chip context menu')

# Sync segmented theme buttons from the existing theme function.
replace_once(
'''      document.documentElement.dataset.beamerTheme = dark ? 'dark' : 'light';
      if(themeBtn){''',
'''      document.documentElement.dataset.beamerTheme = dark ? 'dark' : 'light';
      const themeLightBtn = document.getElementById('themeLightBtn');
      const themeDarkBtn = document.getElementById('themeDarkBtn');
      if(themeLightBtn){
        themeLightBtn.classList.toggle('is-active', !dark);
        themeLightBtn.setAttribute('aria-pressed', String(!dark));
      }
      if(themeDarkBtn){
        themeDarkBtn.classList.toggle('is-active', dark);
        themeDarkBtn.setAttribute('aria-pressed', String(dark));
      }
      if(themeBtn){''',
'theme segmented sync')

# Add settings theme listeners next to the old optional toolbar listener.
replace_once(
'''    if(themeBtn){
      themeBtn.addEventListener('click', () => {
        const dark = document.documentElement.dataset.beamerTheme === 'dark';
        applyBeamerTheme(dark ? 'light' : 'dark');
      });
    }
    if(presentBtn){''',
'''    if(themeBtn){
      themeBtn.addEventListener('click', () => {
        const dark = document.documentElement.dataset.beamerTheme === 'dark';
        applyBeamerTheme(dark ? 'light' : 'dark');
      });
    }
    const themeLightBtn = document.getElementById('themeLightBtn');
    const themeDarkBtn = document.getElementById('themeDarkBtn');
    if(themeLightBtn) themeLightBtn.addEventListener('click', () => applyBeamerTheme('light'));
    if(themeDarkBtn) themeDarkBtn.addEventListener('click', () => applyBeamerTheme('dark'));
    if(presentBtn){''',
'theme segmented listeners')

# Popovers are mutually exclusive: settings closes timer/export.
replace_once(
'''        if(timerPanel){
          timerPanel.hidden = true;
          if(timerBtn) timerBtn.setAttribute('aria-expanded','false');
        }
        setSettingsOpen(settingsPanel.hidden);''',
'''        if(timerPanel){
          timerPanel.hidden = true;
          if(timerBtn) timerBtn.setAttribute('aria-expanded','false');
        }
        if(exportMenu){
          exportMenu.hidden = true;
          if(exportBtn) exportBtn.setAttribute('aria-expanded','false');
        }
        setSettingsOpen(settingsPanel.hidden);''',
'settings closes export')

# Timer closes export as well as settings.
replace_once(
'''        if(open && settingsPanel){
          settingsPanel.hidden = true;
          if(settingsBtn) settingsBtn.setAttribute('aria-expanded','false');
        }
      };''',
'''        if(open && settingsPanel){
          settingsPanel.hidden = true;
          if(settingsBtn) settingsBtn.setAttribute('aria-expanded','false');
        }
        if(open && exportMenu){
          exportMenu.hidden = true;
          if(exportBtn) exportBtn.setAttribute('aria-expanded','false');
        }
      };''',
'timer closes export')

# Export closes settings/timer before opening.
replace_once(
'''      exportBtn.addEventListener('click', event => {
        event.stopPropagation();
        setExportOpen(exportMenu.hidden);
      });''',
'''      exportBtn.addEventListener('click', event => {
        event.stopPropagation();
        const opening = exportMenu.hidden;
        if(opening && settingsPanel){
          settingsPanel.hidden = true;
          if(settingsBtn) settingsBtn.setAttribute('aria-expanded','false');
        }
        if(opening && timerPanel){
          timerPanel.hidden = true;
          if(timerBtn) timerBtn.setAttribute('aria-expanded','false');
        }
        setExportOpen(opening);
      });''',
'export popover exclusivity')

# Generic wording and SVG fallback use the new rectangular default.
replace_once('title="Adjust pill base size"', 'title="Adjust chip base size"', 'size tooltip')
replace_once("const shape = document.documentElement.dataset.chipShape || 'pill';", "const shape = document.documentElement.dataset.chipShape || 'rounded';", 'svg default shape')

# Replace the old dynamically injected shape selector with settings-based controls.
old_shape_script = '''  <script>
    (() => {
      const CHIP_SHAPE_KEY = 'discussion.chipShape.v1';
      const root = document.documentElement;
      const group = document.querySelector('.options-row .control-group');
      if(!group) return;

      const control = document.createElement('div');
      control.className = 'shape-control';
      control.setAttribute('role', 'group');
      control.setAttribute('aria-label', 'Form der Chips');
      control.innerHTML = '<span class="shape-label">Form</span>' +
        '<button id="shapePill" class="shape-btn" type="button">Pill</button>' +
        '<button id="shapeRounded" class="shape-btn" type="button" title="Rechteck abgerundet">Rechteck</button>';

      const masonry = document.getElementById('masonryToggle');
      group.insertBefore(control, masonry || null);

      const pillBtn = document.getElementById('shapePill');
      const roundedBtn = document.getElementById('shapeRounded');

      const readShape = () => {
        try{
          return localStorage.getItem(CHIP_SHAPE_KEY) === 'rounded' ? 'rounded' : 'pill';
        }catch(_){
          return 'pill';
        }
      };

      const applyShape = (shape, persist = true) => {
        const next = shape === 'rounded' ? 'rounded' : 'pill';
        root.dataset.chipShape = next;
        pillBtn.classList.toggle('is-active', next === 'pill');
        roundedBtn.classList.toggle('is-active', next === 'rounded');
        pillBtn.setAttribute('aria-pressed', String(next === 'pill'));
        roundedBtn.setAttribute('aria-pressed', String(next === 'rounded'));
        if(persist){
          try{ localStorage.setItem(CHIP_SHAPE_KEY, next); }catch(_){}
        }
        if(typeof scheduleLayout === 'function') scheduleLayout();
      };

      pillBtn.addEventListener('click', () => applyShape('pill'));
      roundedBtn.addEventListener('click', () => applyShape('rounded'));
      applyShape(readShape(), false);
    })();
  </script>'''
new_shape_script = '''  <script>
    (() => {
      const CHIP_SHAPE_KEY = 'discussion.chipShape.v1';
      const root = document.documentElement;
      const pillBtn = document.getElementById('shapePill');
      const roundedBtn = document.getElementById('shapeRounded');
      if(!pillBtn || !roundedBtn) return;

      const readShape = () => {
        try{
          return localStorage.getItem(CHIP_SHAPE_KEY) === 'pill' ? 'pill' : 'rounded';
        }catch(_){
          return 'rounded';
        }
      };

      const applyShape = (shape, persist = true) => {
        const next = shape === 'pill' ? 'pill' : 'rounded';
        root.dataset.chipShape = next;
        pillBtn.classList.toggle('is-active', next === 'pill');
        roundedBtn.classList.toggle('is-active', next === 'rounded');
        pillBtn.setAttribute('aria-pressed', String(next === 'pill'));
        roundedBtn.setAttribute('aria-pressed', String(next === 'rounded'));
        if(persist){
          try{ localStorage.setItem(CHIP_SHAPE_KEY, next); }catch(_){}
        }
        if(typeof scheduleLayout === 'function') scheduleLayout();
      };

      pillBtn.addEventListener('click', () => applyShape('pill'));
      roundedBtn.addEventListener('click', () => applyShape('rounded'));
      applyShape(readShape(), false);
    })();
  </script>'''
replace_once(old_shape_script, new_shape_script, 'shape settings script')

# Add a final focused style layer for consistent menu hierarchy.
menu_css = r'''

  <style>
    /* ===== Menu structure cleanup ===== */
    .settings-panel{width:min(330px,calc(100vw - 1rem));gap:.6rem}
    .settings-title{font-size:.9rem;letter-spacing:-.01em}
    .settings-section{display:grid;gap:.58rem}
    .settings-section + .settings-section{padding-top:.7rem;border-top:1px solid #e8edf3}
    .menu-section-title,.chip-menu-section-title{
      color:#94a3b8;
      font-size:.67rem;
      font-weight:850;
      letter-spacing:.08em;
      line-height:1;
      text-transform:uppercase;
    }
    .settings-choice-row{display:grid;grid-template-columns:72px 1fr;align-items:center;gap:.65rem;color:#334155;font-size:.82rem;font-weight:750}
    .segmented-control{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));padding:3px;border:1px solid #dbe3ee;border-radius:11px;background:#f1f5f9}
    .segmented-btn{
      min-height:31px;padding:.3rem .45rem;border:0;border-radius:8px;background:transparent;color:#475569;
      font:800 .76rem/1 ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;cursor:pointer;
    }
    .segmented-btn:hover{background:rgba(255,255,255,.72)}
    .segmented-btn.is-active{background:#fff;color:#0f172a;box-shadow:0 1px 5px rgba(15,23,42,.12)}

    .timer-panel{gap:.56rem}
    .timer-panel .menu-section-title{margin-top:.15rem}
    .timer-presets{display:grid;grid-template-columns:repeat(4,1fr)}
    .timer-preset{text-align:center}

    .export-menu{min-width:174px;padding:6px;gap:2px}
    .export-menu .menu-section-title{padding:.42rem .55rem .28rem}
    .export-menu-btn{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.5rem .58rem}
    .export-menu-btn strong{font-size:.8rem;color:inherit}
    .export-menu-btn span{font-size:.7rem;font-weight:700;color:#94a3b8}

    .chip-menu{width:200px;padding:6px;gap:2px}
    .chip-menu-section-title{padding:.45rem .55rem .22rem}
    .chip-menu-btn{position:relative}
    .chip-menu-btn.is-active::after{content:'✓';margin-left:auto;font-weight:900;color:#0f172a}

    html[data-beamer-theme="dark"] .settings-section + .settings-section{border-top-color:#263244}
    html[data-beamer-theme="dark"] .settings-choice-row{color:#cbd5e1}
    html[data-beamer-theme="dark"] .segmented-control{background:#111827;border-color:#334155}
    html[data-beamer-theme="dark"] .segmented-btn{color:#94a3b8}
    html[data-beamer-theme="dark"] .segmented-btn:hover{background:#1e293b}
    html[data-beamer-theme="dark"] .segmented-btn.is-active{background:#334155;color:#fff;box-shadow:none}
    html[data-beamer-theme="dark"] .chip-menu-btn.is-active::after{color:#fff}

    @media (max-width:760px){
      .settings-panel{width:min(320px,calc(100vw - .8rem))}
    }
  </style>
'''
replace_once('\n</head>', menu_css + '\n</head>', 'menu styles')

path.write_text(text, encoding='utf-8')
print('Menu cleanup patch applied')
