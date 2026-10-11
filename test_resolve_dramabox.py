import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def resolve_dramabox(book_id, book_name=""):
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', (book_name or "").lower()).strip('-')
    url = f"https://www.dramaboxdb.com/movie/{book_id}/{slug}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
        if m:
            data = json.loads(m.group(1))
            pp = data.get('props', {}).get('pageProps', {})
            cl = pp.get('chapterList', [])
            bi = pp.get('bookInfo', {})
            if cl:
                c0 = cl[0]
                return {
                    "success": True,
                    "title": bi.get('bookName') or book_name,
                    "video_url": c0.get('mp4') or c0.get('m3u8Url'),
                    "poster_url": bi.get('cover') or c0.get('cover'),
                    "duration": f"{int(c0.get('duration', 0) / 1000)}s",
                    "chapter_count": len(cl),
                    "chapters": cl
                }
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": False, "error": "No chapter list found"}

# Test on 42000021919
res = resolve_dramabox("42000021919", "Shifter Academy: Taming Three Wild Mates")
print("DramaBox 42000021919:", res.get("title"), "| Stream:", (res.get("video_url") or "")[:70], "| Chapters:", res.get("chapter_count"))
