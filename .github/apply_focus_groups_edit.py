from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Visual layer for quiet focus mode, group families and chip menu.
marker = '/* ===== Focus, groups and inline edit ===== */'
if marker not in text:
    style = '''
  <style>
    /* ===== Focus, groups and inline edit ===== */
    #list.focus-mode-active .btn-wrap{
      opacity:.28;
      filter:grayscale(.28) saturate(.72);
      transition:opacity .18s ease,filter .18s ease,transform .22s ease,padding .22s ease;
    }
    #list.focus-mode-active .btn-wrap:has(.chip-focus){
      opacity:1;
      filter:none;
      z-index:5;
    }
    .chip-focus{
      outline:3px solid rgba(8,145,178,.34);
      outline-offset:2px;
      box-shadow:0 8px 22px rgba(15,23,42,.13),inset 0 1px 0 rgba(255,255,255,.22);
    }

    .btn-wrap[data-group]::before{
      position:absolute;
      z-index:7;
      left:-5px;
      top:-8px;
      min-height:18px;
      padding:2px 5px;
      display:grid;
      place-items:center;
      border:1px solid rgba(15,23,42,.12);
      border-radius:999px;
      box-shadow:0 2px 7px rgba(15,23,42,.12);
      font-size:9px;
      font-weight:850;
      line-height:1;
      letter-spacing:.03em;
      pointer-events:none;
    }
    .btn-wrap[data-group="pro"]::before{content:'PRO';background:#dcfce7;color:#166534}
    .btn-wrap[data-group="contra"]::before{content:'CONTRA';background:#ffe4e6;color:#9f1239}
    .btn-wrap[data-group="fragen"]::before{content:'FRAGE';background:#f3e8ff;color:#7e22ce}
    .btn-wrap[data-group="pro"] .chip{outline:2px solid rgba(22,163,74,.34);outline-offset:1px}
    .btn-wrap[data-group="contra"] .chip{outline:2px solid rgba(225,29,72,.32);outline-offset:1px}
    .btn-wrap[data-group="fragen"] .chip{outline:2px solid rgba(147,51,234,.32);outline-offset:1px}
    .btn-wrap[data-group] .chip-focus{outline-width:3px}

    .chip-menu{
      position:fixed;
      z-index:1000;
      width:190px;
      padding:6px;
      display:grid;
      gap:3px;
      border:1px solid #dbe3ee;
      border-radius:14px;
      background:#fff;
      box-shadow:0 18px 45px rgba(15,23,42,.2);
    }
    .chip-menu[hidden]{display:none}
    .chip-menu-sep{height:1px;margin:3px 2px;background:#e2e8f0}
    .chip-menu-btn{
      min-height:34px;
      padding:.45rem .6rem;
      display:flex;
      align-items:center;
      gap:.5rem;
      border:0;
      border-radius:9px;
      background:transparent;
      color:#1e293b;
      text-align:left;
      font:700 .82rem/1.2 ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;
      cursor:pointer;
    }
    .chip-menu-btn:hover,.chip-menu-btn.is-active{background:#f1f5f9}
    .chip-menu-dot{width:9px;height:9px;border-radius:50%;flex:0 0 auto;background:#cbd5e1}
    .chip-menu-dot.pro{background:#22c55e}
    .chip-menu-dot.contra{background:#f43f5e}
    .chip-menu-dot.fragen{background:#a855f7}

    html[data-beamer-theme="dark"] .chip-menu{background:#0f172a;border-color:#334155;box-shadow:0 18px 45px rgba(0,0,0,.42)}
    html[data-beamer-theme="dark"] .chip-menu-btn{color:#e2e8f0}
    html[data-beamer-theme="dark"] .chip-menu-btn:hover,
    html[data-beamer-theme="dark"] .chip-menu-btn.is-active{background:#1e293b}
    html[data-beamer-theme="dark"] .chip-menu-sep{background:#334155}

    @media (prefers-reduced-motion: reduce){
      #list.focus-mode-active .btn-wrap{transition:none}
    }
  </style>
'''
    text = text.replace('</head>', style + '\n</head>', 1)

# Focus constants/state.
if "const CHIP_FOCUS_CLASS = 'chip-focus';" not in text:
    anchor = "    const BEAMER_THEME_KEY = 'discussion.beamerTheme.v1';\n    let lastRandomChip = null;\n"
    replacement = "    const BEAMER_THEME_KEY = 'discussion.beamerTheme.v1';\n    const CHIP_FOCUS_CLASS = 'chip-focus';\n    const CHIP_GROUPS = new Set(['pro','contra','fragen']);\n    let lastRandomChip = null;\n    let chipMenu = null;\n    let chipMenuTarget = null;\n"
    if anchor not in text:
        raise SystemExit('Could not locate feature state block')
    text = text.replace(anchor, replacement, 1)

# Group + edit helpers before pin helper.
if 'function setChipGroup(btn, group)' not in text:
    anchor = '    function toggleChipPinned(btn){\n'
    block = '''    function syncChipGroup(btn){
      if(!btn) return;
      const wrap = btn.closest('.btn-wrap');
      if(!wrap) return;
      const group = CHIP_GROUPS.has(btn.dataset.group || '') ? btn.dataset.group : '';
      if(group) wrap.dataset.group = group;
      else delete wrap.dataset.group;
    }

    function setChipGroup(btn, group){
      if(!btn) return;
      const next = CHIP_GROUPS.has(group) ? group : '';
      const current = CHIP_GROUPS.has(btn.dataset.group || '') ? btn.dataset.group : '';
      if(next === current) return;
      pushUndoSnapshot();
      if(next) btn.dataset.group = next;
      else delete btn.dataset.group;
      syncChipGroup(btn);
      scheduleLayout();
      saveChips();
    }

    function startChipEdit(btn){
      if(!btn) return;
      const current = (btn.dataset.label || '').trim();
      const edited = window.prompt('Text bearbeiten', current);
      if(edited === null) return;
      const next = edited.trim();
      if(!next || next === current) return;
      pushUndoSnapshot();
      const hadEmoji = startsWithEmoji(btn.textContent || '');
      btn.dataset.label = next;
      if(hadEmoji){
        const em = detectEmoji(next);
        btn.textContent = em ? (em + ' ' + next) : next;
      }else{
        btn.textContent = next;
      }
      applyStageToChip(btn, Number(btn.dataset.scaleStage || '0'), { remeasure: true });
      scheduleLayout();
      saveChips();
      btn.focus();
    }

    function closeChipMenu(){
      if(chipMenu) chipMenu.hidden = true;
      chipMenuTarget = null;
    }

    function ensureChipMenu(){
      if(chipMenu) return chipMenu;
      chipMenu = document.createElement('div');
      chipMenu.className = 'chip-menu';
      chipMenu.hidden = true;
      chipMenu.setAttribute('role','menu');
      chipMenu.innerHTML = `
        <button type="button" class="chip-menu-btn" data-action="edit">✎ Bearbeiten</button>
        <button type="button" class="chip-menu-btn" data-action="pin">📌 Anpinnen</button>
        <div class="chip-menu-sep"></div>
        <button type="button" class="chip-menu-btn" data-group=""><span class="chip-menu-dot"></span>Keine Gruppe</button>
        <button type="button" class="chip-menu-btn" data-group="pro"><span class="chip-menu-dot pro"></span>Pro</button>
        <button type="button" class="chip-menu-btn" data-group="contra"><span class="chip-menu-dot contra"></span>Contra</button>
        <button type="button" class="chip-menu-btn" data-group="fragen"><span class="chip-menu-dot fragen"></span>Fragen</button>`;
      document.body.appendChild(chipMenu);
      chipMenu.addEventListener('click', event => {
        const button = event.target instanceof Element ? event.target.closest('.chip-menu-btn') : null;
        if(!button || !chipMenuTarget) return;
        event.stopPropagation();
        if(button.dataset.action === 'edit') startChipEdit(chipMenuTarget);
        else if(button.dataset.action === 'pin') toggleChipPinned(chipMenuTarget);
        else if(Object.prototype.hasOwnProperty.call(button.dataset, 'group')) setChipGroup(chipMenuTarget, button.dataset.group || '');
        closeChipMenu();
      });
      chipMenu.addEventListener('contextmenu', event => event.preventDefault());
      document.addEventListener('click', event => {
        if(chipMenu && !chipMenu.hidden && event.target instanceof Node && !chipMenu.contains(event.target)) closeChipMenu();
      });
      document.addEventListener('keydown', event => {
        if(event.key === 'Escape') closeChipMenu();
      });
      window.addEventListener('resize', closeChipMenu);
      return chipMenu;
    }

    function openChipMenu(btn, event){
      if(!btn) return;
      const menu = ensureChipMenu();
      chipMenuTarget = btn;
      const pinButton = menu.querySelector('[data-action="pin"]');
      if(pinButton) pinButton.textContent = btn.dataset.pinned === '1' ? '📌 Pin lösen' : '📌 Anpinnen';
      const group = CHIP_GROUPS.has(btn.dataset.group || '') ? btn.dataset.group : '';
      menu.querySelectorAll('[data-group]').forEach(option => {
        option.classList.toggle('is-active', (option.dataset.group || '') === group);
      });
      menu.hidden = false;
      menu.style.left = '0px';
      menu.style.top = '0px';
      const rect = menu.getBoundingClientRect();
      const x = Math.min(Math.max(6, event.clientX), Math.max(6, window.innerWidth - rect.width - 6));
      const y = Math.min(Math.max(6, event.clientY), Math.max(6, window.innerHeight - rect.height - 6));
      menu.style.left = x + 'px';
      menu.style.top = y + 'px';
    }

''' + anchor
    if anchor not in text:
        raise SystemExit('Could not locate pin helper')
    text = text.replace(anchor, block, 1)

# Focus helpers after spotlight clear helper.
if 'function toggleChipFocus(btn)' not in text:
    anchor = '    function toggleChipSpotlight(btn){\n'
    block = '''    function clearFocusMode(){
      if(!list) return;
      list.querySelectorAll('.btn-item.' + CHIP_FOCUS_CLASS).forEach(btn => {
        btn.classList.remove(CHIP_FOCUS_CLASS);
        syncChipBadge(btn);
      });
      list.classList.remove('focus-mode-active');
    }

    function toggleChipFocus(btn){
      if(!btn || !list) return;
      const activate = !btn.classList.contains(CHIP_FOCUS_CLASS);
      clearAllSpotlights();
      clearFocusMode();
      if(activate){
        btn.classList.add(CHIP_FOCUS_CLASS);
        list.classList.add('focus-mode-active');
        syncChipBadge(btn);
      }
    }

    function clearAllHighlights(){
      clearAllSpotlights();
      clearFocusMode();
    }

''' + anchor
    if anchor not in text:
        raise SystemExit('Could not locate spotlight helper')
    text = text.replace(anchor, block, 1)

# Badge shows quiet focus state too.
text = text.replace(
    "      if(btn.classList.contains(CHIP_SPOTLIGHT_CLASS)) badges.push('★');\n",
    "      if(btn.classList.contains(CHIP_SPOTLIGHT_CLASS)) badges.push('★');\n      if(btn.classList.contains(CHIP_FOCUS_CLASS)) badges.push('◎');\n",
    1
)

# Activating spotlight exits quiet focus first.
needle = "      const activate = !btn.classList.contains(CHIP_SPOTLIGHT_CLASS);\n      if(list){\n"
replacement = "      const activate = !btn.classList.contains(CHIP_SPOTLIGHT_CLASS);\n      if(activate) clearFocusMode();\n      if(list){\n"
if replacement not in text:
    if needle not in text:
        raise SystemExit('Could not locate spotlight activation')
    text = text.replace(needle, replacement, 1)

# Clicking empty board clears both spotlight and focus.
text = text.replace(
    "        if(event.target === list) clearAllSpotlights();\n",
    "        if(event.target === list) clearAllHighlights();\n",
    1
)

# F hotkey = quiet focus.
needle = "      } else if (key === 's') {\n        const active = document.activeElement;\n        if(active && active.classList && active.classList.contains('btn-item')){\n          e.preventDefault();\n          toggleChipSpotlight(active);\n        }\n      } else if (key === 'e') {\n"
replacement = "      } else if (key === 's') {\n        const active = document.activeElement;\n        if(active && active.classList && active.classList.contains('btn-item')){\n          e.preventDefault();\n          toggleChipSpotlight(active);\n        }\n      } else if (key === 'f') {\n        const active = document.activeElement;\n        if(active && active.classList && active.classList.contains('btn-item')){\n          e.preventDefault();\n          toggleChipFocus(active);\n        }\n      } else if (key === 'e') {\n"
if "key === 'f'" not in text:
    if needle not in text:
        raise SystemExit('Could not locate spotlight hotkey')
    text = text.replace(needle, replacement, 1)

# Persist group assignment.
if "group: btn.dataset.group || null" not in text:
    needle = "          order: Number.isFinite(orderValue) ? orderValue : null,\n          pinned: btn.dataset.pinned === '1'\n"
    replacement = "          order: Number.isFinite(orderValue) ? orderValue : null,\n          pinned: btn.dataset.pinned === '1',\n          group: btn.dataset.group || null\n"
    if needle not in text:
        raise SystemExit('Could not locate chip data payload')
    text = text.replace(needle, replacement, 1)

if "group: item.group || undefined" not in text:
    needle = "        createdAt: Number.isFinite(orderNumeric) ? orderNumeric : undefined,\n        pinned: Boolean(item.pinned)\n"
    replacement = "        createdAt: Number.isFinite(orderNumeric) ? orderNumeric : undefined,\n        pinned: Boolean(item.pinned),\n        group: item.group || undefined\n"
    if needle not in text:
        raise SystemExit('Could not locate chip restore options')
    text = text.replace(needle, replacement, 1)

# Initialize groups when chips are created.
if "if(options.group && CHIP_GROUPS.has(options.group))" not in text:
    needle = "      if(options.pinned){\n        btn.dataset.pinned = '1';\n        btn.classList.add('chip-pinned');\n      }\n      btn.textContent = maybeAddEmoji(label);\n"
    replacement = "      if(options.pinned){\n        btn.dataset.pinned = '1';\n        btn.classList.add('chip-pinned');\n      }\n      if(options.group && CHIP_GROUPS.has(options.group)) btn.dataset.group = options.group;\n      btn.textContent = maybeAddEmoji(label);\n"
    if needle not in text:
        raise SystemExit('Could not locate chip init options')
    text = text.replace(needle, replacement, 1)

# Sync group badge/outline before returning the chip.
needle = "      wrap.appendChild(btn);\n      syncChipBadge(btn);\n      return wrap;\n"
replacement = "      wrap.appendChild(btn);\n      syncChipGroup(btn);\n      syncChipBadge(btn);\n      return wrap;\n"
if "wrap.appendChild(btn);\n      syncChipGroup(btn);" not in text:
    if needle not in text:
        raise SystemExit('Could not locate chip return')
    text = text.replace(needle, replacement, 1)

# Right click opens menu rather than immediately toggling pin.
needle = "      btn.addEventListener('contextmenu',(event)=>{\n        event.preventDefault();\n        toggleChipPinned(btn);\n        btn.focus();\n      });\n"
replacement = "      btn.addEventListener('contextmenu',(event)=>{\n        event.preventDefault();\n        btn.focus();\n        openChipMenu(btn, event);\n      });\n"
if replacement not in text:
    if needle not in text:
        raise SystemExit('Could not locate context menu handler')
    text = text.replace(needle, replacement, 1)

# Replace plain click handling with a short delay so double click edits without two size changes.
old_click = '''      btn.addEventListener('click',(event)=>{
        if(event.ctrlKey || event.metaKey){
          event.preventDefault();
          toggleChipSpotlight(btn);
          btn.focus();
          return;
        }
        if(event.shiftKey){
          event.preventDefault();
          const currentStage = Number(btn.dataset.scaleStage || '0');
          if(currentStage !== 0){
            pushUndoSnapshot();
            updateBaseMetrics(btn);
            applyStageToChip(btn, 0);
            scheduleLayout();
            saveChips();
          }
        }else{
          cycleChipStage(btn);
        }
        btn.focus();
      });
'''
new_click = '''      let chipClickTimer = null;
      btn.addEventListener('click',(event)=>{
        if(event.ctrlKey || event.metaKey){
          event.preventDefault();
          if(chipClickTimer){ clearTimeout(chipClickTimer); chipClickTimer = null; }
          toggleChipSpotlight(btn);
          btn.focus();
          return;
        }
        if(event.altKey){
          event.preventDefault();
          if(chipClickTimer){ clearTimeout(chipClickTimer); chipClickTimer = null; }
          toggleChipFocus(btn);
          btn.focus();
          return;
        }
        if(event.shiftKey){
          event.preventDefault();
          if(chipClickTimer){ clearTimeout(chipClickTimer); chipClickTimer = null; }
          const currentStage = Number(btn.dataset.scaleStage || '0');
          if(currentStage !== 0){
            pushUndoSnapshot();
            updateBaseMetrics(btn);
            applyStageToChip(btn, 0);
            scheduleLayout();
            saveChips();
          }
          btn.focus();
          return;
        }
        if(chipClickTimer){
          clearTimeout(chipClickTimer);
          chipClickTimer = null;
          return;
        }
        chipClickTimer = setTimeout(() => {
          chipClickTimer = null;
          cycleChipStage(btn);
          btn.focus();
        }, 210);
      });
      btn.addEventListener('dblclick',(event)=>{
        event.preventDefault();
        if(chipClickTimer){ clearTimeout(chipClickTimer); chipClickTimer = null; }
        startChipEdit(btn);
      });
'''
if 'let chipClickTimer = null;' not in text:
    if old_click not in text:
        raise SystemExit('Could not locate chip click handler')
    text = text.replace(old_click, new_click, 1)

# Tooltip explains new gestures.
text = text.replace(
    "      btn.title='Click: Grösse · Shift+Click: Reset · Ctrl/Cmd+Click oder S: Spotlight · Rechtsklick: Anpinnen · Delete: Löschen';",
    "      btn.title='Klick: Grösse · Doppelklick: Bearbeiten · Ctrl/Cmd+Klick/S: Spotlight · Alt+Klick/F: Fokus · Rechtsklick: Menü · Delete: Löschen';",
    1
)

path.write_text(text, encoding='utf-8')
