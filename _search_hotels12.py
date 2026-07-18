import sys, re

raw = sys.stdin.read()

# Find the main data array
data_start = raw.find('"ds:0"')
if data_start < 0:
    data_start = raw.find('AtySUc')

# Find the big array
# Search for price patterns near hotel names
hotel_names = [
    "Bad Bubendorf",
    "Zur krummen Eich",
    "Hotel Baslertor",
    "Seilers Hotel",
    "easyHotel",
    "Hotel Alfa",
    "Radisson",
    "Courtyard",
    "Bienenberg",
    "Gasthof zum Ochsen",
    "Bad Schauenburg",
    "Schiff am Rhein"
]

for name in hotel_names:
    pos = raw.find(name)
    if pos > 0:
        # Get context around this hotel
        chunk = raw[max(0,pos-100):pos+2000]
        # Find prices
        prices = re.findall(r'CHF\s*(\d+)', chunk)
        # Find ratings
        ratings = re.findall(r'(\d[,.]\d)\s*[☆★☆★]', chunk)
        # Find reviews count
        reviews = re.findall(r'(\d+)\s+reviews?', chunk, re.IGNORECASE)
        
        print(f"--- {name} ---")
        if prices:
            print(f"  Prices: {', '.join(sorted(set(prices), key=int))}")
        if ratings:
            print(f"  Rating: {ratings[0]}")
        if reviews:
            print(f"  Reviews: {reviews[0]}")
        
        # Also try to find distance
        # Find numbers near "km" 
        dists = re.findall(r'(\d+\.?\d*)\s*km', chunk)
        if dists:
            valid_dists = [d for d in dists if float(d) < 20]
            if valid_dists:
                print(f"  Distance: {valid_dists[0]} km")
        print()