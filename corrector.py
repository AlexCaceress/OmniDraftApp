import customtkinter as ctk
import pyperclip
import pyautogui
import threading
import time
import platform
import os

from pynput import keyboard
from pynput.keyboard import Controller, GlobalHotKeys
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

print(API_KEY)

client = genai.Client(api_key=API_KEY)

OS_NAME = platform.system()

CMD_KEY = "command" if OS_NAME == "Darwin" else "ctrl"

procesando = False

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

popup = None
popup_label = None

teclado = Controller()

listener_actual = None

MI_COLOR_FONDO = "#343638"
MI_COLOR_HOVER = "#2FA572"

def iniciar_listener(atajo_pynput):
    global listener_actual
    
    if listener_actual is not None:
        listener_actual.stop()
        
    listener_actual = keyboard.GlobalHotKeys({atajo_pynput: al_pulsar_atajo})
    listener_actual.start()

def cambiar_atajo(*args):
    modificador = combo_mod.get()
    letra = combo_letra.get().lower()
    
    diccionario_mods = {
        "Ctrl + Shift": "<ctrl>+<shift>",
        "Ctrl + Alt": "<ctrl>+<alt>",
        "Alt + Shift": "<alt>+<shift>"
    }
    
    atajo_pynput = f"{diccionario_mods[modificador]}+{letra}"
    
    info.configure(text=f"Selecciona texto en cualquier app\ny pulsa:\n{modificador} + {letra.upper()}")
    
    iniciar_listener(atajo_pynput)


def mostrar_popup(texto="✍️ Corrigiendo..."):

    global popup
    global popup_label

    cerrar_popup()

    popup = ctk.CTkToplevel(app)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.attributes("-alpha", 0.96)
    popup.configure(fg_color="#1E1E1E")
    x, y = pyautogui.position()

    popup.geometry(f"260x60+{x+20}+{y+20}")

    popup_label = ctk.CTkLabel(
        popup,
        text=texto,
        font=("Helvetica", 14, "bold")
    )

    popup_label.pack(
        expand=True,
        fill="both",
        padx=20,
        pady=10
    )

    popup.update()

def actualizar_popup(texto):

    global popup_label

    if popup_label:

        popup_label.configure(text=texto)

        popup_label.update()


def cerrar_popup():

    global popup
    global popup_label

    try:
        if popup:
            popup.destroy()
    except:
        pass

    popup = None
    popup_label = None


def set_estado(texto, color="gray"):

    app.after(
        0,
        lambda: lbl_estado.configure(
            text=texto,
            text_color=color
        )
    )


def corregir_texto_ia_stream(texto, tono, idioma):
    prompt = f"""Corrige el texto manteniendo significado. Idioma: {idioma} Tono: {tono} Devuelve SOLO el texto final. Texto:{texto}"""

    response = client.models.generate_content_stream(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text


def copiar_texto_seleccionado():

    pyperclip.copy("")

    pyautogui.hotkey(CMD_KEY, "c")

    # esperar clipboard
    for _ in range(20):

        time.sleep(0.05)

        texto = pyperclip.paste()

        if texto and not texto.isspace():
            return texto

    return None


def reemplazar_texto(texto):

    pyperclip.copy(texto)

    time.sleep(0.05)

    pyautogui.hotkey(CMD_KEY, "v")


def ejecutar_correccion():

    global procesando

    if procesando:
        return

    procesando = True

    try:
        time.sleep(0.2) 
        pyautogui.keyUp("shift")
        pyautogui.keyUp("ctrl")
        
        if OS_NAME == "Darwin":
            pyautogui.keyUp("command")

        app.after(
            0,
            lambda: mostrar_popup("Copiando texto...")
        )

        texto_original = copiar_texto_seleccionado()

        if not texto_original:

            app.after(
                0,
                lambda: actualizar_popup("No hay texto seleccionado")
            )

            set_estado(
                "No hay texto seleccionado",
                "#e74c3c"
            )

            time.sleep(2)

            app.after(0, cerrar_popup)

            return
        
        tono = combo_tono.get()
        idioma = combo_idioma.get()

        app.after(
            0,
            lambda: actualizar_popup("Escribiendo...")
        )

        set_estado(
            "Escribiendo en tiempo real...",
            "#3498db"
        )

        # Iteramos sobre los pedazos de texto que llegan en vivo
        try:
            for chunk in corregir_texto_ia_stream(texto_original, tono, idioma):
                # Escribimos el pedazo de texto como si fuéramos un humano muy rápido
                teclado.type(chunk)
                time.sleep(0.005) # Micropausa para no saturar el buffer del SO
        except Exception as ia_error:
            raise Exception(f"Error de IA: {str(ia_error)}")

        app.after(
            0,
            lambda: actualizar_popup("¡Listo!")
        )

        set_estado(
            "Texto corregido",
            "#2ecc71"
        )

        time.sleep(1)
        app.after(0, cerrar_popup)

    except Exception as e:

        app.after(
            0,
            lambda: mostrar_popup(f"{str(e)}")
        )

        set_estado(
            f"Error: {str(e)}",
            "#e74c3c"
        )

        time.sleep(3)
        app.after(0, cerrar_popup)

    finally:
        procesando = False


def al_pulsar_atajo():

    threading.Thread(
        target=ejecutar_correccion,
        daemon=True,
        name="AI-CORRECTOR"
    ).start()

atajo_teclado = (
    "<cmd>+<shift>+t"
    if OS_NAME == "Darwin"
    else "<ctrl>+<shift>+t"
)

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("AI QUICK FIX")

app.geometry("360x380")

app.attributes("-topmost", True)

titulo = ctk.CTkLabel(
    app,
    text="✨ AI QUICK FIX",
    font=("Helvetica", 22, "bold")
)

titulo.pack(pady=20)

ctk.CTkLabel(
    app,
    text="Tono:"
).pack()

combo_tono = ctk.CTkOptionMenu(
    app,
    values=[
        "Formal",
        "Informal",
    ],
    width=220,
    fg_color=MI_COLOR_FONDO,
    button_color=MI_COLOR_FONDO,
    button_hover_color=MI_COLOR_HOVER
)

combo_tono.set("Profesional")
combo_tono.pack(pady=10)

ctk.CTkLabel(
    app,
    text="Idioma:"
).pack()

combo_idioma = ctk.CTkOptionMenu(
    app,
    values=[
        "Español",
        "Inglés",
        "Francés",
        "Alemán",
        "Italiano"
    ],
    width=220,
    fg_color=MI_COLOR_FONDO,
    button_color=MI_COLOR_FONDO,
    button_hover_color=MI_COLOR_HOVER
)

combo_idioma.set("Español")

combo_idioma.pack(pady=10)

ctk.CTkLabel(app, text="Atajo de teclado:").pack(pady=(10, 0))

frame_atajo = ctk.CTkFrame(app, fg_color="transparent")
frame_atajo.pack(pady=5)

combo_mod = ctk.CTkOptionMenu(
    frame_atajo, 
    values=["Ctrl + Shift", "Ctrl + Alt", "Alt + Shift"],
    width=120,
    command=cambiar_atajo,
    fg_color=MI_COLOR_FONDO,
    button_color=MI_COLOR_FONDO,
    button_hover_color=MI_COLOR_HOVER
)
combo_mod.set("Ctrl + Shift")
combo_mod.pack(side="left", padx=5)

combo_letra = ctk.CTkOptionMenu(
    frame_atajo, 
    values=[chr(i) for i in range(65, 91)], 
    width=70,
    command=cambiar_atajo,
    fg_color=MI_COLOR_FONDO,
    button_color=MI_COLOR_FONDO,
    button_hover_color=MI_COLOR_HOVER
)
combo_letra.set("K")
combo_letra.pack(side="left", padx=5)

info = ctk.CTkLabel(
    app,
    text_color="gray",
    font=("Helvetica", 12)
)

info.pack(pady=20)

lbl_estado = ctk.CTkLabel(
    app,
    text="Esperando atajo...",
    text_color="gray",
    font=("Helvetica", 12, "bold")
)

lbl_estado.pack(pady=10)

cambiar_atajo()
app.mainloop()