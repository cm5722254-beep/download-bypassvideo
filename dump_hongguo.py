import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Referer': 'https://hongguoduanju.com/'
}

url = 'https://hongguoduanju.com/category/comic-drama'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

with open(r"c:\Users\NIN\Documents\TDL\hongguo_page.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved HTML to hongguo_page.html, size:", len(html))

# Let's search for interesting patterns in html
links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
print(f"Total links: {len(links)}")
for href, text in links[:25]:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if clean_text and not any(ign in href for ign in ['#', 'javascript', 'wp-']):
        print(f"  Href: {href} | Text: {clean_text[:40]}")
