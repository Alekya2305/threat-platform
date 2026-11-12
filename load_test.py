import csv
import json
import random
import time
import urllib.parse
import urllib.request

API = "http://127.0.0.1:8000/check"
TOTAL = 300
BAD = 60                      # 60 known-bad, 240 clean

random.seed(42)               # same "random" picks every run

# 1. load the known-bad URLs (iocs.csv has a header "url", one column)
with open("iocs.csv", newline="") as f:
    reader = csv.reader(f)
    next(reader)              # skip the header
    bad_urls = [row[0] for row in reader]

# 2. 60 bad + 240 clean, then mix them
urls = random.sample(bad_urls, BAD)        # 60 DIFFERENT bad URLs
urls += [f"http://clean-site-{i}.example.com/page" for i in range(TOTAL - BAD)]
random.shuffle(urls)

# 3. send them one by one
hits = 0
start = time.perf_counter()
for url in urls:
    query = urllib.parse.urlencode({"value": url})   # value=http%3A%2F%2F...
    with urllib.request.urlopen(f"{API}?{query}") as resp:
        body = json.loads(resp.read())               # text -> dict
    if body["known_bad"]:
        hits += 1
    time.sleep(0.1)           # spread over ~30 s, so graphs show a shape

elapsed = time.perf_counter() - start
print(f"Sent {TOTAL} lookups in {elapsed:.1f} s, hits: {hits}, misses: {TOTAL - hits}")