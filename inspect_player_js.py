import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

js_url = "https://lf-fe.fqnovelstatic.com/obj/novel-fanqie-fe/growth/incentive-h5-monorepo/apps/hongguo/static/js/player.d387d94f8b.js"
req = urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
print("Player.js size:", len(content))

for kw in ['main_url', 'video_player_info', 'vid', 'episode', 'api', 'play', 'fetch', 'ajax', 'axios', 'getPlay', 'video_model', 'qznovelvod']:
    matches = [m.start() for m in re.finditer(kw, content, re.IGNORECASE)]
    print(f"Keyword '{kw}': {len(matches)} matches")
    for m in matches[:3]:
        snip = content[max(0, m-40):min(len(content), m+60)].replace('\n', ' ')
        print(f"   ... {snip} ...")

# Dump any URLs or paths in player.js
paths = set(re.findall(r'["\'](/[a-zA-Z0-9_\-\.\/]+)["\']', content))
print(f"\nPaths in player.js: {len(paths)}")
for p in sorted(paths):
    if any(k in p for k in ['api', 'v1', 'video', 'player', 'play', 'novel', 'item']):
        print("   Path:", p)
