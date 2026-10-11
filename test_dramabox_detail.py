import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://www.dramaboxdb.com', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8')
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        data = json.loads(m.group(1))
        pp = data['props']['pageProps']
        items = pp.get('smallData', [{}])[0].get('items', [])
        if items:
            it = items[0]
            book_id = it.get('bookId')
            print("Book:", book_id, it.get('bookName'))
            
            # Check links on homepage for drama
            links = re.findall(r'href=["\'](/[^"\']+)["\']', html)
            drama_links = [l for l in links if str(book_id) in l or 'drama' in l or 'book' in l or 'video' in l]
            print("Drama links:", drama_links[:5])

            if drama_links:
                test_url = 'https://www.dramaboxdb.com' + drama_links[0]
                print("Fetching:", test_url)
                r2 = urllib.request.urlopen(urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'}))
                h2 = r2.read().decode('utf-8')
                m2 = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h2)
                if m2:
                    d2 = json.loads(m2.group(1))
                    print("Detail pageProps keys:", list(d2.get('props', {}).get('pageProps', {}).keys()))
                    print("Detail props snippet:", str(d2.get('props', {}).get('pageProps', {}))[:1000])
except Exception as e:
    print("Error:", e)
