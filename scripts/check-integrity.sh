#!/usr/bin/env bash
# Referential-integrity hook for studio data CI (declared in data-ci.yml).
# Runs after schema validation; pyyaml is present on the CI runner.
# Locally: any python3 with pyyaml (e.g. `pip install pyyaml`).
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/check_integrity.py
