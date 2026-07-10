# kdc scout profile — dataset configuration for gn_info_scout

(Consumed as the `dataset_profile` input; platform `docs/gnome-evolution.md`.
This file defines WHAT the dataset catalogs; the gnome's prompt defines HOW.
kdc is info-archetype build 1 — this profile is the extracted, of-record
domain knowledge of its retired ancestor, `gn_kdc_scout` v0.2.2.)

## The dataset

US data-center projects (international sites appear when sources cover
them). The **subject-of-record ("site") is one physical project-site**: a
campus with phases is one subject; two distinct campuses are two subjects,
even under one program. `site_hint` format for unknown subjects:
`"<site name as reported> — <county>, <state>"`.

## Attribute vocabulary

`status`, `capacity_mw`, `land_acres`, `building_sqft`, `buildings`,
`investment_usd`, `operator`, `developer`, `location`, `announced_date`,
`operational_date`, `parcel_ids`, `name`.

## What is signal-worthy

Lifecycle status (including denials and withdrawals — those are records,
not omissions), headline metrics (MW, acres, sqft, buildings, investment),
operator/developer identity, location facts, and key dates. Feed material
is noisy: most items (opinion pieces, industry commentary, unrelated news)
yield no signal. Skip color quotes and jobs numbers unless they are the
only capacity evidence. Values that must be split per source when sources
differ: e.g. "$2.7B county est. vs $3B developer est." is two signals.

**Cap: the most informative ~8 signals per site.**

## Confidence refinement

Primary sources for this domain: the operator/developer itself and
government bodies (county boards, planning commissions, utility filings).
Trade press (DCD, Data Center Frontier) and local press are `medium`.
