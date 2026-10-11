import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hongguo_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check for JSON data in script tags
scripts = re.findall(r'<script id="([^"]+)"[^>]*>(.*?)</script>', html, re.DOTALL)
print("Scripts with ID:", [s[0] for s in scripts])

for sid, scontent in scripts:
    if 'NEXT' in sid or 'data' in sid.lower():
        try:
            d = json.loads(scontent)
            print(f"Data in {sid}: keys={list(d.keys())}")
            props = d.get('props', {}).get('pageProps', {})
            print("pageProps keys:", list(props.keys()))
            # dump first 1000 chars of pageProps
            print("Sample pageProps:", str(props)[:1000])
        except Exception as e:
            print("JSON parse error:", e)

# Also check for images and drama cards in HTML
images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']+)["\']', html)
if not images:
    images = re.findall(r'<img[^>]+alt=["\']([^"\']+)["\'][^>]*src=["\']([^"\']+)["\']', html)
print(f"\nImages with Alt ({len(images)}):")
for src, alt in images[:15]:
    print(f"  Alt: {alt} | Src: {src}")
