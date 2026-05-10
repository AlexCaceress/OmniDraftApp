import customtkinter as ctk
import pyautogui

class PopupManager:
    def __init__(self, app):
        self.app = app
        self.window = None
        self.label = None

    def mostrar(self, texto):
        # Asegurarnos de que no hay uno abierto antes de crear otro
        self.cerrar()

        self.window = ctk.CTkToplevel(self.app)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.96)
        self.window.configure(fg_color="#1E1E1E")
        
        # Posicionar junto al ratón
        x, y = pyautogui.position()
        self.window.geometry(f"260x60+{x+20}+{y+20}")

        self.label = ctk.CTkLabel(
            self.window,
            text=texto,
            font=("Helvetica", 14, "bold")
        )
        self.label.pack(expand=True, fill="both", padx=20, pady=10)
        
        self.window.update()

    def actualizar(self, texto):
        if self.label and self.window:
            self.label.configure(text=texto)
            self.label.update()

    def cerrar(self):
        try:
            if self.window:
                self.window.destroy()
        except Exception:
            pass
        finally:
            self.window = None
            self.label = None