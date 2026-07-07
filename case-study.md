---
layout: page
title: How KDC gets built — and maintained
eyebrow: Studio
description: "A one-person software studio founded, populated, and now maintains this dataset with its own agent machinery: a ledger entry for every run, a pull request for every change."
permalink: /case-study/
---

KDC is a working example of how the [Bussetech Software
Studio](https://bussetech.com) builds. One human and a workforce of
*gnomes* (single-purpose agents, each named and doing one task end to
end) took this dataset from an empty repository to a live, source-cited,
public site, and every step is on the record.

## Founded by filing one issue

KDC began as a single *new-project* issue. A founder gnome analyzed it and
the studio's factory did the rest (created the repository, wired DNS,
turned on branch protection, published the site, configured its tests), and
a human reviewed and merged the founding change. From there, two project
gnomes do the ongoing work: one researches the world into per-source
*signals*, the other resolves those signals into the *records* you
browse here. Neither can merge its own work. Every change they make arrives
as a pull request a person reviews first.

## Trust is a property of the pipeline, not the model

The very first thing the research gnome produced, live, was invalid against
this dataset's schema, and the site's continuous-integration checks
refused to merge it. The prompt was corrected, the re-run passed, and no
invalid record has ever reached the published dataset. That is the studio's
whole approach in one event: output you can trust is a property of the
pipeline that gates it, not a promise about the model behind it. Every
record on this site carries its sources; the [dataset](/data/) is open under
CC BY 4.0, and the [coverage page](/coverage/) even documents where research
looked and found *nothing* — because an honest negative is data too.

## Open by construction, cheap by design

The dataset now holds 162 source-cited records across 48 US states and its
first international entry, resolved from 716 per-source signals — a
living count you can recount from the [open data](/data/) any time. Putting
those records here took on the order of a dozen dollars of agent spend
(counting the console-directed research runs that expanded coverage, not just
the automated slice), inside a studio budget it publishes in aggregate. The
studio doesn't *promise* transparency; building this way, it can't *not*
provide it.

## What's proven, and what's still being measured

Here is the honest line the studio holds itself to. Cycle correctness
(that the machine advances cleanly from research to record to published
site) is proven: the studio ran the full cycle on demand and watched it
work (and fixed the defects those runs surfaced). Growth to 162 records was
studio-dispatched: real runs, each a reviewed pull request.

What is *not* yet claimed is that the dataset maintains itself *unattended*.
The scheduled daily refresh is now firing, and it is in a short
reliability soak this month. Until that soak returns a verdict, the true
claim is the one the studio makes: built in a day, sustained by dispatched
cycles, a receipt for every run — scheduled autonomy in verification. When
the soak passes, this page will be updated with the run links that earn the
stronger claim, and not before.

---

*Want the verdict when it lands?* The studio will update this page when the
autonomy soak returns. Use the subscribe box on this page to get a note
when KDC resolves new records — and when the next study ships.
