with open('C:/Users/pablo/pabloperez-finance-portfolio-live/tuna/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
print(f"File size: {len(c)}")

for m in re.finditer('RUTA ALTERNATIVA', c):
    print(f'RUTA ALTERNATIVA at {m.start()}: {c[m.start()-10:m.start()+30]}')

for m in re.finditer('/content-r -->', c):
    print(f'/content-r at {m.start()}: {c[m.start()-30:m.start()+20]}')

for m in re.finditer('RUTA REAL', c):
    print(f'RUTA REAL at {m.start()}: {c[m.start()-10:m.start()+30]}')