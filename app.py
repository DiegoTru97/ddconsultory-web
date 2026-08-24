import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/enviar_contacto', methods=['POST'])
def contacto():
    print("--- NUEVA SOLICITUD DE CONTACTO ---")
    try:
        datos = request.get_json()
        nombre = datos.get('nombre')
        servicio = datos.get('servicio')
        mensaje = datos.get('mensaje')

        if not nombre or not mensaje:
            return jsonify({"status": "error", "message": "Faltan datos obligatorios."}), 400

        # La URL secreta que te dio Formspree (se saca de las variables de entorno)
        formspree_url = os.environ.get('FORMSPREE_URL')

        if not formspree_url:
            print(f"SIMULACIÓN: No se configuró FORMSPREE_URL en Render. Mensaje: {mensaje}")
            return jsonify({"status": "success", "message": "Simulado (Falta URL de Formspree)"}), 200

        print(f"Enviando solicitud a Formspree para {nombre}...")

        # Preparamos los datos para la API
        data_to_send = {
            "name": nombre,
            "servicio": servicio,
            "message": mensaje,
            "_subject": f"DDConsultory - Interés en {servicio}"
        }

        # Enviamos los datos usando HTTP (Puerto 443) en vez de SMTP
        response = requests.post(formspree_url, json=data_to_send)

        if response.status_code == 200:
            print("¡Mensaje enviado a través de Formspree exitosamente!")
            return jsonify({"status": "success", "message": "Mensaje enviado"}), 200
        else:
            print(f"Error en Formspree: {response.text}")
            return jsonify({"status": "error", "message": "Fallo la API de correo"}), 500

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"status": "error", "message": "Error interno del servidor."}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)