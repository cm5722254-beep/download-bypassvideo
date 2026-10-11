import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://hongguoduanju.com/player/7686713195246930968"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
for s in scripts:
    print(s)
