# kdc — data design

Signal>canon architecture: **signals** are the raw, per-source
observations; **sites** are the resolved records built from clustered
signals. Both are text stores in `data/`, one JSON Schema per dataset in
`schema/`, validated by studio data CI. One record per file (directory
datasets) keeps PR diffs small and reviewable.

Provenance and the CC BY 4.0 dataset license are stated in
`data/index.md` (required by template + ADR-0002).

## Dataset: `sites` — resolved project records
- **Format:** YAML, one file per record: `data/sites/<id>.yml`
- **Schema:** `schema/site.schema.json`
- **Key:** `id` (slug, unique) · **Refs:** `operator` → `operators.id`,
  `signals[]` → `signals.id`, `location.parcel_ids[]` → `parcels`

| field | type | constraints |
|---|---|---|
| id | string (slug) | required, unique |
| name | string | required |
| operator | string | ref operators.id, optional |
| developer | string | optional |
| status | enum | required: announced \| permitted \| under-construction \| operational |
| location.address | string | optional |
| location.county | string | optional |
| location.state | string | required, 2-letter (US) |
| location.country | string | default `US` |
| location.lat / lon | number | optional |
| location.parcel_ids | array[string] | optional |
| metrics.capacity_mw | number | optional |
| metrics.land_acres | number | optional |
| metrics.building_sqft | number | optional |
| metrics.investment_usd | number | optional |
| metrics.water | string | optional, free-form until a cluster promotes it |
| announced_date | date | optional |
| first_seen | date | required |
| last_updated | date | required |
| confidence | enum | low \| medium \| high (aggregate) |
| sources | array[{url, publisher, date, note}] | required, min 1 |
| signals | array[string] | ref signals.id |
| notes | string | optional |

`metrics.*` is the evolving section: new measurable attributes start as
optional fields and are promoted from `signals` when a trackable cluster
emerges (via an orange issue — see CLAUDE.md).
**Provenance:** built by `gn_kdc_records` from clustered signals; every
field value is traceable to a signal and thence to a source URL.

## Dataset: `signals` — raw per-source observations
- **Format:** YAML, one file per signal: `data/signals/<id>.yml`
  (append-only; superseded signals are kept, not deleted)
- **Schema:** `schema/signal.schema.json`
- **Key:** `id` · **Ref:** `site_id` → `sites.id` (null = candidate)

| field | type | constraints |
|---|---|---|
| id | string | required, unique |
| site_id | string \| null | ref sites.id; null for unmatched candidates |
| attribute | string | required (e.g. `status`, `capacity_mw`, `name`) |
| value | string | required (raw, as reported) |
| source_url | string (url) | required |
| publisher | string | optional |
| observed_date | date | required |
| collected_by | string | required (gnome name + run id) |
| confidence | enum | low \| medium \| high (source-level) |
| notes | string | optional |

**Provenance:** written by `gn_kdc_scout` (untrusted, PR-only). One signal
= one claim from one source; conflicting claims coexist by design.

## Dataset: `operators` — company lookup
- **Format:** YAML list: `data/operators.yml`
- **Schema:** `schema/operators.schema.json` · **Key:** `id`

| field | type | constraints |
|---|---|---|
| id | string (slug) | required, unique |
| name | string | required |
| type | enum | hyperscaler \| reit \| developer \| colo \| utility \| other |
| aliases | array[string] | optional |

**Provenance:** curated; low churn. Cadence: as new operators appear.

## Dataset: `parcels` (deferred) — GIS geometry
- **Format:** GeoJSON per site: `data/parcels/<id>.geojson`
- **Assumption:** deferred until the site schema is stable; sourced from
  county/GIS parcel APIs by plain ingestion code, referenced from
  `sites.location.parcel_ids`. Parcel↔project matching judgment folds
  into `gn_kdc_records`.

## Assumptions
- Per-record directory layout (`data/sites/`, `data/signals/`) rather than
  single-file datasets — better PR diffs at scale. If studio data CI
  expects strictly `data/<name>.*`, adjust to a single file per dataset.
- US-only for now (brief), hence `country` defaults to `US`.