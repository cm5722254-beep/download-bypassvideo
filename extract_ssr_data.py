import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hongguo_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'window\._SSR_DATA\s*=\s*(\{.*?\});\s*(?:window|<)', html, re.DOTALL)
if not m:
    m = re.search(r'window\._SSR_DATA\s*=\s*(\{.*?\})\s*</script>', html, re.DOTALL)

if m:
    print("Found window._SSR_DATA!")
    try:
        data = json.loads(m.group(1))
        print("SSR_DATA keys:", list(data.keys()))
        loader_data = data.get('data', {})
        print("loader_data keys:", list(loader_data.keys()))
        for k, v in loader_data.items():
            print(f"Key: {k}")
            if isinstance(v, dict):
                print(f"  Dict keys: {list(v.keys())}")
                if 'data' in v:
                    d2 = v['data']
                    print(f"  Nested data type: {type(d2)}")
                    if isinstance(d2, dict):
                        print(f"  Nested data keys: {list(d2.keys())}")
                        # Look for drama list
                        for subk in d2:
                            if isinstance(d2[subk], list):
                                print(f"    Found list {subk}: len={len(d2[subk])}")
                                if d2[subk] and isinstance(d2[subk][0], dict):
                                    print("    Sample drama item:", d2[subk][0])
    except Exception as e:
        print("JSON parse error:", e)
else:
    print("window._SSR_DATA not matched by regex")
