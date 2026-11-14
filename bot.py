import os
import time
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class AsistenteMinecraft:
    def __init__(self, ruta_justificacion='Justificacion del dominio.txt',
                 ruta_conocimiento='conocimiento.pl'):
        from google import genai
        from google.genai import types
        self.types = types
        clave = os.getenv('GEMINI_API_KEY')
        if not GEMINI_API_KEY:
            raise RuntimeError('Configura GEMINI_API_KEY en tu archivo .env')
        self.client = genai.Client(api_key=clave)
        justificacion = (BASE / ruta_justificacion).read_text(encoding='utf-8')
        conocimiento = (BASE / ruta_conocimiento).read_text(encoding='utf-8')
        self.modelo = os.getenv('GEMINI_MODEL','gemini-3.5-flash-lite')
        self.instrucciones_sistema = f"""Eres un chatbot de crafteo de Minecraft.
Responde exclusivamente según la base de conocimiento suministrada.
No inventes cantidades, posiciones de crafteo ni recetas que no estén explícitas.
Distingue recetas directas, sus usos, materiales directos e indirectos y materiales básicos.
Si falta un dato indica que no está en la base. Responde breve y en español.

DOMINIO:\n{justificacion}\n\nBASE PROLOG:\n{conocimiento}"""
        self.historial = []

    def reiniciar(self):
        self.historial = []

    def responder(self, pregunta: str) -> str:
        if not pregunta.strip():
            return 'Escribe una pregunta.'
        contenido = self.historial + [
            self.types.Content(role='user',parts=[self.types.Part.from_text(text=pregunta)])]
        ultimo_error = None
        for intento in range(3):
            try:
                respuesta = self.client.models.generate_content(
                    model=self.modelo, contents=contenido,
                    config=self.types.GenerateContentConfig(
                        system_instruction=self.instrucciones_sistema, temperature=0.1))
                texto = (respuesta.text or '').strip()
                if not texto:
                    return '[Error] El modelo no devolvió texto.'
                self.historial = contenido + [self.types.Content(
                    role='model',parts=[self.types.Part.from_text(text=texto)])]
                return texto
            except Exception as exc:
                ultimo_error = str(exc)
                if '429' in ultimo_error or '503' in ultimo_error:
                    if intento < 2:
                        time.sleep(2 * (intento + 1))
                        continue
                break
        return '[Error de Gemini] ' + str(ultimo_error)