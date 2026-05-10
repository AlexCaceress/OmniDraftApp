import customtkinter as ctk
import threading
import time
import pyautogui
import pyperclip
from config.settings import OS_NAME
from gui.ui_builder import InterfazUsuario
from gui.tray import GestorBandeja
from gui.popup import PopupManager
from ia.corrector import corregir_texto_ia_stream
from utils.clipboard import copiar_texto_seleccionado
from hotkeys.listener import iniciar_listener
from pynput.keyboard import Controller, Listener, Key

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

            if not texto_original or len(texto_original.strip()) < 2:
                self.ui.set_estado("Texto no válido", "#e74c3c")
                self.after(0, lambda: self.popup.mostrar("Texto inválido"))
                time.sleep(2)
                self.after(0, self.popup.cerrar)
                return

            # Obtenemos los valores de la UI
            tono = self.ui.combo_tono.get()
            idioma = self.ui.combo_idioma.get()

            self.ui.set_estado("Escribiendo...", "#3498db")
            self.after(0, lambda: self.popup.actualizar("Escribiendo... (Esc para cancelar)"))

            self.cancelar_escritura = False

            def detectar_escape(tecla):
                if tecla == Key.esc:
                    self.cancelar_escritura = True
                    self.ui.set_estado("Cancelado por el usuario", "#e74c3c")
                    self.after(0, lambda: self.popup.actualizar("Cancelado"))
                    return False # Esto apaga el listener de pynput

            try:
                # Envolvemos la escritura en un Listener temporal que escucha el teclado
                with Listener(on_press=detectar_escape) as listener:
                    for chunk in corregir_texto_ia_stream(texto_original, tono, idioma):
                        
                        # Si el usuario pulsó Escape, rompemos el bucle al instante
                        if self.cancelar_escritura:
                            break 
                        
                        self.teclado.type(chunk)
                        time.sleep(0.005)
                        
            except Exception as ia_error:
                if not self.cancelar_escritura:
                    raise Exception(f"Error IA: {str(ia_error)}")

            if not self.cancelar_escritura:
                self.ui.set_estado("Completado", "#2ecc71")
                self.after(0, lambda: self.popup.actualizar("¡Listo!"))
                time.sleep(1)
            else:
                time.sleep(0.3) 
            
            self.after(0, self.popup.cerrar)

        except Exception as e:
            error_msg = str(e).lower()
            error_type = type(e).__name__.lower() # Capturamos también el tipo de error

            match error_msg:
                
                # 1. Errores de Conexión y DNS (Añadimos las palabras reales de fallo de red)
                case msg if any(k in msg or k in error_type for k in ["getaddrinfo", "resolv", "connect", "network", "host", "unreachable", "timeout"]):
                    mensaje_amigable = "Sin conexión a Internet"

                # 2. Errores de API Key (Añadimos 401 y 403, que son los de "No autorizado")
                case msg if any(k in msg for k in ["400", "401", "403", "api key", "unauthorized", "invalid"]):
                    mensaje_amigable = "Problema con la API Key"

                # 3. Límite de uso (Añadimos "too many requests")
                case msg if any(k in msg for k in ["429", "quota", "exhausted", "too many requests"]):
                    mensaje_amigable = "Límite de uso de IA alcanzado"

                # 4. Caso por defecto
                case _:
                    mensaje_amigable = "Error temporal de la IA"

            # Actualizamos la interfaz
            self.ui.set_estado(mensaje_amigable, "#e74c3c")
            self.after(0, lambda m=mensaje_amigable: self.popup.mostrar(m))
            time.sleep(3)
            self.after(0, self.popup.cerrar)

        finally:
            if portapapeles_previso is not None:
                time.sleep(0.1)
                pyperclip.copy(portapapeles_previso)

            self.procesando = False