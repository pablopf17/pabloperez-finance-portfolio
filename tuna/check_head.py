import subprocess

r = subprocess.run(['git', 'show', 'HEAD:tuna/index.html'], capture_output=True, text=True, cwd='C:/Users/pablo/pabloperez-finance-portfolio-live')
c = r.stdout
print(f'HEAD version: {len(c)} bytes')
print(f'Has cover.jpg: {"cover.jpg" in c}')
print(f'Has hero-cover: {"hero-cover" in c}')
print(f'Has RUTA ORIGINAL: {"RUTA ORIGINAL" in c}')
print(f'Has RUTA ALTERNATIVA: {"RUTA ALTERNATIVA" in c}')
print(f'Has content-f: {"content-f" in c}')
print(f'Has content-r: {"content-r" in c}')
print(f'Has route-tabs: {"route-tabs" in c}')
print(f'Has passwordGate: {"passwordGate" in c}')
print(f'Has PRESUPUESTO: {"PRESUPUESTO" in c}')