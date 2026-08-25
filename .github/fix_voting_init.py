from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

bad = "      btn.dataset.metrics = '0';\n      btn.dataset.votes = String(Math.max(0, Math.round(Number(options.votes || 0)) || 0));\n        updateBaseMetrics(btn);"
if bad not in text:
    raise SystemExit('Expected misplaced votes initialization not found')
text = text.replace(bad, "      btn.dataset.metrics = '0';\n        updateBaseMetrics(btn);", 1)

chip_anchor = "      btn.dataset.label = label;\n      btn.dataset.scaleStage = '0';\n      btn.dataset.metrics = '0';\n      if(options.pinned){"
if chip_anchor not in text:
    raise SystemExit('createChip initialization anchor missing')
text = text.replace(
    chip_anchor,
    "      btn.dataset.label = label;\n      btn.dataset.scaleStage = '0';\n      btn.dataset.metrics = '0';\n      btn.dataset.votes = String(Math.max(0, Math.round(Number(options.votes || 0)) || 0));\n      if(options.pinned){",
    1
)

if text.count('Number(options.votes || 0)') != 1:
    raise SystemExit('options.votes must appear exactly once after fix')
apply_start = text.index('function applyStageToChip')
apply_end = text.index('function cycleChipStage', apply_start)
if 'options.votes' in text[apply_start:apply_end]:
    raise SystemExit('options.votes still leaked into applyStageToChip')
create_start = text.index('function createChip')
create_end = text.index('function sortWrapsBy', create_start)
if 'options.votes' not in text[create_start:create_end]:
    raise SystemExit('votes initialization missing from createChip')

path.write_text(text, encoding='utf-8')
