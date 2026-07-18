with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content)} bytes")

# Check key elements
checks = ['<!DOCTYPE html>', '</head>', '<body>', '</body>', '</html>', '<script>', '</script>']
for c in checks:
    print(f"  {c}: {c in content}")

# Check section order
sections = [
    ('back link', '← fraile.ch'),
    ('hero cover', 'hero-cover'),
    ('eyebrow', 'Tuna · Julio 2026'),
    ('h1', 'Gira <em>Suiza</em>'),
    ('subtitle', '13–19 julio'),
    ('cities', 'Ciudades'),
    ('password HTML', 'passwordGate'),
    ('budget', 'PRESUPUESTO'),
    ('script', '<script>'),
]

print("\nSection positions:")
for name, marker in sections:
    idx = content.find(marker)
    print(f"  {idx:>7}: {name}")

# Check password gate is after cities
pw_idx = content.find('passwordGate')
cities_idx = content.find('Ciudades')
script_idx = content.find('<script>')
budget_idx = content.find('PRESUPUESTO')

if pw_idx > cities_idx and budget_idx > cities_idx:
    print("\n✅ Private content moved to bottom (after cities)")
else:
    print("\n❌ Private content NOT after cities")

if pw_idx < script_idx and budget_idx < script_idx:
    print("✅ Private content is before script")
else:
    print("❌ Private content NOT before script")

# Clean up remaining CSS
content = content.replace('''        #route-f:checked ~ #content-f,
        #route-r:checked ~ #content-r,
''', '')

# Remove the broken route-tabs CSS
old_css = '''    .route-tabs { display: flex; gap: 0; margin-bottom: 24px; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
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
        #route-r2:checked ~ #content-r2 { display: block; }'''

# Try to find and remove the remaining CSS
idx = content.find('/* .route-tabs removed */')
if idx > 0:
    # Find the start of this block
    start = content.rfind('    ', 0, idx)
    # Find the end of the block (next blank line or next CSS class)
    end = content.find('\n\n    html', idx)
    if end < 0:
        end = content.find('\n\nbody', idx)
    if end > 0:
        print(f"\nRemoving CSS block from {start} to {end}")
        content = content[:start] + content[end:]

# Also remove the route-wrap CSS that's left
route_wrap_css = content.find('.route-wrap ')
if route_wrap_css > 0:
    # Find the end of this line
    end = content.find('\n', route_wrap_css)
    print(f"Found .route-wrap CSS at {route_wrap_css}, removing line")
    content = content[:route_wrap_css] + content[end:]

# Remove remaining route-tabs label CSS
rt_idx = content.find('.route-tabs label')
if rt_idx > 0:
    end = content.find('\n    .city-card', rt_idx)
    if end > 0:
        content = content[:rt_idx] + content[end:]
        print(f"Removed route-tabs label CSS block")

# Remove stray route-wrap references
content = content.replace('route-wrap ', '')
content = content.replace('route-wrap\n', '\n')

with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Final file: {len(content)} bytes")
print(f"content-r: {'content-r' in content}")
print(f"content-f: {'content-f' in content}")
print(f"route-tabs: {'route-tabs' in content}")
print(f"route-wrap: {'route-wrap' in content}")