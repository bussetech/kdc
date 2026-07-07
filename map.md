---
layout: page
title: Map
eyebrow: Registry
description: "Every tracked data-center project-site on a map — status-coloured, filterable by status, operator, and state."
permalink: /map/
map: true
full_width: true # the map fills the width — no signup rail here
---

{% assign records = "" | split: "" %}
{% for pair in site.data.sites %}{% assign records = records | push: pair[1] %}{% endfor %}
{% assign total = records | size %}

Every tracked project-site, plotted from the same records as the
[registry](/sites/). Markers are status-coloured (colour is wayfinding);
cancelled proposals stay on the map as a hollow ring — a dead project is a
record, not an omission. Coordinates are approximate, geocoded from each
record's sourced location; see [coverage](/coverage/) for
precision and completeness.

{% include map-legend.html %}

{% assign gj = '/data/geo/sites.geojson' | relative_url %}
{% include map-cluster.html
   geojson=gj
   filters="status,operator,state"
   height="34rem"
   label="every tracked project-site"
   caption="© OpenStreetMap contributors. Markers approximate — see coverage." %}

## All sites

The map is an enhancement over this table — with JavaScript off, the table is
the record. **{{ total }}** project-sites:

| site | status | operator | location | MW |
| --- | --- | --- | --- | --- |
{% for r in records -%}
| [{{ r.name }}](/sites/{{ r.id }}/) | {{ r.status }} | {{ r.operator | default: r.developer | default: "—" }} | {{ r.location.county | default: r.location.locality }}, {{ r.location.state }} | {{ r.metrics.capacity_mw | default: "—" }} |
{% endfor %}

Grouped views (by status, state, operator) live on the
[registry](/sites/). Dataset licence and provenance: [datasets](/data/).
