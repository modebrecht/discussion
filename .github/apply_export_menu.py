from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 anchor, found {count}')
    text = text.replace(old, new, 1)

# 1) Export dropdown markup.
replace_once(
'''        <button id="exportBtn" type="button" class="btn" title="Download chips as a file">Export</button>''',
'''        <div class="export-controls">
          <button id="exportBtn" type="button" class="btn" aria-haspopup="true" aria-expanded="false" title="Board exportieren">Export ▾</button>
          <div id="exportMenu" class="export-menu" hidden role="menu" aria-label="Exportformat">
            <button type="button" class="export-menu-btn" data-export-format="json" role="menuitem">JSON</button>
            <button type="button" class="export-menu-btn" data-export-format="png" role="menuitem">PNG</button>
            <button type="button" class="export-menu-btn" data-export-format="svg" role="menuitem">SVG</button>
          </div>
        </div>''',
'export toolbar markup')

# 2) Export menu styles.
css = r'''

  <style>
    /* ===== Board export menu ===== */
    .export-controls{position:relative;display:inline-flex;align-items:center}
    .export-menu{
      position:absolute;
      z-index:220;
      top:calc(100% + .5rem);
      right:0;
      min-width:118px;
      padding:5px;
      display:grid;
      gap:3px;
      border:1px solid #dbe3ee;
      border-radius:13px;
      background:#fff;
      box-shadow:0 16px 38px rgba(15,23,42,.18);
    }
    .export-menu[hidden]{display:none}
    .export-menu-btn{
      min-height:34px;
      padding:.42rem .65rem;
      border:0;
      border-radius:9px;
      background:transparent;
      color:#1e293b;
      text-align:left;
      font:800 .8rem/1 ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;
      cursor:pointer;
    }
    .export-menu-btn:hover,.export-menu-btn:focus-visible{background:#f1f5f9;outline:none}
    .export-menu-btn:disabled{opacity:.5;cursor:wait}
    html[data-beamer-theme="dark"] .export-menu{background:#0f172a;border-color:#334155;box-shadow:0 18px 42px rgba(0,0,0,.42)}
    html[data-beamer-theme="dark"] .export-menu-btn{color:#e2e8f0}
    html[data-beamer-theme="dark"] .export-menu-btn:hover,
    html[data-beamer-theme="dark"] .export-menu-btn:focus-visible{background:#1e293b}
  </style>
'''
replace_once('</head>', css + '\n</head>', 'head closing tag')

# 3) DOM ref.
replace_once(
'''    const exportBtn = document.getElementById('exportBtn');''',
'''    const exportBtn = document.getElementById('exportBtn');
    const exportMenu = document.getElementById('exportMenu');''',
'export DOM ref')

# 4) Export helpers + replace old one-click JSON handler with dropdown behavior.
old_handler = '''    if(exportBtn){
      exportBtn.addEventListener('click', ()=>{
        const payload = getChipData();
        const blob = new Blob([JSON.stringify(payload, null, 2)], { type:'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = EXPORT_FILENAME;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setTimeout(()=>URL.revokeObjectURL(url), 0);
      });
    }
'''

new_handler = r'''    function exportBaseName(){
      const active = getActiveSave();
      const source = active && active.name ? active.name : saveDatePrefix();
      const cleaned = String(source)
        .replace(/#/g, '-')
        .replace(/[^0-9A-Za-z._-]+/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '');
      return 'discussion-' + (cleaned || 'board');
    }

    function downloadBlob(blob, filename){
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(() => URL.revokeObjectURL(url), 0);
    }

    function svgNode(name, attrs = {}){
      const node = document.createElementNS('http://www.w3.org/2000/svg', name);
      Object.entries(attrs).forEach(([key, value]) => {
        if(value !== null && value !== undefined) node.setAttribute(key, String(value));
      });
      return node;
    }

    function svgText(parent, text, attrs = {}){
      const node = svgNode('text', attrs);
      node.textContent = text == null ? '' : String(text);
      parent.appendChild(node);
      return node;
    }

    function buildBoardSvg(){
      if(!list) throw new Error('Board not found');
      layoutChipsNow();
      const boardRect = list.getBoundingClientRect();
      const boardWidth = Math.max(1, Math.ceil(boardRect.width));
      const boardHeight = Math.max(1, Math.ceil(Math.max(boardRect.height, list.offsetHeight || 0)));
      const pad = 26;
      const width = boardWidth + pad * 2;
      const height = boardHeight + pad * 2;
      const dark = document.documentElement.dataset.beamerTheme === 'dark';
      const background = dark ? '#05070b' : (getComputedStyle(document.body).backgroundColor || '#f6f7fb');
      const shape = document.documentElement.dataset.chipShape || 'pill';

      const svg = svgNode('svg', {
        xmlns:'http://www.w3.org/2000/svg',
        width,
        height,
        viewBox:`0 0 ${width} ${height}`
      });
      svg.appendChild(svgNode('rect', { x:0, y:0, width, height, fill:background }));

      const groupMeta = {
        pro:{ label:'PRO', fill:'#dcfce7', color:'#166534' },
        contra:{ label:'CONTRA', fill:'#ffe4e6', color:'#9f1239' },
        fragen:{ label:'FRAGE', fill:'#f3e8ff', color:'#7e22ce' }
      };

      Array.from(list.querySelectorAll('.btn-item')).forEach(btn => {
        const wrap = btn.closest('.btn-wrap');
        if(!wrap) return;
        const rect = btn.getBoundingClientRect();
        const cs = getComputedStyle(btn);
        const ws = getComputedStyle(wrap);
        const x = pad + rect.left - boardRect.left;
        const y = pad + rect.top - boardRect.top;
        const w = Math.max(1, rect.width);
        const h = Math.max(1, rect.height);
        const computedRadius = parseFloat(cs.borderRadius) || 0;
        const rx = shape === 'pill' ? h / 2 : Math.min(h / 2, computedRadius || 16);
        const opacity = Math.max(0, Math.min(1, parseFloat(ws.opacity) || 1));
        const g = svgNode('g', { opacity });
        svg.appendChild(g);

        const chipRect = svgNode('rect', {
          x, y, width:w, height:h, rx, ry:rx,
          fill:cs.backgroundColor || '#ffffff',
          stroke:cs.borderColor || '#cbd5e1',
          'stroke-width':Math.max(1, parseFloat(cs.borderTopWidth) || 1)
        });
        if(btn.classList.contains(CHIP_SPOTLIGHT_CLASS)){
          chipRect.setAttribute('stroke-width','3');
          chipRect.setAttribute('stroke', btn.dataset.color || '#0EA5E9');
        }else if(btn.classList.contains(CHIP_FOCUS_CLASS)){
          chipRect.setAttribute('stroke-width','3');
          chipRect.setAttribute('stroke','#0891b2');
        }
        g.appendChild(chipRect);

        svgText(g, btn.textContent || '', {
          x:x + w / 2,
          y:y + h / 2,
          fill:cs.color || '#111827',
          'font-family':cs.fontFamily || 'system-ui, sans-serif',
          'font-size':parseFloat(cs.fontSize) || 16,
          'font-weight':cs.fontWeight || 700,
          'text-anchor':'middle',
          'dominant-baseline':'central'
        });

        const group = btn.dataset.group || '';
        const meta = groupMeta[group];
        if(meta){
          const gw = meta.label.length * 6.2 + 12;
          const gh = 18;
          const gx = Math.max(2, x - 5);
          const gy = Math.max(2, y - 8);
          g.appendChild(svgNode('rect', { x:gx, y:gy, width:gw, height:gh, rx:9, fill:meta.fill, stroke:'rgba(15,23,42,.12)' }));
          svgText(g, meta.label, {
            x:gx + gw/2, y:gy + gh/2 + .5, fill:meta.color,
            'font-family':'system-ui, sans-serif', 'font-size':9, 'font-weight':850,
            'text-anchor':'middle', 'dominant-baseline':'central'
          });
        }

        const badgeText = wrap.dataset.badge || '';
        if(badgeText){
          const bw = Math.max(21, Array.from(badgeText).length * 12 + 6);
          const bh = 21;
          const bx = Math.min(width - bw - 2, x + w - bw/2 + 4);
          const by = Math.max(2, y - 10);
          g.appendChild(svgNode('rect', {
            x:bx, y:by, width:bw, height:bh, rx:bh/2,
            fill:dark ? '#0f172a' : '#ffffff', stroke:dark ? '#475569' : '#cbd5e1'
          }));
          svgText(g, badgeText, {
            x:bx+bw/2, y:by+bh/2+.5, fill:dark ? '#ffffff' : '#111827',
            'font-family':'system-ui, sans-serif', 'font-size':11,
            'text-anchor':'middle', 'dominant-baseline':'central'
          });
        }

        const votes = Math.max(0, Math.round(Number(btn.dataset.votes || '0')) || 0);
        if(votes > 0){
          const label = String(votes);
          const vw = Math.max(22, label.length * 7 + 12);
          const vh = 22;
          const vx = Math.min(width - vw - 2, x + w - vw/2 + 5);
          const vy = Math.min(height - vh - 2, y + h - 7);
          const voteFill = dark ? '#f8fafc' : '#0f172a';
          const voteInk = dark ? '#0f172a' : '#ffffff';
          g.appendChild(svgNode('rect', { x:vx, y:vy, width:vw, height:vh, rx:vh/2, fill:voteFill, stroke:background, 'stroke-width':2 }));
          svgText(g, label, {
            x:vx+vw/2, y:vy+vh/2+.5, fill:voteInk,
            'font-family':'system-ui, sans-serif', 'font-size':11, 'font-weight':850,
            'text-anchor':'middle', 'dominant-baseline':'central'
          });
        }
      });

      const xml = new XMLSerializer().serializeToString(svg);
      return { xml, width, height };
    }

    function exportBoardSvg(){
      const snapshot = buildBoardSvg();
      const blob = new Blob([snapshot.xml], { type:'image/svg+xml;charset=utf-8' });
      downloadBlob(blob, exportBaseName() + '.svg');
    }

    async function exportBoardPng(){
      const snapshot = buildBoardSvg();
      const svgBlob = new Blob([snapshot.xml], { type:'image/svg+xml;charset=utf-8' });
      const url = URL.createObjectURL(svgBlob);
      try{
        const image = new Image();
        const loaded = new Promise((resolve, reject) => {
          image.onload = resolve;
          image.onerror = () => reject(new Error('SVG could not be rendered'));
        });
        image.src = url;
        await loaded;
        const maxDimension = 8192;
        const scale = Math.max(1, Math.min(2, maxDimension / Math.max(snapshot.width, snapshot.height)));
        const canvas = document.createElement('canvas');
        canvas.width = Math.max(1, Math.round(snapshot.width * scale));
        canvas.height = Math.max(1, Math.round(snapshot.height * scale));
        const ctx = canvas.getContext('2d');
        if(!ctx) throw new Error('Canvas unavailable');
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
        const pngBlob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
        if(!pngBlob) throw new Error('PNG creation failed');
        downloadBlob(pngBlob, exportBaseName() + '.png');
      }finally{
        URL.revokeObjectURL(url);
      }
    }

    function exportBoardJson(){
      const payload = getChipData();
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type:'application/json' });
      downloadBlob(blob, exportBaseName() + '.json');
    }

    if(exportBtn && exportMenu){
      const setExportOpen = (open) => {
        exportMenu.hidden = !open;
        exportBtn.setAttribute('aria-expanded', String(open));
      };
      exportBtn.addEventListener('click', event => {
        event.stopPropagation();
        setExportOpen(exportMenu.hidden);
      });
      exportMenu.addEventListener('click', async event => {
        event.stopPropagation();
        const button = event.target instanceof Element ? event.target.closest('[data-export-format]') : null;
        if(!button) return;
        const format = button.dataset.exportFormat;
        setExportOpen(false);
        button.disabled = true;
        try{
          if(format === 'json') exportBoardJson();
          else if(format === 'svg') exportBoardSvg();
          else if(format === 'png') await exportBoardPng();
        }catch(err){
          console.error('Export failed:', err);
          alert('Export fehlgeschlagen. Bitte erneut versuchen.');
        }finally{
          button.disabled = false;
        }
      });
      document.addEventListener('click', () => setExportOpen(false));
      document.addEventListener('keydown', event => {
        if(event.key === 'Escape') setExportOpen(false);
      });
    }
'''
replace_once(old_handler, new_handler, 'old export handler')

path.write_text(text, encoding='utf-8')
print('Applied JSON/PNG/SVG board export menu patch')
