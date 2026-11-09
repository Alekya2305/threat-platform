from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("detect").getOrCreate()   # start Spark; this script = driver
spark.sparkContext.setLogLevel("WARN")                          # hide most INFO lines

# Read the two tables (transformations, nothing runs yet)
logs = spark.read.csv("fake_logs.csv", header=True)             # 1,000 log lines: timestamp, user, url
iocs = spark.read.csv("iocs.csv", header=True)                  # 126,786 bad URLs: url

# Match: keep only log lines whose url is in the IOC list
alerts = logs.join(F.broadcast(iocs), on="url", how="inner")    # copy iocs to every executor, keep matches

# Save the result for the next job (action → work starts)
alerts.write.mode("overwrite").parquet("out/alerts")            # folder of part files + _SUCCESS

print("Log lines:", logs.count())                               # expect 1000
print("IOCs:", iocs.count())                                    # expect 126786
print("Alerts:", alerts.count())                                # expect 25
alerts.show(5, truncate=False)                                  # peek at 5 alerts, full URLs

spark.stop()