import customtkinter as ctk
import pyperclip
import pyautogui
import threading
import time
import platform

from pynput import keyboard
from google import genai

# =========================================================
# CONFIG
# =========================================================

API_KEY = "AIzaSyAovAz2RSv6MkBciK7-6vyG8N3d-fC5n9s"

client = genai.Client(api_key=API_KEY)

OS_NAME = platform.system()

CMD_KEY = "command" if OS_NAME == "Darwin" else "ctrl"

# evita múltiples ejecuciones simultáneas
procesando = False

# pyautogui optimización
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

# popup global
popup = None
popup_label = None

# =========================================================
# POPUP FLOTANTE
# =========================================================

def mostrar_popup(texto="✍️ Corrigiendo..."):

    global popup
    global popup_label

    cerrar_popup()

    popup = ctk.CTkToplevel(app)

    # no mostrar barra ventana
    popup.overrideredirect(True)

    # siempre arriba
    popup.attributes("-topmost", True)

    # transparencia
    popup.attributes("-alpha", 0.96)

    # color
    popup.configure(fg_color="#1E1E1E")

    # posición cerca cursor
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


# =========================================================
# UI STATUS
# =========================================================

def set_estado(texto, color="gray"):

    app.after(
        0,
        lambda: lbl_estado.configure(
            text=texto,
            text_color=color
        )
    )


# =========================================================
# GEMINI
# =========================================================
def corregir_texto_ia(texto, tono, idioma):

    prompt = f"""Corrige el texto manteniendo significado. Idioma: {idioma} Tono: {tono} Devuelve SOLO el texto final. Texto:{texto}"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text.strip()

# =========================================================
# COPIAR TEXTO SELECCIONADO
# =========================================================

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


# =========================================================
# REEMPLAZAR TEXTO
# =========================================================

def reemplazar_texto(texto):

    pyperclip.copy(texto)

    time.sleep(0.05)

    # reemplaza la selección actual
    pyautogui.hotkey(CMD_KEY, "v")


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def ejecutar_correccion():

    global procesando

    if procesando:
        return

    procesando = True

    try:

        # -------------------------------------------------
        # liberar teclas modificadoras
        # -------------------------------------------------

        pyautogui.keyUp("shift")
        pyautogui.keyUp("ctrl")
        pyautogui.keyUp("alt")
        pyautogui.keyUp("command")

        # -------------------------------------------------
        # popup
        # -------------------------------------------------

        app.after(
            0,
            lambda: mostrar_popup("📋 Copiando texto...")
        )

        set_estado(
            "📋 Copiando texto...",
            "#3498db"
        )

        # -------------------------------------------------
        # copiar selección
        # -------------------------------------------------

        texto_original = copiar_texto_seleccionado()

        if not texto_original:

            app.after(
                0,
                lambda: actualizar_popup("❌ No hay texto seleccionado")
            )

            set_estado(
                "❌ No hay texto seleccionado",
                "#e74c3c"
            )

            time.sleep(2)

            app.after(0, cerrar_popup)

            return

        # -------------------------------------------------
        # obtener settings
        # -------------------------------------------------

        tono = combo_tono.get()
        idioma = combo_idioma.get()

        # -------------------------------------------------
        # popup IA
        # -------------------------------------------------

        app.after(
            0,
            lambda: actualizar_popup("🧠 Corrigiendo texto...")
        )

        set_estado(
            "🧠 Corrigiendo texto...",
            "#3498db"
        )

        # -------------------------------------------------
        # IA
        # -------------------------------------------------

        texto_corregido = corregir_texto_ia(
            texto_original,
            tono,
            idioma
        )

        if not texto_corregido:

            app.after(
                0,
                lambda: actualizar_popup("❌ Error generando texto")
            )

            set_estado(
                "❌ Error generando texto",
                "#e74c3c"
            )

            time.sleep(2)

            app.after(0, cerrar_popup)

            return

        # -------------------------------------------------
        # reemplazar texto
        # -------------------------------------------------

        app.after(
            0,
            lambda: actualizar_popup("✨ Aplicando cambios...")
        )

        set_estado(
            "✨ Aplicando cambios...",
            "#3498db"
        )

        reemplazar_texto(texto_corregido)

        # -------------------------------------------------
        # éxito
        # -------------------------------------------------

        app.after(
            0,
            lambda: actualizar_popup("✅ Texto corregido")
        )

        set_estado(
            "✅ Texto corregido",
            "#2ecc71"
        )

        time.sleep(1)

        app.after(0, cerrar_popup)

    except Exception as e:

        app.after(
            0,
            lambda: mostrar_popup(f"❌ {str(e)}")
        )

        set_estado(
            f"❌ Error: {str(e)}",
            "#e74c3c"
        )

        time.sleep(3)

        app.after(0, cerrar_popup)

    finally:

        procesando = False

        app.after(
            3000,
            lambda: lbl_estado.configure(
                text="Esperando atajo...",
                text_color="gray"
            )
        )


# =========================================================
# HOTKEY
# =========================================================

def al_pulsar_atajo():

    threading.Thread(
        target=ejecutar_correccion,
        daemon=True,
        name="AI-CORRECTOR"
    ).start()


atajo_teclado = (
    "<cmd>+<shift>+k"
    if OS_NAME == "Darwin"
    else "<ctrl>+<shift>+k"
)

listener = keyboard.GlobalHotKeys({
    atajo_teclado: al_pulsar_atajo
})

listener.start()


# =========================================================
# UI
# =========================================================

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("AI QUICK FIX")

app.geometry("360x380")

app.attributes("-topmost", True)

# =========================================================
# TÍTULO
# =========================================================

titulo = ctk.CTkLabel(
    app,
    text="✨ AI QUICK FIX",
    font=("Helvetica", 22, "bold")
)

titulo.pack(pady=20)

# =========================================================
# TONO
# =========================================================

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

# =========================================================
# IDIOMA
# =========================================================

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

# =========================================================
# INFO ATAJO
# =========================================================

atajo_texto = (
    "Cmd + Shift + K"
    if OS_NAME == "Darwin"
    else "Ctrl + Shift + K"
)

info = ctk.CTkLabel(
    app,
    text=f"Selecciona texto en cualquier app\ny pulsa:\n{atajo_texto}",
    text_color="gray",
    font=("Helvetica", 12)
)

info.pack(pady=20)

# =========================================================
# ESTADO
# =========================================================

lbl_estado = ctk.CTkLabel(
    app,
    text="Esperando atajo...",
    text_color="gray",
    font=("Helvetica", 12, "bold")
)

lbl_estado.pack(pady=10)

# =========================================================
# START
# =========================================================

app.mainloop()