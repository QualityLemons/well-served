#!/bin/bash
set -e

nix-env -iA nixpkgs.mesa 2>/dev/null || true

pip install -r requirements.txt --quiet
python manage.py migrate --settings=config.settings.local --no-input
