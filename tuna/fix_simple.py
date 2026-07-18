import sys
f=open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html','r',encoding='utf-8')
c=f.read()
f.close()

# 1. Hero below subtitle + remove comparison line
old = '<div class="back"><a href="/">\u2190 fraile.ch</a></div>\n\n    <div class="hero-cover">\n      <img src="cover.jpg" alt="Tuna Suiza 2026 \u2014 foto de grupo" />\n    </div>\n\n    <p class="eyebrow">Tuna \u00b7 Julio 2026</p>\n  <h1>Gira <em>Suiza</em></h1>\n  <p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>\n  <p style="font-size:12px;color:var(--warm-grey);margin-top:-28px;margin-bottom:36px;">\U0001f680 Ruta Original \u00b7 <strong>\u2195</strong> \u00b7 \U0001f504 Ruta Alternativa \u00b7 <strong>\u2195</strong> \u00b7 \U0001f195 Ruta Real (v\u00eda Aosta/Chamonix)</p>'
new = '<div class="back"><a href="/">\u2190 fraile.ch</a></div>\n\n    <p class="eyebrow">Tuna \u00b7 Julio 2026</p>\n  <h1>Gira <em>Suiza</em></h1>\n  <p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>\n\n    <div class="hero-cover">\n      <img src="cover.jpg" alt="Tuna Suiza 2026 \u2014 foto de grupo" />\n    </div>'
c = c.replace(old, new)
print('1. ' + str(len(c)))

# 2. Remove radio + tabs + content-f
s = c.find('<input type="radio"')
e = c.find('</div><!-- /content-f -->', s) + len('</div><!-- /content-f -->')
c = c[:s] + c[e:]
print('2. ' + str(len(c)))

# 3. Remove content-r (Ruta Alternativa) - find by nearest <!-- before RUTA ALTERNATIVA
alt_pos = c.find('RUTA ALTERNATIVA')
comment_start = c.rfind('<!--', 0, alt_pos)
close_pos = c.find('</div><!-- /content-r -->', alt_pos) + len('</div><!-- /content-r -->')
c = c[:comment_start] + c[close_pos:]
print('3. ' + str(len(c)))

# 4. Remove wrappers
c = c.replace('<div class="route-wrap">\n        ', '')
c = c.replace('\n        </div><!-- /route-wrap -->', '')
c = c.replace('<div class="route-content" id="content-r2">\n\n                ', '')
c = c.replace('\n        </div><!-- /content-r2 -->', '')
print('4. ' + str(len(c)))

# 5. Remove route-tabs CSS
old_css = '\n    .route-tabs { display: flex; gap: 0; margin-bottom: 24px; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }\n    .route-wrap input[type="radio"] { display: none; }\n    .route-tabs label {\n      flex: 1; padding: 14px 18px; cursor: pointer; text-align: center;\n      font-size: 12px; font-weight: 500; letter-spacing: 0.06em;\n      text-transform: uppercase; color: var(--warm-grey);\n      background: rgba(255,255,255,0.3);\n      transition: all 0.25s; user-select: none;\n      border-right: 1px solid var(--border);\n    }\n    .route-tabs label:last-child { border-right: none; }\n    #route-f:checked ~ .route-tabs label[for="route-f"],\n        #route-r:checked ~ .route-tabs label[for="route-r"],\n        #route-r2:checked ~ .route-tabs label[for="route-r2"] { background: var(--accent); color: #fff; }\n        .route-wrap .route-content { display: none; }\n        #route-f:checked ~ #content-f,\n        #route-r:checked ~ #content-r,\n        #route-r2:checked ~ #content-r2 { display: block; }'
c = c.replace(old_css, '')
print('5. ' + str(len(c)))

# 6. Milan collapsed - find nearest <!-- MILAN then remove 'open'
mil_pos = c.find('MIL\u00c1N')
open_tag = '<details class="city-card" open>'
oi = c.find(open_tag, mil_pos)
c = c[:oi] + '<details class="city-card">' + c[oi + len(open_tag):]
print('6. ' + str(len(c)))

# 7. Friburgo-Stuttgart
c = c.replace('Ginebra \u00b7 Neuch\u00e2tel \u00b7 Basilea', 'Friburgo \u00b7 Stuttgart')
print('7. ' + str(len(c)))

# 8. Move password + links + budget to bottom
pw_s = c.find('passwordGate')
pw_comment_start = c.rfind('<!--', 0, pw_s)
pw_e = c.find('</section>', pw_s) + len('</section>')
pw_sec = c[pw_comment_start:pw_e]
c = c[:pw_comment_start] + c[pw_e:]
print('8a. ' + str(len(c)))

bg_s = c.find('PRESUPUESTO')
bg_comment_start = c.rfind('<!--', 0, bg_s)
bg_e = c.find('</div><!-- /budget-wrap -->', bg_s) + len('</div><!-- /budget-wrap -->')
bg_sec = c[bg_comment_start:bg_e]
c = c[:bg_comment_start] + c[bg_e:]
print('8b. ' + str(len(c)))

script_s = c.find('<script>')
c = c[:script_s] + '\n\n' + pw_sec + '\n\n' + bg_sec + '\n\n' + c[script_s:]
print('8. ' + str(len(c)))

# 9. Clean budget
c = c.replace('<!-- Forward -->', '')
c = c.replace('<!-- Reverse -->', '')
c = c.replace('grid-template-columns:1fr 1fr 1fr', 'grid-template-columns:1fr')
fwd = c.find('<!-- Forward -->')
real = c.find('<!-- Real -->')
if fwd > 0 and real > fwd:
    c = c[:fwd] + c[real:]
print('9. ' + str(len(c)))

# 10. Meta description
old = 'Tres rutas: Original (Mil\u00e1n\u2192Suiza\u2192Stuttgart), Alternativa (Tur\u00edn\u2192Suiza) y Real (Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Basilea\u2192Stuttgart\u2192Lugano\u2192Mil\u00e1n). Parking, restaurantes espa\u00f1oles, presupuesto.'
new_d = 'Ruta Real: Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Friburgo\u2192Stuttgart\u2192Z\u00farich\u2192Lugano\u2192Mil\u00e1n. Parking, restaurantes espa\u00f1oles, presupuesto.'
c = c.replace(old, new_d)

# 11. Subtitle margin
c = c.replace('.subtitle { margin-bottom: 40px; }', '.subtitle { margin-bottom: 0; }')

# Write
f=open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html','w',encoding='utf-8')
f.write(c)
f.close()

print('\nDONE: ' + str(len(c)) + ' bytes')
checks = [
    ('RUTA ALTERNATIVA', 'ALT removed'),
    ('RUTA ORIGINAL', 'ORI removed'),
    ('route-tabs', 'tabs removed'),
    ('route-wrap', 'wrap removed'),
    ('content-f', 'c-f removed'),
    ('content-r', 'c-r removed'),
    ('Friburgo', 'Friburgo present'),
]
for term, msg in checks:
    print('  ' + msg + ': ' + str(not (term in c)) if 'removed' in msg else str(term in c))

pw_pos = c.find('passwordGate')
budget_pos = c.find('PRESUPUESTO')
print('  PW at bottom: ' + str(pw_pos > len(c)*0.6))
print('  Budget at bottom: ' + str(budget_pos > len(c)*0.6))
print('  Milan open: ' + str('<details class="city-card" open>' in c))
print('  Hero below subtitle: ' + str(c.find('hero-cover') > c.find('13')))