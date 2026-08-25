from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, got {count}')
    text = text.replace(old, new, 1)

# Remove the separate Auto-Emoji control. The remaining Emoji button becomes the mode toggle.
replace_once(
'''            <label data-placement-control="autoEmoji" class="label" title="Automatically prepend an emoji based on the text"><input id="autoEmoji" type="checkbox"> Emoji</label>\n''',
'',
'auto emoji html')

# Promote Emoji button to an accessible mode toggle.
replace_once(
'''            <button data-placement-control="emoji" id="reEmoji" type="button" title="Add or remove emojis on all existing chips" class="btn">Emoji</button>''',
'''            <button data-placement-control="emoji" id="reEmoji" type="button" class="btn" aria-pressed="false" title="Emoji-Modus: neue Chips automatisch mit passendem Emoji">Emoji</button>''',
'emoji button html')

# Remove obsolete DOM ref and add a direct mode button ref.
replace_once(
'''    const randToggle = document.getElementById('randColor');\n    const emojiToggle = document.getElementById('autoEmoji');\n    const exportBtn = document.getElementById('exportBtn');''',
'''    const randToggle = document.getElementById('randColor');\n    const emojiModeBtn = document.getElementById('reEmoji');\n    const exportBtn = document.getElementById('exportBtn');''',
'emoji dom ref')

# Add persisted emoji mode state alongside other global UI state.
replace_once(
'''    const BEAMER_THEME_KEY = 'discussion.beamerTheme.v1';\n    const CHIP_FOCUS_CLASS = 'chip-focus';''',
'''    const BEAMER_THEME_KEY = 'discussion.beamerTheme.v1';\n    const EMOJI_MODE_KEY = 'discussion.emojiMode.v1';\n    let emojiMode = readStorage(EMOJI_MODE_KEY) === '1';\n    const CHIP_FOCUS_CLASS = 'chip-focus';''',
'emoji mode storage state')

# Replace checkbox-driven automatic emoji behavior with the single persisted mode.
replace_once(
'''    function detectEmoji(label){ if(label.includes('?')) return '❓'; if(label.includes('!')) return '❗'; for(const r of emojiRules) if(hasAny(label,r.words)) return r.e; return ''; }\n    function maybeAddEmoji(label){ if(!emojiToggle||!emojiToggle.checked) return label; if(startsWithEmoji(label)) return label; const em=detectEmoji(label); return em? (em+' '+label):label; }''',
'''    function detectEmoji(label){ if(label.includes('?')) return '❓'; if(label.includes('!')) return '❗'; for(const r of emojiRules) if(hasAny(label,r.words)) return r.e; return ''; }\n    function maybeAddEmoji(label){ if(!emojiMode) return label; if(startsWithEmoji(label)) return label; const em=detectEmoji(label); return em? (em+' '+label):label; }\n\n    function syncEmojiModeUI(){\n      if(!emojiModeBtn) return;\n      emojiModeBtn.classList.toggle('btn-primary', emojiMode);\n      emojiModeBtn.setAttribute('aria-pressed', String(emojiMode));\n      emojiModeBtn.title = emojiMode\n        ? 'Emoji-Modus aktiv: neue Chips erhalten automatisch ein passendes Emoji'\n        : 'Emoji-Modus aus: neue Chips werden ohne automatisches Emoji erstellt';\n    }\n\n    function setEmojiMode(active){\n      emojiMode = Boolean(active);\n      writeStorage(EMOJI_MODE_KEY, emojiMode ? '1' : '0');\n      syncEmojiModeUI();\n    }''',
'maybe add emoji mode')

# Replace the old bulk re-emoji behavior with simple mode toggling. Existing chips are untouched.
old_block = '''    // Toggle emojis on existing chips\n    const reEmojiBtn=document.getElementById('reEmoji');\n    if(reEmojiBtn){\n      reEmojiBtn.addEventListener('click', ()=>{\n        const buttons=Array.from(list.querySelectorAll('.btn-item'));\n        const removeEmojis=buttons.some(btn=>startsWithEmoji(btn.textContent||''));\n        if(buttons.length) pushUndoSnapshot();\n        let changed=0;\n        buttons.forEach(btn=>{\n          const txt=btn.textContent||'';\n          if(removeEmojis){\n            const clean=removeLeadingEmoji(txt);\n            if(clean!==txt){ btn.textContent=clean; changed++; }\n          }else if(!startsWithEmoji(txt)){\n            const em=detectEmoji(txt);\n            if(em){ btn.textContent=em+' '+txt; changed++; }\n          }\n        });\n        try{ reEmojiBtn.animate([{transform:'scale(1)'},{transform:'scale(1.06)'},{transform:'scale(1)'}],{duration:220}); }catch(err){}\n        reEmojiBtn.title = removeEmojis\n          ? (changed ? ('Removed emojis from '+changed+' chip'+(changed===1?'':'s')) : 'No emojis to remove')\n          : (changed ? ('Added emojis to '+changed+' chip'+(changed===1?'':'s')) : 'No changes (nothing matched)');\n        refreshChipMetrics();\n        saveChips();\n      });\n    }'''
new_block = '''    // Emoji mode affects newly created chips only; existing chips stay unchanged.\n    if(emojiModeBtn){\n      syncEmojiModeUI();\n      emojiModeBtn.addEventListener('click', ()=>{\n        setEmojiMode(!emojiMode);\n        try{ emojiModeBtn.animate([{transform:'scale(1)'},{transform:'scale(1.06)'},{transform:'scale(1)'}],{duration:180}); }catch(err){}\n      });\n    }'''
replace_once(old_block, new_block, 'old emoji bulk behavior')

# Update smoke test so it tests the new mode instead of the removed checkbox/bulk rewrite behavior.
old_smoke = '''    function runSmokeTests(){ try{ const before=list.children.length; if(emojiToggle) emojiToggle.checked=true; ['Bug','Kaffeemaschine','Lift','YouTube','TikTok','Webseite','Computer','Netzwerk','Drucker'].forEach(t=>{ input.value=t; addFromInput(); }); const after=list.children.length; console.assert(after>=before+9, 'Should add 9 chips'); const first=list.querySelector('.btn-item'); console.assert(first && /\\p{Extended_Pictographic}/u.test(first.textContent.trim().charAt(0))===true, 'First chip should start with an emoji'); first.click(); console.assert(Number(first.dataset.scaleStage||'0')===1,'First cycle should set stage 1'); first.click(); console.assert(Number(first.dataset.scaleStage||'0')===2,'Second cycle should set stage 2'); first.click(); console.assert(Number(first.dataset.scaleStage||'0')===3,'Third cycle should set stage 3'); first.click(); console.assert(Number(first.dataset.scaleStage||'0')===0,'Fourth cycle should reset stage'); const emojiBtn=document.getElementById('reEmoji'); emojiBtn.click(); console.assert(!startsWithEmoji(first.textContent),'Emoji button should remove leading emojis'); emojiBtn.click(); console.assert(startsWithEmoji(first.textContent),'Emoji button should add leading emojis'); }catch(e){ console.warn('Smoke tests issue (non-fatal):', e); } }'''
new_smoke = '''    function runSmokeTests(){ try{ const before=list.children.length; setEmojiMode(true); ['Bug','Kaffeemaschine','Lift','YouTube','TikTok','Webseite','Computer','Netzwerk','Drucker'].forEach(t=>{ input.value=t; addFromInput(); }); const after=list.children.length; console.assert(after>=before+9, 'Should add 9 chips'); const first=list.querySelector('.btn-item'); console.assert(first && /\\p{Extended_Pictographic}/u.test(first.textContent.trim().charAt(0))===true, 'First chip should start with an emoji'); first.click(); console.assert(Number(first.dataset.scaleStage||'0')===1,'First cycle should set stage 1'); first.click(); console.assert(Number(first.dataset.scaleStage||'0')===2,'Second cycle should set stage 2'); first.click(); console.assert(Number(first.dataset.scaleStage||'0')===3,'Third cycle should set stage 3'); first.click(); console.assert(Number(first.dataset.scaleStage||'0')===0,'Fourth cycle should reset stage'); const beforeToggle = first.textContent; setEmojiMode(false); console.assert(first.textContent===beforeToggle,'Changing Emoji mode must not rewrite existing chips'); }catch(e){ console.warn('Smoke tests issue (non-fatal):', e); } }'''
replace_once(old_smoke, new_smoke, 'smoke test')

# Remove Auto-Emoji from the user-configurable placement list. Old saved keys are harmless and ignored.
replace_once(
'''        { key:'color', label:'Color', defaultPlace:'main' },\n        { key:'autoEmoji', label:'Auto-Emoji', defaultPlace:'main' },\n        { key:'emoji', label:'Emoji', defaultPlace:'main' },''',
'''        { key:'color', label:'Color', defaultPlace:'main' },\n        { key:'emoji', label:'Emoji', defaultPlace:'main' },''',
'placement auto emoji')

# Remove obsolete special styling for the deleted checkbox.
old_css = '''    label:has(#autoEmoji){font-size:0}\n    label:has(#autoEmoji)::after{\n      content:'Auto-Emoji';\n      font-size:.84rem;\n      font-weight:650;\n      color:#334155;\n    }\n\n'''
replace_once(old_css, '', 'auto emoji css')

path.write_text(text, encoding='utf-8')
