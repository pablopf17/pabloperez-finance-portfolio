import json, re, shutil, os

HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, 'index.html')
BACKUP_PATH = os.path.join(HERE, 'index.html.bak2')

# ── 1. READ ──
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract template
match = re.search(r'<script type="__bundler/template">\n(.*)\n  <\/script>', content, re.DOTALL)
if not match:
    print("ERROR: Could not find __bundler/template")
    exit(1)

raw_escaped = match.group(1)
template_str = json.loads(raw_escaped)

# ── 2. Find the issue ──
# The problem is that re-escaping introduces literal </script> which HTML parser 
# treats as closing the script tag. We need to ensure the escaped version uses
# <\\u002Fscript> for any </script> in the template content.

# Count problematic patterns in template_str
count_problematic = template_str.count('</script>')
print(f"Found {count_problematic} literal </script> in template")

# Replace </script> with <\\u002Fscript> in the template content
original_len = len(template_str)
template_str = template_str.replace('</script>', '<\\u002Fscript>')
print(f"Replaced, length: {len(template_str)} (was {original_len})")

# ── 3. Re-escape ──
# json.dumps will properly escape everything, but we need to verify no </script> survives
escaped = json.dumps(template_str)

# Verify no raw </script> in the escaped output
if '</script>' in escaped:
    print("ERROR: </script> still present in escaped output!")
    # Additional fix - make sure all occurrences use unicode escape
    escaped = escaped.replace('</script>', '<\\u002Fscript>')

# ── 4. Build new script tag ──
new_script = '<script type="__bundler/template">\n' + escaped + '\n  </script>'

# ── 5. Replace ──
old_script_match = re.search(r'<script type="__bundler/template">\n.*?\n  <\/script>', content, re.DOTALL)
if not old_script_match:
    print("ERROR: Could not match old script tag")
    exit(1)

new_content = content[:old_script_match.start()] + new_script + content[old_script_match.end():]

# ── 6. Verify ──
# Test that the new template parses correctly
new_match = re.search(r'<script type="__bundler/template">\n(.*)\n  <\/script>', new_content, re.DOTALL)
new_raw = new_match.group(1)
try:
    json.loads(new_raw)
    print("✅ New JSON parses correctly")
except json.JSONDecodeError as e:
    print(f"❌ JSON error in new content: {e}")
    exit(1)

# Test that there are no literal </script> in the raw script content (would break HTML parser)
if '</script>' in new_raw and '<\\u002Fscript>' not in new_raw:
    # It might be the one at the very end (the actual closing tag)
    # Count occurrences
    count = new_raw.count('</script>')
    print(f"⚠️  {count} literal </script> in raw script content (may break HTML parser)")
    
    # Check each occurrence
    for i, m in enumerate(re.finditer('</script>', new_raw)):
        ctx = new_raw[max(0,m.start()-10):m.end()+10]
        print(f"  Occurrence {i} at {m.start()}: ...{repr(ctx)}...")
else:
    print("✅ No literal </script> in raw script content")

# Check file sizes
print(f"Original size: {len(content)}")
print(f"New size: {len(new_content)}")
ratio = len(new_content) / len(content)
print(f"Size ratio: {ratio:.3f}")

if ratio < 0.8 or ratio > 1.2:
    print("⚠️  Suspicious size change, writing backup but not overwriting")
    shutil.copy2(HTML_PATH, BACKUP_PATH)
    print(f"Backup at {BACKUP_PATH}")
    exit(1)

# ── 7. Write ──
shutil.copy2(HTML_PATH, BACKUP_PATH)
print(f"Backup at {BACKUP_PATH}")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Written {len(new_content)} bytes to {HTML_PATH}")