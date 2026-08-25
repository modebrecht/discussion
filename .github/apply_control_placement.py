from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = '.settings-panel{width:min(330px,calc(100vw - 1rem));gap:.6rem}'
new = '.settings-panel{width:min(330px,calc(100vw - 1rem));max-height:calc(100dvh - 5rem);overflow:auto;overscroll-behavior:contain;gap:.6rem}'
if text.count(old) != 1:
    raise SystemExit(f'expected one settings panel style, got {text.count(old)}')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
