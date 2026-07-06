#!/usr/bin/env python3
"""Pre-render data/sites/*.yml -> data/geo/sites.geojson (one Point feature per
geocoded site), for the theme's static map layer. Deterministic: features are
id-sorted and the JSON is stably formatted, so integrity CI can drift-check the
committed file exactly like the page stubs.

Records WITHOUT location.lat/lon are NOT dropped silently — they are listed on
stdout and reported by the coverage page's geo-completeness section (which
computes the same set live from the data). GeoJSON uses [lon, lat] order.

Properties carried per feature (consumed by the theme map popup + filters):
name, status, operator (resolved display name), capacity_mw, state, county,
location (human string), url (the record page).
"""
from __future__ import annotations

import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = ROOT / "data" / "sites"
GEO = ROOT / "data" / "geo"
OUT = GEO / "sites.geojson"


def load_operators() -> dict[str, str]:
    path = ROOT / "data" / "operators.yml"
    ops = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else []
    return {o["id"]: o.get("name", o["id"]) for o in ops or []}


def human_location(loc: dict) -> str:
    place = loc.get("county") or loc.get("locality")
    state = loc.get("state")
    return ", ".join(p for p in (place, state) if p)


def build() -> tuple[list[dict], list[str]]:
    operators = load_operators()
    features: list[dict] = []
    uncovered: list[str] = []
    for path in sorted(SITES.glob("*.yml")):
        rec = yaml.safe_load(path.read_text(encoding="utf-8"))
        loc = rec.get("location") or {}
        lat, lon = loc.get("lat"), loc.get("lon")
        if lat is None or lon is None:
            uncovered.append(rec["id"])
            continue
        props = {
            "id": rec["id"],
            "name": rec.get("name", rec["id"]),
            "status": rec.get("status"),
            "url": f"/sites/{rec['id']}/",
        }
        if rec.get("operator"):
            props["operator"] = operators.get(rec["operator"], rec["operator"])
        if loc.get("state"):
            props["state"] = loc["state"]
        if loc.get("county"):
            props["county"] = loc["county"]
        hl = human_location(loc)
        if hl:
            props["location"] = hl
        cap = (rec.get("metrics") or {}).get("capacity_mw")
        if cap is not None:
            props["capacity_mw"] = cap
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": props,
            }
        )
    return features, uncovered


def render(features: list[dict]) -> str:
    fc = {"type": "FeatureCollection", "features": features}
    # Stable, drift-checkable formatting: sorted keys, 2-space indent, LF, EOF newline.
    return json.dumps(fc, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> None:
    GEO.mkdir(parents=True, exist_ok=True)
    features, uncovered = build()
    OUT.write_text(render(features), encoding="utf-8")
    total = len(features) + len(uncovered)
    print(f"gen-geo: {len(features)}/{total} sites geocoded -> {OUT.relative_to(ROOT)}")
    if uncovered:
        print(f"gen-geo: {len(uncovered)} without coordinates (listed, not dropped):")
        for rid in uncovered:
            print(f"  - {rid}")


if __name__ == "__main__":
    main()
