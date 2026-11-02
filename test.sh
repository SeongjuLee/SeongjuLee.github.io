#!/bin/sh
set -eu
python3 scripts/build.py --check
python3 tests/check_site.py
