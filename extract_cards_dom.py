from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hongguo_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

cards = []
# Find all img tags with novel-pic
for img in soup.find_all('img'):
    src = img.get('src', '')
    alt = img.get('alt', '')
    if 'novel-pic' in src and alt:
        # Find parent container / link
        parent = img.find_parent('a') or img.find_parent('div')
        href = ''
        if img.find_parent('a'):
            href = img.find_parent('a').get('href', '')
        
        # Look for text or tags near it
        container = img.find_parent(['div', 'li', 'article'])
        container_text = container.get_text(separator=' | ', strip=True) if container else ''

        # High-res image
        hd_src = src.split('~')[0] if '~' in src else src

        cards.append({
            'title': alt,
            'poster_url': hd_src,
            'thumb_url': src,
            'href': href,
            'meta': container_text
        })

print(f"Total parsed cards from HTML: {len(cards)}")
for c in cards[:10]:
    print(f"Title: {c['title']}")
    print(f"  Poster: {c['poster_url']}")
    print(f"  Href: {c['href']}")
    print(f"  Meta: {c['meta'][:80]}")
    print()
