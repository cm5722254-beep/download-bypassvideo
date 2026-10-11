import re

with open(r'C:\Users\NIN\.gemini\antigravity-ide\brain\49425f56-258e-4105-bfc4-6b54bbb79909\.system_generated\steps\361\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

files = re.findall(r'href="(/M4St3r0/hongguo-downloader/blob/[^"]+)"', text)
print("Blobs:", len(files))
for f in set(files):
    print("  ", f)

# Also check for readme content or description
m = re.search(r'readme[^>]*>(.*?)</article>', text, re.DOTALL | re.IGNORECASE)
if m:
    clean = re.sub(r'<[^>]+>', ' ', m.group(1))
    print("\nReadme snippet:\n", clean[:1500])
