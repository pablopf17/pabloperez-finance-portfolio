with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content)} bytes")

sections = [
    ('back', '← fraile.ch'),
    ('hero', 'hero-cover'),
    ('eyebrow', 'Tuna · Julio 2026'),
    ('h1', 'Gira <em>Suiza</em>'),
    ('subtitle', '13–19 julio'),
    ('cities', 'Ciudades'),
    ('password gate', 'passwordGate'),
    ('budget', 'budget-wrap'),
    ('script', '<script>'),
]
print("\nSection order:")
for name, marker in sections:
    idx = content.find(marker)
    print(f"  {idx:>7}: {name}")

# Verify order is correct
cities_idx = content.find('Ciudades')
pw_idx = content.find('passwordGate')
budget_idx = content.find('budget-wrap')
script_idx = content.find('<script>')

if pw_idx > cities_idx:
    print("\n✅ Password gate after cities")
else:
    print("\n❌ Password gate NOT after cities")
if budget_idx > cities_idx:
    print("✅ Budget after cities")
else:
    print("❌ Budget NOT after cities")
if pw_idx < script_idx and budget_idx < script_idx:
    print("✅ Private content before script")
else:
    print("❌ Private content NOT before script")

# Check Milan is collapsed
milan_collapsed = 'details class="city-card">' in content
milan_open = 'details class="city-card" open' in content
print(f"\nMilán collapsed: {milan_collapsed}")
print(f"Milán open: {milan_open}")

# Check Estrasburgo
estrasburgo = 'Estrasburgo' in content
print(f"Estrasburgo: {estrasburgo}")

# Check Ruta Original budget removed
orig_budget = 'Ruta Original' in content
print(f"Ruta Original (budget text): {orig_budget}")

# Check Ruta Alternativa removed
alt_removed = 'RUTA ALTERNATIVA' not in content
print(f"Ruta Alternativa removed: {alt_removed}")