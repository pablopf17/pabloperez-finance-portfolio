import subprocess

# Read the original file via git
result = subprocess.run(
    ['git', 'show', 'HEAD:tuna/index.html'],
    capture_output=True, text=True,
    cwd='C:/Users/pablo/pabloperez-finance-portfolio-live'
)
original = result.stdout

content = original

# 1. Move hero cover below the subtitle
content = content.replace(
    '<div class="back"><a href="/">\u2190 fraile.ch</a></div>\n\n    <div class="hero-cover">\n      <img src="cover.jpg" alt="Tuna Suiza 2026 \u2014 foto de grupo" />\n    </div>\n\n    <p class="eyebrow">Tuna \u00b7 Julio 2026</p>',
    '<div class="back"><a href="/">\u2190 fraile.ch</a></div>\n\n    <p class="eyebrow">Tuna \u00b7 Julio 2026</p>'
)

content = content.replace(
    '<p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>',
    '<p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>\n\n    <div class="hero-cover">\n      <img src="cover.jpg" alt="Tuna Suiza 2026 \u2014 foto de grupo" />\n    </div>'
)

# 2. Remove route comparison line
content = content.replace(
    '<p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>\n  <p style="font-size:12px;color:var(--warm-grey);margin-top:-28px;margin-bottom:36px;">\U0001f680 Ruta Original \u00b7 <strong>\u2195</strong> \u00b7 \U0001f504 Ruta Alternativa \u00b7 <strong>\u2195</strong> \u00b7 \U0001f195 Ruta Real (v\u00eda Aosta/Chamonix)</p>',
    '<p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>'
)

# 3. Remove route tabs and radio inputs
content = content.replace(
    '    <input type="radio" name="route" id="route-f" checked>\n    <input type="radio" name="route" id="route-r">\n    <input type="radio" name="route" id="route-r2">\n    <div class="route-tabs">\n      <label for="route-f">\U0001f680 Ruta Original</label>\n      <label for="route-r">\U0001f504 Ruta Alternativa</label>\n      <label for="route-r2">\U0001f195 Ruta Real</label>\n    </div>\n\n    <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 RUTA ORIGINAL',
    '    <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 RUTA REAL'
)

# 4. Remove Ruta Original section (content-f)
cf_start = content.find('<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 RUTA ORIGINAL')
cf_end = content.find('</div><!-- /content-f -->', cf_start) + len('</div><!-- /content-f -->')
if cf_start > 0 and cf_end > 0:
    content = content[:cf_start] + content[cf_end:]

# 5. Remove Ruta Alternativa section (content-r)
alt_start = content.find('<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 RUTA ALTERNATIVA')
alt_end = content.find('</div><!-- /content-r -->', alt_start) + len('</div><!-- /content-r -->')
if alt_start > 0 and alt_end > 0:
    content = content[:alt_start] + content[alt_end:]

# 6. Remove route-wrap wrapper
content = content.replace('<div class="route-wrap">', '')
content = content.replace('</div><!-- /route-wrap -->', '')

# 7. Remove route-content wrappers
content = content.replace('<div class="route-content" id="content-r2">', '')
content = content.replace('</div><!-- /content-r2 -->', '')

# 8. Remove route-tabs CSS
route_tabs_css = '    .route-tabs { display: flex; gap: 0; margin-bottom: 24px; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }\n    .route-wrap input[type="radio"] { display: none; }\n    .route-tabs label {\n      flex: 1; padding: 14px 18px; cursor: pointer; text-align: center;\n      font-size: 12px; font-weight: 500; letter-spacing: 0.06em;\n      text-transform: uppercase; color: var(--warm-grey);\n      background: rgba(255,255,255,0.3);\n      transition: all 0.25s; user-select: none;\n      border-right: 1px solid var(--border);\n    }\n    .route-tabs label:last-child { border-right: none; }\n    #route-f:checked ~ .route-tabs label[for="route-f"],\n        #route-r:checked ~ .route-tabs label[for="route-r"],\n        #route-r2:checked ~ .route-tabs label[for="route-r2"] { background: var(--accent); color: #fff; }\n        .route-wrap .route-content { display: none; }\n        #route-f:checked ~ #content-f,\n        #route-r:checked ~ #content-r,\n        #route-r2:checked ~ #content-r2 { display: block; }'
content = content.replace(route_tabs_css, '')

# 9. Milan collapsed in Ruta Real
milan_open = content.find('<details class="city-card" open>')
milan_closed_tag = '<details class="city-card">'
if milan_open > 0:
    content = content[:milan_open] + milan_closed_tag + content[milan_open + len('<details class="city-card" open>'):]

# 10. Move password gate + links to bottom
pw_start = content.find('<div class="password-gate" id="passwordGate">')
links_end = content.find('</section>', content.find('<!-- Links -->')) + len('</section>')
pw_section = content[pw_start:links_end]
content = content[:pw_start] + content[links_end:]

# 11. Move budget to bottom
budget_start = content.find('<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 PRESUPUESTO')
budget_end = content.find('</div><!-- /budget-wrap -->', budget_start) + len('</div><!-- /budget-wrap -->')
budget_section = content[budget_start:budget_end]
content = content[:budget_start] + content[budget_end:]

# 12. Insert private content before script
script_start = content.find('<script>')
content = content[:script_start] + '\n' + pw_section + '\n\n' + budget_section + '\n' + content[script_start:]

# 13. Update Jue 16 to Estrasburgo-Stuttgart
content = content.replace('Ginebra \u00b7 Neuch\u00e2tel \u00b7 Basilea', 'Estrasburgo \u00b7 Stuttgart')
content = content.replace('\U0001f697 Ginebra \u2192 Neuch\u00e2tel', '\U0001f697 Ginebra \u2192 Estrasburgo')
content = content.replace('~1h 15min \u00b7 120 km</strong> \u2014 autopista A1', '~4h \u00b7 360 km</strong> \u2014 autopista A1/A35 (peaje ~25\u20ac)')
content = content.replace('\U0001f3b5 Neuch\u00e2tel (tarde)', '\U0001f3b5 Estrasburgo (tarde)')
content = content.replace('\U0001f697 Neuch\u00e2tel \u2192 Basilea', '\U0001f697 Estrasburgo \u2192 Stuttgart')
content = content.replace('~1h 30min \u00b7 140 km</strong> \u2014 autopista A5', '~2h \u00b7 160 km</strong> \u2014 autopista A5 (peaje DE ~15\u20ac)')
content = content.replace('\U0001f3b5 Basilea (noche)', '\U0001f3b5 Stuttgart (noche)')

# 14. Clean budget - remove Original and Alternative tables
content = content.replace('<!-- Forward -->', '')
content = content.replace('<!-- Reverse -->', '')
content = content.replace('grid-template-columns:1fr 1fr 1fr', 'grid-template-columns:1fr')

# Remove Forward budget table (from Forward to Real)
fwd = content.find('<!-- Forward -->')
real = content.find('<!-- Real -->')
if fwd > 0 and real > fwd:
    content = content[:fwd] + content[real:]

# 15. Update meta description
old_desc = 'Tres rutas: Original (Mil\u00e1n\u2192Suiza\u2192Stuttgart), Alternativa (Tur\u00edn\u2192Suiza) y Real'
new_desc = 'Ruta Real: Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Estrasburgo\u2192Stuttgart\u2192Z\u00farich\u2192Lugano\u2192Mil\u00e1n'
content = content.replace(old_desc, new_desc)

# 16. Remove subtitle margin
content = content.replace('.subtitle { margin-bottom: 40px; }', '.subtitle { margin-bottom: 0; }')

# Write the file
with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
checks = {
    'RUTA ALTERNATIVA': 'RUTA ALTERNATIVA' in content,
    'RUTA ORIGINAL (content)': 'RUTA ORIGINAL' in content,
    'content-r': 'content-r' in content,
    'content-f': 'content-f' in content,
    'route-tabs': 'route-tabs' in content,
    'route-wrap': 'route-wrap' in content,
    'Estrasburgo': 'Estrasburgo' in content,
    'Ginebra · Neuchâtel': 'Ginebra · Neuchâtel' in content,
    'Ruta Original budget': 'Ruta Original' in content,
    'Ruta Alternativa budget': 'Ruta Alternativa' in content,
    'Password gate at bottom': content.find('passwordGate') > len(content) * 0.5,
    'Budget at bottom': content.find('PRESUPUESTO') > len(content) * 0.5,
    'Milán collapsed': content.find('<details class="city-card">') > 0,
    'Milán NOT open': content.find('<details class="city-card" open>') == -1,
    'Hero below subtitle': content.find('hero-cover') > content.find('13\u201319 julio'),
}
for k, v in checks.items():
    status = 'PASS' if v else 'FAIL'
    print(f"  [{status}] {k}")

print(f"\nFile size: {len(content)} bytes")

# Count sections
print(f"PRESUPUESTO count: {content.count('PRESUPUESTO')}")
print(f"budget-wrap count: {content.count('budget-wrap')}")