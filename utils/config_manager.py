import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "tono": "Profesional",
    "idioma": "Español",
    "atajo_mod": "Ctrl + Shift",
    "atajo_tecla": "K",
    "api_key": ""
}

def cargar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def guardar_config(config_dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=4, ensure_ascii=False)