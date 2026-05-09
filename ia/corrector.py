# Lógica de interacción con la IA
from google import genai
from config.settings import API_KEY

client = genai.Client(api_key=API_KEY)

def corregir_texto_ia_stream(texto, tono, idioma):
	prompt = f"""Corrige el texto manteniendo significado. Idioma: {idioma} Tono: {tono} Devuelve SOLO el texto final. Texto:{texto}"""
	response = client.models.generate_content_stream(
		model="gemini-3.1-flash-lite",
		contents=prompt
	)
	for chunk in response:
		if chunk.text:
			yield chunk.text
