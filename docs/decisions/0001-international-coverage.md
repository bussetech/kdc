# 0001 — International coverage (country-aware location)

- **Status:** accepted
- **Date:** 2026-07-06
- **Deciders:** sysop (via console)

## Context

kdc bootstrapped **US-only**: `schema/sites.schema.json` fixed
`location.country` to the enum `["US"]` and *required* a 2-letter USPS
`state`. But `gn_kdc_scout` discovers from open press feeds, and the world's
data-center buildout is global — the scout collected a UK site (a Clearstone
campus near Dartford, Kent). `gn_kdc_records` then produced a record the US-only
schema rejected (`state` required; `country` outside the enum), so data CI
blocked the resolution and the signals stranded (platform#120).

Two ways out: (a) enforce US-only — scout/records exclude non-US sites; or
(b) make the dataset country-aware. The dataset's value is a neutral,
source-transparent map of *the* data-center buildout; excluding half the planet
narrows that value, and the buildout outside the US is large and growing.

## Decision

**kdc covers data-center project-sites internationally, US-first.** The
location model becomes country-aware:

- `location.country` — **ISO 3166-1 alpha-2** code (`US`, `GB`, `IE`, …),
  required, default `US`.
- `location.state` — **US sites: required, 2-letter USPS code** (enforced by a
  conditional schema `if country == US`). **Non-US sites: omit** — locate via
  the new optional `region` (province / land / UK nation) and the existing
  `county` / `locality`, which are already free-form.

Emphasis stays US-first (Virginia / Greater Richmond remain the depth targets);
international sites are recorded as discovered, not sought out as a separate
program.

## Consequences

- **Schema** (`schema/sites.schema.json`): `country` enum → alpha-2 pattern +
  required; `state` moved from unconditional-required to a `country == US`
  conditional; new optional `region`. All 33 existing US records validate
  unchanged (verified).
- **`gn_kdc_records`** must emit `country` as an alpha-2 code and, for US sites,
  `state` as the 2-letter USPS code (never the full name — the `Texas` vs `TX`
  bug that surfaced this). Prompt updated (platform).
- **Rendering** already tolerates a stateless site (the site build was green on
  the pre-fix UK record); location displays fall back to country + county +
  locality. The map plots any lat/lon; a US-centric default view is cosmetic
  follow-up, not a blocker.
- **`state` is no longer a proxy for "US".** Any code that keyed US-ness off
  `state` presence must key off `country` instead.

## Alternatives considered

- **US-only (exclude non-US).** Simpler, but permanently narrows the dataset's
  premise and throws away real, sourced signals. Rejected.
- **Free-form `country` string.** Rejected for `US`/`USA`/`United States`
  drift; alpha-2 is the stable canonical key (mirrors the `state` 2-letter
  discipline).
