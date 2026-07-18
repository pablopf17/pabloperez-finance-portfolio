import json, re, shutil, os

HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, 'index.html')

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<script type="__bundler/template">\n(.*)\n  <\/script>', content, re.DOTALL)
decoded = json.loads(match.group(1))

# ─── 1. ADD i18n KEYS TO T OBJECT ───
playlist_keys = {
    'es': "play:'▶ Reproducir todo',stop:'⏹ Detener',shuffle:'Aleatorio',showList:'Mostrar lista',prev:'Anterior',next:'Siguiente',playlist:'Playlist',emptyPl:'Selecciona un vídeo y pulsa Reproducir todo',closePl:'Cerrar playlist'",
    'en': "play:'▶ Play All',stop:'⏹ Stop',shuffle:'Shuffle',showList:'Show list',prev:'Previous',next:'Next',playlist:'Playlist',emptyPl:'Select a video and press Play All',closePl:'Close playlist'",
    'fr': "play:'▶ Tout lire',stop:'⏹ Arrêter',shuffle:'Aléatoire',showList:'Voir la liste',prev:'Précédent',next:'Suivant',playlist:'Playlist',emptyPl:'Sélectionnez une vidéo et appuyez sur Tout lire',closePl:'Fermer la playlist'",
    'de': "play:'▶ Alle abspielen',stop:'⏹ Stoppen',shuffle:'Zufall',showList:'Liste anzeigen',prev:'Vorherige',next:'Nächste',playlist:'Playlist',emptyPl:'Wählen Sie ein Video und drücken Sie Alle abspielen',closePl:'Playlist schließen'",
    'it': "play:'▶ Riproduci tutto',stop:'⏹ Ferma',shuffle:'Casuale',showList:'Mostra lista',prev:'Precedente',next:'Successivo',playlist:'Playlist',emptyPl:'Seleziona un video e premi Riproduci tutto',closePl:'Chiudi playlist'",
    'zh': "play:'▶ 全部播放',stop:'⏹ 停止',shuffle:'随机',showList:'显示列表',prev:'上一个',next:'下一个',playlist:'播放列表',emptyPl:'选择视频并按全部播放',closePl:'关闭播放列表'",
}

t_start = decoded.find('const T = {')
t_end = decoded.find('};', t_start) + 2

# For each language block, insert keys before the closing brace
old_t = decoded[t_start:t_end]
for lang, keys in playlist_keys.items():
    marker = f"  {lang}: {{"
    idx = old_t.find(marker)
    if idx < 0:
        print(f"SKIP {lang}: not found")
        continue
    # Find the closing '  },' or '  }' of this lang block
    close_marker = '  },\n' if lang != 'zh' else '  }\n'
    # Actually, the last one is '  }\n' and the rest are '  },\n'
    close_idx = old_t.find(f'  }},\n', idx)
    if close_idx < 0:
        close_idx = old_t.find(f'  }}\n', idx)
    if close_idx < 0:
        print(f"SKIP {lang}: closing brace not found")
        continue
    # Insert before the closing '  }'
    # Find the start of '  }' line
    brace_start = close_idx
    old_t = old_t[:brace_start] + f',\n    {keys}' + old_t[brace_start:]

decoded = decoded[:t_start] + old_t + decoded[t_end:]
print("T object updated")

# ─── 2. UPDATE FUNCTIONS TO USE T ───

# plUI: use t.play/t.stop
old_plui = 'function plUI(){var b=document.getElementById("pl-play-all");b&&(b.textContent=plA?"\\u23f9 Detener":"\\u25b6 Reproducir todo",b.classList.toggle("active",plA));plRender()}'
new_plui = 'function plUI(){var t=T[currentLang],b=document.getElementById("pl-play-all");b&&(b.textContent=plA?t.stop:t.play,b.classList.toggle("active",plA));plRender()}'
if old_plui in decoded:
    decoded = decoded.replace(old_plui, new_plui)
    print("plUI updated")
else:
    print("WARNING: plUI pattern not found, trying fuzzy match")
    # Find by function name
    fu = decoded.find('function plUI(){')
    fe = decoded.find('}', fu) + 1
    print(f"  Found at {fu}: {repr(decoded[fu:fe][:80])}...")

# plRender: use t.emptyPl
old_empty = 'e.textContent="Selecciona un v\\u00eddeo y pulsa Reproducir todo"'
new_empty = 'e.textContent=T[currentLang].emptyPl'
if old_empty in decoded:
    decoded = decoded.replace(old_empty, new_empty)
    print("plRender empty state updated")
else:
    print("WARNING: empty text not found")

# plAddCtl: use t.prev/t.next for titles and text
old_plc1 = '"<button class=\\"modal-pl-btn\\" id=\\"pl-prev\\" title=\\"Anterior\\">\\u23ee Anterior</button><button class=\\"modal-pl-btn\\" id=\\"pl-next\\" title=\\"Siguiente\\">Siguiente \\u23ed</button>"'
new_plc1 = '""+T[currentLang].prev+"||prev||\\u23ee "+T[currentLang].prev+"||next||"+T[currentLang].next+" "+T[currentLang].next+" \\u23ed"'
# This approach is getting messy. Let me use a different strategy:
# Build the HTML with JavaScript string operations

# Find the plAddCtl function and replace its innerHTML
old_plc_fn = 'function plAddCtl(){var mi=document.querySelector(".modal-info");if(!mi||mi.querySelector(".modal-pl-btn"))return;var d=document.createElement("div");d.className="modal-pl-controls";d.innerHTML="<button class=\\"modal-pl-btn\\" id=\\"pl-prev\\" title=\\"Anterior\\">\\u23ee Anterior</button><button class=\\"modal-pl-btn\\" id=\\"pl-next\\" title=\\"Siguiente\\">Siguiente \\u23ed</button>";mi.appendChild(d);document.getElementById("pl-prev").addEventListener("click",function(e){e.stopPropagation();plI>0&&plPrev()});document.getElementById("pl-next").addEventListener("click",function(e){e.stopPropagation();plNext()})}'

new_plc_fn = 'function plAddCtl(){var mi=document.querySelector(".modal-info"),t=T[currentLang];if(!mi||mi.querySelector(".modal-pl-btn"))return;var d=document.createElement("div");d.className="modal-pl-controls";d.innerHTML="<button class=\\"modal-pl-btn\\" id=\\"pl-prev\\">\\u23ee "+t.prev+"</button><button class=\\"modal-pl-btn\\" id=\\"pl-next\\">"+t.next+" \\u23ed</button>";mi.appendChild(d);document.getElementById("pl-prev").addEventListener("click",function(e){e.stopPropagation();plI>0&&plPrev()});document.getElementById("pl-next").addEventListener("click",function(e){e.stopPropagation();plNext()})}'

if old_plc_fn in decoded:
    decoded = decoded.replace(old_plc_fn, new_plc_fn)
    print("plAddCtl updated")
else:
    print("WARNING: plAddCtl pattern not found")
    # Debug: find it
    fp = decoded.find('function plAddCtl(){')
    if fp >= 0:
        fp_end = decoded.find('})}', fp) + 3
        print(f"  Found at {fp}: {repr(decoded[fp:min(fp+100, len(decoded))])}")

# ─── 3. UPDATE setLang to handle playlist ───
old_setlang_end = "localStorage.setItem('ppf-music-lang', lang);"
idx = decoded.find(old_setlang_end)
if idx >= 0:
    close_brace = decoded.find('\n}', idx) + 2
    pl_i18n = (
        '\n  // Playlist i18n\n'
        "  var pb=document.getElementById('pl-play-all');if(pb){pb.textContent=plA?t.stop:t.play}\n"
        "  var ps=document.getElementById('pl-shuffle');if(ps)ps.title=t.shuffle\n"
        "  var pp=document.getElementById('pl-panel-toggle');if(pp)pp.title=t.showList\n"
        "  var pl=document.getElementById('pl-title');if(pl)pl.textContent=t.playlist\n"
        "  var pc=document.getElementById('pl-close');if(pc)pc.setAttribute('aria-label',t.closePl)\n"
    )
    decoded = decoded[:close_brace] + pl_i18n + decoded[close_brace:]
    print("setLang updated")
else:
    print("WARNING: setLang end not found")

# ─── 4. VERIFY ───
checks = ['Reproducir todo', 'Play All', 'Tout lire', 'Alle abspielen', 'Riproduci tutto', '全部播放']
for c in checks:
    print(f"  '{c}': {'OK' if c in decoded else 'MISSING'}")

# ─── 5. ENCODE ───
bs = chr(92)
fix = '<' + bs + 'u002F' + 'script>'
escaped = json.dumps(decoded).replace('</script>', fix)
new_script = '<script type="__bundler/template">\n' + escaped + '\n  </script>'
match = re.search(r'<script type="__bundler/template">\n.*?\n  <\/script>', content, re.DOTALL)
new_content = content[:match.start()] + new_script + content[match.end():]

new_raw = re.search(r'<script type="__bundler/template">\n(.+?)\n  <\/script>', new_content, re.DOTALL).group(1)
if '</script>' in new_raw:
    print("ERROR: </script> in raw!"); exit(1)

d = json.loads(new_raw)
print(f"JSON valid, size: {len(content)} -> {len(new_content)}")
shutil.copy2(HTML_PATH, HTML_PATH+'.bak')
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Written!")