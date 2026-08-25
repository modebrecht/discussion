from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# 1) Denser chip padding via a small override layer.
marker = '/* ===== Compact chip density ===== */'
if marker not in text:
    style = '''
  <style>
    /* ===== Compact chip density ===== */
    .chip{
      padding:calc(.34rem * var(--chip-font-scale, 1)) calc(.72rem * var(--chip-font-scale, 1));
    }
    #list{
      padding-top:6px;
      padding-bottom:12px;
    }
  </style>
'''
    text = text.replace('</head>', style + '\n</head>', 1)

# 2) New default spacing: 4 instead of 8.
text = text.replace(
    "const layoutConfig = { step: 4, gutter: 8, chipScale: 1, mode: 'flow' };",
    "const layoutConfig = { step: 4, gutter: 4, chipScale: 1, mode: 'flow' };"
)
text = text.replace(
    "const defaultSettings = { chipScale: 1, gutter: 8 };",
    "const defaultSettings = { chipScale: 1, gutter: 4 };"
)
text = text.replace(
    'id="chipMargin" type="range" min="0" max="32" step="1" value="8"',
    'id="chipMargin" type="range" min="0" max="32" step="1" value="4"'
)

# 3) One-time migration of the old untouched default (8 -> 4).
old = """    const uiSettings = loadSettings();
    layoutConfig.gutter = clampNumber(uiSettings.gutter, sliderBounds.margin.min, sliderBounds.margin.max);"""
new = """    const uiSettings = loadSettings();
    const COMPACT_SPACING_MIGRATION_KEY = 'discussion.compactSpacing.v1';
    if(readStorage(COMPACT_SPACING_MIGRATION_KEY) !== '1'){
      if(Number(uiSettings.gutter) === 8) uiSettings.gutter = 4;
      writeStorage(COMPACT_SPACING_MIGRATION_KEY, '1');
    }
    layoutConfig.gutter = clampNumber(uiSettings.gutter, sliderBounds.margin.min, sliderBounds.margin.max);"""
if old in text:
    text = text.replace(old, new, 1)
elif 'COMPACT_SPACING_MIGRATION_KEY' not in text:
    raise SystemExit('Could not locate uiSettings block')

path.write_text(text, encoding='utf-8')
