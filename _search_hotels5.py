import sys, re, json

raw = sys.stdin.read()

# Find the AF_initDataCallback data chunks
# Google Travel embeds hotel data in JS callbacks
callbacks = re.findall(r"AF_initDataCallback\s*\(\s*({.*?})\s*\)\s*;", raw, re.DOTALL)

for cb in callbacks[:5]:
    try:
        data = json.loads(cb)
        key = data.get('key', 'unknown')
        print(f"=== Data chunk: {key} ===")
        # Print the structure
        if 'data' in data:
            d = json.dumps(data['data'], indent=2)[:2000]
            print(d)
        print()
    except:
        pass