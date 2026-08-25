from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Ensure persisted pinned chips get their badge after being attached to the wrap.
needle = "      wrap.appendChild(btn);\n      return wrap;\n"
replacement = "      wrap.appendChild(btn);\n      syncChipBadge(btn);\n      return wrap;\n"
if replacement not in text:
    if needle not in text:
        raise SystemExit('Could not locate wrap append')
    text = text.replace(needle, replacement, 1)

# Reliable Escape for presentation mode + standard Ctrl/Cmd+Z undo.
marker = '// ===== Classroom shortcuts ====='
if marker not in text:
    anchor = '    // ===== Hotkeys =====\n'
    block = '''    // ===== Classroom shortcuts =====\n    document.addEventListener('keydown', event => {\n      if(event.key === 'Escape' && document.documentElement.classList.contains('presentation-mode')){\n        setPresentationMode(false);\n        return;\n      }\n      if((event.ctrlKey || event.metaKey) && !event.altKey && !event.shiftKey && typeof event.key === 'string' && event.key.toLowerCase() === 'z'){\n        if(isTypingContext(event.target)) return;\n        event.preventDefault();\n        undoLastAction();\n      }\n    });\n\n''' + anchor
    if anchor not in text:
        raise SystemExit('Could not locate hotkeys section')
    text = text.replace(anchor, block, 1)

path.write_text(text, encoding='utf-8')
