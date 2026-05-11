import platform

OS_NAME = platform.system()
CMD_KEY = "command" if OS_NAME == "Darwin" else "ctrl"

# Colores y constantes de UI
MI_COLOR_FONDO = "#343638"
MI_COLOR_HOVER = "#2FA572"
