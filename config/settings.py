import platform
import sys
import os
from dotenv import load_dotenv

def obtener_ruta_recurso(ruta_relativa):
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")
    return os.path.join(ruta_base, ruta_relativa)

ruta_env = obtener_ruta_recurso(".env")
load_dotenv(ruta_env)

API_KEY = os.getenv("API_KEY")

OS_NAME = platform.system()
CMD_KEY = "command" if OS_NAME == "Darwin" else "ctrl"

MI_COLOR_FONDO = "#343638"
MI_COLOR_HOVER = "#2FA572"