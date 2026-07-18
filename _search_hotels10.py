import sys, re

raw = sys.stdin.read()

# Find the AF_initDataCallback for ds:0
# Try a broader pattern
match = re.search(r'AF_initDataCallback\s*\(\s*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*key\s*:\s*"ds:0"(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*data\s*:\s*(\[.*?)\}\s*\)\s*;', raw, re.DOTALL)

if match:
    data = match.group(1)
    print(f"Data length: {len(data)}")
    # Print first 2000 chars
    print(data[:2000])
else:
    # Try an even broader pattern
    print("Trying broader pattern...")
    # Just find everything between the key and the closing of the callback
    pos = raw.find('"ds:0"')
    if pos > 0:
        # Find "data:" after this
        data_pos = raw.find('data:', pos)
        if data_pos > 0:
            snippet = raw[data_pos:data_pos+5000]
            print(snippet[:2000])
    else:
        print("No ds:0 found")