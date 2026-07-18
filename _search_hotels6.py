import sys, re, json

html = sys.stdin.read()

# Find all large text blocks that may contain hotel data
# Look for patterns around CHF prices
segments = re.split(r'(?<=\.)\s+(?=[A-Z])', html)
hotel_data = []
for s in segments:
    if 'CHF' in s and len(s) < 500:
        clean = re.sub(r'<[^>]+>', '', s).strip()
        if clean and 'hotel' in clean.lower() or 'CHF' in clean:
            hotel_data.append(clean)

for h in hotel_data[:30]:
    print(h)
    print('---')