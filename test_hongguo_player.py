import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

js_url = "https://lf-fe.fqnovelstatic.com/obj/novel-fanqie-fe/growth/incentive-h5-monorepo/apps/hongguo/static/js/detail.03657c0638.js"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36'}

req = urllib.request.Request(js_url, headers=headers)
content = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
print(f"detail.js size: {len(content)} chars")

# Search for endpoints or paths
paths = re.findall(r'["\'](/[a-zA-Z0-9_\-\.\/]+)["\']', content)
clean_paths = [p for p in paths if any(k in p for k in ['api', 'video', 'play', 'episode', 'series', 'drama', 'stream', 'token', 'auth'])]
print("\nUnique matched paths in detail.js:")
for p in sorted(list(set(clean_paths))):
    print("  ", p)

# Search for domains / urls
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/:\?=%&;~]+', content)
print(f"\nUnique URLs ({len(urls)}):")
for u in set(urls):
    print("  ", u)
