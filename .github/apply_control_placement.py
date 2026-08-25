from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, got {count}')
    text = text.replace(old, new, 1)

# Mark the main controls host.
replace_once(
    '<div class="control-group" style="flex-wrap:wrap; gap:.75rem">',
    '<div id="mainControlsHost" class="control-group" style="flex-wrap:wrap; gap:.75rem">',
    'main controls host'
)

# Mark currently-main board controls as movable.
replace_once(
    '<label class="label" title="Give new chips a random background color"><input id="randColor" type="checkbox" checked> Color</label>',
    '<label data-placement-control="color" class="label" title="Give new chips a random background color"><input id="randColor" type="checkbox" checked> Color</label>',
    'color control'
)
replace_once(
    '<label class="label" title="Automatically prepend an emoji based on the text"><input id="autoEmoji" type="checkbox"> Emoji</label>',
    '<label data-placement-control="autoEmoji" class="label" title="Automatically prepend an emoji based on the text"><input id="autoEmoji" type="checkbox"> Emoji</label>',
    'auto emoji control'
)
replace_once(
    '<button id="reEmoji" type="button" title="Add or remove emojis on all existing chips" class="btn">Emoji</button>',
    '<button data-placement-control="emoji" id="reEmoji" type="button" title="Add or remove emojis on all existing chips" class="btn">Emoji</button>',
    'emoji control'
)
replace_once(
    '<label class="label" style="gap:.35rem" title="Adjust chip base size"><span>Size</span>',
    '<label data-placement-control="size" class="label" style="gap:.35rem" title="Adjust chip base size"><span>Size</span>',
    'size control'
)
replace_once(
    '<button id="masonryToggle" type="button" class="btn" title="Toggle dense masonry packing for chips">Masonry</button>',
    '<button data-placement-control="masonry" id="masonryToggle" type="button" class="btn" title="Toggle dense masonry packing for chips">Masonry</button>',
    'masonry control'
)
replace_once(
    '<button id="oneLineToggle" type="button" class="btn" title="Show chips in a single vertical column">OneLine</button>',
    '<button data-placement-control="oneLine" id="oneLineToggle" type="button" class="btn" title="Show chips in a single vertical column">OneLine</button>',
    'oneline control'
)

# Replace fixed settings categories with a movable controls host plus placement editor.
old_settings = '''          <div class="settings-section">
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
          </div>'''
new_settings = '''          <div class="settings-section">
            <div class="menu-section-title">Werkzeuge</div>
            <div id="settingsControlsHost" class="settings-controls-host">
              <div data-placement-control="shape" class="settings-choice-row">
                <span>Form</span>
                <div class="segmented-control" role="group" aria-label="Form der Chips">
                  <button id="shapeRounded" class="segmented-btn" type="button" aria-pressed="false">Rechteck</button>
                  <button id="shapePill" class="segmented-btn" type="button" aria-pressed="false">Pill</button>
                </div>
              </div>
              <div data-placement-control="theme" class="settings-choice-row">
                <span>Beamer</span>
                <div class="segmented-control" role="group" aria-label="Beamer-Darstellung">
                  <button id="themeLightBtn" class="segmented-btn" type="button" aria-pressed="false">Hell</button>
                  <button id="themeDarkBtn" class="segmented-btn" type="button" aria-pressed="false">Dunkel</button>
                </div>
              </div>
              <label data-placement-control="padding" class="settings-row" for="chipPadding">
                <span class="settings-row-head"><span>Padding</span><output id="chipPaddingValue">4 / 8 px</output></span>
                <input id="chipPadding" type="range" min="1" max="12" step="0.5" value="4" />
              </label>
              <label data-placement-control="margin" class="settings-row" for="chipMargin">
                <span class="settings-row-head"><span>Margin</span><output id="chipMarginValue">2 px</output></span>
                <input id="chipMargin" type="range" min="0" max="16" step="1" value="2" />
              </label>
            </div>
          </div>
          <div class="settings-section placement-editor-section">
            <div class="menu-section-title">Menü anpassen</div>
            <div class="placement-bulk-actions">
              <button type="button" class="placement-bulk-btn" data-placement-all="main">Alles Hauptmenü</button>
              <button type="button" class="placement-bulk-btn" data-placement-all="settings">Alles Einstellungen</button>
            </div>
            <div id="placementEditor" class="placement-editor"></div>
          </div>'''
replace_once(old_settings, new_settings, 'settings movable controls')

# Add styles for controls that can live in either host and for the placement editor.
style = r'''

  <style>
    /* ===== User-configurable control placement ===== */
    .settings-controls-host{display:grid;gap:.5rem}
    .settings-controls-host:empty::after{
      content:'Alle Werkzeuge sind im Hauptmenü.';
      padding:.55rem .1rem;
      color:#94a3b8;
      font-size:.76rem;
      font-weight:650;
    }
    .settings-controls-host > .label,
    .settings-controls-host > .btn,
    .settings-controls-host > .settings-choice-row,
    .settings-controls-host > .settings-row{width:100%;margin:0}
    .settings-controls-host > .label{justify-content:space-between}
    .settings-controls-host > .btn{text-align:left}
    .settings-controls-host > .label:has(input[type="range"]){display:grid;grid-template-columns:auto 1fr;align-items:center;gap:.7rem}
    .settings-controls-host > .label input[type="range"]{width:100%}

    #mainControlsHost > .settings-choice-row{
      display:inline-flex;
      grid-template-columns:none;
      width:auto;
      min-height:34px;
      padding:2px 3px 2px .55rem;
      gap:.45rem;
      border:1px solid #e2e8f0;
      border-radius:12px;
      background:#f8fafc;
      white-space:nowrap;
    }
    #mainControlsHost > .settings-choice-row > span{font-size:.78rem;color:#64748b}
    #mainControlsHost > .settings-choice-row .segmented-control{min-height:28px}
    #mainControlsHost > .settings-choice-row .segmented-btn{min-height:27px;padding:.28rem .48rem;font-size:.74rem}

    #mainControlsHost > .settings-row{
      display:inline-flex;
      align-items:center;
      width:auto;
      min-height:34px;
      padding:.3rem .55rem;
      gap:.5rem;
      border:1px solid #e2e8f0;
      border-radius:12px;
      background:#f8fafc;
      white-space:nowrap;
    }
    #mainControlsHost > .settings-row .settings-row-head{gap:.35rem}
    #mainControlsHost > .settings-row input[type="range"]{width:88px}
    #mainControlsHost > .settings-row output{font-size:.72rem}

    .placement-editor{display:grid;gap:4px}
    .placement-row{
      display:grid;
      grid-template-columns:minmax(0,1fr) auto;
      align-items:center;
      gap:.65rem;
      min-height:36px;
      padding:.22rem 0;
    }
    .placement-name{min-width:0;color:#334155;font-size:.79rem;font-weight:720}
    .placement-choice{
      display:inline-flex;
      padding:2px;
      border:1px solid #e2e8f0;
      border-radius:9px;
      background:#f8fafc;
    }
    .placement-choice-btn{
      min-height:27px;
      padding:.26rem .48rem;
      border:0;
      border-radius:7px;
      background:transparent;
      color:#64748b;
      font:760 .7rem/1 ui-sans-serif,system-ui,sans-serif;
      cursor:pointer;
      white-space:nowrap;
    }
    .placement-choice-btn.is-active{background:#0f172a;color:#fff}
    .placement-bulk-actions{display:grid;grid-template-columns:1fr 1fr;gap:.4rem}
    .placement-bulk-btn{
      min-height:31px;
      padding:.32rem .45rem;
      border:1px solid #e2e8f0;
      border-radius:9px;
      background:#f8fafc;
      color:#475569;
      font:740 .71rem/1.15 ui-sans-serif,system-ui,sans-serif;
      cursor:pointer;
    }
    .placement-bulk-btn:hover{background:#fff;border-color:#cbd5e1}

    html[data-beamer-theme="dark"] #mainControlsHost > .settings-choice-row,
    html[data-beamer-theme="dark"] #mainControlsHost > .settings-row,
    html[data-beamer-theme="dark"] .placement-choice,
    html[data-beamer-theme="dark"] .placement-bulk-btn{background:#111827;border-color:#334155;color:#cbd5e1}
    html[data-beamer-theme="dark"] #mainControlsHost > .settings-choice-row > span,
    html[data-beamer-theme="dark"] .placement-name{color:#cbd5e1}
    html[data-beamer-theme="dark"] .placement-choice-btn{color:#94a3b8}
    html[data-beamer-theme="dark"] .placement-choice-btn.is-active{background:#334155;color:#fff}
    html[data-beamer-theme="dark"] .settings-controls-host:empty::after{color:#64748b}

    @media (max-width:760px){
      .placement-choice-btn{padding-inline:.4rem}
      #mainControlsHost > .settings-row input[type="range"]{width:72px}
    }
  </style>
'''
replace_once('\n</head>', style + '\n</head>', 'placement styles')

# Add placement script after the existing shape script and before body close.
script = r'''

  <script>
    (() => {
      const PLACEMENT_KEY = 'discussion.controlPlacement.v1';
      const mainHost = document.getElementById('mainControlsHost');
      const settingsHost = document.getElementById('settingsControlsHost');
      const editor = document.getElementById('placementEditor');
      if(!mainHost || !settingsHost || !editor) return;

      const controls = [
        { key:'color', label:'Color', defaultPlace:'main' },
        { key:'autoEmoji', label:'Auto-Emoji', defaultPlace:'main' },
        { key:'emoji', label:'Emoji', defaultPlace:'main' },
        { key:'size', label:'Size', defaultPlace:'main' },
        { key:'shape', label:'Form', defaultPlace:'settings' },
        { key:'theme', label:'Beamer', defaultPlace:'settings' },
        { key:'padding', label:'Padding', defaultPlace:'settings' },
        { key:'margin', label:'Margin', defaultPlace:'settings' },
        { key:'masonry', label:'Masonry', defaultPlace:'main' },
        { key:'oneLine', label:'OneLine', defaultPlace:'main' }
      ];

      const defaults = Object.fromEntries(controls.map(item => [item.key, item.defaultPlace]));

      const readPlacement = () => {
        try{
          const raw = localStorage.getItem(PLACEMENT_KEY);
          if(!raw) return { ...defaults };
          const parsed = JSON.parse(raw);
          const next = { ...defaults };
          if(parsed && typeof parsed === 'object'){
            controls.forEach(item => {
              if(parsed[item.key] === 'main' || parsed[item.key] === 'settings') next[item.key] = parsed[item.key];
            });
          }
          return next;
        }catch(_){
          return { ...defaults };
        }
      };

      let placement = readPlacement();

      const persist = () => {
        try{ localStorage.setItem(PLACEMENT_KEY, JSON.stringify(placement)); }catch(_){}
      };

      const renderEditor = () => {
        editor.innerHTML = '';
        controls.forEach(item => {
          const row = document.createElement('div');
          row.className = 'placement-row';
          row.innerHTML = `
            <span class="placement-name">${item.label}</span>
            <span class="placement-choice" role="group" aria-label="${item.label} platzieren">
              <button type="button" class="placement-choice-btn" data-place-key="${item.key}" data-place-value="main">Hauptmenü</button>
              <button type="button" class="placement-choice-btn" data-place-key="${item.key}" data-place-value="settings">⚙</button>
            </span>`;
          editor.appendChild(row);
        });
      };

      const syncEditor = () => {
        editor.querySelectorAll('[data-place-key]').forEach(button => {
          const active = placement[button.dataset.placeKey] === button.dataset.placeValue;
          button.classList.toggle('is-active', active);
          button.setAttribute('aria-pressed', String(active));
        });
      };

      const applyPlacement = ({ save = false } = {}) => {
        controls.forEach(item => {
          const node = document.querySelector(`[data-placement-control="${item.key}"]`);
          if(!node) return;
          const target = placement[item.key] === 'settings' ? settingsHost : mainHost;
          target.appendChild(node);
        });
        syncEditor();
        if(save) persist();
        if(typeof scheduleLayout === 'function') scheduleLayout();
      };

      renderEditor();
      applyPlacement();

      editor.addEventListener('click', event => {
        const button = event.target instanceof Element ? event.target.closest('[data-place-key]') : null;
        if(!button) return;
        const key = button.dataset.placeKey;
        const value = button.dataset.placeValue;
        if(!controls.some(item => item.key === key)) return;
        if(value !== 'main' && value !== 'settings') return;
        placement[key] = value;
        applyPlacement({ save:true });
      });

      document.querySelectorAll('[data-placement-all]').forEach(button => {
        button.addEventListener('click', () => {
          const value = button.dataset.placementAll;
          if(value !== 'main' && value !== 'settings') return;
          placement = Object.fromEntries(controls.map(item => [item.key, value]));
          applyPlacement({ save:true });
        });
      });
    })();
  </script>
'''
replace_once('\n</body>', script + '\n</body>', 'placement script')

path.write_text(text, encoding='utf-8')
