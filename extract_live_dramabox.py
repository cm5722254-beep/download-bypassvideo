import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://www.dramaboxdb.com', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=8) as r:
    html = r.read().decode('utf-8')
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        data = json.loads(m.group(1))
        pageProps = data['props']['pageProps']
        for section in pageProps.get('smallData', []):
            print(f"=== Section: {section.get('name')} ({len(section.get('items', []))} items) ===")
            for item in section.get('items', []):
                print("  Title:", item.get('bookName'), "| Chapters:", item.get('chapterCount'), "| Cover:", item.get('cover'))
