with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 3. Replace radio+tabs+RutaOriginal section with just Ruta Real header  
cf_start = c.find('    <input type="radio" name="route" id="route-f"')
cf_end = c.find('</div><!-- /content-f -->', cf_start) + len('</div><!-- /content-f -->')
c = c[:cf_start] + c[cf_end:]
print(f"3. Removed content-f: {len(c)}")

# 4. Remove Ruta Alternativa section
alt_start = c.find('    <!-- \u2550\u2550\u2550 RUTA ALTERNATIVA')
alt_end = c.find('</div><!-- /content-r -->', alt_start) + len('</div><!-- /content-r -->')
c = c[:alt_start] + c[alt_end:]
print(f"4. Removed content-r: {len(c)}")

# 5. Remove route-wrap wrapper
c = c.replace('<div class="route-wrap">', '').replace('</div><!-- /route-wrap -->', '')
print(f"5. Removed route-wrap: {len(c)}")

# 6. Remove route-content wrapper
c = c.replace('<div class="route-content" id="content-r2">', '').replace('</div><!-- /content-r2 -->', '')
print(f"6. Removed route-content: {len(c)}")

# 7. Remove route-tabs CSS
old_css = '\n    .route-tabs { display: flex; gap: 0; margin-bottom: 24px; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }\n    .route-wrap input[type="radio"] { display: none; }\n    .route-tabs label {\n      flex: 1; padding: 14px 18px; cursor: pointer; text-align: center;\n      font-size: 12px; font-weight: 500; letter-spacing: 0.06em;\n      text-transform: uppercase; color: var(--warm-grey);\n      background: rgba(255,255,255,0.3);\n      transition: all 0.25s; user-select: none;\n      border-right: 1px solid var(--border);\n    }\n    .route-tabs label:last-child { border-right: none; }\n    #route-f:checked ~ .route-tabs label[for="route-f"],\n        #route-r:checked ~ .route-tabs label[for="route-r"],\n        #route-r2:checked ~ .route-tabs label[for="route-r2"] { background: var(--accent); color: #fff; }\n        .route-wrap .route-content { display: none; }\n        #route-f:checked ~ #content-f,\n        #route-r:checked ~ #content-r,\n        #route-r2:checked ~ #content-r2 { display: block; }'
c = c.replace(old_css, '')
print(f"7. Removed CSS: {len(c)}")

# 8. Milan collapsed (the first details in the remaining content)
idx = c.find('details class="city-card" open>')
if idx > 0:
    c = c[:idx] + 'details class="city-card">' + c[idx + len('details class="city-card" open>'):]
print(f"8. Milan collapsed: {len(c)}")

# 9. Update Jue 16 - Estrasburgo
c = c.replace('Ginebra \u00b7 Neuch\u00e2tel \u00b7 Basilea', 'Estrasburgo \u00b7 Stuttgart')
print(f"9. Estrasburgo: {len(c)}")

# 10. Move private content to bottom
pw_start = c.find('<div class="password-gate" id="passwordGate">')
links_end = c.find('</section>', c.find('<!-- Links -->')) + len('</section>')
pw_section = c[pw_start:links_end]
c = c[:pw_start] + c[links_end:]

budget_start = c.find('<!-- \u2550\u2550\u2550 PRESUPUESTO')
budget_end = c.find('</div><!-- /budget-wrap -->', budget_start) + len('</div><!-- /budget-wrap -->')
budget_section = c[budget_start:budget_end]
c = c[:budget_start] + c[budget_end:]

script_start = c.find('<script>')
c = c[:script_start] + '\n' + pw_section + '\n\n' + budget_section + '\n' + c[script_start:]
print(f"10. Moved private: {len(c)}")

# 11. Clean budget  
c = c.replace('<!-- Forward -->', '').replace('<!-- Reverse -->', '')
c = c.replace('grid-template-columns:1fr 1fr 1fr', 'grid-template-columns:1fr')
fwd = c.find('<!-- Forward -->')
real = c.find('<!-- Real -->')
if fwd > 0 and real > fwd:
    c = c[:fwd] + c[real:]
print(f"11. Cleaned budget: {len(c)}")

# 12. Update meta
old = 'Tres rutas: Original (Mil\u00e1n\u2192Suiza\u2192Stuttgart), Alternativa (Tur\u00edn\u2192Suiza) y Real (Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Basilea\u2192Stuttgart\u2192Lugano\u2192Mil\u00e1n). Parking, restaurantes espa\u00f1oles, presupuesto.'
new = 'Ruta Real: Mil\u00e1n\u2192Tur\u00edn\u2192Aosta/Chamonix\u2192Ginebra\u2192Estrasburgo\u2192Stuttgart\u2192Z\u00farich\u2192Lugano\u2192Mil\u00e1n. Parking, restaurantes espa\u00f1oles, presupuesto.'
c = c.replace(old, new)

# 13. Subtitle margin
c = c.replace('.subtitle { margin-bottom: 40px; }', '.subtitle { margin-bottom: 0; }')

# Write
with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\nDONE: {len(c)} bytes")
print(f"RUTA ALTERNATIVA: {'RUTA ALTERNATIVA' in c}")
print(f"RUTA ORIGINAL: {'RUTA ORIGINAL' in c}")
print(f"route-tabs: {'route-tabs' in c}")
print(f"route-wrap: {'route-wrap' in c}")
print(f"Estrasburgo: {'Estrasburgo' in c}")
print(f"PW in top half: {c.find('passwordGate') < len(c) * 0.5}")
print(f"Budget in top half: {c.find('PRESUPUESTO') < len(c) * 0.5}")
