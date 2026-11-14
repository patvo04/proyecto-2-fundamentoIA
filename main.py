from bot import AsistenteMinecraft
from prolog_conect import responder_prolog


def iniciar():
    opcion = input('Motor (1 = Prolog; 2 = Gemini): ').strip()
    if opcion not in ('1','2'):
        print('Opción no válida.'); return
    bot = AsistenteMinecraft() if opcion == '2' else None
    print("===================================================")
    print("  Bienvenido al Chatbot de Crafteo de Minecraft    ")
    print("Puedes preguntarme cosas como:")
    print(" - ¿Cómo hago el pico de hierro?")
    print(" - ¿Para qué sirve la espada de diamante?")
    print(" - ¿Qué materiales necesito en total para una antorcha?")
    print(" - salir")
    print("---------------------------------------------------")
    while True:
        pregunta = input('Tú: ').strip()
        if pregunta.lower() in ('salir','exit','quit'): break
        if not pregunta: continue
        try:
            respuesta = responder_prolog(pregunta)['respuesta'] if opcion == '1' else bot.responder(pregunta)
            print('Chatbot:',respuesta)
        except (RuntimeError, ValueError) as exc:
            print('Error:', exc)

if __name__ == '__main__':
    iniciar()