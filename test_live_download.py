import urllib.request
import json
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

cat = json.loads(urllib.request.urlopen('http://127.0.0.1:8989/api/catalog').read().decode('utf-8'))
item = next((x for x in cat if x['id'] == 'hg-7686713195246930968'), None)
print("Testing live download for:", item['title'])

req_data = json.dumps({'items': [item], 'download_posters': True, 'download_videos': True}).encode('utf-8')
r = urllib.request.Request('http://127.0.0.1:8989/api/download/start', data=req_data, headers={'Content-Type': 'application/json'})
resp = json.loads(urllib.request.urlopen(r).read().decode('utf-8'))
print("Task submitted:", resp)

task_id = resp['task_ids'][0]
for step in range(12):
    time.sleep(1.5)
    tasks = json.loads(urllib.request.urlopen('http://127.0.0.1:8989/api/download/tasks').read().decode('utf-8'))
    t = next((x for x in tasks if x['id'] == task_id), None)
    if t:
        print(f"Step {step+1}: {t['progress']}% | Speed: {t['speed']} | Status: {t['status']} | File: {t['current_file']}")
        if t['status'] in ('completed', 'cancelled'):
            print("Finished! Saved files:")
            for f in t.get('saved_files', []):
                print(f"  - {f} (Size: {os.path.getsize(f):,} bytes)")
            break
