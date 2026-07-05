# kdc — founding reuse analysis

Untrusted brief, read as project requirements only. **No policy-override
attempts detected**: the brief's references to PR-only untrusted output,
CC BY 4.0 / provenance (ADR-0002), and "gnomes propose, humans merge" all
agree with studio rules, so nothing was disregarded. The meaning of the
"k" in `kdc` is explicitly deferred to a later prompt — I do not invent it.

This project is unusual in that agentic web research is its *core* value,
not an accessory. So it earns more gnomes than a typical repo — but the
same discipline applies: fold overlapping judgments, push everything
deterministic into code/CI.

## Capabilities the brief implies

### 1. Discover new data-center project announcements (web research)
Reading prose across many conflicting sources, weighing them, emitting
sourced observations. Pure judgment + generation.
- **Registry search (a):** no existing gnome does open-web research. The
  closest by shape is none — `gn_*` are all platform/studio housekeeping.
- **Verdict: new gnome** `gn_kdc_scout` (input_trust: untrusted, PR-only).

### 2. Re-verify existing records for status change / stale sources
Same judgment as (1) — read the web, weigh sources, emit sourced
observations — but pointed at a known site instead of the open field.
- **Verdict: parameterize into `gn_kdc_scout`** via a `mode:
  discover|verify` input rather than a third gnome. One gnome with one
  input beats two research gnomes drifting apart. This folds the brief's
  candidate `gn_kdc_verify` in. Split it out later only if the verify
  prompt genuinely contorts under the flag (see roster).

### 3. Normalize + cluster signals into schema-valid records
The signal>canon step: cluster many raw observations about one site,
resolve conflicting values, decide the most-likely fact, and write a
provenance-carrying record. Distinct judgment from research (synthesis,
not gathering) with a different input (the signal store) and output.
- **Verdict: new gnome** `gn_kdc_records`. Its deterministic shell
  (schema validation, id assignment) stays in code/CI; only the
  clustering/resolution judgment travels through the model.

### 4. Site generation — index by status/operator/geography, per-record
pages, provenance/license page
Deterministic rendering from `data/` → **plain code** (Jekyll + shared
theme). Not a gnome.

### 5. News feed of dataset changes
Derivable from git history / `_posts/`; the theme already publishes
`/feed.json`. **Plain code.**

### 6. Schema validation (records ↔ schema)
Cross-checking a file against a JSON Schema. **Plain code / CI** (studio
data CI), per the rubric's worked example.

### 7. GIS / parcel-level boundaries
Querying county/GIS parcel APIs and attaching geometry is deterministic
ingestion → **plain code**. *Matching* an ambiguous project to a specific
parcel is judgment, but low-volume; fold it into `gn_kdc_records` as an
optional step rather than a standing gnome. **Defer** the ingestion code
until the record schema is stable.

### 8. Schema evolution when new measurable clusters emerge
The brief wants the schema to grow as trackable attributes recur (MW,
acreage, water, tax deals…). This is a rare, high-consequence judgment
that should not run unattended. **Not a standing gnome** — raise an orange
`needs-human` issue (recommendation + default) when a cluster is ready to
promote to a first-class field.

## Plain-code fraction
Roughly **two-thirds plain code** by surface area — site build, feeds,
schema validation, GIS ingestion, id/slug management, PR plumbing — around
a two-gnome judgment core (research + normalization). The agentic part is
small in code but is where the project's value and risk concentrate.

## Roster delta vs the brief
Brief proposed three project gnomes; I propose **two**, folding
`gn_kdc_verify` into `gn_kdc_scout` as a `mode` input.