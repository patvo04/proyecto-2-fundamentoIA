""" hace 20 preguntas con las dos implementaciones y exporta resultados reales."""
import csv
import json
import time
from pathlib import Path
from bot import AsistenteMinecraft
from prolog_conect import responder_prolog

BASE = Path(__file__).resolve().parent

def ejecutar_evaluacion():
    preguntas = json.loads((BASE / 'preguntas.json').read_text(encoding='utf-8'))
    bot = AsistenteMinecraft()
    resultados = []
    for item in preguntas:
        pregunta = item['pregunta']
        inicio = time.perf_counter()
        try:
            prolog = responder_prolog(pregunta)
            respuesta_prolog = prolog['respuesta']
            dato_prolog = prolog['datos']
        except Exception as exc:
            respuesta_prolog = f'[ERROR PROLOG] {exc}'
            dato_prolog = ''
        tiempo_prolog = round((time.perf_counter() - inicio)*1000,2)

        bot.reiniciar()  # Todas las preguntas 
        inicio = time.perf_counter()
        respuesta_llm = bot.responder(pregunta)
        time.sleep(5)
        tiempo_llm = round((time.perf_counter() - inicio)*1000,2)

        resultados.append({
            'ID':item['id'], 'Categoria':item['categoria'], 'Pregunta':pregunta,
            'Referencia_esperada':item['esperado_prolog'],
            'Respuesta_Prolog_real':respuesta_prolog,
            'Dato_Prolog_real':dato_prolog,
            'Latencia_Prolog_ms':tiempo_prolog,
            'Respuesta_LLM_real':respuesta_llm,
            'Latencia_LLM_ms':tiempo_llm,
            'Prolog_correcto_1_0':'', 'LLM_correcto_1_0':'',
            'Observaciones':''
        })
        print(f"[{item['id']}/20] Prolog: {respuesta_prolog} | LLM: {respuesta_llm}")

    destino = BASE / 'resultados_evaluacion.csv'
    with destino.open('w',newline='',encoding='utf-8-sig') as archivo:
        writer=csv.DictWriter(archivo,fieldnames=resultados[0].keys(),delimiter=';')
        writer.writeheader();writer.writerows(resultados)
    print('Archivo creado:',destino)
    print('Evalúa manualmente la corrección semántica de cada respuesta en el CSV.')

if __name__ == '__main__':
    ejecutar_evaluacion()