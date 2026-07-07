#!/usr/bin/env bash
# Run the Haven Stays demo BFF proxy locally: serves the storefront + proxies
# to AdaL Cloud with the Clerk JWT injected server-side (never exposed to the
# browser).
#
# Provide the token one of two ways (never commit it):
#   export ADAL_JWT="eyJ..."         # env var, OR
#   echo "eyJ..." > proxy/.adal_jwt  # gitignored file
#
# Usage:
#   ./run_local.sh                              # http://127.0.0.1:8500/
#   PORT=9000 ./run_local.sh
#   ADAL_BASE_URL=http://localhost:8080 ./run_local.sh   # point at a local platform
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/proxy"

PORT="${PORT:-8500}"
HOST="${HOST:-127.0.0.1}"

python -m pip install -q -r requirements.txt
echo "Starting Haven Stays proxy on http://${HOST}:${PORT}/"
exec python -m uvicorn server:app --host "${HOST}" --port "${PORT}"
