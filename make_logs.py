import csv
import random
from datetime import datetime, timedelta

random.seed(42)                          # same "random" picks every run

# 1. Load the real bad URLs from Step 1
bad_urls = []
with open("iocs.csv", newline="") as f:
    reader = csv.reader(f)
    next(reader)                         # skip the header line "url"
    for row in reader:
        bad_urls.append(row[0])          # collect each URL into the list

clean_urls = [
    "https://www.google.com/",
    "https://github.com/",
    "https://docs.python.org/3/",
    "https://www.wikipedia.org/",
    "https://aws.amazon.com/",
]
users = ["alice", "bob", "carol", "dave"]

TOTAL = 1000
BAD = 25

# 2. Pick the URLs and mix them
urls = random.choices(clean_urls, k=TOTAL - BAD) + random.sample(bad_urls, BAD)   # 975 clean + 25 different bad
random.shuffle(urls)                     # mix the order

# 3. Write the log file
start = datetime(2026, 11, 9, 10, 0, 0)
with open("fake_logs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "user", "url"])    # header line
    for i, url in enumerate(urls):                   # i = 0, 1, 2, ... next to each url
        ts = start + timedelta(seconds=i)            # one log line per second
        writer.writerow([ts.isoformat(), random.choice(users), url])

print("Wrote", len(urls), "lines,", BAD, "bad")