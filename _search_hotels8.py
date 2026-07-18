import sys, re, json

raw = sys.stdin.read()

# Find the main data chunk (ds:0)
# Look for hotel names in the data
hotel_pattern = re.compile(r'null,\s*"([^"]*(?:Hotel|Inn|Hostel|Suites|Apartments?|Residence)[^"]*)"', re.DOTALL)
hotels = hotel_pattern.findall(raw)
for h in sorted(set(hotels)):
    print(f"HOTEL: {h}")

print("\n=== PRICES ===")
# Look for price data
price_pattern = re.compile(r'CHF\s*(\d+)')
prices = price_pattern.findall(raw)
for p in sorted(set(prices), key=int):
    print(f"CHF {p}")

print("\n=== DETAILS ===")
# Find phone numbers
phones = re.findall(r'tel:(\d+)', raw)
for p in sorted(set(phones)):
    print(f"Tel: {p}")

# Find addresses
addrs = re.findall(r'"(?:[A-Z][a-z]+strasse|Via|Rue|Place)\s[^"]{5,60}"', raw)
for a in sorted(set(addrs))[:20]:
    print(f"Addr: {a}")