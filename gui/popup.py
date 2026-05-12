import customtkinter as ctk

class PopupManager:
    def __init__(self, app):
        self.app = app
        self.window = None

    def mostrar(self, texto):
        self.cerrar()

        self.window = ctk.CTkToplevel(self.app)
        self.window.withdraw()
        self.window.overrideredirect(True)
        self.window.attributes("-toolwindow", True)
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.96)
        
        COLOR_INVISIBLE = "#000001" 
        self.window.configure(fg_color=COLOR_INVISIBLE)
        
        try:
            self.window.wm_attributes("-transparentcolor", COLOR_INVISIBLE)
        except Exception:
            pass

        self.frame = ctk.CTkFrame(
            self.window, 
            fg_color="#2B2B2B", 
            border_color="#3A3A3A",
            border_width=1,
            corner_radius=12
        )
        self.frame.pack(expand=True, fill="both")

        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(5, 0))

        btn_cerrar = ctk.CTkButton(
            header_frame, 
            text="✖", 
            width=25, height=25, 
            fg_color="transparent", 
            text_color="#666666", 
            hover_color="#444444", 
            font=("Segoe UI", 14),
            command=self.cerrar
        )
        btn_cerrar.pack(side="right")

        content_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        self.label_texto = ctk.CTkLabel(
            content_frame,
            text=texto,
            font=("Segoe UI", 14),
            wraplength=400,
            justify="center",
            text_color="#E0E0E0" 
        )
        self.label_texto.pack(fill="both", expand=True)

        self.window.update_idletasks() 
        
        ancho_pantalla = self.window.winfo_screenwidth()
        alto_pantalla = self.window.winfo_screenheight()
        
        ancho_ventana = self.window.winfo_width()
        alto_ventana = self.window.winfo_height()

        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))

        self.window.geometry(f"+{x}+{y}")
        
        self.window.deiconify()
        self.window.update()

    def actualizar(self, texto):
        if self.window and self.window.winfo_exists():
            self.label_texto.configure(text=texto)
            
            self.window.update_idletasks()
            
            ancho_pantalla = self.window.winfo_screenwidth()
            alto_pantalla = self.window.winfo_screenheight()
            ancho_ventana = self.window.winfo_width()
            alto_ventana = self.window.winfo_height()
            
            x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
            y = int((alto_pantalla / 2) - (alto_ventana / 2))
            
            self.window.geometry(f"+{x}+{y}")
            self.window.update()

    def cerrar(self):
        if self.window:
            try:
                self.window.withdraw()
                self.window.destroy()
            except Exception:
                pass
            finally:
                self.window = None