from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Move spacing out of the main controls; it will live in the settings popover.
spacing_block = '''            <label class="label" style="gap:.35rem" title="Adjust spacing between pills"><span>Spacing</span>\n              <input id="chipMargin" type="range" min="0" max="32" step="1" value="4" />\n            </label>\n'''
text = text.replace(spacing_block, '', 1)

# Add settings button + popover beside NEW.
if 'id="settingsBtn"' not in text:
    anchor = '        <button id="newSaveBtn" type="button" class="btn btn-primary" title="Create a new empty save">NEW</button>\n'
    panel = anchor + '''        <button id="settingsBtn" type="button" class="btn settings-btn" aria-haspopup="true" aria-expanded="false" title="Chip settings">⚙ Einstellungen</button>\n        <div id="settingsPanel" class="settings-panel" hidden>\n          <div class="settings-title">Chip-Abstände</div>\n          <label class="settings-row" for="chipPadding">\n            <span class="settings-row-head"><span>Padding</span><output id="chipPaddingValue">4 / 8 px</output></span>\n            <input id="chipPadding" type="range" min="1" max="12" step="0.5" value="4" />\n          </label>\n          <label class="settings-row" for="chipMargin">\n            <span class="settings-row-head"><span>Margin</span><output id="chipMarginValue">2 px</output></span>\n            <input id="chipMargin" type="range" min="0" max="16" step="1" value="2" />\n          </label>\n        </div>\n'''
    if anchor not in text:
        raise SystemExit('Could not locate NEW button')
    text = text.replace(anchor, panel, 1)

# Settings UI styling and denser default chip padding.
marker = '/* ===== Chip spacing settings ===== */'
if marker not in text:
    style = '''\n  <style>\n    /* ===== Chip spacing settings ===== */\n    .save-controls{position:relative}\n    .settings-btn{min-height:42px;white-space:nowrap}\n    .settings-panel{\n      position:absolute;\n      z-index:100;\n      top:calc(100% + .55rem);\n      right:0;\n      width:min(300px,calc(100vw - 1rem));\n      padding:.8rem;\n      border:1px solid #dbe3ee;\n      border-radius:16px;\n      background:#fff;\n      box-shadow:0 18px 45px rgba(15,23,42,.16);\n      display:grid;\n      gap:.75rem;\n    }\n    .settings-panel[hidden]{display:none}\n    .settings-title{font-size:.82rem;font-weight:800;color:#0f172a}\n    .settings-row{display:grid;gap:.38rem;color:#334155;font-size:.82rem;font-weight:700}\n    .settings-row-head{display:flex;align-items:center;justify-content:space-between;gap:.75rem}\n    .settings-row output{color:#64748b;font-variant-numeric:tabular-nums;font-weight:700}\n    .settings-row input[type="range"]{\n      width:100%;\n      height:22px;\n      margin:0;\n      accent-color:#0891b2;\n      cursor:pointer;\n    }\n    .chip{padding:var(--chip-pad-y,4px) var(--chip-pad-x,8px)}\n    @media (max-width:760px){\n      .settings-btn{padding-inline:.65rem}\n      .settings-panel{right:-.2rem}\n    }\n  </style>\n'''
    text = text.replace('</head>', style + '\n</head>', 1)

# DOM refs.
anchor = "    const chipSizeInput = document.getElementById('chipSize');\n    const chipMarginInput = document.getElementById('chipMargin');\n"
replacement = anchor + "    const chipPaddingInput = document.getElementById('chipPadding');\n    const chipPaddingValue = document.getElementById('chipPaddingValue');\n    const chipMarginValue = document.getElementById('chipMarginValue');\n    const settingsBtn = document.getElementById('settingsBtn');\n    const settingsPanel = document.getElementById('settingsPanel');\n"
if 'const chipPaddingInput' not in text:
    if anchor not in text:
        raise SystemExit('Could not locate chip input refs')
    text = text.replace(anchor, replacement, 1)

# Denser defaults.
text = text.replace("const layoutConfig = { step: 4, gutter: 4, chipScale: 1, mode: 'flow' };", "const layoutConfig = { step: 4, gutter: 2, chipScale: 1, mode: 'flow' };")
text = text.replace("const defaultSettings = { chipScale: 1, gutter: 4 };", "const defaultSettings = { chipScale: 1, gutter: 2, chipPadding: 4 };")

# Add padding bounds next to the existing size/margin bounds.
if 'padding: chipPaddingInput ? {' not in text:
    needle = "      margin: chipMarginInput ? {\n"
    addition = "      padding: chipPaddingInput ? {\n        min: parseFloat(chipPaddingInput.min) || 1,\n        max: parseFloat(chipPaddingInput.max) || 12,\n        step: parseFloat(chipPaddingInput.step) || 0.5\n      } : { min: 1, max: 12, step: 0.5 },\n" + needle
    if needle not in text:
        raise SystemExit('Could not locate slider bounds')
    text = text.replace(needle, addition, 1)

# Allow a real 0px margin (0 must not fall through via `||`).
text = text.replace(
    "        min: parseFloat(chipMarginInput.min) || defaultSettings.gutter,",
    "        min: Number.isFinite(parseFloat(chipMarginInput.min)) ? parseFloat(chipMarginInput.min) : defaultSettings.gutter,"
)

# Persist padding.
if 'chipPadding: Number(chipPadding.toFixed(1))' not in text:
    needle = "        chipScale: Number(chipScale.toFixed(3)),\n        gutter: Math.round(layoutConfig.gutter)\n"
    replacement = "        chipScale: Number(chipScale.toFixed(3)),\n        gutter: Math.round(layoutConfig.gutter),\n        chipPadding: Number(chipPadding.toFixed(1))\n"
    if needle not in text:
        raise SystemExit('Could not locate settings payload')
    text = text.replace(needle, replacement, 1)

# Migrate untouched 4px spacing to the new 2px default, then initialize padding.
if 'DENSE_SPACING_MIGRATION_KEY' not in text:
    needle = "    layoutConfig.gutter = clampNumber(uiSettings.gutter, sliderBounds.margin.min, sliderBounds.margin.max);\n"
    block = '''    const DENSE_SPACING_MIGRATION_KEY = 'discussion.compactSpacing.v2';\n    if(readStorage(DENSE_SPACING_MIGRATION_KEY) !== '1'){\n      if(Number(uiSettings.gutter) === 4) uiSettings.gutter = 2;\n      writeStorage(DENSE_SPACING_MIGRATION_KEY, '1');\n    }\n    const initialChipPadding = Number(uiSettings.chipPadding);\n    let chipPadding = Number.isFinite(initialChipPadding)\n      ? clampNumber(initialChipPadding, sliderBounds.padding.min, sliderBounds.padding.max)\n      : defaultSettings.chipPadding;\n    const applyChipPadding = (value, { persist = true } = {}) => {\n      const numeric = Number(value);\n      if(!Number.isFinite(numeric)) return;\n      const step = sliderBounds.padding.step || 0.5;\n      const clamped = clampNumber(numeric, sliderBounds.padding.min, sliderBounds.padding.max);\n      chipPadding = Math.round(clamped / step) * step;\n      const vertical = Number(chipPadding.toFixed(1));\n      const horizontal = Number((chipPadding * 2).toFixed(1));\n      document.documentElement.style.setProperty('--chip-pad-y', vertical + 'px');\n      document.documentElement.style.setProperty('--chip-pad-x', horizontal + 'px');\n      if(chipPaddingInput) chipPaddingInput.value = String(vertical);\n      if(chipPaddingValue) chipPaddingValue.textContent = vertical + ' / ' + horizontal + ' px';\n      refreshChipMetrics();\n      if(persist) persistSettings();\n    };\n    applyChipPadding(chipPadding, { persist: false });\n''' + needle
    if needle not in text:
        raise SystemExit('Could not locate gutter init')
    text = text.replace(needle, block, 1)

# Show the live margin value whenever gutter changes.
needle = "      if(chipMarginInput){\n        chipMarginInput.value = String(clamped);\n      }\n      scheduleLayout();\n"
replacement = "      if(chipMarginInput){\n        chipMarginInput.value = String(clamped);\n      }\n      if(chipMarginValue) chipMarginValue.textContent = clamped + ' px';\n      scheduleLayout();\n"
if "chipMarginValue.textContent = clamped + ' px'" not in text:
    if needle not in text:
        raise SystemExit('Could not locate updateGutter')
    text = text.replace(needle, replacement, 1)

# Initialize margin output after reading saved settings.
needle = "    if(chipMarginInput) chipMarginInput.value = String(Math.round(layoutConfig.gutter));\n"
replacement = needle + "    if(chipMarginValue) chipMarginValue.textContent = Math.round(layoutConfig.gutter) + ' px';\n"
if "chipMarginValue.textContent = Math.round(layoutConfig.gutter)" not in text:
    if needle not in text:
        raise SystemExit('Could not locate margin init')
    text = text.replace(needle, replacement, 1)

# Padding slider listener.
if "chipPaddingInput.addEventListener('input'" not in text:
    needle = "    if (chipMarginInput){\n"
    block = '''    if (chipPaddingInput){\n      chipPaddingInput.addEventListener('input', () => applyChipPadding(chipPaddingInput.value));\n    }\n\n''' + needle
    if needle not in text:
        raise SystemExit('Could not locate margin listener')
    text = text.replace(needle, block, 1)

# Settings popover behavior.
if 'const setSettingsOpen' not in text:
    needle = "    if(saveSelect){\n"
    block = '''    if(settingsBtn && settingsPanel){\n      const setSettingsOpen = (open) => {\n        settingsPanel.hidden = !open;\n        settingsBtn.setAttribute('aria-expanded', String(open));\n      };\n      settingsBtn.addEventListener('click', (event) => {\n        event.stopPropagation();\n        setSettingsOpen(settingsPanel.hidden);\n      });\n      settingsPanel.addEventListener('click', event => event.stopPropagation());\n      document.addEventListener('click', () => setSettingsOpen(false));\n      document.addEventListener('keydown', event => {\n        if(event.key === 'Escape') setSettingsOpen(false);\n      });\n    }\n\n''' + needle
    if needle not in text:
        raise SystemExit('Could not locate save selector listener')
    text = text.replace(needle, block, 1)

path.write_text(text, encoding='utf-8')
