from gui.app import AIQuickFixApp
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = AIQuickFixApp()
    app.mainloop()