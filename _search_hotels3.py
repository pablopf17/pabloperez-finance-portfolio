import sys, re

html = sys.stdin.read()

# Remove all tags to get text
text = re.sub(r'<[^>]+>', '\n', html)
lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2]

# Look for lines that look like hotel names (capitalized words, 2-6 words)
hotel_pattern = re.compile(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*(?:Hotel|Inn|Hostel|Motel|Resort|Lodge|House|Apartments?|Suites?|Villa)')
seen = set()
for l in lines:
    if hotel_pattern.search(l) and l not in seen:
        seen.add(l)
        print(l)

print("=== CLEAN TEXT ===")
for l in lines[:100]:
    print(l)