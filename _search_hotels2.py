import sys, re, json

html = sys.stdin.read()

# Extract all text content between tags
texts = re.findall(r'>([^<]{3,100})<', html)
for t in texts:
    t = t.strip()
    if t and len(t) > 3:
        print(t)