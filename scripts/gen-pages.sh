#!/usr/bin/env bash
# Regenerate sites/<id>.md page stubs from data/sites/*.yml (deterministic;
# integrity CI fails when stubs and records drift). Needs python3 + pyyaml.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/gen_pages.py "$@"
