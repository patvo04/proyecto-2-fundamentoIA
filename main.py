from bot import AsistenteMinecraft

def iniciar():
    bot = AsistenteMinecraft(
        ruta_justificacion="Justificacion del dominio.txt",
        ruta_conocimiento="minecraft proyecto (1).txt"
    )

    print("===================================================")
    print("  Bienvenido al Chatbot de Crafteo de Minecraft    ")
    print("Puedes preguntarme cosas como:")
    print(" - ¿Cómo hago el pico de hierro?")
    print(" - ¿Para qué sirve la espada de diamante?")
    print(" - ¿Qué materiales necesito en total para una antorcha?")
    print(" - salir")
    print("---------------------------------------------------")

    while True:
        usuario = input("\nTú: ").strip()
        if not usuario:
            continue
        if usuario.lower() in ["salir", "exit", "quit"]:
            print("Chatbot: ¡Hasta luego! Buena suerte en tu mundo de Minecraft.")
            break

        respuesta = bot.responder(usuario)
        print(f"Chatbot: {respuesta}")

if __name__ == "__main__":
    iniciar()