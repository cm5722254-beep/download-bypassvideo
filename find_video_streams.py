import urllib.request
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Referer': 'https://hongguoduanju.com/category/real-drama'
}

url = 'https://hongguoduanju.com/detail?series_id=7686713195246930968'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

print("Detail page length:", len(html))

# Find all occurrences of http/https urls in the page
all_urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/:\?=%&;~]+', html)
video_urls = [u for u in all_urls if any(u.lower().endswith(ext) or ext in u.lower() for ext in ['.mp4', '.m3u8', '.ts', 'video', 'stream', 'play'])]
print(f"Video-like URLs ({len(video_urls)}):")
for v in list(set(video_urls))[:10]:
    print("  ", v)

# Find byteimg or bytecdn or douyin or snssdk or aweme urls
byte_urls = [u for u in all_urls if any(k in u for k in ['byteimg', 'zijie', 'snssdk', 'douyin', 'aweme', 'volces', 'hongguo'])]
print(f"\nByteDance/Hongguo media URLs ({len(byte_urls)}):")
for b in list(set(byte_urls))[:10]:
    print("  ", b)

# Check scripts for episode data or video IDs
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for s in scripts:
    if 'item_id' in s or 'series_id' in s or 'video_id' in s or 'play_url' in s:
        print("\nFound Script with video/series tokens (len):", len(s))
        # print snippet
        clean = re.sub(r'\s+', ' ', s)
        print("  Snippet:", clean[:400])
