# Listener de atajos de teclado
from pynput import keyboard

listener_actual = None

def iniciar_listener(atajo_pynput, callback):
	global listener_actual
	if listener_actual is not None:
		listener_actual.stop()
	listener_actual = keyboard.GlobalHotKeys({atajo_pynput: callback})
	listener_actual.start()
