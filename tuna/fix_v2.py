import subprocess

# Read the HEAD version
r = subprocess.run(['git', 'show', 'HEAD:tuna/index.html'], capture_output=True, text=True, cwd='C:/Users/pablo/pabloperez-finance-portfolio-live')
c = r.stdout

# 1. Move hero cover below subtitle  
c = c.replace(
    '<div class="back"><a href="/">\u2190 fraile.ch</a></div>\n\n    <div class="hero-cover">\n      <img src="cover.jpg" alt="Tuna Suiza 2026 \u2014 foto de grupo" />\n    </div>\n\n    <p class="eyebrow">Tuna \u00b7 Julio 2026</p>\n  <h1>Gira <em>Suiza</em></h1>\n    <p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>',
    '<div class="back"><a href="/">\u2190 fraile.ch</a></div>\n\n    <p class="eyebrow">Tuna \u00b7 Julio 2026</p>\n  <h1>Gira <em>Suiza</em></h1>\n    <p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>\n\n    <div class="hero-cover">\n      <img src="cover.jpg" alt="Tuna Suiza 2026 \u2014 foto de grupo" />\n    </div>'
)

# 2. Remove route comparison line
c = c.replace(
    '  <p style="font-size:12px;color:var(--warm-grey);margin-top:-28px;margin-bottom:36px;">\U0001f680 Ruta Original \u00b7 <strong>\u2195</strong> \u00b7 \U0001f504 Ruta Alternativa \u00b7 <strong>\u2195</strong> \u00b7 \U0001f195 Ruta Real (v\u00eda Aosta/Chamonix)</p>\n\n  <!-- Password gate -->',
    '\n\n  <!-- Password gate -->'
)

# 3. Remove radio inputs, tabs, and Ruta ORIGINAL section (content-f)
cf_start = c.find('    <input type="radio" name="route" id="route-f" checked>\n    <input type="radio" name="route" id="route-r">\n    <input type="radio" name="route" id="route-r2">\n    <div class="route-tabs">')
cf_end = c.find('</div><!-- /content-f -->', cf_start) + len('</div><!-- /content-f -->')
c = c[:cf_start] + c[cf_end:]

# 4. Remove Ruta Alternativa section (content-r)
alt_start = c.find('    <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 RUTA ALTERNATIVA')
alt_end = c.find('</div><!-- /content-r -->', alt_start) + len('</div><!-- /content-r -->')
c = c[:alt_start] + c[alt_end:]

# 5. Remove route-wrap wrapper 
c = c.replace('<div class="route-wrap">\n        ', '')
c = c.replace('\n        </div><!-- /route-wrap -->', '')

# 6. Remove route-content wrapper from r2
c = c.replace('<div class="route-content" id="content-r2">\n\n                ', '\n                ')
c = c.replace('\n        </div><!-- /content-r2 -->', '')

# 7. Remove route-tabs CSS (between section CSS and budget CSS)
old_css = '\n    .route-tabs { display: flex; gap: 0; margin-bottom: 24px; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }\n    .route-wrap input[type="radio"] { display: none; }\n    .route-tabs label {\n      flex: 1; padding: 14px 18px; cursor: pointer; text-align: center;\n      font-size: 12px; font-weight: 500; letter-spacing: 0.06em;\n      text-transform: uppercase; color: var(--warm-grey);\n      background: rgba(255,255,255,0.3);\n      transition: all 0.25s; user-select: none;\n      border-right: 1px solid var(--border);\n    }\n    .route-tabs label:last-child { border-right: none; }\n    #route-f:checked ~ .route-tabs label[for="route-f"],\n        #route-r:checked ~ .route-tabs label[for="route-r"],\n        #route-r2:checked ~ .route-tabs label[for="route-r2"] { background: var(--accent); color: #fff; }\n        .route-wrap .route-content { display: none; }\n        #route-f:checked ~ #content-f,\n        #route-r:checked ~ #content-r,\n        #route-r2:checked ~ #content-r2 { display: block; }'
c = c.replace(old_css, '')

# 8. Milan collapsed (only in r2 section - find the first details tag in r2)
# After removing alt, the first details in r2 should be at a specific position  
r2_milan = c.find('<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 MIL\u00c1N')
details_open = c.find('<details class="city-card" open>', r2_milan)
if details_open > 0:
    c = c[:details_open] + '<details class="city-card">' + c[details_open + len('<details class="city-card" open>'):]

# 9. Update Jue 16 to Estrasburgo-Stuttgart
c = c.replace('Ginebra \u00b7 Neuch\u00e2tel \u00b7 Basilea', 'Estrasburgo \u00b7 Stuttgart')

# 10. Move password gate + links + budget to bottom  
pw_start = c.find('<div class="password-gate" id="passwordGate">')
links_end = c.find('</section>', c.find('<!-- Links -->')) + len('</section>')
pw_section = c[pw_start:links_end]
c = c[:pw_start] + c[links_end:]

budget_start = c.find('<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 PRESUPUESTO')
budget_end = c.find('</div><!-- /budget-wrap -->', budget_start) + len('</div><!-- /budget-wrap -->')
budget_section = c[budget_start:budget_end]
c = c[:budget_start] + c[budget_end:]

script_start = c.find('<script>')
c = c[:script_start] + '\n\n' + pw_section + '\n\n' + budget_section + '\n\n' + c[script_start:]

# 11. Clean budget - remove Forward and Reverse budget tables  
c = c.replace('<!-- Forward -->', '')
c = c.replace('<!-- Reverse -->', '')
c = c.replace('grid-template-columns:1fr 1fr 1fr', 'grid-template-columns:1fr')

fwd = c.find('<!-- Forward -->')
real = c.find('<!-- Real -->')
if fwd > 0 and real > fwd:
    c = c[:fwd] + c[real:]

# 12. Update meta
old_desc = 'Tres rutas: Original (Mil\u00e1n\u2192Suiza\u2192Stuttgart), Alternativa (Tur\u00edn\u2192Suiza) y Real (Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Basilea\u2192Stuttgart\u2192Lugano\u2192Mil\u00e1n). Parking, restaurantes espa\u00f1oles, presupuesto.'
new_desc = 'Ruta Real: Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Estrasburgo\u2192Stuttgart\u2192Z\u00farich\u2192Lugano\u2192Mil\u00e1n. Parking, restaurantes espa\u00f1oles, presupuesto.'
c = c.replace(old_desc, new_desc)

# 13. Remove subtitle margin  
c = c.replace('.subtitle { margin-bottom: 40px; }', '.subtitle { margin-bottom: 0; }')

# Write
with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"File written: {len(c)} bytes")
print(f"RUTA ALTERNATIVA: {'RUTA ALTERNATIVA' in c}")
print(f"RUTA ORIGINAL: {'RUTA ORIGINAL' in c}")
print(f"content-f: {'content-f' in c}")
print(f"content-r: {'content-r' in c}")
print(f"route-tabs: {'route-tabs' in c}")
print(f"route-wrap: {'route-wrap' in c}")
print(f"Estrasburgo: {'Estrasburgo' in c}")
print(f"Ginebra · Neuch: {'Ginebra · Neuch' in c}")
print(f"Ruta Original text: {'Ruta Original' in c}")
print(f"Ruta Alternativa text: {'Ruta Alternativa' in c}")
print(f"Password at bottom: {c.find('passwordGate') > len(c) * 0.6}")
print(f"Budget at bottom: {c.find('PRESUPUESTO') > len(c) * 0.6}")
print(f"Hero below: {c.find('hero-cover') > c.find('13')}")
print(f"PRESUPUESTO count: {c.count('PRESUPUESTO')}")
print(f"budget-wrap count: {c.count('budget-wrap')}")