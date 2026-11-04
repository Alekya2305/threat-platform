import csv

class IOCStore:
    def __init__(self):
        self.bad_urls = set()

    def add(self, url):
        self.bad_urls.add(url)

    def is_bad(self, url):
        return url in self.bad_urls

    def load(self, path):
        try:
            with open(path, newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or row[0].startswith("#"):
                        continue
                    self.add(row[2])
        except FileNotFoundError as e:
            print("Could not load feed:", e)

if __name__ == "__main__":

    store = IOCStore()
    store.load("missing.csv")
    print(len(store.bad_urls))

    store.load("urlhaus.csv")
    print(len(store.bad_urls))