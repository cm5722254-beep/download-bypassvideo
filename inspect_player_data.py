import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://hongguoduanju.com/player/7686713195246930968"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

idx = html.find('_ROUTER_DATA = ')
sub = html[idx + len('_ROUTER_DATA = '):]
data, _ = json.JSONDecoder().raw_decode(sub)
page_data = data.get('loaderData', {}).get('player_(series_id)/page', {})

print("Page data keys:", list(page_data.keys()))
for k in page_data:
    if k != 'req':
        v = page_data[k]
        if isinstance(v, dict):
            print(f"\n--- Key: {k} (dict keys: {list(v.keys())}) ---")
            for sub_k in v:
                sub_v = v[sub_k]
                if isinstance(sub_v, list):
                    print(f"  {sub_k}: list of {len(sub_v)} items, first: {str(sub_v[:1])[:200]}")
                elif isinstance(sub_v, dict):
                    print(f"  {sub_k}: dict keys {list(sub_v.keys())}")
                else:
                    print(f"  {sub_k}: {str(sub_v)[:100]}")
        elif isinstance(v, list):
            print(f"\n--- Key: {k} (list of {len(v)}) ---")
            print(str(v[:2])[:300])
        else:
            print(f"\n--- Key: {k} --- {v}")
