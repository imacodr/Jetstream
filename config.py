# Config Setup
# Config Template: {"token": ".ROBOSECURITY"}
import json
from pathlib import Path
from typing import Any

template = {"robloxKey": None}

CONFIG_DIR = Path.home() / ".jetstream"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config(config_path: Path = CONFIG_FILE):
    if not config_path.exists():
        return template
    with open(config_path, "r") as file:
        return json.load(file)
    
def save_config(config: dict[str, Any]):
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent = 4)