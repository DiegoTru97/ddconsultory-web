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
        contacto_info = datos.get('contacto_info')  # RECUPERAMOS EL CAMPO DE CONTACTO
        mensaje = datos.get('mensaje')

        # Validamos que nos manden lo importante
        if not nombre or not mensaje or not contacto_info:
            return jsonify(
                {"status": "error", "message": "Faltan datos obligatorios (Nombre, Contacto o Mensaje)."}), 400

        # La URL secreta que te dio Formspree
        formspree_url = os.environ.get('FORMSPREE_URL')

        if not formspree_url:
            print(f"SIMULACIÓN: No se configuró FORMSPREE_URL. Mensaje de {nombre} ({contacto_info})")
            return jsonify({"status": "success", "message": "Simulado (Falta URL de Formspree)"}), 200

        print(f"Enviando solicitud a Formspree para {nombre}...")

        # Preparamos los datos EXACTAMENTE como quieres que se lean en tu correo
        data_to_send = {
            "Nombre_del_Cliente": nombre,
            "Servicio_de_Interes": servicio,
            "Medio_de_Contacto": contacto_info,  # AHORA SÍ LO ENVIAMOS A FORMSPREE
            "Mensaje": mensaje,
            "_subject": f"DDConsultory - Interés en {servicio} ({nombre})"
        }

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