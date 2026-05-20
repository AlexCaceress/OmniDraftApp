import webbrowser

import customtkinter as ctk
from config.settings import obtener_ruta_recurso
from utils.config_manager import guardar_config

class ConfigPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.title("Advanced Settings")
        self.geometry("400x250")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        ruta_icono = obtener_ruta_recurso("assets/icon.ico")
        self.after(200, lambda: self.iconbitmap(ruta_icono))
        
        self.grab_set()
        
        self.parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (230 // 2)
        self.geometry(f"400x250+{x}+{y}")
        
        self.construir_ui()
        
    def construir_ui(self):
        ctk.CTkLabel(
            self, 
            text="Personal Gemini API Key", 
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            self, 
            text="Leave blank to use OmniDraft's free quota.\nGet your own key at aistudio.google.com", 
            font=("Segoe UI", 11),
            text_color="gray",
            justify="center"
        ).pack(pady=(0, 15))
        
        self.entry_key = ctk.CTkEntry(
            self, 
            width=320, 
            show="*", 
            placeholder_text="AIzaSy..."
        )

        key_actual = self.parent.config.get("custom_api_key", "")
        self.entry_key.insert(0, key_actual)
        self.entry_key.pack(pady=5)
        
        # Botón Guardar
        btn_guardar = ctk.CTkButton(
            self, 
            text="Save Changes", 
            fg_color="#2FA572", 
            hover_color="#25875d",
            font=("Segoe UI", 13, "bold"),
            command=self.guardar_cambios
        )
        btn_guardar.pack(pady=20)

        link_label = ctk.CTkLabel(
            self,
            text="Get your API key at Google AI Studio",
            font=ctk.CTkFont(family="Segoe UI", size=12, underline=True),
            text_color="#58a6ff",
            cursor="hand2"
        )
        link_label.pack(pady=(0, 10))
        
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://aistudio.google.com/"))
        
    def guardar_cambios(self):
        nueva_key = self.entry_key.get().strip()
        
        self.parent.config["custom_api_key"] = nueva_key
        
        guardar_config(self.parent.config)
        
        self.parent.popup.actualizar("API Key Updated")
        
        self.destroy()