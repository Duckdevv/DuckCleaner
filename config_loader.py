import json
from pathlib import Path


def load_rules(json_path="organizer.json"):
    config_file = Path(json_path).resolve()

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {json_path}")

    with open(config_file, "r", encoding="utf-8") as f:
        raw_rules = json.load(f)

    clean_rules = {}
    for folder, extensions in raw_rules.items():
        clean_exts = []
        for ext in extensions:
            ext_clean = str(ext).strip().lower()
            if not ext_clean.startswith("."):
                ext_clean = f".{ext_clean}"
            clean_exts.append(ext_clean)
        clean_rules[folder] = clean_exts

    return clean_rules
