import customtkinter as ctk
import threading
import time
import pyautogui
import pyperclip
from pynput.keyboard import Controller
from config.settings import OS_NAME
from gui.ui_builder import InterfazUsuario
from gui.tray import GestorBandeja
from gui.popup import PopupManager
from ia.corrector import corregir_texto_ia_stream
from utils.clipboard import copiar_texto_seleccionado
from hotkeys.listener import iniciar_listener

class AIQuickFixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI QUICK FIX")
        self.geometry("360x380")
        self.attributes("-topmost", True)

        self.procesando = False
        self.teclado = Controller()

        # Iniciamos la UI
        self.popup = PopupManager(self)
        self.ui = InterfazUsuario(self, callback_atajo=self._cambiar_atajo)
        self.tray = GestorBandeja(self)

        # Configuramos la X para usar la bandeja
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.bind("<Unmap>", self.tray.al_minimizar)
        
        # Iniciamos atajo por defecto
        self._cambiar_atajo()

    def _cambiar_atajo(self, *args):
        modificador = self.ui.combo_mod.get()
        letra = self.ui.combo_letra.get().lower()
        diccionario_mods = {
            "Ctrl + Shift": "<ctrl>+<shift>",
            "Ctrl + Alt": "<ctrl>+<alt>",
            "Alt + Shift": "<alt>+<shift>"
        }
        atajo_pynput = f"{diccionario_mods[modificador]}+{letra}"
        self.ui.info.configure(text=f"Selecciona texto en cualquier app\ny pulsa:\n{modificador} + {letra.upper()}")
        
        iniciar_listener(atajo_pynput, self._al_pulsar_atajo)

    def _al_pulsar_atajo(self):
        threading.Thread(target=self._ejecutar_correccion, daemon=True).start()

    def _ejecutar_correccion(self):
        if self.procesando: return
        self.procesando = True

        portapapeles_previso = pyperclip.paste()
        
        try:
            time.sleep(0.2)
            pyautogui.keyUp("shift")
            pyautogui.keyUp("ctrl")
            if OS_NAME == "Darwin": pyautogui.keyUp("command")

            self.after(0, lambda: self.popup.mostrar("Escribiendo..."))
            texto_original = copiar_texto_seleccionado()

            if not texto_original:
                self.ui.set_estado("No hay texto", "#e74c3c")
                time.sleep(2)
                self.after(0, self.popup.cerrar)
                return

            # Obtenemos los valores de la UI
            tono = self.ui.combo_tono.get()
            idioma = self.ui.combo_idioma.get()

            self.ui.set_estado("Escribiendo...", "#3498db")

            try:
                for chunk in corregir_texto_ia_stream(texto_original, tono, idioma):
                    self.teclado.type(chunk)
                    time.sleep(0.005)
            except Exception as ia_error:
                raise Exception(f"Error IA: {str(ia_error)}")

            self.ui.set_estado("Completado", "#2ecc71")
            self.after(0, lambda: self.popup.actualizar("¡Listo!"))
            
            time.sleep(1)
            self.after(0, self.popup.cerrar)

        except Exception as e:
            self.ui.set_estado(f"Error: {str(e)}", "#e74c3c")
            self.after(0, lambda: self.popup.mostrar(f"Error: {str(e)[:20]}..."))
            time.sleep(3)
            self.after(0, self.popup.cerrar)
        finally:
            if portapapeles_previso is not None:
                time.sleep(0.1)
                pyperclip.copy(portapapeles_previso)
                
            self.procesando = False