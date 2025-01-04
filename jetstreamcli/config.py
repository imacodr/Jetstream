# Config Setup
# Config Template: {"robloxToken": "API_TOKEN"}
import json
from pathlib import Path
from typing import Any

template = {"robloxKey": None, "uploader": None, "groupKey": False}

TOOL_DIR = Path.home() / ".jetstream"
PROJECTS_DIR = TOOL_DIR / "projects"
CONFIG_FILE = TOOL_DIR / "config.json"

def load_config(config_path: Path = CONFIG_FILE):
    if not config_path.exists():
        return template
    with open(config_path, "r") as file:
        return json.load(file)
    
def save_config(config: dict[str, Any]):
    if not TOOL_DIR.exists():
        TOOL_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent = 4)