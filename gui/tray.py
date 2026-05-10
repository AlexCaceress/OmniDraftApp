import pystray
from PIL import Image, ImageDraw
import threading

class GestorBandeja:
    def __init__(self, app):
        self.app = app

    def crear_icono_dummy(self):
        image = Image.new('RGB', (64, 64), color='#3498db')
        draw = ImageDraw.Draw(image)
        draw.text((15, 20), "AI", fill='white')
        return image

    def mostrar_ventana(self, icon, item):
        icon.stop()
        self.app.after(0, self.app.deiconify)

    def salir_del_programa(self, icon, item):
        icon.stop()
        self.app.quit()

    def ocultar_en_bandeja(self):
        self.app.withdraw() # Ocultamos la ventana

        menu = pystray.Menu(
            pystray.MenuItem('Abrir Panel', self.mostrar_ventana),
            pystray.MenuItem('Salir', self.salir_del_programa)
        )
        
        icono = pystray.Icon("AI_Quick_Fix", self.crear_icono_dummy(), "AI Quick Fix", menu)
        threading.Thread(target=icono.run, daemon=True).start()