import json
import os
import uuid

def obtener_ruta_config():
    appdata = os.getenv('APPDATA')
    
    if not appdata:
        appdata = os.path.expanduser('~')
    
    carpeta_app = os.path.join(appdata, "OmniDraft")
    
    if not os.path.exists(carpeta_app):
        os.makedirs(carpeta_app)
        
    return os.path.join(carpeta_app, "config.json")

CONFIG_FILE = obtener_ruta_config()

DEFAULT_CONFIG = {
    "tono": "Profesional",
    "idioma": "Español",
    "atajo_mod": "Ctrl + Shift",
    "atajo_tecla": "K",
    "tutorial_visto": False,
    "user_id": str(uuid.uuid4()),
    "custom_api_key": ""
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