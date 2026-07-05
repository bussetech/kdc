#!/usr/bin/env python3
"""kdc dataset referential integrity (runs after schema validation).

Checks, each with a readable error:
  - site/signal ids are unique and equal their filename stem
  - signals.site_id (when set) references an existing site
  - sites.signals[] reference existing signals
  - sites.operator / sites.developer reference operators.yml ids
  - every site record has a page stub sites/<id>.md with site_id: <id>,
    and every stub has a record (scripts/gen-pages.sh regenerates)
  - data/geo/sites.geojson matches what scripts/gen-geo.sh would emit
    (committed pre-rendered map data must not drift from the records)
"""
from __future__ import annotations

import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors: list[str] = []


def load_dir(dirpath: pathlib.Path) -> dict[str, dict]:
    docs = {}
    if not dirpath.is_dir():
        return docs
    for path in sorted(dirpath.glob("*.yml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        rid = doc.get("id") if isinstance(doc, dict) else None
        if rid != path.stem:
            errors.append(f"{path.relative_to(ROOT)}: id {rid!r} != filename stem {path.stem!r}")
        if rid in docs:
            errors.append(f"{path.relative_to(ROOT)}: duplicate id {rid!r}")
        docs[rid] = doc
    return docs


sites = load_dir(ROOT / "data" / "sites")
signals = load_dir(ROOT / "data" / "signals")

operators_path = ROOT / "data" / "operators.yml"
operators = yaml.safe_load(operators_path.read_text(encoding="utf-8")) if operators_path.exists() else []
operator_ids = {o["id"] for o in operators or []}
seen = set()
for o in operators or []:
    if o["id"] in seen:
        errors.append(f"data/operators.yml: duplicate operator id {o['id']!r}")
    seen.add(o["id"])

for sid, sig in signals.items():
    ref = sig.get("site_id")
    if ref is not None and ref not in sites:
        errors.append(f"data/signals/{sid}.yml: site_id {ref!r} is not a site record")

for rid, rec in sites.items():
    for field in ("operator", "developer"):
        ref = rec.get(field)
        if ref is not None and ref not in operator_ids:
            errors.append(f"data/sites/{rid}.yml: {field} {ref!r} is not in data/operators.yml")
    for sref in rec.get("signals") or []:
        if sref not in signals:
            errors.append(f"data/sites/{rid}.yml: signal ref {sref!r} does not exist")

# page stubs ↔ records
stub_dir = ROOT / "sites"
stub_ids = set()
for stub in sorted(stub_dir.glob("*.md")):
    if stub.name == "index.md":
        continue
    m = re.search(r"^site_id:\s*(\S+)\s*$", stub.read_text(encoding="utf-8"), re.M)
    stub_id = m.group(1) if m else None
    if stub_id != stub.stem:
        errors.append(f"sites/{stub.name}: site_id {stub_id!r} != filename stem")
    if stub_id not in sites:
        errors.append(f"sites/{stub.name}: no record data/sites/{stub_id}.yml (stale stub? run scripts/gen-pages.sh)")
    stub_ids.add(stub_id)
for rid in sites:
    if rid not in stub_ids:
        errors.append(f"data/sites/{rid}.yml: missing page stub sites/{rid}.md (run scripts/gen-pages.sh)")

# pre-rendered map data ↔ records (drift-checked like the page stubs)
import gen_geo  # noqa: E402  (same scripts/ dir)

geojson_path = ROOT / "data" / "geo" / "sites.geojson"
expected = gen_geo.render(gen_geo.build()[0])
if not geojson_path.exists():
    errors.append("data/geo/sites.geojson missing (run scripts/gen-geo.sh)")
elif geojson_path.read_text(encoding="utf-8") != expected:
    errors.append("data/geo/sites.geojson is stale — drifts from data/sites/ (run scripts/gen-geo.sh)")

if errors:
    for e in errors:
        print(f"::error::integrity: {e}")
    print(f"Referential integrity FAILED: {len(errors)} problem(s)")
    sys.exit(1)
print(f"Referential integrity OK: {len(sites)} sites, {len(signals)} signals, {len(operator_ids)} operators")
