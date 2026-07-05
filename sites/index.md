---
layout: page
title: Sites
eyebrow: Registry
description: "Every tracked data-center project-site, grouped by status, state, and operator."
permalink: /sites/
---

{% assign records = "" | split: "" %}
{% for pair in site.data.sites %}{% assign records = records | push: pair[1] %}{% endfor %}
{% assign total = records | size %}

**{{ total }}** project-sites tracked. Each record is resolved from clustered,
per-source signals — see [the datasets](/data/) for license and provenance.

## By status

{% assign statuses = "announced,permitted,under-construction,operational" | split: "," %}
{% for st in statuses %}
{% assign group = records | where: "status", st %}
{% if group.size > 0 %}
### {{ st }} ({{ group.size }})

| site | operator | location | MW |
| --- | --- | --- | --- |
{% for r in group -%}
| [{{ r.name }}](/sites/{{ r.id }}/) | {{ r.operator | default: r.developer | default: "—" }} | {{ r.location.county | default: r.location.locality }}, {{ r.location.state }} | {{ r.metrics.capacity_mw | default: "—" }} |
{% endfor %}
{% endif %}
{% endfor %}

## By state

{% assign by_state = records | group_by_exp: "r", "r.location.state" | sort: "name" %}
{% for g in by_state %}
### {{ g.name }} ({{ g.items | size }})
{% for r in g.items %}- [{{ r.name }}](/sites/{{ r.id }}/) — {{ r.location.county | default: r.location.locality }} · {{ r.status }}
{% endfor %}
{% endfor %}

## By operator

{% assign by_op = records | group_by_exp: "r", "r.operator" | sort: "name" %}
{% for g in by_op %}
{% if g.name != "" %}
### {{ g.name }} ({{ g.items | size }})
{% for r in g.items %}- [{{ r.name }}](/sites/{{ r.id }}/) — {{ r.location.state }} · {{ r.status }}
{% endfor %}
{% endif %}
{% endfor %}
