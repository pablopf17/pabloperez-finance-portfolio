import sys, re, json

html = sys.stdin.read()

# Extract hotel names from title attributes
titles = re.findall(r'title="([^"]+)"', html)
for t in sorted(set(titles))[:50]:
    print(t)

print("---")

# Look for price-like patterns
prices = re.findall(r'CHF\s*\d+', html)
for p in sorted(set(prices))[:20]:
    print(p)

print("---")

# Look for hotel names in aria-labels
labels = re.findall(r'aria-label="([^"]+)"', html)
for l in sorted(set(labels))[:30]:
    print(l)