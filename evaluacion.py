import csv
import time
from bot import AsistenteMinecraft

# Set de 20 preguntas diseñadas según la base de conocimiento de Prolog
SET_EVALUACION = [
    # --- CATEGORÍA 1: Recetas directas (receta/2) ---
    {"id": 1, "categoria": "Receta directa", "pregunta": "¿Cómo hago el pico_hierro?", "esperado_prolog": "[palo, hierro]"},
    {"id": 2, "categoria": "Receta directa", "pregunta": "¿Cómo crafteo una antorcha?", "esperado_prolog": "[palo, carbon]"},
    {"id": 3, "categoria": "Receta directa", "pregunta": "¿Qué ingredientes directos lleva la mesa_crafteo?", "esperado_prolog": "[madera]"},
    {"id": 4, "categoria": "Receta directa", "pregunta": "¿Cómo hago un horno?", "esperado_prolog": "[piedra]"},
    {"id": 5, "categoria": "Receta directa", "pregunta": "¿Cómo crafteo la espada_diamante?", "esperado_prolog": "[palo, diamante]"},

    # --- CATEGORÍA 2: Utilidad de herramientas y objetos (uso/2) ---
    {"id": 6, "categoria": "Utilidad", "pregunta": "¿Para qué sirve el pico_diamante?", "esperado_prolog": "minar_obsidiana"},
    {"id": 7, "categoria": "Utilidad", "pregunta": "¿Para qué sirve el pico_hierro?", "esperado_prolog": "minar_diamante"},
    {"id": 8, "categoria": "Utilidad", "pregunta": "¿Qué acción cumple la pala_piedra?", "esperado_prolog": "excavar_tierra_rapido"},
    {"id": 9, "categoria": "Utilidad", "pregunta": "¿Para qué sirve el hacha_hierro?", "esperado_prolog": "talar_madera_muy_rapido"},
    {"id": 10, "categoria": "Utilidad", "pregunta": "¿Para qué sirve la azada_diamante?", "esperado_prolog": "arar_tierra_maxima_durabilidad"},
    {"id": 11, "categoria": "Utilidad", "pregunta": "¿Para qué sirve el horno?", "esperado_prolog": "fundir_minerales"},

    # --- CATEGORÍA 3: Cadena recursiva de prerequisitos (requiere_material/2) ---
    {"id": 12, "categoria": "Inferencia recursiva", "pregunta": "¿Qué necesito en total en la cadena de crafteo para hacha_madera?", "esperado_prolog": "[madera, palo]"},
    {"id": 13, "categoria": "Inferencia recursiva", "pregunta": "¿Qué materiales base y componentes requiere la antorcha?", "esperado_prolog": "[carbon, madera, palo]"},
    {"id": 14, "categoria": "Inferencia recursiva", "pregunta": "¿Qué necesito para construir pico_piedra considerando toda su cadena?", "esperado_prolog": "[madera, palo, piedra]"},
    {"id": 15, "categoria": "Inferencia recursiva", "pregunta": "¿Qué materiales requiere espada_diamante en toda su cadena de crafteo?", "esperado_prolog": "[diamante, madera, palo]"},
    {"id": 16, "categoria": "Inferencia recursiva", "pregunta": "¿Qué necesito para hacer un palo?", "esperado_prolog": "[madera]"},

    # --- CATEGORÍA 4: Control de dominio cerrado y casos borde ---
    {"id": 17, "categoria": "Fuera de dominio", "pregunta": "¿Cómo hago un pico_oro?", "esperado_prolog": "No encontrado / fuera de base de conocimiento"},
    {"id": 18, "categoria": "Fuera de dominio", "pregunta": "¿Para qué sirve la armadura_diamante?", "esperado_prolog": "No encontrado / fuera de base de conocimiento"},
    {"id": 19, "categoria": "Variación lingüística", "pregunta": "Necesito saber qué hace una espada de piedra", "esperado_prolog": "combatir_monstruos_mayor_dano"},
    {"id": 20, "categoria": "Clasificación", "pregunta": "¿Es el hierro un material básico según la base de conocimiento?", "esperado_prolog": "Sí (es_material_basico(hierro))"},
]

def ejecutar_evaluacion():
    bot = AsistenteMinecraft(
        ruta_justificacion="Justificacion del dominio.txt",
        ruta_conocimiento="minecraft proyecto (1).txt"
    )

    resultados = []
    print("Iniciando evaluación automática de 20 preguntas...\n")

    for item in SET_EVALUACION:
        # Limpiamos el historial en cada pregunta para evaluar cada consulta de forma independiente
        bot.historial = []

        inicio = time.perf_counter()
        respuesta_llm = bot.responder(item["pregunta"])
        latencia_ms = round((time.perf_counter() - inicio) * 1000, 2)

        print(f"[{item['id']}/20] ({item['categoria']}) {item['pregunta']}")
        print(f"   -> Esperado (Prolog): {item['esperado_prolog']}")
        print(f"   -> Respuesta LLM ({latencia_ms} ms): {respuesta_llm.strip()}\n")

        resultados.append({
            "ID": item["id"],
            "Categoria": item["categoria"],
            "Pregunta": item["pregunta"],
            "Esperado_Prolog": item["esperado_prolog"],
            "Respuesta_LLM": respuesta_llm.replace("\n", " ").strip(),
            "Latencia_LLM_ms": latencia_ms,
            "Coincide_Logica (1/0)": ""  # Columna lista para que marques tu análisis manual
        })

        # Pausa breve de 2 segundos entre consultas para evitar saturar el límite por minuto (RPM) del Free Tier
        time.sleep(2)

    archivo_salida = "resultados_evaluacion.csv"
    with open(archivo_salida, mode="w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=resultados[0].keys(), delimiter=";")
        escritor.writeheader()
        escritor.writerows(resultados)

    print(f"Evaluación completada. Resultados exportados a '{archivo_salida}'.")

if __name__ == "__main__":
    ejecutar_evaluacion()