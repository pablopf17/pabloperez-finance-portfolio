import sys, re, json

raw = sys.stdin.read()

# Find the main data chunk (ds:0) - look for the AF_initDataCallback
# Extract the data array
match = re.search(r'AF_initDataCallback\s*\(\s*\{[^}]*key\s*:\s*"ds:0"[^}]*data\s*:\s*(\[.*?)\}\s*\)\s*;', raw, re.DOTALL)

if match:
    data_str = match.group(1)
    # Find hotel names and their associated prices
    # Hotels appear like: null,"Hotel Name",[[lat,lon],...]
    hotel_blocks = re.findall(r'null,\s*"([^"]*(?:Hotel|Inn|Hostel|Suites|Apartment|Residence)[^"]*)"\s*,\s*\[\[([\d.,\-]+)', data_str)
    
    for name, coords in hotel_blocks:
        print(f"Hotel: {name}")
        print(f"  Coords: {coords}")
        
        # Look for price near this hotel block
        # Find the hotel position in the string
        pos = data_str.find(f'null,"{name}"')
        if pos > 0:
            chunk = data_str[pos:pos+5000]
            # Find "CHF" prices near this hotel
            prices = re.findall(r'CHF\s*(\d+)', chunk)
            if prices:
                print(f"  Prices: {', '.join(sorted(set(prices), key=int))}")
            # Find ratings
            ratings = re.findall(r'(\d\.\d)\s*stars?', chunk, re.IGNORECASE)
            if ratings:
                print(f"  Rating: {ratings[0]}")
            # Find distance
            dist = re.findall(r'(\d+\.?\d*)\s*km', chunk)
            if dist:
                print(f"  Distance: {dist[0]} km")
        
        print()
        print("---")
else:
    print("No match found")
    # Try alternative pattern
    match2 = re.search(r'"ds:0"[^}]*data\s*:\s*(\[.*)', raw, re.DOTALL)
    if match2:
        print(f"Found alt match, {len(match2.group(1))} chars")
    else:
        print("No alt match either")