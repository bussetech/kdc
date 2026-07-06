---
layout: page
title: Datasets
eyebrow: Data
description: The datasets behind kdc — text-based, versioned, schema-validated.
permalink: /data/
---

Every dataset in this project is a text file in the repo (`data/`), validated
in CI against a JSON Schema (`schema/`), and served here verbatim. The design
principle is **signal > canon**: signals are raw per-source claims; sites are
records resolved from clustered signals with explicit confidence.

## Datasets

| dataset | files | schema |
| --- | --- | --- |
| sites — resolved project records | `data/sites/<id>.yml` ([browse](/sites/)) | [`sites.schema.json`](/schema/sites.schema.json) |
| signals — raw per-source claims, append-only | `data/signals/<id>.yml` | [`signals.schema.json`](/schema/signals.schema.json) |
| operators — company lookup | [`operators.yml`](/data/operators.yml) | [`operators.schema.json`](/schema/operators.schema.json) |

Referential integrity across the three (`signals.site_id` ↔ sites,
`sites.operator` ↔ operators, `sites.signals[]` ↔ signals) is enforced by
`scripts/check-integrity.sh` in data CI.

{%- comment -%}
  Email capture (platform EPIC3-03, #98). Dormant until the theme pin carries
  signup.html and studio.signup is enabled with a real provider action (see
  platform docs/gtm/provider-evaluation.md). The guard keeps the include
  unresolved — and the build green — while enabled is false.
{%- endcomment -%}
{%- if site.studio.signup.enabled %}
{% include signup.html placement="kdc-dataset" %}
{%- endif %}

## License

The datasets published by this project are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (studio default,
ADR-0002). The project's code is MIT-licensed (see the repo's LICENSE).

## Provenance

Records are researched from public sources — press coverage, operator
announcements, county/municipal filings and press releases — each cited by
URL inside the record itself (`sources:`) and, at the signal level, one claim
per source. Nothing is asserted without a source; conflicting reports are
kept visible (record `notes:` and coexisting signals) rather than silently
resolved. Transformations applied: normalization of names/units into the
schema, clustering of per-source signals into one record per project-site,
and a human-or-gnome-assigned aggregate `confidence`. Collection began
2026-07-05 (project founding); each record carries `first_seen` /
`last_updated` dates. Known gaps are documented rather than filled:
[coverage notes](/coverage/).
