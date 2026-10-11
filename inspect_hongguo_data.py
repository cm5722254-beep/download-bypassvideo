import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hongguo_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
if m:
    data = json.loads(m.group(1))
    pageProps = data.get('props', {}).get('pageProps', {})
    print("pageProps keys:", list(pageProps.keys()))
    # Check data list
    for k in pageProps:
        val = pageProps[k]
        if isinstance(val, dict):
            print(f"Dict {k} keys:", list(val.keys()))
        elif isinstance(val, list):
            print(f"List {k} len={len(val)}")

    # Check if there is a drama list or book list
    drama_list = pageProps.get('dramaList') or pageProps.get('list') or pageProps.get('items') or pageProps.get('data', {}).get('list') or pageProps.get('data')
    if drama_list:
        if isinstance(drama_list, dict):
            print("drama_list dict keys:", list(drama_list.keys()))
            items = drama_list.get('items') or drama_list.get('list') or drama_list.get('data') or []
        else:
            items = drama_list
        print(f"Total drama items found: {len(items)}")
        if items and isinstance(items[0], dict):
            print("First item keys:", list(items[0].keys()))
            print("Sample item:", items[0])
