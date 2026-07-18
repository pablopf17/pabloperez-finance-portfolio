import sys, re, json

raw = sys.stdin.read()

# Find all AF_initDataCallback calls
pattern = r'AF_initDataCallback\s*\(\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}\s*\)\s*;'
matches = re.findall(pattern, raw, re.DOTALL)

for i, m in enumerate(matches[:5]):
    try:
        # Try to find the key
        key_match = re.search(r'key\s*:\s*["\']([^"\']+)["\']', m)
        key = key_match.group(1) if key_match else f"chunk_{i}"
        
        # Try to find data
        data_match = re.search(r'data\s*:\s*(\[.*)', m, re.DOTALL)
        if data_match:
            data_str = data_match.group(1)
            # Remove trailing comma/brace
            data_str = re.sub(r',\s*\}\s*$', '}', data_str)
            print(f"=== {key} ({len(data_str)} chars) ===")
            print(data_str[:1000])
            print()
    except Exception as e:
        print(f"Error: {e}")