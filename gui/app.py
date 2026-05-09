# Lógica de la ventana principal
import customtkinter as ctk
import threading
import time
import pyautogui
from pynput.keyboard import Controller
from config.settings import MI_COLOR_FONDO, MI_COLOR_HOVER, OS_NAME
from gui.widgets import mostrar_popup, actualizar_popup, cerrar_popup
from ia.corrector import corregir_texto_ia_stream
from utils.clipboard import copiar_texto_seleccionado, reemplazar_texto
from hotkeys.listener import iniciar_listener

procesando = False
teclado = Controller()

def set_estado(app, lbl_estado, texto, color="gray"):
	app.after(
		0,
		lambda: lbl_estado.configure(
			text=texto,
			text_color=color
		)
	)

def ejecutar_correccion(app, combo_tono, combo_idioma, lbl_estado):
	global procesando
	if procesando:
		return
	procesando = True
	try:
		time.sleep(0.2)
		pyautogui.keyUp("shift")
		pyautogui.keyUp("ctrl")
		if OS_NAME == "Darwin":
			pyautogui.keyUp("command")
		app.after(0, lambda: mostrar_popup(app, "Copiando texto..."))
		texto_original = copiar_texto_seleccionado()
		if not texto_original:
			app.after(0, lambda: actualizar_popup("No hay texto seleccionado"))
			set_estado(app, lbl_estado, "No hay texto seleccionado", "#e74c3c")
			time.sleep(2)
			app.after(0, cerrar_popup)
			return
		tono = combo_tono.get()
		idioma = combo_idioma.get()
		app.after(0, lambda: actualizar_popup("Escribiendo..."))
		set_estado(app, lbl_estado, "Escribiendo en tiempo real...", "#3498db")
		try:
			for chunk in corregir_texto_ia_stream(texto_original, tono, idioma):
				teclado.type(chunk)
				time.sleep(0.005)
		except Exception as ia_error:
			raise Exception(f"Error de IA: {str(ia_error)}")
		app.after(0, lambda: actualizar_popup("¡Listo!"))
		set_estado(app, lbl_estado, "Texto corregido", "#2ecc71")
		time.sleep(1)
		app.after(0, cerrar_popup)
	except Exception as e:
		app.after(0, lambda: mostrar_popup(app, f"{str(e)}"))
		set_estado(app, lbl_estado, f"Error: {str(e)}", "#e74c3c")
		time.sleep(3)
		app.after(0, cerrar_popup)
	finally:
		procesando = False

def run_app():
	ctk.set_appearance_mode("dark")
	ctk.set_default_color_theme("blue")
	app = ctk.CTk()
	app.title("AI QUICK FIX")
	app.geometry("360x380")
	app.attributes("-topmost", True)
	titulo = ctk.CTkLabel(
		app,
		text="✨ AI QUICK FIX",
		font=("Helvetica", 22, "bold")
	)
	titulo.pack(pady=20)
	ctk.CTkLabel(app, text="Tono:").pack()
	combo_tono = ctk.CTkOptionMenu(
		app,
		values=["Formal", "Informal"],
		width=220,
		fg_color=MI_COLOR_FONDO,
		button_color=MI_COLOR_FONDO,
		button_hover_color=MI_COLOR_HOVER
	)
	combo_tono.set("Profesional")
	combo_tono.pack(pady=10)
	ctk.CTkLabel(app, text="Idioma:").pack()
	combo_idioma = ctk.CTkOptionMenu(
		app,
		values=["Español", "Inglés", "Francés", "Alemán", "Italiano"],
		width=220,
		fg_color=MI_COLOR_FONDO,
		button_color=MI_COLOR_FONDO,
		button_hover_color=MI_COLOR_HOVER
	)
	combo_idioma.set("Español")
	combo_idioma.pack(pady=10)
	ctk.CTkLabel(app, text="Atajo de teclado:").pack(pady=(10, 0))
	frame_atajo = ctk.CTkFrame(app, fg_color="transparent")
	frame_atajo.pack(pady=5)
	combo_mod = ctk.CTkOptionMenu(
		frame_atajo,
		values=["Ctrl + Shift", "Ctrl + Alt", "Alt + Shift"],
		width=120,
		fg_color=MI_COLOR_FONDO,
		button_color=MI_COLOR_FONDO,
		button_hover_color=MI_COLOR_HOVER
	)
	combo_mod.set("Ctrl + Shift")
	combo_mod.pack(side="left", padx=5)
	combo_letra = ctk.CTkOptionMenu(
		frame_atajo,
		values=[chr(i) for i in range(65, 91)],
		width=70,
		fg_color=MI_COLOR_FONDO,
		button_color=MI_COLOR_FONDO,
		button_hover_color=MI_COLOR_HOVER
	)
	combo_letra.set("K")
	combo_letra.pack(side="left", padx=5)
	info = ctk.CTkLabel(
		app,
		text_color="gray",
		font=("Helvetica", 12)
	)
	info.pack(pady=20)
	lbl_estado = ctk.CTkLabel(
		app,
		text="Esperando atajo...",
		text_color="gray",
		font=("Helvetica", 12, "bold")
	)
	lbl_estado.pack(pady=10)

	def cambiar_atajo(*args):
		modificador = combo_mod.get()
		letra = combo_letra.get().lower()
		diccionario_mods = {
			"Ctrl + Shift": "<ctrl>+<shift>",
			"Ctrl + Alt": "<ctrl>+<alt>",
			"Alt + Shift": "<alt>+<shift>"
		}
		atajo_pynput = f"{diccionario_mods[modificador]}+{letra}"
		info.configure(text=f"Selecciona texto en cualquier app\ny pulsa:\n{modificador} + {letra.upper()}")
		def al_pulsar_atajo():
			threading.Thread(
				target=ejecutar_correccion,
				args=(app, combo_tono, combo_idioma, lbl_estado),
				daemon=True,
				name="AI-CORRECTOR"
			).start()
		iniciar_listener(atajo_pynput, al_pulsar_atajo)

	combo_mod.configure(command=cambiar_atajo)
	combo_letra.configure(command=cambiar_atajo)
	cambiar_atajo()
	app.mainloop()
