import csv

def count_threats(path):
    counts = {}
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            threat = row[5]
            counts[threat] = counts.get(threat, 0) + 1
    return counts

result = count_threats("urlhaus.csv")
print(result)