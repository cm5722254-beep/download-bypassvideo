import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_dramabox():
    print("=== TESTING DRAMABOX LIVE SCRAPE ===")
    url = "https://www.dramaboxdb.com"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print("DramaBox HTML length:", len(html))
            
            # Check for next data
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if m:
                data = json.loads(m.group(1))
                print("Found __NEXT_DATA__ keys:", list(data.keys()))
                page_props = data.get('props', {}).get('pageProps', {})
                print("pageProps keys:", list(page_props.keys()))
                # Look for dramas / books
                for k, v in page_props.items():
                    if isinstance(v, list) and len(v) > 0:
                        print(f"List {k} ({len(v)} items):")
                        if isinstance(v[0], dict):
                            print("  Sample item keys:", list(v[0].keys()))
                            print("  Sample item:", v[0].get('bookName') or v[0].get('title') or v[0].get('name'))
            else:
                print("No __NEXT_DATA__ found, checking regex...")
    except Exception as e:
        print("DramaBox error:", e)

def test_donghua():
    print("\n=== TESTING DONGHUA / ANIME LIVE APIS ===")
    endpoints = [
        "https://api.jikan.moe/v4/top/anime?type=tv&filter=airing",
        "https://api.jikan.moe/v4/anime?genres=10&order_by=popularity", # Fantasy / Donghua
        "https://gogoanimehd.io",
    ]
    for ep in endpoints:
        try:
            req = urllib.request.Request(ep, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = resp.read()
                print(f"SUCCESS {ep}: len={len(data)}")
                if ep.startswith("https://api.jikan"):
                    j = json.loads(data.decode('utf-8'))
                    items = j.get('data', [])
                    print(f"  Got {len(items)} anime/donghua live titles:")
                    for it in items[:4]:
                        print("   -", it.get('title'), "| Poster:", it.get('images', {}).get('jpg', {}).get('image_url'))
        except Exception as e:
            print(f"FAIL {ep}: {e}")

if __name__ == '__main__':
    test_dramabox()
    test_donghua()
