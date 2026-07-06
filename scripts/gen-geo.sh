#!/usr/bin/env bash
# Regenerate data/geo/sites.geojson from data/sites/*.yml (deterministic;
# integrity CI fails when the committed file drifts). Needs python3 + pyyaml.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/gen_geo.py "$@"
