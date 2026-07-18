import sys, re, html as html_mod

raw = sys.stdin.read()

# Decode HTML entities
decoded = html_mod.unescape(raw)

# Find data points that look like hotel cards
# Look for patterns like: hotel name followed by price
text = re.sub(r'<script[^>]*>.*?</script>', '', decoded, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', text)
lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2]

seen = set()
for l in lines:
    # Filter for likely hotel-related content
    if any(kw in l.lower() for kw in ['hotel', 'chf', 'pratteln', 'muttenz', 'basel', 'stars', 'review', 'inn', 'hostel', 'apartment']):
        if l not in seen:
            seen.add(l)
            print(l)
