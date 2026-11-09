from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("stream-detect").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

SCHEMA = "event_id STRING, ts TIMESTAMP, user STRING, url STRING"

# Static table: the bad URLs (same as detect.py)
iocs = spark.read.csv("iocs.csv", header=True)

# 1. Read the stream from Kafka
raw = (spark.readStream.format("kafka")
       .option("kafka.bootstrap.servers", "localhost:9092")
       .option("subscribe", "logs")
       .option("startingOffsets", "earliest")                # first run: from the start
       .load())

# 2. Unpack the JSON: bytes → text → columns
events = (raw
    .select(F.from_json(F.col("value").cast("string"), SCHEMA).alias("e"))
    .select("e.*"))

# 3. Remove duplicates (remember IDs for 10 min of event time), then flag bad URLs
clean = (events
         .withWatermark("ts", "10 minutes")                   # lateness limit
         .dropDuplicates(["event_id", "ts"]))                 # skip rows already seen
alerts = clean.join(F.broadcast(iocs), on="url", how="inner")

# 4. Print alerts live
query = (alerts.writeStream
         .outputMode("append")                                # only NEW rows
         .format("console")
         .option("truncate", False)                           # don't cut long URLs
         .option("numRows", 50)                               # console shows only 20 rows by default
         .option("checkpointLocation", "chk/alerts_v2")       # NEW bookmark folder
         .start())                                            # begin the stream
query.awaitTermination()                                      # keep running until Ctrl+C