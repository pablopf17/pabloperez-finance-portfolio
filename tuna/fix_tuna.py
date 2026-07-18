with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# === POSITIONS ===
head_end = content.find('</head>') + len('</head>')

# Password gate (to move to bottom)
pw_start = content.find('<div class="password-gate" id="passwordGate">')
links_end = content.find('</section>', content.find('<!-- Links -->')) + len('</section>')

# Route wrap
route_wrap_start = content.find('<div class="route-wrap">')
route_wrap_end = content.find('</div><!-- /route-wrap -->') + len('</div><!-- /route-wrap -->')

# Content-r2 (what we keep)
r2_div_start = content.find('<div class="route-content" id="content-r2">')
r2_div_end = content.find('</div><!-- /content-r2 -->') + len('</div><!-- /content-r2 -->')

# Budget
budget_start = content.find('<!-- PRESUPUESTO')
budget_end = content.find('</div><!-- /budget-wrap -->', budget_start) + len('</div><!-- /budget-wrap -->')

# Script and closing
script_start = content.find('<script>')
close_html = content.find('</html>', script_start) + len('</html>')
script_and_close = content[script_start:close_html]

# === BUILD ===

# Part 1: Everything before password gate
before_pw = content[:pw_start]

# Part 2: Extract r2 inner content
inner_start = r2_div_start + len('<div class="route-content" id="content-r2">')
inner_end = r2_div_end - len('</div><!-- /content-r2 -->')
r2_inner = content[inner_start:inner_end].strip()

# Update Jue 16 - Ginebra/Neuchatel/Basilea -> Estrasburgo/Stuttgart
r2_inner = r2_inner.replace(
    '<span class="city-name">Ginebra \u00b7 Neuch\u00e2tel \u00b7 Basilea</span>',
    '<span class="city-name">Estrasburgo \u00b7 Stuttgart</span>'
)
r2_inner = r2_inner.replace(
    '<h3>\U0001f697 Ginebra \u2192 Neuch\u00e2tel</h3>',
    '<h3>\U0001f697 Ginebra \u2192 Estrasburgo</h3>'
)
r2_inner = r2_inner.replace(
    '~1h 15min \u00b7 120 km',
    '~4h \u00b7 360 km'
)
r2_inner = r2_inner.replace(
    'autopista A1',
    'autopista A1/A35 (peaje ~25\u20ac)'
)
r2_inner = r2_inner.replace(
    '\U0001f3b5 Neuch\u00e2tel (tarde)',
    '\U0001f3b5 Estrasburgo (tarde)'
)
r2_inner = r2_inner.replace(
    'Place Pury',
    'Catedral de Estrasburgo'
)
r2_inner = r2_inner.replace(
    'Paseo del Lago (Promenade du Lac)',
    'Petite France'
)
r2_inner = r2_inner.replace(
    'Rue du Nord / Rue du Ch\u00e2teau',
    'Place de la Catedral / Rue des Fr\u00e8res'
)
r2_inner = r2_inner.replace(
    '<h3>\U0001f697 Neuch\u00e2tel \u2192 Basilea</h3>',
    '<h3>\U0001f697 Estrasburgo \u2192 Stuttgart</h3>'
)
r2_inner = r2_inner.replace(
    '~1h 30min \u00b7 140 km',
    '~2h \u00b7 160 km'
)
r2_inner = r2_inner.replace(
    'autopista A5',
    'autopista A5 (peaje DE ~15\u20ac)'
)
r2_inner = r2_inner.replace(
    'Basilea (noche)',
    'Stuttgart (noche)'
)
r2_inner = r2_inner.replace(
    'Barf\u00fcsserplatz',
    'Schlossplatz'
)
r2_inner = r2_inner.replace(
    'Marktplatz',
    'K\u00f6nigstra\u00dfe'
)
r2_inner = r2_inner.replace(
    'Rheinufer (paseo del Rin)',
    'Stuttgart centro'
)
r2_inner = r2_inner.replace(
    '<h3>\U0001f6cf\ufe0f Parking Basilea</h3>',
    '<h3>\U0001f6cf\ufe0f Parking Stuttgart</h3>'
)
r2_inner = r2_inner.replace(
    'Parkgarage Elisabethen',
    'Parkhaus Schlossplatz'
)
r2_inner = r2_inner.replace(
    'Elisabethenanlage 13',
    'Schlossplatz 1'
)
r2_inner = r2_inner.replace(
    '<h3>\U0001f6cd\ufe0f Hostel / Airbnb Basilea</h3>',
    '<h3>\U0001f6cd\ufe0f A&O Stuttgart City</h3>'
)
r2_inner = r2_inner.replace(
    '~250-350 CHF total (~42-58 CHF/pers)',
    'Rosensteinstra\u00dfe 14-16 \u00b7 ~120-160 \u20ac total (~20-27 \u20ac/pers)'
)
r2_inner = r2_inner.replace(
    '~3 CHF/h',
    '\u20ac2.50/h \u00b7 \u20ac15/d\u00eda'
)
r2_inner = r2_inner.replace(
    'gratis despu\u00e9s 19:30',
    ''
)

# Part 3: Cities section
cities_section = f'  <!-- Ciudades -->\n  <section>\n    <h2>\U0001f3d9\ufe0f Ciudades</h2>\n{r2_inner}\n  </section>'

# Part 4: Private content at bottom
private_section = content[pw_start:links_end] + '\n\n' + content[budget_start:budget_end]

# Clean up budget: remove Original and Alternative tables, keep only Ruta Real
# Find the Forward and Reverse budget tables
fwd_marker = '<!-- Forward -->'
real_marker = '<!-- Real -->'
rev_marker = '<!-- Reverse -->'

if fwd_marker in private_section and real_marker in private_section:
    fwd_i = private_section.find(fwd_marker)
    real_i = private_section.find(real_marker)
    before_fwd = private_section[:fwd_i]
    after_real = private_section[real_i:]
    private_section = before_fwd + after_real

# Update grid to 1 column
private_section = private_section.replace(
    'grid-template-columns:1fr 1fr 1fr',
    'grid-template-columns:1fr'
)

# Update meta description
old_desc = 'Tuna Suiza 2026 — Tres rutas: Original (Milán→Suiza→Stuttgart), Alternativa (Turín→Suiza) y Real (Milán→Turín→Aosta/Chamonix→Ginebra→Basilea→Stuttgart→Lugano→Milán). Parking, restaurantes españoles, presupuesto.'
new_desc = 'Tuna Suiza 2026 — Ruta Real: Milán→Turín→Aosta/Chamonix→Ginebra→Estrasburgo→Stuttgart→Zúrich→Lugano→Milán. Parking, restaurantes españoles, presupuesto.'
before_pw = before_pw.replace(old_desc, new_desc)

# Fix subtitle margin
before_pw = before_pw.replace('.subtitle { margin-bottom: 40px; }', '.subtitle { margin-bottom: 0; }')

# Remove route-tabs CSS
before_pw = before_pw.replace('        #route-r2:checked ~ #content-r2 { display: block; }', '')
before_pw = before_pw.replace('input[type="radio"] { display: none; }', '')
before_pw = before_pw.replace('.route-tabs { display: flex;', '/* .route-tabs removed */')

# Remove the route-wrap CSS
# Find and remove the .route-tabs and .route-wrap related CSS
before_pw = before_pw.replace('''    .route-tabs { display: flex; gap: 0; margin-bottom: 24px; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
    .route-wrap input[type="radio"] { display: none; }
    .route-tabs label {
      flex: 1; padding: 14px 18px; cursor: pointer; text-align: center;
      font-size: 12px; font-weight: 500; letter-spacing: 0.06em;
      text-transform: uppercase; color: var(--warm-grey);
      background: rgba(255,255,255,0.3);
      transition: all 0.25s; user-select: none;
      border-right: 1px solid var(--border);
    }
    .route-tabs label:last-child { border-right: none; }
    #route-f:checked ~ .route-tabs label[for="route-f"],
        #route-r:checked ~ .route-tabs label[for="route-r"],
        #route-r2:checked ~ .route-tabs label[for="route-r2"] { background: var(--accent); color: #fff; }
        .route-wrap .route-content { display: none; }
        #route-f:checked ~ #content-f,
        #route-r:checked ~ #content-r,
        #route-r2:checked ~ #content-r2 { display: block; }''', '')

# Assemble final file
final = before_pw + '\n' + cities_section + '\n\n<!-- Contenido privado -->\n' + private_section + '\n\n' + script_and_close

with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'w', encoding='utf-8') as f:
    f.write(final)

# Verify
print(f"File written: {len(final)} bytes")
print(f"RUTA ALTERNATIVA: {'RUTA ALTERNATIVA' in final}")
print(f"content-r: {'content-r' in final}")
print(f"content-f: {'content-f' in final}")
print(f"route-tabs: {'route-tabs' in final}")
print(f"Ginebra · Neuchâtel · Basilea: {'Ginebra · Neuchâtel · Basilea' in final}")
print(f"Estrasburgo · Stuttgart: {'Estrasburgo · Stuttgart' in final}")
print(f"password-gate at top: {pw_start < 13000}")
print(f"route-wrap: {'route-wrap' in final}")
print(f"Ruta Original budget: {'Ruta Original' in final[budget_start:]}")
print(f"Ruta Alternativa budget: {'Ruta Alternativa' in final[budget_start:]}")