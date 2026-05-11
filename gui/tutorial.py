import customtkinter as ctk

class VentanaTutorial(ctk.CTkToplevel):
    def __init__(self, master, on_completado):
        super().__init__(master)
        self.title("OmniDraft - Primeros pasos")
        # Un poco más alta para dar espacio a los saltos de línea
        self.geometry("420x400") 
        self.resizable(False, False)
        self.attributes("-topmost", True)
        # Bloquea la ventana principal hasta que se cierre esta
        self.grab_set() 
        
        self.on_completado = on_completado
        
        # Añadimos dobles saltos de línea (\n\n) para que el texto respire y no se vea apelotonado
        self.pasos = [
            {
                "icono": "✨",
                "titulo": "Bienvenido a OmniDraft", 
                "texto": "El asistente de IA que corrige, traduce y mejora tus textos.\n\nActúa directamente donde estés escribiendo, sin necesidad de copiar y pegar en otras ventanas."
            },
            {
                "icono": "⚡",
                "titulo": "Selecciona y Pulsa", 
                "texto": "1. Selecciona texto en cualquier app (Word, Chrome...)\n\n2. Pulsa tu atajo de teclado.\n\n3. OmniDraft lo reescribirá al instante."
            },
            {
                "icono": "🎨",
                "titulo": "Todo a tu gusto", 
                "texto": "Personaliza el tono y el idioma en la ventana principal.\n\nAl minimizar la app, seguirá funcionando en segundo plano minimizada junto al reloj de Windows."
            }
        ]
        self.paso_actual = 0

        self.construir_ui()
        self.actualizar_pantalla()

    def construir_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=20)

        # Icono gigante
        self.lbl_icono = ctk.CTkLabel(self.main_frame, text="", font=("Segoe UI Emoji", 48))
        self.lbl_icono.pack(pady=(10, 10))

        # Título principal
        self.lbl_titulo = ctk.CTkLabel(self.main_frame, font=("Helvetica", 22, "bold"))
        self.lbl_titulo.pack(pady=(0, 20))

        # Texto descriptivo (Aumentamos un poco la fuente y el padding)
        self.lbl_texto = ctk.CTkLabel(
            self.main_frame, 
            font=("Helvetica", 15), 
            text_color="#ced4da", 
            wraplength=340, 
            justify="center"
        )
        self.lbl_texto.pack(pady=5)

        # --- ZONA INFERIOR (Puntos y Botones) ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", side="bottom", padx=25, pady=25)

        # Botón Omitir (Izquierda)
        self.btn_omitir = ctk.CTkButton(
            self.bottom_frame, text="Omitir", width=60, 
            fg_color="transparent", text_color="#6c757d", 
            hover_color="#343a40", font=("Helvetica", 13, "underline"),
            command=self.finalizar
        )
        self.btn_omitir.pack(side="left")

        # Contenedor para botones derechos (Atrás y Siguiente)
        self.right_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.right_frame.pack(side="right")

        # Botón Atrás (Se mostrará u ocultará dinámicamente)
        self.btn_atras = ctk.CTkButton(
            self.right_frame, text="Atrás", width=60, 
            fg_color="transparent", text_color="#ced4da", 
            hover_color="#343a40", font=("Helvetica", 14),
            command=self.anterior
        )
        
        # Botón Siguiente
        self.btn_siguiente = ctk.CTkButton(
            self.right_frame, text="Siguiente ➔", width=110, height=36,
            font=("Helvetica", 14, "bold"),
            command=self.siguiente
        )
        self.btn_siguiente.pack(side="right")

        # Indicador de progreso (Centro)
        self.frame_puntos = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.frame_puntos.pack(side="left", expand=True)
        self.lbl_puntos = ctk.CTkLabel(self.frame_puntos, text="", font=("Helvetica", 18), text_color="#495057")
        self.lbl_puntos.pack()

    def actualizar_pantalla(self):
        datos = self.pasos[self.paso_actual]
        self.lbl_icono.configure(text=datos["icono"])
        self.lbl_titulo.configure(text=datos["titulo"])
        self.lbl_texto.configure(text=datos["texto"])
        
        # Mostrar u ocultar el botón Atrás
        if self.paso_actual > 0:
            self.btn_atras.pack(side="left", padx=(0, 10))
        else:
            self.btn_atras.pack_forget()
        
        # Actualizar los puntos de progreso visualmente
        puntos = ["○"] * len(self.pasos)
        puntos[self.paso_actual] = "●"
        self.lbl_puntos.configure(text=" ".join(puntos))
        
        # Cambiar el estilo del botón si es el último paso
        if self.paso_actual == len(self.pasos) - 1:
            self.btn_siguiente.configure(text="Empezar ✨", fg_color="#2FA572", hover_color="#248259")
        else:
            self.btn_siguiente.configure(text="Siguiente ➔", fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#36719F", "#144870"])

    def anterior(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self.actualizar_pantalla()

    def siguiente(self):
        if self.paso_actual < len(self.pasos) - 1:
            self.paso_actual += 1
            self.actualizar_pantalla()
        else:
            self.finalizar()

    def finalizar(self):
        self.on_completado()
        self.destroy()