# Parcel-geometry ingestion — assessment (EPIC2-06)

**Status:** assessed, mechanism proven, **build deferred** (founder's original
deferral stands, now with a documented pattern and a concrete blocker).

The site schema carries `location.parcel_ids` and reserves
`data/parcels/<id>.geojson` for parcel geometry (per `CLAUDE.md`, deferred
until the site schema stabilised). EPIC2-06 was asked to assess whether one
Richmond-metro county's parcels are *cheaply* ingestable and, if so, do one
proof and document the pattern — **without** building a general GIS pipeline.

## Finding: one clean statewide source covers the whole cluster

We do not need per-county integrations. **VGIN** (the Virginia Geographic
Information Network, hosted by VDEM) publishes an authoritative **statewide
parcel layer** as an ArcGIS REST FeatureServer — keyless, GeoJSON-capable, and
covering every Richmond-metro locality (Henrico, Chesterfield, Goochland,
Hanover, Powhatan, New Kent) plus the rest of Virginia:

```
https://vginmaps.vdem.virginia.gov/arcgis/rest/services/VA_Base_Layers/VA_Parcels/FeatureServer/0/query
```

It answers both query shapes we would ever need:

- **point-in-polygon** — given a site's `location.lat/lon`, return the parcel
  that contains it;
- **by identifier** — given a `PARCELID` (GPIN) / `VGIN_QPID`, return that
  parcel.

Returned fields include `VGIN_QPID`, `FIPS` (locality FIPS), `LOCALITY`,
`PARCELID` (the local GPIN), and `LASTUPDATE`, with a `Polygon` geometry.

### Proof (reproducible, keyless)

Point query against the geocoded Meta / White Oak Technology Park coordinate
(`37.436, -77.283`):

```sh
curl -s "https://vginmaps.vdem.virginia.gov/arcgis/rest/services/VA_Base_Layers/VA_Parcels/FeatureServer/0/query?\
geometry=-77.283,37.436&geometryType=esriGeometryPoint&inSR=4326&\
spatialRel=esriSpatialRelIntersects&outFields=VGIN_QPID,FIPS,LOCALITY,PARCELID,LASTUPDATE&\
returnGeometry=true&outSR=4326&resultRecordCount=1&f=geojson"
```

returns one GeoJSON `Feature`: a 13-vertex `Polygon` with
`PARCELID: "836-684-2627"`, `FIPS: "51087"` (Henrico), `LOCALITY: "Henrico
County"`. So the *mechanism* is cheap and works today.

## Why the build is still deferred (the honest blocker)

The proof also shows why coordinate-driven ingestion must **not** be automated
yet: the point query returned *a* ~13-acre parcel at our approximate marker —
**not a verified Meta parcel**. Two problems:

1. **Our coordinates are approximate** (locality/address geocodes, ~3-decimal;
   see `coverage.md`). A point lands in whatever parcel happens to contain it,
   which for an approximate point is often a neighbour.
2. **Campuses span many parcels.** A hyperscaler site is an assemblage of GPINs,
   not one polygon. Ingesting the single containing parcel would misrepresent
   the site.

Authoritative parcel geometry therefore requires **source-stated GPINs** —
captured by `gn_kdc_scout` from county filings / assessor records into
`location.parcel_ids[]`, the same signal→record path every other fact takes.
Parcels are downstream of that capture, not a substitute for it. Committing
coordinate-derived polygons now would launder an approximate marker into false
precision — exactly what `signal > canon` forbids. So no parcel file is
committed in this session.

## The pattern, when GPIN capture lands (deterministic code, not a gnome)

1. `gn_kdc_scout` records `location.parcel_ids: ["836-684-2627", ...]` on a site
   from a cited source (filing / assessor), like any other signal.
2. Register the VGIN endpoint in `data/sources.yml` under the fetch allowlist
   with its robots/ToS review (ADR-0025) — parcel geometry is a fetched source
   and must live on the allowlist, never be hit ad hoc by the scheduled layer.
3. A deterministic `scripts/gen-parcels.sh` (plain code, like `gen-geo.sh`)
   fetches each record's GPIN polygons → `data/parcels/<id>.geojson`,
   integrity-drift-checked like the geojson and stubs.
4. The theme locator/cluster map can then render the polygon (an additive
   enhancement over the point marker — no theme change needed for points).

## Verdict

- **Ingestable?** Yes — cheaply, via one keyless statewide VGIN endpoint. No
  per-county work, no shapefile wrangling, no key.
- **Built this session?** No. The precondition (source-stated GPINs) is missing,
  and coordinate-derived parcels would be unverified. Filed as follow-up.
- **Not built (per prompt):** no general GIS pipeline, no ad-hoc fetching.
