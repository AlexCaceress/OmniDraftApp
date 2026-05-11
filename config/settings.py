import platform
import sys
import os
from PIL import Image

OS_NAME = platform.system()
CMD_KEY = "command" if OS_NAME == "Darwin" else "ctrl"

# Colores y constantes de UI
MI_COLOR_FONDO = "#343638"
MI_COLOR_HOVER = "#2FA572"

def obtener_ruta_recurso(ruta_relativa):
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")
    return os.path.join(ruta_base, ruta_relativa)

