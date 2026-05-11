import customtkinter as ctk
from config.settings import MI_COLOR_FONDO, MI_COLOR_HOVER

class InterfazUsuario:
    def __init__(self, app, callback_atajo):
        self.app = app
        self.callback_atajo = callback_atajo
        self.construir_ui()

    def construir_ui(self):
        ctk.CTkLabel(self.app, text="OmniDraft", font=("Helvetica", 22, "bold")).pack(pady=20)

        # Tono
        ctk.CTkLabel(self.app, text="Tono:").pack()
        self.combo_tono = ctk.CTkOptionMenu(
            self.app, values=["Formal", "Informal", "Profesional"], width=220,
            fg_color=MI_COLOR_FONDO, button_color=MI_COLOR_FONDO, button_hover_color=MI_COLOR_HOVER
        )
        self.combo_tono.set("Profesional")
        self.combo_tono.pack(pady=10)

        # Idioma
        ctk.CTkLabel(self.app, text="Idioma:").pack()
        self.combo_idioma = ctk.CTkOptionMenu(
            self.app, values=["Español", "Inglés", "Francés", "Alemán", "Italiano", "Catalan"], width=220,
            fg_color=MI_COLOR_FONDO, button_color=MI_COLOR_FONDO, button_hover_color=MI_COLOR_HOVER
        )
        self.combo_idioma.set("Español")
        self.combo_idioma.pack(pady=10)

        # Atajo
        ctk.CTkLabel(self.app, text="Atajo de teclado:").pack(pady=(10, 0))
        frame_atajo = ctk.CTkFrame(self.app, fg_color="transparent")
        frame_atajo.pack(pady=5)

        self.combo_mod = ctk.CTkOptionMenu(
            frame_atajo, values=["Ctrl + Shift", "Ctrl + Alt", "Alt + Shift"], width=120,
            command=self.callback_atajo, # Avisamos a la app principal
            fg_color=MI_COLOR_FONDO, button_color=MI_COLOR_FONDO, button_hover_color=MI_COLOR_HOVER
        )
        self.combo_mod.set("Ctrl + Shift")
        self.combo_mod.pack(side="left", padx=5)

        self.combo_letra = ctk.CTkOptionMenu(
            frame_atajo, values=[chr(i) for i in range(65, 91)], width=70,
            command=self.callback_atajo, # Avisamos a la app principal
            fg_color=MI_COLOR_FONDO, button_color=MI_COLOR_FONDO, button_hover_color=MI_COLOR_HOVER
        )
        self.combo_letra.set("K")
        self.combo_letra.pack(side="left", padx=5)

        self.label_api = ctk.CTkLabel(self.app, text="API Key del corrector:")
        self.label_api.pack(pady=(10, 0))

        self.entry_api = ctk.CTkEntry(
            self.app, 
            width=220, 
            placeholder_text="Pega tu clave aquí...", 
            show="*",
            justify="center"
        )
        self.entry_api.pack(pady=5)
        
        self.btn_ayuda = ctk.CTkButton(
            self.app, 
            text="¿Cómo conseguir una?", 
            width=120, 
            height=20,
            fg_color="transparent", 
            text_color="#3498db",
            hover_color="#2c3e50",
            command=lambda: __import__('webbrowser').open("https://aistudio.google.com/app/apikey")
        )
        self.btn_ayuda.pack(pady=(0, 10))

        # Textos informativos
        self.info = ctk.CTkLabel(self.app, text_color="gray", font=("Helvetica", 12))
        self.info.pack(pady=(10,5))
        self.lbl_estado = ctk.CTkLabel(self.app, text="Esperando atajo...", text_color="gray", font=("Helvetica", 12, "bold"))
        self.lbl_estado.pack(pady=(0, 10))

    def set_estado(self, texto, color="gray"):
        self.app.after(0, lambda: self.lbl_estado.configure(text=texto, text_color=color))