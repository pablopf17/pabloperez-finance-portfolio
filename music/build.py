import json, re, shutil, os

HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, 'index.html')

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<script type="__bundler/template">\n(.*)\n  <\/script>', content, re.DOTALL)
decoded = json.loads(match.group(1))

# Panel
panel = '\n<!-- PLAYLIST PANEL -->\n<div id="playlist-panel"><div class="pl-header"><span id="pl-title">Playlist</span><button id="pl-close" class="pl-close-btn" aria-label="Cerrar playlist">&times;</button></div><ul id="pl-list"></ul></div>\n<div id="pl-overlay" class="pl-overlay"></div>\n'
body_idx = decoded.rfind('</body>')
decoded = decoded[:body_idx] + panel + decoded[body_idx:]

# Buttons
btns = '\n  <div class="pl-controls">\n    <button id="pl-play-all" class="pl-btn">\u25b6 Reproducir todo</button>\n    <button id="pl-shuffle" class="pl-btn" title="Aleatorio">\U0001f500</button>\n    <button id="pl-panel-toggle" class="pl-btn" title="Mostrar lista">\u2630 <span id="pl-count-badge">0</span></button>\n  </div>\n'
grid_idx = decoded.find('<!-- GRID -->')
before_grid = decoded[:grid_idx]
last_div = before_grid.rfind('</div>')
decoded = decoded[:last_div] + '</div>' + btns + decoded[last_div+6:]

# CSS
pl_css = '\n.pl-controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:0 48px 18px;max-width:1000px;margin:0 auto}'
pl_css += '.pl-btn{font-family:var(--font-body);font-size:12px;letter-spacing:.04em;padding:7px 16px;border-radius:20px;border:1px solid var(--border);background:transparent;color:var(--cream);cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:5px;line-height:1}'
pl_css += '.pl-btn:hover{background:var(--accent);border-color:var(--accent);color:#fff}'
pl_css += '.pl-btn.active{background:var(--accent);border-color:var(--accent)}'
pl_css += '#pl-count-badge{font-size:10px;opacity:.7;min-width:14px;text-align:center}'
pl_css += '.pl-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:998;display:none}'
pl_css += '.pl-overlay.show{display:block}'
pl_css += '#playlist-panel{position:fixed;top:0;right:-360px;width:340px;max-width:90vw;height:100vh;background:#1A1714;border-left:1px solid var(--border);z-index:999;overflow-y:auto;transition:right .3s ease;display:flex;flex-direction:column}'
pl_css += '#playlist-panel.open{right:0}'
pl_css += '.pl-header{display:flex;justify-content:space-between;align-items:center;padding:16px 18px;border-bottom:1px solid var(--border);flex-shrink:0}'
pl_css += '.pl-header span{font-family:var(--font-display);font-size:18px;color:var(--cream);font-style:italic}'
pl_css += '.pl-close-btn{background:0;border:none;color:var(--warm-grey);font-size:24px;cursor:pointer;padding:0 4px}'
pl_css += '.pl-close-btn:hover{color:var(--cream)}'
pl_css += '#pl-list{list-style:none;padding:8px 0;margin:0;flex:1;overflow-y:auto}'
pl_css += '.pl-item{display:flex;align-items:center;gap:10px;padding:10px 18px;cursor:pointer;transition:background .15s;border-left:3px solid transparent;font-family:var(--font-body);font-size:13px;color:var(--warm-grey)}'
pl_css += '.pl-item:hover{background:rgba(255,255,255,.03)}'
pl_css += '.pl-item.active{color:var(--cream);border-left-color:var(--accent);background:rgba(184,147,90,.08)}'
pl_css += '.pl-item .pl-num{font-size:11px;opacity:.5;min-width:22px;text-align:right}'
pl_css += '.pl-item .pl-title{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
pl_css += '.pl-item .pl-context{font-size:10px;opacity:.5;min-width:50px;text-align:right;white-space:nowrap}'
pl_css += '.pl-item.played{opacity:.4}'
pl_css += '.modal-pl-controls{display:flex;gap:12px;justify-content:center;margin-top:14px}'
pl_css += '.modal-pl-btn{background:0;border:1px solid var(--border);color:var(--cream);padding:6px 18px;border-radius:20px;cursor:pointer;transition:all .2s;font-family:var(--font-body);font-size:13px}'
pl_css += '.modal-pl-btn:hover{background:var(--accent);border-color:var(--accent)}'
pl_css += '.modal-pl-btn:disabled{opacity:.3;cursor:default}'
last_style = decoded.rfind('</style>')
decoded = decoded[:last_style] + pl_css + decoded[last_style:]

# JS - ; prefix prevents ASI breakage when original code ends with (function(){...})()
pl_js = ';\n// PLAYLIST\n'
pl_js += 'var plQ=[],plI=-1,plA=false,plS=false,plY=null,plYr=false;\n'
pl_js += 'function plShuf(a){var b=[].concat(a),i,j,t;for(i=b.length-1;i>0;i--){j=Math.floor(Math.random()*(i+1));t=b[i];b[i]=b[j];b[j]=t}return b}\n'
pl_js += 'function plBuild(f){var c=document.querySelectorAll(".video-card:not(.hidden)"),d=Array.from(c).map(function(x){return +x.dataset.index});if(!d.length)return;plQ=plS?plShuf(d):[].concat(d);if(f!==void 0&&!plS){var p=plQ.indexOf(f);p>=0&&(plQ=plQ.slice(p).concat(plQ.slice(0,p)))}plI=0;plA=true;plRender();plBadge()}\n'
pl_js += 'function plNext(){plI++;if(plI>=plQ.length){plA=false;plY&&plY.stopVideo();closeModal();plUI();return}openModal(plQ[plI]);plRender()}\n'
pl_js += 'function plPrev(){if(plI>0){plI--;openModal(plQ[plI]);plRender()}}\n'
pl_js += 'function plStop(){plA=false;plQ=[];plI=-1;plY&&plY.stopVideo();plRender();plBadge()}\n'
pl_js += 'function plTog(){plS=!plS;document.getElementById("pl-shuffle").classList.toggle("active",plS);if(plA&&plQ.length>0){var c=plQ[plI],r=plQ.slice(plI+1);plQ=[c].concat(plS?plShuf(r):r);plI=0;plRender()}}\n'
pl_js += 'function plRender(){var l=document.getElementById("pl-list");if(!l)return;l.innerHTML="";if(!plQ.length){var e=document.createElement("li");e.className="pl-item";e.style.cssText="justify-content:center;padding:30px 18px;opacity:.4;font-style:italic";e.textContent="Selecciona un v\\u00eddeo y pulsa Reproducir todo";l.appendChild(e);return}plQ.forEach(function(idx,i){var v=VIDEOS[idx],li=document.createElement("li");li.className="pl-item"+(i===plI?" active":"")+(i<plI?" played":"");li.innerHTML="<span class=\\"pl-num\\">"+(i+1)+".</span><span class=\\"pl-title\\">"+v.title+"</span><span class=\\"pl-context\\">"+v.context+"</span>";li.addEventListener("click",function(){plI=i;plA=true;openModal(idx);plRender()});l.appendChild(li)});var a=l.querySelector(".active");a&&a.scrollIntoView({block:"nearest",behavior:"smooth"})}\n'
pl_js += 'function plBadge(){var b=document.getElementById("pl-count-badge");b&&(b.textContent=plQ.length||"0")}\n'
pl_js += 'function plUI(){var b=document.getElementById("pl-play-all");b&&(b.textContent=plA?"\\u23f9 Detener":"\\u25b6 Reproducir todo",b.classList.toggle("active",plA));plRender()}\n'
pl_js += 'function plAddCtl(){var mi=document.querySelector(".modal-info");if(!mi||mi.querySelector(".modal-pl-btn"))return;var d=document.createElement("div");d.className="modal-pl-controls";d.innerHTML="<button class=\\"modal-pl-btn\\" id=\\"pl-prev\\" title=\\"Anterior\\">\\u23ee Anterior</button><button class=\\"modal-pl-btn\\" id=\\"pl-next\\" title=\\"Siguiente\\">Siguiente \\u23ed</button>";mi.appendChild(d);document.getElementById("pl-prev").addEventListener("click",function(e){e.stopPropagation();plI>0&&plPrev()});document.getElementById("pl-next").addEventListener("click",function(e){e.stopPropagation();plNext()})}\n'
pl_js += 'function plLoadYT(){if(window.YT){plYr=true;return}if(document.querySelector("script[src=\\"https://www.youtube.com/iframe_api\\"]"))return;var t=document.createElement("script");t.src="https://www.youtube.com/iframe_api";document.getElementsByTagName("script")[0].parentNode.insertBefore(t,document.getElementsByTagName("script")[0])}\n'
pl_js += 'window.onYouTubeIframeAPIReady=function(){plYr=true};\n'
pl_js += 'var _oO=openModal;openModal=function(i){_oO(i);plAddCtl();var p=document.getElementById("pl-prev"),n=document.getElementById("pl-next");p&&(p.disabled=!plA||plI<=0);n&&(n.disabled=!plA||plI>=plQ.length-1);if(plA&&plQ.length>0){var v=VIDEOS[i],w=document.getElementById("modal-video-wrap");if(w&&plYr){var pd=document.getElementById("pl-yt-div");pd||(pd=document.createElement("div"),pd.id="pl-yt-div",w.innerHTML="",w.appendChild(pd));plY&&"function"==typeof plY.destroy&&plY.destroy();plY=new YT.Player("pl-yt-div",{height:"100%",width:"100%",videoId:v.id,playerVars:{autoplay:1,rel:0,enablejsapi:1},events:{onStateChange:function(e){e.data===YT.PlayerState.ENDED&&(plA&&plI<plQ.length-1?plNext():plA&&(plA=false,plUI()))},onError:function(){plA&&plNext()}}})}}};\n'
pl_js += 'var _oC=closeModal;closeModal=function(){_oC();!plA&&plY&&"function"==typeof plY.destroy&&(plY.destroy(),plY=null)};\n'
pl_js += 'plLoadYT();\n'
pl_js += 'document.getElementById("pl-play-all")&&document.getElementById("pl-play-all").addEventListener("click",function(){if(plA){plStop();plUI();return}var c=document.querySelectorAll(".video-card:not(.hidden)");if(!c.length)return;plBuild(+c[0].dataset.index);plUI();openModal(plQ[0])});\n'
pl_js += 'document.getElementById("pl-shuffle")&&document.getElementById("pl-shuffle").addEventListener("click",plTog);\n'
pl_js += 'var pt=document.getElementById("pl-panel-toggle"),pn=document.getElementById("playlist-panel"),ov=document.getElementById("pl-overlay"),cp=document.getElementById("pl-close");\n'
pl_js += 'pt&&pn&&pt.addEventListener("click",function(){pn.classList.toggle("open");ov&&ov.classList.toggle("show");plRender()});\n'
pl_js += 'cp&&pn&&ov&&cp.addEventListener("click",function(){pn.classList.remove("open");ov.classList.remove("show")});\n'
pl_js += 'ov&&pn&&ov.addEventListener("click",function(){pn.classList.remove("open");ov.classList.remove("show")});\n'

last_script = decoded.rfind('</script>')
decoded = decoded[:last_script] + pl_js + decoded[last_script:]

# Encode
bs = chr(92)
fix = '<' + bs + 'u002F' + 'script>'
escaped = json.dumps(decoded)
c = escaped.count('</script>')
print(f'Found {c} </script>')
escaped = escaped.replace('</script>', fix)

new_script = '<script type="__bundler/template">\n' + escaped + '\n  </script>'
old_match = re.search(r'<script type="__bundler/template">\n.*?\n  <\/script>', content, re.DOTALL)
new_content = content[:old_match.start()] + new_script + content[old_match.end():]

# Verify
new_raw = re.search(r'<script type="__bundler/template">\n(.+?)\n  <\/script>', new_content, re.DOTALL).group(1)
assert '</script>' not in new_raw, '</script> in raw!'
d = json.loads(new_raw)
for k in ['playlist-panel', 'pl-play-all', 'pl-shuffle', 'YT.Player']:
    print(f'  {k}: {"OK" if k in d else "MISSING"}')

shutil.copy2(HTML_PATH, HTML_PATH+'.bak')
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f'Written {len(new_content)} bytes')