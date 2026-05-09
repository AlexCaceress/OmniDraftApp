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

listener = keyboard.GlobalHotKeys({
    atajo_teclado: al_pulsar_atajo
})

listener.start()

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

combo_tono = ctk.CTkComboBox(
    app,
    values=[
        "Profesional",
        "Formal",
        "Informal",
        "Amigable",
        "Persuasivo"
    ],
    width=220
)

combo_tono.set("Profesional")
combo_tono.pack(pady=10)

ctk.CTkLabel(
    app,
    text="Idioma:"
).pack()

combo_idioma = ctk.CTkComboBox(
    app,
    values=[
        "Español",
        "Inglés",
        "Francés",
        "Alemán",
        "Italiano"
    ],
    width=220
)

combo_idioma.set("Español")

combo_idioma.pack(pady=10)

atajo_texto = (
    "Cmd + Shift + T"
    if OS_NAME == "Darwin"
    else "Ctrl + Shift + T"
)

info = ctk.CTkLabel(
    app,
    text=f"Selecciona texto en cualquier app\ny pulsa:\n{atajo_texto}",
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
app.mainloop()