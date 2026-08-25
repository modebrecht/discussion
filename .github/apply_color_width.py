from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_width = """    .container{\n      padding-left:clamp(.9rem,1.5vw,1.5rem);\n      padding-right:clamp(.9rem,1.5vw,1.5rem);\n    }"""
new_width = """    .container{\n      padding-left:clamp(.35rem,.6vw,.7rem);\n      padding-right:clamp(.35rem,.6vw,.7rem);\n    }\n\n    #list{\n      padding-left:2px;\n      padding-right:2px;\n    }"""
if old_width not in text:
    raise SystemExit('Full-width block not found')
text = text.replace(old_width, new_width, 1)

old_mobile = """      .container{padding-left:.8rem;padding-right:.8rem}"""
new_mobile = """      .container{padding-left:.55rem;padding-right:.55rem}"""
if old_mobile not in text:
    raise SystemExit('Mobile width block not found')
text = text.replace(old_mobile, new_mobile, 1)

old_color = """    function randomColorHex(){ return BEAMER_COLORS[Math.floor(Math.random()*BEAMER_COLORS.length)]; }"""
new_color = """    function randomColorHex(){\n      if(!BEAMER_COLORS.length) return '#60A5FA';\n      const lastWrap = list ? list.lastElementChild : null;\n      const lastChip = lastWrap && lastWrap.querySelector ? lastWrap.querySelector('.btn-item') : null;\n      const previousColor = lastChip && lastChip.dataset ? lastChip.dataset.color : null;\n      const choices = BEAMER_COLORS.filter(color => color !== previousColor);\n      const pool = choices.length ? choices : BEAMER_COLORS;\n      return pool[Math.floor(Math.random()*pool.length)];\n    }"""
if old_color not in text:
    raise SystemExit('Random color function not found')
text = text.replace(old_color, new_color, 1)

path.write_text(text, encoding='utf-8')
