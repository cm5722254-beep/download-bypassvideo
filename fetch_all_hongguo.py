import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

categories = {
    "Real Drama (真人剧)": "https://hongguoduanju.com/category/real-drama",
    "Comic Drama (漫剧)": "https://hongguoduanju.com/category/comic-drama",
    "AI Drama (AI剧)": "https://hongguoduanju.com/category/ai-drama",
    "Comic (漫画)": "https://hongguoduanju.com/category/comic"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://hongguoduanju.com/'
}

results = {}

for cat_name, cat_url in categories.items():
    print(f"\nFetching {cat_name} from {cat_url}...")
    try:
        req = urllib.request.Request(cat_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')

            items = []
            for img in soup.find_all('img'):
                src = img.get('src', '')
                alt = img.get('alt', '')
                if 'novel-pic' in src and alt:
                    parent_a = img.find_parent('a')
                    href = parent_a.get('href', '') if parent_a else ''
                    
                    # Clean high-res cover
                    hd_poster = src.split('~')[0] if '~' in src else src

                    # Look for episode count or tags in parent text
                    container = img.find_parent(['div', 'li', 'article'])
                    meta_text = container.get_text(separator=' | ', strip=True) if container else ''

                    items.append({
                        'title': alt,
                        'poster_url': hd_poster,
                        'detail_url': ('https://hongguoduanju.com' + href) if href.startswith('/') else href,
                        'meta': meta_text
                    })

            results[cat_name] = items
            print(f"  -> Extracted {len(items)} real dramas!")
            for it in items[:3]:
                print(f"     * {it['title']} | URL: {it['detail_url']}")
    except Exception as e:
        print(f"  Error fetching {cat_name}: {e}")

# Save results to a json file
with open(r"c:\Users\NIN\Documents\TDL\hongguo_categories_dump.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nDone! Saved to hongguo_categories_dump.json")
