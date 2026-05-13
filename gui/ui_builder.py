import customtkinter as ctk
from config.settings import MI_COLOR_FONDO, MI_COLOR_HOVER

class InterfazUsuario:
    def __init__(self, app, callback_atajo):
        self.app = app
        self.callback_atajo = callback_atajo
        self.construir_ui()

    def construir_ui(self):
        # 1. Cabecera elegante
        ctk.CTkLabel(
            self.app, 
            text="OmniDraft", 
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(25, 5))
        
        ctk.CTkLabel(
            self.app, 
            text="Correction settings", 
            font=("Segoe UI", 13), 
            text_color="#888888"
        ).pack(pady=(0, 15))

        tarjeta = ctk.CTkFrame(self.app, fg_color="#2B2B2B", corner_radius=12)
        tarjeta.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(tarjeta, text="Tone:", font=("Segoe UI", 13, "bold")).pack(pady=(20, 5))
        
        self.combo_tono = ctk.CTkOptionMenu(
            tarjeta, values=["Professional", "Casual", "Academic", "Friendly", "Concise"], width=220,
            fg_color=MI_COLOR_FONDO, button_color=MI_COLOR_FONDO, button_hover_color=MI_COLOR_HOVER
        )
        self.combo_tono.set("Professional")
        self.combo_tono.pack(pady=(0, 15))

        ctk.CTkLabel(tarjeta, text="Language:", font=("Segoe UI", 13, "bold")).pack(pady=(0, 5))
        
        self.combo_idioma = ctk.CTkOptionMenu(
            tarjeta, values=["Spanish", "English", "French", "German", "Italian", "Catalan"], width=220,
            fg_color=MI_COLOR_FONDO, button_color=MI_COLOR_FONDO, button_hover_color=MI_COLOR_HOVER
        )
        self.combo_idioma.set("Spanish")
        self.combo_idioma.pack(pady=(0, 15))

        ctk.CTkLabel(tarjeta, text="Keyboard shortcut:", font=("Segoe UI", 13, "bold")).pack(pady=(0, 5))
        
        frame_atajo = ctk.CTkFrame(tarjeta, fg_color="transparent")
        frame_atajo.pack(pady=(0, 35)) 

        self.combo_mod = ctk.CTkOptionMenu(
            frame_atajo, values=["Ctrl + Shift", "Ctrl + Alt", "Alt + Shift"], 
            width=140, 
            command=self.callback_atajo,
            fg_color=MI_COLOR_FONDO, button_color=MI_COLOR_FONDO, button_hover_color=MI_COLOR_HOVER
        )
        self.combo_mod.pack(side="left", padx=(0, 10)) 

        self.combo_letra = ctk.CTkOptionMenu(
            frame_atajo, values=[chr(i) for i in range(65, 91)], 
            width=70,
            command=self.callback_atajo,
            fg_color=MI_COLOR_FONDO, button_color=MI_COLOR_FONDO, button_hover_color=MI_COLOR_HOVER
        )
        self.combo_letra.pack(side="left", padx=0)

        self.info = ctk.CTkLabel(self.app, text="Select any text and press:", text_color="gray", font=("Segoe UI", 13))
        self.info.pack(pady=(20, 0))

        self.atajo = ctk.CTkLabel(self.app, text_color=MI_COLOR_HOVER, font=("Segoe UI", 14, "bold"))
        self.atajo.pack(pady=2)

        self.lbl_estado = ctk.CTkLabel(
            self.app, 
            text="Waiting for shortcut...",
            font=("Segoe UI", 12),
            wraplength=300 
        )
        self.lbl_estado.pack(pady=5)

    def set_estado(self, texto, color="white"):
        self.app.after(0, lambda: self.lbl_estado.configure(text=texto, text_color=color))