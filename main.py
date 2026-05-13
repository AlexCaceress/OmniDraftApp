import sys
import ctypes
import customtkinter as ctk
from gui.app import OmniDraftApp

def asegurar_instancia_unica():
    nombre_mutex = "OmniDraft_Mutex"
    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, False, nombre_mutex)    
    ultimo_error = kernel32.GetLastError()
    
    if ultimo_error == 183:
        sys.exit(0)
        
    return mutex

if __name__ == "__main__":
    mutex_proteccion = asegurar_instancia_unica()
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = OmniDraftApp()
    app.mainloop()