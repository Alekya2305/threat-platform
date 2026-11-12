import sqlite3
import time

from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()
conn = sqlite3.connect("iocs.db", check_same_thread=False)

# --- metrics: created once, when the API starts ---
LOOKUPS = Counter("ioc_lookups_total", "Number of /check lookups")
RESULTS = Counter(
    "ioc_lookup_results_total",
    "Lookups by result: hit = known bad, miss = not in list",
    ["result"],
)
LATENCY = Histogram(
    "ioc_lookup_seconds",
    "Time to answer one /check, in seconds",
    buckets=[0.0005, 0.001, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/check")
def check(value: str):
    start = time.perf_counter()
    try:
        LOOKUPS.inc()
        row = conn.execute("SELECT 1 FROM iocs WHERE url = ?", (value,)).fetchone()
        known_bad = row is not None
        if known_bad:
            RESULTS.labels(result="hit").inc()
        else:
            RESULTS.labels(result="miss").inc()
        return {"value": value, "known_bad": known_bad}
    finally:
        LATENCY.observe(time.perf_counter() - start)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)