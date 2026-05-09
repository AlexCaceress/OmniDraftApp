# Configuración y constantes globales
import os
import platform
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
OS_NAME = platform.system()
CMD_KEY = "command" if OS_NAME == "Darwin" else "ctrl"

# Colores y constantes de UI
MI_COLOR_FONDO = "#343638"
MI_COLOR_HOVER = "#2FA572"
