import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://hongguoduanju.com/player/7686713195246930968"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Referer': 'https://hongguoduanju.com/detail?series_id=7686713195246930968'
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

print("Player HTML length:", len(html))

# Check for video tag
videos = re.findall(r'<video[^>]*src=["\']([^"\']+)["\']', html)
print(f"Direct <video src>: {videos}")

# Check for all mp4, m3u8, ts urls
media = re.findall(r'https?://[^\s"\'<>]+\.(?:mp4|m3u8|flv)[^\s"\'<>]*', html)
print(f"Media stream links found: {len(media)}")
for m in set(media):
    print("  Media link:", m)

# Check _ROUTER_DATA or _SSR_DATA
idx = html.find('_ROUTER_DATA = ')
if idx != -1:
    sub = html[idx + len('_ROUTER_DATA = '):]
    try:
        data, _ = json.JSONDecoder().raw_decode(sub)
        print("Player _ROUTER_DATA loaderData keys:", list(data.get('loaderData', {}).keys()))
        player_page = data.get('loaderData', {}).get('player_page', {}) or data.get('loaderData', {})
        print("player_page keys:", list(player_page.keys()))
        for k in player_page:
            v = player_page[k]
            print(f"  {k} ({type(v).__name__}): {str(v)[:300]}")
    except Exception as e:
        print("JSON parse error:", e)

# Also dump any play_url, main_url, video_url
tokens = re.findall(r'["\'](https?://[^"\']*(?:video|douyin|byte|volc|stream|sign)[^"\']*)["\']', html)
print(f"\nOther ByteDance/media tokens: {len(tokens)}")
for t in set(tokens[:15]):
    print("  ", t)
