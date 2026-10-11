import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def resolve_hongguo(series_id):
    url = f"https://hongguoduanju.com/player/{series_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36'})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        idx = html.find('_ROUTER_DATA = ')
        if idx != -1:
            data, _ = json.JSONDecoder().raw_decode(html[idx + len('_ROUTER_DATA = '):])
            page = data.get('loaderData', {}).get('player_(series_id)/page', {})
            vpi = page.get('video_player_info', {})
            sd = page.get('seriesDetail', {})
            return {
                "success": True,
                "title": sd.get('series_name'),
                "main_url": vpi.get('main_url'),
                "duration": vpi.get('duration'),
                "poster_url": vpi.get('poster_url') or sd.get('series_cover'),
                "episodes": sd.get('episode_cnt'),
                "tags": sd.get('tags'),
                "vid_count": len(sd.get('vid_list', []))
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": False, "error": "Not found"}

# Test on 2 sample series IDs
for sid in ["7686713195246930968", "7691228619774905368"]:
    res = resolve_hongguo(sid)
    print(f"Series {sid}:", res.get("title"), "| Video stream:", (res.get("main_url") or "")[:70], "| Episodes:", res.get("episodes"))
