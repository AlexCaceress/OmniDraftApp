# Funciones para copiar/pegar texto
import pyperclip
import pyautogui
import time
from config.settings import CMD_KEY

def copiar_texto_seleccionado():
	pyperclip.copy("")
	pyautogui.hotkey(CMD_KEY, "c")
	for _ in range(20):
		time.sleep(0.05)
		texto = pyperclip.paste()
		if texto and not texto.isspace():
			return texto
	return None

def reemplazar_texto(texto):
	pyperclip.copy(texto)
	time.sleep(0.05)
	pyautogui.hotkey(CMD_KEY, "v")
