#!/usr/bin/env bash
set -euo pipefail

# Simple reproducible build via Docker
# Usage: ./build_deb_docker.sh [version]
VER="${1:-${PACKAGE_VERSION:-0.1.0~dev}}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

docker run --rm -v "$ROOT_DIR":/src -w /src ubuntu:22.04 /bin/bash -lc "\
  apt-get update \&\& apt-get install -y --no-install-recommends ca-certificates rsync fakeroot dpkg-dev python3 python3-venv python3-pip \n\
  && ./camoufox/scripts/package_deb.sh $VER \n\
"
