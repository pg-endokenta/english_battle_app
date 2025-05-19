# utils/static_manifest.py
import json
from django.conf import settings
import os

def get_vite_asset_path(entry_name: str) -> str:
    manifest_path = os.path.join(
        settings.BASE_DIR, 'static', 'frontend', '.vite', 'manifest.json'
    )
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    if entry_name not in manifest:
        raise ValueError(f"{entry_name} not found in manifest.json")
    return settings.STATIC_URL + 'frontend/' + manifest[entry_name]['file']
