# Read
with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"Start: {len(c)} bytes")

# 1. Hero-cover below subtitle + remove comparison line
old = '<div class="back"><a href="/">\u2190 fraile.ch</a></div>\n\n    <div class="hero-cover">\n      <img src="cover.jpg" alt="Tuna Suiza 2026 \u2014 foto de grupo" />\n    </div>\n\n    <p class="eyebrow">Tuna \u00b7 Julio 2026</p>\n  <h1>Gira <em>Suiza</em></h1>\n  <p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>\n  <p style="font-size:12px;color:var(--warm-grey);margin-top:-28px;margin-bottom:36px;">\U0001f680 Ruta Original \u00b7 <strong>\u2195</strong> \u00b7 \U0001f504 Ruta Alternativa \u00b7 <strong>\u2195</strong> \u00b7 \U0001f195 Ruta Real (v\u00eda Aosta/Chamonix)</p>'
new = '<div class="back"><a href="/">\u2190 fraile.ch</a></div>\n\n    <p class="eyebrow">Tuna \u00b7 Julio 2026</p>\n  <h1>Gira <em>Suiza</em></h1>\n  <p class="subtitle">13\u201319 julio \u00b7 6 personas \u00b7 2 coches \u00b7 ~1.800 km</p>\n\n    <div class="hero-cover">\n      <img src="cover.jpg" alt="Tuna Suiza 2026 \u2014 foto de grupo" />\n    </div>'
c = c.replace(old, new)
print(f"1. {len(c)}")

# 2. Remove radio + tabs + content-f
start = c.find('<input type="radio" name="route" id="route-f"')
end_marker = '</div><!-- /content-f -->'
end = c.find(end_marker, start)
if end > 0:
    end += len(end_marker)
    c = c[:start] + c[end:]
    print(f"2. {len(c)}")
else:
    print(f"2. ERROR: end_marker not found! start={start}")

# 3. Remove content-r  
start = c.find('<!-- \u2550\u2550\u2550 RUTA ALTERNATIVA')
end_marker = '</div><!-- /content-r -->'
end = c.find(end_marker, start)
if end > 0:
    end += len(end_marker)
    c = c[:start] + c[end:]
    print(f"3. {len(c)}")
else:
    print(f"3. ERROR: end_marker not found! start={start}")

# 4. Remove wrappers
c = c.replace('<div class="route-wrap">\n        ', '')
c = c.replace('\n        </div><!-- /route-wrap -->', '')
c = c.replace('<div class="route-content" id="content-r2">\n\n                ', '')
c = c.replace('\n        </div><!-- /content-r2 -->', '')
print(f"4. {len(c)}")

# 5. Remove route-tabs CSS
old_css = '\n    .route-tabs { display: flex; gap: 0; margin-bottom: 24px; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }\n    .route-wrap input[type="radio"] { display: none; }\n    .route-tabs label {\n      flex: 1; padding: 14px 18px; cursor: pointer; text-align: center;\n      font-size: 12px; font-weight: 500; letter-spacing: 0.06em;\n      text-transform: uppercase; color: var(--warm-grey);\n      background: rgba(255,255,255,0.3);\n      transition: all 0.25s; user-select: none;\n      border-right: 1px solid var(--border);\n    }\n    .route-tabs label:last-child { border-right: none; }\n    #route-f:checked ~ .route-tabs label[for="route-f"],\n        #route-r:checked ~ .route-tabs label[for="route-r"],\n        #route-r2:checked ~ .route-tabs label[for="route-r2"] { background: var(--accent); color: #fff; }\n        .route-wrap .route-content { display: none; }\n        #route-f:checked ~ #content-f,\n        #route-r:checked ~ #content-r,\n        #route-r2:checked ~ #content-r2 { display: block; }'
c = c.replace(old_css, '')
print(f"5. {len(c)}")

# 6. Milan collapsed
idx = c.find('<!-- \u2550\u2550\u2550 MIL\u00c1N')
open_tag = '<details class="city-card" open>'
open_idx = c.find(open_tag, idx)
c = c[:open_idx] + '<details class="city-card">' + c[open_idx + len(open_tag):]
print(f"6. {len(c)}")

# 7. Friburgo-Stuttgart
c = c.replace('Ginebra \u00b7 Neuch\u00e2tel \u00b7 Basilea', 'Friburgo \u00b7 Stuttgart')
print(f"7. {len(c)}")

# 8. Move password + links + budget to bottom
pw_start = c.find('<div class="password-gate" id="passwordGate">')
links_end = c.find('</section>', c.find('<!-- Links -->')) + len('</section>')
pw_section = c[pw_start:links_end]
c = c[:pw_start] + c[links_end:]

budget_start = c.find('<!-- \u2550\u2550\u2550 PRESUPUESTO')
budget_end = c.find('</div><!-- /budget-wrap -->', budget_start) + len('</div><!-- /budget-wrap -->')
budget_section = c[budget_start:budget_end]
c = c[:budget_start] + c[budget_end:]

script_start = c.find('<script>')
c = c[:script_start] + '\n\n' + pw_section + '\n\n' + budget_section + '\n\n' + c[script_start:]
print(f"8. {len(c)}")

# 9. Clean budget
c = c.replace('<!-- Forward -->', '')
c = c.replace('<!-- Reverse -->', '')
c = c.replace('grid-template-columns:1fr 1fr 1fr', 'grid-template-columns:1fr')
fwd = c.find('<!-- Forward -->')
real = c.find('<!-- Real -->')
if fwd > 0 and real > fwd:
    c = c[:fwd] + c[real:]
print(f"9. {len(c)}")

# 10. Meta
old = 'Tres rutas: Original (Mil\u00e1n\u2192Suiza\u2192Stuttgart), Alternativa (Tur\u00edn\u2192Suiza) y Real (Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Basilea\u2192Stuttgart\u2192Lugano\u2192Mil\u00e1n). Parking, restaurantes espa\u00f1oles, presupuesto.'
new = 'Ruta Real: Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Friburgo\u2192Stuttgart\u2192Z\u00farich\u2192Lugano\u2192Mil\u00e1n. Parking, restaurantes espa\u00f1oles, presupuesto.'
c = c.replace(old, new)

# 11. Subtitle margin
c = c.replace('.subtitle { margin-bottom: 40px; }', '.subtitle { margin-bottom: 0; }')

# Write
with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

# Verify
print(f"\nFinal: {len(c)} bytes")
for check, msg in [
    ('RUTA ALTERNATIVA', 'Has ALTERNATIVA'),
    ('RUTA ORIGINAL', 'Has ORIGINAL'),
    ('route-tabs', 'Has route-tabs'),
    ('route-wrap', 'Has route-wrap'),
    ('content-f', 'Has content-f'),
    ('content-r', 'Has content-r'),
    ('Friburgo', 'Has Friburgo'),
    ('Ginebra \u00b7 Neuch', 'Has Ginebra-Neuch'),
]:
    val = check in c
    print(f"  {msg}: {val}")

pw_pos = c.find('passwordGate')
budget_pos = c.find('PRESUPUESTO')
print(f"  PW at bottom: {pw_pos > len(c) * 0.6}")
print(f"  Budget at bottom: {budget_pos > len(c) * 0.6}")
milan_open_tag = '<details class="city-card" open>'
print("  Milan open: " + str(milan_open_tag in c))
print(f"  Hero below: {c.find('hero-cover') > c.find('13')}")