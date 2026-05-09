# Componentes CustomTkinter reutilizables
import customtkinter as ctk
import pyautogui

popup = None
popup_label = None

def mostrar_popup(app, texto="✍️ Corrigiendo..."):
	global popup
	global popup_label
	cerrar_popup()
	popup = ctk.CTkToplevel(app)
	popup.overrideredirect(True)
	popup.attributes("-topmost", True)
	popup.attributes("-alpha", 0.96)
	popup.configure(fg_color="#1E1E1E")
	x, y = pyautogui.position()
	popup.geometry(f"260x60+{x+20}+{y+20}")
	popup_label = ctk.CTkLabel(
		popup,
		text=texto,
		font=("Helvetica", 14, "bold")
	)
	popup_label.pack(
		expand=True,
		fill="both",
		padx=20,
		pady=10
	)
	popup.update()

def actualizar_popup(texto):
	global popup_label
	if popup_label:
		popup_label.configure(text=texto)
		popup_label.update()

def cerrar_popup():
	global popup
	global popup_label
	try:
		if popup:
			popup.destroy()
	except:
		pass
	popup = None
	popup_label = None
