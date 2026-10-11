import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

r = urllib.request.urlopen(urllib.request.Request('https://www.dramaboxdb.com/movie/42000021919/shifter-academy-taming-three-wild-mates-', headers={'User-Agent': 'Mozilla/5.0'}))
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.read().decode('utf-8'))
if m:
    data = json.loads(m.group(1))
    cl = data['props']['pageProps'].get('chapterList', [])
    print("Total chapters in DramaBox:", len(cl))
    if cl:
        print("Chapter 0 keys:", list(cl[0].keys()))
        print("Chapter 0 data:", json.dumps(cl[0], indent=2))
