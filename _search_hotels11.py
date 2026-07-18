import sys, re

raw = sys.stdin.read()

# Find ds:0 data
start = raw.find('"ds:0"')
if start < 0:
    start = raw.find('AtySUc')
    
# Find the large data array
# Look for the pattern: hotels with their data
# Hotels appear as: null,"Hotel Name",[[lat,lon],...]
hotels = re.findall(r'null,\s*"([^"]+(?:Hotel|Inn|Hostel|Suites|Apartment|Residence)[^"]*?)"\s*,\s*\[\[([\d.,\-]+)\]', raw)

# Also look for prices near hotels
# Find CHF prices with context
price_blocks = re.findall(r'CHF\s*(\d+)[^"]{0,200}?(?:"([^"]{10,60})")?', raw)

for name, coords in hotels:
    print(f"Hotel: {name}")
    print(f"  Coords: [{coords}]")
    
    # Find position in raw HTML
    pos = raw.find(f'null,"{name}"')
    if pos > 0:
        chunk = raw[pos:pos+3000]
        # Find prices
        prices = re.findall(r'CHF\s*(\d+)', chunk)
        if prices:
            print(f"  Prices: {', '.join(sorted(set(prices), key=int))}")
        # Find rating
        rating = re.search(r'(\d[,.]\d)\s*[☆★]', chunk)
        if rating:
            print(f"  Rating: {rating.group(1)}")
        # Find phone
        phone = re.search(r'tel:(\d+)', chunk)
        if phone:
            print(f"  Tel: {phone.group(1)}")
        # Find distance
        dist = re.search(r'(\d+\.?\d*)\s*km\s+from', chunk)
        if dist:
            print(f"  Distance from center: {dist.group(1)} km")
    print()