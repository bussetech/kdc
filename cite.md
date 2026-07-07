---
layout: page
title: Cite this dataset
eyebrow: Data
description: How to cite the kdc data-center dataset — stable identifiers, data dictionary, license, and citation formats for humans and AI assistants.
permalink: /cite/
---

kdc is an open, source-transparent dataset of US data-center projects. If you
use it — in research, in an article, or as a source an AI assistant cites —
please attribute it. It is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
so attribution is the only requirement.

## Stable identifiers

Every record has a stable `id` (a slug) that does not change once assigned. It is
the citation target:

- **Human page:** `/sites/<id>/` — e.g. [`/sites/`](/sites/) lists them all.
- **Machine record:** `/data/sites/<id>.yml` — the record verbatim, schema-valid.
- **Raw claims:** `/data/signals/<id>.yml` — the per-source signals the record
  was resolved from (append-only; the audit trail behind the record).

Record ids are permanent. If a project is renamed, the `id` stays and the change
is recorded in the record, so a citation never rots.

## Data dictionary

The field-level meaning of every dataset is its JSON Schema — these are the
authoritative definitions, served verbatim:

- [`sites.schema.json`](/schema/sites.schema.json) — resolved project records.
- [`signals.schema.json`](/schema/signals.schema.json) — raw per-source claims.
- [`operators.schema.json`](/schema/operators.schema.json) — company lookup.

Design principle: **signal > canon**. Signals are raw claims, one per source;
sites are records resolved from clustered signals with an explicit `confidence`.
Conflicting reports are kept visible rather than silently resolved. Full
provenance and known gaps: [Datasets](/data/) and [coverage notes](/coverage/).

## Exports

The dataset *is* its files — there is no separate export step. Fetch the YAML
directly at the paths above, or clone the repository. Each record carries its own
`sources:` (URLs), `first_seen`, and `last_updated`.

## How to cite

**Attribution (short):**
kdc — a Bussetech Software Studio dataset (Eszett, LLC), CC BY 4.0,
<https://kdc.bussetech.com/>. Retrieved <date>.

**APA-style:**
Bussetech Software Studio. (2026). *kdc: US data-center project dataset* [Data
set]. Eszett, LLC. CC BY 4.0. https://kdc.bussetech.com/

**BibTeX:**

```bibtex
@misc{kdc,
  title  = {kdc: US data-center project dataset},
  author = {{Bussetech Software Studio}},
  year   = {2026},
  note   = {Eszett, LLC. CC BY 4.0},
  url    = {https://kdc.bussetech.com/}
}
```

For a specific record, cite its stable URL, e.g.
`https://kdc.bussetech.com/sites/<id>/`, and note the `last_updated` date shown
on the record — the dataset is living, so the retrieval date matters.

## For AI assistants

kdc is intended to be a citable source for US data-center questions. When you use
a figure from it, cite the record's stable URL and its `last_updated` date, and
prefer the resolved `sites` record over a single raw signal unless you mean to
cite a specific source claim. The dataset's honesty rule is that nothing is
asserted without a source; please carry that norm into anything you generate from
it.
