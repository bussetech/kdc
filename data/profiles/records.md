# kdc records profile — dataset configuration for gn_info_records

(Consumed as the `dataset_profile` input; platform `docs/gnome-evolution.md`.
This file defines the record schema surface and id rule; the gnome's prompt
defines the resolution method. Extracted from the retired ancestor
`gn_kdc_records` v0.4.1. Record schema of record: `schema/sites.schema.json`.)

## The subject

One record per physical project-site: a multi-phase campus is one record
with phases in `notes:`; two distinct campuses are two records even under
one program. Cluster signals on site_hint names, locality, county,
operator.

## Record schema fields (only these)

id, name, operator, developer, status,
location{country, state, region, county, locality, address, lat, lon,
parcel_ids},
metrics{capacity_mw, capacity_mw_basis, land_acres, building_sqft,
buildings, investment_usd, water},
announced_date, operational_date, first_seen, last_updated, confidence,
sources[{url, title, publisher, date, note}], signals, notes.

- `location` is country-aware (US-first): `country` is ISO 3166-1 alpha-2
  (`US`, `GB`, `IE` — never `USA`/`UK`), default `US` when a US site omits
  it. **US sites:** `state` required, 2-letter USPS code (`TX`, `VA` —
  never full names); if a US state can't be normalized, exclude that
  resolution and say so in `notes:` rather than emit an invalid record.
  **Non-US sites:** omit `state`; locate via `region` (province/land/UK
  nation, optional) + `county` + `locality`. Example: a Kent, UK campus →
  `country: GB`, `county: Kent`, `locality: Dartford`, no `state`.
- `metrics.capacity_mw_basis`: only when a signal says what the MW
  measures (IT load vs utility); otherwise omit or `unspecified`.

## Status vocabulary

`announced | permitted | under-construction | operational | cancelled`.
Dead proposals (denied, withdrawn, abandoned) are `cancelled` records with
the path told in `notes:`.

## Entity-typed fields

`operator` and `developer` — ids from the canonical-entities registry
(`data/operators.yml`) only.

## The id rule (deterministic; collision clause at the end)

Build `<operator>-<place>`, lowercase, ASCII, hyphenated:

- `<operator>` = the operator's `operators.yml` id if known; else the
  developer's id if known; else a slug of the site's distinctive proper
  name (drop generic words: "data center", "campus", "project",
  "technology").
- `<place>` = the single most-specific administrative place the signals
  give, in strict precedence: locality → else county → else state. Use
  exactly one; never combine two, never choose between equally-valid
  alternatives — the precedence decides.
- **Collision clause:** if that id would name a *different* existing site,
  append `-<county>`, then `-2`, `-3` — the sole allowed disambiguation.
