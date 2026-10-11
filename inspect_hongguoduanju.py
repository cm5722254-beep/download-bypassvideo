import urllib.request
import re
import json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://hongguoduanju.com/'
}

def inspect_category(cat_url):
    print(f"\n=================== INSPECTING {cat_url} ===================")
    try:
        req = urllib.request.Request(cat_url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print("HTML Length:", len(html))

            soup = BeautifulSoup(html, 'html.parser')

            # Find drama links, cards, titles, and images
            # Let's inspect article or card containers
            articles = soup.find_all(['article', 'div'], class_=re.compile(r'post|card|item|drama|video|entry', re.I))
            print(f"Candidate card elements: {len(articles)}")

            # Find all links to dramas
            dramas = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text(strip=True)
                img = a.find('img')
                img_src = img.get('src') or img.get('data-src') or img.get('data-original') if img else None

                # Check if it looks like a drama detail link
                if href and ('/drama/' in href or '/video/' in href or '/post/' in href or '/detail/' in href or re.search(r'/\d+\.html', href) or (href.startswith('https://hongguoduanju.com/') and len(href.split('/')) == 4)):
                    if (text or img_src) and href not in [d['url'] for d in dramas] and not any(href.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg']):
                        dramas.append({
                            'title': text,
                            'url': href,
                            'poster': img_src
                        })

            print(f"Extracted Drama Links count: {len(dramas)}")
            for d in dramas[:8]:
                print(" - Title:", d['title'], "| Link:", d['url'], "| Poster:", d['poster'])

            # If dramas found, let's inspect the first drama detail page to see video player / m3u8 / mp4!
            if dramas:
                detail_url = dramas[0]['url']
                if not detail_url.startswith('http'):
                    detail_url = 'https://hongguoduanju.com' + detail_url
                print(f"\n--- INSPECTING FIRST DETAIL PAGE: {detail_url} ---")
                req_det = urllib.request.Request(detail_url, headers=headers)
                with urllib.request.urlopen(req_det, timeout=12) as d_resp:
                    det_html = d_resp.read().decode('utf-8', errors='ignore')
                    print("Detail HTML length:", len(det_html))
                    # search for video / iframe / m3u8 / mp4
                    videos = re.findall(r'(https?://[^\s"\'<>]+\.(?:mp4|m3u8)[^\s"\'<>]*)', det_html)
                    print(f"Direct Video Links found: {len(videos)}")
                    for v in set(videos)[:5]:
                        print("   Video Stream:", v)

                    # search for iframes or player configs
                    iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', det_html)
                    print(f"Player IFrames found: {len(iframes)}")
                    for ifr in iframes[:3]:
                        print("   Iframe:", ifr)

    except Exception as e:
        print("Inspection Error:", e)

if __name__ == '__main__':
    inspect_category('https://hongguoduanju.com/category/real-drama')
    inspect_category('https://hongguoduanju.com/category/comic-drama')
