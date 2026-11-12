import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def cargar_archivo(ruta: str) -> str:
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()

class AsistenteMinecraft:
    def __init__(self, ruta_justificacion: str, ruta_conocimiento: str):
        justificacion = cargar_archivo(ruta_justificacion)
        base_prolog = cargar_archivo(ruta_conocimiento)

        self.instrucciones_sistema = f"""
Eres un chatbot experto en el sistema de crafteo de Minecraft diseñado para contrastar inferencia lógica contra un sistema en Prolog.

CONTEXTO DEL PROYECTO:
{justificacion}

BASE DE CONOCIMIENTO ESTRICTA (HECHOS Y REGLAS):
{base_prolog}

REGLAS DE RESPUESTA OBLIGATORIAS:
1. Responde ÚNICAMENTE usando los hechos, recetas, usos y reglas de inferencia definidos en la BASE DE CONOCIMIENTO ESTRICTA anterior.
2. Si el usuario pregunta por un objeto, material o receta que NO está en la base de conocimiento (por ejemplo: oro, netherita, armaduras, cantidades exactas de bloques), indica explícitamente que ese elemento no forma parte de la base de conocimiento del proyecto.
3. Puedes responder tres tipos de consultas principales (tanto en formato lenguaje natural como con nombres de átomos como 'pico_hierro'):
   - Recetas directas: qué ingredientes directos requiere un objeto (`receta`).
   - Utilidad / Uso: para qué sirve un objeto o herramienta (`uso`).
   - Cadena de prerequisitos: todos los materiales directos e indirectos necesarios en la cadena de crafteo (`requiere_material`, por ejemplo: pico_hierro requiere palo, hierro y madera).
4. Responde en español, de forma clara, precisa y directa.
"""
        self.client = genai.Client()
        # Lista de modelos en orden de prioridad: si uno devuelve 503, pasa al siguiente
        self.modelos_disponibles = [
            "gemini-3.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-3.8-flash",
        ]
        self.historial = []

    def responder(self, mensaje_usuario: str) -> str:
        # Agregamos el turno actual al historial manualmente para conservarlo entre cambios de modelo
        contenido_actual = self.historial + [
            types.Content(role="user", parts=[types.Part.from_text(text=mensaje_usuario)])
        ]

        for modelo in self.modelos_disponibles:
            for intento in range(3):
                try:
                    respuesta = self.client.models.generate_content(
                        model=modelo,
                        contents=contenido_actual,
                        config=types.GenerateContentConfig(
                            system_instruction=self.instrucciones_sistema,
                            temperature=0.1,
                        )
                    )
                    # Guardamos ambos turnos en el historial solo si tuvo éxito
                    self.historial = contenido_actual + [
                        types.Content(role="model", parts=[types.Part.from_text(text=respuesta.text)])
                    ]
                    return respuesta.text

                except Exception as e:
                    error_str = str(e)
                    # Si es saturación (503) o límite por minuto (429), espera y reintenta
                    if "503" in error_str or "429" in error_str:
                        espera = 2 * (intento + 1)
                        print(f"[Servidor saturado en {modelo}, reintentando en {espera}s...]")
                        time.sleep(espera)
                    else:
                        # Si el modelo no existe o no está habilitado (404/403), salta al siguiente modelo
                        break

        return "[Error]: Todos los modelos están saturados temporalmente. Intenta de nuevo en unos segundos."