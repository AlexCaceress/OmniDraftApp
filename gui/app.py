import uuid

import customtkinter as ctk
import threading
import time
import pyautogui
import pyperclip
import requests
import threading
from config.settings import MI_COLOR_HOVER, OS_NAME
from config.settings import obtener_ruta_recurso
from gui.config_popup import ConfigPopup
from gui.ui_builder import InterfazUsuario
from gui.tray import GestorBandeja
from gui.popup import PopupManager
from ia.corrector import corregir_texto_ia_stream
from utils.clipboard import copiar_texto_seleccionado
from hotkeys.listener import iniciar_listener
from pynput.keyboard import Controller, Key
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from utils.config_manager import cargar_config, guardar_config
from gui.tutorial import VentanaTutorial
from utils.logger import SupabaseLogger

class OmniDraftApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config = cargar_config()

        self.title("OmniDraft")
        self.geometry("380x550")        
        self.attributes("-topmost", True)      
        ruta_icono = obtener_ruta_recurso("assets/icon.ico")
        self.iconbitmap(ruta_icono) 

        self.procesando = False
        self.cancelar_escritura = False
        self.teclado = Controller()

        self.popup = PopupManager(self)
        self.ui = InterfazUsuario(self, callback_atajo=self._cambiar_atajo,)
        self.tray = GestorBandeja(self)
        self.logger = SupabaseLogger(self.config["user_id"])
        self.logger.enviar_log("App Iniciada")

        self.ui.combo_tono.set(self.config["tono"])
        self.ui.combo_idioma.set(self.config["idioma"])
        self.ui.combo_mod.set(self.config["atajo_mod"])
        self.ui.combo_letra.set(self.config["atajo_tecla"])

        self._cambiar_atajo()

        if not self.config.get("tutorial_visto", False):
         self.after(500, self.mostrar_tutorial)

        self.ui.combo_tono.configure(command=self._guardar_configuracion)
        self.ui.combo_idioma.configure(command=self._guardar_configuracion)

        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.bind("<Unmap>", self.tray.al_minimizar)

    def abrir_ajustes(self):
        ConfigPopup(self)

    def mostrar_tutorial(self):
     def al_terminar_tutorial():
         self.config["tutorial_visto"] = True
         guardar_config(self.config)

     VentanaTutorial(self, on_completado=al_terminar_tutorial)

    def _guardar_configuracion(self, valor_seleccionado=None):
        nueva_config = {
            "tono": self.ui.combo_tono.get(),
            "idioma": self.ui.combo_idioma.get(),
            "atajo_mod": self.ui.combo_mod.get(),
            "atajo_tecla": self.ui.combo_letra.get(),
            "tutorial_visto": self.config.get("tutorial_visto", False),
            "user_id": self.config.get("user_id", str(uuid.uuid4())),
            "custom_api_key": self.config.get("custom_api_key", "")
        }
        guardar_config(nueva_config)
        self.config = nueva_config

    def _cambiar_atajo(self, *args):
        modificador = self.ui.combo_mod.get()
        letra = self.ui.combo_letra.get().lower()
        diccionario_mods = {
            "Ctrl + Shift": "<ctrl>+<shift>",
            "Ctrl + Alt": "<ctrl>+<alt>",
            "Alt + Shift": "<alt>+<shift>"
        }
        atajo_pynput = f"{diccionario_mods[modificador]}+{letra}"
        self.ui.atajo.configure(text=f"{modificador} + {letra.upper()}")
        
        iniciar_listener(atajo_pynput, self._al_pulsar_atajo)
        self._guardar_configuracion()

    def _al_pulsar_atajo(self):
        self.logger.enviar_log("Atajo Pulsado")
        threading.Thread(target=self._ejecutar_correccion, daemon=True).start()

    def detectar_escape(self, tecla):
        if tecla == Key.esc:
            self.cancelar_escritura = True
            self.logger.enviar_log("Cancelado por Usuario (ESC)")
            self.ui.set_estado("Cancelado (Tecla ESC)", "#e74c3c")
            self.after(0, lambda: self.popup.actualizar("Cancelado"))
            return False
        
    def detectar_clics(self, x, y, boton, presionado):
        if presionado:
            self.cancelar_escritura = True
            self.logger.enviar_log("Cancelado por Usuari (Clic)")
            self.ui.set_estado("Cancelado (Clic detectado)", "#e74c3c")
            self.after(0, lambda: self.popup.actualizar("Cancelado"))
            return False

    def _ejecutar_correccion(self):
        if self.procesando: return
        self.procesando = True

        portapapeles_previso = pyperclip.paste()
        
        try:
            time.sleep(0.2)
            pyautogui.keyUp("shift")
            pyautogui.keyUp("ctrl")
            if OS_NAME == "Darwin": pyautogui.keyUp("command")

            self.after(0, lambda: self.popup.mostrar("Typing..."))
            texto_original = copiar_texto_seleccionado()
            
            if not texto_original or len(texto_original.strip()) < 2:
                self.ui.set_estado("Invalid text", "#e74c3c")
                self.after(0, lambda: self.popup.mostrar("Invalid text"))
                time.sleep(2)
                self.after(0, self.popup.cerrar)
                return

            tono = self.ui.combo_tono.get()
            idioma = self.ui.combo_idioma.get()
            key_usuario = self.config.get("custom_api_key", "")

            self.ui.set_estado("Typing...", MI_COLOR_HOVER)
            self.after(0, lambda: self.popup.actualizar("Typing... (Esc to cancel)"))

            self.cancelar_escritura = False

            try:
                with KeyboardListener(on_press=self.detectar_escape) as k_listener, \
                     MouseListener(on_click=self.detectar_clics) as m_listener:
                    
                    for chunk in corregir_texto_ia_stream(texto_original, tono, idioma, key_usuario):
                                         
                        if self.cancelar_escritura: 
                            break
                              
                        for letra in chunk:
                            if self.cancelar_escritura:
                                break
                            
                            if letra == '\r':
                                continue
                            
                            if letra == ' ':
                                self.teclado.press(Key.space)
                                self.teclado.release(Key.space)
                            
                            elif letra == '¶' or letra == '\n':
                                self.teclado.press(Key.shift)
                                self.teclado.press(Key.enter)
                                self.teclado.release(Key.enter)
                                self.teclado.release(Key.shift)
                                
                            elif letra == '\t':
                                self.teclado.press(Key.tab)
                                self.teclado.release(Key.tab)
                            else:
                                self.teclado.type(letra)
                            
                            time.sleep(0.020)
                        
            except Exception as ia_error:
                if not self.cancelar_escritura:
                    raise Exception(f"AI Error: {str(ia_error)}")

            if not self.cancelar_escritura:
                self.logger.enviar_log("Texto Completado")
                self.ui.set_estado("Completed", "#2ecc71")
                self.after(0, lambda: self.popup.actualizar("Done!"))
                time.sleep(1)
            else:
                time.sleep(0.3)

        except Exception as e:
            error_msg = str(e).lower()
            error_type = type(e).__name__.lower()
            usando_clave_propia = bool(self.config.get("custom_api_key", "").strip())

            match error_msg:
                
                case msg if any(k in msg or k in error_type for k in ["getaddrinfo", "resolv", "connect", "network", "host", "unreachable", "timeout"]):
                    mensaje_amigable = "No Internet connection"

                case msg if any(k in msg for k in ["400", "401", "403", "api key", "unauthorized", "invalid"]):
                    if usando_clave_propia:
                        mensaje_amigable = "Invalid Custom API Key. Please check your settings."
                    else:
                        mensaje_amigable = "Servers saturated. Update the app, or add your own API Key in Settings to continue normally."
                
                case msg if any(k in msg for k in ["429", "quota", "exhausted", "too many requests"]):
                    if usando_clave_propia:
                        mensaje_amigable = "Your API Key quota reached. Check Google AI Studio."
                    else:
                        mensaje_amigable = "App usage limit reached. Add your own API Key in Settings."

                case _:
                    mensaje_amigable = "Error running the model, please try again later."

            print(f"Error al ejecutar el modelo: {error_msg} + {error_type}")
            self.logger.enviar_log("Error de IA")
            self.ui.set_estado(mensaje_amigable, "#e74c3c")
            self.after(0, lambda m=mensaje_amigable: self.popup.mostrar(m))
            time.sleep(3)
            self.after(0, self.popup.cerrar)

        finally:
            if portapapeles_previso is not None:
                time.sleep(0.1)
                pyperclip.copy(portapapeles_previso)

            self.ui.set_estado("Waiting for shortcut...")
            self.after(0, self.popup.cerrar)

            self.procesando = False
