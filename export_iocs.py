import csv
import sqlite3

conn = sqlite3.connect("iocs.db")
rows = conn.execute("SELECT url from iocs").fetchall()
conn.close()

with open("iocs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["url"])
    writer.writerows(rows)

print("Exported", len(rows), "IOCs")