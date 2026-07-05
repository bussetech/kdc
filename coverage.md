---
layout: page
title: Coverage
eyebrow: Data
description: What has been researched, what was found, and what was honestly not found.
permalink: /coverage/
---

KDC records what exists — and documents where research found nothing, so an
empty area reads as *surveyed*, not *unexamined*. Fewer real records beat
many invented ones.

## Bootstrap survey (2026-07-05)

**United States, broad:** major operators, hyperscalers, AI builders, REITs
and developers — seeded with flagship campuses across TX, LA, IN, TN, WI, IA
plus Virginia depth.

**Virginia, deep — Greater Richmond Metro:**

| county | result |
| --- | --- |
| Henrico | surveyed — see records |
| Chesterfield | 5 project-sites (3 Google, 2 Chirisa/PowerHouse at Meadowville) |
| Goochland | 1 project-site (Tract, first under the Nov 2025 Technology Overlay District) |
| Powhatan | 1 project-site (Province Group, Page Road — rezoned 2024-10, expanded 2025-10) |
| Hanover | surveyed — see records |
| New Kent | **no project exists** — the county is drafting a technology overlay district along Route 33, and its community development director stated (2026-03) it "has not received a proposal nor an application for a data center" ([New Kent-Charles City Chronicle](https://nkccnews.com/local-news/2026/03/08/consideration-for-development-of-technology-overlay-district-targets-data-center-development/)) |

## Geo-completeness

The [map](/map/) renders from `data/geo/sites.geojson`, pre-rendered from the
records by `scripts/gen-geo.sh` and drift-checked in CI. A record appears on
the map only when it carries `location.lat`/`location.lon`; records without
coordinates are **listed here, never dropped**.

{% assign records = "" | split: "" %}
{% for pair in site.data.sites %}{% assign records = records | push: pair[1] %}{% endfor %}
{% assign total = records | size %}
{% assign uncovered = "" | split: "" %}
{% for r in records %}{% unless r.location.lat and r.location.lon %}{% assign uncovered = uncovered | push: r %}{% endunless %}{% endfor %}
{% assign mapped = total | minus: uncovered.size %}

**{{ mapped }} of {{ total }}** records are geocoded and on the map.
{% if uncovered.size > 0 %}The following have no coordinates yet:

{% for r in uncovered %}- [{{ r.name }}](/sites/{{ r.id }}/) — {{ r.location.county | default: r.location.locality }}, {{ r.location.state }}
{% endfor %}
{% else %}Every current record is placed.{% endif %}

**On precision (honest disclosure):** these coordinates are *editorially
geocoded* from each record's already-sourced location — county, locality, or
street address — at locality-to-address precision and rounded to ~3 decimals.
They are a cartographic rendering aid, **not** a source-stated coordinate, and
are not survey-grade; several co-located campuses (e.g. White Oak Technology
Park) are nudged apart for legibility. Exact parcel geometry
(`data/parcels/<id>.geojson`, keyed off `location.parcel_ids`) is the deferred
precise layer — see the [map decision](https://github.com/bussetech/platform/blob/main/docs/decisions/ADR-0027-map-tiles-and-library.md).
Capturing source-stated coordinates and parcel GPINs (upgrading derived →
sourced) is tracked as follow-up scout/records work.

## Notable negatives

Notable negatives elsewhere: the **Prince William Digital Gateway**
(QTS/Compass, ~2,100 acres) was cancelled — courts voided the rezoning and
both developers withdrew by mid-2026 — so Prince William is represented by
the operational Iron Mountain Manassas campus instead. The **City of
Richmond** has no data-center project; the "Richmond" DC Blox site is in
Henrico County.
