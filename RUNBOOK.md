# Runbook: Lookup API – P99 latency too high

## The alert
- **Name:** `LookupApiP99LatencyHigh`
- **Fires when:** P99 of `/check` is above **100 ms for 5 minutes**
- **Query:**
  `histogram_quantile(0.99, sum by (le) (rate(ioc_lookup_seconds_bucket[5m]))) > 0.1`
- **Normal (baseline, Nov 12):** P95 ≈ 0.9 ms, P99 ≈ 1 ms, ~9 lookups/s, hit rate ≈ 20%
- **Dashboard:** Grafana → "Lookup API"

## What it means
- The slowest 1% of lookups take more than 100 ms (normal is ~1 ms).
- Callers (detection jobs, analysts) wait longer. If they time out, a known-bad
  URL may be treated as "not bad" → **missed detections**. This is a security risk,
  not just a speed problem.
- It does NOT mean the API is down (that is a separate alert: `up == 0`).

## How to check (first 5 minutes)
1. **Still happening?** Dashboard → latency panel. Is P99 still high now?
2. **P95 too, or only P99?**
   - Both high → the whole service is slow.
   - Only P99 → a small group of requests (one pod, one node, one kind of query).
3. **Traffic spike?** Lookups/s panel, or `sum(rate(ioc_lookups_total[5m]))`. Compare with normal.
4. **Hit rate normal?** A drop to 0% means the IOC table may be empty or missing.
5. **Prometheus reaching the API?** `up{job="lookup-api"}` → 1 = yes, 0 = no.
6. **Server or caller?** The histogram only times the code inside `/check`.
   If callers say "slow" but server P99 is fine, the delay is outside the API:
   network, DNS, connection setup. (Nov 12 example: Windows `localhost` → IPv6
   first → 2 s per request, while server P99 stayed at 1 ms.)
7. **Recent change?** A deploy, new image, or new `iocs.db` in the last hour?
   `kubectl rollout history deployment/lookup-api`
8. **Pods healthy?**
   `kubectl get pods` (RESTARTS going up? OOMKilled?)
   `kubectl top pods` (CPU near the 500m limit → throttled)
   `kubectl logs <pod> --since=15m`

## Likely causes → fixes
| Cause | Signs | Fix |
|---|---|---|
| Traffic spike | Lookups/s up, P95 + P99 up together | Add replicas (`kubectl scale` or HPA); find which caller is spiking |
| CPU throttling | `kubectl top pods` near the CPU limit | More replicas, or raise the CPU limit |
| Bad deploy | Started right after a release | Roll back: `kubectl rollout undo deployment/lookup-api` |
| Database slow | P99 grows with table size; queries slow in logs | Check `url` is the PRIMARY KEY (index); restore the previous `iocs.db` |
| Pod restarting | RESTARTS going up, gaps in graphs | `kubectl logs <pod> --previous`; fix the cause or raise the memory limit |
| One bad pod / node | Only P99 high, P95 normal | `kubectl delete pod <pod>` (Kubernetes replaces it) |
| Caller-side delay | Server P99 normal, callers slow | Check DNS / IPv6 / network; measure from the caller's side |

## Escalate
- **After 15 minutes** with no clear cause, **or** P99 above **1 s**, **or** errors (5xx) rising:
  - Detection Platform on-call (secondary): `<name / pager>`
  - Team lead: `<name>`
  - Infra problem (nodes, network): platform / SRE on-call `<channel>`
- If lookups are timing out: tell the detection / SOC team that **detections may be missed**
  for this time window.

## After the incident
- Write a short note: start time, end time, cause, fix, follow-up tasks.
- Update this runbook with anything that was missing.