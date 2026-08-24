import os
import smtplib
from email.message import EmailMessage
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
            print("Error: Datos incompletos enviados por el cliente.")
            return jsonify({"status": "error", "message": "Datos incompletos"}), 400

        # Credenciales seguras (Variables de entorno)
        remitente = os.environ.get('EMAIL_USER')
        password = os.environ.get('EMAIL_PASS')
        destinatario = 'diegotru1230@gmail.com'

        # Si no hay credenciales, simular el envío (para pruebas locales)
        if not remitente or not password:
            print(f"MENSAJE SIMULADO (Faltan credenciales): De {nombre} - {mensaje}")
            return jsonify({"status": "success", "message": "Simulado correctamente."}), 200

        print(f"Preparando correo de {nombre} usando la cuenta {remitente}...")

        # Configurar el correo
        msg = EmailMessage()
        msg['Subject'] = f'Nueva solicitud en DDConsultory: {servicio}'
        msg['From'] = remitente
        msg['To'] = destinatario

        cuerpo_correo = f"""
        ¡Hola Diego! Tienes un nuevo mensaje desde tu sitio web DDConsultory.

        Detalles del cliente:
        ----------------------------------------
        Nombre: {nombre}
        Servicio de interés: {servicio}

        Mensaje del cliente:
        ----------------------------------------
        {mensaje}
        """
        msg.set_content(cuerpo_correo)

        # Enviar el correo conectándose a Gmail
        print("Conectando con smtp.gmail.com...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(msg)
            print("¡Mensaje enviado exitosamente!")

        return jsonify({"status": "success", "message": "Mensaje recibido correctamente"}), 200

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"status": "error", "message": "Hubo un problema al procesar el mensaje."}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)