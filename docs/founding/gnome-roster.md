# kdc — proposed founding gnome roster

Two new project-level gnomes. Both are homed in `bussetech/kdc`, both
carry untrusted input, both are PR-only. Everything else the brief asked
for is plain code (see analysis).

## `gn_kdc_scout`
- **display_name:** Gnome KDC Scout
- **level:** project · **home:** kdc · **deployments:** [kdc]
- **trigger:** scheduled (weekly cron) + manual `workflow_dispatch`
- **input_trust:** untrusted (open web) → **PR only**, never direct commit
- **inputs:** `mode: discover|verify` (default `discover`),
  optional `target` (site id, for verify runs)
- **purpose:** research data-center project announcements and status
  changes on the open web; emit sourced *signals* (one claim per source)
  as a PR to `data/signals/`. Never writes records directly.

## `gn_kdc_records`
- **display_name:** Gnome KDC Records
- **level:** project · **home:** kdc · **deployments:** [kdc]
- **trigger:** on merged PRs touching `data/signals/`; scheduled sweep
- **input_trust:** untrusted (signals derive from the web) → **PR only**
- **purpose:** cluster signals per site, resolve conflicting values into
  the most-likely fact with confidence + provenance, and open a PR that
  creates or updates a schema-valid record in `data/sites/`.

## Deliberately not gnomes
- **Site build, feeds, provenance page** — deterministic, plain code.
- **Schema validation** — studio data CI.
- **GIS/parcel ingestion** — deterministic API pulls, code; deferred.
- **`gn_kdc_verify`** — folded into `gn_kdc_scout` (`mode: verify`).
  Promote to its own gnome only if the verify prompt cannot share the
  scout prompt without contortion.

## What would earn more gnomes
- A **third research gnome** if discover vs verify genuinely diverge
  (different sources, different evidence standards) and the `mode` flag
  bloats the prompt.
- A **schema-evolution gnome** only if attribute clusters emerge fast
  enough that human-reviewed promotion (current plan) becomes a
  bottleneck — until then it stays an orange issue.