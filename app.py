
from flask import Flask, jsonify, render_template, request
from bot import AsistenteMinecraft
from prolog_conect import responder_prolog

app = Flask(__name__, template_folder=".")

# Mostrar la interfaz web
@app.get("/")
def inicio():
    return render_template("index.html")


# Recibir preguntas desde la interfaz
@app.post("/preguntar")
def preguntar():
    datos = request.get_json(silent=True) or {}
    pregunta = str(datos.get("pregunta", "")).strip()
    motor = datos.get("motor", "prolog")
    if not pregunta or len(pregunta) > 500:
        return jsonify({
            "error": "La pregunta debe tener entre 1 y 500 caracteres."
        }), 400
    if motor not in ("prolog", "llm"):
        return jsonify({"error": "Motor inválido"}), 400
    try:
        if motor == "prolog":
            resultado = responder_prolog(pregunta)
            return jsonify({
                "motor": "prolog",
                **resultado
            })

        respuesta = AsistenteMinecraft().responder(pregunta)

        return jsonify({
            "motor": "llm",
            "respuesta": respuesta
        })
    except Exception as exc:
        app.logger.exception("Error en la consulta")
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    app.run(debug=False)
