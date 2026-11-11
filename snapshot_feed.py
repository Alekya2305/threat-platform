import boto3
from datetime import date

BUCKET = "aw-prep-alekya-20261110"
today = date.today().isoformat()            # "2026-11-10"
key = f"raw/urlhaus/{today}/recent.csv"     # dated name inside the bucket

s3 = boto3.client("s3")                      # prepare the S3 client (no network yet)
s3.upload_file("urlhaus.csv", BUCKET, key)   # (local file, bucket, key) → uploads now
print("Uploaded", key)

resp = s3.list_objects_v2(Bucket=BUCKET, Prefix="raw/urlhaus/")   # list names only, no download
for obj in resp.get("Contents", []):        # Contents = list of objects ([] if none)
    print(obj["Key"], obj["Size"])          # name in S3, size in bytes