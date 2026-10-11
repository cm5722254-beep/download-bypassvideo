import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Referer': 'https://hongguoduanju.com/category/comic-drama'
}

url = 'https://hongguoduanju.com/detail?series_id=7691228619774905368'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

print("Detail page length:", len(html))

# search for video links, m3u8, mp4, episode lists
videos = re.findall(r'(https?://[^\s"\'<>]+\.(?:mp4|m3u8)[^\s"\'<>]*)', html)
print(f"Videos found: {len(videos)}")
for v in set(videos)[:5]:
    print("  Video:", v)

# search for episode numbers, chapters, or play links
play_links = re.findall(r'<a[^>]+href=["\']([^"\']*(?:play|episode|watch|chapter)[^"\']*)["\'][^>]*>(.*?)</a>', html, re.I)
print(f"Play links found: {len(play_links)}")
for p, t in play_links[:10]:
    print("  Play Link:", p, "|", t)

# check for scripts with JSON data (episodes list)
scripts = re.findall(r'<script([^>]*)>(.*?)</script>', html, re.DOTALL)
for attrs, body in scripts:
    if 'series_id' in body or 'episode' in body.lower() or 'item_id' in body:
        print("Script with series data:", body[:300])
