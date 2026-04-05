import base64
import os
import re

# Extract base64 from dash.py
with open('dash.py', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r"e = b'([a-zA-Z0-9+/=\n]+)'", content)
if match:
    b64_string = match.group(1).replace('\n', '')
    decoded = base64.b64decode(b64_string).decode('utf-8')
    
    # Save decoded version
    with open('_dash_decoded.py', 'w', encoding='utf-8') as f:
        f.write(decoded)
    
    print(f"✓ Saved decoded dash.py to _dash_decoded.py ({len(decoded)} bytes)")
