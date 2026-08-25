from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# 1) CSS for compact toolbar actions, presentation mode, dark beamer mode and pin/status badges.
marker = '/* ===== Classroom feature pack ===== */'
if marker not in text:
    style = '''\n  <style>\n    /* ===== Classroom feature pack ===== */\n    .toolbar-action-btn{\n      width:42px;\n      min-width:42px;\n      min-height:42px;\n      padding:0;\n      display:grid;\n      place-items:center;\n      font-size:1rem;\n      line-height:1;\n    }\n    .toolbar-action-btn:disabled{opacity:.38;cursor:not-allowed;transform:none;box-shadow:none}\n    .btn-wrap[data-badge]::after{\n      content:attr(data-badge);\n      position:absolute;\n      z-index:6;\n      top:-8px;\n      right:-7px;\n      min-width:20px;\n      height:20px;\n      padding:0 3px;\n      display:grid;\n      place-items:center;\n      border:1px solid rgba(15,23,42,.14);\n      border-radius:999px;\n      background:rgba(255,255,255,.96);\n      box-shadow:0 3px 9px rgba(15,23,42,.14);\n      font-size:11px;\n      line-height:1;\n      pointer-events:none;\n    }\n    .chip-pinned{box-shadow:0 0 0 2px rgba(15,23,42,.18),0 4px 12px rgba(15,23,42,.085),inset 0 1px 0 rgba(255,255,255,.2)}\n\n    html.presentation-mode .toolbar,\n    html.presentation-mode main > .card{display:none}\n    html.presentation-mode .container{padding-top:.15rem;padding-bottom:.2rem}\n    html.presentation-mode main > section:last-child{margin-top:0 !important}\n    html.presentation-mode #list{padding-top:2px;padding-bottom:2px}\n\n    html[data-beamer-theme="dark"] body{\n      background:#05070b;\n      color:#f8fafc;\n    }\n    html[data-beamer-theme="dark"] .toolbar{\n      background:rgba(8,12,20,.97);\n      border-bottom-color:#1e293b;\n      box-shadow:0 8px 28px rgba(0,0,0,.28);\n    }\n    html[data-beamer-theme="dark"] .title{color:#f8fafc}\n    html[data-beamer-theme="dark"] .font-controls,\n    html[data-beamer-theme="dark"] .label,\n    html[data-beamer-theme="dark"] .shape-control{background:#111827;border-color:#334155;color:#e2e8f0}\n    html[data-beamer-theme="dark"] .font-controls .btn,\n    html[data-beamer-theme="dark"] .btn:not(.btn-primary),\n    html[data-beamer-theme="dark"] .shape-btn{background:#111827;border-color:#334155;color:#e2e8f0}\n    html[data-beamer-theme="dark"] .font-controls .btn:hover,\n    html[data-beamer-theme="dark"] .btn:not(.btn-primary):hover,\n    html[data-beamer-theme="dark"] .shape-btn:hover{background:#1e293b}\n    html[data-beamer-theme="dark"] .font-pct,\n    html[data-beamer-theme="dark"] .shape-label{color:#94a3b8}\n    html[data-beamer-theme="dark"] .font-pct strong{color:#f8fafc}\n    html[data-beamer-theme="dark"] .save-select,\n    html[data-beamer-theme="dark"] .input{background:#0f172a;border-color:#334155;color:#f8fafc}\n    html[data-beamer-theme="dark"] .card{background:rgba(10,15,25,.96);border-color:#273449;box-shadow:0 18px 50px rgba(0,0,0,.32)}\n    html[data-beamer-theme="dark"] .options-row{border-top-color:#263244}\n    html[data-beamer-theme="dark"] .settings-panel{background:#0f172a;border-color:#334155;color:#e2e8f0}\n    html[data-beamer-theme="dark"] .settings-title{color:#f8fafc}\n    html[data-beamer-theme="dark"] .settings-row{color:#cbd5e1}\n    html[data-beamer-theme="dark"] .settings-row output{color:#94a3b8}\n    html[data-beamer-theme="dark"] .chip:not(.chip-colored){background:#1e293b;color:#f8fafc;border-color:#475569}\n    html[data-beamer-theme="dark"] .btn-wrap[data-badge]::after{background:#0f172a;border-color:#475569;color:#fff}\n\n    @media (max-width:760px){\n      .toolbar-action-btn{width:40px;min-width:40px;min-height:40px}\n    }\n  </style>\n'''
    text = text.replace('</head>', style + '\n</head>', 1)

# 2) Add icon-only toolbar actions before settings.
if 'id="undoBtn"' not in text:
    anchor = '        <button id="settingsBtn" type="button" class="btn settings-btn" aria-haspopup="true" aria-expanded="false" aria-label="Einstellungen" title="Einstellungen">⚙</button>\n'
    actions = '''        <button id="undoBtn" type="button" class="btn toolbar-action-btn" aria-label="Rückgängig" title="Rückgängig" disabled>↶</button>\n        <button id="randomBtn" type="button" class="btn toolbar-action-btn" aria-label="Zufälligen Chip auswählen" title="Zufälligen Chip auswählen">🎲</button>\n        <button id="themeBtn" type="button" class="btn toolbar-action-btn" aria-label="Beamer-Dunkelmodus" aria-pressed="false" title="Beamer-Dunkelmodus">◐</button>\n        <button id="presentBtn" type="button" class="btn toolbar-action-btn" aria-label="Präsentationsmodus" aria-pressed="false" title="Präsentationsmodus (Esc zum Beenden)">⛶</button>\n''' + anchor
    if anchor not in text:
        raise SystemExit('Could not locate settings button')
    text = text.replace(anchor, actions, 1)

# 3) DOM refs.
if "const undoBtn = document.getElementById('undoBtn');" not in text:
    anchor = "    const settingsBtn = document.getElementById('settingsBtn');\n    const settingsPanel = document.getElementById('settingsPanel');\n"
    refs = anchor + "    const undoBtn = document.getElementById('undoBtn');\n    const randomBtn = document.getElementById('randomBtn');\n    const themeBtn = document.getElementById('themeBtn');\n    const presentBtn = document.getElementById('presentBtn');\n"
    if anchor not in text:
        raise SystemExit('Could not locate settings refs')
    text = text.replace(anchor, refs, 1)

# 4) History + presentation/theme helpers after storage helpers.
if 'const HISTORY_LIMIT = 30;' not in text:
    anchor = '''    const removeStorage = (key) => {\n      if (!storage) return;\n      try { storage.removeItem(key); }\n      catch (err) { console.warn('Local storage remove failed:', err); }\n    };\n'''
    block = anchor + '''\n    const HISTORY_LIMIT = 30;\n    const undoStack = [];\n    const BEAMER_THEME_KEY = 'discussion.beamerTheme.v1';\n    let lastRandomChip = null;\n\n    function updateUndoButton(){\n      if(undoBtn) undoBtn.disabled = undoStack.length === 0;\n    }\n\n    function clearUndoHistory(){\n      undoStack.length = 0;\n      updateUndoButton();\n    }\n\n    function pushUndoSnapshot(){\n      if(!list) return;\n      const snapshot = {\n        chips: getChipData().map(item => ({ ...item })),\n        mode: layoutConfig.mode\n      };\n      const key = JSON.stringify(snapshot);\n      const previous = undoStack.length ? undoStack[undoStack.length - 1] : null;\n      if(previous && previous.key === key) return;\n      undoStack.push({ ...snapshot, key });\n      if(undoStack.length > HISTORY_LIMIT) undoStack.shift();\n      updateUndoButton();\n    }\n\n    function undoLastAction(){\n      const snapshot = undoStack.pop();\n      if(!snapshot){ updateUndoButton(); return; }\n      replaceChips(snapshot.chips, { persist: false, focus: false });\n      setLayoutMode(snapshot.mode, { force: true });\n      saveChips();\n      updateUndoButton();\n    }\n\n    function applyBeamerTheme(mode, persist = true){\n      const dark = mode === 'dark';\n      document.documentElement.dataset.beamerTheme = dark ? 'dark' : 'light';\n      if(themeBtn){\n        themeBtn.setAttribute('aria-pressed', String(dark));\n        themeBtn.textContent = dark ? '☀' : '◐';\n        themeBtn.title = dark ? 'Heller Beamer-Modus' : 'Beamer-Dunkelmodus';\n      }\n      if(persist) writeStorage(BEAMER_THEME_KEY, dark ? 'dark' : 'light');\n    }\n\n    function setPresentationMode(active){\n      const on = Boolean(active);\n      document.documentElement.classList.toggle('presentation-mode', on);\n      if(presentBtn) presentBtn.setAttribute('aria-pressed', String(on));\n      scheduleLayout();\n    }\n'''
    if anchor not in text:
        raise SystemExit('Could not locate storage helpers')
    text = text.replace(anchor, block, 1)

# 5) Spotlight clear helper and chip badge sync.
if 'function syncChipBadge(btn)' not in text:
    anchor = '    function toggleChipSpotlight(btn){\n'
    block = '''    function syncChipBadge(btn){\n      if(!btn) return;\n      const wrap = btn.closest('.btn-wrap');\n      if(!wrap) return;\n      const badges = [];\n      if(btn.dataset.pinned === '1') badges.push('📌');\n      if(btn.classList.contains(CHIP_SPOTLIGHT_CLASS)) badges.push('★');\n      if(badges.length) wrap.dataset.badge = badges.join('');\n      else delete wrap.dataset.badge;\n    }\n\n    function clearAllSpotlights(){\n      if(!list) return;\n      list.querySelectorAll('.btn-item.' + CHIP_SPOTLIGHT_CLASS).forEach(btn => {\n        btn.classList.remove(CHIP_SPOTLIGHT_CLASS);\n        clearSpotlightTheme(btn);\n        setWrapSpotlightState(btn.closest('.btn-wrap'), 0);\n        syncChipBadge(btn);\n      });\n      scheduleLayout();\n    }\n\n''' + anchor
    if anchor not in text:
        raise SystemExit('Could not locate spotlight toggle')
    text = text.replace(anchor, block, 1)

# Keep spotlight badges in sync inside existing toggle logic.
text = text.replace(
    "          setWrapSpotlightState(otherHost, 0);\n",
    "          setWrapSpotlightState(otherHost, 0);\n          syncChipBadge(other);\n",
    1
)
text = text.replace(
    "        setWrapSpotlightState(host, CHIP_SPOTLIGHT_PAD);\n",
    "        setWrapSpotlightState(host, CHIP_SPOTLIGHT_PAD);\n        syncChipBadge(btn);\n",
    1
)
text = text.replace(
    "        setWrapSpotlightState(host, 0);\n      }\n      scheduleLayout();\n    }\n\n    function registerChipDragHandlers",
    "        setWrapSpotlightState(host, 0);\n        syncChipBadge(btn);\n      }\n      scheduleLayout();\n    }\n\n    function registerChipDragHandlers",
    1
)

# 6) Pinning helpers.
if 'function toggleChipPinned(btn)' not in text:
    anchor = '    function registerChipDragHandlers(btn){\n'
    block = '''    function toggleChipPinned(btn){\n      if(!btn) return;\n      pushUndoSnapshot();\n      const pinned = btn.dataset.pinned !== '1';\n      if(pinned){\n        btn.dataset.pinned = '1';\n        btn.classList.add('chip-pinned');\n      }else{\n        delete btn.dataset.pinned;\n        btn.classList.remove('chip-pinned');\n      }\n      syncChipBadge(btn);\n      restoreCreationOrder();\n      syncStackDragState();\n      scheduleLayout();\n      saveChips();\n    }\n\n''' + anchor
    if anchor not in text:
        raise SystemExit('Could not locate drag registration')
    text = text.replace(anchor, block, 1)

# Pinned chips stay fixed in OneLine drag mode.
text = text.replace(
    "      if(layoutConfig.mode === 'stack'){\n        btn.setAttribute('draggable', 'true');\n      }else{",
    "      if(layoutConfig.mode === 'stack' && btn.dataset.pinned !== '1'){\n        btn.setAttribute('draggable', 'true');\n      }else{",
    1
)
text = text.replace(
    "        if(enable){\n          btn.setAttribute('draggable', 'true');\n        }else{",
    "        if(enable && btn.dataset.pinned !== '1'){\n          btn.setAttribute('draggable', 'true');\n        }else{",
    1
)

# 7) Pinned chips sort before unpinned chips while preserving creation order.
old_restore = '''    function restoreCreationOrder(){\n      sortWrapsBy((a, b) => {\n        const aOrder = Number(a.dataset.createdAt || '0');\n        const bOrder = Number(b.dataset.createdAt || '0');\n        if(!Number.isFinite(aOrder) && !Number.isFinite(bOrder)) return 0;\n        if(!Number.isFinite(aOrder)) return 1;\n        if(!Number.isFinite(bOrder)) return -1;\n        return aOrder - bOrder;\n      });\n    }\n'''
new_restore = '''    function restoreCreationOrder(){\n      sortWrapsBy((a, b) => {\n        const aChip = a.firstElementChild instanceof HTMLElement ? a.firstElementChild : null;\n        const bChip = b.firstElementChild instanceof HTMLElement ? b.firstElementChild : null;\n        const aPinned = Boolean(aChip && aChip.dataset.pinned === '1');\n        const bPinned = Boolean(bChip && bChip.dataset.pinned === '1');\n        if(aPinned !== bPinned) return aPinned ? -1 : 1;\n        const aOrder = Number(a.dataset.createdAt || '0');\n        const bOrder = Number(b.dataset.createdAt || '0');\n        if(!Number.isFinite(aOrder) && !Number.isFinite(bOrder)) return 0;\n        if(!Number.isFinite(aOrder)) return 1;\n        if(!Number.isFinite(bOrder)) return -1;\n        return aOrder - bOrder;\n      });\n    }\n'''
if old_restore in text:
    text = text.replace(old_restore, new_restore, 1)
elif 'const aPinned = Boolean' not in text:
    raise SystemExit('Could not locate restoreCreationOrder')

# 8) Persist pinned state in saves/import/export.
if 'pinned: btn.dataset.pinned' not in text:
    text = text.replace(
        "          display: btn.textContent || '',\n          order: Number.isFinite(orderValue) ? orderValue : null\n",
        "          display: btn.textContent || '',\n          order: Number.isFinite(orderValue) ? orderValue : null,\n          pinned: btn.dataset.pinned === '1'\n",
        1
    )

if 'pinned: Boolean(item.pinned)' not in text:
    text = text.replace(
        "        displayText: display,\n        createdAt: Number.isFinite(orderNumeric) ? orderNumeric : undefined\n",
        "        displayText: display,\n        createdAt: Number.isFinite(orderNumeric) ? orderNumeric : undefined,\n        pinned: Boolean(item.pinned)\n",
        1
    )

# 9) Initialize pin state and right-click behavior on every chip.
if 'if(options.pinned)' not in text:
    anchor = "      btn.dataset.metrics = '0';\n      btn.textContent = maybeAddEmoji(label);\n"
    block = "      btn.dataset.metrics = '0';\n      if(options.pinned){\n        btn.dataset.pinned = '1';\n        btn.classList.add('chip-pinned');\n      }\n      btn.textContent = maybeAddEmoji(label);\n"
    if anchor not in text:
        raise SystemExit('Could not locate chip init')
    text = text.replace(anchor, block, 1)

if "btn.addEventListener('contextmenu'" not in text:
    anchor = "      btn.addEventListener('click',(event)=>{\n"
    block = "      syncChipBadge(btn);\n      btn.addEventListener('contextmenu',(event)=>{\n        event.preventDefault();\n        toggleChipPinned(btn);\n        btn.focus();\n      });\n" + anchor
    if anchor not in text:
        raise SystemExit('Could not locate chip click handler')
    text = text.replace(anchor, block, 1)

# Improve chip tooltip.
text = text.replace(
    "      btn.title='Click to cycle size (+30%, +60%, +90%, +120%, +150%). Shift+Click resets. Press Delete to remove';",
    "      btn.title='Click: Grösse · Shift+Click: Reset · Ctrl/Cmd+Click oder S: Spotlight · Rechtsklick: Anpinnen · Delete: Löschen';",
    1
)

# 10) Undo snapshots for common destructive/edit actions.
if 'function cycleChipStage(btn){\n      pushUndoSnapshot();' not in text:
    text = text.replace(
        '    function cycleChipStage(btn){\n      const current = Number(btn.dataset.scaleStage || \'0\');',
        '    function cycleChipStage(btn){\n      pushUndoSnapshot();\n      const current = Number(btn.dataset.scaleStage || \'0\');',
        1
    )

# Shift reset snapshot.
text = text.replace(
    "          if(currentStage !== 0){\n            updateBaseMetrics(btn);",
    "          if(currentStage !== 0){\n            pushUndoSnapshot();\n            updateBaseMetrics(btn);",
    1
)

# Add snapshot before adding.
text = text.replace(
    "      if(!value) return;\n      const node=createChip(value);",
    "      if(!value) return;\n      pushUndoSnapshot();\n      const node=createChip(value);",
    1
)

# Clear all snapshot.
text = text.replace(
    "    function clearAllChips(){\n      if(!list) return;\n      list.innerHTML='';",
    "    function clearAllChips(){\n      if(!list) return;\n      if(list.children.length) pushUndoSnapshot();\n      list.innerHTML='';",
    1
)

# Snapshot both delete paths.
text = text.replace(
    "          if(host){\n            if(chipResizeObserver) chipResizeObserver.unobserve(btn);\n            host.remove();",
    "          if(host){\n            pushUndoSnapshot();\n            if(chipResizeObserver) chipResizeObserver.unobserve(btn);\n            host.remove();",
    1
)
text = text.replace(
    "        if(host){\n          if(chipResizeObserver) chipResizeObserver.unobserve(btn);\n          host.remove();",
    "        if(host){\n          pushUndoSnapshot();\n          if(chipResizeObserver) chipResizeObserver.unobserve(btn);\n          host.remove();",
    1
)

# Emoji toggle snapshot.
text = text.replace(
    "        const removeEmojis=buttons.some(btn=>startsWithEmoji(btn.textContent||''));\n        let changed=0;",
    "        const removeEmojis=buttons.some(btn=>startsWithEmoji(btn.textContent||''));\n        if(buttons.length) pushUndoSnapshot();\n        let changed=0;",
    1
)

# Import snapshot.
text = text.replace(
    "            if(!Array.isArray(parsed)) throw new Error('Invalid JSON');\n            replaceChips(parsed);",
    "            if(!Array.isArray(parsed)) throw new Error('Invalid JSON');\n            pushUndoSnapshot();\n            replaceChips(parsed);",
    1
)

# Clear history on save switches/new saves.
text = text.replace(
    "      saveChips();\n      saveState.activeId = id;",
    "      saveChips();\n      clearUndoHistory();\n      saveState.activeId = id;",
    1
)
text = text.replace(
    "    function createNewSave(){\n      saveChips();",
    "    function createNewSave(){\n      saveChips();\n      clearUndoHistory();",
    1
)

# 11) Easier spotlight: click empty board to clear; S on focused chip.
if "if(event.target === list) clearAllSpotlights();" not in text:
    text = text.replace(
        "      list.addEventListener('drop', handleListDrop);\n",
        "      list.addEventListener('drop', handleListDrop);\n      list.addEventListener('click', event => {\n        if(event.target === list) clearAllSpotlights();\n      });\n",
        1
    )

text = text.replace(
    "      } else if (key === 'e') {\n        if (!input) return;",
    "      } else if (key === 's') {\n        const active = document.activeElement;\n        if(active && active.classList && active.classList.contains('btn-item')){\n          e.preventDefault();\n          toggleChipSpotlight(active);\n        }\n      } else if (key === 'e') {\n        if (!input) return;",
    1
)

# 12) Random spotlight helper.
if 'function spotlightRandomChip()' not in text:
    anchor = '    function getChipData(){\n'
    block = '''    function spotlightRandomChip(){\n      if(!list) return;\n      const chips = Array.from(list.querySelectorAll('.btn-item'));\n      if(!chips.length) return;\n      let pool = chips;\n      if(chips.length > 1 && lastRandomChip){\n        const filtered = chips.filter(chip => chip !== lastRandomChip);\n        if(filtered.length) pool = filtered;\n      }\n      const target = pool[Math.floor(Math.random() * pool.length)];\n      clearAllSpotlights();\n      toggleChipSpotlight(target);\n      target.focus({ preventScroll: true });\n      try{ target.scrollIntoView({ behavior:'smooth', block:'center', inline:'center' }); }catch(_){}\n      lastRandomChip = target;\n    }\n\n''' + anchor
    if anchor not in text:
        raise SystemExit('Could not locate getChipData')
    text = text.replace(anchor, block, 1)

# 13) Wire toolbar actions and initialize theme.
if "undoBtn.addEventListener('click', undoLastAction)" not in text:
    anchor = '''    if(newSaveBtn){\n      newSaveBtn.addEventListener('click', createNewSave);\n    }\n'''
    block = anchor + '''\n    if(undoBtn) undoBtn.addEventListener('click', undoLastAction);\n    if(randomBtn) randomBtn.addEventListener('click', spotlightRandomChip);\n    if(themeBtn){\n      themeBtn.addEventListener('click', () => {\n        const dark = document.documentElement.dataset.beamerTheme === 'dark';\n        applyBeamerTheme(dark ? 'light' : 'dark');\n      });\n    }\n    if(presentBtn){\n      presentBtn.addEventListener('click', () => {\n        const active = document.documentElement.classList.contains('presentation-mode');\n        setPresentationMode(!active);\n      });\n    }\n'''
    if anchor not in text:
        raise SystemExit('Could not locate new save handler')
    text = text.replace(anchor, block, 1)

# Theme init and undo state after normal load.
if "applyBeamerTheme(readStorage(BEAMER_THEME_KEY) === 'dark' ? 'dark' : 'light', false);" not in text:
    text = text.replace(
        "    updateLayoutModeUI();\n\n    if(settingsBtn && settingsPanel){",
        "    updateLayoutModeUI();\n    updateUndoButton();\n    applyBeamerTheme(readStorage(BEAMER_THEME_KEY) === 'dark' ? 'dark' : 'light', false);\n\n    if(settingsBtn && settingsPanel){",
        1
    )

# Esc exits presentation mode without interfering with the existing settings-panel escape handler.
if "document.documentElement.classList.contains('presentation-mode')" not in text[text.find('// ===== Hotkeys ====='):]:
    anchor = '    // ===== Hotkeys =====\n'
    block = '''    document.addEventListener('keydown', event => {\n      if(event.key === 'Escape' && document.documentElement.classList.contains('presentation-mode')){\n        setPresentationMode(false);\n      }\n    });\n\n''' + anchor
    if anchor not in text:
        raise SystemExit('Could not locate hotkeys section')
    text = text.replace(anchor, block, 1)

path.write_text(text, encoding='utf-8')
